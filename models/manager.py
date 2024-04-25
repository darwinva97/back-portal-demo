from models.db import db


class Manager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    names = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    created_by = db.Column(db.Integer, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'names': self.names,
            'created_at': self.created_at.isoformat(),
            'created_by': self.created_by
            # Aquí puedes agregar más atributos si lo deseas
        }
