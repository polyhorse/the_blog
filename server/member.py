from flask.ext.classy import FlaskView
from flask_user import login_required


class MemberView(FlaskView):
	decorators = [login_required]

	def index(self):
		return 'hello'