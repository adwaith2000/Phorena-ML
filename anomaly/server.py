from flask import Flask
from anomaly import find_anomalies
import json
from flask_cors import CORS, cross_origin

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
@cross_origin()
def get_anomalies():
    anomalies=find_anomalies()
    return json.dumps(anomalies)