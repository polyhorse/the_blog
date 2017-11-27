import os
from flask import Flask, request, render_template, redirect, url_for, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import random, string
import flask_restless
from flask_migrate import Migrate
from flask_user import login_required
from flask_themes2 import Themes, render_theme_template, get_theme, get_themes_list
from flask import Blueprint
from flask_menu import Menu, register_menu
from flask import render_template_string
from flask_menu.classy import register_flaskview

# from flaskext.markdown import Markdown
from flask.ext.misaka import Misaka

#########################################
################ INIT ###################
#########################################

def create_app():
	#APP init
	app = Flask(__name__)
	app.config.from_object('config.DevelopmentConfig')

	#THEMES init
	Themes(app, app_identifier='app')

	#MAIL init
	from flask_mail import Mail
	mail = Mail(app)
	#DATABASE init
	from models import db
	db.init_app(app)
	#content, blog, tutorials
	from content import init_content
	init_content(app, db)

	#MIGRATIONS
	migrate = Migrate(app, db)
	with app.app_context():
		#User init
		from flask_user import SQLAlchemyAdapter, UserManager
		from users import User
		db_adapter = SQLAlchemyAdapter(db, User)
		user_manager = UserManager(db_adapter, app)
		#db finalization
		db.create_all()

	#admin
	from admin import init_admin
	init_admin(app, db)
	#MEMBER VIEWS
	from member import init_members
	init_members(app)

	#we render markdown for the user on the server (cache will work better), but editors will get it rendered clientside
	# Markdown(app)
	Misaka(app, fenced_code=True)
	

	return app, migrate, db

app, migrate, db = create_app()


# bp = Blueprint('bp', __name__)
# from content import ContentView
# ContentView.register(bp)
# register_flaskview(bp, ContentView)
# @app.route('/')
# @register_menu(app, '.', 'Home')
# def index():
# 	return render_template_string(
#         """
#         {%- for item in current_menu.children %}
#             {% if item.active %}*{% endif %}{{ item.text }}
#         {% endfor -%}
#         """)

# @app.route('/sdfsdfsdf')
# @register_menu(app, '.first', 'dsfd')
# def index2():
# 	return render_template_string(
#         """
#         {%- for item in current_menu.children %}
#             {% if item.active %}*{% endif %}{{ item.text }}
#         {% endfor -%}
#         """)


#disables cache for testing and content updates
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


############## FILE UPLOAD ###################
@app.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			return redirect(request.url)
		file = request.files['file']
		count = request.form['count']
		# if user does not select file, browser also
		# submit a empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			#we'll dumbly add a hash if this file already exists
			if os.path.isfile( os.path.join(app.config['UPLOAD_FOLDER'], filename) ):
				name_fragments = filename.rsplit('.', 1)
				name_fragments[0] = name_fragments[0].replace('.', '')
				name_fragments[1] = '.' + name_fragments[1]
				name_fragments[0] = name_fragments[0] + '_' + randomword(8) 
				filename = ''.join(name_fragments)

			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			new_dummy_file = DummyFile()
			new_dummy_file.filename = filename
			db.session.add(new_dummy_file)
			db.session.commit()
			files = DummyFile.query.all()
			return redirect(url_for('upload'), code=303)
	#if GET
	files = DummyFile.query.all()
	return render_template('upload.html', files=files)

@app.route('/auth_test')
@login_required
def auth_test():
	return 'Hello'



#########################################
############# UTILITY ###################
#########################################
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def randomword(length):
	return ''.join(random.choice(string.lowercase) for i in range(length))

#this serves uplaoded files when requested
@app.route('/uploads/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def get_current_theme():
	themes = get_themes_list()
	theme = app.config['HOMEPAGE_THEME']
	return get_theme(theme)




if __name__ == "__main__":
	app.run(host='0.0.0.0')