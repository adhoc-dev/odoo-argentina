##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
import base64
from odoo import _, api, fields, models
from odoo.exceptions import UserError

# TODO improve. este modelo es una copia exacta del de de account_tax_settlement.
# Ver de mover esta a un modulo generico aparte y que de alli dependa los dos
# modulos para no repetir codigo


class DownloadFilesWizard(models.TransientModel):
    _name = 'p13n_download_files_wizard'
    _description = 'Wizard genérico para descargar archivos'

    line_ids = fields.One2many(
        'p13n_download_files_wizard_line',
        'wizard_id',
        'Files',
        readonly=True,
    )

    student_ids = fields.Many2many('res.partner', string='Estudiantes', readonly=True)
    company_id = fields.Many2one('res.company', readonly=True)

    @api.model
    def action_get_files(self, files_values, students, company):
        # transformamos a binary y agregamos formato para campos o2m

        wizard = self.env['p13n_download_files_wizard'].create({
            'line_ids': [(0, False, {
                'txt_filename': x['txt_filename'],
                'txt_binary': base64.encodestring(
                    x['txt_content'].encode('ascii')),
            }) for x in files_values if x['txt_content']],
            'student_ids': [(6, 0, students.ids)],
            'company_id': company.id,
        })

        return {
            'type': 'ir.actions.act_window',
            'res_id': wizard.id,
            'res_model': wizard._name,
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
        }

    def action_update_volumen(self):
        company = self.company_id
        company.red_link_volumen += 1
        if company.red_link_volumen > 9:
            raise UserError(_('Solo puede informar hasta 9 volumenes por dia'))
        for student in self.with_context(company_id=company.id).student_ids:
            student.red_link_id_deuda += 1

        return {'type': 'ir.actions.act_window_close'}


class DownloadFileWizardLine(models.TransientModel):
    _name = 'p13n_download_files_wizard_line'
    _description = 'Wizard genérico para descargar archivos'

    wizard_id = fields.Many2one(
        'p13n_download_files_wizard',
    )
    txt_filename = fields.Char(
    )
    txt_binary = fields.Binary(
    )
