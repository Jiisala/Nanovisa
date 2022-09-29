from db import db
from flask import session

def get_get_questions(keywords=[]):
    #This most likely will fail if used as it is. Will get more atteintion in the future
    sql = "SELECT id, question, choice1, choice2, choice3, choice4, answer, userid FROM questions WHERE flag=false AND keywords = ANY(:keywords)"
    result = db.session.execute(sql, {"keywords":keywords})
    questions = result.fetchall() 
    
    
    return questions
def get_all_questions():
    #Development time function, might be useless in the finall version
    #Just wanted to have an easy way of implementing the basic ask/answer routine
    sql = "SELECT * FROM questions"
    result = db.session.execute(sql)
    questions = result.fetchall()
    return questions

def add_question(question, choices, answer, keywords):
    userid = session.get("user_id")
    
    if question == "":
        return False
    try:
        sql = """INSERT INTO questions (question, choice1, choice2, choice3, choice4, answer, keywords, user_id)
                 VALUES (:question, :choice1, :choice2, :choice3, :choice4, :answer, :keywords, :userid)"""
        db.session.execute(sql, {"question":question, "choice1":choices[0], "choice2":choices[1], "choice3":choices[2], "choice4":choices[3], "answer":answer, "keywords":keywords, "userid":userid})
        db.session.commit()
    except:
        
        return False
    return True

