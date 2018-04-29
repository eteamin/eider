from datetime import datetime

from gino import Gino

db = Gino()


class Conversation(db.Model):
    __tablename__ = 'conversations'

    uid = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.Unicode(), nullable=True)
    created = db.Column(db.DateTime(), default=datetime.now)
