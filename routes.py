from app import app
import users
from flask import flash, request, render_template, redirect, session

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    first_name = request.form["first_name"]
    username = request.form["username"]
    password = request.form["password"]
    if not 0 < len(first_name) < 31:
        return render_template("error.html", message="First name must be 1-30 characters long.")
    if not 3 < len(username) < 41:
        return render_template("error.html", message="Username must be 4-40 characters long.")
    if not 7 < len(password) < 41:
        return render_template("error.html", message="Password must be 8-40 characters long.")
    if users.register(first_name, username, password):
        flash("Thank you for registering, you can now login.")
        return redirect("/")
    else:
        return render_template("error.html", message="Something went wrong, please try again.")

        
@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if users.login(username, password):
        session["username"] = username
        return redirect("/")
    else:
        return render_template("error.html", message="No matches with the given username and password, please try again.")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")