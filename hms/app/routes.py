from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from datetime import datetime
from .models import Patient, Doctor, Appointment, Admission, MedicalRecord, Test, Prescription
from . import db


main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/dashboard")
@login_required
def dashboard():
    stats = {
        "patients": Patient.query.count(),
        "doctors": Doctor.query.count(),
        "appointments": Appointment.query.count(),
        "admissions": Admission.query.count(),
    }
    return render_template("dashboard.html", stats=stats)


# Patients CRUD (list, create, delete)
@main_bp.route("/patients")
@login_required
def patients():
    items = Patient.query.order_by(Patient.name).all()
    return render_template("patients/list.html", items=items)


@main_bp.route("/patients/create", methods=["GET", "POST"])
@login_required
def patients_create():
    if request.method == "POST":
        dob_raw = request.form.get("dob")
        dob_value = None
        if dob_raw:
            try:
                dob_value = datetime.strptime(dob_raw, "%Y-%m-%d").date()
            except ValueError:
                flash("Invalid date format for DOB", "danger")
                return render_template("patients/create.html")
        patient = Patient(
            name=request.form.get("name"),
            dob=dob_value,
            gender=request.form.get("gender"),
            contact=request.form.get("contact"),
        )
        db.session.add(patient)
        db.session.commit()
        flash("Patient created", "success")
        return redirect(url_for("main.patients"))
    return render_template("patients/create.html")


@main_bp.route("/patients/<int:patient_id>/delete")
@login_required
def patients_delete(patient_id: int):
    patient = Patient.query.get_or_404(patient_id)
    db.session.delete(patient)
    db.session.commit()
    flash("Patient deleted", "info")
    return redirect(url_for("main.patients"))

