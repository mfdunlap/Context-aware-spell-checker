from configparser import ConfigParser
from flask import render_template, request, jsonify
from flaskSpellChecker import utils, app, babel
import json
from nltk import util

@babel.localeselector
def get_locale():
    return 'ga'
    #return request.accept_languages.best_match(['de', 'en', 'es', 'fr', 'ga', 'pt'])

@app.route('/')
@app.route('/home')
def default_page():
    spellCheckLang = "en"
    return render_template('base.html', spellCheckLang=spellCheckLang)

@app.route('/', methods=['POST'])
def computeMispelledWords():
    print(request.accept_languages)
    
    #This function gets the text in the editor from the web page at https://localhost:5000/ and compute
    #backend spell checker.
    #Output: json of suggestions for the misspelled words
    
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
        json_path = utils.getResultsPath()
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
     json_path = utils.getResultsPath()


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