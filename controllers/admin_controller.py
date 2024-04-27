from flask import jsonify
from models.admin import Admin
from models.manager import Manager
from models.client import Client


def get_admins(user_data=None):
    admins = Admin.query.all()

    serialized_admins = [admin.serialize() for admin in admins]

    return jsonify({
        'data': serialized_admins
    })


def get_managers(user_data=None):
    managers = Manager.query.all()

    serialized_managers = [manager.serialize() for manager in managers]

    return jsonify({
        'data': serialized_managers
    })


def get_clients(user_data=None):
    clients = Client.query.all()

    serialized_clients = [client.serialize() for client in clients]

    return jsonify({
        'data': serialized_clients
    })
