from lib.config import SQLALCHEMY_DATABASE_URI, TOKEN_ODOO_CLIENT_REGISTER
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from lib.auth import get_token_required, hash_password
from models.db import db
from models.client import Client
from controllers.user_controller import get_users
from controllers.auth_controller import change_password
from controllers.auth.client_controller import login_client, register_client
from controllers.auth.manager_controller import login_manager, register_manager
from controllers.auth.admin_controller import login_admin, register_admin
from controllers.admin_controller import get_admins, get_managers, get_clients
from lib.odoo import get_leads, get_client, get_partner_subscription, get_partner_bill
from flask import request, jsonify
from lib.mail import mail
from flask_mail import Message
import random
import string

app = Flask(__name__)
domains = [
    'http://127.0.0.1:5000',
    'http://localhost:5000',
    'http://127.0.0.1:5173',
    'http://localhost:5173'
]
CORS(app, resources={r"/api/*": {"origins": domains}})
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

migrate = Migrate(app, db)
db.init_app(app)

with app.app_context():
    db.create_all()

# region Auth


def password_generator(longitud=12):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    contrasena = ''.join(random.choice(caracteres) for _ in range(longitud))
    return contrasena


@app.route('/api/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    document_number = data.get('document_number')
    token = data.get('token')
    id_subscription = data.get('id_subscription')
    partner_email = data.get('partner_email')

    if (document_number is None) or (token is None) or (id_subscription is None):
        return jsonify({'message': "Faltan datos"})

    if token != TOKEN_ODOO_CLIENT_REGISTER:
        return jsonify({'message': "Token invalido"})

    password = password_generator(8)

    hashed_password = hash_password(password)

    new_client = Client(
        odoo_client_id=id_subscription,
        doc_nro=document_number,
        password=hashed_password,
        created_by='AUTOMATIC',
        created_by_type='AUTOMATIC'
    )

    if partner_email:
        pass
        # mensaje = Message(subject="Credenciales Portal",
        #                   recipients=[partner_email],
        #                   body="Se ha creado una nueva cuenta en el portal. Su usuario es: " + document_number + " y su contraseña es: " + password)
        # mail.send(mensaje)

    db.session.add(new_client)
    db.session.commit()

    return jsonify({'data': "Done"}), 200


app.add_url_rule(
    '/api/auth/change_password',
    view_func=get_token_required(
        change_password, ['admin', 'manager', 'client']
    ),
    methods=['POST']
)
# region Client
app.add_url_rule(
    '/api/auth/client/login',
    view_func=login_client,
    methods=['POST']
)

app.add_url_rule(
    '/api/auth/client/register',
    view_func=get_token_required(register_client, ['manager', 'admin']),
    methods=['POST']
)
# endregion Client

# region Admin
app.add_url_rule('/api/auth/admin/login',
                 view_func=login_admin, methods=['POST'])
app.add_url_rule(
    '/api/auth/admin/register',
    view_func=get_token_required(register_admin, []),
    methods=['POST']
)
# endregion Admin

# region Manager
app.add_url_rule('/api/auth/manager/login',
                 view_func=login_manager, methods=['POST'])
app.add_url_rule(
    '/api/auth/manager/register',
    view_func=get_token_required(register_manager, ['admin']),
    methods=['POST']
)
# endregion Manager
# endregion Auth

# region Rest
app.add_url_rule('/api/users', view_func=get_users, methods=['GET'])
app.add_url_rule(
    '/api/admins',
    view_func=get_token_required(get_admins, ['admin']),
    methods=['GET']
)

app.add_url_rule(
    '/api/managers',
    view_func=get_token_required(get_managers, ['admin']),
    methods=['GET']
)

app.add_url_rule(
    '/api/clients',
    view_func=get_token_required(get_clients, ['admin']),
    methods=['GET']
)

app.add_url_rule('/api/partners', view_func=get_client, methods=['GET'])

app.add_url_rule(
    '/api/partner_subscription',
    view_func=get_token_required(get_partner_subscription, ['client']),
    methods=['GET']
)
app.add_url_rule(
    '/api/partner_bill/<subscription_id>',
    view_func=get_token_required(get_partner_bill, ['client']),
    methods=['GET']
)

app.add_url_rule('/api/leads', view_func=get_leads, methods=['GET'])
# endregion Rest


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
