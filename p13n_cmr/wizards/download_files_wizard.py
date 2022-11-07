import base64
from odoo import _, api, fields, models
from datetime import datetime

# TODO improve. este modelo es una copia exacta del de de account_tax_settlement.
# Ver de mover esta a un modulo generico aparte y que de alli dependa los dos
# modulos para no repetir codigo. Una lógica similar la tienen en personalizations_jureclaplata


class DownloadFilesWizard(models.TransientModel):
    _name = 'p13n_download_files_wizard'
    _description = 'Wizard genérico para descargar archivos'

    line_ids = fields.One2many(
        'p13n_download_files_wizard_line',
        'wizard_id',
        'Files',
        readonly=True,
    )

    @api.model
    def action_get_files(self, content_txt, content_csv):
        # transformamos a binary y agregamos formato para campos o2m
        fecha_generacion_archivo = datetime.now().strftime('%Y/%m/%d')
        wizard = self.env['p13n_download_files_wizard'].create({
            'line_ids': [(0, False, {
                'txt_filename': 'Transferencias inmediatas banco Municipal'  + "-" +  fecha_generacion_archivo,
                'txt_binary': base64.encodestring(
                    content_txt.encode('cp1252')),
            }),
            (0, False, {
                'txt_filename': 'Archivo con datos de transferencias inmediatas (para control)'  + "-" + fecha_generacion_archivo + '.csv' ,
                'txt_binary': base64.encodestring(
                    content_csv.encode('ascii')),
            })],
        })

        return {
            'type': 'ir.actions.act_window',
            'res_id': wizard.id,
            'res_model': wizard._name,
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
        }


class DownloadFileWizardLine(models.TransientModel):
    _name = 'p13n_download_files_wizard_line'
    _description = 'Wizard genérico para descargar archivos'

    wizard_id = fields.Many2one(
        'p13n_download_files_wizard',
    )
    txt_binary = fields.Binary(
    )
    txt_filename = fields.Char(
    )
