{
    'name': 'School Management',
    'version': '18.0',
    'license': 'LGPL-3',
    'author': 'Mamduha Younus',
    'depends': ['mail'],
    'data': [
        "views/security_groups.xml",
        "security/ir.model.access.csv",
        "views/menu.xml",
        "views/student.xml",
        "views/admission.xml",
        "views/section.xml",
        "views/grade.xml",
        "views/level.xml",
        "views/branch.xml",
        "views/institute.xml",
        "report/report.xml",
    ],
    'installable': True,
    'application': True
}