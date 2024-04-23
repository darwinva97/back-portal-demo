from flask import jsonify

def protegido():
    return jsonify({'message': 'Esta es una ruta protegida!'})