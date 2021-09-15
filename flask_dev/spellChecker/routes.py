#from werkzeug.wrappers import request
import requests
from spellChecker import utils, app
from flask import render_template, request

@app.route('/')
@app.route('/home')
@app.route('/eng')
def default_page():
    return render_template('english.html')

@app.route('/submit', methods=['POST'])
def submit():
    results = {}
    errors = []
    if request.method=='POST':
        try:
            text = request.form['message']
            print(text)
            utils.simpleChecker(text)
        except:
            errors.append("Unable to get text.")
        #print(raw)
    #return 'You entered: {}'.format(request.form['message'])
    return render_template('english.html', errors=errors, results=results)

