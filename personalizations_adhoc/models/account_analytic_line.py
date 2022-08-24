from odoo.osv import expression
from odoo.addons.sale_timesheet.models.account import AccountAnalyticLine


def _timesheet_get_portal_domain(self):

    #Heredamos este método para modificar el dominio y solamente tener en cuenta horas facturadas para mostrar en el portal de clientes
    #Esto es para que al consultar los clientes el consumo de sus horas en el portal no aparezcan horas imputadas en tickets de mesa de ayuda por ejemplo.

    domain = super(AccountAnalyticLine, self)._timesheet_get_portal_domain()
    return expression.AND(
        [domain, [('timesheet_invoice_type', 'in', ['billable_time', 'billable_fixed'])]])


AccountAnalyticLine._timesheet_get_portal_domain = _timesheet_get_portal_domain
