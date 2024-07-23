from . import db

class Floor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True, nullable=False)
    rooms = db.relationship('Room', backref='floor', lazy=True)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    floor_id = db.Column(db.Integer, db.ForeignKey('floor.id'), nullable=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(50), db.ForeignKey('room.name'), nullable=False)
    floor = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(10), nullable=False)
    initials = db.Column(db.String(10), nullable=False)

