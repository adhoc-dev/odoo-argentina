# License AGPL-3 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "personalizations_jureclaplata",
    'version': "13.0.4.8.0",
    'author': "Adhoc SA",
    'category': 'Personalizations',
    'license': 'AGPL-3',
    'depends': [
        'academic',
        'account',
        'base',
        'base',
        'contacts',
        'sale_subscription',
    ],
    'data': [
        'data/base_automation.xml',
        'data/student_code.xml',
        'data/ir_actions_server_data.xml',
        'data/ir_cron_data.xml',
        'views/account_move_views.xml',
        'views/res_partner_views.xml',
        'views/res_company_view.xml',
        'views/report_invoice_barcode.xml',
        'views/sale_subscription_views.xml',
        'views/res_config_settings_views.xml',
        'wizards/download_files_wizard_views.xml',
    ],
    'installable': False,
    'auto_install': False,
    'application': False,
}
