import http.client
import json

from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title="Hello")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/matches')
def matches():
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = { 'X-Auth-Token': 'fe4c5aaa344a40a78cef8547f5840478' }
    connection.request('GET', '/v2/matches', None, headers )
    response = json.loads(connection.getresponse().read().decode())

    connection.close()
    return render_template("matches.html")
