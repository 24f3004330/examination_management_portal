from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime 

db = SQLAlchemy()

class User(UserMixin, db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(100),unique=True,nullable=False)
    password = db.Column(db.String(100),nullable=False)
    role = db.Column(db.String(10),nullable=False)

    slots = db.relationship('ExamSlot', backref='examiner', lazy=True,foreign_keys='ExamSlot.examiner_id')
    bookings = db.relationship('Booking', backref='student', lazy=True,foreign_keys='Booking.student_id')

class ExaminerProfile(db.Model):

    __tablename__ = 'examiner_profile'

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),unique=True,nullable=False)
    name = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(20), default='pending')

    user = db.relationship('User', backref=db.backref('examiner_profile', uselist=False, cascade='all, delete-orphan'))

class Course(db.Model):

    __tablename__ = 'Course'

    id = db.Column(db.Integer,primary_key=True)
    code = db.Column(db.String(10),unique=True,nullable=False)
    description = db.Column(db.Text, default='')
    status = db.Column(db.String(20),default='active')

    examinations = db.relationship('Examination', backref='course', lazy=True)

class Examination(db.Model):

    __tablename__ = 'examination'

    id = db.Column(db.Integer,primary_key=True)
    course_id = db.Column(db.Integer,db.ForeignKey('course.id'),nullable=False)
    name = db.Column(db.String(100), nullable=False)
    exam_type = db.Column(db.String(20), default='pending')
    duration = db.Column(db.Integer,default=60)
    max_marks = db.Column(db.Integer,default=100)
    id = db.Column(db.Integer,primary_key=True)
    slot_creation_start_date = db.Column(db.DateTime,nullable=True)
    slot_creation_end_date = db.Column(db.DateTime,nullable=True)
    slot_booking_start = db.Column(db.DateTime,nullable=True)
    slot_booking_end = db.Column(db.DateTime,nullable=True)
    status = db.Column(db.String(10), default='draft')

    rubrics = db.relationship('Rubric', backref='exaamination', lazy=True, cascade='all, delete-orphan')
    slots = db.relationship('ExamSlots', backref='exaamination', lazy=True, cascade='all, delete-orphan')

class Rubric(db.model):

    __tablename__ = 'rubric'

    id = db.Column(db.Integer,primary_key=True)
    examination_id = db.Column(db.Integer, db.ForeignKey('examination.id'),nullable=False)
    criterion_name = db.Column(db.String(200), nullable=False)
    max_marks = db.Column(db.Integer, nullable=False)
    weightage = db.Column(db.Float, default=1.0)
    description = db.Column(db.Text, default='')

class ExamSlots(db.model):

    __tablename__ = 'exam_slot'

    id = db.Column(db.Integer,primary_key=True)
    examiner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    max_capacity = db.Column(db.Integer, default=1)
    available_seats = db.Column(db.Integer, default=1)
    status = db.Column(db.String(20), default='Available')

    bookings = db.relationship('Booking', backref='slot', lazy=True,cascade='all, delete-orphan')

class Booking(db.model):

    __tablename__ = 'booking'

    id = db.Column(db.Integer,primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    slot_id = db.Column(db.Integer, db.ForeignKey('exam_slot.id'), nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.String(20), default='Booked')
    evaluations = db.relationship('Evaluation', backref='booking', lazy=True,cascade='all, delete-orphan')

class Evaluation(db.model):

    __tablename__ = 'evaluation'

    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)
    rubric_id = db.Column(db.Integer, db.ForeignKey('rubric.id'), nullable=False)
    marks = db.Column(db.Float, default=0)
    remarks = db.Column(db.Text, default='')
    
    rubric = db.relationship('Rubric', backref='evaluations', lazy=True)