from db import db
from flask import session
from random import shuffle

#This function will pass calls to other specialized functions
#The queries will get all questons matching the given arguments, 
#because selecting random lines in SQL is costly operation compared to python
#I'm fairly certain that there is a more elegant way of doing many things here, but this should work

def get_new_question_set(how_many, keywords, include_own, include_answered, fill_with_random ):
    print("alku", keywords)
    user_id = session.get("user_id")
    if include_own and include_answered:
        print("eka")
        questions = get_questions_include_own_and_answered(keywords)
    elif include_own:
        print("toka")
        questions = get_questions_include_own(keywords, user_id)
    elif include_answered:
        print("kolmas")
        questions = get_questions_include_answered(keywords, user_id)
    else:
        print("neljäs")
        questions = get_questions_with_all_constrains(keywords, user_id)   
    
    if fill_with_random:
        if len(questions) < how_many:
            questions = fill_with_rest_with_random(questions, how_many)
            
            
    for question in questions:
        print (question)
    shuffle(questions)
    return questions[:how_many]

def get_questions_with_all_constrains(keywords, user_id):
    if all(a == '' for a in keywords):
        try:
            sql = """SELECT * FROM questions AS Q
            LEFT JOIN flagged_questions AS F 
            on Q.id = F.question_id 
            LEFT JOIN answers_given AS A
            ON :user_id = A.user_id AND Q.id = A.question_id
            WHERE F.question_id IS NULL 
            AND A.user_id IS NULL 
            AND A.question_id IS NULL
            AND Q.user_id <> :user_id 
            """
            result = db.session.execute(sql,{"user_id":user_id, "keywords0":keywords[0], "keywords1":keywords[1],"keywords2":keywords[2],"keywords3":keywords[3]})
            questions = result.fetchall()
        except:
            print("fails, allconst")
            return False
                
    else:
        try:
            sql = """SELECT * FROM questions AS Q
            LEFT JOIN flagged_questions AS F 
            on Q.id = F.question_id 
            LEFT JOIN answers_given AS A
            ON :user_id = A.user_id AND Q.id = A.question_id
            WHERE F.question_id IS NULL 
            AND A.user_id IS NULL 
            AND A.question_id IS NULL
            AND  (
                (Q.keyword1 IN (:keywords0, :keywords1, :keywords2, :keywords3)
            AND Q.keyword1 <> '')
            OR  (Q.keyword2 IN (:keywords0, :keywords1, :keywords2, :keywords3)
            AND Q.keyword2 <> '')
            OR  (Q.keyword3 IN (:keywords0, :keywords1, :keywords2, :keywords3)
            AND Q.keyword3 <> '')
            OR  (Q.keyword4 IN (:keywords0, :keywords1, :keywords2, :keywords3)
            AND Q.keyword4 <> '')
            )
            AND Q.user_id <> :user_id 
            """
            result = db.session.execute(sql,{"user_id":user_id, "keywords0":keywords[0], "keywords1":keywords[1],"keywords2":keywords[2],"keywords3":keywords[3]})
            questions = result.fetchall()
        except:
            print("fails, allconst")
            return False
    return questions    
def get_questions_include_own(keywords, user_id):
    if all(a == '' for a in keywords):
        try:
            sql = """SELECT * FROM questions AS Q
            LEFT JOIN flagged_questions AS F 
            on Q.id = F.question_id 
            LEFT JOIN answers_given AS A
            ON :user_id = A.user_id AND Q.id = A.question_id
            WHERE F.question_id IS NULL 
            AND A.user_id IS NULL 
            AND A.question_id IS NULL
            """
            result = db.session.execute(sql,{"user_id":user_id, "keywords0":keywords[0], "keywords1":keywords[1],"keywords2":keywords[2],"keywords3":keywords[3]})
            questions = result.fetchall()
        except:
            print("fails, includeown")
            return False
    else:
        try:
            sql = """SELECT * FROM questions AS Q
            LEFT JOIN flagged_questions AS F 
            on Q.id = F.question_id 
            LEFT JOIN answers_given AS A
            ON :user_id = A.user_id AND Q.id = A.question_id
            WHERE F.question_id IS NULL 
            AND A.user_id IS NULL 
            AND A.question_id IS NULL
            AND  (
                (Q.keyword1 IN (:keywords0, :keywords1, :keywords2, :keywords3)
            AND Q.keyword1 <> '')
            OR  (Q.keyword2 IN (:keywords0, :keywords1, :keywords2, :keywords3)
            AND Q.keyword2 <> '')
            OR  (Q.keyword3 IN (:keywords0, :keywords1, :keywords2, :keywords3)
            AND Q.keyword3 <> '')
            OR  (Q.keyword4 IN (:keywords0, :keywords1, :keywords2, :keywords3)
            AND Q.keyword4 <> '')
            )
            """
            result = db.session.execute(sql,{"user_id":user_id, "keywords0":keywords[0], "keywords1":keywords[1],"keywords2":keywords[2],"keywords3":keywords[3]})
            questions = result.fetchall()
        except:
            print("fails, includeown")
            return False
    return questions
def get_questions_include_answered(keywords, user_id):
    if all(a == '' for a in keywords):
        try:
            sql = """SELECT * FROM questions AS Q
            LEFT JOIN flagged_questions AS F 
            on Q.id = F.question_id 
            WHERE F.question_id IS NULL 
            AND Q.user_id <> :user_id 
            """
            result = db.session.execute(sql,{"user_id":user_id, "keywords0":keywords[0], "keywords1":keywords[1],"keywords2":keywords[2],"keywords3":keywords[3]})
            questions = result.fetchall()
        except:
            print("fails, includeanswered")
            return False
    else:    
        try:
            sql = """SELECT * FROM questions AS Q
            LEFT JOIN flagged_questions AS F 
            on Q.id = F.question_id 
            WHERE F.question_id IS NULL 
            AND  (
                (Q.keyword1 IN (:keywords0, :keywords1, :keywords2, :keywords3)
            AND Q.keyword1 <> '')
            OR  (Q.keyword2 IN (:keywords0, :keywords1, :keywords2, :keywords3)
            AND Q.keyword2 <> '')
            OR  (Q.keyword3 IN (:keywords0, :keywords1, :keywords2, :keywords3)
            AND Q.keyword3 <> '')
            OR  (Q.keyword4 IN (:keywords0, :keywords1, :keywords2, :keywords3)
            AND Q.keyword4 <> '')
            )
            AND Q.user_id <> :user_id 
            """
            result = db.session.execute(sql,{"user_id":user_id, "keywords0":keywords[0], "keywords1":keywords[1],"keywords2":keywords[2],"keywords3":keywords[3]})
            questions = result.fetchall()
        except:
            print("fails, includeanswered")
            return False
    return questions

def get_questions_include_own_and_answered(keywords):
    if all(a == '' for a in keywords):
        try:
            sql = """SELECT * FROM questions AS Q
            LEFT JOIN flagged_questions AS F 
            on Q.id = F.question_id 
            WHERE F.question_id IS NULL  
            """
            result = db.session.execute(sql,{"keywords0":keywords[0], "keywords1":keywords[1],"keywords2":keywords[2],"keywords3":keywords[3]})
            questions = result.fetchall()
        except:
            print("fails")
            return False
    else:
        try:
            sql = """SELECT * FROM questions AS Q
            LEFT JOIN flagged_questions AS F 
            on Q.id = F.question_id 
            WHERE F.question_id IS NULL 
            AND  (
                (Q.keyword1 IN (:keywords0, :keywords1, :keywords2, :keywords3)
            AND Q.keyword1 <> '')
            OR  (Q.keyword2 IN (:keywords0, :keywords1, :keywords2, :keywords3)
            AND Q.keyword2 <> '')
            OR  (Q.keyword3 IN (:keywords0, :keywords1, :keywords2, :keywords3)
            AND Q.keyword3 <> '')
            OR  (Q.keyword4 IN (:keywords0, :keywords1, :keywords2, :keywords3)
            AND Q.keyword4 <> '')
            ) 
            """
            result = db.session.execute(sql,{"keywords0":keywords[0], "keywords1":keywords[1],"keywords2":keywords[2],"keywords3":keywords[3]})
            questions = result.fetchall()
        except:
            print("fails")
            return False
    return questions

def fill_with_rest_with_random(questions, how_many):
    temp = [q[0] for q in questions]
    print (temp)
    additional_questions = get_all_questions()
    
    filterer = filter(lambda a: a[0] not in temp, additional_questions)
    filtered_questions = list(filterer)
    
    shuffle(filtered_questions)
    print("filt", filtered_questions)
    missing = how_many-len(questions)
    print ("missing", missing)
    if len(filtered_questions) < missing:
        return questions
    for i in range(missing):
        questions.append(filtered_questions[i])
        print(i)
    print("quest", questions)
    return questions

#Used when user given constrains return too few questions and user has checked the fill with random checkbox
def get_all_questions():
    
    sql = "SELECT * FROM questions"
    result = db.session.execute(sql)
    questions = result.fetchall()
    return questions

def add_question(question, choices, answer, keywords):
    user_id = session.get("user_id")
    
    if question == "":
        return False
    try:
        sql = """INSERT INTO questions (question, choice1, choice2, choice3, choice4, answer, keyword1,keyword2,keyword3,keyword4, user_id)
                 VALUES (:question, :choice1, :choice2, :choice3, :choice4, :answer, :keyword1,:keyword2, :keyword3, :keyword4, :user_id)"""
        db.session.execute(sql, {"question":question, "choice1":choices[0], "choice2":choices[1], "choice3":choices[2], "choice4":choices[3], "answer":answer, "keyword1":keywords[0],"keyword2":keywords[1],"keyword3":keywords[2],"keyword4":keywords[3], "user_id":user_id})
        db.session.commit()
    except:
        
        return False
    return True

def question_answered(question_id, correct):
    user_id = session.get("user_id")

    try:
        sql = """INSERT INTO answers_given (question_id, user_id, correct)
                 VALUES (:question_id, :user_id, :correct)"""
        db.session.execute(sql, {"question_id": question_id, "user_id" :user_id, "correct" :correct})
        db.session.commit()
    except:
        return False    
    return True 

#used for autocomplete
def get_all_keywords():
    
    try:
        sql= " SELECT keyword1, keyword2, keyword3, keyword4 FROM questions"
        result = db.session.execute(sql)
        all_keywords = result.fetchall()
    except:
        return False
    suggestions =[word for word in all_keywords for word in word]
    suggestions = list(dict.fromkeys(suggestions))
    #print (suggestions)
    ##for subset in all_keywords:
    ##    suggestions += subset[0][1:-1].split(",")    
    return suggestions
