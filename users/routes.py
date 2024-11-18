from flask import request, jsonify
from users import db, users_bp
from users.models import User

# Route to add a new user
@users_bp.route('/add', methods=['POST'])
def add_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({"error": "Name and Email are required!"}), 400

    # Create and add the new user to the database
    new_user = User(name=name, email=email)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User added successfully!"})

# Route to get all users
@users_bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()  # Query all users from the User model
    users_list = [{"id": user.id, "name": user.name, "email": user.email} for user in users]
    return jsonify(users_list)
