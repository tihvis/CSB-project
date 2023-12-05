from db import db
import users
from sqlalchemy.sql import text
import datetime 

def send(message):
    username = users.username()
    if username == "":
        return False
    visibility = True
    sql = "INSERT INTO messages (message, user_id, sent_at, visibility) VALUES (:content, :user_id, NOW(), :visibility)"
    db.session.execute(text(sql), {"message":message, "user_id":user_id, "visibility":visibility})
    db.session.commit()
    return True

def list():
    sql = "SELECT M.message, U.username, M.sent_at FROM messages M, users U WHERE M.user_id=U.id ORDER BY M.id"
    result = db.session.execute(text(sql))
    return result.fetchall()

