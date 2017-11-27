from flask_admin import Admin
import os

admin = Admin()

def init_admin(app, db):
	admin.init_app(app)
	#upload example
	from flask_admin.contrib.fileadmin import FileAdmin
	path = os.path.join(os.path.dirname(__file__), app.config['UPLOAD_FOLDER'])
	admin.add_view(FileAdmin(path, '/uploads/', name='Uploads'))

	from flask_admin.contrib.sqla import ModelView
	from content import Article, Tag, Category
	admin.add_view(ModelView(Article, db.session))
	admin.add_view(ModelView(Tag, db.session))
	admin.add_view(ModelView(Category, db.session))