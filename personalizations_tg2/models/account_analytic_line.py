from odoo import api, models, fields
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    x_presupuestado = fields.Boolean(string="Presupuestado")

    @api.onchange('unit_amount', 'product_id')
    def complete_analytic_price(self):
        for rec in self:
            if rec.product_id and rec.unit_amount:
                rec.amount = rec.product_id.standard_price * rec.unit_amount
            else:
                rec.amount = 0.0

    @api.onchange('project_id')
    def set_domain_to_account_id(self):
        if len(self) == 1:
            return {'domain': {'account_id': [('id', 'child_of', self.project_id.analytic_account_id.id)]}}

    @api.constrains('move_id', 'employee_id', 'product_id')
    def _check_product_exists(self):
        for rec in self:
            msg = "Debe elegir un producto para generar la entrada analitica"
            if rec.move_id and rec.move_id.journal_id.type != 'general' and not rec.employee_id and not rec.product_id:
                ValidationError(msg)
            elif not rec.move_id and not rec.employee_id and not rec.product_id:
                ValidationError(msg)
            else:
                continue

    @api.model
    def create(self, vals):
        res = super(AccountAnalyticLine, self).create(vals)
        msg = ''
        if res.move_id and res.move_id.journal_id.type != 'general' and not res.employee_id and not res.product_id:
            msg = "Debe elegir un producto para generar la entrada analitica"
        if not res.move_id and not res.employee_id and not res.product_id:
            msg = "Debe elegir un producto para generar la entrada analitica"
        if msg:
            raise ValidationError(msg)
        if not res.product_id and res.employee_id:
            res.write({'product_id': res.employee_id.x_product_id.id, 'amount': -res.employee_id.x_product_id.standard_price * res.unit_amount})
        return res
