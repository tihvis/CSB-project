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
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if password == user.password:
            # Corrected check for hashed password
            # if check_password_hash(user.password, password):
            session["username"] = username
            return True
        else:
            return False
            
def username():
    return session.get("username", "")

def update(username, new_username):
    sql = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":str(username)})
    user_id = result.fetchone()[0]
    if not user_id:
        return False
    else:
        sql = f"UPDATE users SET username='{str(new_username)}' WHERE id={user_id}"
        db.session.execute(text(sql))
        db.session.commit()
        session["username"] = new_username
        return True