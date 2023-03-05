{
    'name': "Ant POS Custom Reports",
    'version': '1.0',
    'depends': ['base','stock'],
    'author': "Ant Developments",
    'category': 'Ant/Reports',
    'description': """
    Custom reports for Ant POS
    """,
    'data': [
        'report/inv_report.xml',
        'report/inv_report_action.xml',
        'report/pat_report.xml',
        'report/pat_report_action.xml',
        'security/ir.model.access.csv',
        'views/custom_report_views.xml',
        'wizard/inv_report_wizard.xml',
        'wizard/pat_report_wizard.xml'
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False
}