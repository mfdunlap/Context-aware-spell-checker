from werkzeug.wrappers import request
from spellChecker import app
from flask import render_template

@app.route('/')
@app.route('/home')
@app.route('/eng')
def default_page():
    return render_template('english.html')