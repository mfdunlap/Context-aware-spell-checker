import os
from spellChecker import app
#from flask import Flask, render_template, request
#from flask_sqlalchemy import SQLAlchemy

# Check if the run.py file has executed directly and not imported
if __name__ == "__main__":
    app.run(debug=True)