import os

from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask_cors import CORS
from lib.auth import token_required
from models.user import db
from controllers.demo_controller import protegido
from controllers.auth_controller import login_with_secret
from controllers.user_controller import get_users, create_user
from lib.odoo import get_leads, get_client, get_partner_subscription

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5000"}})
app.config['SQLALCHEMY_DATABASE_URI'] =  os.getenv('DATABASE_URI') or 'sqlite:///example.db'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'tu_clave_secreta'

db.init_app(app)

with app.app_context():
    db.create_all()

app.add_url_rule('/api/login', view_func=login_with_secret(app.config['SECRET_KEY']), methods=['POST'])
app.add_url_rule('/api/users', view_func=create_user, methods=['POST'])

app.add_url_rule('/api/users', view_func=get_users, methods=['GET'])
app.add_url_rule('/api/partners', view_func=get_client, methods=['GET'])
app.add_url_rule('/api/partner_subscription', view_func=get_partner_subscription, methods=['GET'])
app.add_url_rule('/api/leads', view_func=get_leads, methods=['GET'])
app.add_url_rule('/api/protegido', view_func=token_required(app.config['SECRET_KEY'])(protegido), methods=['GET'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
