from odoo import _, models, fields, api
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    student_id = fields.Many2one('res.partner', string='Alumno', domain="[('parent_id', '=', partner_id), ('partner_type', '=', 'student')]")

    @api.constrains('student_id')
    def _check_student(self):
        invoices_wo_student = self.filtered(lambda x: x.type in ["out_invoice", "out_refund"] and not x.student_id)
        if invoices_wo_student:
            msg = _("Las facturas de clientes y notas de debito debe tener asociado siempre un alumno")
            if len(invoices_wo_student) > 1:
                msg += ".\n" + _("Los siguientes documentos no cumplen esa condición:") + "\n\n - %s" % '\n - '.join(invoices_wo_student.mapped('display_name'))
            raise ValidationError(msg)

    def get_student_debt_total(self):
        debt_total = self.search([
            ('student_id.student_code', '=', self.student_id.student_code),
            ('type', '=', 'out_invoice'), ('state', '=', 'posted'),
            ('invoice_payment_state', '=', 'not_paid')
        ])
        return debt_total

    def get_debt_first_due(self, debt_total):
        """ calcula la deuda total, en este caso seria lo que queda pendiente por pagar de todas las facturas antes
        del primer vencimiento. Las deudas que vienen de meses anteriores vienen includias por las facturas de intereses
        (notas de debito auto generadas mes a mes) """
        self.ensure_one()
        return sum(debt_total.mapped('amount_residual'))

    def get_debt_second_due(self, debt_total):
        """ devuelve directamente la suma del monto audado de todas las facturas que no han sido pagadas, solo suma
        el recargo a aquellas facturas cuyo mes sea el actual o futuros (alli las nd aun no existen)"""
        self.ensure_one()
        debt_first_due = self.get_debt_first_due(debt_total)
        subcharge = 0.0
        for invoice in debt_total.filtered(lambda x: x.invoice_date.month >= fields.Date.context_today(self).month):
            subcharge += invoice.amount_residual * (invoice.company_id.surcharge / 100.0)
        return debt_first_due + subcharge

    def get_files_red_link(self):
        """ Este método recibe una lista de varios account move y devuelve el wizard que permite pre visualizar los archivos a descargar """

        active_ids = self.env.context.get('active_ids')
        invoices = self.browse(active_ids) if active_ids else self

        if not invoices:
            raise UserError(_('Por favor seleccione las facturas que quiere incluir'))

        not_valid_invoices = invoices.filtered(lambda x: x.state != 'posted')
        if not_valid_invoices:
            raise UserError(_(
                'Solo puede generar los archivos de facturas que esten publicadas. Las siguientes que fueron seleccionadas '
                ' estan en otros estados: %s') % not_valid_invoices.mapped('display_name'))
        _logger.info("Generando archivos para red link")

        invoices.verify_data_for_red_link_files()
        filename1, content1, other_info = invoices.get_files_red_link_file1()
        filename3, content3 = invoices.get_files_red_link_file3(other_info)

        values = [
            {'txt_filename': filename1, 'txt_content': content1},
            {'txt_filename': filename3, 'txt_content': content3},
        ]

        return self.env['p13n_download_files_wizard'].action_get_files(values, invoices.mapped('student_id'), invoices.mapped('company_id'))

    def _month_mapping(self, month):
        return month if month < 10 else {10: 'A', 11: 'B', 12: 'C'}.get(month)

    def _get_id_volumen(self):
        return str(self.company_id.red_link_volumen)

    def _get_id_user(self):
        """ Este es el que usamos para informar el usuario asociado a la euda de red link. este seria el codigo de
        estudiante pero de 7 digitos de longitud el codigo de estudiante tiene maximo 5 asi que estamos completando con
        ceros a la izquiera. Este campo se usa en los archivos de refresh pero tambien en el archivo de extract que se
        recibe tras procesado el pago por red link. Campo: Identificador de Usuario (19, N. completado a la derecha con
        espacios en blanco) """
        self.ensure_one()
        if not self.student_id:
            raise UserError(_('No se pudo generar el archivo ya que la factura "%s" no tiene estudiante asociado' % self.display_name))
        if not self.student_id.student_code:
            raise UserError(_('No se pudo generar el archivo ya que el estudiante "%s" no tiene codigo de estudiante' % self.student_id.display_name))
        return str(self.student_id.student_code.zfill(7)).ljust(19)

    def _get_id_concept(self):
        """ Metodo para obtener el Campo: Identificador de concepto (3, N, Alineado izquierda co ceros). Que es usado en el archivo refresh.
        Por los momentos siempre es 001. que sinifica que el concepto es "CUOTA. Este sera 001 = CUOTA siempre y cuando la empesa no
        define conceptos del lado de red link.

        NOTA: En caso de tener varios conceptos en futuro evaluar de:
        1. almacenar en odoo o en python la lista de conceptos y sus codigos.
        2. en la factura almancenar en un campo (ref?) dicho codigo para que podamos identificarlo """
        return "001"

    def _get_id_deuda(self, student):
        """ Para obtener el campo usado en archivo refresh de red link
        Campo: Identificador de deuda (5, N). Numero acordado entre el ente y Red Link.
        Ejemplo para el mes de Noviembre si hay varias deudas 01119, 11119, 21119 y así sucesivamente. """
        self.ensure_one()
        return "%s%02d%s" % (student.red_link_id_deuda, self.date.month, self.date.strftime('%y'))

    def verify_data_for_red_link_files(self):

        # 1. todas las facturas deben pertencer al mismo mes porque si no no deberiamos imprimir el archivo.
        months = set([item.month for item in self.mapped('invoice_date')])
        if len(months) > 1:
            raise UserError(_('Solo puede generar un archivo relacionado a un mismo mes. Ha seleccionado facturas de varios meses %s') % months)

        # 2. todas las facturas deberían pertenecer a la misma compañia
        companies = self.mapped('company_id')
        if len(companies) > 1:
            raise UserError(_('Solo puede generar archivos con facturas de una compañia por vez, tiene seleccionado registros de %s') % companies.mapped('name'))

        # 3. Si el codigo ente esta vacio no se va a poder continuar
        codigo_ente = self[0].company_id.red_link_code
        if not codigo_ente:
            raise UserError(_('No existe un Código Red Link para esta compañia %s, por favor definalo para poder continuar en Ajustes > Contabilidad en la sección Bancos') % companies.name)

    def get_files_red_link_file1(self):
        """ ARCHIVO 1: Archivo Refresh - (DISENO ESTANDARD)
        Se trata del archivo  entes quieren que puedan ser abonadas mediante el servicio de PAGAR.

        Un mismo archivo puede contener varios lotes.
        Cada lote debe tener un registro inicial (HEADER), el registro de datos y un registro final (TRAILER).

        NOTA: NO estamos informando lote spor los momentos, no le vimos utilizada. solo estamos tomando en cuenta los volumenes """
        # Las fecha de proceso a informar es la del dia de la generación del archivo.
        today = fields.Date.context_today(self)
        month = today.month
        day = today.day

        # Datos extraidos de la compañia
        codigo_ente = self[0].company_id.red_link_code
        first_due_date_days = self[0].company_id.first_due_date_days
        second_due_date_days = self[0].company_id.second_due_date_days
        fecha_ultimo_venc = self[0].invoice_date

        # ----------------------------------------------------------------------
        # filename:
        # El nombre de archivo debe respetar la siguiente nomenclatura:  PEEEVMDD. Ejemplo PDKG2303
        # P:	Fijo
        # EEE: 	Código del ente
        # V: 	Identificación numérica consecutiva de volumen
        # M: 	Identificación del mes al que corresponde la información (a partir del mes 10 se usan letras desde la A)
        # DD.: 	Identificación del día al que corresponde la información.
        numero_volumen = self._get_id_volumen()
        month_map = self._month_mapping(month)
        filename = 'P%s%s%s%02d' % (codigo_ente, numero_volumen, month_map, day)

        # ----------------------------------------------------------------------
        # Header: Registro Inicial. Ejemplo HRFACTURACIONDKG22030300001

        # Campo 1: Identificación del registro (13) Valor Fijo
        content = 'HRFACTURACION'

        # Campo 2: Código de Ente (3, AN). Ejemplo: DKG
        content += codigo_ente

        # Campo 3: Fecha de Proceso (6, N AAMMDD). Ejemplo: 220303
        content += today.strftime('%y%m%d')
        # NOTA: si en un futuro decidimos manejar esto en un wizard a parte seria la fecha indicada en ese wizard en lugar de la fecha de hoy

        # Campo 4: Lote (5, N). Ejemplo: 00001
        content += '00001'
        # NOTA: por los momentos solo un lote

        # Campo 5: Filler (104). Espacios con espacias
        content += ' ' * 104
        content += '\r\n'

        total_primer_venc = total_segundo_venc = total_tercer_venc = 0.0

        # ----------------------------------------------------------------------
        # Lineas de datos
        # Registro de datos: Ejemplo: 221550010001563            22031000000053755122032100000053755122032100000053755100000000000000000000000000000000000000000002022155

        # Reportar una linea por cada cliente, pueden ser varias lineas si son diferentes deudas para un mismo mes
        for student in self.mapped('student_id'):

            for num, inv in enumerate(self.filtered(lambda x: x.student_id == student)):

                # Campo 1: Identificador de deuda (5, N). Numero acordado entre el ente y Red Link.
                content += inv._get_id_deuda(student)

                # Campo 2: Identificador de concepto (3, N, Alineado izquierda co ceros).
                content += inv._get_id_concept()

                # Campo 3: Identificador de Usuario (19, N. completado a la derecha con espacios en bllaconco)
                content += inv._get_id_user()

                # Campo 4: Fecha Primer Vencimiento (6, N) AAMMDD.
                content += fields.Date.add(inv.invoice_date, days=first_due_date_days).strftime('%y%m%d')

                # Campo 5: Importe Primer Vencimiento (10 + 2, N. Completar con 0 a la izq)
                debt_total = inv.get_student_debt_total()
                importe_primer_vencimiento = inv.get_debt_first_due(debt_total)
                importe_primer_vencimiento = round(importe_primer_vencimiento, 2)
                content += ('%.2f' % (importe_primer_vencimiento)).replace('.', '').zfill(12)
                total_primer_venc += importe_primer_vencimiento

                # Campo 6: Fecha Segundo Vencimiento (6, N)
                fecha_segundo_venc = fields.Date.add(inv.invoice_date, days=second_due_date_days)
                content += fecha_segundo_venc.strftime('%y%m%d')

                # Campo 7: Importe Segundo Vencimiento (10 + 2, N. Completar con 0 a la izq)
                importe_segundo_vencimiento = inv.get_debt_second_due(debt_total)
                importe_segundo_vencimiento = round(importe_segundo_vencimiento, 2)
                total_segundo_venc += importe_segundo_vencimiento
                content += ('%.2f' % (importe_segundo_vencimiento)).replace('.', '').zfill(12)

                # Ellos en particular no utilizan tercer vencimiento asi que hay que mandar los siguientes dos campos
                # en vacío

                # Campo 8: Fecha Tercer Vencimiento (6, N).  N. Completar con 0 si no esta definido
                content += "000000"
                # content += fecha_segundo_venc.strftime('%y%m%d')

                # Campo 9: Importe Tercer Vencimiento (10 + 2), N. Completar con 0 a la izq)
                content += ''.zfill(12)
                # total_tercer_venc += importe_segundo_vencimiento
                # content += ('%.2f' % (importe_segundo_vencimiento)).replace('.', '').zfill(12)

                # Campo 10: Discrecional (50, AN)
                content += inv.name[:50].zfill(50) if inv.name else '0' * 50
                content += '\r\n'

                fecha_ultimo_venc = max(fecha_ultimo_venc, fecha_segundo_venc)

        # ----------------------------------------------------------------------
        # Registro Final
        # Ejemplo: TRFACTURACION00000753000000000482420269000000000482420269000000000482420269

        # Campo 1: Identificación del registro (13) Valor Fijo
        content += 'TRFACTURACION'

        # Campo 2: Cantidad de registros (8, N). Incluyendo inicial y final
        content += str(2 + len(self)).zfill(8)

        # Campo 3: Total primer vencimiento (16 + 2, N)
        content += ('%.2f' % total_primer_venc).replace('.', '').zfill(16 + 2)

        # Campo 4: Total segundo vencimiento (16 + 2, N)
        content += ('%.2f' % total_segundo_venc).replace('.', '').zfill(16 + 2)

        # Campo 5: Total tercer vencimiento (16 + 2, N)
        content += ('%.2f' % total_tercer_venc).replace('.', '').zfill(16 + 2)

        # Campo 6: Filler (104). Espacios con espacias
        content += ' ' * 56
        content += '\r\n'

        return filename, content, {
            'total_primer_venc': total_primer_venc,
            'total_segundo_venc': total_segundo_venc,
            'total_tercer_venc': total_tercer_venc,
            'len_file_1': len(content.strip().split('\r\n')),
            'fecha_ultimo_venc': fecha_ultimo_venc,
            'nombre_archivo_refresh': filename,
        }

    def get_files_red_link_file3(self, data):
        """ Archivo de control

        Para que los archivos REFRESH puedan ser procesados, deben venir acompañados de un Archivo Control cuya función
        es servir de Volante de Lote de la información que el ente remite.

        Es necesario que tanto el archivo Refresh como su correspondiente archivo control se transmitan juntos para que
        puedan ser incorporados automáticamente al proceso.
        """
        codigo_ente = self[0].company_id.red_link_code

        # Nombre del archivo
        # Debe identificarse con un nombre compuesto de 8 caracteres alfanuméricos, sin espacios intermedios y sin extensión,
        # Donde        # de acuerdo al siguiente detalle: CEEE1MDD

        # C: 	es un valor fijo,
        # 000:	es el código de ente a ser asignado por Red Link,
        # 1:	es el número de volumen (De “0” a “9” en el caso de que se envíe más de un archivo físico),
        # M:	es el número de mes, que va de “1” a “9” y de “A” a “C” (este ultimo rango reservado para los meses de octubre, noviembre y diciembre respectivamente),
        # DD:	es el número de día de “01” a “31” (si el numero de día es menor a 10, se agrega un cero a la izquierda, de modo de completar las 2 posiciones).

        # TODO KZ mejora ver de colocar esto en un metodo generico def _get_process_day(self):
        today = fields.Date.context_today(self)
        month = today.month
        day = today.day
        nro_volumen = self._get_id_volumen()
        filename = 'C' + codigo_ente + nro_volumen + str(self._month_mapping(month)) + ("%02d" %  day)

        # ----------------------------------------------------------------------
        # Header: Registro Inicial

        # Campo 1: Identificación de inicio (13) Valor Fijo
        content = 'HRPASCTRL'

        # Campo 2: Fecha (9, 8). Fecha de generación del archivo en formato AAAAMMDD
        content += today.strftime('%Y%m%d')
        # NOTA: si decidimos manejar esto en un wizard a parte seria la fecha  indicada en ese wizard en lugar de la fecha de hoy

        # Campo 3: Ente (X,3). Código asignado al ente por Red Link S.A.
        content += codigo_ente

        # Campo 4: Nombre Archivo (X, 8). Nombre del archivo refresh al que acompaña. (por ejemplo: P0141727)
        content += data['nombre_archivo_refresh']

        # Campo 5: Longitud del archivo 9(10)
        # Cantidad total de bytes de todos los lotes que conforman el archivo REFRESH. Este total se obtiene multiplicando la cantidad total de registros del archivo Refresh por la longitud del registro.
        # ( Por ejemplo si la longitud del registro es de 54 caracteres y el archivo contiene 1000 registros incluyendo los Header y Trailler, el total a colocar es 54000).
        content += str(data['len_file_1'] * 133).zfill(10)
        # NOTA Hacemos por 133 y no por 131 porque segun nos comento mesa de ayuda de link debemos hacer cantidad de caracteres + los saltos de linea y retorno de carros

        # Campo 6: Filler (x, 37). Espacios con espacias
        content += ' ' * 37
        content += '\r\n'

        # ----------------------------------------------------------------------
        # Lineas de datos. Registro de datos

        # Campo 1: 1 Identificación de datos (X, 5). Fijo LOTES
        content += "LOTES"

        # Campo 2: Número de lote (9, 5). Identificación numérica asignada al lote incluido dentro del archivo Refresh,
        # Por los momento solo reportamos un lote
        content += "00001"

        # Campo 3: Cantidad de registros del lote (9, 8).
        content += str(data['len_file_1']).zfill(8)

        # Campo 4: Importe primer vencimiento 9(16)V99. Suma de importes del campo primer vencimiento del lote. Completado con ceros a la izquierda.
        content += ('%.2f' % data['total_primer_venc']).replace('.', '').zfill(18)

        # Campo 5: 5 Importe segundo vencimiento 9(16)V99. Suma de importes del campo segundo vencimiento del lote. Completado con ceros a la izquierda.
        content += ('%.2f' % data['total_segundo_venc']).replace('.', '').zfill(18)

        # Campo 6: 6 Importe tercer vencimiento 9(16)V99. Suma de importes del campo tercer vencimiento del lote. Completado con ceros a la izquierda.
        content += ('%.2f' % data['total_tercer_venc']).replace('.', '').zfill(18)

        # Campo 7: Filler (4). Espacios en blanco
        content += ' ' * 3
        content += '\r\n'

        # ----------------------------------------------------------------------
        # TRAILER: Registro Final

        # Campo 1: 1 Identificación de fin. Valor Fijo: 'FINAL'
        content += 'FINAL'

        # Campo 2 Cantidad. total de Registros (9, 8). Cantidad total de registros de todos los lotes que integran el archivo REFRESH
        content += str(data['len_file_1']).zfill(8)

        # NOTA: En un futuro en caso de tener mas de un lote toca ajustar el campo 3, 4, 5

        # Campo 3 Importe total primer vencimiento (9, 16). Suma total de los importes correspondientes al primer vencimiento de todos los lotes que componen el archivo. Completado con ceros a la izquierda.
        content += ('%.2f' % data['total_primer_venc']).replace('.', '').zfill(18)

        # Campo 4 Importe total segundo vencimiento (9, 16).
        content += ('%.2f' % data['total_segundo_venc']).replace('.', '').zfill(18)

        # Campo 5 Importe total tercer vencimiento (9, 16).
        content += ('%.2f' % data['total_tercer_venc']).replace('.', '').zfill(18)

        # Campo 6: Fecha de último Vencimiento (X, 8) Fecha correspondiente al último vencimiento incorporado en el archivo a transmitir, en cualquiera de los lotes
        content += data['fecha_ultimo_venc'].strftime('%Y%m%d')
        content += '\r\n'

        return filename, content
