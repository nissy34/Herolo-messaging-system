from DB.database import get_db

db = get_db()


class MessageReceiver(db.Model):
    message_id = db.Column(db.Integer,
                           db.ForeignKey('message.id'),
                           primary_key=True)
    receiver_id = db.Column(db.Integer,
                            db.ForeignKey('user.id'),
                            primary_key=True)
    read = db.Column(db.Boolean,
                     nullable=False,
                     default=False)
    message = db.relationship("Message", back_populates="receiver")
    receiver = db.relationship("User", back_populates="receivedMessages")
