from models.db import db


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    names = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'names': self.names,
            'created_at': self.created_at.isoformat()
            # Aquí puedes agregar más atributos si lo deseas
        }
