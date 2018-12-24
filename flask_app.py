import http.client
import json
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    connection = http.client.HTTPConnection('www.python.org')
    
    connection.request('GET', '/' )
    response = connection.getresponse()
    connection.close()
    return 'Hello from Flask!' + '\n' + str(response)
