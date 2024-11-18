from flask_restful import Resource
from flask import request, jsonify
from notes.models import Note
from extensions import db
from users.models import User


class NotesListCreate(Resource):

    def get(self):
        notes = Note.query.all()
        # Use `to_dict()` to make each note JSON-serializable
        return jsonify([note.to_dict() for note in notes])

    def post(self):
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')
        user_email = data.get('email')
        user = User.query.filter_by(email=user_email).first()
        user_id = user.id
        print(user_id)

        if not title or not content or not user_id:
            return jsonify({"error": "Title, Content, and User ID are required!"}), 400

        new_note = Note(title=title, content=content, user_id=user_id)
        db.session.add(new_note)
        db.session.commit()

        # Return the created note in JSON format
        return {"message": "Note added successfully!", "note": new_note.to_dict()}, 201
