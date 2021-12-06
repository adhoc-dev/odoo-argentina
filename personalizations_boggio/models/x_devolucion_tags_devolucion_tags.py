from odoo import models, fields


class XDevolucionTagsDevolucionTags(models.Model):
    _name = 'x_devolucion_tags.devolucion_tags'
    _description = 'x_devolucion_tags'

    x_name = fields.Char(string="Name", required=True)

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.x_name))
        return result
