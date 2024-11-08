from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required
from .forms import UserForm
from .models import User, db  # Import SQLAlchemy instance and User model

# Create a Blueprint for your routes
main_bp = Blueprint('main', __name__)

# =====================
# Form Routes
# =====================

# Homepage route (for the web interface)
@main_bp.route('/')
def index():
    return render_template('index.html')

# Route to render the 'add user' form page
@main_bp.route('/add_user', methods=['GET', 'POST'])
def add_user_form_submit():
    form = UserForm()
    if form.validate_on_submit():
        # Create a new user
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)

        # Add user to the database
        db.session.add(user)
        db.session.commit()

        flash('User successfully added!', 'success')
        return redirect(url_for('main.list_users'))

    return render_template('add_user.html', form=form)

# Route to render the user list page (for the web interface)
@main_bp.route('/list_users', methods=['GET'])
@login_required
def list_users():
    users = User.query.all()
    return render_template('list_users.html', users=users)


# =====================
# API Routes
# =====================

# API route to add a user via JSON
@main_bp.route('/api/users', methods=['POST'])
def api_add_user():
    # Check if the request is JSON
    if request.is_json:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        # Create a new user
        user = User(username=username, email=email)
        user.set_password(password)

        # Insert user into the database
        db.session.add(user)
        db.session.commit()

        return jsonify({'message': 'User added successfully!'}), 201
    else:
        return jsonify({'error': 'Invalid request format, must be JSON'}), 400

# API route to get the list of users in JSON format
@main_bp.route('/api/users', methods=['GET'])
def api_get_users():
    users = User.query.all()  # Use SQLAlchemy ORM to get all users
    users_list = [{'id': user.id, 'username': user.username} for user in users]
    return jsonify(users_list), 200
