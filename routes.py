from app import app
from flask import Flask
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
            return render_template("error.html", message="Virheellinen käyttäjänimi tai salasana")
        return redirect("/")

@app.route("/newuser", methods=["POST"])
def login_user():
    username = request.form["username"]
    password = request.form["password"]
    pwcheck = request.form["passwordAgain"]
    if password != pwcheck:
        return "Syötä kahdesti sama salasana"
    if not users.new_user(username, password):
        return render_template("error.html", message = "Syystä tai toisesta käyttäjän luominen ei onnistunut")
    
    return redirect("/")


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
        
        if not all(choices):
            return render_template("error.html", message= "Anna neljä vastausvaihtoehtoa")
        keywords =request.form.getlist("keywords")
        if not any([a is not "" for a in keywords]):
            return render_template("error.html", message= "Anna vähintään yksi avainsana")

        print(keywords)
        if not questions.add_question(question, choices, answer, keywords):
            return render_template("error.html", message = "Syystä tai toisesta kysymyksen lisääminen meni pieleen")
        
        return render_template("newquestion.html")

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

    if request.form["answer"] == request.form["correct_answer"]:
        print("correct")
        #This will of course get replaced by some magnificent program logic later
    print("wrong")
    return redirect(f"/game/{request.form['id']}")

@app.route("/logout")

def logout():
    if not users.check_logged():
        return render_template("login.html")
    users.logout()
    return redirect("/")