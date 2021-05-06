from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

csrf = CSRFProtect(app)

import os
file_path = os.path.abspath(os.getcwd())+"\mydb.db"

app.config['SECRET_KEY'] = '1b2b031d8067f24a1ea7a11d37238842'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///'+file_path
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from . import routes