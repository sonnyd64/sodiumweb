import os
basedir = os.path.abspath(os.path.dirname(__name__))

class Config(object):
	DEBUG = False
	TESTING = False
	CSRF_ENABLED = True
	SECRET_KEY = 'mr-belvedere'
	# Was this causing the issue where helper functions would default to the real DB instead of test_helper.py's DB?
	SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

class ProductionConfig(Config):
	DEBUG = False

class StagingConfig(Config):
	DEVELOPMENT = True
	DEBUG = True

class TestingConfig(Config):
	TESTING = True
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = "sqlite://:memory:"

class DevelopmentConfig(Config):
	TESTING = True