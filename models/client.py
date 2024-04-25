from datetime import datetime
from models.db import db


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    odoo_client_id = db.Column(db.Integer, unique=True, nullable=False)
    doc_nro = db.Column(db.String(50), unique=True, nullable=False)
    doc_type = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    created_by = db.Column(db.String(50), nullable=False)
    created_by_type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    def serialize(self):
        return {
            'id': self.id,
            'doc_nro': self.doc_nro,
            'doc_type': self.doc_type,
            'created_by': self.created_by,
            'created_by_type': self.created_by_type,
            'created_at': self.created_at.isoformat(),
            # Aquí puedes agregar más atributos si lo deseas
        }
