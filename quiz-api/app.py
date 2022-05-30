from asyncio.windows_events import NULL
from flask import Flask, request
from jwt_utils import build_token, decode_token
from controller import AddQuestion, FetchQuestion, UpdateQuestion, RemoveQuestion, AddParticipation, RemoveParticipations

app = Flask(__name__)

@app.route('/')
def hello_world():
	x = 'world'
	return f"Hello, {x}"

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	return {"size": 0, "scores": []}, 200

@app.route('/login', methods=['POST'])
def Login():
	payload = request.get_json()
	if(payload['password'] == "Vive l'ESIEE !"):
		return {'token':build_token()}, 200
	else:
		return '', 401

@app.route('/questions', methods=['POST'])
def PostQuestion():
	#Récupérer le token envoyé en paramètre
	token = request.headers.get('Authorization')

	if(token == None):
		return '', 401

	if(decode_token(token[7:]) != "quiz-app-admin"):
		return '', 401

	#récupèrer un l'objet json envoyé dans le body de la requète
	payload = request.get_json()

	AddQuestion(payload)

	return '', 200

@app.route('/questions/<position>', methods=['GET'])
def GetQuestion(position):
	
	json = FetchQuestion(position)

	return json, 200

@app.route('/questions/<position>', methods=['PUT'])
def PutQuestion(position):
	#Récupérer le token envoyé en paramètre
	token = request.headers.get('Authorization')

	if(token == None):
		return '', 401

	if(decode_token(token[7:]) != "quiz-app-admin"):
		return '', 401
	
	payload = request.get_json()

	UpdateQuestion(payload)

	return '', 200

@app.route('/questions/<position>', methods=['DELETE'])
def DeleteQuestion(position):

	#Récupérer le token envoyé en paramètre
	token = request.headers.get('Authorization')

	if(token == None):
		return '', 401

	if(decode_token(token[7:]) != "quiz-app-admin"):
		return '', 401
	
	RemoveQuestion(position)

	return '', 204

@app.route('/participations', methods=['POST'])
def PostParticipation():
	
	payload = request.get_json()

	return_json = AddParticipation(payload)
	
	return return_json, 200

@app.route('/participations', methods=['DELETE'])
def DeleteParticipation():

	#Récupérer le token envoyé en paramètre
	token = request.headers.get('Authorization')

	if(token == None):
		return '', 401

	if(decode_token(token[7:]) != "quiz-app-admin"):
		return '', 401

	RemoveParticipations()
	
	return '', 204

if __name__ == "__main__":
    app.run(ssl_context='adhoc')