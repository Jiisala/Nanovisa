import app
from flask import Flask
from flask import redirect, render_template, request
from services import users

@app.route("/")
def index():
 #   result = db.session.execute("SELECT * FROM questions")
 #   messages = result.fetchall()
 #   return render_template("index.html", count=len(messages), messages=messages) 
    return render_template("index.html") 

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not users.login(username, password):
            return "errorhandling goes here"
        return redirect("/")

@app.route("/newuser", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    pwcheck = request.form["passwordAgain"]
    if password != pwcheck:
        return "errorhandling goes here"
    if not users.addNew(username, password):
        return "errorhandling goes here"
    
    return redirect("/")



def newquestion():
    #result = db.session.execute("SELECT * FROM questions")
    #messages = result.fetchall()
    return render_template("newquestion.html") 