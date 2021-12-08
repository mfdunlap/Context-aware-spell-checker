import os
from flask import Flask
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
babel = Babel(app)

app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = os.path.join(os.getcwd(), "translations")
app.config['SECRET_KEY'] = 'b00716a7c0e15501c1ba3ba0' 

from flaskSpellChecker import routes
from flaskSpellChecker.dictionary import Dictionary

#ga = Dictionary('ga',100)
# en = Dictionary('en')
