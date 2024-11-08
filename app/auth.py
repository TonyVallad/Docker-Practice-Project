from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from .forms import LoginForm
from . import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.list_users'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        # If username is not found
        if user is None:
            form.username.errors.append('Username not recognized.')
        # If password is incorrect
        elif not user.check_password(form.password.data):
            form.password.errors.append('Incorrect password.')
        else:
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('main.list_users'))

    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))
