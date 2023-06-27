from google.cloud import bigquery
from google.cloud import iot_v1
from datetime import datetime
import base64, json, sys, os


def actuator_handler(event, context):
    if event['data'] is None:
        print('Invalid data received: {}'.format(event))
        return

    attributes = event['attributes']

    json_data = base64.b64decode(event['data']).decode('utf-8')

    if "pump" in json_data:
        #tabla hardcodeada
        to_bigquery(os.environ['dataset'], pumpstatus, json.loads(json_data))

    elif "light" in json_data:
        #tabla hardcodeada
        to_bigquery(os.environ['dataset'], lightstatus, json.loads(json_data))

    else:
        print('Invalid acttuator data received: {}'.format(event))
        return

def to_bigquery(dataset, table, document):
   print("Saving data")
   bigquery_client = bigquery.Client()
   dataset_ref = bigquery_client.dataset(dataset)
   table_ref = dataset_ref.table(table)
   table = bigquery_client.get_table(table_ref)
   errors = bigquery_client.insert_rows(table, [document])
   if errors != [] :
      print(errors, file=sys.stderr)
