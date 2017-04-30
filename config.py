import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MAIN_DB_URL = os.path.join(BASE_DIR, 'bucketlist.sqlite')
TEST_DB_URL = os.path.join(BASE_DIR, 'test.sqlite')


class BaseConfig(object):
    '''
    The class holds base config for each environment
    '''
    SECRET_KEY = os.getenv('SECRET_KEY', 'This should be changed')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI', "'sqlite:///' + {}".format(MAIN_DB_URL))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ERROR_404_HELP = False
    DEBUG = False
    TESTING = False


class DevelopmentConfig(BaseConfig):
    '''
    configuration for the development environment
    '''
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + MAIN_DB_URL
    DEBUG = True
    DEVELOPMENT = True


class TestingConfig(BaseConfig):
    '''
    config when testing
    '''
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + TEST_DB_URL
    CSRF_ENABLED = False


class StagingConfig(BaseConfig):
    DEVELOPMENT = True
    DEBUG = True


class ProductionConfig(BaseConfig):
    '''
    config for when in production
    '''
    DEBUG = False
