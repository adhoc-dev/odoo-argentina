from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    x_studio_field_5G9jj = fields.Char(string="ISBN", copy=False)
    x_studio_field_EqNtz = fields.Many2one(string="Editorial", comodel_name="x_product_editorial", on_delete="set null", copy=False)
    x_studio_field_euxHW = fields.Many2one(string="Autor", comodel_name="x_product_autor", on_delete="set null", copy=False)
    x_studio_field_nqwdw = fields.Many2one(string="Versión", comodel_name="x_product_version", on_delete="set null", copy=False)
    x_studio_field_k203V = fields.Many2one(string="Idioma", comodel_name="x_product_language", on_delete="set null", copy=False)
    x_studio_field_NlwHP = fields.Many2one(string="Familia", comodel_name="x_product_familia", on_delete="set null", copy=False)
    x_studio_field_Bn7Ka = fields.Many2one(string="Presupuesto", comodel_name="x_product_categoria", on_delete="set null", copy=False)
    x_studio_field_8WqdD = fields.Many2one(string="Subcategoria", comodel_name="x_product_subcategoria", on_delete="set null", copy=False)
