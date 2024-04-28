# app/controllers/penerimaan_controllers.py

from flask import Blueprint, render_template, request, url_for, abort, redirect, session
from app.models.penerimaan_pakan import get_all, insert, get_by_id, update, delete
from app.models.auth import verify_user

penerimaan_bp = Blueprint('penerimaan', __name__)

# Blueprint menampilkan halaman penerimaan dan menampilkan semua data penerimaan
@penerimaan_bp.route('/penerimaan')
def penerimaan():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    verif = verify_user(session.get('user'))
    
    if verif['status'] != 'success':
        return redirect(url_for('auth.login'))
    elif verif['status'] == 'error':
        session.clear()
        return render_template('auth/login.html', status='error')

    data = get_all()
    return render_template('penerimaan/index.html', title='Penerimaan', data=data)

# Blueprint menampilkan form penerimaan by id
@penerimaan_bp.route('/form-penerimaan/<string:id>')
def form_penerimaan_by_id(id):
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
    return render_template('penerimaan/form.html', title='Edit Penerimaan Pakan', action='/update-penerimaan', id=id, data=data)

# Blueprint menampilkan from penerimaan
@penerimaan_bp.route('/form-penerimaan')
def form_penerimaan():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    verif = verify_user(session.get('user'))
    
    if verif['status'] != 'success':
        return redirect(url_for('auth.login'))
    elif verif['status'] == 'error':
        session.clear()
        return render_template('auth/login.html', status='error')

    return render_template('penerimaan/form.html', title='Tambah Penerimaan Pakan', action='/add-penerimaan')

# Blueprint mengirim data melalui method POST ke database
@penerimaan_bp.route('/add-penerimaan', methods=['POST'])
def add_penerimaan():
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
        kode_pakan = request.form['kode_pakan']
        jenis = request.form['jenis']
        jumlah_pakan = request.form['jumlah_pakan']
        kondisi = request.form['kondisi']
        sumber = request.form['sumber']

        insert(tanggal, kode_pakan, jenis, jumlah_pakan, kondisi, sumber)
    else:
        abort(404)
    return redirect(url_for('penerimaan.penerimaan'))

# Blueprint mengupdate data melalui method POST ke database
@penerimaan_bp.route('/update-penerimaan/<string:id>', methods=['POST'])
def update_penerimaan(id):
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
        kode_pakan = request.form['kode_pakan']
        jenis = request.form['jenis']
        jumlah_pakan = request.form['jumlah_pakan']
        kondisi = request.form['kondisi']
        sumber = request.form['sumber']

        update(id, tanggal, kode_pakan, jenis, jumlah_pakan, kondisi, sumber)
    else:
        abort(404)
    return redirect(url_for('penerimaan.penerimaan'))

# Blueprint menghapus data
@penerimaan_bp.route('/delete-penerimaan/<string:id>')
def delete_penerimaan(id):
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    verif = verify_user(session.get('user'))
    
    if verif['status'] != 'success':
        return redirect(url_for('auth.login'))
    elif verif['status'] == 'error':
        session.clear()
        return render_template('auth/login.html', status='error')

    delete(id)
    return redirect(url_for('penerimaan.penerimaan'))