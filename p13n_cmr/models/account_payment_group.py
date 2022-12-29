from odoo import models
from odoo.exceptions import UserError
import logging
import re
_logger = logging.getLogger(__name__)
import stdnum

class AccountPaymentGroup(models.Model):

    _inherit = "account.payment.group"

    def validate_cbu(self, number):
        """Método para verificar que el cbu sea válido"""
        def _check_digit(number):
            """Calculate the check digit."""
            weights = (3, 1, 7, 9)
            check = sum(int(n) * weights[i % 4] for i, n in enumerate(reversed(number)))
            return str((10 - check) % 10)
        number = stdnum.util.clean(number, ' -').strip()
        if len(number) != 22 or not number.isdigit() or _check_digit(number[:7]) != number[7] or _check_digit(number[8:-1]) != number[-1]:
            if number == self.company_id.cbu_company:
                raise UserError(f'La compañía tiene CBU Inválido - {number}')
            else:
                raise UserError(f'El partner tiene CBU Inválido - {number}')
        return number

    def _generate_export_file(self):
        """Método que sirve para computar los campos que se van a tener en cuenta para la generación del archivo de transferencias inmediatas para banco Municipal"""

        active_ids = self.env.context.get('active_ids')
        payments = self.browse(active_ids) if active_ids else self

        # validación para que genere la op
        if not payments:
            raise UserError('Por favor seleccione los pagos que quiere incluir')

        # validación de estado de las op
        not_valid_payments = payments.filtered(lambda x: x.state not in ['signed', 'posted'])

        if not_valid_payments:
            mensaje = f'No puede generarse el archivo para OP que no se encuentren en estado de Firmado o Pagado. Dichas órdenes de pago son: {str(not_valid_payments.mapped("name"))}'
            raise UserError(mensaje)
        _logger.info("Generando archivos de transferencia de débito automático")


        limite_diario_transferencias_bco_municipal = float(self.env['ir.config_parameter'].sudo().get_param(
            'p13n_cmr.limite_diario_transferencias_bco_municipal',
        ))
        # se completa el archivo con la información de cada uno de los pagos
        content_txt = ''
        content_csv = ''
        total_payment_amount = 0
        banco_municipal = self.env['account.journal'].browse(13).name

        for pay in payments:
            # cbu débito
            if not pay.company_id.cbu_company:
                raise UserError(f'La compañía no tiene cbu ingresado')
            cbu_company = pay.validate_cbu(pay.company_id.cbu_company)
            content_txt += cbu_company
            content_csv += cbu_company + ','

            # cbu crédito
            if not pay.partner_id.bank_ids.filtered(lambda x: x.acc_type == 'cbu'):
                raise UserError(f'El partner {pay.partner_id.name} no tiene cbu registrado, por lo tanto no se puede incluir el pago correspondiente en el archivo de transferencias masivas')
            cbu_partner = pay.partner_id.bank_ids.filtered(lambda x: x.acc_type == 'cbu')[-1].acc_number
            if cbu_company == cbu_partner:
                # el cbu del emisor es el mismo que el cbu del receptor
                raise UserError(f'El partner no puede tener el mismo cbu que la compañía')
            content_txt += cbu_partner
            content_csv += cbu_partner + ','

            # alias cbu débito + alias cbu crédito
            content_txt += ' '*44

            # importe
            to_transfer_amount = 0
            municipal_payment_lines = pay.payment_ids.filtered(lambda x: x.journal_id.id == 13)
            if not municipal_payment_lines:
                raise UserError(f'No existe línea de pago perteneciente al banco "{banco_municipal}", (diario con id 13) para la orden de pago {pay.name} con id {pay.id}')
            for line in municipal_payment_lines:
                to_transfer_amount += line.amount
            payment_amount = round(to_transfer_amount,2)
            total_payment_amount += payment_amount
            content_txt += ('%013.2f' % to_transfer_amount).replace('.','')
            content_csv += str(payment_amount) + ','

            # concepto
            concepto = re.sub('[^A-Za-z0-9 ]', '', pay.communication)[:50].ljust(50)if pay.communication else ' '*50
            content_txt += concepto
            content_csv += (concepto + ',')

            # motivo
            content_txt += 'VAR'
            content_csv += 'VAR' + ','

            # referencia
            referencia = re.sub('[^A-Za-z0-9 ]', '', pay.partner_id.name)[:12].ljust(12)
            content_txt += referencia
            content_csv += referencia

            # email + titulares
            content_txt += ' '*51

            content_txt += '\r\n'
            content_csv += '\n'

        # pie del archivo
        # cantidad de registros
        content_txt += '%05d' % (len(payments) + 1)

        # total importes
        content_txt += ('%018.2f' % total_payment_amount).replace('.','')

        if total_payment_amount > limite_diario_transferencias_bco_municipal:
            raise UserError(f'Se ha excedido el limite para realizar transferencias inmediatas diarias, el mismo de es  ${limite_diario_transferencias_bco_municipal}\nSi dicho importe corresponde actualizarlo entonces debe hacerlo en "Ajustes / Técnico / Parámetros / Parámetros del Sistema" y ajustar el valor del parámetro "p13n_cmr.limite_diario_transferencias_bco_municipal"')

        # relleno
        content_txt += ' '*194

        # salto de línea
        content_txt += '\r\n'

        return self.env['p13n_download_files_wizard'].action_get_files(content_txt, content_csv)

