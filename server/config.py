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
	MAIL_USERNAME = 'username'
	MAIL_PASSWORD = 'password'
	MAIL_DEFAULT_SENDER = 'a sender'
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 465
	MAIL_USE_SSL = True
	MAIL_USE_TLS = False
	#flask-user settings
	#flask-user URLs
	USER_APP_NAME = 'MyApp'
	USER_LOGOUT_URL = '/logout'
	USER_LOGIN_URL = '/login'
	#flask-user Endpoints
	USER_AFTER_CHANGE_PASSWORD_ENDPOINT = ''
	USER_AFTER_CHANGE_USERNAME_ENDPOINT = ''
	USER_AFTER_CONFIRM_ENDPOINT = ''
	USER_AFTER_FORGOT_PASSWORD_ENDPOINT = ''
	USER_AFTER_LOGIN_ENDPOINT = 'MemberView:index'
	USER_AFTER_LOGOUT_ENDPOINT = 'user.login'
	USER_AFTER_REGISTER_ENDPOINT = 'MemberView:index'
	USER_AFTER_RESEND_CONFIRM_EMAIL_ENDPOINT = 'user.login'
	USER_AFTER_RESET_PASSWORD_ENDPOINT = 'user.login'
	USER_INVITE_ENDPOINT = ''
	#flask-themes2 settings
	THEME_PATHS = ['themes']
	HOMEPAGE_THEME = 'polyhorse_theme'
	ADMIN_THEME = 'admin_theme'
	MEMBER_THEME = 'member_theme'

# class ProductionConfig(Config):

class DevelopmentConfig(Config):
	DEBUG = True

class TestingConfig(Config):
	TESTING = True
