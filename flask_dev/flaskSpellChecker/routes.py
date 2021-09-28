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
def search():
        """
        This function gets the text in the editor from the web page at https://localhost:5000/ and compute
        backend spell checker.

        output: json of suggestions for the last mispelled word
        """
        # Retrieve test
        term = request.form['q']
        print('term: ', term)
        # Get the mispelled and the candidates
        candidates, misspelled = utils.simpleChecker(term)
        # Get the last mispelled word candidates
        if misspelled:
            last_mispelled = misspelled[len(misspelled)-1]
            print("last mispelled : ", last_mispelled)
            last_candidate = candidates[str(last_mispelled)]
            #print("last candidate : ", candidates[str(last_mispelled)])
            last_candidate = list([c for c in last_candidate])
            print('last candidate : ', last_candidate)


        #print("all mispelled : ", misspelled)
        #print("all candidates : ", candidates)
        
        #corrected_text = term.replace(last_mispelled)
        #json_cand = jsonify(candidates)
        #print(json_cand)
        # Set json url for results
        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        json_url = os.path.join(SITE_ROOT, "data", "results.json")
        json_data = json.loads(open(json_url).read())
        #print (json_data)
        #print (json_data[0])
        # Compute
        filtered_dict = [v for v in json_data if term in v]
        #print(filtered_dict)
        resp = jsonify(last_candidate if misspelled else None)
        print(resp)
        resp.status_code = 200
        return resp
