from odoo import models, fields


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    x_sale_order = fields.Many2one(string="Presupuesto", comodel_name="sale.order", on_delete="set null", copy=False)
    x_saleorder_phone = fields.Char(string="Teléfono Inst.", related="x_sale_order.partner_shipping_id.phone", readonly=True, copy=False, store=True)
    x_saleorder_mobile = fields.Char(string="Celular Inst.", related="x_sale_order.partner_shipping_id.mobile", readonly=True, copy=False, store=True)
    x_sale_order_street = fields.Char(string="Calle Inst.", related="x_sale_order.partner_shipping_id.street", readonly=True, copy=False, store=True)
    x_saleorder_street2 = fields.Char(string="Barrio Inst.", related="x_sale_order.partner_shipping_id.street2", readonly=True, copy=False, store=True)
    x_saleorder_state = fields.Char(string="Estado Inst.", related="x_sale_order.partner_shipping_id.state_id.name", help="Administrative divisions of a country. E.g. Fed. State, Departement, Canton", readonly=True, copy=False, store=True)
    x_dropbox_adress = fields.Char(string="Info", copy=False)
    x_task_partner_mobile = fields.Char(string="Celular Cliente", related="task_id.x_partner_shipping_mobile", readonly=True, copy=False, store=True)
    x_task_parnter_phone = fields.Char(string="Teléfono Cliente", related="task_id.x_partner_shipping_phone", readonly=True, copy=False, store=True)
    x_task_partner_street = fields.Char(string="Calle Cliente", related="task_id.x_partner_shipping_street", readonly=True, copy=False, store=True)
    x_task_partner_street2 = fields.Char(string="Barrio Cliente", related="task_id.x_partner_shipping_street2", readonly=True, copy=False, store=True)
    x_task_partner_city = fields.Char(string="Ciudad Cliente", related="task_id.x_partner_shipping_city", readonly=True, copy=False, store=True)
    x_task_partner_state = fields.Many2one(string="Provincia", related="task_id.x_partner_shipping_state", on_delete="set null", readonly=True, copy=False, store=True)
    x_datetime_start = fields.Datetime(string="Fecha Inicio", copy=False)
    x_task_instaladores = fields.Many2one(string="Nombre Inst.", related="task_id.x_instaladores", on_delete="set null", readonly=True, copy=False, store=True)
    x_last_stage_update = fields.Datetime(string="Last  Stage Update", copy=False)
