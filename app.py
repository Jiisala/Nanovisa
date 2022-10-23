from flask import Flask
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
from os import getenv

app = Flask(__name__)

app.secret_key = getenv("SECRET_KEY")
app.config["SESSION_TYPE"] = "filesystem"
csrf = CSRFProtect()
csrf.init_app(app)
Session(app)

import routes
