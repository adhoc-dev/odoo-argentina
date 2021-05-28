from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    send_automatic_pending_email = fields.Boolean("Envío automático de mis pendientes", help="Al tener esto activado se enviara un mail con las pendientes por comercial de OV")
    send_automatic_debt_email = fields.Boolean("Envio automatico de deuda de facturas", help="Al tener esto activado se enviara un mail con las facturas de deuda por comercial de factura")
