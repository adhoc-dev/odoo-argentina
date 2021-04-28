from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    x_so_create_uids = fields.Many2many(string="Usuario creador OV", comodel_name="res.users", relation="False", column1="False", column2="False", compute="_compute_x_so_create_uids", readonly=True, copy=False)
    x_so_create_uid = fields.Many2one(string="Usuario Creador OV", comodel_name="res.users", compute="_compute_x_so_create_uid", readonly=True, copy=False)
    x_pricelist_id = fields.Many2one(string="Lista Precios de NV", comodel_name="product.pricelist", compute="_compute_x_pricelist_id", help="Lista de precios de Nota de venta", on_delete="set null", readonly=True, copy=False)

    @api.depends('sale_order_ids')
    def _compute_x_so_create_uids(self):
        for record in self:
                record['x_so_create_uids'] = record.sale_order_ids.mapped('create_uid')

    @api.depends('sale_order_ids')
    def _compute_x_so_create_uid(self):
        for record in self:
            ids = record.sale_order_ids.mapped('create_uid')
            record['x_so_create_uid'] = ids[0] if len(ids) else False

    @api.depends('sale_order_ids')
    def _compute_x_pricelist_id(self):
        for record in self:
              record['x_pricelist_id'] = record.sale_order_ids and record.sale_order_ids.mapped('pricelist_id')[0] or False
