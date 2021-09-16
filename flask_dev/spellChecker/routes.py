from werkzeug.wrappers import request
from spellChecker import app
from flask import render_template

@app.route('/')
@app.route('/home')
@app.route('/english')
def default_page():
    return render_template('english.html')

@app.route('/french')
def french_page():
    return render_template('french.html')

@app.route('/german')
def german_page():
    return render_template('german.html')

@app.route('/portuguese')
def portuguese_page():
    return render_template('portuguese.html')

@app.route('/spanish')
def spanish_page():
    return render_template('spanish.html')
