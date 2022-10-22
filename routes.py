from app import app
from flask import flash, session
from flask import redirect, render_template, request
from services import users
from services import questions

@app.context_processor
def context_processor():
    return dict(is_admin =users.check_admin_rights)

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

@app.route("/logout")
def logout():
    if not users.check_logged():
        return render_template("login.html")
    users.logout()
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

@app.route("/newquestion", methods=["GET", "POST"])
def new_question():
    
    if not users.check_logged():
        return render_template("login.html")
    if request.method == "GET":
        suggestions = questions.get_all_keywords()
        
        return render_template("newquestion.html", suggestions = suggestions)
    if request.method == "POST":
        
        question =request.form["question"]
        answer = request.form["answer"]
        choices = request.form.getlist("choice")
        keywords_rest = request.form.getlist("keywords_rest")
        keywords = [request.form["keywords0"].strip()] 
        for word in keywords_rest:
            keywords.append(word.strip())

        if not questions.add_question(question, choices, answer, keywords):
            flash("Syystä tai toisesta kysymyksen lisääminen meni pieleen", "error")
            return render_template("newquestion.html")
        suggestions = questions.get_all_keywords()
        flash(f'Kysymys:" {question} "lisätty.', "message success")            
        return render_template("newquestion.html", suggestions= suggestions)

@app.route("/game_start", methods=["POST"])
def full_game():

    how_many = int(request.form.get("how_many"))
    keywords = request.form.getlist("keywords")
    include_own= request.form.get("include_own")
    include_answered= request.form.get("include_answered")
    fill_with_random = request.form.get("fill_with_random")
    
    questions.get_new_question_set(how_many, keywords, include_own, include_answered, fill_with_random )
    return redirect("game/0")

@app.route("/game/<int:id>")
def one_question(id):
    if not users.check_logged():
        return render_template("login.html")
    if id >= len(session.get("question_set")):
        return redirect("/results")
    id +=1
    return render_template("game.html", id=id)    

@app.route("/results")
def results():
    if not users.check_logged():
        return render_template("login.html")
    user_score = questions.get_user_score()
    position = questions.get_user_position()
    return render_template("results.html",  user_score = user_score, position = position )
    
@app.route("/answer", methods=["POST"])
def answered_question():
    id = request.form.get("id")
    question_id = session["question_set"][int(id)]["id"]
    question_user_id = session["question_set"][int(id)]["user_id"]
    answer = int(request.form.get("answer"))
    correct_or_not =  answer == int(session["question_set"][int(id)]["answer"])
    if session.get("user_id") == question_user_id:
        session["question_set"][int(id)]["player_answer"] = answer
        session["question_set"][int(id)]["new_question"] = False
      
    elif questions.question_answered(question_id, correct_or_not):
        session["question_set"][int(id)]["player_answer"] = answer
        session["question_set"][int(id)]["new_question"] = True
    else:
        session["question_set"][int(id)]["player_answer"] = answer
        session["question_set"][int(id)]["new_question"] = False
      
    return redirect(f"/game/{id}")

@app.route("/highscores")
def highscores():
    if not users.check_logged():
        return render_template("login.html")
    highscorelist = questions.count_highscore()
    return render_template("highscores.html", highscorelist = highscorelist)

@app.route("/flag_question", methods=["POST"])
def tag_question():
    id = request.form.get("id")
    return render_template("flag.html", id = id)

@app.route("/confirm_flag", methods=["POST"])
def confirm_flag():
    question_id = request.form.get("id")
    reason = request.form.get("reason")
    try:
        print("routes", question_id, reason)
        questions.flag_question(question_id,reason)
    except:
        print("error handling goes here, when I get around adding it")
    return render_template("results.html")

@app.route("/admin")
def admin():
    if users.check_admin_rights():
        flagged_questions = questions.get_flagged_questions()
        return render_template("admin.html", flagged_questions= flagged_questions)
    return redirect("/")

@app.route("/deal_with_flagged_question", methods=["POST"])
def deald_with_flagged_questions():
    action = request.form.get("deal_with_flag").split(" ")

    if users.check_admin_rights():
        if action[0] == "remove_flag":
            questions.remove_flag(int(action[1]))
        if action[0] == "remove_question":
            questions.remove_question(int(action[1]))
        if action[0] == "update_question":
            return redirect (f"updatequestion/{action[1]}")
                
    return redirect("/admin")

@app.route("/updatequestion/<int:id>", methods=["GET", "POST"])
def update_question(id):
    question_to_update = questions.get_one_question(id)
    if request.method == "GET":
        return render_template("updatequestion.html", id = id, question = question_to_update)
    if request.method == "POST":
        
        question =request.form["question"]
        answer = request.form["answer"]
        choices = request.form.getlist("choice")
        keywords_rest = request.form.getlist("keywords_rest")
        keywords = [request.form["keywords0"].strip()] 
        for word in keywords_rest:
            keywords.append(word.strip())

        if not questions.update_question(question_to_update[0],question_to_update[11] ,question, choices, answer, keywords):
            flash("Syystä tai toisesta kysymyksen päivittäminen meni pieleen", "error")
            return render_template("updatequestion.html", id = id, question = question_to_update)
        question_to_update = questions.get_one_question(id)
        questions.remove_flag(id)
        flash(f'Kysymys: {question_to_update[0]} päivitetty.', "message success")            
        return redirect("/admin")
        
    return redirect("/admin")

@app.route("/updateuser", methods=["POST"])
def update_user():
    user_id = request.form.get("user_id")
    if request.form.get("action") == "oikeudet":
        
        admin_status = users.toggle_admin(user_id)
        if admin_status:
            flash(f'Käyttäjän {user_id} ylläpito oikeus on nyt: {admin_status}', "message success")
        else:
            print("HERE")
            flash(f"Käyttäjää {user_id} ei löytynyt, tarkista ID", "message error")
            

    if request.form.get("action") == "poista":
        try:
            users.remove_user(user_id)
            flash(f'Käyttäjän {user_id} on nyt poistettu', "message success")
        except:
            flash("Syystä tai toisesta käyttäjää ei voitu poistaa", "message error")
                
    return redirect("/admin")

@app.route("/profile")
def profile():
    return render_template("profile.html")