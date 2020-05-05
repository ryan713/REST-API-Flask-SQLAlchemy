from flask import Flask, request, Response, jsonify
import jwt
import datetime, json
from UserModel import User
from ConversationModel import *
from functools import wraps
from HotorBot import *
from settings import *

user = User()
conv = Conversation()
app.config['SECRET_KEY'] = 'marcos'

def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.args.get('token')
        try:
            jwt.decode(token, app.config['SECRET_KEY'], algorithms = ['HS256'])
        except:
            return jsonify({'Error': 'Provide a valid JWT.'}), 401
        return func(*args, **kwargs)    

    return wrapper                

def getJWT():
    exp_date = datetime.datetime.utcnow() + datetime.timedelta(minutes = 30)
    token = jwt.encode({'exp': exp_date}, app.config['SECRET_KEY'], algorithm = 'HS256')        
    return jsonify({'token': token})

@app.route('/login/', methods = ['POST'])
def login():
    request_data = request.get_json()
    username = request_data["username"]
    password = request_data["password"]

    if user.validateUser(username, password) is True:
        return getJWT()
        
    return jsonify({'Error': 'Username or Password incorrect'}), 401

@app.route('/signup/', methods = ['POST'])
def signUp():
    request_data = request.get_json()
    username = request_data["username"]
    password = request_data["password"]

    if user.addNewUser(username, password) is True:
        return getJWT()

    return jsonify({'Error': 'Username Taken!'}), 401

@app.route('/marcos/', methods = ['POST'])
@token_required
def marcos():
	resp = request.get_json()
	convo = conv.getConversation(resp["username"])
	return jsonify({"messages": convo})

@app.route('/getReply/', methods = ['POST'])
@token_required
def askMarcos():
    resp = request.get_json()
    replies = reply(resp['message'])
    
    conv.addNewMessage(resp['username'], resp)

    messages = []
    for rep in replies:
        rep = rep.replace(' end', '.').replace(' comma', ',').capitalize()

        conv.addNewMessage(resp['username'], {
            'username': 'marcos',
            'message': rep
        })
                 
        messages.append({
            'message': rep,
        	'id': len(messages) + 1
        })

    return jsonify({'messages': messages})

app.run(port = 3000)	
