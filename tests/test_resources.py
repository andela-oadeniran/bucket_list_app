import json
from flask_testing import TestCase

from tests import config, app, db, BucketList, BucketListItem


class BucketListResource(TestCase):
    '''
    The test suite for the bucket list bucket list api
    POST : To create a new Bucket List
    GET : To retrieve the list of all Bucket Lists
    GET : Retrieve a single bucket list
    PUT: To update a single bucket list.
    DELETE: To remove a bucket List
    '''

    @staticmethod
    def init_db():
        db.drop_all()
        db.create_all()

    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    def setUp(self):
        app = self.create_app()
        self.app = app.test_client()
        with app.app_context():
            self.init_db()
        self.req = ({'username': 'marcus', 'password': 'polymath'})
        self.bucketlist_url = '/api/v1/bucketlists/'

    def reg_user(self):
        self.app.post('/api/v1/auth/register', data=self.req)

    def login_user(self):
        resp = json.loads((
            self.app.post('/api/v1/auth/login', data=self.req).data))
        return resp.get('token')

    def tearDown(self):
        db.session.remove()
        db.session.close()

    def test_bl_table_initially_empty(self):
        query = db.session.query(BucketList).all()
        assert not query

    def test_bucketlist_created_got_successfully(self):
        # Should return valid for an invalid input
        req = {'name': 'Before I turn 50'}
        self.reg_user()
        self.token = self.login_user()
        res = self.app.post(
            self.bucketlist_url, data=req, headers={'Token': self.token})
        assert res.status_code == 201
        assert json.loads(res.data).get('created_by') == '1'
        assert 'Before I Turn 50' in (json.loads(res.data)).get('name')
        assert 'Before I Turn 50' in BucketList.query.get(1).name
        # get the bucketlist added
        res = self.app.get(
            '/api/v1/bucketlists/1',
            headers={'Token': self.token})
        assert res.status_code == 200
        assert 'Before I Turn 50' in (json.loads(res.data)).get('name')
        # get all the bucketlists
        req = {'name': 'Before December'}
        self.app.post(
            self.bucketlist_url, data=req, headers={'Token': self.token})
        res = self.app.get(
            self.bucketlist_url, headers={'Token': self.token, 'limit': 1})
        assert res.status_code == 200

        res = self.app.get(
            self.bucketlist_url, headers={
                'Token': self.token, 'q': 'December'})
        assert res.status_code == 200

    def test_invalid_params_post_method(self):
        #
        req = {'name': 'Before I turn 50'}
        self.reg_user()
        self.token = self.login_user()
        res = self.app.post(
            '/api/v1/bucketlists/1', data=req, headers={'Token': self.token})
        assert res.status_code == 405
        assert not BucketList.query.get(1)
        req = {'name': '          '}
        res = self.app.post(
            '/api/v1/bucketlists/', data=req, headers={'Token': self.token})
        assert res.status_code == 400

    def test_existing_bucketlist_with_current_user(self):
        #
        req = {'name': 'Before I turn 60'}
        self.reg_user()
        self.token = self.login_user()
        self.app.post(
            '/api/v1/bucketlists/', data=req, headers={'Token': self.token})
        req = {'name': 'Before I turn 60'}
        self.reg_user()
        self.token = self.login_user()
        res = self.app.post(
            '/api/v1/bucketlists/', data=req, headers={'Token': self.token})
        assert res.status_code == 400
        assert 'Bucket List name already exists' in (
            json.loads(res.data)).get('message')

    def test_put_delete_bucketlist(self):
        req = {'name': 'Before Marriage'}
        self.reg_user()
        token = self.login_user()
        self.app.post(
            '/api/v1/bucketlists/', data=req, headers={'Token': token})
        req = {'name': 'Before January'}
        res = self.app.put(
            '/api/v1/bucketlists/1', data=req, headers={'Token': token})
        assert res.status_code == 200
        assert 'Before January' in (json.loads(res.data)).get('name')
        assert BucketList.query.get(1).name == 'Before January'
        res = self.app.delete(
            '/api/v1/bucketlists/1', headers={'Token': token})
        assert res.status_code == 200

    def test_invalid_delete_put_params(self):
        req = {'name': 'Before January'}
        self.reg_user()
        token = self.login_user()
        self.app.post(
            '/api/v1/bucketlists/', data=req, headers={'Token': token})
        req = {'name': 'Before January'}
        res = self.app.put(
            '/api/v1/bucketlists/', data=req, headers={'Token': token})
        assert res.status_code == 405
        res = self.app.delete(
            '/api/v1/bucketlists/', headers={'Token': token})
        assert res.status_code == 405
        #
        req = {'name': 'Before January'}
        res = self.app.put(
            '/api/v1/bucketlists/1', data=req, headers={'Token': token})
        assert res.status_code == 400
        assert 'Bucket List name already exists' in (
            json.loads(res.data)).get('message')
        req = {'name': 'Before     '}
        res = self.app.put(
            '/api/v1/bucketlists/1', data=req, headers={'Token': token})
        assert res.status_code == 400


class BucketListItemResource(TestCase):
    '''
    '''
    @staticmethod
    def init_db():
        db.drop_all()
        db.create_all()

    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    def setUp(self):
        app = self.create_app()
        self.app = app.test_client()
        with app.app_context():
            self.init_db()
        self.user = ({'username': 'marcus', 'password': 'polymath'})
        self.bucketlist = ({'name': 'Before the end of the Year'})
        self.item_url = '/api/v1/bucketlists/1/items/'

    def tearDown(self):
        db.session.remove()
        db.session.close()

    def reg_user(self):
        self.app.post('/api/v1/auth/register', data=self.user)

    def login_user(self):
        resp = json.loads((
            self.app.post('/api/v1/auth/login', data=self.user).data))
        self.token = resp.get('token')
        return self.token

    def post_bucketlist(self):
        self.app.post('/api/v1/bucketlists/',
                      data=self.bucketlist, headers={'Token': self.token})

    def test_bucketlist_item(self):
        self.reg_user()
        self.login_user()
        self.post_bucketlist()
        #
        req = {'name': 'Learn Python'}
        res = self.app.post('/api/v1/bucketlists/1/items/1',
                            data=req, headers={'Token': self.token})
        assert res.status_code == 405
        res = self.app.post('/api/v1/bucketlists/2/items/',
                            data=req, headers={'Token': self.token})
        assert res.status_code == 404
        req = {'name': '          learn'}
        res = self.app.post('/api/v1/bucketlists/1/items/',
                            data=req, headers={'Token': self.token})
        assert res.status_code == 400
        req = {'name': 'Learn Python'}
        res = self.app.post('/api/v1/bucketlists/1/items/',
                            data=req, headers={'Token': self.token})
        assert res.status_code == 201
        res = self.app.post('/api/v1/bucketlists/1/items/',
                            data=req, headers={'Token': self.token})
        assert res.status_code == 400
        assert 'item name already exists' in (
            json.loads(res.data)).get('message')
        #
        req = {'name': 'Learn JavaScript'}
        res = self.app.put('/api/v1/bucketlists/1/items/',
                           data=req, headers={'Token': self.token})
        assert res.status_code == 405
        res = self.app.put('/api/v1/bucketlists/2/items/1',
                           data=req, headers={'Token': self.token})
        assert res.status_code == 404
        req = {'name': 'Learn          '}
        res = self.app.put('/api/v1/bucketlists/1/items/1',
                           data=req, headers={'Token': self.token})
        assert res.status_code == 400
        req = {'name': 'Learn JavaScript'}
        res = self.app.put('/api/v1/bucketlists/1/items/1',
                           data=req, headers={'Token': self.token})
        res.status_code == 201
        req = {'done': 'True'}
        res = self.app.put('/api/v1/bucketlists/1/items/1',
                           data=req, headers={'Token': self.token})
        assert res.status_code == 201
        res = self.app.delete('/api/v1/bucketlists/1/items/',
                              headers={'Token': self.token})
        assert res.status_code == 405
        res = self.app.delete('/api/v1/bucketlists/1/items/2',
                              headers={'Token': self.token})
        assert res.status_code == 404
        res = self.app.delete('/api/v1/bucketlists/1/items/1',
                              headers={'Token': self.token})
        assert res.status_code == 200





