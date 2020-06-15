from DB.database import get_db

db = get_db()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    receivedMessages = db.relationship("MessageReceiver", back_populates="receiver", cascade="all")
    sentMessagas = db.relationship('Message', back_populates="sender", cascade="all")
   
   
    def __repr__(self):
        return '<User %r>' % self.username
