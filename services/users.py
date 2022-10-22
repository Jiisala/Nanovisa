from db import db
from flask import request, session
from werkzeug.security import generate_password_hash, check_password_hash

def login(name, password):
    sql = "SELECT id, name, password, admin FROM users WHERE name=:name"
    result = db.session.execute(sql, {"name":name})
    user = result.fetchone()
    if not user:
        return False
    if not check_password_hash(user.password, password):
        return False
    print(user.id, user.name)
    session["user_id"] = user.id
    session["user_name"] = user.name
    return True

def logout():
    del session["user_id"]
    del session["user_name"]

def check_logged():
    return session.get("user_id")

def new_user(name, password, admin=False):
    if name == "" or password == "":
        return False

    pwhash = generate_password_hash(password)
    try:
        sql = """INSERT INTO users (name, password, admin)
                 VALUES (:name, :password, :admin)"""
        db.session.execute(sql, {"name":name, "password":pwhash, "admin":admin})
        db.session.commit()
    except:
        return False
    return login(name, password)  

def check_admin_rights():
    user_id = session.get("user_id")
    try:
        sql = "SELECT admin FROM users WHERE id=:user_id"
        result = db.session.execute(sql, {"user_id":user_id})
        is_admin = result.fetchone()
    except:
        return False
        
    return is_admin[0]

def toggle_admin(user_id):
    
    if check_admin_rights():
            
        sql = """UPDATE users 
        SET admin = NOT admin
        WHERE id = :user_id
        RETURNING admin"""
                
        result = db.session.execute(sql, {"user_id":user_id})
        db.session.commit()
        admin = result.fetchone()
        
    return admin

def remove_user(user_id):
    if check_admin_rights():
            
        sql = "DELETE FROM users WHERE id = :user_id RETURNING id"
                
        result = db.session.execute(sql, {"user_id":user_id})
        db.session.commit()
        user = result.fetchone()
    
    return user

def get_id_for_name(user_name):

    sql = "SELECT id FROM users WHERE name = :user_name"
    result = db.session.execute(sql, {"user_name":user_name})
    db.session.commit()
    user_id = result.fetchone()

    return user_id

def get_name_for_id(user_id):

    sql = "SELECT name FROM users WHERE id = :user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    db.session.commit()
    user_name = result.fetchone()

    return user_name


def send_message(receiver_id, message):
    user_id = session.get("user_id")

    try:
        sql = """INSERT INTO messages (from_id, to_id, content)
                 VALUES (:from_id, :to_id, :content)"""
        db.session.execute(sql, {"from_id":user_id, "to_id":receiver_id, "content":message})
        db.session.commit()
    except:
        return False
    return True  

def get_messages():
    user_id = session.get("user_id")

    sql = "SELECT * FROM messages WHERE to_id = :user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    messages = result.fetchall()

    return messages

