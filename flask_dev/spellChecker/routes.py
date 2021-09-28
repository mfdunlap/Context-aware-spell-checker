#from werkzeug.wrappers import request
import requests
from spellChecker import utils, app
from flask import render_template, request
from flask import Flask, jsonify, request, redirect, render_template
import os, json

"""
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
"""
"""
@app.route("/", methods=["POST", "GET"])
def home():
	if request.method == "GET":
		languages = ["C++", "Python", "PHP", "Java", "C", "Ruby",
					"R", "C#", "Dart", "Fortran", "Pascal", "Javascript"]
		
		return render_template("index.html", languages=languages)
"""

@app.route('/')
def default_page():
	return render_template('english.html')

@app.route('/submit', methods=['POST'])
def submit():
    results = {}
    errors = []
    #if request.method=='POST':
    #    try:
    #        text = request.form['message']
            #print(text)
            #utils.simpleChecker(text)
    #    except:
    #        errors.append("Unable to get text.")
        #print(raw)
    #return 'You entered: {}'.format(request.form['message'])
    return render_template('english.html', errors=errors, results=results)

@app.route('/search', methods=['POST'])
def search():
    
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