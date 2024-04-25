from flask import request, jsonify
from models.client import db, Client
from lib.auth import hash_password

def create_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Se requieren username y password'}), 400

    if Client.query.filter_by(username=username).first():
        return jsonify({'message': 'El username ya está en uso'}), 400

    hashed_password = hash_password(password)

    nuevo_usuario = Client(username=username, password=hashed_password)
    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify(nuevo_usuario.serialize()), 201  # Serialize el nuevo usuario antes de devolverlo
    
def get_users():
    users = Client.query.all()
    return jsonify([user.serialize() for user in users])