from werkzeug.security import check_password_hash, generate_password_hash
from db import db
from flask import session
from sqlalchemy.sql import text

def register(username, password):
# FLAW 1: Cryptographic Failures
    is_admin = False
    try:
    # Wrong way, where password is saved as it is:
        sql = "INSERT INTO users (username, password, is_admin) VALUES (:username, :password, :is_admin)"
        db.session.execute(text(sql), {"username":username, "password":password, "is_admin":is_admin})
        db.session.commit()
    # Corrected version, where password is saved as a hash value:
        # hash_value = generate_password_hash(password)
        # sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        # db.session.execute(text(sql), {"username":username, "password":hash_value, "is_admin":is_admin})
        # db.session.commit()
    except:            
        return False
    return login(username, password)

def login(username, password):
    sql = "SELECT id, username, password, is_admin FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if password == user.password:
            # Corrected check for hashed password
            # if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.username
            session["admin"] = user.is_admin
            return True
        
def logout():
    del session["user_id"]
    del session["username"]
    del session["admin"]
    return True

def user_id():
    return session.get("user_id")

def is_logged_in():
    if user_id() is None:
        return False
    else:
        return True
    
def is_admin():
    if session["admin"]:
        return True
    else:
        return False
    
def username_in_use(username):
    sql = "SELECT id, username FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()
    if user:
        return True
    return False

def update_username(new_username):
    user_id_value = user_id()
    if user_id_value is None:
        return False
    else:
        #FLAW 2: INJECTION
        #This allows user to type in for example "username, is_admin=True", and get admin rights.
        db.session.execute(text("UPDATE users SET username='" + new_username + "' WHERE id=" + str(user_id_value)))
        #Corrected version:
        #if new_username 
            #sql = "UPDATE users SET username=:new_username WHERE user_id=:user_id"
            #db.session.execute(text(sql), {"username":new_username, "user_id":user_id}
        db.session.commit()
        session["username"] = new_username
        return True