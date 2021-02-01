from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    x_department = fields.Char(string="Partido / Departamento / Centro")
    x_barrio = fields.Char(string="Barrio")
    x_zona = fields.Char(string="Zona")
    x_studio_field_qcof1 = fields.Char(string="Email personal", copy=False)
    x_studio_field_l5Gzo = fields.Date(string="Fecha de nacimiento", copy=False)
    # agregamos espacio para evitar warning por label duplicado con otro
    # modulo en este repo hasta que encontremos mejor solucion
    x_studio_field_j5Qb2 = fields.Integer(string="Edad ", copy=False)
    x_studio_field_t95ga = fields.Boolean(string="Titular OS / Prepaga", copy=False)
