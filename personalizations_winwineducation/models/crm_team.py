from odoo import models, fields


class CrmTeam(models.Model):
    _inherit = 'crm.team'

    x_type = fields.Selection(string="Tipo", selection=[('a','Admisión'),('r','Rematriculaciones')])
