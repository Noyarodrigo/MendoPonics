from datetime import datetime
import base64, json, sys, os

def pubsub_reader(event, context):
    if event['data'] is None or event['attributes'] is None or event['attributes']['deviceId'] is None:
        print('Invalid data received: {}'.format(event))
        return

    json_data = base64.b64decode(event['data']).decode('utf-8')
    print(json_data)
