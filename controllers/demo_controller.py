from flask import jsonify


def protegido(arg1, arg2):
    return jsonify({'message': 'Esta es una ruta protegida!'})
