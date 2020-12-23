##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models


class AcademicLevel(models.Model):

    _inherit = 'academic.level'
    _order = 'section_id asc, name asc'
