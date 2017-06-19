from flask.ext.classy import FlaskView
from flask_user import login_required
from flask_themes2 import Themes, render_theme_template, get_theme, get_themes_list


from config import Config


class MemberView(FlaskView):
	decorators = [login_required]
	theme = Config().MEMBER_THEME

	def index(self):
		return render_theme_template(self.theme, 'index.html')