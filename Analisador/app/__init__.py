from flask import Flask, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
app.config['SITES_OBJECT'] = {}
# db = SQLAlchemy(app)



