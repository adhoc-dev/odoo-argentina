{
    'name': 'personalizations_winwineducation',
    'version': '13.0.1.1.0',
    'category': 'Personalizations',
    'author': 'ADHOC SA',
    'depends': [
        'academic',
        'account',
        'account_payment_group',
        'account_reports',
        'base',
        'crm_survey',
        'hr',
        'hr_recruitment_survey',
        'mail',
        'maintenance',
        'payment',
        'product',
        'sale',
        'sale_subscription',
        'sales_team',
        'stock',
        'survey',
        'report_aeroo',
        'l10n_ar_ux',
    ],
    'data': [
        'security/res_groups.xml',
        'report/academic_report_data.xml',
        'views/account_payment_group_views.xml',
        'views/crm_lead_views.xml',
        'views/crm_team_views.xml',
        'views/hr_applicant_views.xml',
        'views/hr_employee_views.xml',
        'views/hr_job_views.xml',
        'views/maintenance_request_views.xml',
        'views/payment_token_views.xml',
        'views/res_partner_views.xml',
        'views/res_users_views.xml',
        'views/sale_subscription_views.xml',
        'views/survey_survey_views.xml',
        'views/survey_user_input_views.xml',
        'views/x_motive_rejected_proposal_views.xml',
        'views/x_no_vacancy_specification_motive_views.xml',
        'views/x_account_overdue_type.xml',
        'data/ir_actions_act_window.xml',
        'data/ir_cron.xml',
        'data/ir_actions_server.xml',
        'data/ir_ui_menu.xml',
        'data/base_automation.xml',
        'views/academic_group_views.xml',
        'views/academic_menuitem.xml',
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
    ],
    'installable': False,
    'application': False,
    'license': 'OPL-1',
}
