from datetime import datetime
import re
import base64
from odoo import models, fields
from odoo.exceptions import UserError


class AccountBatchPayment(models.Model):
    _inherit = 'account.batch.payment'

    def get_partner_identification(self, payment):
        invoice = payment.invoice_ids[0]
        return invoice.student_id.student_code or ''

    def _pago_mis_cuentas_content(self):
        #Recargos
        first_due_date_days = self.journal_id.company_id.first_due_date_days
        second_due_date_days = self.journal_id.company_id.second_due_date_days
        second_due_surcharge = self.journal_id.company_id.surcharge
        # Las fecha de proceso a informar es la del dia de la generación del archivo.
        filename = self.journal_id.company_id.vat + '.' + datetime.now().strftime('%Y%m%d')
        content = ''
        # CABECERA

        # código de registro, código banelco, código empresa
        content += '04000000'

        # fecha de archivo
        content += datetime.now().strftime('%Y%m%d')

        # filler
        content += '0'*264
        content += '\r\n'

        # DETALLE
        debt_total = 0
        for rec in self.payment_ids:
            # código registro
            content += '5'

            # nro de referencia o código de pago electrónico (es único por cada pago informado)
            if len(rec.invoice_ids)>1 and len(set(rec.invoice_ids.mapped('student_id.student_code'))>1):
                raise UserError(_('El pago tiene asociada más de una factura y cada una de ellas refiere a diferentes estudiantes o alguna de ellas no tiene student_code asociado "%s"' % rec.display_name))
            if not rec.invoice_ids[-1].student_id:
                raise UserError(_('No se pudo generar el archivo ya que la factura "%s" no tiene estudiante asociado' % rec.invoice_ids[-1].name))
            if not rec.invoice_ids[-1].student_id.student_code:
                raise UserError(_('No se pudo generar el archivo ya que el estudiante "%s" no tiene codigo de estudiante' % rec.invoice_ids[-1].student_id.name))
            if not rec.invoice_ids[-1].partner_id.child_ids:
                raise UserError(_('La familia "%s" no tiene alumnos a cargo' % rec.partner_id.name))
            if rec.invoice_ids[-1].partner_id != rec.invoice_ids[-1].commercial_partner_id:
                raise UserError(_('Por favor verificar si la factura "%s" se hizo a nombre de una familia y no de un alumno' % rec.invoice_ids[-1].name))

            nro_referencia = rec.invoice_ids[-1].student_id.student_code.ljust(19)[:19]
            content += nro_referencia

            # id factura VER
            content += rec.invoice_ids[-1].l10n_latam_document_number.ljust(20)[:20]

            # código moneda
            content += '0'

            # fecha 1er vencimiento
            content += fields.Date.add(rec.invoice_ids[-1].invoice_date, days=first_due_date_days).strftime('%Y%m%d')

            # importe 1er vencimiento
            debt_payment_amount = round(rec.amount,2)
            content += '%011d' % int(re.sub('[^0-9]', '', "%.2f" % debt_payment_amount))

            # fecha 2do vencimiento
            second_due_date = fields.Date.add(rec.invoice_ids[-1].invoice_date, days=second_due_date_days).strftime('%Y%m%d')
            content += second_due_date

            # importe 2do vencimiento
            second_expiration_amount = round((debt_payment_amount * (1 + second_due_surcharge / 100.0)),2)
            second_expiration_amount_formatted = '%011d' % int(re.sub('[^0-9]', '', "%.2f" % second_expiration_amount))
            content += second_expiration_amount_formatted

            # fecha e importe 3er vencimiento(repito fecha e importe 2do vencimiento)
            content += second_due_date
            content += second_expiration_amount_formatted

            # filler1
            content += '0'*19

            # nro referencia ant VER
            content += nro_referencia

            # mensaje ticket y mensaje pantalla
            content += ' '*55

            # codigo de barras VER
            content += ' '*60

            # filler2
            content += '0'*29
            content += '\r\n'

        # PIE

        # código de registro, código banelco, código empresa
        content += '94000000'

        # fecha de archivo
        content += datetime.now().strftime('%Y%m%d')

        # cantidad de registros
        content += '%07d' % len(self.payment_ids)

        # filler1
        content += '0'*7

        # total importe
        content += '%011d' % int(re.sub('[^0-9]', '', str(self.amount)))

        # filler2
        content += '0'*239
        content += '\r\n'

        return filename, content

    def _generate_export_file(self):
        if self.direct_debit_format == 'pago_mis_cuentas':
            content = self._pago_mis_cuentas_content()
        else:
            super()._generate_export_file()
        return {
            'file': base64.encodebytes(content[1].encode('UTF-8')),
            'filename': content[0] + ".txt",
        }
