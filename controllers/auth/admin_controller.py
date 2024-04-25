from flask import request, jsonify
import jwt
import datetime

from models.db import db
from models.admin import Admin

from lib.auth import check_hash, hash_password
from lib.config import SECRET_KEY


def login_admin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        message = 'Se requiere Correo y contraseña'
        return jsonify({'message': message}), 400

    admin = Admin.query.filter_by(
        email=email
    ).first()

    if not admin:
        return jsonify({'message': 'El admin no esta registrado'}), 401

    match_password = check_hash(password, admin.password)

    # Compara los hashes de las contraseñas
    if not match_password:
        return jsonify({'message': 'Las credenciales son incorrectas'}), 401

    # Genera el token JWT si las credenciales son válidas
    expires = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)

    data = {'type': 'admin', 'user': admin.serialize(), 'exp': expires}
    token = jwt.encode(data, SECRET_KEY, algorithm='HS256')

    return jsonify({'token': token, 'exp': expires}), 200


def register_admin():
    data = request.get_json()
    names = data.get('names')
    email = data.get('email')
    password = data.get('password')

    if not email or not password or not names:
        message = 'Se requieren Nombres, Correo y Contraseña'
        return jsonify({'message': message}), 400

    admin = Admin.query.filter_by(
        email=email
    ).first()

    if admin:
        return jsonify({'message': 'El asesor ya existe'}), 401

    hashed_password = hash_password(password)

    new_admin = Admin(
        names=names,
        email=email,
        password=hashed_password
    )

    db.session.add(new_admin)
    db.session.commit()

    return jsonify(new_admin.serialize()), 201
