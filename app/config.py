import os


class Config(object):
    SECRET_KEY = 'super_secret_key_for_project_00023'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.mail.ru'
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "")
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_SUPPRESS_SEND = False
    TESTING = False
