from db import db
from flask import session
from random import shuffle

# The first function calls bunch of other functions to gather a question set corresponding to user input.
# There propably is a more elegant way of achieving all this, but this works.
# I chose to fetch all of the questions passing the criteria, shuffle them and return needed amount,
# This is due the fact that getting a random sample from database using straight up SQL queries leads 
# to some performance isssues if the database grows. Python on the otherhand seems to handle randomizing 
# relatively nicely.
 
def get_new_question_set(how_many, keywords, include_own, include_answered, fill_with_random ):
    user_id = session.get("user_id")
    if include_own and include_answered:
        questions = get_questions_include_own_and_answered(keywords)
    elif include_own:
        questions = get_questions_include_own(keywords, user_id)
    elif include_answered:
        questions = get_questions_include_answered(keywords, user_id)
    else:
        questions = get_questions_with_all_constrains(keywords, user_id)   
    
    if fill_with_random:
        if len(questions) < how_many:
            questions = fill_with_rest_with_random(questions, how_many)
                
    shuffle(questions)

    if how_many > len(questions):
        how_many = len(questions)

    question_set = {}
    for i in range (1, how_many +1):
        question_set[i] = {
            "id":questions[i-1][0],
            "question": questions[i-1][1],
            "choice1": questions[i-1][2],
            "choice2": questions[i-1][3],
            "choice3": questions[i-1][4],
            "choice4": questions[i-1][5],
            "answer": questions[i-1][6],
            "keyword1": questions[i-1][7],
            "keyword2": questions[i-1][8],
            "keyword3": questions[i-1][9],
            "keyword4": questions[i-1][10],
            "user_id": questions[i-1][11]} 

    session["question_set"] = question_set        
                   

def get_questions_with_all_constrains(keywords, user_id):
    if all(a == '' for a in keywords):
        try:
            sql = """SELECT * FROM questions AS Q
            WHERE Q.id NOT IN(
                SELECT question_id 
                FROM flagged_questions)
            AND
            Q.id NOT IN (
                SELECT question_id
                FROM answers_given
                WHERE user_id = :user_id
            )
            AND Q.user_id <> :user_id
            
            """
            result = db.session.execute(sql,{
                "user_id":user_id, 
                "keywords0":keywords[0], 
                "keywords1":keywords[1],
                "keywords2":keywords[2],
                "keywords3":keywords[3]
                })
            questions = result.fetchall()            
            for q in questions:
                print(q)


        except:
            return False
                
    else:
        try:
            sql = """SELECT * FROM questions AS Q
            WHERE Q.id NOT IN(
                SELECT question_id 
                FROM flagged_questions)
            AND
            Q.id NOT IN (
                SELECT question_id
                FROM answers_given
                WHERE user_id = :user_id
            )
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
            result = db.session.execute(sql,{
                "user_id":user_id, 
                "keywords0":keywords[0], 
                "keywords1":keywords[1],
                "keywords2":keywords[2],
                "keywords3":keywords[3]
                })
            questions = result.fetchall()
        except:
            return False
    return questions    

def get_questions_include_own(keywords, user_id):
    if all(a == '' for a in keywords):
        try:
            sql = """SELECT * FROM questions AS Q
            WHERE Q.id NOT IN(
                SELECT question_id 
                FROM flagged_questions)
            AND
            Q.id NOT IN (
                SELECT question_id
                FROM answers_given
                WHERE user_id = :user_id
            )
            """
            result = db.session.execute(sql,{
                "user_id":user_id, 
                "keywords0":keywords[0], 
                "keywords1":keywords[1],
                "keywords2":keywords[2],
                "keywords3":keywords[3]
                })
            questions = result.fetchall()
        except:
            return False
    else:
        try:
            sql = """SELECT * FROM questions AS Q
            WHERE Q.id NOT IN(
                SELECT question_id 
                FROM flagged_questions)
            AND
            Q.id NOT IN (
                SELECT question_id
                FROM answers_given
                WHERE user_id = :user_id
            )
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
            result = db.session.execute(sql,{
                "user_id":user_id, 
                "keywords0":keywords[0], 
                "keywords1":keywords[1],
                "keywords2":keywords[2],
                "keywords3":keywords[3]
                })
            questions = result.fetchall()
        except:
            return False
    return questions

def get_questions_include_answered(keywords, user_id):
    if all(a == '' for a in keywords):
        try:
            sql = """SELECT * FROM questions AS Q
            WHERE Q.id NOT IN(
                SELECT question_id 
                FROM flagged_questions)
            AND Q.user_id <> :user_id 
            """
            result = db.session.execute(sql,{
                "user_id":user_id, 
                "keywords0":keywords[0], 
                "keywords1":keywords[1],
                "keywords2":keywords[2],
                "keywords3":keywords[3]
                })
            questions = result.fetchall()
        except:
            return False
    else:    
        try:
            sql = """SELECT * FROM questions AS Q
            WHERE Q.id NOT IN(
                SELECT question_id 
                FROM flagged_questions) 
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
            result = db.session.execute(sql,{
                "user_id":user_id, 
                "keywords0":keywords[0], 
                "keywords1":keywords[1],
                "keywords2":keywords[2],
                "keywords3":keywords[3]
                })
            questions = result.fetchall()
        except:
            return False
    return questions

def get_questions_include_own_and_answered(keywords):
    if all(a == '' for a in keywords):
        try:
            sql = """SELECT * FROM questions AS Q
            WHERE Q.id NOT IN(
                SELECT question_id 
                FROM flagged_questions)  
            """
            result = db.session.execute(sql,{
                "keywords0":keywords[0], 
                "keywords1":keywords[1],
                "keywords2":keywords[2],
                "keywords3":keywords[3]
                })
            questions = result.fetchall()
        except:
            return False
    else:
        try:
            sql = """SELECT * FROM questions AS Q
            WHERE Q.id NOT IN(
                SELECT question_id 
                FROM flagged_questions)
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
            result = db.session.execute(sql,{
                "keywords0":keywords[0], 
                "keywords1":keywords[1],
                "keywords2":keywords[2],
                "keywords3":keywords[3]
                })
            questions = result.fetchall()
        except:
            return False
    return questions

def fill_with_rest_with_random(questions, how_many):
    temp = [q[0] for q in questions]
    additional_questions = get_all_questions()
    
    filterer = filter(lambda a: a[0] not in temp, additional_questions)
    filtered_questions = list(filterer)
    
    shuffle(filtered_questions)
    missing = how_many-len(questions)
    if len(filtered_questions) < missing:
        
        for q in filtered_questions:
            questions.append(q)
          
        return questions
    for i in range(missing):
        questions.append(filtered_questions[i])
    
    return questions

def get_all_questions():
    
    sql = """SELECT * FROM questions AS Q
            WHERE Q.id NOT IN(
                SELECT question_id 
                FROM flagged_questions)
            """
    result = db.session.execute(sql)
    questions = result.fetchall()
    return questions

def get_one_question(question_id):
    
    sql = """SELECT * FROM questions 
            WHERE id = :question_id"""
    result = db.session.execute(sql, {"question_id":question_id})
    question = result.fetchone()
    return question

def add_question(question, choices, answer, keywords):
    user_id = session.get("user_id")
    
    if question == "":
        return False
    try:
        sql = """INSERT INTO questions (question, choice1, choice2, choice3, choice4, answer, keyword1,keyword2,keyword3,keyword4, user_id)
                 VALUES (:question, :choice1, :choice2, :choice3, :choice4, :answer, :keyword1,:keyword2, :keyword3, :keyword4, :user_id)"""
        db.session.execute(sql, {
            "question":question, 
            "choice1":choices[0], 
            "choice2":choices[1], 
            "choice3":choices[2], 
            "choice4":choices[3], 
            "answer":answer, 
            "keyword1":keywords[0],
            "keyword2":keywords[1],
            "keyword3":keywords[2],
            "keyword4":keywords[3], 
            "user_id":user_id})
        db.session.commit()
    except:
        return False
    return True

def update_question(question_id, user_id, question, choices, answer, keywords):
    
    
    if question == "":
        return False
    try:
        sql = """UPDATE questions 
            SET 
            question = :question, 
            choice1 = :choice1, 
            choice2 =:choice2, 
            choice3 =:choice3, 
            choice4 =:choice4, 
            answer = :answer, 
            keyword1 = :keyword1,
            keyword2 = :keyword2,
            keyword3 = :keyword3,
            keyword4 = :keyword4, 
            user_id = :user_id
                 WHERE id = :question_id
                  
                 """
        db.session.execute(sql, {
            "question_id":question_id,
            "question":question, 
            "choice1":choices[0], 
            "choice2":choices[1], 
            "choice3":choices[2], 
            "choice4":choices[3], 
            "answer":answer, 
            "keyword1":keywords[0],
            "keyword2":keywords[1],
            "keyword3":keywords[2],
            "keyword4":keywords[3], 
            "user_id":user_id})
        db.session.commit()
    except:
        return False
    return True

def question_answered(question_id, correct):
    user_id = session.get("user_id")
    print("bäkkär qid uid", question_id, user_id )
    try:
        sql = """INSERT INTO answers_given (question_id, user_id, correct)
                 VALUES (:question_id, :user_id, :correct)"""
        db.session.execute(sql, {"question_id": question_id, "user_id" :user_id, "correct" :correct})
        db.session.commit()
    except:
        return False    
    return True 

def count_highscore():
    try:
        sql = """SELECT A.id, A.name, count(B.correct) FROM answers_given AS B 
        JOIN users AS A on A.id = B.user_id 
        WHERE correct = TRUE 
        GROUP BY A.id 
        ORDER BY (count) DESC
        """
        result = db.session.execute(sql)
        highscores = result.fetchall()
    except:
        return False
    return highscores

def get_user_score():
    user_id = session.get("user_id")
    try:
        sql = """SELECT COUNT(correct) FROM answers_given as A
        WHERE A.correct = TRUE and user_id = :user_id
        """
        result = db.session.execute(sql, {"user_id":user_id})
        user_score = result.fetchone()
    except:
        return False
    return user_score

def get_user_position():
    highscores = count_highscore()
    position = [a for a, b in enumerate(highscores) if b[0] == session.get("user_id")]
    return position

#used for autocomplete
def get_all_keywords():
    
    try:
        sql= " SELECT keyword1, keyword2, keyword3, keyword4 FROM questions"
        result = db.session.execute(sql)
        all_keywords = result.fetchall()
    except:
        return []
    suggestions =[word for word in all_keywords for word in word]
    suggestions = list(dict.fromkeys(suggestions)) 
    return suggestions

def flag_question(id, reason):
    user_id = session.get("user_id")
    question_id = session["question_set"][id]["id"]
    try:
        sql="""INSERT INTO flagged_questions (question_id, flagger_id, reason)
            VALUES(:question_id, :user_id, :reason)"""
        db.session.execute(sql, {"question_id":question_id, "user_id":user_id, "reason":reason})
        db.session.commit()
    except:
        return False
    return True

def get_flagged_questions():
    try:
        sql="""SELECT a.*, b.flagger_id, b.reason FROM questions AS a 
        JOIN flagged_questions AS b
        ON a.id = b.question_id"""
        result = db.session.execute(sql)
        flagged_questions = result.fetchall()
    except:
        return False
    return flagged_questions

def remove_flag(question_id):
    try:
        sql = """DELETE FROM flagged_questions WHERE question_id = :question_id"""
        db.session.execute(sql, {"question_id":question_id})
        db.session.commit()
    except:
        return False
    return True

def remove_question(question_id):
    try:
        sql = """DELETE FROM questions WHERE id = :question_id"""
        db.session.execute(sql, {"question_id":question_id})
        db.session.commit()
    except:
        return False
    return True