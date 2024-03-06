from flask import Flask
from app.controllers import default

app = Flask(__name__)

app.register_blueprint(default.blueprint)
