# app/controllers/stok_controllers.py

from flask import Blueprint, render_template, request, url_for, abort, redirect, session
from app.models.stok_pakan import get_all, insert, get_by_id, update, delete
from app.models.auth import verify_user

stok_bp = Blueprint('stok', __name__)

# Blueprint menampilkan halaman stok dan menampilkan semua data stok
@stok_bp.route('/stok')
def stok():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    verif = verify_user(session.get('user'))
    
    if verif['status'] != 'success':
        return redirect(url_for('auth.login'))
    elif verif['status'] == 'error':
        session.clear()
        return render_template('auth/login.html', status='error')

    data = get_all()
    return render_template('stok/index.html', title='Stok', data=data)

# Blueprint menampilkan from stok by id
@stok_bp.route('/form-stok/<string:id>')
def form_stok_by_id(id):
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
    return render_template('stok/form.html', title='Edit Stok', action='/update-stok', id=id, data=data)

# Blueprint menampilkan form stok
@stok_bp.route('/form-stok')
def form_stok():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    verif = verify_user(session.get('user'))
    
    if verif['status'] != 'success':
        return redirect(url_for('auth.login'))
    elif verif['status'] == 'error':
        session.clear()
        return render_template('auth/login.html', status='error')

    return render_template('stok/form.html', title='Tambah Stok', action='/add-stok')

# Blueprint mengirim data menggunakan method POST ke database
@stok_bp.route('/add-stok', methods=['POST'])
def add_stok():
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
        jumlah_masuk = request.form['jumlah_masuk']
        jumlah_penggunaan = request.form['jumlah_penggunaan']
        total_stok = request.form['total_stok']
        kondisi = request.form['kondisi']

        insert(tanggal, jenis_pakan, jumlah_masuk, jumlah_penggunaan, total_stok, kondisi)
    else:
        abort(404)
    return redirect(url_for('stok.stok'))

# Blueprint mengupdate data melalui method POST ke database
@stok_bp.route('/update-stok/<string:id>', methods=['POST'])
def update_stok(id):
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
        jumlah_masuk = request.form['jumlah_masuk']
        jumlah_penggunaan = request.form['jumlah_penggunaan']
        total_stok = request.form['total_stok']
        kondisi = request.form['kondisi']

        update(id, tanggal, jenis_pakan, jumlah_masuk, jumlah_penggunaan, total_stok, kondisi)
    else:
        abort(404)
    return redirect(url_for('stok.stok'))

# Blueprint menghapus data
@stok_bp.route('/delete-stok/<string:id>')
def delete_stok(id):
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    verif = verify_user(session.get('user'))
    
    if verif['status'] != 'success':
        return redirect(url_for('auth.login'))
    elif verif['status'] == 'error':
        session.clear()
        return render_template('auth/login.html', status='error')

    delete(id)
    return redirect(url_for('stok.stok'))