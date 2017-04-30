# from bucketlist import db
from flask_restful import abort
from webargs import fields, validate

from bucketlist_api import db


user_reg_login_field = {
    'username': fields.Str(required=True, validate=validate.Length(4)),
    'password': fields.Str(required=True, validate=validate.Length(8))
}

name_field = {
    'name': fields.Str(required=True, validate=validate.Length(10))
}

name_done_field = {
    'name': fields.Str(validate=validate.Length(10)),
    'done': fields.Bool()
}

limit_field = {
    'limit': fields.Int(),
    'page': fields.Int(),
    'q': fields.String()
}


def save(obj):
    # adds a valid instance to the session
    try:
        db.session.add(obj)
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        abort(400, message='Request cannot be handled now')
