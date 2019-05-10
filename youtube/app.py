from flask import Flask
from flask_cors import CORS, cross_origin
import os
from flask_login import LoginManager

app = Flask(__name__)

# when commented we have : "The session is unavailable because no secret was set"
# if uncommented there is another error, probably because it is the wrong way to deal with it
# app.secret_key = os.urandom(24)

# login_manager = LoginManager()
# login_manager.init_app(app)

CORS(app)