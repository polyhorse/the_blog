class Config(object):
	DEBUG = False
	TESTING = False
	#upload settings
	UPLOAD_FOLDER = 'uploaded_files'
	ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
	#database settings
	SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SECRET_KEY = 'secret key'
	#flask-mail settings
	MAIL_USERNAME = 'email'
	MAIL_PASSWORD = 'password'
	MAIL_DEFAULT_SENDER = 'a sender'
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 465
	MAIL_USE_SSL = True
	MAIL_USE_TLS = False
	#flask-user setting
	USER_APP_NAME = 'MyApp'
	#flask-themes2 settings
	THEME_PATHS = ['themes']
	HOMEPAGE_THEME = 'homepage_theme'
	ADMIN_THEME = 'admin_theme'
	MEMBER_THEME = 'member_theme'

# class ProductionConfig(Config):

class DevelopmentConfig(Config):
	DEBUG = True

class TestingConfig(Config):
	TESTING = True
