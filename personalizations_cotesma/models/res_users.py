from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    tag_ids = fields.Many2many(comodel_name="product.template.tag",string="Product Tags",relation="res_user_product_tag_rel",column1="user_id",column2="tag_id")
