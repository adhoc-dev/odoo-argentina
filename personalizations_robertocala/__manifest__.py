{
    'name': 'personalizations_robertocala',
    'version': '13.0.1.4.0',
    'category': 'Personalizations',
    'author': 'ADHOC SA',
    'depends': [
        'account_ux',
        'base_automation',
        'board',
        'delivery',
        'l10n_ar_ux',
        'l10n_ar_stock',
        'note',
        'price_security',
        'product_planned_price',
        'product_replenishment_cost',
        'product_price_taxes_included',
        'product_brand',
        'purchase',
        'stock_picking_labels',
        'website_sale',
    ],
    'data': [
        'security/res_groups.xml',
        'data/ir_actions_server.xml',
        'data/base_automation.xml',
        'views/account_move_views.xml',
        'views/product_product_views.xml',
        'views/product_template_views.xml',
        'views/purchase_order_views.xml',
        'views/sale_order_views.xml',
        'views/stock_move_line_views.xml',
        'data/ir_actions_act_window.xml',
        'report/ir_actions_report.xml',
        'data/ir_ui_menu.xml',
        'data/ir_cron.xml',
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
    ],
    'installable': False,
    'application': False,
    'auto-install': False,
    'license': 'OPL-1',
}