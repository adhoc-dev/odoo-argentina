# License AGPL-3 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "personalizations_electricidadcanning",
    'version': "13.0.1.0.0",
    'author': "Adhoc SA",
    'category': 'Personalizations',
    'license': 'AGPL-3',
    'depends': [
        'sale',
    ],
    'data': [
        'views/sale_order_views.xml',
        'views/sale_report_personalization.xml',
    ],
    'installable': False,
    'auto_install': False,
    'application': False,
}
