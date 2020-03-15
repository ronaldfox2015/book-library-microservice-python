# /src/config.py

import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class Development(object):
    """
    Development environment configuration
    """
    DEBUG = True
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_POOL_SIZE=20
    SQLALCHEMY_POOL_TIMEOUT=300
class Production(object):
    """
    Production environment configurations
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_POOL_SIZE=20
    SQLALCHEMY_POOL_TIMEOUT=300
class Testing(object):
    """
    Development environment configuration
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_TEST_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_POOL_SIZE=20
    SQLALCHEMY_POOL_TIMEOUT=300
app_config = {
    'development': Development,
    'production': Production,
    'testing': Testing
}
