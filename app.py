from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

@app.route("/")
def index():
    result = db.session.execute("SELECT * FROM questions")
    messages = result.fetchall()
    return render_template("index.html", count=len(messages), messages=messages) 

#SAVED THIS FOR FUTURE REFERENCE CAN BE IGNORED AND WILL VANISH SOON 
#@app.route("/send", methods=["POST"])
#def send():
#    content = request.form["content"]I
#    sql = "INSERT INTO testi (content) VALUES (:content)"
#    db.session.execute(sql, {"content":content})
#    db.session.commit()
#    return redirect("/")
