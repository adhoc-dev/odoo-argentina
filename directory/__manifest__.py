# Copyright 2019 Vauxoo
# License AGPL-3 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "directory",
    'summary': """
        Odoo module to telephone directory Cotesma webpage""",
    'author': "Vauxoo",
    'website': "http://www.cotesma.coop",
    'category': 'Directory Telephone',
    'license': 'AGPL-3',
    'version': "13.0.1.0.0",
    'depends': ['website'],
    'data': [
        'security/directory_access_rules.xml',
        'security/ir.model.access.csv',
        'templates/directory_telephone_template.xml',
        'views/directory_telephone_views.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
