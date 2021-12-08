from werkzeug.datastructures import ContentSecurityPolicy
from flaskSpellChecker import utils, app
from flask import render_template, request, jsonify
import json
from flaskSpellChecker import utils

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

@app.route('/irish')
def irish_page():
    # Set language to UTF-8 code for Irish
    # Can be tested by looking at viewing source code on page (Ctrl+U)
    language = "ga"
    return render_template('irish.html', language=language)

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
        misspellings, wordIndex = utils.spellCheckText(utils.en, text)
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


def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError