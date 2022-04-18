from odoo import models, fields


class HrSeniority(models.Model):
    _name = 'hr.seniority'
    _description = 'hr.seniority'
    _order = 'sequence'

    name = fields.Char(required=True)
    description = fields.Text()
    sequence = fields.Integer(default=10)
