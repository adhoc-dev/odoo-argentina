from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    birthdate = fields.Date(string='Fecha de Nacimiento')
    highschool_complete = fields.Boolean(string='Secundario Completo')
    age = fields.Integer(string='Edad', compute="_compute_age")
    credit_card_id = fields.Many2one('res.partner.credit_card', 'Tarjeta de Crédito')
    bank_id = fields.Many2one(comodel_name='res.bank', string='Banco Emisor')
    automatic_debit = fields.Selection([('si','Si'), ('no','No')], string="Débito automático")
    debit_day = fields.Selection([
        ('1','1'), ('2','2'), ('3','3'), ('4','4'), ('5','5'), ('6','6'), ('7','7'),
        ('8','8'), ('9','9'), ('10','10'), ('11','11'), ('12','12'), ('13','13'),
        ('14','14'), ('15','15'), ('16','16'), ('17','17'), ('18','18'), ('19','19'),
        ('20','20'), ('21','21'), ('22','22'), ('23','23'), ('24','24'), ('25','25'),
        ('26','26'), ('27','27'), ('28','28'), ('29','29'), ('30','30'), ('31', '31')
        ], string="Día del débito")

    @api.depends("birthdate")
    def _compute_age(self):
        for record in self:
            if record.birthdate:
                record.age = (fields.Date.today().year - record.birthdate.year -
                              ((fields.Date.today().month, fields.Date.today().day)
                              < (record.birthdate.month, record.birthdate.day)))
            else:
                record.age = False
