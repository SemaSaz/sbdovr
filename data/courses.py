import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired

class Courses(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'courses'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                    sqlalchemy.ForeignKey("users.id"))
    type_of_cours = sqlalchemy.Column(sqlalchemy.Text)
    price = sqlalchemy.Column(sqlalchemy.Float)
    user = orm.relationship('User')


class CoursesForm(FlaskForm):
    type_of_cours = StringField('Название курса', validators=[DataRequired()])
    price = StringField('Цена курса', validators=[DataRequired()])
    submit = SubmitField('Применить')
