# app/controllers/check_controllers.py

from flask import Blueprint, render_template, request, redirect, session, url_for
from app.models.prediksi import get_result
from app.models.auth import verify_user


check_bp = Blueprint('check', __name__)


# Blueprint menampilkan halaman check
@check_bp.route('/check')
def check():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    verif = verify_user(session.get('user'))
    
    if verif['status'] != 'success':
        return redirect(url_for('auth.login'))
    elif verif['status'] == 'error':
        session.clear()
        return render_template('auth/login.html', status='error')
    
    return render_template('check/index.html')

# Blueprint memperoses data prediksi dan menampilkan hasil prediksi
@check_bp.route('/result', methods=['POST'])
def result(): 

    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    verif = verify_user(session.get('user'))
    
    if verif['status'] != 'success':
        return redirect(url_for('auth.login'))
    elif verif['status'] == 'error':
        session.clear()
        return render_template('auth/login.html', status='error')
    
    start_day = int(request.form['start_day'])
    days = min(int(request.form['days']), 35)  # Batasi maksimal 35 hari
    selected_model = request.form["model"]

    predictions, total_predictions, grand_total_prediction, average_total_prediction = get_result(start_day, days, selected_model)

    return render_template('check/result.html', predictions=predictions, total_predictions=total_predictions,
                           grand_total_prediction=grand_total_prediction, average_total_prediction=average_total_prediction, day=days)