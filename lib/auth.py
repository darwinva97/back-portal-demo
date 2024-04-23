from flask import request, jsonify
import jwt
from functools import wraps
from models.user import Usuario
import bcrypt

def token_required(secret_key):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            if 'Authorization' in request.headers:
                token = request.headers['Authorization'].split()[1]

            if not token:
                return jsonify({'message': 'Token faltante'}), 401

            try:
                data = jwt.decode(token, secret_key, algorithms=["HS256"])
                usuario_id = data['usuario_id']
                usuario = Usuario.query.get(usuario_id)
                if not usuario:
                    return jsonify({'message': 'Usuario no encontrado'}), 401

                token = request.headers['Authorization'].split()[1]

                data = jwt.decode(token, secret_key, algorithms=["HS256"])
                usuario_id = data.get('usuario_id')

                # Compara los hashes de las contraseñas
                if usuario.id != usuario_id:
                    return jsonify({'message': 'Credenciales incorrectas'}), 401

            except Exception as e:
                print(e)
                return jsonify({'message': 'Token inválido'}), 401

            return f(*args, **kwargs)

        return decorated
    return decorator

def hash_password(password):
    bytes = password.encode('utf-8') 
  
    # generating the salt 
    salt = bcrypt.gensalt() 
    
    # Hashing the password 
    hashed_password_provided = bcrypt.hashpw(bytes, salt) 

    return hashed_password_provided

def check_hash(password, hashed_password):
    userBytes = password.encode('utf-8') 
    match_password  = bcrypt.checkpw(userBytes, hashed_password)
    return match_password
