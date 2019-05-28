from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from datetime import datetime
import re
import os

app = Flask(__name__)
app.secret_key = "blackbeltexam"
bcrypt = Bcrypt(app)

#connect to the database with app
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///poke.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
migrate = Migrate(app, db)
