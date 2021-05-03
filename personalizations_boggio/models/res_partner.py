from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    x_operate_with_checks = fields.Boolean(string="Opera con Cheques", help="Si el campo esta activo quiere decir que el cliente puede operar con cheques en los recibos", copy=False)
    x_credit_nosis_score = fields.Integer(string="Score de Nosis (objetivo >400)")
    x_no_recibe_remito = fields.Boolean(string="No Recibe remitos automaticamente", help="Si esta campo esta tildado el contacto no recibirá remitos y sus pendientes en forma automática")
    x_lista_proveedor = fields.Char(string="Lista de precio de proveedor", help="Se carga fecha de ultima actualizacion y nombre de lista", copy=False)
    x_desc_pago_prov = fields.Char(string="Descuento Pago Proveedor", help="Descuento al hacer el pago al proveedor. (descuento de contado)", copy=False)
    x_deuda_email = fields.Boolean(string="No envia cuenta corriente por email automaticamente", help="Si esta tildado no envia deuda por email automaticamente")
    x_detalle_deuda_facturas = fields.Integer(string="Detalle de deuda en facturas", help="0 - no envia nada"
"1 - envia saldo deuda"
"2 - envia detalle de deuda"
"3 - envia detalle de deuda+saldo")
    x_order_cycle = fields.Integer(string="Dias entre compras", copy=False)
    x_global_supply = fields.Boolean(string="Compra Global", help="Si el campo esta tildado la compra de este proveedor se hace en forma central de la casa central. Si no esta marcado se compra en forma distribuida en las sucursales.", copy=False)
    x_abc_sales_freq = fields.Char(string="ABC Cliente Frecuencia  (0,1,2,3)", help="0 → 0-70% de los ventas (+1 compra por mes)"
"1→ 70-90% de los ventas (de una compra por mes a 1 compra por semestre)"
"2 resto (valor por defecto) (una compra por semestre)"
"3 no tuvieron ventas en el  último tiempo", copy=False)
    x_metodo_envio_compras = fields.Many2one(string="Método de envío Santa Fe", comodel_name="delivery.carrier", on_delete="set null")
    x_metodo_envio_rafaela = fields.Many2one(string="Metodo de envio Rafaela", comodel_name="delivery.carrier", on_delete="set null")
