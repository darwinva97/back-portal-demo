from flask import request, jsonify
import jwt
import datetime
from lib.auth import check_hash
from models.user import Usuario
from lib.odoo import get_client

def login_with_secret(secret_key):
    def login():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        client = get_client(username)

        if not client:
            return jsonify({'message': 'Tu usuario no se encuentro registrado'}), 400

        if not username or not password:
            return jsonify({'message': 'Se requieren username y password'}), 400

        usuario = Usuario.query.filter_by(username=username).first()
        if not usuario:
            return jsonify({'message': 'Credenciales incorrectas'}), 401
        
        match_password  = check_hash(password, usuario.password)

        # Compara los hashes de las contraseñas
        if not match_password:
            return jsonify({'message': 'Credenciales incorrectas'}), 401

        # Genera el token JWT si las credenciales son válidas
        expires = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data = {'usuario_id': usuario.id, 'exp': expires}
        token = jwt.encode(data, secret_key, algorithm='HS256')
        return jsonify({'token': token, 'exp': expires}), 200

    return login