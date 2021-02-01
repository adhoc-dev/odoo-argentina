{
    'name': 'Personalizations Edicioneslogos',
    'version': '13.0.1.1.0',
    'category': 'Personalizations',
    'author': 'ADHOC SA',
    'depends': [
        'account_invoice_prices_update',
        'delivery',
        'l10n_ar_stock',
        'portal_sale_distributor',
        'stock',
        'l10n_ar_ux',
        'report_aeroo',
    ],
    'data': [
        'views/res_partner_views.xml',
        'views/sale_order_views.xml',
        'views/stock_picking_views.xml',
        'views/x_partner_project_views.xml',
        'views/x_project_views.xml',
        'views/product_product_view.xml',
        'views/product_template_view.xml',
        'data/ir_actions_act_window.xml',
        'reports/ir_actions_report.xml',
        'reports/account_invoice_report_view.xml',
        'data/ir_cron.xml',
        'data/ir_ui_menu.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
    'auto-install': False,
    'license': 'OPL-1',
}
