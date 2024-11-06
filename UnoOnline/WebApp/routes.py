from WebApp import app
from flask import render_template
# from scripts import load_in

@app.route('/')
@app.route('/index')
def index():
    user = {'username':'Test User'}
    return render_template('index.html',title='Uno Online',user = user)