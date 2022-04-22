from google.cloud import bigquery
from datetime import datetime
import base64, json, sys, os

def pubsub_to_bigq(event, context):
    if event['data'] is None:
        print('Invalid data received: {}'.format(event))
        return

    device_id = event['attributes']['deviceId']
    json_data = base64.b64decode(event['data']).decode('utf-8')

    to_bigquery(os.environ['dataset'], os.environ['table'], json.loads(json_data))

def to_bigquery(dataset, table, document):
   bigquery_client = bigquery.Client()
   dataset_ref = bigquery_client.dataset(dataset)
   table_ref = dataset_ref.table(table)
   table = bigquery_client.get_table(table_ref)
   errors = bigquery_client.insert_rows(table, [document])
   if errors != [] :
      print(errors, file=sys.stderr)
