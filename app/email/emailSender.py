import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
import base64, json
from datetime import datetime

class EmailHandler:
    def __init__(self) -> None:
        credentials_path = 'config/mendoponics-privatekey.json'
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

        self.project_id = os.getenv('project_id')
        self.subscription_id = os.getenv('subscription_id')
        self.fromaddr = os.getenv('fromaddr')
        self.password = os.getenv('password')

        # Number of seconds the subscriber should listen for messages
        #self.timeout = 5.0


        self.subscriber = pubsub_v1.SubscriberClient()
        # The `subscription_path` method creates a fully qualified identifier
        # in the form `projects/{project_id}/subscriptions/{subscription_id}`
        self.subscription_path = self.subscriber.subscription_path(self.project_id, self.subscription_id)

    def sendmail(self, data: dict) -> None:
        date = datetime.fromtimestamp(data['timestamp'])
        date_formatted = date.strftime("%m/%d/%Y, %H:%M:%S")
        toaddr = data['email']

        port = 465

        try:
            msg = MIMEMultipart()
            msg['Subject'] = 'MendoPonics defense system'
            msg['From'] = self.fromaddr
            msg['To'] = toaddr

            mensaje = ("\n> WARNING! <\nOne of your hydroponic system sent an alert!\n\n"
                    "Date: {}\nDevice: {}\nError: {}").format(date_formatted,data['deviceid'],data['message'])
            text = MIMEText(mensaje)
            msg.attach(text)
            
        except:     
            print("Error cabeceras")

        context = ssl.create_default_context()
      
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(self.fromaddr, self.password)
            server.sendmail(self.fromaddr, toaddr, msg.as_string())
            print("\n\n---------------------------------\nALERT SENT!\n------------------------------")

    def callback(self, message: pubsub_v1.subscriber.message.Message) -> None:
        #message is an object, so we muest acces data "properties" and decode 'em
        data = json.loads(message.data.decode('utf-8'))
        message.ack()
        self.sendmail(data)

    def start_subscriber(self) -> None:
        streaming_pull_future = self.subscriber.subscribe(self.subscription_path, callback=self.callback)
        print(f"Listening for messages on {self.subscription_path}..\n")
        # Wrap subscriber in a 'with' block to automatically call close() when done.
        with self.subscriber:
            try:
                # When `timeout` is not set, result() will block indefinitely,
                # unless an exception is encountered first.
                streaming_pull_future.result()
                #streaming_pull_future.result(timeout=timeout)
            except TimeoutError:
                streaming_pull_future.cancel()  # Trigger the shutdown.
                streaming_pull_future.result()  # Block until the shutdown is complete.

if __name__ == '__main__':
    email_handler = EmailHandler()
    email_handler.start_subscriber()
