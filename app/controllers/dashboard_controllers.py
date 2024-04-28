# app/controllers/dashboard_controller.py
from flask import Blueprint
from flask import render_template, session, redirect, url_for
from app.models.dashboard import check_db
from app.models.auth import verify_user


dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    verif = verify_user(session.get('user'))
    
    if verif['status'] != 'success':
        return redirect(url_for('auth.login'))
    elif verif['status'] == 'error':
        session.clear()
        return render_template('auth/login.html', status='error')


    status, version = check_db()
    return render_template('dashboard/index.html', status=status, version=version, user=verif['username'])
