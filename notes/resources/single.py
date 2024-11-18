from flask import jsonify, request
from flask_restful import Resource
from extensions import db
from notes.models import Note


class NoteResource(Resource):
    def get(self, note_id):
        note = Note.query.get_or_404(note_id)
        return jsonify(note.to_dict())

    def put(self, note_id):
        note = Note.query.get_or_404(note_id)
        data = request.get_json()
        note.title = data['title']
        note.content = data['content']
        db.session.commit()
        return jsonify(note.to_dict())

    def delete(self, note_id):
        note = Note.query.get_or_404(note_id)  # Fetch the note by ID
        db.session.delete(note)  # Delete the note
        db.session.commit()  # Commit the changes to the database
        return jsonify({'message': 'Note deleted successfully'})  # Return a success message
