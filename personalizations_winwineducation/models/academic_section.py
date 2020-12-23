##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models


class AcademicSection(models.Model):

    _inherit = 'academic.section'
    _order = 'name'
