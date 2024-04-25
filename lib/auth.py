from flask import request, jsonify
import jwt
from functools import wraps
from typing import NamedTuple, Union
from models.client import Client
from models.manager import Manager
from models.admin import Admin
from lib.config import SECRET_KEY
import bcrypt


class UserData(NamedTuple):
    type: str
    user: Union[Admin, Manager, Client]


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]

        if not token:
            return jsonify({'message': 'Token faltante'}), 401

        try:
            data_decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_type_decoded = data_decoded['type']
            user_data_decoded = data_decoded['user']

            user = None

            if user_type_decoded == 'manager':
                user = Client.query.get(user_data_decoded['id'])
            elif user_type_decoded == 'client':
                user = Manager.query.get(user_data_decoded['id'])
            elif user_type_decoded == 'admin':
                user = Admin.query.get(user_data_decoded['id'])

            if not user:
                return jsonify({'message': 'Usuario no encontrado'}), 401

            if user.id != user_data_decoded["id"]:
                return jsonify({'message': 'Credenciales incorrectas'}), 401

        except Exception as e:
            print(e)
            return jsonify({'message': 'Token inválido'}), 401

        return f(*args, **kwargs)

    return decorated


def get_token_required(f, list_type_users=[]):
    @wraps(f)
    def decorated(*args, **kwargs):

        if list_type_users == []:
            return f(*args, **kwargs)

        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]

        if not token:
            return jsonify({'message': 'Token faltante'}), 401

        try:
            data_decoded = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=["HS256"]
            )
            user_type_decoded = data_decoded['type']
            user_data_decoded = data_decoded['user']

            if user_type_decoded not in list_type_users:
                return jsonify({'message': 'Usuario no autorizado'}), 401

            user_data = None

            if user_type_decoded == 'client':
                user = Client.query.get(user_data_decoded['id'])
                user_data = {
                    'type': 'client',
                    'user': user
                }
            elif user_type_decoded == 'manager':
                user = Manager.query.get(user_data_decoded['id'])
                user_data = {
                    'type': 'manager',
                    'user': user
                }
            elif user_type_decoded == 'admin':
                user = Admin.query.get(user_data_decoded['id'])
                user_data = {
                    'type': 'admin',
                    'user': user
                }

            if not user_data:
                return jsonify({'message': 'Usuario no encontrado'}), 401

            return f(user_data, *args, **kwargs)

        except Exception as e:
            print(e)
            error_message = 'Token inválido: ' + str(e)
            return jsonify({'message': error_message}), 401

    return decorated


def hash_password(password):
    bytes = password.encode('utf-8')

    # generating the salt
    salt = bcrypt.gensalt()

    # Hashing the password
    hashed_password_provided = bcrypt.hashpw(bytes, salt)

    return hashed_password_provided


def check_hash(password, hashed_password):
    userBytes = password.encode('utf-8')
    match_password = bcrypt.checkpw(userBytes, hashed_password)
    return match_password
