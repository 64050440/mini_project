# store database
from . import db  # import db from this package equal to using from website import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(100))
    date = db.Column(db.DateTime(timezone=True), default=func.now())  # date
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'))  # foreign key use lower


class User(db.Model, UserMixin):  # reference by user
    id = db.Column(db.Integer, primary_key=True)
    # need to pick maximum length for string in this is 150 #unique is cant have same email as other
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    # multiple note of user relatyion use name of class
    notes = db.relationship('Note')
    bookings = db.relationship('Booking')


class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(10), unique=True, nullable=False)
    bookings = db.relationship('Booking')


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.Integer)
    end_time = db.Column(db.Integer)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    classroom_id = db.Column(db.Integer, db.ForeignKey(
        'classroom.id'))
    user = db.relationship('User', back_populates='bookings')
    classroom = db.relationship('Classroom', back_populates='bookings')
