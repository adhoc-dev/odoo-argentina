from odoo import api, models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    supplier_invoicing_company_id = fields.Many2one('res.company', string="Compañia de Facturacion de Proveedor", required=False)
