from flask import request, jsonify
import jwt
import datetime

from models.db import db
from models.manager import Manager

from lib.auth import check_hash, hash_password, UserData
from lib.config import SECRET_KEY

from models.admin import Admin


def login_manager():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        message = 'Se requiere Correo y Contraseña'
        return jsonify({'message': message}), 400

    manager = Manager.query.filter_by(
        email=email
    ).first()

    if not manager:
        return jsonify({'message': 'El asesor no esta registrado'}), 401

    match_password = check_hash(password, manager.password)

    # Compara los hashes de las contraseñas
    if not match_password:
        return jsonify({'message': 'Las credenciales son incorrectas'}), 401

    # Genera el token JWT si las credenciales son válidas
    expires = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    data = {'type': 'manager', 'user': manager.serialize(), 'exp': expires}
    token = jwt.encode(data, SECRET_KEY, algorithm='HS256')

    return jsonify({'token': token, 'exp': expires}), 200


def register_manager(user_data: UserData):
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    names = data.get('names')

    user_type = user_data.get("type")

    if user_type != 'admin':
        return jsonify({'message': 'No autorizado'}), 401

    admin: Admin = user_data.get("user")
    created_by = admin.id

    if not email or not password or not names or not created_by:
        message = 'Se requieren Nombres, Correo y Contraseña. Y debe ser creada por el admin.'
        return jsonify({'message': message}), 400

    manager = Manager.query.filter_by(
        email=email
    ).first()

    if manager:
        return jsonify({'message': 'El asesor ya existe'}), 401

    hashed_password = hash_password(password)

    new_manager = Manager(
        email=email,
        password=hashed_password,
        names=names,
        created_by=created_by
    )

    db.session.add(new_manager)
    db.session.commit()

    return jsonify(new_manager.serialize()), 201
