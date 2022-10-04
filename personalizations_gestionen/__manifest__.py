# License AGPL-3 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "personalizations_gestionen",
    'version': "13.0.1.0.0",
    'author': "Adhoc SA",
    'category': 'Personalizations',
    'license': 'AGPL-3',
    'depends': [
        'l10n_ar_ux',
        'l10n_ar_purchase',
    ],
    'data': [
        'reports/report_payment_group.xml',
        'reports/purchase_report_templates.xml',
        'views/purchase_order_views.xml'
    ],
    'demo': [
    ],
    'installable': False,
    'auto_install': False,
    'application': False,
}
