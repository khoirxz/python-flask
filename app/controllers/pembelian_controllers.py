# app/controllers/pembelian_controllers.py

from flask import Blueprint, render_template, request, url_for, abort, redirect, session
from app.models.pembelian_pakan import get_all, insert, get_by_id, update, delete
from app.models.auth import verify_user


pembelian_bp = Blueprint('pembelian', __name__)

# Blueprint menampilkan halaman pembelian dan menampilkan semua data pembelian
@pembelian_bp.route('/pembelian')
def pembelian():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    verif = verify_user(session.get('user'))
    
    if verif['status'] != 'success':
        return redirect(url_for('auth.login'))
    elif verif['status'] == 'error':
        session.clear()
        return render_template('auth/login.html', status='error')

    data = get_all()
    return render_template('pembelian/index.html', title='Pembelian', data=data)

# Blueprint menampilkan form pembelian by id
@pembelian_bp.route('/form-pembelian/<string:id>')
def form_pembelian_by_id(id):
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
    return render_template('pembelian/form.html', title='Edit Pembelian', action='/update-pembelian', id=id, data=data)

# Blueprint menampilkan form pembelian
@pembelian_bp.route('/form-pembelian')
def form_pembelian():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    verif = verify_user(session.get('user'))
    
    if verif['status'] != 'success':
        return redirect(url_for('auth.login'))
    elif verif['status'] == 'error':
        session.clear()
        return render_template('auth/login.html', status='error')
    
    return render_template('pembelian/form.html', title='Tambah Pembelian', action='/add-pembelian')

# Blueprint mengirim data melalui method POST ke database
@pembelian_bp.route('/add-pembelian', methods=['POST'])
def add_pembelian():
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
        nama_pakan = request.form['nama_pakan']
        supplier = request.form['supplier']
        item = request.form['item']
        jumlah_pakan = request.form['jumlah_pakan']

        insert(tanggal, nama_pakan, supplier, item, jumlah_pakan)
    else:
        abort(404)
    return redirect(url_for('pembelian.pembelian'))

# Blueprint mengupdate data melalui method POST ke database
@pembelian_bp.route('/update-pembelian/<string:id>', methods=['POST'])
def update_pembelian(id):
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
        nama_pakan = request.form['nama_pakan']
        supplier = request.form['supplier']
        item = request.form['item']
        jumlah_pakan = request.form['jumlah_pakan']

        update(id, tanggal, nama_pakan, supplier, item, jumlah_pakan)
    else:
        abort(404)
    return redirect(url_for('pembelian.pembelian'))

# Blueprint menghapus data
@pembelian_bp.route('/delete-pembelian/<string:id>')
def delete_pembelian(id):
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    verif = verify_user(session.get('user'))
    
    if verif['status'] != 'success':
        return redirect(url_for('auth.login'))
    elif verif['status'] == 'error':
        session.clear()
        return render_template('auth/login.html', status='error')

    delete(id)
    return redirect(url_for('pembelian.pembelian'))