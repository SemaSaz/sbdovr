import flask
from flask import jsonify

from . import db_session
from .users import User

blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/user')
def get_user():
    db_sess = db_session.create_session()
    news = db_sess.query(User).all()
    try:
        return jsonify(
            {
                'news':
                    [item.to_dict(only=('id'))
                     for item in news]
            }
        )
    except:
        f = open('id.txt', 'r')
        a = str(f.read())
        return jsonify(
            {
                'news':
                    [a]
            }
        )