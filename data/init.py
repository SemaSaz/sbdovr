from flask import Flask
from my_config import Config

app = Flask(__name__)
app.config.from_object(Config)

from core import views