from datetime import datetime

from gino import Gino

db = Gino()


class Conversation(db.Model):
    __tablename__ = 'conversations'

    uid = db.Column(db.Integer(), primary_key=True)


class Message(db.Model):
    __tablename__ = 'messages'

    uid = db.Column(db.Integer(), primary_key=True)
    conversation_uid = db.Column(db.Integer, db.ForeignKey('conversations.uid'))
    author_uid = db.Column(db.Integer, db.ForiegnKey('users.uid'))
    text = db.Column(db.Unicode(), nullable=True)
    created = db.Column(db.DateTime(), default=datetime.now)
