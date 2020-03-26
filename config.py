import os


class Config(object):
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))  # This directory

    DB_NAME = 'app.db'
    DB_PATH = os.path.join(PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)

    # Enable protection against CSRF
    CSRF_ENABLED = True

    CSRF_SESSION_KEY = "secretkey"

    CSRF_KEY = "secret"
