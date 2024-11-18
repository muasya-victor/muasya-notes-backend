from flask_restful import Resource
from flask import request, jsonify
from users.models import User
from extensions import db


class UsersListCreate(Resource):
    def get(self):
        users = User.query.all()
        if not users:
            return jsonify([])
        return jsonify([user.to_dict() for user in users])

    def post(self):
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')

        if not name or not email:
            return jsonify({"error": "Name and Email are required!"}), 400

        new_user = User(name=name, email=email)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User added successfully!"}), 201
