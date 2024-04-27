from flask import request, jsonify

from models.db import db
from models.client import Client
from models.manager import Manager
from models.admin import Admin

from lib.auth import hash_password


def change_password(user_data=None):
    user_type = user_data.get("type")
    body = request.get_json()
    password = body.get("password")

    if not password:
        return jsonify({'message': 'Se requiere contraseña'}), 400

    hashed_password = hash_password(password)
    user = user_data.get("user")
    user_id = user.id
    user_updated = None

    if user_type == 'admin':
        user_updated = Admin.query.filter_by(id=user_id).update(
            {"password": hashed_password}
        )

    elif user_type == 'manager':
        user_updated = Manager.query.filter_by(id=user_id).update(
            {"password": hashed_password}
        )

    elif user_type == 'client':
        user_updated = Client.query.filter_by(id=user_id).update(
            {"password": hashed_password}
        )

    if user_updated:
        db.session.commit()
        return jsonify({'message': 'Cambio existoso'}), 200
    else:
        return jsonify({'message': 'Cambio fallido'}), 400
