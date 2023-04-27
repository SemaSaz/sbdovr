import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

class config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    UPLOAD_FOLDER = os.path.join(basedir, 'static/img')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024