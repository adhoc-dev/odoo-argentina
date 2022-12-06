{
    'name': 'Laboratorio',
    'version': '15.0.1.0.0',
    'summary': 'Genera protocolos de control analítico de aguas',
    'category': 'Uncategorized',
    'author': 'RMF',
    'maintainer': 'RMF',
    'website': '',
    'license': 'AGPL-3',
    'depends': [
        'mail',
        'web_widget_x2many_2d_matrix',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'reports/laboratory_report.xml',
        'data/data_chemical_parameters.xml',
        'data/laboratory_order_sequence.xml',
        'data/laboratory_mail_template.xml',
        'views/res_partner.xml',
        'views/view_chemical_parameters.xml',
        'views/view_muestras_medidas.xml',
        'views/view_orden_de_servicio.xml',
        'views/menu.xml',
    ],
    #TODO ver si es solo letras, porque si es solo eso... es horrible
    # 'assets': {
    #     'web.assets_backend': [
    #         'p13n_vatten/static/src/scss/laboratory_report.scss',
    #     ]
    # },
    'installable': True,
    'auto_install': False,
    'application': True,
}

