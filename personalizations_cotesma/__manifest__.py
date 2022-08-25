# License AGPL-3 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "personalizations_cotesma",
    'version': "13.0.1.16.0",
    'author': "Adhoc SA",
    'category': 'Personalizations',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'fleet',
        'l10n_ar_account_withholding',
        'stock_request_ux',
        'purchase_ux',
        'purchase_requisition',
        'purchase_request_to_requisition',
        'purchase_suggest',
        'product_template_tags',
        'project_ux',
        'purchase_request',
        'product_stock_by_location',
        'purchase_tier_validation',
        'project_stage',
        'saas_client_account',
    ],
    'data': [
        'security/cotesma_security.xml',
        'security/ir.model.access.csv',
        'views/account_journal_dashboard_view.xml',
        'views/purchase_order_views.xml',
        'views/res_users_views.xml',
        'views/stock_request_order_views.xml',
        'views/purchase_requisition_views.xml',
        'views/account_report.xml',
        'views/report_journal_entries.xml',
        'views/product_views.xml',
        'wizards/purchase_suggest_view.xml',
        'views/stock_menu_views.xml',
        'views/stock_location_views.xml',
    ],
    'demo': [
    ],
    'installable': False,
    'auto_install': False,
    'application': False,
}
