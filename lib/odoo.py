from lib.config import ODOO_URL, ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD
from flask import jsonify, request
import xmlrpc.client
from lib.auth import UserData
from models.client import Client

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


def get_partner_subscription(user_data=None):
    user: Client = user_data.get("user")
    doc_nro = user.serialize()["doc_nro"]
    list_partner_subscription = []
    sale_subscription = models.execute_kw(db, uid, password, 'sale.subscription', 'search_read', [[['x_studio_nro_de_documento', '=', doc_nro]]],
                                          {'fields': ['x_studio_nro_de_documento', 'partner_id',
                                                      'x_studio_nombre_direccion', 'x_studio_correo_electronico',
                                                      'x_studio_tipo_doc', 'stage_id']})
    for rec in sale_subscription:
        field_relational = rec['id']
        phone_partner = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                          [[['id', '=', rec['partner_id'][0]]]],
                                          {'fields': ['phone']})
        sale_subscription_line = models.execute_kw(db, uid, password, 'sale.subscription.line', 'search_read',
                                                   [[['analytic_account_id',
                                                       '=', field_relational]]],
                                                   {'fields': ['price_unit', 'product_id', 'x_studio_mbps']})
        data_partner_subscription = {'id': field_relational,
                                     'partner_name': rec['partner_id'][1],
                                     'state_subscription': rec['stage_id'][1],
                                     'type_document': rec['x_studio_tipo_doc'],
                                     'number_document': rec['x_studio_nro_de_documento'],
                                     'plan_type': sale_subscription_line[0]['product_id'][1],
                                     'price_subscription': sale_subscription_line[0]['price_unit'],
                                     'email': str(rec['x_studio_correo_electronico']),
                                     'address': str(rec['x_studio_nombre_direccion']),
                                     'phone': phone_partner[0]['phone'],
                                     }
        list_partner_subscription.append(data_partner_subscription)
    return jsonify({'messagee': 'Datos obtenidos satisfacotiramente', 'data': list_partner_subscription})


def get_partner_bill(user_data=None, subscription_id=None):
    if subscription_id is None:
        return jsonify({'messagee': 'Debe enviar el subscription_id', 'data': []}), 400

    list_partner_bills = []

    fields = [
        'name',
        'x_studio_nro_de_documento',
        'amount_total',
        'amount_residual',
        'partner_id',
        'amount_untaxed',
        'x_studio_producto',
        'invoice_date'
    ]

    meta = {
        'fields': fields,
        'limit': 6,
        'order': 'id DESC'
    }

    search = [['x_studio_subscription_id.id', '=', subscription_id]]

    partner_invoice = models.execute_kw(
        db, uid, password, 'account.move', 'search_read', [search], meta
    )

    for rec in partner_invoice:
        field_relational = rec['id']
        partner_discount_invoice = models.execute_kw(db, uid, password, 'account.move.line', 'search_read',
                                                     [[['move_id.id', '=',
                                                         field_relational]]],
                                                     {'fields': ['product_id', 'x_studio_monto_de_descuento']})

        sale_subscription = models.execute_kw(db, uid, password, 'sale.subscription', 'search_read',
                                              [[['id',
                                                 '=', subscription_id]]],
                                              {'fields': ['x_plan_actual_id', 'x_studio_nombre_direccion', 'x_studio_contrato_id']})

        contrato_id = sale_subscription[0]['x_studio_contrato_id']

        data_partner_subscription = {'invoice_id': field_relational,
                                     'partner_name': rec['partner_id'][1],
                                     'number_document': rec['x_studio_nro_de_documento'],
                                     'invoice_date': rec['invoice_date'],
                                     'street': sale_subscription[0]['x_studio_nombre_direccion'],
                                     'plan_name': sale_subscription[0]["x_plan_actual_id"][1],
                                     'plan_name_invoice': rec['x_studio_producto'],
                                     'amount_discount_invoice': round(partner_discount_invoice[0]['x_studio_monto_de_descuento'], 2),
                                     'amount_subtotal': rec['amount_untaxed'],
                                     'amount_total': rec['amount_total'],
                                     'amount_residual': rec['amount_residual'],
                                     'IGV': round(rec['amount_total']-rec['amount_untaxed'], 2),
                                     'contract_number': contrato_id[1] if contrato_id else contrato_id,
                                     'date_due': '5 del Siguiente Mes',
                                     }

        if data_partner_subscription['plan_name_invoice']:
            if "Mbps" in data_partner_subscription['plan_name_invoice']:
                list_partner_bills.append(data_partner_subscription)
    return jsonify({'messagee': 'Datos obtenidos satisfacotiramente', 'data': list_partner_bills})
