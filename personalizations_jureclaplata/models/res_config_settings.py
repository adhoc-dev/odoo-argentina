from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    red_link_code = fields.Char(related='company_id.red_link_code', readonly=False)
    red_link_volumen = fields.Integer(related='company_id.red_link_volumen', readonly=False)
