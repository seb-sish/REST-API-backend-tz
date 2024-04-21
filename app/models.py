from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    reg_date = db.Column(db.DateTime, index=True, default=datetime.now, nullable=False)
    
    @property
    def serialize(self):
       return {
           "id": self.id,
           "username": self.username,
           "email": self.email,
           "reg_date": self.dump_datetime(self.reg_date)
       }
    
    def dump_datetime(self, value):
        if value is None: return ""
        return [value.strftime("%d-%m-%Y"), value.strftime("%H:%M:%S")]

    def __repr__(self):
        return '<User {}>'.format(self.username) 