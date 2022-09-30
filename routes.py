from app import app
from flask import Flask, flash
from flask import redirect, render_template, request
from services import users
from services import questions

@app.route("/")
def index():
    if not users.check_logged():
        return render_template("login.html")

    return render_template("index.html") 

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not users.login(username, password):
            flash("virheellinen käyttäjätunnus tai salasana", "error_login")
        return redirect("/")

@app.route("/newuser", methods=["POST"])
def login_user():
    username = request.form["username"]
    password = request.form["password"]
    pwcheck = request.form["passwordAgain"]
    if password != pwcheck:
        flash("syötä sama salasana kahdesti", "error_new_user")
    elif not users.new_user(username, password):
        flash("Syystä tai toisesta käyttäjän luominen ei onnistunut", "error_new_user")
    
    return redirect("/")

#TODO muista tutkia miten lomakkeen saisi säilyttämään tiedot jos jotain menee pieleen
@app.route("/newquestion", methods=["GET", "POST"])
def new_question():
    if not users.check_logged():
        return render_template("login.html")
    if request.method == "GET":
        return render_template("newquestion.html")
    if request.method == "POST":
        users.check_csrf()

        question =request.form["question"]
        answer = request.form["answer"]
        choices = request.form.getlist("choice")
        keywords = [request.form["keywords0"]] + request.form.getlist("keywords_rest")

        if not questions.add_question(question, choices, answer, keywords):
            flash("Syystä tai toisesta kysymyksen lisääminen meni pieleen", "error")
            return render_template("newquestion.html")
        
        flash(f'Kysymys:" {question} "lisätty.', "message success")            
        return render_template("newquestion.html", question= question)

@app.route("/game/<int:id>")
def one_question(id):
    question_set = questions.get_all_questions()    
    if id >= len(question_set):
        #This will ultimately render the results view 
        return redirect("/")
    id +=1
    return render_template("game.html", id=id, question=question_set[id-1])    

@app.route("/answer", methods=["POST"])
def answered_question():
    users.check_csrf()
    question_id = request.form["id"]
    correct = request.form["answer"] == request.form["correct_answer"]
    #    print("correct")
    #    #This will of course get replaced by some magnificent program logic later
    #print("wrong")
    questions.question_answered(question_id, correct)
    return redirect(f"/game/{question_id}")

@app.route("/logout")

def logout():
    if not users.check_logged():
        return render_template("login.html")
    users.logout()
    return redirect("/")