import requests
from flaskSpellChecker import utils, app
from flask import render_template, request, flash, get_flashed_messages

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
            flash(f'Text submitted to backend.', category='danger')
        except:
            errors.append("Unable to get text.")
            flash(f'Text was not submitted', category='danger')
    return render_template('english.html', errors=errors, results=results)

