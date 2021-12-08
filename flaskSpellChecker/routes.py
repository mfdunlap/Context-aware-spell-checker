from configparser import ConfigParser
from flask import render_template, request, jsonify, session
from flaskSpellChecker import utils, app, babel
import json
from nltk import util

@babel.localeselector
def get_locale():
    try:
        return session['webTextLang']
    except:
        return 'en'

@app.route('/')
@app.route('/home')
def default_page():
    if not 'spellCheckLang' in session:
        session['spellCheckLang'] = 'en'

    if not 'webTextLang' in session:
        session['webTextLang'] = 'en'

    return render_template('base.html', spellCheckLang=session['spellCheckLang'])

@app.route('/', methods=['POST'])
def computeMispelledWords():
    print(request.accept_languages)
    
    #This function gets the text in the editor from the web page at https://localhost:5000/ and compute
    #backend spell checker.
    #Output: json of suggestions for the misspelled words
    
    if request.method=='POST' :
        
        # Retrieve test
        text = request.form['text']
        print('text: ', text)

        # Index dictionary of misspelled words
        wordIndex = dict()

        #  Get misspelled words with word indexes with context aware utility function
        dictTag = session.get('spellCheckLang', None)
        if dictTag == "ga":
            dictLang = utils.ga
        else:
            dictLang = utils.en

        misspellings, wordIndex = utils.spellCheckText(dictLang, text)
        misspelledWordList = list()
        misspelledWordDict = dict()

        print("misspellings keys: ", list(misspellings.keys()))
        
        for contextedWord in list(misspellings.keys()):
            print("contexted word: ", contextedWord)
            print("misspelled text index: ", wordIndex[contextedWord])
            # Three words: the misspelling is in the middle
            if len(contextedWord.split())>2:
                misspelledWord = contextedWord.split()[1]
            else: misspelledWord = text.split()[wordIndex[contextedWord][0]]
            # Add misspelled word to list of misspellings
            misspelledWordList.append(misspelledWord)
            misspelledWordList.append(wordIndex[contextedWord])
            # Add correction to misspelled word
            misspelledWordDict[misspelledWord] = misspellings[contextedWord]

        resp = jsonify(misspelledWordList if misspelledWordList else None)

        # Save misspelled words
        
        json_path = utils.getResultsPath()
        with open(json_path, "w") as f:
            json.dump(misspelledWordDict, f, default=set_default)

        #resp = jsonify(misspellings.keys)
        print(resp)
        resp.status_code = 200
        return resp


@app.route('/selected', methods=['POST'])
def forwardSuggestions():
    """
    Forward suggestions to front-end for the selected misspelled word
    """
    if request.method == "POST":
     selected = request.form['test']
     print('selected: ', selected)
     #misspelledDict = dict()
     json_path = utils.getResultsPath()


     with open(json_path) as f:
        misspelledDict = json.load(f)
    
        if selected in misspelledDict:
            return jsonify(misspelledDict[selected][:6])
            
    return render_template("base.html")

@app.route('/set_webtext_language', methods=['GET','POST'])
def set_lang():
    if request.method == "POST":
        webTextLang = request.form['langCode']
        session['webTextLang'] = webTextLang
        return jsonify({'Confirmation': 'SUCCESS'})
    return jsonify({'Confirmation': 'FAIL'})

@app.route('/set_checker_language', methods=['GET','POST'])
def set_dictionary():
    if request.method == "POST":
        spellCheckLang = request.form['langCode']
        session['spellCheckLang'] = spellCheckLang
        print('Dictionary', session['spellCheckLang'])
        return jsonify({'Confirmation': 'SUCCESS'})
    return jsonify({'Confirmation': 'FAIL'})  

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError