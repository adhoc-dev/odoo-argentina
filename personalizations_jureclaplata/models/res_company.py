from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    nro_entidad_bapro = fields.Char(string="Número de Entidad Bapro", size=9,
        help="Numero de entidad otorgado por Bapro Medios de Pagos SA")

    header_left = fields.Html(help="Header text displayed at the left-top of reports.")
    header_right = fields.Html(help="Header text displayed at the right-top of reports.")

    first_due_date_days = fields.Integer(string="Días a vencimiento 1")
    second_due_date_days = fields.Integer(string="Días a vencimiento 2")
    surcharge = fields.Float(string="Recargo [%]")

    red_link_code = fields.Char('Codigo de Ente Red Link', size=3)
    red_link_volumen = fields.Integer('Volumen (Dia)', default=1, help='Campo Tecnico: Numero Volumen usado de Red Link (por dia)')

    def action_cron_restart_red_link_volumen_count(self):
        """ resetea el volumen de manera diaria """
        self.search([('red_link_code', '!=', False)]).red_link_volumen = 1

    def action_cron_restart_red_link_id_deuda(self):
        """ resetea los id de duda de estudiantes a 1 """
        self.env['res.partner'].search([('partner_type', '=', 'student'), ('red_link_id_deuda', '!=', 1)]).red_link_id_deuda = 1
