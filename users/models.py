from extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name
        }
