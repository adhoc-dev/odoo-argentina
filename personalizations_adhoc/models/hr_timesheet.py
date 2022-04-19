# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, _
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    @api.constrains('task_id', 'project_id')
    def _check_task_project(self):
        for line in self:
            # matenemos constraint similar a la de odoo pero permitimos también proyectos y tareas de misma entidad
            # comercial
            if line.task_id and line.project_id and line.task_id.project_id != line.project_id and \
               line.task_id.project_id.partner_id.commercial_partner_id != \
               line.helpdesk_ticket_id.project_id.partner_id.commercial_partner_id:
                raise ValidationError(
                    "EL proyecto y la tarea son inconsistentes. "
                    "La tarea seleccionada debe pertenecer al proyecto seleccionado o las entidades comerciales de "
                    "la tarea y el proyecto deben ser las mismas. ID Tarea %s, ID Proyecto %s" % (
                        line.task_id.id, line.project_id.id))
