from odoo import models, fields


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    sla_deadline = fields.Datetime(tracking=True)

    def _compute_sla_deadline(self):
        """ Evitamos que se recomputen los tickets de equipos que NO usan sla. Es decir, solo llamamos a recomputar
        los que tienen SLA.
        Este cambio va de la mano del cambio de vista que hacemos para hacer editable el campo deadline
        """
        with_sla = self.filtered('use_sla')
        return super(HelpdeskTicket, with_sla)._compute_sla_deadline()
