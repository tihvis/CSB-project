from flask import flash, request, render_template, redirect, session
from app import app
import users
import messages

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    if not 3 < len(username) < 41:
        return render_template("error.html", message="Username must be 4-40 characters long.")
    if not 7 < len(password) < 41:
        return render_template("error.html", message="Password must be 8-40 characters long.")
    if users.register(username, password):
        flash("Thank you for registering, you are now logged in and can start messaging.")
        return redirect("/")
    else:
        return render_template("error.html", message="Please try to register again.")

        
@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if not users.login(username, password):
        return render_template("error.html", message="No matches with the given username and password, please try again.")
    session["username"] = username
    return redirect("/")

@app.route("/change_username")
def change_username():
    return render_template("change_username.html")

@app.route("/update_username", methods=["POST"])
def update_username():
    new_username = request.form["new_username"]
    if users.update_username(new_username):
        flash("Your username has now been changed.")
        return redirect("/")
    else:
        return render_template("error.html", message="We couldn't update your information, please try again.")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/new_message")
def new_message():
    return render_template("new_message.html")

@app.route("/send", methods=["POST"])
def send():
    message = request.form["message"]
    if messages.send(message):
        flash("Your message has been saved!")
        return redirect("/")
    else:
        return render_template("error.html", message="...")
    
@app.route("/list", methods=["GET"])
def list():
    list = messages.list()
    print("lista on", list)
    return render_template("list.html", messages=list)