from lib.config import SQLALCHEMY_DATABASE_URI
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from lib.auth import get_token_required
from models.db import db
from controllers.user_controller import get_users
from controllers.auth.client_controller import login_client, register_client
from controllers.auth.manager_controller import login_manager, register_manager
from controllers.auth.admin_controller import login_admin, register_admin
from lib.odoo import get_leads, get_client, get_partner_subscription

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
    view_func=get_token_required(register_admin, ['admin']),
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

app.add_url_rule('/api/partners', view_func=get_client, methods=['GET'])

app.add_url_rule(
    '/api/partner_subscription',
    view_func=get_partner_subscription,
    methods=['GET']
)

app.add_url_rule('/api/leads', view_func=get_leads, methods=['GET'])
# endregion Rest


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
