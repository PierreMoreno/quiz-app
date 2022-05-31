import json
from multiprocessing.connection import answer_challenge
import sqlite3
import pathlib
from turtle import position
from Question import Question
from Answer import Answer
from Participation import Participation
from ParticipationAnswer import ParticipationAnswer

def ConvertJSONToQuestion(data):
	q = Question(data["position"], data["title"], data["text"], data["image"])
	return q

def GetQuestionIdFromPosition(db_connection, position):
    get_question = db_connection.execute(
        "SELECT Id FROM Question WHERE Position = ?",
        (position,))

    question = get_question.fetchall()
    
    if len(question) == 0:
        return -1

    return question[0][0]

def QuizInfo():
    #création d'un objet connection
    path = pathlib.Path(__file__).parent.resolve()/"Database.db"

    db_connection = sqlite3.connect(path)
    # set the sqlite connection in "manual transaction mode"
    # (by default, all execute calls are performed in their own transactions, not what we want)
    db_connection.isolation_level = None
    
    # start transaction
    db_connection.execute("begin")

    get_question_count = db_connection.execute(
        "SELECT COUNT(*) FROM Question;",)

    size = get_question_count.fetchall()[0][0]

    get_player_scores = db_connection.execute(
        "SELECT Player, Score FROM Participation ORDER BY Score DESC;",)

    player_scores = get_player_scores.fetchall()

    scores = list()
    for s in player_scores:
        scores.append({"playerName": s[0], "score": s[1]})

    db_connection.execute("commit")
    
    return {"size": size, "scores": scores}

def AddQuestion(input):
    #création d'un objet connection
    path = pathlib.Path(__file__).parent.resolve()/"Database.db"

    db_connection = sqlite3.connect(path)
    # set the sqlite connection in "manual transaction mode"
    # (by default, all execute calls are performed in their own transactions, not what we want)
    db_connection.isolation_level = None
    
    # start transaction
    db_connection.execute("begin")

    question = ConvertJSONToQuestion(input)

    # increment position for higher position questions
    update_questions = db_connection.execute(
        "UPDATE Question SET Position = Position + ? WHERE Position >= ?",
        (1, question.position))

    # save the question to db
    insert_question = db_connection.execute(
        "INSERT INTO Question (Position, Title, Text, Image) VALUES (?, ?, ?, ?)",
        (question.position, question.title, question.text, question.image))

    question_id = GetQuestionIdFromPosition(db_connection, question.position)

    answers_list = list()
    for answer in input['possibleAnswers']:
        answers_list.append((answer["text"], question_id, answer["isCorrect"]))

    # save the answer to db
    insert_answers = db_connection.executemany(
        "INSERT INTO Answer(Text, Question_Id, Is_Correct) VALUES(?,?,?)", answers_list)
    
    #send the request
    db_connection.execute("commit")

    return '', 200

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
        "SELECT Id, Position, Title, Text, Image FROM Question WHERE Position = ?",
        (position,))
    
    question = get_question.fetchall()
    
    if len(question) == 0:
        return '', 404
    
    q = Question(question[0][1], question[0][2], question[0][3], question[0][4])

    get_answers = db_connection.execute(
        "SELECT Text, Id, Is_Correct FROM Answer WHERE Question_Id = ?",
        (question[0][0],))
    
    answers = get_answers.fetchall()

    answers_list = list()
    for answer in answers:
        a = Answer(answer[0], answer[1], True if answer[2] == 1 else False)
        answers_list.append(a.ConvertToJson())

    return_json = json.loads(q.ConvertToJson())
    return_json["possibleAnswers"] = answers_list

    #send the request
    db_connection.execute("commit")

    return return_json, 200

def UpdateQuestion(old_position, input):
    #création d'un objet connection
    path = pathlib.Path(__file__).parent.resolve()/"Database.db"
    
    db_connection = sqlite3.connect(path)
    # set the sqlite connection in "manual transaction mode"
    # (by default, all execute calls are performed in their own transactions, not what we want)
    db_connection.isolation_level = None

    # start transaction
    db_connection.execute("begin")
    
    question_id = GetQuestionIdFromPosition(db_connection, old_position)

    if question_id == -1:
        return '', 404
    
    # delete old answers
    delete_answers = db_connection.execute(
        "DELETE FROM Answer WHERE Question_Id = ?",
        (question_id,))

    answers_list = list()
    for answer in input['possibleAnswers']:
        answers_list.append((answer["text"], question_id, answer["isCorrect"]))

    old_position = int(old_position)
    
    switch_question_positions = db_connection.execute(
            "UPDATE Question SET Position = ?, Title = ?, Text = ?, Image = ? WHERE Position = ? AND Id = ?",
            (input["position"], input["title"], input["text"], input["image"], old_position, question_id))

    if input["position"] == old_position:
        print("same")
        # update question
        update_question = db_connection.execute(
            "UPDATE Question SET Position = ?, Title = ?, Text = ?, Image = ? WHERE Position = ?",
            (input["position"], input["title"], input["text"], input["image"], old_position))
    
    if input["position"] < old_position:
        print("lesser than")
        # increment other questions position
        update_question_positions = db_connection.execute(
            "UPDATE Question SET Position = Position + ? WHERE Position >= ? AND Position < ? AND NOT Id = ?",
            (1, input["position"], old_position, question_id))
    
    if input["position"] > old_position:
        print("greater than")
        # decrement other questions position
        update_question_positions = db_connection.execute(
            "UPDATE Question SET Position = Position - ? WHERE Position <= ? AND Position > ? AND NOT Id = ?",
            (1, input["position"], old_position, question_id))
    
    # save new answers
    insert_answers = db_connection.executemany(
        "INSERT INTO Answer(Text, Question_Id, Is_Correct) VALUES(?,?,?)", answers_list)

    #send the request
    db_connection.execute("commit")

    return '', 200

def RemoveQuestion(position):
    #création d'un objet connection
    path = pathlib.Path(__file__).parent.resolve()/"Database.db"

    db_connection = sqlite3.connect(path)
    # set the sqlite connection in "manual transaction mode"
    # (by default, all execute calls are performed in their own transactions, not what we want)
    db_connection.isolation_level = None

    # start transaction
    db_connection.execute("begin")

    question_id = GetQuestionIdFromPosition(db_connection, position)

    if question_id == -1:
        return '', 404
    
    delete_answers = db_connection.execute(
        "DELETE FROM Answer WHERE Question_Id = ?",
        (question_id,))

    delete_Question = db_connection.execute(
        "DELETE FROM Question WHERE Position = ?",
        (position,))

    # decrement position for higher position questions
    update_questions = db_connection.execute(
        "UPDATE Question SET Position = Position - ? WHERE Position > ?",
        (1, position))

    #send the request
    db_connection.execute("commit")

    return '', 204

def AddParticipation(input):
    quiz_info = QuizInfo()
    if len(input["answers"]) != quiz_info["size"]:
        return '', 400

    p = Participation(input["playerName"])
    
    #création d'un objet connection
    path = pathlib.Path(__file__).parent.resolve()/"Database.db"

    db_connection = sqlite3.connect(path)
    # set the sqlite connection in "manual transaction mode"
    # (by default, all execute calls are performed in their own transactions, not what we want)
    db_connection.isolation_level = None

    # start transaction
    db_connection.execute("begin")

    insert_participation = db_connection.execute(
        "INSERT INTO Participation (Player) VALUES (?)",
        (p.player,))

    get_participation = db_connection.execute(
        "SELECT Id FROM Participation WHERE Player = ?",
        (p.player,))
    
    participation_id = get_participation.fetchall()[0][0]

    participation_answers_list = list()
    question_position = 0
    score = 0
    for answer in input["answers"]:
        question_position += 1
        question_id = GetQuestionIdFromPosition(db_connection, question_position)
        get_answer = db_connection.execute(
            "SELECT Id, Is_Correct FROM Answer WHERE Question_Id = ?",
            (question_id,))
        fetch_answer = get_answer.fetchall()
        score += fetch_answer[answer-1][1]
        participation_answers_list.append((participation_id, fetch_answer[answer-1][0]))
    
    insert_answers = db_connection.executemany(
        "INSERT INTO Participation_Answer(Participation_Id, Answer_Id) VALUES(?,?)", participation_answers_list)

    update_score = db_connection.execute(
        "UPDATE Participation SET Score = ? WHERE Id = ?",
        (score,participation_id))
    
    #send the request
    db_connection.execute("commit")

    return_json = {"playerName": p.player, "score": score}
    
    return return_json, 200

def RemoveParticipations():
    #création d'un objet connection
    path = pathlib.Path(__file__).parent.resolve()/"Database.db"

    db_connection = sqlite3.connect(path)
    # set the sqlite connection in "manual transaction mode"
    # (by default, all execute calls are performed in their own transactions, not what we want)
    db_connection.isolation_level = None

    # start transaction
    db_connection.execute("begin")

    delete_answers = db_connection.execute(
        "DELETE FROM Participation_Answer;",)
    
    delete_participations = db_connection.execute(
        "DELETE FROM Participation;",)

    #send the request
    db_connection.execute("commit")