{
    'name': 'personalizations_brunetti',
    'version': '13.0.1.5.0',
    'category': 'Personalizations',
    'author': 'ADHOC SA',
    'depends': [
        'account',
        'base_automation',
        'account_payment_group',
        'base',
        'calendar',
        'crm',
        'delivery',
        'helpdesk',
        'inter_company_rules',
        'mass_editing',
        'product',
        'purchase',
    ],
    'data': [
        'data/mail_activity_type.xml',
        'security/security.xml',
        'data/ir_actions_server.xml',
        'data/base_automation.xml',
        'views/account_move_views.xml',
        'views/crm_lead_views.xml',
        'views/crm_stage_views.xml',
        'views/product_template_views.xml',
        'views/purchase_order_views.xml',
        'views/stock_picking_views.xml',
        'security/ir_rule.xml',
        'data/ir_cron.xml'

    ],
    'application': False,
    'license': 'OPL-1',
}
