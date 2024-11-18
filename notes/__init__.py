from flask import Blueprint
from flask_restful import Api

from notes.resources.list_create import NotesListCreate
from notes.resources.single import NoteResource

notes_bp = Blueprint('notes', __name__)

api = Api(notes_bp)

api.add_resource(NotesListCreate, '/')
api.add_resource(NoteResource, '/<int:note_id>')