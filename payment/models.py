import datetime

from payment import db


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                   unique=True)
    currency = db.Column(db.String(3))
    amount = db.Column(db.Float)
    time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    description = db.Column(db.String(300))
