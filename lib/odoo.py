from lib.config import ODOO_URL, ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD
from flask import jsonify, request
import xmlrpc.client

url = ODOO_URL
db = ODOO_DB
username = ODOO_USERNAME
password = ODOO_PASSWORD

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))


def get_leads():
    models_data = models.execute_kw(
        db, uid, password, 'x_landing_page', 'search_read', [[]], {})
    return jsonify({'messagee': 'Datos obtenidos satisfacotiramente', 'data': models_data})


def get_clientid_by_creds(doc_nro: str):
    field_nro_doc = "x_studio_nro_de_documento"

    domain = [
        (field_nro_doc, '=', doc_nro)
    ]

    client_ids = models.execute_kw(
        db,
        uid,
        password,
        'sale.subscription',
        'search',
        [domain],
        {'limit': 1}
    )

    if client_ids and client_ids[0]:
        client_id = client_ids[0]

        return client_id

    else:
        return None


def get_client():
    models_data = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                    [[['email', '=', 'azure.Interior24@example.com']]], {'fields': ['name', 'country_id', 'phone']})
    print(models_data)
    return jsonify({'messagee': 'Datos obtenidos satisfacotiramente', 'data': models_data})


def get_partner_subscription():
	partner_subscription = []
	sale_subscription = models.execute_kw(db, uid, password, 'sale.subscription', 'search_read',
									[[['x_studio_nro_de_documento','=', '71767949']]], {'fields': ['x_studio_nro_de_documento', 'partner_id', 'recurring_invoice_line_ids']})
	partner_subscription.append(sale_subscription)
	# sale_subscription_line = models.execute_kw(db, uid, password, 'sale.subscription.line', 'search_read',
	# 								[[['analytic_account_id', '=',sale_subscription[0]]]], {'fields': ['price_unit', 'product_id', 'x_studio_mbps']})
	# partner_subscription.append(sale_subscription_line)

	print(partner_subscription)
	return jsonify({'messagee': 'Datos obtenidos satisfacotiramente', 'data': sale_subscription})

def add_lead():
    lead = request.json

    body = {
        'x_name': lead['x_name'],
        'x_studio_celular': lead['x_studio_celular']
    }

    print(lead['x_name'])
    # # models_data = models.execute_kw(db, uid, password, 'ir.model', 'search_read', [[]], {'fields': ['model', 'name']})
    new_record_id = models.execute_kw(
        db, uid, password, 'x_landing_page', 'create', [body])
    print(new_record_id)
    return jsonify({'mensaje': "Usuario agregado correctamente"}), 201
