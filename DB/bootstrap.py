from DB.database import get_db
from DB.models.user import User
from DB.models.message import Message
from DB.models.messageReceiver import MessageReceiver


def bootstrap():
    db = get_db()
    # db.drop_all()
    db.create_all()
    # user1 = User(username="test1",email="a@a.com")
    # user2 = User(username="test2",email="b@a.com")

    # messsage = Message(message="test",subject="test")
    # user1.sentMessagas.append(messsage)

    # user2.receivedMessages.append(MessageReceiver(message=messsage))

    # db.session.add(user1)
    # db.session.add(user2)
    # db.session.commit()
    # user1 = User.query.filter_by(username="test1").first()
    # user2 = User.query.filter_by(username="test2").first()
    # m1 = Message.query.with_parent(user1).first()
    # m2 = Message.query.with_parent(user2).first()
    # db.session.delete(messsage)
    # db.session.commit()
    # d=4
    # user = User(userName="a",)
