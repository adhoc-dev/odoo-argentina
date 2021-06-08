from odoo import models, fields, api
import datetime

class ProjectTask(models.Model):
    _inherit = 'project.task'

    x_instaladores = fields.Many2one(string="Instaladores", comodel_name="x_instaladores", on_delete="restrict")
    x_instalacion_type = fields.Many2one(string="Tipo Instalación", comodel_name="x_tipoinsta", on_delete="set null", copy=False)
    x_avisado = fields.Boolean(string="Avisado", copy=False)
    x_vendedor = fields.Char(string="Vendedor", related="sale_line_id.salesman_id.name", readonly=True, copy=False)
    x_partner_shipping_name = fields.Char(string="Nombre", related="sale_line_id.order_id.partner_shipping_id.display_name", readonly=True, copy=False)
    x_partner_shipping_street = fields.Char(string="Calle", related="sale_line_id.order_id.partner_shipping_id.street", readonly=True, copy=False)
    x_partner_shipping_street2 = fields.Char(string="Barrio", related="sale_line_id.order_id.partner_shipping_id.street2", readonly=True, copy=False)
    x_partner_shipping_city = fields.Char(string="Ciudad", related="sale_line_id.order_id.partner_shipping_id.city", readonly=True, copy=False)
    x_partner_shipping_state = fields.Many2one(string="Provincia", related="sale_line_id.order_id.partner_shipping_id.state_id", on_delete="set null", readonly=True, copy=False)
    x_partner_shipping_zip = fields.Char(string="CP", related="sale_line_id.order_id.partner_shipping_id.zip", readonly=True, copy=False)
    x_partner_shipping_phone = fields.Char(string="Teléfono", related="sale_line_id.order_id.partner_shipping_id.phone", readonly=True, copy=False)
    x_partner_shipping_mobile = fields.Char(string="Celular", related="sale_line_id.order_id.partner_shipping_id.mobile", readonly=True, copy=False)
    x_partner_shipping_email = fields.Char(string="Email ", related="sale_line_id.order_id.partner_shipping_id.email", readonly=True, copy=False)
    x_partner_name = fields.Char(string="Nombre C", related="sale_line_id.order_id.partner_id.name", readonly=True, copy=False)
    x_partner_mobile = fields.Char(string="Celular C", related="sale_line_id.order_id.partner_id.mobile", readonly=True, copy=False)
    x_partner_phone = fields.Char(string="Teléfono C", related="sale_line_id.order_id.partner_id.phone", readonly=True, copy=False)
    x_partner_email = fields.Char(string="Email C", related="sale_line_id.order_id.partner_id.email", readonly=True, copy=False)
    x_duration = fields.Integer(string="Duración (Días)", copy=False)
    date_start = fields.Datetime(string='Starting Date', default=fields.Datetime.now, index=True, copy=False)
    x_fecha_fin_calc = fields.Date(string="Fecha Fin", compute="_compute_x_fecha_fin_calc", readonly=True, copy=False, store=True)
    x_department = fields.Many2one(string="Departamento", comodel_name="x_res.country.state.department", on_delete="set null", copy=False)

    @api.depends('date_start','x_duration')
    def _compute_x_fecha_fin_calc(self):
        for record in self:
            record[("x_fecha_fin_calc")] = record.date_start + datetime.timedelta(days=record.x_duration)
