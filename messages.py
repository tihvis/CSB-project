from db import db
import users
from sqlalchemy.sql import text
import datetime 

def send(message):
    user_id = users.user_id()
    print("user id on", user_id)
    if user_id == "":
        return False
    visibility = True
    sql = "INSERT INTO messages (message, user_id, sent_at, visibility) VALUES (:message, :user_id, NOW(), :visibility)"
    db.session.execute(text(sql), {"message":message, "user_id":user_id, "visibility":visibility})
    db.session.commit()
    return True

def list():
    sql = "SELECT M.message, U.username, M.sent_at FROM messages M LEFT JOIN users U ON U.id=M.user_id WHERE M.visibility=True ORDER BY M.id"
    result = db.session.execute(text(sql))
    return result.fetchall()

