from flask_mail import Mail, Message
from lib.config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS

# Configurar el servidor de correo
mail_server = SMTP_HOST
mail_port = SMTP_PORT
mail_username = SMTP_USER
mail_password = SMTP_PASS
mail_use_tls = True

config = {
    'MAIL_SERVER': mail_server,
    'MAIL_PORT': mail_port,
    'MAIL_USERNAME': mail_username,
    'MAIL_PASSWORD': mail_password,
    'MAIL_USE_TLS': mail_use_tls
}

# Crear una instancia de Mail sin una aplicación Flask
mail = Mail()

mail.init_mail(config)