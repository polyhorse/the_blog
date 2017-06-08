import os
from flask import Flask, request, render_template, redirect, url_for, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import random, string
import flask_restless
from flask_migrate import Migrate
from flask_user import login_required

#########################################
################ INIT ###################
#########################################
def create_app():
	#APP init
	app = Flask(__name__)
	app.config.from_object('config.DevelopmentConfig')
	#MAIL init
	from flask_mail import Mail
	mail = Mail(app)
	#DATABASE init
	from models import db
	db.init_app(app)
	#MIGRATIONS init
	migrate = Migrate(app, db)
	with app.app_context():
		#User init
		from flask_user import SQLAlchemyAdapter, UserManager
		from users import User
		db_adapter = SQLAlchemyAdapter(db, User)
		user_manager = UserManager(db_adapter, app)
		#db finalization
		db.create_all()
	#API - is for IOT, or mobile
	from models import DummyObject, DummyFile
	manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)
	manager.create_api(DummyObject)
	manager.create_api(DummyFile)
	#ADMIN - is for basic crud for trained users
	from admin import admin
	admin.init_app(app)
	#upload example
	from flask_admin.contrib.fileadmin import FileAdmin
	path = os.path.join(os.path.dirname(__file__), app.config['UPLOAD_FOLDER'])
	admin.add_view(FileAdmin(path, '/uploads/', name='Uploads'))
	#sqlmodel example
	from flask_admin.contrib.sqla import ModelView
	admin.add_view(ModelView(DummyObject, db.session))
	#DASHBOARD - is for customer login pages
	#I'll have to make that custom
	return app, migrate

app, migrate = create_app()


#########################################
############## ROUTES ###################
#########################################

############## INDEX ###################
@app.route("/")
def index():
	dummy_objects = DummyObject.query.all()
	dummy_files = DummyFile.query.all()
	print(dummy_objects)
	print(dummy_files)
	return render_template('index.html', dummy_objects=dummy_objects, dummy_files=dummy_files)

############## CRUD ###################
@app.route("/crud", methods=['GET', 'POST'])
def crud():
	if request.method == 'POST':
		#WTFORMS crud example
		pass
	#return this if get
	dummy_objects = DummyObject.query.all()
	return render_template('crud.html', dummy_objects=dummy_objects)

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




if __name__ == "__main__":
	app.run(host='0.0.0.0')