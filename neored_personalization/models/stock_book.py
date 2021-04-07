##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import fields, models


class StockBook(models.Model):
    _inherit = 'stock.book'

    print_report_number = fields.Boolean(string='Imprimir Número', default=True)
