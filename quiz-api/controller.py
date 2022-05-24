import json
import sqlite3
import pathlib
from Question import Question
from Answer import Answer

def ConvertJSONToQuestion(data):
	q = Question(data["position"], data["title"], data["text"], data["image"])
	return q

def AddQuestion(input):
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

def FetchQuestion(position):
    #création d'un objet connection
    path = pathlib.Path(__file__).parent.resolve()/"Database.db"

    db_connection = sqlite3.connect(path)
    # set the sqlite connection in "manual transaction mode"
    # (by default, all execute calls are performed in their own transactions, not what we want)
    db_connection.isolation_level = None

    # start transaction
    db_connection.execute("begin")

    # save the question to db
    get_question = db_connection.execute(
        "SELECT Position, Title, Text, Image FROM Question WHERE Position = ?",
        position)
    
    question = get_question.fetchall()
    q = Question(question[0][0], question[0][1], question[0][2], question[0][3])

    get_answers = db_connection.execute(
        "SELECT Text, Id, Is_Correct FROM Answer WHERE Question_Id = ?",
        position)
    
    answers = get_answers.fetchall()

    answers_list = list()
    for answer in answers:
        a = Answer(answer[0], answer[1], answer[2])
        answers_list.append(json.loads(a.ConvertToJson()))

    return_json = json.loads(q.ConvertToJson())
    return_json["possibleAnswers"] = answers_list

    #send the request
    db_connection.execute("commit")

    return return_json

def UpdateQuestion(input):
    #création d'un objet connection
    path = pathlib.Path(__file__).parent.resolve()/"Database.db"

    answers_list = list()
    for answer in input['possibleAnswers']:
        answers_list.append((answer["text"], input["position"], answer["isCorrect"]))
    
    db_connection = sqlite3.connect(path)
    # set the sqlite connection in "manual transaction mode"
    # (by default, all execute calls are performed in their own transactions, not what we want)
    db_connection.isolation_level = None

    # start transaction
    db_connection.execute("begin")
    
    # delete old answers
    delete_answers = db_connection.execute(
        "DELETE FROM Answer WHERE Question_Id = ?",
        (input["position"],))

    # update question
    update_question = db_connection.execute(
        "UPDATE Question SET Position = ?, Title = ?, Text = ?, Image = ? WHERE Position = ?",
        (input["position"], input["title"], input["text"], input["image"], input["position"]))
    
    # save new answers
    insert_answers = db_connection.executemany(
        "INSERT INTO Answer(Text, Question_Id, Is_Correct) VALUES(?,?,?)", answers_list)

    #send the request
    db_connection.execute("commit")

    return

def RemoveQuestion(position):
    #création d'un objet connection
    path = pathlib.Path(__file__).parent.resolve()/"Database.db"

    db_connection = sqlite3.connect(path)
    # set the sqlite connection in "manual transaction mode"
    # (by default, all execute calls are performed in their own transactions, not what we want)
    db_connection.isolation_level = None

    # start transaction
    db_connection.execute("begin")

    delete_answers = db_connection.execute(
        "DELETE FROM Answer WHERE Question_Id = ?",
        position)

    delete_Question = db_connection.execute(
        "DELETE FROM Question WHERE Position = ?",
        position)

    #send the request
    db_connection.execute("commit")
