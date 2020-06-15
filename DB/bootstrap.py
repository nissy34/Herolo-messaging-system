from DB.database import db
from DB.models.user import User
from DB.models.message import Message
from DB.models.messageReceiver import MessageReceiver


def bootstrap():
    db.create_all()
 