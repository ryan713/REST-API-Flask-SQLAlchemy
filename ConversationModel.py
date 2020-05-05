from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
import json
from settings import app

db = SQLAlchemy(app)

class Conversation(db.Model):

	__tablename__ = 'conversations'

	id = db.Column(db.Integer(), primary_key = True)
	user = db.Column(db.String(50), nullable = False)
	messages = db.Column(db.String())

	def __repr__(self):
		return json.dumps({
			'id': self.id,
			'user': self.user,
			'conversation': json.loads(self.messages)
		}, indent = 4)

	def addNewMessage(self, _user, _message):
		conv = Conversation.query.filter_by(user = _user).first()
		temp = json.loads(conv.messages)
		temp['messages'].append(_message)
		conv.messages = json.dumps(temp)
		db.session.commit()

	def addNewConversation(self, _user):
		conv = Conversation(user = _user, messages = json.dumps({'messages': []}))
		db.session.add(conv)
		db.session.commit()	

	def getConversation(self, _user):
		conv = Conversation.query.filter_by(user = _user).first()
		return json.loads(conv.messages)

	def getAllConversations(self):
		return Conversation.query.all()			

	def reset(self):
		Conversation.query.delete()	
		db.session.commit()	