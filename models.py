from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    phone = db.Column(db.String(30))
    address = db.Column(db.String(250))
    medical_history = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    appointments = db.relationship('Appointment', backref='patient', cascade='all, delete-orphan')

class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor = db.Column(db.String(120), nullable=False)
    appt_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='Scheduled')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
