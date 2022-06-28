from odoo import models, fields


class XResPartnerStage(models.Model):
    _name = 'x_res.partner_stage'
    _description = 'Contacto etapas'
    _rec_name = 'x_name'

    x_name = fields.Char(string="Name", copy=False)
