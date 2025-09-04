from datetime import datetime
from . import db, login_manager
from flask_login import UserMixin


class Patient(db.Model):
    patient_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10))
    contact = db.Column(db.String(120))
    admissions = db.relationship("Admission", backref="patient", lazy=True)
    appointments = db.relationship("Appointment", backref="patient", lazy=True)
    medical_records = db.relationship("MedicalRecord", backref="patient", lazy=True)


class Doctor(db.Model):
    doctor_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    specialty = db.Column(db.String(120))
    contact = db.Column(db.String(120))
    appointments = db.relationship("Appointment", backref="doctor", lazy=True)


class Appointment(db.Model):
    appointment_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.patient_id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.doctor_id"), nullable=False)
    datetime = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default="scheduled")


class Admission(db.Model):
    admission_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.patient_id"), nullable=False)
    room = db.Column(db.String(50))
    admit_date = db.Column(db.DateTime, default=datetime.utcnow)
    discharge_date = db.Column(db.DateTime)


class MedicalRecord(db.Model):
    record_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.patient_id"), nullable=False)
    diagnosis = db.Column(db.String(255))
    treatment_notes = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    tests = db.relationship("Test", backref="record", lazy=True)
    prescriptions = db.relationship("Prescription", backref="record", lazy=True)


class Test(db.Model):
    test_id = db.Column(db.Integer, primary_key=True)
    record_id = db.Column(db.Integer, db.ForeignKey("medical_record.record_id"), nullable=False)
    test_type = db.Column(db.String(120))
    result = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)


class Prescription(db.Model):
    prescription_id = db.Column(db.Integer, primary_key=True)
    record_id = db.Column(db.Integer, db.ForeignKey("medical_record.record_id"), nullable=False)
    medicine = db.Column(db.String(120))
    dosage = db.Column(db.String(120))
    duration = db.Column(db.String(120))


class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    role = db.Column(db.String(50), default="staff")
    password_hash = db.Column(db.String(255), nullable=False)

    def get_id(self):
        return str(self.user_id)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

