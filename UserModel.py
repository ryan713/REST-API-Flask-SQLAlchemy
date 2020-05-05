from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
import json
from settings import app
from ConversationModel import *

db = SQLAlchemy(app)

class User(db.Model):

	__tablename__ = 'users'
	
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(50), unique = True, nullable = False)
	password = db.Column(db.String(50), nullable = False)

	def __repr__(self):
		return json.dumps({
			'id': self.id,
			'username': self.username,
			'password': self.password
		}, indent = 4)

	def validateUser(self, _username, _password):
		user = User.query.filter_by(username = _username).filter_by(password = _password).first()
		if user is None:
			return False
		return True

	def addNewUser(self, _username, _password):
		new_user = User(username = _username, password = _password)
		try:	
			db.session.add(new_user)
			db.session.commit()
			conv = Conversation()
			conv.addNewConversation(_username)
			return True
		except:
			return False

	def getAllUsers(self):
		return User.query.all()	

	def reset(self):
		User.query.delete()	
		db.session.commit()
