from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    birthdate = fields.Date(string='Fecha de Nacimiento')
    age = fields.Integer(string='Edad', compute="_compute_age")
    credit_card_id = fields.Many2one(comodel_name='res.partner.credit_card', string='Tarjeta de Crédito')
    bank_id = fields.Many2one(comodel_name='res.bank', string='Banco Emisor')

    @api.depends("birthdate")
    def _compute_age(self):
        for record in self:
            if record.birthdate:
                record.age = (fields.Date.today().year - record.birthdate.year -
                             ((fields.Date.today().month, fields.Date.today().day)
                             < (record.birthdate.month, record.birthdate.day)))
            else:
                record.age = False
