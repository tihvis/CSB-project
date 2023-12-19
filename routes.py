from flask import flash, request, render_template, redirect, session
from app import app
import re
import user
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
    if not 7 < len(password) < 41 or not re.search("[0-9]", password) or not re.search("[A-Z]", password):
        return render_template("error.html", message="Password must be 8-40 characters long and include atleast one number and one capital letter.")
    if user.username_in_use(username):
        return render_template("error.html", message="The username you chose is already in use, please choose another one.")
    if user.register(username, password):
        flash("Thank you for registering, you are now logged in and can start messaging.")
        return redirect("/")
    else:
        return render_template("error.html", message="Please try to register again.")

        
@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if user.login(username, password):
        return redirect("/")
    else:
        return render_template("error.html", message="No matches with the given username and password, please try again.")

@app.route("/update_username", methods=["GET", "POST"])
def update_username():
    if request.method == "GET":
        if user.is_logged_in():
            return render_template("update_username.html")
        else:
            return render_template("error.html", message="You do not have access to this page, please login to continue.")
    
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        new_username = request.form["new_username"]
        if user.username_in_use(new_username):
            return render_template("error.html", message="The username is already in use, please choose another one.")
        if user.update_username(new_username):
            flash("Your username has now been changed.")
            return redirect("/")
        else:
            return render_template("error.html", message="We couldn't update your information, please try again.")

@app.route("/logout")
def logout():
    if user.logout():
        flash("You have now been logged out.")
        return redirect("/")
    else:
        return render_template("error.html", message="Please try again.")

@app.route("/new_message", methods=["GET", "POST"])
def new_message():
    if request.method == "GET":
        if user.is_logged_in():
            return render_template("new_message.html")
        else:
            return render_template("error.html", message="You do not have access to this page, please login to continue.")
        
    if request.method == "POST":
        #FLAW 1: Missing CSRF-protection
        # This method is not checking whether the session related csrf_token is valid.

        # CSRF-check added below as comments. The html-form related to this already has the CSRF-token as a hidden input.
        # if session["csrf_token"] != request.form["csrf_token"]:
        #     abort(403)

        message = request.form["message"]
        if messages.save_message(message):
            flash("Your message has been saved!")
            return redirect("/")
        else:
            return render_template("error.html", message="Please try again.")
    
@app.route("/list", methods=["GET"])
def list():
    if user.is_logged_in():
        message_list = messages.list()
        if len(message_list) == 0:
            return render_template("error.html", message="There are no messages to show yet.")
        else:
            return render_template("list.html", messages=message_list)
    else:
        return render_template("error.html", message="You do not have access to this page, please login to continue.")
    
@app.route("/delete_message", methods=["GET", "POST"])
def delete_message():
    if request.method == "GET":
        message_list = messages.list()
        if len(message_list) < 1:
            return render_template("error.html", message="There are no messages to show yet.")
        return render_template("delete_message.html", messages=message_list)
    
    if request.method == "POST":
        # FLAW 2: Broken access control
        # The below code does not check whether user is admin or not, and thus allows non-admin users
        # and even non-logged in users to view the page and delete messages,
        # if the user types in "/delete_message" after the home page url.

        # The fix for this is commented below:
        # if not user.is_admin():
        #     return render_template("error.html", message="Only admins can delete messages.")

        messages_to_delete = request.form.getlist("message_id")
        if len(messages_to_delete) < 1:
            return render_template("error.html", message="It looks like you didn't choose any restaurants to delete.")
        if messages.delete(messages_to_delete):
            flash("The messages you chose have now been deleted.")
            return redirect("/")
        else:
            return render_template("error.html", message="Please try again.")
