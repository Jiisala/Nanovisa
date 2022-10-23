from flask import flash, session
from flask import redirect, render_template, request
from app import app
from services import users
from services import questions

@app.context_processor
def context_processor():
    return dict(is_admin= users.check_admin_rights)

@app.route("/")
def index():
    if not users.check_logged():
        return render_template("login.html")
    suggestions = questions.get_all_keywords()
    return render_template("index.html", suggestions= suggestions)

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
    if len(username) > 20:
        flash("Nimen maksimipituus on 20 merkkiä", "error_new_user")
    elif not users.new_user(username, password):
        flash("Syystä tai toisesta käyttäjän luominen ei onnistunut", "error_new_user")

    return redirect("/")

@app.route("/newquestion", methods=["GET", "POST"])
def new_question():

    if not users.check_logged():
        return render_template("login.html")
    if request.method == "GET":
        suggestions = questions.get_all_keywords()

        return render_template("newquestion.html", suggestions= suggestions)
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
    admin=users.check_admin_rights()
    return render_template("results.html", user_score = user_score, position = position, admin= admin)

@app.route("/answer", methods=["POST"])
def answered_question():
    id = request.form.get("id")
    question_id = session["question_set"][int(id)]["id"]
    question_user_id = session["question_set"][int(id)]["user_id"]
    answer = int(request.form.get("answer"))
    correct_or_not =  answer == int(session["question_set"][int(id)]["answer"])

    if session.get("user_id") == question_user_id or users.check_admin_rights():
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

# I'm pretty sure that error handling here is completely uneccesary.
# The flashed message is not shown anywhere.
# However I can't remember why I added it and I'm afraid that if
# I remove it, something will break.
@app.route("/confirm_flag", methods=["POST"])
def confirm_flag():
    question_id = request.form.get("id")
    reason = request.form.get("reason")
    try:
        questions.flag_question(question_id,reason)
    except:
        flash("Syystä tai toisesta vastalauseen esittäminen epäonnistui", "error")

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

@app.route("/user_update_question", methods=["POST"])
def user_update_question():
    question_id = request.form.get("question_id")

    return redirect(f"/updatequestion/{question_id}")

@app.route("/user_remove_question", methods=["POST"])
def user_remove_question():
    question_id = request.form.get("question_id")
    questions.remove_question(question_id)
    return redirect("/profile")

@app.route("/updatequestion/<int:id>", methods=["GET", "POST"])
def update_question(id):
    question_to_update = questions.get_one_question(id)

    if request.method == "GET":
        if not users.check_logged():
            return render_template("login.html")
        if users.check_admin_rights() or question_to_update[11] == session.get("user_id"):
            return render_template("updatequestion.html",
                                    id= id,
                                    question= question_to_update,
                                    is_admin = users.check_admin_rights
                                    )
    if request.method == "POST":

        question = request.form["question"]
        answer = request.form["answer"]
        choices = request.form.getlist("choice")
        keywords_rest = request.form.getlist("keywords_rest")
        keywords = [request.form["keywords0"].strip()]
        for word in keywords_rest:
            keywords.append(word.strip())

        if not questions.update_question(question_to_update[0], question_to_update[11] ,question, choices, answer, keywords):
            flash("Syystä tai toisesta kysymyksen päivittäminen meni pieleen", "error")
            return render_template("updatequestion.html", id = id, question = question_to_update)
        if users.check_admin_rights():
            questions.remove_flag(id)
            flash(f'Kysymys: {question_to_update[0]} päivitetty.', "message success")
            return redirect("/admin")
        else:
            return redirect("/profile")
    return redirect("/")

@app.route("/updateuser", methods=["POST"])
def update_user():
    user_id = request.form.get("user_id")
    if request.form.get("action") == "oikeudet":
        admin_status = users.toggle_admin(user_id)
        if admin_status:
            flash(f'Käyttäjän {user_id} ylläpito oikeus on nyt: {admin_status}', "message success")
        else:
            flash(f"Käyttäjää {user_id} ei löytynyt, tarkista ID", "message error")

    if request.form.get("action") == "poista":
        user =users.remove_user(user_id)
        if user:
            flash(f'Käyttäjä {user_id} on nyt poistettu', "message success")
        else:
            flash(f"Käyttäjää {user_id} ei löytynyt, tarkista ID", "message error")

    return redirect("/admin")

@app.route("/profile")
def profile():
    if not users.check_logged():
        return render_template("login.html")
    user_questions = questions.get_questions_by_user()
    user_answered = questions.count_questions_answered_by()
    user_position = questions.get_user_position()
    return render_template("profile.html",
                            user_questions = user_questions,
                            user_answered = user_answered,
                            user_position = user_position)

@app.route("/messages", methods=["GET", "POST"])
def messages():
    user_messages = users.get_messages()
    if request.method == "GET":
        if not users.check_logged():
            return render_template("login.html")
        return render_template("messages.html", messages=user_messages, get_name= users.get_name_for_id)
    if request.method == "POST":
        receiver = request.form.get("receiver")
        receiver_id = users.get_id_for_name(receiver)
        message = request.form.get("message")

        if receiver_id:
            users.send_message(receiver_id[0], message)
            flash(f"Viesti lähetetty käyttäjälle {receiver} ", "message success")

        else:
            flash(f"Käyttäjää {receiver} ei löytynyt, tarkista nimi", "message error")

        return render_template("messages.html", messages=user_messages, get_name= users.get_name_for_id)
