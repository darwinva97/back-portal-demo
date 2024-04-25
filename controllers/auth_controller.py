from flask import request, jsonify
import jwt
import datetime

from models.db import db
from models.client import Client
from models.manager import Manager
from models.admin import Admin

from lib.auth import check_hash, hash_password
from lib.odoo import get_clientid_by_creds


def register():
    data = request.get_json()
    doc_nro = data.get('doc_nro')
    password = data.get('password')

    if not doc_nro or not password:
        message = 'Se requieren el Documento y contraseña'
        return jsonify({'message': message}), 400

    odoo_client_id = get_clientid_by_creds(doc_nro)

    if not odoo_client_id:
        return jsonify({'message': 'El usuario no existe'}), 400

    usuario = Client.query.filter_by(
        username=odoo_client_id
    ).first()

    if usuario:
        return jsonify({'message': 'El usuario ya existe'}), 401

    hashed_password = hash_password(password)

    nuevo_usuario = Client(
        username=odoo_client_id, password=hashed_password)

    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify(nuevo_usuario.serialize()), 201


def login_with_secret(secret_key):
    def login():
        data = request.get_json()
        password = data.get('password')
        doc_nro = data.get('doc_nro')

        if not doc_nro or not password:
            message = 'Se requiere Documento y contraseña'
            return jsonify({'message': message}), 400

        odoo_client_id = get_clientid_by_creds(doc_nro)

        if not odoo_client_id:
            return jsonify({'message': 'El usuario no existe'}), 400

        usuario = Client.query.filter_by(
            username=odoo_client_id
        ).first()

        if not usuario:
            return jsonify({'message': 'El usuario no esta registrado'}), 401

        match_password = check_hash(password, usuario.password)

        # Compara los hashes de las contraseñas
        if not match_password:
            return jsonify({'message': 'Las credenciales son incorrectas'}), 401

        # Genera el token JWT si las credenciales son válidas
        expires = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data = {type: 'client', 'user': usuario.serialize(), 'exp': expires}
        token = jwt.encode(data, secret_key, algorithm='HS256')

        return jsonify({'token': token, 'exp': expires}), 200

    return login


def manager_login_with_secret(secret_key):
    def login():
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
            return jsonify({'message': 'El asesor no existe'}), 401

        match_password = check_hash(password, manager.password)

        # Compara los hashes de las contraseñas
        if not match_password:
            return jsonify({'message': 'Las credenciales son incorrectas'}), 401

        # Genera el token JWT si las credenciales son válidas
        expires = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data = {'type': 'client', 'user': manager.serialize(), 'exp': expires}
        token = jwt.encode(data, secret_key, algorithm='HS256')

        return jsonify({'token': token, 'exp': expires}), 200

    return login


def admin_login_with_secret(secret_key):
    def login():
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            message = 'Se requiere Correo y Contraseña'
            return jsonify({'message': message}), 400

        admin = Admin.query.filter_by(
            email=email
        ).first()

        if not admin:
            return jsonify({'message': 'El admin no existe'}), 401

        match_password = check_hash(password, admin.password)

        # Compara los hashes de las contraseñas
        if not match_password:
            return jsonify({'message': 'Las credenciales son incorrectas'}), 401

        # Genera el token JWT si las credenciales son válidas
        expires = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data = {'type': 'client', 'user': admin.serialize(), 'exp': expires}
        token = jwt.encode(data, secret_key, algorithm='HS256')

        return jsonify({'token': token, 'exp': expires}), 200

    return login
