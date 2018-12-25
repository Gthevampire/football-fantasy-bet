import http.client
import json
from flask import render_template

from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title="Hello")

@app.route('/matches')
def matches():
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = { 'X-Auth-Token': 'fe4c5aaa344a40a78cef8547f5840478' }
    connection.request('GET', '/v2/matches', None, headers )
    response = json.loads(connection.getresponse().read().decode())

    connection.close()
    return render_template("matches.html")