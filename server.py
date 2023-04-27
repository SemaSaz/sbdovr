import os.path

from flask import render_template, flash, request, redirect, url_for
import os

from flask import Flask, flash, request, redirect, url_for
# объясняется ниже
from werkzeug.utils import secure_filename
from data.my_config import config
# папка для сохранения загруженных файлов
UPLOAD_FOLDER = 'static/img'
# расширения файлов, которые разрешено загружать
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
from werkzeug.utils import secure_filename
from config import Config
import os
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, request, abort, jsonify, send_from_directory
from data import db_session
from data.loginfrom import LoginForm
from data.users import User
from data.courses import Courses, CoursesForm
from flask_login import LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired
from flask_login import login_user
from data.users import RegisterForm
import requests
from flask_restful import reqparse, abort, Api, Resource
from data import db_session,  users_api
from flask import make_response


name_us = ''
app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/product')
def prod():
    return render_template('product.html')

@app.route('/handledata', methods=['POST'])
def handle_data():
    projectpath = request.form['projectFilepath']


@app.route('/cont')
def contact():
    return render_template('Contact.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    file = request.files['file']
    filename = file.filename
    # сохраняем файл на сервере или обрабатываем его каким-то другим способом
    return 'Файл {} загружен на сервер!'.format(filename)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/cab', methods=['POST'])
def cab():
    projectpath = request.form['projectFilepath']
    return render_template('cab.html')


@app.route('/display')
def display():
    try:
        return app.send_static_file("uploaded_image.png")
    except:
        return app.send_static_file("1.jpg")


@app.route('/')
@app.route('/home')
def index():
    f = open('1.txt', 'r')
    a = f.read()
    print(type(a))
    # user = User()
    # user.name = "Пользователь 1"
    # user.about = "биография пользователя 1"
    # user.email = "email@email.ru"
    # db_sess = db_session.create_session()
    return render_template('HomePage.html',my=a)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        global name_us
        name_us = str(user)
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            x = open('id.txt', 'w')
            x.write(str(current_user.id))
            x.close()
            return redirect("/home")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/reg', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            email=form.email.data,
        )
        print(form.email.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/cabinet', methods=['GET', 'POST'])
@login_required
def cabinet():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            db_sess = db_session.create_session()
            items = db_sess.query(User).filter(User.id == current_user.id
                                                ).first()
            file.save(os.path.join(UPLOAD_FOLDER, str(items.id) + '.jpg'))
    else:
        db_sess = db_session.create_session()
        courses = db_sess.query(User).filter(User.id == current_user.id
                                                ).first()
        filename = f'{courses.id}.jpg'
    return render_template('lich.html', filename=filename)


# @app.route('/show/<filename>')
# def uploaded_file(filename):
#     filename = 'http://127.0.0.1:5000/uploads/' + filename
#     return render_template('lich.html', filename=filename)
#
#
# @app.route('/uploads/<filename>')
# def send_file(filename):
#     return send_from_directory(UPLOAD_FOLDER, filename)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def allowed_file(filename):
    """ Функция проверки расширения файла """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS





@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', num=404)


@app.errorhandler(500)
def oshibka(error):
    return render_template('404.html', num=404)
@app.errorhandler(400)
def badrequest():
    return render_template('404.html', num=404)


if __name__ == '__main__':
    db_session.global_init("db/courses.db")
    app.register_blueprint(users_api.blueprint)
    # api.add_resource(jobs_resources.JobsListResource, '/api/v2/jobs')
    # api.add_resource(jobs_resources.JobsResource, '/api/v2/jobs/<int:jobs_id>')
    app.run(port=8083, host='127.0.0.1')
