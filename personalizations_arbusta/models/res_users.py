from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    x_studio_field_rAVo7 = fields.Boolean(string="Auto-Aprobar", copy=False)
    x_studio_field_NM2K0 = fields.Boolean(string="New Campo relacionado", related="self.employee",
                                          help="Check this box if this contact is an Employee.",
                                          readonly=True, copy=False, store=True)
