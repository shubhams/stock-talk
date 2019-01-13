from flask_login import UserMixin
from stocktalk import db


class User(UserMixin, db.Document):
	username = db.StringField()
	password = db.StringField()
	meta = {'collection':'users'}


class UserSymbols(db.Document):
	username = db.StringField()
	symbols = db.ListField(db.StringField())
	meta = {'collection': 'user_symbols'}