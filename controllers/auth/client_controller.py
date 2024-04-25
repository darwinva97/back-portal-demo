from flask import request, jsonify
import jwt
import datetime
from typing import Union

from models.db import db
from models.client import Client
from models.manager import Manager
from models.admin import Admin

from lib.auth import check_hash, hash_password, UserData
from lib.odoo import get_clientid_by_creds
from lib.config import SECRET_KEY


def login_client():
    data = request.get_json()
    password = data.get('password')
    doc_nro = data.get('doc_nro')

    if not doc_nro or not password:
        message = 'Se requieren el Documento y contraseña'
        return jsonify({'message': message}), 400

    odoo_client_id = get_clientid_by_creds(doc_nro)

    if not odoo_client_id:
        return jsonify({'message': 'El usuario no existe'}), 400

    client = Client.query.filter_by(
        odoo_client_id=odoo_client_id
    ).first()

    if not client:
        return jsonify({'message': 'El cliente no esta registrado en odoo'}), 401

    match_password = check_hash(password, client.password)

    # Compara los hashes de las contraseñas
    if not match_password:
        return jsonify({'message': 'Las credenciales son incorrectas'}), 401

    # Genera el token JWT si las credenciales son válidas
    expires = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    data = {'type': 'client', 'user': client.serialize(), 'exp': expires}
    token = jwt.encode(data, SECRET_KEY, algorithm='HS256')

    return jsonify({'token': token, 'exp': expires}), 200


def register_client(user_data: UserData):
    data = request.get_json()
    doc_nro = data.get('doc_nro')
    password = data.get('password')

    user = user_data.get('user')
    user_type = user_data.get("type")

    if user_type != 'manager' and user_type != 'admin':
        return jsonify({'message': 'No autorizado'}), 401

    created_by = user.id
    created_by_type = user_type

    if not doc_nro or not password or not created_by_type or not created_by:
        message = 'Se requiere Documento y Contraseña. Y debe ser creado por el Asesor o Administrador'
        return jsonify({'message': message}), 400

    odoo_client_id = get_clientid_by_creds(doc_nro)

    if not odoo_client_id:
        return jsonify({'message': 'El cliente no existe en odoo'}), 400

    client = Client.query.filter_by(
        odoo_client_id=odoo_client_id,
    ).first()

    if client:
        return jsonify({'message': 'El cliente ya existe'}), 401

    hashed_password = hash_password(password)

    new_client = Client(
        odoo_client_id=odoo_client_id,
        doc_nro=doc_nro,
        password=hashed_password,
        created_by=created_by,
        created_by_type=created_by_type
    )

    db.session.add(new_client)
    db.session.commit()

    return jsonify(new_client.serialize()), 201
