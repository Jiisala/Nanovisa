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

def toggleAdmin(id):
    #This is a scetch made for future use and is completely untested
    #Admin stuff is yet to be implemented completely
    if check_admin_rights():
        sql = "SELECT admin FROM users WHERE id=:id"
        result = db.session.execute(sql, {"id":id})

        user = result.fetchone()
        isAdmin = not user.admin
        try:
            sql = "UPDATE users SET admin =:isAdmin WHERE id=:id"
                    
            db.session.execute(sql, {"admin":isAdmin})
            db.session.commit()
        except:
            return False

def banUser(id):
    #placeholder for future use
    pass

