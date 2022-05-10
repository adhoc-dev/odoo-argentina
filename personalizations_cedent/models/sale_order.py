from logging.config import dictConfig
from mailbox import NoSuchMailboxError
from odoo import  models
from odoo.tools.safe_eval import safe_eval

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _get_applicable_programs(self):
        programs = super()._get_applicable_programs()
        programs = programs.filtered(lambda p: p._check_available_stock(self))
        return programs

    def _get_applicable_no_code_promo_program(self):
        programs = super()._get_applicable_no_code_promo_program()
        programs = programs.filtered(lambda p: p._check_available_stock(self))
        return programs
