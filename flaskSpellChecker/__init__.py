from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/websiteText.db'
app.config['SECRET_KEY'] = 'b00716a7c0e15501c1ba3ba0' 

db = SQLAlchemy(app)

from flaskSpellChecker import routes, dictionary
from dictionary import Dictionary

ga = Dictionary('ga')
# en = Dictionary('en')
