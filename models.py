from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import date
db=SQLAlchemy()

class User(db.Model):
    __tablename__="users"
    user_id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(150),unique=True,nullable=False)
    password=db.Column(db.String(255),nullable=False)
    contact=db.Column(db.String(20),nullable=False)
    role=db.Column(db.String(50),nullable=False)
    approved=db.Column(db.Boolean,default=False)
    blacklisted=db.Column(db.Boolean,nullable=False,default=False)

    bookings=db.relationship("Booking",backref="user",lazy=True)
    assigned_treks=db.relationship("Trek",backref="staff",lazy=True,foreign_keys="Trek.assigned_staff_id")

class Trek(db.Model):
    __tablename__="treks"
    trek_id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    location=db.Column(db.String(100),nullable=False)
    difficulty=db.Column(db.String(50),nullable=False)
    duration=db.Column(db.Integer,nullable=False)
    available_slots=db.Column(db.Integer,nullable=False)
    assigned_staff_id=db.Column(db.Integer,db.ForeignKey("users.user_id"),nullable=True)
    status=db.Column(db.String(50),nullable=False)
    start_date=db.Column(db.Date, nullable=False)
    end_date=db.Column(db.Date, nullable=False)

    bookings=db.relationship("Booking",backref="treks",lazy=True)

class Booking(db.Model):
    __tablename__="bookings"
    booking_id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("users.user_id"),nullable=False)
    trek_id=db.Column(db.Integer,db.ForeignKey("treks.trek_id"),nullable=False)
    booking_date=db.Column(db.Date,default=date.today,nullable=False)
    status=db.Column(db.String(50),default="pending",nullable=False)
