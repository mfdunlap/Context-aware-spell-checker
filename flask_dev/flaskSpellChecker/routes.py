import requests
from flaskSpellChecker import utils, app
from flask import render_template, request, flash, get_flashed_messages, jsonify
import os, json

json_path = "flask_dev/flaskSpellChecker/data/results.json"

@app.route('/')
@app.route('/home')
@app.route('/english')
def default_page():
    # Set language to UTF-8 code for English
    # Can be tested by looking at viewing source code on page (Ctrl+U)
    language = "en"
    return render_template('english.html', language=language)

@app.route('/french')
def french_page():
    # Set language to UTF-8 code for French
    # Can be tested by looking at viewing source code on page (Ctrl+U)
    language = "fr"
    return render_template('french.html', language=language)

@app.route('/german')
def german_page():
    # Set language to UTF-8 code for German
    # Can be tested by looking at viewing source code on page (Ctrl+U)
    language = "de"
    return render_template('german.html', language=language)

@app.route('/portuguese')
def portuguese_page():
    # Set language to UTF-8 code for Portuguese
    # Can be tested by looking at viewing source code on page (Ctrl+U)
    language = "pt"
    return render_template('portuguese.html', language=language)

@app.route('/spanish')
def spanish_page():
    # Set language to UTF-8 code for Spanish
    # Can be tested by looking at viewing source code on page (Ctrl+U)
    language = "es"
    return render_template('spanish.html', language=language)
    
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
    print(request.accept_languages)
    
    #This function gets the text in the editor from the web page at https://localhost:5000/ and compute
    #backend spell checker.

    #output: json of suggestions for the misspelled words
    
    if request.method=='POST' :
        
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
        #SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        #json_url = os.path.join(SITE_ROOT, "data", "results.json")
        #json_data = json.loads(open(json_url).read())
        # Compute
        #filtered_dict = [v for v in json_data if term in v]
        #resp = jsonify(last_candidate if misspelled else None
    
        # Save misspelled words
        with open(json_path, "w") as f:
            json.dump(candidates, f, default=set_default)

        resp = jsonify(misspelled)
        print(resp)
        #resp = jsonify(misspelled)
        #resp.status_code = 200
        return resp


@app.route('/selected', methods=['POST'])
def forwardSuggestions():
    """
    Forward suggestions to front-end for the selected misspelled word
    """
    if request.method == "POST":
     selected = request.form['test']
     print('selected', selected)
     misspelledDict = dict()
     with open(json_path) as f:
        misspelledDict = json.load(f)
    
        if selected in misspelledDict:
            #print(misspelledDict[selected])
            return jsonify(misspelledDict[selected][:6])
            
    return render_template("base.html")


def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError