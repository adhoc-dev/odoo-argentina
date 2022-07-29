from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    nro_entidad_bapro = fields.Char(string="Número de Entidad Bapro", size=9,
        help="Numero de entidad otorgado por Bapro Medios de Pagos SA")

    header_left = fields.Html(help="Header text displayed at the left-top of reports.")
    header_right = fields.Html(help="Header text displayed at the right-top of reports.")

    first_due_date_days = fields.Integer(string="Días a vencimiento 1")
    second_due_date_days = fields.Integer(string="Días a vencimiento 2")
    surcharge = fields.Float(string="Recargo [%]")
