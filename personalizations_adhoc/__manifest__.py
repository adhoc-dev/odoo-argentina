{
    'name': 'personalizations_adhoc',
    'version': "15.0.1.7.0",
    'category': 'Personalizations',
    'author': 'ADHOC SA',
    'depends': [
        'hr_timesheet',
        'hr_contract',
        'helpdesk',
        'project',
        'project_ux',
        'helpdesk_ux',
        'sale_timesheet',
        'helpdesk_timesheet',
        'helpdesk_solutions_project',
        'saas_provider_adhoc',
    ],
    'data': [
        'views/hr_contract_views.xml',
        'views/adhoc_product_views.xml',
        'views/adhoc_product_menus.xml',
        'views/adhoc_module_views.xml',
        'views/hr_job_views.xml',
        'views/hr_salary_category_views.xml',
        'views/hr_seniority_views.xml',
        'views/helpdesk_ticket_views.xml',
        'views/project_task_views.xml',
        'views/portal_my_timesheets.xml',
        'data/hr_salary_category_data.xml',
        'data/hr_seniority_data.xml',
        'security/ir.model.access.csv',
    ],

    'installable': True,
    'application': False,
    'license': 'OPL-1',
}
