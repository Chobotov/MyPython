from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = 'my secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:123@localhost/py_blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
manager = LoginManager(app)

from blog_package import models, routes

db.create_all()