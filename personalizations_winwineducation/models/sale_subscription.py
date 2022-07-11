from odoo import models, fields, api


class SaleSubscription(models.Model):
    _inherit = 'sale.subscription'

    x_renewal_lead_id = fields.Many2one(string="Oportunidad de renovación", comodel_name="crm.lead", on_delete="set null")
    x_renewal_state = fields.Selection(string="Estado rematriculación", selection=[('er','En proceso de rematriculación'),('r','Rematricula'),('nr','No rematricula'),('sr','Sin proceso de rematriculación')], compute="_compute_x_renewal_state", readonly=True, copy=False, store=True)

    partner_phone = fields.Char(related='partner_id.phone', string='Contacto del familiar')
    partner_email = fields.Char(related='partner_id.email', string='Correo electrónico')
    partner_semaforo = fields.Selection(related='partner_id.semaforo', string='Situación de Semáforo')

    @api.depends('x_renewal_lead_id.probability')
    def _compute_x_renewal_state(self):
        for rec in self:
          if rec.x_renewal_lead_id:
            if rec.x_renewal_lead_id.probability == 0:
              rec['x_renewal_state'] = 'nr'
            elif rec.x_renewal_lead_id.probability > 0 and rec.x_renewal_lead_id.probability < 100:
              rec['x_renewal_state'] = 'er'
            elif rec.x_renewal_lead_id.probability == 100:
              rec['x_renewal_state'] = 'r'
          else:
            rec['x_renewal_state'] = 'sr'
