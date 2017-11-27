from flask import Flask, render_template_string, redirect, url_for
from sqlalchemy import create_engine, MetaData
from flask_login import UserMixin, LoginManager, login_user, logout_user
from flask_blogging import SQLAStorage, BloggingEngine
import datetime
from flask_themes2 import Themes, render_theme_template, get_theme, get_themes_list
from flask_classy import FlaskView, route

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
import inspect


from flask_menu import Menu, register_menu
from flask_menu.classy import classy_menu_item

from flask import Blueprint
from flask_menu.classy import register_flaskview

db = SQLAlchemy()

#########################################
############## MODELS ###################
#########################################
tags = db.Table('tags',
	db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
	db.Column('article_id', db.Integer, db.ForeignKey('article.id'), primary_key=True)
)

categories = db.Table('categories',
	db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True),
	db.Column('article_id', db.Integer, db.ForeignKey('article.id'), primary_key=True)
)

class Article(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	url_headline = db.Column(db.String(256))
	created = db.Column(db.DateTime, default=datetime.datetime.now)
	publish_date = db.Column(db.DateTime, nullable=True)
	deleted = db.Column(db.DateTime, nullable=True)
	headline = db.Column(db.String(256))
	copy = db.Column(db.Text)
	tags = db.relationship('Tag', secondary=tags, lazy='subquery',backref=db.backref('articles', lazy=True))
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'),nullable=True)
	featured_image = db.Column(db.String(256), nullable=True)

	def __repr__(self):
		return self.headline

class Tag(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))

	def __repr__(self):
		return self.name

class Category(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	articles = db.relationship('Article', backref='category', lazy=True)

	def __repr__(self):
		return self.name

@event.listens_for(Article, "before_insert")
def ArticleUrlBeforeInsert(mapper, connection, instance):
	instance.url_headline = instance.headline.replace(' ', '-').lower()

@event.listens_for(Article, "before_update")
def ArticleUrlBeforeUpdate(mapper, connection, instance):
	instance.url_headline = instance.headline.replace(' ', '-').lower()


#########################################
############## VIEWS ###################
#########################################

from config import Config

# class MenuMixin:

# 	shitlist = ['base_args', 'get', 'theme', 'index']

# 	def build_menu(self, active_endpoint):
# 		my_attributes = [a for a in dir(self) if not a.startswith('_')]
# 		for attr in my_attributes:
# 			if callable(attr):
# 				attr.remove(attr)
# 		parent_attributes = dir(FlaskView) + dir(MenuMixin) + self.shitlist
# 		for attr in parent_attributes:
# 			if attr in my_attributes:
# 				my_attributes.remove(attr)

# 		print(my_attributes)
# 		print(self.__class__.__name__)
# 		class_name = self.__class__.__name__
# 		menu = []
# 		for attr in my_attributes:
# 			endpoint = '%s:%s' % (class_name, attr)
# 			url = url_for(endpoint)
# 			active = (attr == active_endpoint)
# 			menu.append({
# 				'url':url,
# 				'name':attr.replace('_', ' '),
# 				'active':active
# 				})
# 		return menu


from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, HiddenField
from wtforms.validators import DataRequired
import flask

class ArticleForm(FlaskForm):
    headline = StringField('headline')
    copy = TextAreaField('copy')
    id = HiddenField('id')
	# url_headline = db.Column(db.String(256))
	# publish_date = db.Column(db.DateTime, nullable=True)
	# deleted = db.Column(db.DateTime, nullable=True)
	# tags = db.relationship('Tag', secondary=tags, lazy='subquery',backref=db.backref('articles', lazy=True))
	# category_id = db.Column(db.Integer, db.ForeignKey('category.id'),nullable=True)
	# featured_image = db.Column(db.String(256), nullable=True)

class ContentView(FlaskView):
	# decorators = [login_required]
	theme = Config().HOMEPAGE_THEME
	route_base = '/'

	#homepage /
	@classy_menu_item('index', 'Home', order=0)
	def index(self):
		return render_theme_template(self.theme, 'index.html')

	# any page by title - ARTICLE
	@route('/<url_headline>')
	def view_article(self, url_headline):
		previous_url = flask.request.referrer
		if previous_url == flask.request.url:
			previous_url = None
		article = Article.query.filter_by(url_headline=url_headline).filter(Article.publish_date.isnot(None)).first()
		if article is None:
			return redirect(url_for('ContentView:index'))
		return render_theme_template(self.theme, 'article.html', article=article, previous_url=previous_url)

	@route('/edit/<url_headline>', methods=['GET'])
	def get_edit_article(self, url_headline):
		article = Article.query.filter_by(url_headline=url_headline).filter(Article.publish_date.isnot(None)).first()
		if article is None:
			return redirect(url_for('ContentView:index'))
		form = ArticleForm(obj=article)
		return render_theme_template(self.theme, 'article_edit.html', article=article, form=form)

	@route('/edit/<url_headline>', methods=['POST'])
	def post_edit_article(self, url_headline):
		article = Article.query.filter_by(url_headline=url_headline).filter(Article.publish_date.isnot(None)).first()
		if article is None:
			return redirect(url_for('ContentView:index'))
		form = ArticleForm(obj=article)
		if form.validate_on_submit():
			form.populate_obj(article)
			db.session.commit()
			return redirect(url_for('ContentView:get_edit_article', url_headline=article.url_headline))

	@route('/tag/<tag>')
	def tag(self, tag):
		print(tag)
		return redirect(url_for('ContentView:index'))

	# the blog category stream - send you to an article page when you click a link
	@classy_menu_item('blog', 'Blog', order=2)
	def blog(self):
		category = Category.query.filter_by(name='blog').first()
		articles = Article.query.filter_by(category_id=category.id).filter(Article.publish_date.isnot(None)).all()
		tags = Tag.query.all()
		recent_posts = Article.query.filter_by(category_id=category.id).filter(Article.publish_date.isnot(None)).order_by(Article.publish_date.desc()).limit(5).all()
		return render_theme_template(self.theme, 'blog.html', articles=articles, tags=tags, recent_posts=recent_posts)

	#the tutorials category stream - send you to an article page when you click a link
	@classy_menu_item('tutorials', 'Tutorials', order=3)
	def tutorials(self):
		category = Category.query.filter_by(name='tutorials').first()
		articles = Article.query.filter_by(category_id=category.id).filter(Article.publish_date.isnot(None)).all()
		return render_theme_template(self.theme, 'tutorials.html', articles=articles)

	#static html page
	@route('/for-hire')
	@classy_menu_item('guns_for_hire', 'Guns For Hire', order=1)
	def guns_for_hire(self):
		return render_theme_template(self.theme, 'for-hire.html')

	#static html page
	@classy_menu_item('contact', 'Contact', order=4)
	def contact(self):
		return render_theme_template(self.theme, 'contact.html')

	#dunno yet - probably static
	@route('/tools-for-unity')
	@classy_menu_item('tools_fore_unity', 'Tools For Unity', order=0)
	def tools_for_unity(self):
		return render_theme_template(self.theme, 'tools-for-unity.html')


def init_content(app, db):
	#cause i am lazy and want it to automigrate
	db.init_app(app)
	#doing mthe menu is kinda a bitch - so expect some fragility if you mess with this
	bp = Blueprint('bp', __name__)
	ContentView.register(bp)
	register_flaskview(bp, ContentView)
	Menu(app=app)
	app.register_blueprint(bp)
	ContentView.register(app)
	
	
	



