from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    nro_entidad_bapro = fields.Char(string="Número de Entidad Bapro", size=9,
        help="Numero de entidad otorgado por Bapro Medios de Pagos SA")

    first_due_date_days = fields.Integer(string="Días a vencimiento 1")
    second_due_date_days = fields.Integer(string="Días a vencimiento 2")
    surcharge = fields.Float(string="Recargo [%]")
