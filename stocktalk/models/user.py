from flask_login import UserMixin
from stocktalk import db


class User(UserMixin, db.Document):
	username = db.StringField()
	password = db.StringField()
	meta = {'collection':'users'}