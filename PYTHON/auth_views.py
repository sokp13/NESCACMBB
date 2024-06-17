from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from model import User, db

auth_views = Blueprint('auth', __name__)

@auth_views.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists.', 'error')
            return redirect(url_for('auth.register'))

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', 'error')
            return redirect(url_for('auth.register'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))  # Redirect to the login page

    return render_template('register.html')

# Other views...


@auth_views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            print(f"User found: {user.username}")  # Add this line
            if check_password_hash(user.password_hash, password):
                print("Password matched")  # Add this line
                login_user(user)
                flash('Login successful!', 'success')
                print("Redirecting to profile")  # Add this line
                return redirect(url_for('auth.profile'))
            else:
                print("Invalid password")  # Add this line
        else:
            print("User not found")  # Add this line

        flash('Invalid email or password.', 'error')

    return render_template('login.html')

@auth_views.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@auth_views.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))