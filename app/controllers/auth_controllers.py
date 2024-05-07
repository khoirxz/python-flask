# app/controllers/auth_controllers.py

from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models.auth import signup_user, login_user, verify_user

auth_bp = Blueprint('auth', __name__)


# Blueprint menampilkan halaman login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('dashboard.dashboard'))
    
    # jika user sudah login, maka redirect ke dashboard
    verify = verify_user(session.get('user'))
    if verify['status'] == 'success':
        return redirect(url_for('dashboard.dashboard'))
    elif verify['status'] == 'error':
        session.clear()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        data = login_user(username, password)

        if data and 'status' in data and data['status'] != 'success':
            
            return render_template('auth/login.html', status={'status': 'error', 'message': 'Username atau password salah'})

        # jika data ditemukan makan informasi data akan disimpan pada session storage

        if data and 'status' in data and data['status'] == 'success':
            # data tersimpan pada session storage
            session['user'] = data['user']
            print(session.get('user'))
            return redirect(url_for('dashboard.dashboard'))
        
    return render_template('auth/login.html')

# Blueprint menampilkan halaman signup
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user' in session:
        return redirect(url_for('dashboard.dashboard'))
    
    verify = verify_user(session.get('user'))
    if verify['status'] == 'success':
        return redirect(url_for('dashboard.dashboard'))
    elif verify['status'] == 'error':
        session.clear()

    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']

        # check if password same as confirm password
        if password != confirmPassword:
            return render_template('auth/register.html', status={"status": "error", "message": "Password harus sama"})

        data = signup_user(email=email, username=username, password=password)

        if data and 'status' in data and data['status'] != 'success':
            return render_template('auth/register.html', status={'status': 'error', 'message': 'Username sudah ada'})
        elif data and 'status' in data and data['status'] == 'success':
            return render_template('auth/register.html', status={'status': 'success', 'message': 'Akun berhasil dibuat'})

    return render_template('auth/register.html')

# Blueprint logout
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
