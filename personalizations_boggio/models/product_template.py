from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    x_ubica_sfe = fields.Char(string="Ubicacion SFE", help="Ubicacion SFE")
    x_ubica_sfe2 = fields.Char(string="Ubicacion SFE2", help="Ubicacion SFE")
    x_ubica_raf = fields.Char(string="Ubicacion RAF", help="Ubicacion RAf")
    x_ubica_raf2 = fields.Char(string="Ubicacion RAF2", help="Ubicacion RAF2")
    x_auxiliar_busquedas = fields.Char(string="Auxiliar para busquedas", readonly=True, index=True)
    x_website_catalog = fields.Char(string="Website Catalog")
    x_replenishment_cost_moneda = fields.Float(string="Costo en Moneda", compute="_compute_x_replenishment_cost_moneda", help="Campo de iboggio que calcula el costo final del proveedor en moneda del proveedor", readonly=True, copy=False)
    x_google_product_category = fields.Integer(string="google_product_category", help="Campo para Google Merchant	")
    x_ml_pack_qty = fields.Integer(string="MercadoLibre cantidad por pack", help="si la cantidad es mayor a cero se toma el multiplicador en descripcion y en precio")
    x_energy_efficiency_class = fields.Char(string="Eficiencia Energetica", help="Campos validos"
"A+++"
"A++"
"A+"
"A"
"B"
"C"
"D"
"E"
"F"
"G")
    x_location_aux = fields.Many2one(string="Ubicacion Auxiliar", comodel_name="stock.location", on_delete="set null", copy=False)
    x_energiu = fields.Boolean(string="Energiu")
    x_power = fields.Float(string="Potencia en W", help="Potencia en W para reportes")
    x_documents = fields.Many2one(string="Documentacion", comodel_name="website.doc.toc", help="Visible en presupuesto, remitos y facturas"
"(aplica para términos y condiciones por ejemplo)", on_delete="set null")

    def _compute_x_replenishment_cost_moneda(self):
        for record in self:
             record['x_replenishment_cost_moneda'] = record.replenishment_base_cost_currency_id.inverse_rate >0 and record.replenishment_cost/record.replenishment_base_cost_currency_id.inverse_rate or 0
