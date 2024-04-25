from flask import request, jsonify
from models.client import db, Client
from lib.auth import hash_password

def get_users():
    users = Client.query.all()
    return jsonify([user.serialize() for user in users])