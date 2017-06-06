from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class SerializableMixin:
	@property
	def json(self):
		my_attributes = [a for a in dir(self) if not a.startswith('_')]
		for attr in my_attributes:
			if callable(attr):
				attr.remove(attr)
		parent_attributes = dir(db.Model) + dir(SerializableMixin)
		for attr in parent_attributes:
			if attr in my_attributes:
				my_attributes.remove(attr)

		print(my_attributes)
		jsn = {}
		for attr in my_attributes:
			jsn[attr] = getattr(self,attr)
		return jsonify(jsn)

#########################################
############## MODELS ###################
#########################################
class DummyObject(db.Model, SerializableMixin):
	id = db.Column(db.Integer, primary_key=True)
	a_number = db.Column(db.Integer, default=8)
	a_boolean = db.Column(db.Boolean, default=True)
	some_text = db.Column(db.String(80))

class DummyFile(db.Model, SerializableMixin):
	id = db.Column(db.Integer, primary_key=True)
	filename = db.Column(db.String(80))