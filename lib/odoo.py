import os
from flask import jsonify, request
import xmlrpc.client

url = os.getenv('ODOO_URL')
db = os.getenv('ODOO_DB')
username = os.getenv('ODOO_USERNAME')
password = os.getenv('ODOO_PASSWORD')

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))

print(common.version())

uid = common.authenticate(db, username, password, {})

print(uid)

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

print('Models loaded')

def get_leads():
	models_data = models.execute_kw(db, uid, password, 'x_landing_page', 'search_read', [[]], {})
	return jsonify({'messagee': 'Datos obtenidos satisfacotiramente', 'data': models_data})

def get_client():
	models_data = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
									[[['email','=', 'azure.Interior24@example.com']]], {'fields': ['name', 'country_id', 'phone']})
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
	new_record_id = models.execute_kw(db, uid, password, 'x_landing_page', 'create', [body])
	print(new_record_id)
	return jsonify({'mensaje': "Usuario agregado correctamente"}), 201