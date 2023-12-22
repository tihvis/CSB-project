from db import db
import user
from sqlalchemy.sql import text
import datetime 

def save_message(message):
    user_id = user.user_id()
    if user_id is None:
        return False
    if not 1 <= len(message) <= 1000:
        return False
    visibility = True
    sql = "INSERT INTO messages (message, user_id, sent_at, visibility) VALUES (:message, :user_id, NOW(), :visibility)"
    db.session.execute(text(sql), {"message":message, "user_id":user_id, "visibility":visibility})
    db.session.commit()
    return True

def list():
    sql = "SELECT M.id, M.message, U.username, M.sent_at FROM messages M LEFT JOIN users U ON U.id=M.user_id WHERE M.visibility=True ORDER BY M.id"
    result = db.session.execute(text(sql))
    return result.fetchall()

def delete(messages_to_delete):
    try:
        for id in messages_to_delete:
            sql = "UPDATE messages SET visibility = False WHERE id=:id"
            db.session.execute(text(sql), {"id":id})
            db.session.commit()
        return True
    except:
        return False

