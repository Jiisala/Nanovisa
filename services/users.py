import secrets
from db import db
from flask import request, session
from werkzeug.security import generate_password_hash, check_password_hash
from os import abort

def login(name, password):
    sql = "SELECT id, name, password, admin FROM users WHERE name=:name"
    result = db.session.execute(sql, {"name":name})
    user = result.fetchone()
    if not user:
        return False
    if not check_password_hash(user.password, password):
        return False
    session["csrf_token"]= secrets.token_hex(16)
    session["user_id"] = user.id
    session["user_name"] = user.name
    session["admin"] = user.admin
    return True

def logout():
    del session["user_id"]
    del session["user_name"]
    del session["admin"]
    del session["csrf_token"]      

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

def check_adminRights():
    return session.get("admin") 

def toggleAdmin(id):
    #This is made for future use and is completely untested
    #Admin stuff is yet to be implemented
    if check_adminRights():
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

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)