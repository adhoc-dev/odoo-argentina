from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    cant_madres = fields.Integer(string='Cantidad de Madres')
    genetica = fields.Char(string='Genética')
    linea_inseminacion = fields.Char(string='Línea Inseminación')
    prov_inseminacion = fields.Char(string='Proveedor Inseminación')
    compra_semen = fields.Boolean(string='Compra Semen')
    prov_dosis_semen = fields.Char(string='Proveedor de Dosis de Semen')
    linea_vacunas = fields.Char(string='Línea de Vacunas')
    prov_vacunas = fields.Char(string='Proovedor de Vacunas')
