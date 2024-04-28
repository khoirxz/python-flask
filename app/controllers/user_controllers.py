# app/controllers/user_controllers.py

from flask import Blueprint, render_template, request, redirect, url_for, session, abort
from app.models.user import get_all, get_by_id, update, delete
from app.models.auth import signup_user, verify_user

user_bp = Blueprint('user', __name__)

# Blueprint menampilkan halaman user dan menampilkan semua data user
@user_bp.route('/user')
def user():
    if 'user' not in session:
            return redirect(url_for('auth.login'))
        
    verif = verify_user(session.get('user'))
    
    if verif['status'] != 'success':
        return redirect(url_for('auth.login'))
    elif verif['status'] == 'error':
        session.clear()
        return render_template('auth/login.html', status='error')
    
    data = get_all()
    return render_template('user/index.html', title='User', data=data)
    
# Blueprint menampilkan form user
@user_bp.route('/form-user')
def form_user():
    if 'user' not in session:
            return redirect(url_for('auth.login'))
        
    verif = verify_user(session.get('user'))
    
    if verif['status'] != 'success':
        return redirect(url_for('auth.login'))
    elif verif['status'] == 'error':
        session.clear()
        return render_template('auth/login.html', status='error')
    
    return render_template('user/form.html', title='Tambah User', action='/add-user')

# Blueprint menampilkan form by id
@user_bp.route('/form-user/<string:id>')
def form_user_by_id(id):
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
    return render_template('user/form.html', title='Edit User', action='/update-user', id=id, data=data)

# Blueprint menambahkan data melalui method POST ke database
@user_bp.route('/add-user', methods=['POST'])
def add_user():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
        
    verif = verify_user(session.get('user'))
    
    if verif['status'] != 'success':
        return redirect(url_for('auth.login'))
    elif verif['status'] == 'error':
        session.clear()
        return render_template('auth/login.html', status='error')
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']

        # check jika password sama dengan confirm password
        if password != confirmPassword:
            return render_template('user/form.html', status='error')

        data = signup_user(email, username, password)

        if data and 'status' in data and data['status'] == 'success':
            return redirect(url_for('user.user'))
        
    return render_template('user/form.html', status='error')

# Blueprint mengupdate data melalui method POST ke database
@user_bp.route('/update-user/<string:id>', methods=['POST'])
def update_user(id):
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    verif = verify_user(session.get('user'))
    
    if verif['status'] != 'success':
        return redirect(url_for('auth.login'))
    elif verif['status'] == 'error':
        session.clear()
        return render_template('auth/login.html', status='error')
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        data = update(id, email, username, password)

        if data and 'status' in data and data['status'] == 'success':
            return redirect(url_for('user.user'))
    
# Blueprint menghapus data
@user_bp.route('/delete-user/<string:id>')
def delete_user(id):
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    verif = verify_user(session.get('user'))
    
    if verif['status'] != 'success':
        return redirect(url_for('auth.login'))
    elif verif['status'] == 'error':
        session.clear()
        return render_template('auth/login.html', status='error')
    
    delete(id)
    return redirect(url_for('user.user'))