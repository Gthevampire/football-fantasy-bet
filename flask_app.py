import http.client
import json
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = { 'X-Auth-Token': 'fe4c5aaa344a40a78cef8547f5840478' }
    connection.request('GET', '/v2/matches', None, headers )
    response = json.loads(connection.getresponse().read().decode())
    
    return 'Hello from Flask!' + '\n' + response
