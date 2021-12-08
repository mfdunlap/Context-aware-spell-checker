from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b00716a7c0e15501c1ba3ba0' 

from flaskSpellChecker import routes
from flaskSpellChecker._dictionary import Dictionary
