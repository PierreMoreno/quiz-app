import sqlite3
import pathlib
from Question import Question
from Answer import Answer

def ConvertJSONToQuestion(data):
	q = Question(data["position"], data["title"], data["text"], data["image"])
	return q

def AddQuestion(input):
    print(input)
    question = ConvertJSONToQuestion(input)

    answers_list = list()
    for answer in input['possibleAnswers']:
        answers_list.append((answer["text"], question.position, answer["isCorrect"]))

    #création d'un objet connection
    path = pathlib.Path(__file__).parent.resolve()/"Database.db"

    db_connection = sqlite3.connect(path)
    # set the sqlite connection in "manual transaction mode"
    # (by default, all execute calls are performed in their own transactions, not what we want)
    db_connection.isolation_level = None

    # start transaction
    db_connection.execute("begin")

    # save the question to db
    insert_question = db_connection.execute(
        "INSERT INTO Question (Position, Title, Text, Image) VALUES (?, ?, ?, ?)",
        (question.position, question.title, question.text, question.image))

    # save the answer to db
    insert_answers = db_connection.executemany(
        "INSERT INTO Answer(Text, Question_Id, Is_Correct) VALUES(?,?,?)", answers_list)
    
    #send the request
    db_connection.execute("commit")
