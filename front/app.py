import os
import pathlib

import requests
from functools import wraps
from flask import Flask, session, abort, redirect, request, render_template
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from google.cloud import bigquery
from google.cloud import iot_v1
from google.cloud import pubsub_v1

import base64, json
import datetime

app = Flask("Google Login App")
#app.config.from_pyfile('/app/src/config/config.txt')
app.config.from_pyfile('config/config.txt')

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = app.config['GOOGLE_CLIENT_ID']
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "config/client_secret.json")
credentials_path = 'config/mendoponics-privatekey.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:8000/callback"
)

def login_is_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return redirect('/login')
            #return abort(401)  # Authorization required
        else:
            return f(*args, **kwargs)
    return wrapper


@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID,
        clock_skew_in_seconds=1
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session["email"] = id_info.get("email")

    return redirect("/home")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/")
def index():
    return redirect('/login')
    #return "Hello World <a href='/login'><button>Login</button></a>"

@app.route("/home")
@login_is_required
def home():
    #get devices with the owner email
    bq_client = bigquery.Client(project='mendoponics')

    query = "SELECT * FROM `mendoponics.main.devices`\
            WHERE owner = '"+ str(session["email"]) + \
            "' LIMIT 100"
    query_job = bq_client.query(query)  # Make an API request.
    result = query_job.result()
    devices = []
    for row in result:
        devices.append(row[0])
    devices_str= '(\'' +'\',\''.join(devices)+'\')'

    #get the configuration from the previous devices list
    query2 = "SELECT * FROM `mendoponics.main.configurations`\
            WHERE deviceid in "+ devices_str + \
            " LIMIT 100"
    query_job2 = bq_client.query(query2)  # Make an API request.
    result2 = query_job2.result()
    configurations_to_send = []
    for row in result2:
        configuration_dict = {}
        configuration_dict['timestamp'] = row[0]
        configuration_dict['sunrise'] = row[1]
        configuration_dict['sunset'] = row[2]
        configuration_dict['pump_interval'] = row[3]
        configuration_dict['pump_timeon'] = row[4]
        configuration_dict['deviceid'] = row[5]
        configuration_dict['location'] = row[6]
        configuration_dict['registry'] = row[7]
        configuration_dict['description'] = row[8]
        configurations_to_send.append(configuration_dict)
    return render_template('user.html', configurations = configurations_to_send)


@app.route("/user/handler",methods=['GET','POST'])
@login_is_required
def user_handler():
    if request.method == 'GET':
        arg_data = request.args
        if '_method' in arg_data and arg_data['_method'] == '_UPDATE':
            bq_client = bigquery.Client(project='mendoponics')
            query3 = "SELECT * FROM `mendoponics.main.configurations`\
                    WHERE deviceid = '"+ str(arg_data['deviceid']) + \
                    "' LIMIT 1"
            query_job3 = bq_client.query(query3)  # Make an API request.
            result3 = query_job3.result()
            configuration_dict = {}
            for row in result3:
                configuration_dict['sunrise'] = row[1]
                configuration_dict['sunset'] = row[2]
                configuration_dict['pump_interval'] = row[3]
                configuration_dict['pump_timeon'] = row[4]
                configuration_dict['location'] = row[6]
                configuration_dict['registry'] = row[7]
                configuration_dict['description'] = row[8]
                configuration_dict['location'] = row[6]
                configuration_dict['registry'] = row[7]
                configuration_dict['deviceid'] = str(arg_data['deviceid'])
            return render_template('alterdevice.html',data=configuration_dict)

    if request.method == 'POST':
        form_data = request.form
        #modify logic/query
        bq_client = bigquery.Client(project='mendoponics')

        query4 = "UPDATE `mendoponics.main.configurations`\
                SET sunrise ="+ form_data['sunrise'] + ", sunset ="+ form_data['sunset'] + ", pump_interval = " + form_data['pump_interval']\
                + ", pump_timeon = " + form_data['pump_timeon'] + ", timestamp ='" + str(datetime.datetime.now()) + \
                "' , description = '" + form_data['description'] + "' WHERE deviceid = '"+ str(form_data['deviceid']) + "'"
        query_job4 = bq_client.query(query4)  # Make an API request.
        result4 = query_job4.result()

        publisher = pubsub_v1.PublisherClient()

        #messages are formated in json in the same way that the esp8266 send them
        #that's why keys are different in this case, like deviceRegistryId instead of just registry
        #this way there's no need to modify variables in the function that is subscribed to the topic
        msg = {'command':'connected',
                'deviceId': str(form_data['deviceid']),
                'deviceRegistryLocation': str(form_data['location']),
                'deviceRegistryId': str(form_data['registry'])}
        data = json.dumps(msg).encode("utf-8")
        topic_path = publisher.topic_path('mendoponics', 'main')
        future = publisher.publish(topic_path, data)
        return redirect('/home')
        #return render_template('alterdevice.html',data=arg_data)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.getenv('PORT'),debug=True)