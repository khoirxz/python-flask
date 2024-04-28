# app/controllers/riwayat_controllers.py

from flask import Blueprint, render_template, request, url_for, abort, redirect, session
from app.models.riwayat import get_all, insert, get_by_id, update, delete
from app.models.auth import verify_user

riwayat_bp = Blueprint('riwayat', __name__)

# Blueprint menampilkan halaman riwayat dan menampilkan semua data riwayat
@riwayat_bp.route('/riwayat')
def riwayat():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    verif = verify_user(session.get('user'))
    
    if verif['status'] != 'success':
        return redirect(url_for('auth.login'))
    elif verif['status'] == 'error':
        session.clear()
        return render_template('auth/login.html', status='error')

    data = get_all()
    return render_template('riwayat/index.html', title="Riwayat", data=data)

# Blueprint menampilkan form riwayat by id
@riwayat_bp.route('/form-riwayat/<string:id>')
def form_riwayat_by_id(id):
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    verif = verify_user(session.get('user'))
    
    if verif['status'] != 'success':
        return redirect(url_for('auth.login'))
    elif verif['status'] == 'error':
        session.clear()
        return render_template('auth/login.html', status='error')

    data = get_by_id(id)
    if data and 'status' in data and data['status'] == 'error' and data['message'] == 'id not found':
        abort(404)
    return render_template('riwayat/form.html', title='Edit Riwayat', action='/update-riwayat', id=id, data=data)

# Blueprint menampilkan form riwayat
@riwayat_bp.route('/form-riwayat')
def form_riwayat():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    verif = verify_user(session.get('user'))
    
    if verif['status'] != 'success':
        return redirect(url_for('auth.login'))
    elif verif['status'] == 'error':
        session.clear()
        return render_template('auth/login.html', status='error')

    return render_template('riwayat/form.html', title='Add Riwayat', action='/add-riwayat')

# Blueprint mengirim data melalui method POST ke database
@riwayat_bp.route('/add-riwayat', methods=['POST'])
def add_riwayat():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    verif = verify_user(session.get('user'))
    
    if verif['status'] != 'success':
        return redirect(url_for('auth.login'))
    elif verif['status'] == 'error':
        session.clear()
        return render_template('auth/login.html', status='error')

    if request.method == 'POST':
        tanggal = request.form['tanggal']
        model_regresi = request.form['model_regresi']
        hari_mulai_prediksi = request.form['hari_mulai_prediksi']
        jumlah_prediksi = request.form['jumlah_prediksi']

        insert(tanggal, model_regresi, hari_mulai_prediksi, jumlah_prediksi)
    else:
        abort(404)
    return redirect(url_for('riwayat.riwayat'))

# Blueprint mengupdate data melalui method POST ke database
@riwayat_bp.route('/update-riwayat/<string:id>', methods=['POST'])
def update_riwayat(id):
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    verif = verify_user(session.get('user'))
    
    if verif['status'] != 'success':
        return redirect(url_for('auth.login'))
    elif verif['status'] == 'error':
        session.clear()
        return render_template('auth/login.html', status='error')

    if request.method == 'POST':
        tanggal = request.form['tanggal']
        model_regresi = request.form['model_regresi']
        hari_mulai_prediksi = request.form['hari_mulai_prediksi']
        jumlah_prediksi = request.form['jumlah_prediksi']

        update(id, tanggal, model_regresi, hari_mulai_prediksi, jumlah_prediksi)
    else:
        abort(404)
    return redirect(url_for('riwayat.riwayat'))

# Blueprint menghapus data
@riwayat_bp.route('/delete-riwayat/<string:id>')
def delete_riwayat(id):
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    verif = verify_user(session.get('user'))
    
    if verif['status'] != 'success':
        return redirect(url_for('auth.login'))
    elif verif['status'] == 'error':
        session.clear()
        return render_template('auth/login.html', status='error')

    delete(id)
    return redirect(url_for('riwayat.riwayat'))