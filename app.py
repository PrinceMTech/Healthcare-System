from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, Patient, Appointment
from datetime import datetime
from dateutil import parser as dateparser
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///healthcare.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

    register_routes(app)
    return app

def register_routes(app):

    @app.route('/')
    def index():
        patient_count = Patient.query.count()
        appt_count = Appointment.query.count()
        upcoming = Appointment.query.order_by(Appointment.appt_time.asc()).limit(5).all()
        return render_template('index.html', patient_count=patient_count, appt_count=appt_count, upcoming=upcoming)

    @app.route('/patients')
    def patients_list():
        q = request.args.get('q', '').strip()
        if q:
            patients = Patient.query.filter(Patient.name.ilike(f'%{q}%')).order_by(Patient.created_at.desc()).all()
        else:
            patients = Patient.query.order_by(Patient.created_at.desc()).all()
        return render_template('patients_list.html', patients=patients, q=q)

    @app.route('/patients/new', methods=['GET', 'POST'])
    def patient_new():
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            if not name:
                flash('Name is required', 'danger')
                return redirect(url_for('patient_new'))
            age = request.form.get('age')
            age = int(age) if age else None
            gender = request.form.get('gender')
            phone = request.form.get('phone')
            address = request.form.get('address')
            medical_history = request.form.get('medical_history')
            p = Patient(name=name, age=age, gender=gender, phone=phone, address=address, medical_history=medical_history)
            db.session.add(p)
            db.session.commit()
            flash('Patient created', 'success')
            return redirect(url_for('patients_list'))
        return render_template('patient_form.html', patient=None)

    @app.route('/patients/<int:pid>/edit', methods=['GET', 'POST'])
    def patient_edit(pid):
        patient = Patient.query.get_or_404(pid)
        if request.method == 'POST':
            patient.name = request.form.get('name', '').strip() or patient.name
            age = request.form.get('age')
            patient.age = int(age) if age else None
            patient.gender = request.form.get('gender')
            patient.phone = request.form.get('phone')
            patient.address = request.form.get('address')
            patient.medical_history = request.form.get('medical_history')
            db.session.commit()
            flash('Patient updated', 'success')
            return redirect(url_for('patients_list'))
        return render_template('patient_form.html', patient=patient)

    @app.route('/patients/<int:pid>/delete', methods=['POST'])
    def patient_delete(pid):
        patient = Patient.query.get_or_404(pid)
        db.session.delete(patient)
        db.session.commit()
        flash('Patient deleted', 'warning')
        return redirect(url_for('patients_list'))

    @app.route('/appointments')
    def appointments_list():
        appts = Appointment.query.order_by(Appointment.appt_time.desc()).all()
        return render_template('appointments_list.html', appointments=appts)

    @app.route('/appointments/new', methods=['GET', 'POST'])
    def appointment_new():
        if request.method == 'POST':
            patient_id = request.form.get('patient_id')
            doctor = request.form.get('doctor', '').strip()
            appt_time_str = request.form.get('appt_time')
            status = request.form.get('status', 'Scheduled')
            notes = request.form.get('notes')
            if not (patient_id and doctor and appt_time_str):
                flash('Patient, doctor and appointment time are required', 'danger')
                return redirect(url_for('appointment_new'))
            appt_time = dateparser.parse(appt_time_str)
            appt = Appointment(patient_id=int(patient_id), doctor=doctor, appt_time=appt_time, status=status, notes=notes)
            db.session.add(appt)
            db.session.commit()
            flash('Appointment created', 'success')
            return redirect(url_for('appointments_list'))
        patients = Patient.query.order_by(Patient.name.asc()).all()
        default_time = (datetime.now()).strftime('%Y-%m-%d %H:%M')
        return render_template('appointment_form.html', patients=patients, default_time=default_time)

    @app.route('/appointments/<int:aid>/delete', methods=['POST'])
    def appointment_delete(aid):
        appt = Appointment.query.get_or_404(aid)
        db.session.delete(appt)
        db.session.commit()
        flash('Appointment deleted', 'warning')
        return redirect(url_for('appointments_list'))

    @app.route('/api/patients')
    def api_patients():
        patients = Patient.query.order_by(Patient.created_at.desc()).all()
        data = [
            {
                'id': p.id,
                'name': p.name,
                'age': p.age,
                'gender': p.gender,
                'phone': p.phone,
                'address': p.address,
                'medical_history': p.medical_history,
                'created_at': p.created_at.isoformat(),
            } for p in patients
        ]
        return jsonify(data)

    @app.route('/api/appointments')
    def api_appointments():
        appts = Appointment.query.order_by(Appointment.appt_time.desc()).all()
        data = [
            {
                'id': a.id,
                'patient_id': a.patient_id,
                'patient_name': a.patient.name if a.patient else None,
                'doctor': a.doctor,
                'appt_time': a.appt_time.isoformat(),
                'status': a.status,
                'notes': a.notes,
                'created_at': a.created_at.isoformat(),
            } for a in appts
        ]
        return jsonify(data)

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
