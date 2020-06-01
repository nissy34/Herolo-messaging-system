from datetime import datetime
from DB.database import get_db

db = get_db()

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    sender_id = db.Column(db.Integer,
                          db.ForeignKey('user.id'))

    sender = db.relationship("User", back_populates="sentMessagas")
    receiver = db.relationship("MessageReceiver", back_populates="message", cascade="all")
 
    message = db.Column(db.String(120), unique=False, nullable=False)
    subject = db.Column(db.String(120), unique=False, nullable=False)
    creation_date = db.Column(
        db.DateTime, unique=False, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.username
