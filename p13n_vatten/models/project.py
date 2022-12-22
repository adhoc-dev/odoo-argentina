from odoo import models, fields, api


class ProjectTask(models.Model):
    _inherit = 'project.task'


    partner_email = fields.Char(related='partner_id.email', string="Email", readonly=True)
    determinacion_ids = fields.One2many(comodel_name='fsm_determinaciones', inverse_name='order_id',
                                        tracking=True, readonly=False)
    instrucciones = fields.Html(string='Instrucciones', readonly=False)
    adjuntos = fields.Many2many('ir.attachment', string="Adjuntos", readonly=False)

    @api.onchange('determinacion_ids')
    def _onchange_determinacion_ids(self):
        alcalinidades = {}
        for det in self.determinacion_ids:
            det.parametro_name = "".join(det.parametro_name.split())
            if det.muestra_name not in alcalinidades.keys():
                alcalinidades[det.muestra_name] = {}
            if det.parametro_name == "AlcF" and det.valor:
                alcalinidades[det.muestra_name][det.parametro_name] = det.valor
            if det.parametro_name == 'AlcM' and det.valor:
                alcalinidades[det.muestra_name][det.parametro_name] = det.valor
            if det.parametro_name == 'AlcOH' and det.valor:
                alcalinidades[det.muestra_name][det.parametro_name] = det
        for key in alcalinidades.keys():
            if len((alcalinidades[key].keys())) == 3:
                AlcF = int(alcalinidades[key]['AlcF'])
                AlcM = int(alcalinidades[key]['AlcM'])
                AlcOH = 2 * AlcF - AlcM
                if AlcOH < 0:
                    AlcOH = 0
                alcalinidades[key]['AlcOH'].valor = str(AlcOH)

    @api.onchange('partner_id')
    def _onchange_partner_id(self):

        if(not self.partner_id):
            return {}

        # borra los registros que haya
        self.update({'determinacion_ids':[(2,individual.id) for individual in self.determinacion_ids]})

        # crea nuevos registros
        r=[]
        for muestra in self.env['muestras'].search([('partner_service_id.id', '=', self.partner_id.id)]).sorted(key=lambda r: r.sequence):
            for parametro in muestra.parametro_ids.sorted(key=lambda r: r.sequence):
                r.append((0, 0, {
                    'muestra_name': muestra.name.replace(' ','\N{NO-BREAK SPACE}'),
                    'parametro_name': parametro.name.name.replace(' ','\N{NO-BREAK SPACE}'),
                    'unit_name': parametro.unit.replace(' ','\N{NO-BREAK SPACE}'),
                    'parametro_display': parametro.name.name.replace(' ','\N{NO-BREAK SPACE}') + '\n' + parametro.name.unit.replace(' ','\N{NO-BREAK SPACE}'),
                    'valor': '',
                    'min_value': parametro.min_value,
                    'max_value': parametro.max_value,
                    'in_report': parametro.in_report,
                    'in_chart': parametro.in_chart,
                    }))
        self.update({'determinacion_ids': r })