# License AGPL-3 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "personalizations_jureclaplata",
<<<<<<< HEAD
    'version': "13.0.1.0.0",
=======
    'version': "13.0.3.0.0",
>>>>>>> 6b5ef1a... temp
    'author': "Adhoc SA",
    'category': 'Personalizations',
    'license': 'AGPL-3',
    'depends': [
        'academic',
<<<<<<< HEAD
=======
        'account',
        'base',
>>>>>>> 6b5ef1a... temp
        'contacts',
        'sale_subscription',
    ],
    'data': [
        'views/res_partner_views.xml',
        'views/res_company_view.xml',
        'views/report_invoice_barcode.xml',
        'views/sale_subscription_views.xml',
        'data/base_automation.xml',
    ],
    'installable': False,
    'auto_install': False,
    'application': False,
}
