import os
from dotenv import load_dotenv


APP_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir))
PROJECT_DIR = os.path.abspath(os.path.join(APP_DIR, os.pardir))
load_dotenv(os.path.join(PROJECT_DIR, '.env'))


class base_config(object):
    """Default configuration options."""
    SITE_NAME = os.environ.get('SITE_NAME', 'Analyze Sentiment')
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secrets')
    SERVER_NAME = os.environ.get('SERVER_NAME', 'localhost')
    JSONIFY_PRETTYPRINT_REGULAR = False


class dev_config(base_config):
    """Development configuration options."""
    DEBUG = True
    SERVER_NAME = 'localhost:5000'
    WTF_CSRF_ENABLED = False


class test_config(base_config):
    """Testing configuration options."""
    TESTING = True
    WTF_CSRF_ENABLED = False