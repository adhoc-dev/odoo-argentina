from odoo import models, fields


class DocumentPage(models.Model):
    _inherit = 'document.page'

    x_studio_field_EBTl8 = fields.Many2many(string="Área", comodel_name="project.tags", relation="x_document_page_project_tags_rel", column1="document_page_id", column2="project_tags_id", copy=False)
