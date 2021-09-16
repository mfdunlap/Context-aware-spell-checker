import requests
from flaskSpellChecker import utils, app
from flask import render_template, request

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

