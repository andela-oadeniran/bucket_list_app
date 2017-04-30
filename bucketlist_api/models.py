from collections import OrderedDict

from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from passlib.apps import custom_app_context as pwd_context

from bucketlist_api import app, db


class Base(db.Model):
    '''
    Base class for the models. Contains common data
    to The User, Bucketlist and Bucketlist Item
    id: primary key
    date created: date object was created sample format "2017-04-14 10:10:58"
    date modified: date object was modified sample format "2017-04-14 11:10:58"
    '''
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True),
                             default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime(timezone=True), default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())


class User(Base):
    '''
    This model holds data for a single User.
    The user ID, Username and Password_Hash used for verification.
    '''
    username = db.Column(
        db.String(256), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    bucketlists = db.relationship('BucketList',
                                  backref=db.backref('user', lazy='joined'),
                                  cascade='all, delete-orphan', lazy='dynamic'
                                  )

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def hash_password(self):
        # generate a hash for the password
        self.password_hash = pwd_context.encrypt(self.password)
        return self.password_hash

    def verify_password(self, password):
        # check password hash matches password.
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=86400):
        # generate an auth token that lasts for a day.
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        # check token to ascertain validity
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except BadSignature:
            raise ValueError  # invalid token
        except SignatureExpired:
            return None
        return User.query.get(data['id'])

    def as_dict(self):
        return "Hello your username is {} ".format(
            self.username)

    def __repr__(self):
        return {
            "username": self.username
        }


class BucketList(Base):
    '''
    This is the one stop data place for
    a single bucketlist.
    '''
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(256))
    items = db.relationship('BucketListItem',
                            backref=db.backref('bucket_list', lazy='joined'),
                            cascade='all, delete-orphan', lazy='dynamic')

    def __init__(self, bucketlistname, created_by):
        self.name = bucketlistname
        self.created_by = created_by

    def as_dict(self):
        # render the bucketlists
        items = [item.as_dict() for item in self.items.all()]
        return OrderedDict([
            ('id', str(self.id)),
            ('name', str(self.name)),
            ('items', items),
            ('date_created', str(self.date_created)),
            ('date_modified', str(self.date_modified)),
            ('created_by', str(self.created_by))
        ])

    def __repr__(self):
        return '<BucketList {}>'.format(self.name)


class BucketListItem(Base):
    '''
    This is the data center for a single
    item in the bucket list
    '''
    done = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(256))
    bucketlist_id = db.Column(db.Integer, db.ForeignKey(
        'bucket_list.id'))

    def __init__(self, item_name, bucketlist_id):
        self.name = item_name
        self.bucketlist_id = bucketlist_id

    def as_dict(self):
        return {col.name: str(getattr(
            self, col.name))
            for col in self.__table__.columns if col.name != 'bucketlist_id'}

    def __repr__(self):
        return '<BucketListItem {}>'.format(self.name)
