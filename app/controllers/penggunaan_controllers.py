# app/controllers/penggunaan_controller.py

from flask import Blueprint, render_template, request, url_for, abort, redirect, session
from app.models.penggunaan_pakan import get_all, get_by_id, insert, update, delete
from app.models.auth import verify_user

penggunaan_bp = Blueprint('penggunaan', __name__)

# Blueprint menampilkan halaman penggunaan pakan dan menampilkan semua data penggunaan pakan
@penggunaan_bp.route('/penggunaan')
def penggunaan():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    verif = verify_user(session.get('user'))
    
    if verif['status'] != 'success':
        return redirect(url_for('auth.login'))
    elif verif['status'] == 'error':
        session.clear()
        return render_template('auth/login.html', status='error')

    data = get_all()
    return render_template('penggunaan/index.html', title='Penggunaan pakan', data=data)

# Blueprint menampilkan form penggunaan pakan by id
@penggunaan_bp.route('/form-penggunaan/<string:id>')
def form_penggunaan_by_id(id):
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
    return render_template('penggunaan/form.html', title='Update Penggunaan Pakan', action='/update-penggunaan', id=id, data=data)

# Blueprint menampilkan form penggunaan pakan
@penggunaan_bp.route('/form-penggunaan')
def form_penggunaan():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    verif = verify_user(session.get('user'))
    
    if verif['status'] != 'success':
        return redirect(url_for('auth.login'))
    elif verif['status'] == 'error':
        session.clear()
        return render_template('auth/login.html', status='error')

    return render_template('penggunaan/form.html', title='Tambah Penggunaan Pakan', action='/add-penggunaan')

# Blueprint menambahkan data melaui method POST ke database
@penggunaan_bp.route('/add-penggunaan', methods=['POST'])
def add_penggunaan():
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
        jenis_pakan = request.form['jenis_pakan']
        nomor_kandang = request.form['nomor_kandang']
        pagi = request.form['pagi']
        sore = request.form['sore']
        total = request.form['total']

        insert(tanggal, jenis_pakan, nomor_kandang, pagi, sore, total)
    else:
        abort(404)
    return redirect(url_for('penggunaan.penggunaan'))

# Blueprint mengupdate data melaui method POST ke database
@penggunaan_bp.route('/update-penggunaan/<string:id>', methods=['POST'])
def update_penggunaan(id):
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
        jenis_pakan = request.form['jenis_pakan']
        nomor_kandang = request.form['nomor_kandang']
        pagi = request.form['pagi']
        sore = request.form['sore']
        total = request.form['total']

        update(id, tanggal, jenis_pakan, nomor_kandang, pagi, sore, total)
    else:
        abort(404)
    return redirect(url_for('penggunaan.penggunaan'))

# Blueprint menghapus data
@penggunaan_bp.route('/delete-penggunaan/<string:id>')
def delete_penggunaan(id):
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    verif = verify_user(session.get('user'))
    
    if verif['status'] != 'success':
        return redirect(url_for('auth.login'))
    elif verif['status'] == 'error':
        session.clear()
        return render_template('auth/login.html', status='error')

    delete(id)
    return redirect(url_for('penggunaan.penggunaan'))