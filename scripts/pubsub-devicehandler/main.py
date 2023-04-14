from google.cloud import bigquery
from google.cloud import iot_v1
from datetime import datetime
import base64, json, sys, os


def device_handler(event, context):
    if event['data'] is None:
        print('Invalid data received: {}'.format(event))
        return

    attributes = event['attributes']

    json_data = base64.b64decode(event['data']).decode('utf-8')

    if "connected" in json_data:
        if attributes is None or attributes == '':
            conf_device(json.loads(json_data))
        else:
            conf_device(attributes)
        return
    to_bigquery(os.environ['dataset'], os.environ['table'], json.loads(json_data))

def to_bigquery(dataset, table, document):
   print("Saving data")
   bigquery_client = bigquery.Client()
   dataset_ref = bigquery_client.dataset(dataset)
   table_ref = dataset_ref.table(table)
   table = bigquery_client.get_table(table_ref)
   errors = bigquery_client.insert_rows(table, [document])
   if errors != [] :
      print(errors, file=sys.stderr)

def conf_device(attributes):
    print('attr: ', attributes)
    print(f"Device {attributes['deviceId']} connected, sending configuration")
    client = iot_v1.DeviceManagerClient()
    device_path = client.device_path('mendoponics-383115',attributes['deviceRegistryLocation'], attributes['deviceRegistryId'], attributes['deviceId'])

    bq_client = bigquery.Client()

    query = "SELECT * FROM `mendoponics-383115.main.configurations`\
            WHERE deviceid = '"+ str(attributes['deviceId']) + \
            "' LIMIT 1"
    query_job = bq_client.query(query)  # Make an API request.
    result = query_job.result()
    for row in result:
        data = row
    data_dict = {'timestamp': str(data['timestamp']),
            'sunrise': data['sunrise'],
            'sunset':data['sunset'],
            'pump_interval':data['pump_interval'],
            'pump_timeon':data['pump_timeon']
            }
    payload = json.dumps(data_dict)
    print('payload: ',payload)
    return client.send_command_to_device(request={"name": device_path, "binary_data": payload.encode('utf-8')})
