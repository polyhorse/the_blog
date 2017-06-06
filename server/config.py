class Config(object):
	DEBUG = False
	TESTING = False
	SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	UPLOAD_FOLDER = 'uploaded_files'
	ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
	SECRET_KEY = 'secret key'

# class ProductionConfig(Config):

class DevelopmentConfig(Config):
	DEBUG = True

class TestingConfig(Config):
	TESTING = True
