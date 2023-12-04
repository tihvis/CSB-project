from db import db
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text

def user_id():
    return session.get("user_id", 0)

def register(first_name, username, password):
# FLAW 1: Cryptographic Failures
# In the first sql-query, the password is not saved in the db using  cryptographic keys.
# The second query is a corrected version to the secure_users table.
    hash_value = generate_password_hash(password)
    is_admin = False
    try:
    # Wrong way:
        sql = "INSERT INTO users (first_name, username, password, is_admin) VALUES (:first_name, :username, :password, :is_admin)"
        db.session.execute(text(sql), {"first_name":first_name, "username":username, "password":password, "is_admin":is_admin})
        db.session.commit()
        print("eka taulu onnistui")
    # Corrected version:
        sql = "INSERT INTO secure_users (first_name, username, password) VALUES (:first_name, :username, :password)"
        db.session.execute(text(sql), {"first_name":first_name, "username":username, "password":hash_value, "is_admin":is_admin})
        db.session.commit()
        print("toka taulu onnistu")
    except:
        print("return false")
        return False
    print("loginiin ohjaus")
    return login(username, password)


def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    # sql = "SELECT id, password FROM secure_users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()
    print("user on", user)
    if not user:
        return False
    else:
        if password == user.password:
#In the original program, the password has not been saved to the db using the hash-method,
#If the generate_password_hash function would have been used, then the commented code below would work.
#        if check_password_hash(user.password, password):
            session["username"] = username
            return True
        else:
            return False