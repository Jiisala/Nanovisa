from app import app
from flask import Flask, flash, session
from flask import redirect, render_template, request
from services import users
from services import questions

question_set = []


@app.route("/")
def index():
    if not users.check_logged():
        return render_template("login.html")
    suggestions = questions.get_all_keywords()
    
    return render_template("index.html", suggestions = suggestions) 

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
    #print("TÄÄLLÄ OLLAAN")
    if not users.check_logged():
        return render_template("login.html")
    if request.method == "GET":
        #print("UUS KYSYMYS GET")
        suggestions = questions.get_all_keywords()
        #print(suggestions)
        return render_template("newquestion.html", suggestions = suggestions)
    if request.method == "POST":
     #   print("UUS KYSYMSY POST")
        users.check_csrf()
        

        question =request.form["question"]
        answer = request.form["answer"]
        choices = request.form.getlist("choice")
        keywords_rest = request.form.getlist("keywords_rest")
        keywords = [request.form["keywords0"].strip()] 
        for word in keywords_rest:
            keywords.append(word.strip())
            
                    
      #  print("lisäämässä täällä")
        if not questions.add_question(question, choices, answer, keywords):
            flash("Syystä tai toisesta kysymyksen lisääminen meni pieleen", "error")
            return render_template("newquestion.html")
        suggestions = questions.get_all_keywords()
        flash(f'Kysymys:" {question} "lisätty.', "message success")            
        return render_template("newquestion.html", suggestions= suggestions)
#PARAMETERS HERE
@app.route("/game_start", methods=["POST"])
def full_game():
    
    how_many = int(request.form.get("how_many"))
    keywords = request.form.getlist("keywords")
    include_own= request.form.get("include_own")
    include_answered= request.form.get("include_answered")

    fill_with_random = request.form.get("fill_with_random")
    print(fill_with_random)
    global question_set 
    question_set= questions.get_new_question_set(how_many, keywords, include_own, include_answered, fill_with_random )
    
    return redirect("game/0")

@app.route("/game/<int:id>")
def one_question(id):
    global question_set
    if id >= len(question_set): 
        return redirect("/results")
    id +=1
    return render_template("game.html", id=id, question=question_set[id-1])    

@app.route("/results")
def results():
    global question_set
    return render_template("results.html", temp =question_set )
    
@app.route("/answer", methods=["POST"])
def answered_question():
    users.check_csrf()
    question_id = request.form["id"]
    correct = request.form["answer"] == request.form["correct_answer"]
    questions.question_answered(question_id, correct)
    return redirect(f"/game/{question_id}")

@app.route("/logout")

def logout():
    if not users.check_logged():
        return render_template("login.html")
    users.logout()
    return redirect("/")