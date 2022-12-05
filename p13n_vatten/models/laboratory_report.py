# -*- coding: utf-8 -*-
from odoo import models, api
import logging

_logger = logging.getLogger(__name__)


class LaboratoryReport(models.AbstractModel):
    _name = 'report.laboratory.reporte_protocolo'
    _description = 'Imprime informe de orden de servicio'

    @api.model
    def _get_report_values(self, docids, data=None):
        reporte = self.env['ir.actions.report']._get_report_from_name('laboratory.reporte_protocolo')
        docs = self.env[reporte.model].browse(docids)

        docargs = {
            'doc_ids': docids,
            'doc_model': reporte.model,
            'docs': docs,
        }
        return docargs
