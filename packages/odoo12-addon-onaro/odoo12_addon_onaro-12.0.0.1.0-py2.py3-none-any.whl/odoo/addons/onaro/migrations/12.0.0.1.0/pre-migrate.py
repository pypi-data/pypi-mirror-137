# Onaro X.Y.Z+1: CRMLeadLine, SaleOrderLine y ContractLine apuntan a productos del catalogo atiguo y tenemos que sustituir las referencias por productos del catalogo nuevo.
#   - Pre:
#       1. Crear mapeo de productos antiguos a nuevos.
#       2. Recorrer los CRMLeadLine, SaleOrderLine, ContractLine y sustituir el producto por la nueva referencia.
from odoo import SUPERUSER_ID, api

import logging

_logger = logging.getLogger(__name__)


def change_product(cr, model):
    env = api.Environment(cr, SUPERUSER_ID, {})

    products_map = dict([
        (2, "GSM Recurring ['Sin Minutos', 'Sin Datos']"),
        (3, "GSM Recurring ['150 Min', '2 GB']"),
        (4, "GSM Recurring ['200 Min', '3 GB']"),
        (5, "GSM Recurring ['200 Min', '5 GB']"),
        (6, "GSM Recurring ['Llamadas Ilimitadas', 'Sin Datos']"),
        (7, "GSM Recurring ['Llamadas Ilimitadas', '9 GB']"),
        (8, "GSM Recurring ['Llamadas Ilimitadas', '23 GB']"),
        (9, "GSM Recurring ['Llamadas Ilimitadas', '30 GB']"),
        (10, "GSM Recurring ['Llamadas Ilimitadas', '50 GB']"),
        (11, "Radiofrequency Recurring ['30 Mb']"),
        (12, "Fiber Recurring ['100 Mb']"),
        (13, "Fiber Recurring ['600 Mb']"),
        (14, "Landline Recurring []"),
        (16, "GSM Recurring ['Llamadas Ilimitadas', '5 GB']"),
    ])

    records = env[model].search([])
    for record in records:
        _logger.info('START: {} {}, current product id: {}, current product name: {}'.format(model, record.id, record.product_id.id, record.product_id.showed_name))
        new_product = env['product.product'].search([
            ('showed_name', '=', products_map[record.product_id.id]),
        ])
        record.product_id = new_product.id
        _logger.info('END: {} {}, current product id: {}, current product name: {}'.format(model, record.id, record.product_id.id, record.product_id.showed_name))

def migrate(cr, version):
    change_product(cr, "crm.lead.line")
    change_product(cr, "sale.order.line")
    change_product(cr, "contract.line")
