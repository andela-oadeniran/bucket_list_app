from flask_testing import TestCase
import json

from tests import app, config, db, User


class TestRegLogin(TestCase):
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
        self.reg_url = '/api/v1/auth/register'
        self.login_url = '/api/v1/auth/login'
        self.bucketlist_url = '/api/v1/bucketlists'

    def tearDown(self):
        db.session.remove()
        db.session.close()
        # os.unlink(app.config['SQLALCHEMY_DATABASE_URI'])

    def test_db_initially_empty(self):
        query = db.session.query(User).all()
        assert not query

    def test_home(self):
        resp = self.app.get('/')
        assert resp.status_code == 200

    def test_username_field_required(self):
        req = ({'password': 'No username'})
        resp = self.app.post(self.reg_url, data=req)
        # assert 'Missing data in required field' in str(resp.data)
        assert resp.status_code == 422

    def test_password_field_required(self):
        req = ({'username': 'no_password'})
        resp = self.app.post(self.reg_url, data=req)
        #
        assert resp.status_code == 422

    def test__bad_short_required_input(self):
        req = ({'username': 'tes   ', 'password': '          '})
        resp = self.app.post(self.reg_url, data=req)
        #
        assert resp.status_code == 400

    def test_user_added_status(self):
        # status code should be 201 for user created
        req = ({'username': 'Adebayo', 'password': 'andela007'})
        resp = self.app.post(self.reg_url, data=req)
        assert resp.status_code == 201

    def test_user_added_to_db_successfully(self):
        # test user present in data base
        req = ({'username': 'Adebayo', 'password': 'andela007'})
        self.app.post(self.reg_url, data=req)
        user = User.query.get(1)
        assert user.username == "Adebayo"

    def test_user_duplicate_status_code(self):
        # status code should be 400 for an existing user
        req = ({'username': 'Adebayo', 'password': 'andela007'})
        self.app.post(self.reg_url, data=req)
        resp = self.app.post(self.reg_url, data=req)
        assert resp.status_code == 400

    def test_user_login_status(self):
        # get a status code of 200 when token is returne
        req = ({'username': 'Adebayo', 'password': 'andela007'})
        self.app.post(self.reg_url, data=req)
        resp = self.app.post(self.login_url, data=req)
        assert resp.status_code == 200

    def test_status_code_user_login_with_invalid_details(self):
        # status should return
        req = ({'username': 'Adebayo', 'password': 'andela007'})
        resp = self.app.post(self.login_url, data=req)
        # json.loads(resp.data)
        assert resp.status_code == 404

    def test_user_can_access_auth_routes(self):
        #
        req = ({'username': 'Adebayo', 'password': 'andela007'})
        self.app.post(self.reg_url, data=req)
        token = json.loads((self.app.post(self.login_url, data=req)).data)
        token = token.get('token')
        resp = self.app.post(
            self.bucketlist_url, data=req, headers={'Token': token})

        assert resp.status_code != 401

    def test_user_cannot_access_protected_route_with_invalid_token(self):
        #
        invalid_token = "eyJhbGciOiJIUzI1NiIsImlh\
        dCI6MTQ5Mjg2MjcwOSwiZXhwIjoxNDkyOTQ5MTA5fQ.eyJpZCI6MX0.\
        L5GNE_X7WspxUmLk0XKTpEJmS3XsFZfeFgdiQhLNRIo"
        req = ({'username': 'Adebayo', 'password': 'andela007'})
        resp = self.app.post(
            self.bucketlist_url, data=req, headers={'Token': invalid_token})
        assert resp.status_code == 401

    def test_token_present(self):
        req = ({'username': 'Adebayo', 'password': 'andela007'})
        resp = self.app.post(
            self.bucketlist_url, data=req)
        assert resp.status_code == 401

    def test_error_404_handler(self):
        resp = self.app.get('/bucketlists')
        assert resp.status_code == 404
