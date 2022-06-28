from odoo import models, fields


class XResPartnerEmergencyContact(models.Model):
    _name = 'x_res.partner.emergency.contact'
    _description = 'Contacto de emergencia'
    _rec_name = 'x_name'

    x_name = fields.Char(string="Name", copy=False)
    x_type = fields.Selection(string="Tipo", selection=[('a','Autorización'),('r','Restricción'),('ce','Contacto de Emergencia'),('ie','Institución de Emergencia')])
    x_contact_name = fields.Char(string="Nombre")
    x_contact_dni = fields.Char(string="DNI")
    x_observations = fields.Char(string="Observaciones")
    x_res_partner_id = fields.Many2one(string="Partner", comodel_name="res.partner", on_delete="set null")
