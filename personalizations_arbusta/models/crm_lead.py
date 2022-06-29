from odoo import models, fields


class CrmLead(models.Model):
    _inherit = 'crm.lead'


    x_studio_field_1IT3n = fields.Selection(string="TribuX",
                                            selection=[('Data Services', 'Data Services'),
                                                       ('Development', 'Development'),
                                                       ('Customer Experience',
                                                        'Customer Experience'),                                                       ('Machine Learning Training', 'Machine Learning Training'),
                                                       ('QA & Testing', 'QA & Testing')], copy=False)
    x_studio_field_hkOoC = fields.Date(string="Inicio estimado", copy=False)
    x_studio_field_KPykh = fields.Integer(string="Horas mensuales", copy=False)
    x_studio_field_eegYH = fields.Float(string="Rate mensual", copy=False)
    x_studio_field_9ZMsr = fields.Selection(string="Origen",
                                            selection=[('Farming Cross-Selling', 'Farming Cross-Selling'),
                                                       ('Farming Upselling', 'Farming Upselling'),
                                                       ('Hunting', 'Hunting'),('Hunting Networking', 'Hunting Networking'),
                                                       ('Hunting Linkedin', 'Hunting Linkedin'),
                                                       ('Hunting Agencia SQR', 'Hunting Agencia SQR'),
                                                       ('Hunting Evento', 'Hunting Evento'),
                                                       ('Hunting web','Hunting web')], copy=False)
    x_studio_field_8wDdo = fields.Selection(string="Idioma requerido",
                                            selection=[('N/A', 'N/A'), ('Inglés oral', 'Inglés oral'),
                                                       ('Inglés escrito', 'Inglés escrito'),
                                                       ('Inglés oral + escrito', 'Inglés oral + escrito'),
                                                       ('Portugués oral', 'Portugués oral'),
                                                       ('Portugués escrito', 'Portugués escrito'),
                                                       ('Portugués oral + escrito', 'Portugués oral + escrito')],
                                            copy=False)
    x_studio_field_4OBuE = fields.Selection(string="Oficina OPS",
                                            selection=[('Buenos Aires', 'Buenos Aires'),
                                                       ('Medellín', 'Medellín'), ('Montevideo', 'Montevideo'),
                                                       ('Rosario', 'Rosario'), ('Indistinto', 'Indistinto')],
                                            copy=False)
    x_studio_field_dtLz9 = fields.Float(string="Plazo (meses)", copy=False)
    x_studio_field_lj29Z = fields.Char(string="Link Calculadora", copy=False)
    x_studio_field_Wq8M7 = fields.Char(string="Link Propuesta", copy=False)
    x_studio_field_jyLyQ = fields.Boolean(string="Check Capacity", tracking=100, copy=False)
    x_project_currency = fields.Many2one(comodel_name='res.currency', string='Project Currency')
    x_studio_field_QI5H4 = fields.Selection(string="Industria",
                                        selection=[('Aeronáutica', 'Aeronáutica'),
                                                    ('Agrobusiness', 'Agrobusiness'), ('Banca', 'Banca'),
                                                    ('Beauty', 'Beauty'), ('Cryptomonedas', 'Cryptomonedas'),
                                                    ('E-commerce & marketplace', 'E-commerce & marketplace'),
                                                    ('Educación', 'Educación'),
                                                    ('Electrónica', 'Electrónica'),
                                                    ('Entretenimiento', 'Entretenimiento'),
                                                    ('Fintech', 'Fintech'), ('Gobierno', 'Gobierno'),
                                                    ('Marketplace', 'Marketplace'), ('Oil & Gas', 'Oil & Gas'),
                                                    ('ONG', 'ONG'), ('Otra', 'Otra'), ('Paperless', 'Paperless'),
                                                    ('Recursos Humanos', 'Recursos Humanos'), ('Salud', 'Salud'),
                                                    ('Seguros', 'Seguros'), ('Tecnología', 'Tecnología'),
                                                    ('N/A', 'N/A')], copy=False)
    tribu = fields.Many2one("account.analytic.group", string="Tribu")
