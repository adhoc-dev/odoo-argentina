from odoo import models, fields, api
from datetime import timedelta

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    x_client = fields.Many2one(string="Cliente", comodel_name = 'res.partner',
                               on_delete="set null",
                               copy=False)
    x_client_display = fields.Char(compute="compute_display_name")
    x_ultima_ov = fields.Many2one(compute="action_ov_compute",comodel_name = 'sale.order')
    x_last_date = fields.Date(string="Ultima partida")
    x_orden_de_compra = fields.Char(string="Nº Orden de Compra",
                                    readonly=False,
                                    store=True)
    x_quantity = fields.Integer(string="Contenido neto")
    x_cantidad = fields.Char(string="Cantidad")
    x_unity = fields.Many2one(string="Unidad/es", comodel_name = 'uom.uom')
    x_barcode = fields.Char(string="Código de barras")
    x_date_of_delivery = fields.Date(string="Fecha de entrega",
                                    readonly=False,
                                    store=True)
    x_envase_id = fields.Many2one('product.template.containers', string="Tipo de envase")


    x_machine_id = fields.Many2one('product.template.machines', string="Máquinas")
    x_cylinder_ids = fields.Many2many('product.template.cylinder', compute="_compute_cylinder_ids")
    x_cylinder_id = fields.Many2one('product.template.cylinder', string = "Cilindro")


    x_distancia_tacos = fields.Integer(string="Distancia de tacos [mm]")
    x_cantidad_imagenes = fields.Integer(string="Cantidad de imágenes")
    x_ancho_banda = fields.Integer(string="Ancho de banda [mm]")
    x_cantidad_bandas = fields.Integer(string="Cantidad de bandas")
    x_ancho_lamina = fields.Integer(string="Ancho de lámina [mm]",
                                    compute="_ancho_compute")
    x_coil = fields.Many2one('product.template.coil',string="Bobinado nº")
    x_ubicacion_taco = fields.Selection([('Izquierda','Izquierda'),('Derecha','Derecha'),('Ambos','Ambos'),('Sin tacos','Sin tacos'),('Otros','Otros')], string="Ubicación del taco")
    x_ubicacion_taco_otros = fields.Char(string="Describir otro", compute="_otro_taco", readonly=False, store=True)
    x_mts_kg = fields.Integer(string = "Mts x Kg")
    x_kg_1000 = fields.Integer(string = "Kg x 1.000mts")
    x_mts_imprimir = fields.Integer(string = "Mts a imprimir")

    x_diametro_bobina = fields.Char(string="Diam de bobina [mm]")
    x_tara = fields.Integer(string = "Tara [g]")
    x_maximo_bobina = fields.Integer(string = "Peso maximo de bobina [kg]")
    x_minimo_bobina = fields.Integer(string = "Peso Minimo de bobina [kg]")
    x_empalme = fields.Char(string = "Tipo de empalme")

    x_material_imprimir_a = fields.Many2one('product.product',string = "Material a imprimir A")
    x_ancho_a = fields.Many2many('product.template.attribute.value', 'product_template_attribute_value_a_rel', 'product_template_id', 'product_template_attibute_value',  string = "Ancho Material A [mm]")

    x_material_laminar_b = fields.Many2one('product.product', string = "Material a laminar B")
    x_ancho_b = fields.Many2many('product.template.attribute.value' , 'product_template_attribute_value_b_rel', 'product_template_id', 'product_template_attibute_value', string = "Ancho Material B")

    x_material_laminar_c = fields.Many2one('product.product', string = "Material a laminar C")
    x_ancho_c = fields.Many2many('product.template.attribute.value','product_template_attribute_value_c_rel', 'product_template_id', 'product_template_attibute_value', string = "Ancho Material C")

    x_tinta1 = fields.Many2one('product.product', string = "Tinta")
    x_pantone1 = fields.Char(string="Pantone")
    x_anilox1 = fields.Char(string="Anilox")

    x_tinta2 = fields.Many2one('product.product', string = "Tinta")
    x_pantone2 = fields.Char(string="Pantone")
    x_anilox2 = fields.Char(string="Anilox")

    x_tinta3 = fields.Many2one('product.product', string = "Tinta")
    x_pantone3 = fields.Char(string="Pantone")
    x_anilox3 = fields.Char(string="Anilox")

    x_tinta4 = fields.Many2one('product.product', string = "Tinta")
    x_pantone4 = fields.Char(string="Pantone")
    x_anilox4 = fields.Char(string="Anilox")

    x_tinta5 = fields.Many2one('product.product', string = "Tinta")
    x_pantone5 = fields.Char(string="Pantone")
    x_anilox5 = fields.Char(string="Anilox")

    x_tinta6 = fields.Many2one('product.product', string = "Tinta")
    x_pantone6 = fields.Char(string="Pantone")
    x_anilox6 = fields.Char(string="Anilox")

    x_tinta7 = fields.Many2one('product.product', string = "Tinta")
    x_pantone7 = fields.Char(string="Pantone")
    x_anilox7 = fields.Char(string="Anilox")

    x_tinta8 = fields.Many2one('product.product', string = "Tinta")
    x_pantone8 = fields.Char(string="Pantone")
    x_anilox8 = fields.Char(string="Anilox")

    x_observations = fields.Char(string = "Observaciones")

    @api.depends('x_client')
    def compute_display_name(self):
        for rec in self:
            if rec.x_client:
                rec.x_client_display = '[%s] %s' % (rec.x_client.internal_code, rec.x_client.name)
            else:
                rec.x_client_display = rec.x_client

    @api.depends('x_machine_id')
    def _compute_cylinder_ids(self):
        for rec in self:
            if rec.x_machine_id:
                rec.x_cylinder_ids = rec.x_machine_id.cylinder_ids
            else:
                rec.x_cylinder_ids = False


    @api.depends('x_ubicacion_taco')
    def _otro_taco(self):
        for rec in self:
            if rec.x_ubicacion_taco != "Otros":
                rec.x_ubicacion_taco_otros = False
            else:
                rec.x_ubicacion_taco_otros = False


    @api.depends('x_material_imprimir_a')
    def _laminar_a(self):
        for rec in self:
            if rec.x_material_imprimir_a:
                rec.x_material_laminar_a = rec.x_material_imprimir_a.product_template_attribute_value_ids
            else:
                rec.x_material_laminar_a = False

    def action_ov_compute(self):
        for rec in self:
            ov = self.env["sale.order"].search([('state','!=','cancel'),("order_line.product_id.product_tmpl_id","=",rec.id),('order_line.product_uom_qty','>',0)], order='date_order desc', limit=1)
            line = ov.order_line.search([('product_template_id','=',rec.id)])
            date = timedelta(30)
            if ov:
                rec.x_ultima_ov = ov
                rec.x_orden_de_compra = ov.client_order_ref
                rec.x_date_of_delivery = ov.date_order + date
                rec.x_cantidad = '%s %s' % (line.product_uom_qty, line.product_uom.name)
            else:
                rec.x_ultima_ov = False
                rec.x_orden_de_compra = False
                rec.x_date_of_delivery = False

    def action_print_ficha(self):
        self.x_last_date = fields.Date.today()
        return self.env.ref('personalizations_flexocolor.action_ficha_tecnica').report_action(self)    

    @api.depends('x_ancho_banda','x_cantidad_bandas')
    def _ancho_compute(self):
        for rec in self:
            if rec.x_ancho_banda and rec.x_cantidad_bandas:
                rec.x_ancho_lamina = rec.x_ancho_banda * rec.x_cantidad_bandas
            else:
                rec.x_ancho_lamina = False
