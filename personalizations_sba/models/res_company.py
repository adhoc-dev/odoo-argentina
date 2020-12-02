from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    x_rango_fecha_recargo = fields.Integer(string="Cantidad de días por recargo", help="Establezca la cantidad de días de recargo desde la fecha de vencimiento de la factura.", copy=False)
