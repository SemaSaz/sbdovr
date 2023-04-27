from flask import render_template,flash,request,redirect
from core import app
from werkzeug.utils import secure_filename
from config import Config
import os

@app.route('/', methods=['POST','GET'])
def index():
    greeting="Hello there, Ace"

    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            flash('No file was selected')
            return redirect(request.url)
        elif file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(Config.UPLOAD_FOLDER, filename))
            flash('Image has been successfully uploaded')
            return redirect('/')
        else:
            flash('Allowed media types are - png, jpg, jpeg, gif')
            return redirect(request.url)
    else:
        return render_template('index.html', greet=greeting)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS
