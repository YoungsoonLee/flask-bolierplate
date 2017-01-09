# configuration
import os


class Configuration(object):
    # Flask settings
    APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/flaskBoilerplate.db' % APPLICATION_DIR
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # ???
    SECRET_KEY = 'flask is fun!'
    CSRF_ENABLED = True
    STATIC_DIR = os.path.join(APPLICATION_DIR, 'static')
    IMAGES_DIR = os.path.join(STATIC_DIR, 'images')

    # Flask-Mail settings
    MAIL_USERNAME = 'email@example.com'
    MAIL_PASSWORD = 'password'
    MAIL_DEFAULT_SENDER = '"Sender" <noreply@example.com>'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
