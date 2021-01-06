# -*- coding: utf-8 -*-
{
    'name': 'personalizations_arbusta',
    'version': '13.0.1.8.1',
    'category': 'Personalizations',
    'author': 'ADHOC SA',
    'depends': [
        'account',
        'account_accountant',
        'analytic',
        'base',
        'crm',
        'helpdesk_timesheet_ux',
        'hr_attendance',
        'hr_contract',
        'hr_expense',
        'hr_holidays',
        'hr_gamification',
        'hr_timesheet',
        'hr_recruitment',
        'hr_skills',
        'mail',
        'maintenance',
        'mass_mailing',
        'project_ux',
        'project_stage',
        'resource',
        'sale_subscription',
    ],
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'views/account_account_views.xml',
        'views/account_analytic_account_views.xml',
        'views/account_analytic_line_views.xml',
        'views/account_move_views.xml',
        'views/account_move_line_views.xml',
        'views/crm_lead_views.xml',
        'views/helpdesk_ticket_views.xml',
        'views/hr_attendance_views.xml',
        'views/hr_contract_views.xml',
        'views/hr_employee_views.xml',
        'views/hr_expense_views.xml',
        'views/hr_expense_sheet_views.xml',
        'views/hr_leave_views.xml',
        'views/hr_leave_report_calendar_views.xml',
        'views/mailing_mailing_views.xml',
        'views/maintenance_equipment_views.xml',
        'views/project_project_views.xml',
        'views/project_stage_views.xml',
        'views/project_task_views.xml',
        'views/res_partner_views.xml',
        'views/res_users_views.xml',
        'views/sale_subscription_views.xml',
        'views/x_seguimientos_views.xml',
        'views/x_seguimientos_stage_views.xml',
        'data/ir_actions_act_window.xml',
        'data/ir_ui_menu.xml',
    ],
    'application': False,
    'license': 'OPL-1',
}
