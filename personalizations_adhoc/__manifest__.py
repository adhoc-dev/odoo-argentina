{
    'name': 'personalizations_adhoc',
    'version': "15.0.1.0.0",
    'category': 'Personalizations',
    'author': 'ADHOC SA',
    'depends': [
        'hr_timesheet',
        'hr_contract',
    ],
    'data': [
        'views/hr_contract_views.xml',
        'views/hr_job_views.xml',
        'views/hr_salary_category_views.xml',
        'views/hr_seniority_views.xml',
        'data/hr_salary_category_data.xml',
        'data/hr_seniority_data.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
    'license': 'OPL-1',
}
