from odoo import models, fields, api

class Level(models.Model):
    _name = 'level.level'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Level"

    name=fields.Char(string = 'Level of Education')
    code=fields.Char(string = 'Code')

    branch_ids = fields.Many2many(
        'branch.branch',
        string='Branches',
        ondelete="restrict"
    )

    grade_ids = fields.One2many(
        "grade.grade",
        "level_id",
        string = 'Grade'
    )