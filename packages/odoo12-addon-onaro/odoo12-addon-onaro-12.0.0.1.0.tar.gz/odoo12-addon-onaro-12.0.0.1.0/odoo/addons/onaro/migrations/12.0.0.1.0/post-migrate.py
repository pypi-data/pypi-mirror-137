# Producto
# Onaro X.Y.Z+1: CRMLeadLine, SaleOrderLine y ContractLine apuntan a productos del catalogo atiguo y tenemos que sustituir las referencias por productos del catalogo nuevo.
#   - Post: Recomputar el product_id de Contrato. TODO: Mirar si hay mas campos que recomputar.
from odoo import SUPERUSER_ID, api

import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})

    models = [
        env['sale.order'],
        env['contract.contract'],
    ]

    for model in models:
        _logger.info('BEFORE')
        # We could not recompute the following contracts: 239, 264, 283, 92, 175, 176
        env.add_todo(model._fields['product_id'], model.search([]))
        model.recompute()
        _logger.info('AFTER')
