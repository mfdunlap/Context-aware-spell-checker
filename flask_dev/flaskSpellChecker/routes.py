import requests
from flaskSpellChecker import utils, app
from flask import render_template, request, flash, get_flashed_messages, jsonify
import os, json

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


@app.route('/', methods=['POST'])
def computeMispelledWords():
        """
        This function gets the text in the editor from the web page at https://localhost:5000/ and compute
        backend spell checker.

        output: json of suggestions for the mispelled words
        """

        # Retrieve test
        term = request.form['text']
        print('text: ', term)
        # Index dictionary of misspelled words
        idxDict = dict()
        # Get the misspelled words, the candidates for correction and the indexes of the misspelled words in the text
        candidates, misspelled, idxDict = utils.simpleChecker(term)
        # Get the last mispelled word candidates
        if misspelled:
            last_mispelled = misspelled[len(misspelled)-1]
            last_candidate = candidates[str(last_mispelled)]
            last_candidate = list([c for c in last_candidate])

        # Set json url for results
        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        json_url = os.path.join(SITE_ROOT, "data", "results.json")
        json_data = json.loads(open(json_url).read())
        # Compute
        filtered_dict = [v for v in json_data if term in v]
        #resp = jsonify(last_candidate if misspelled else None)
        resp = jsonify(misspelled)
        resp.status_code = 200
        return resp


"""
@app.route('/', methods=['POST'])
def test():
    if request.method == "POST":
     selected = request.form['text']
     print('selected', selected)
    return render_template('english.html')
"""