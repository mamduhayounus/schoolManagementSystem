from odoo import models, fields, api

class Grade(models.Model):
    _name = 'grade.grade'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Grade"

    name = fields.Char(string='Grade Name')
    code = fields.Char(string = 'Code')


    level_id = fields.Many2one(
        "level.level",
        string = 'Level',
        ondelete="restrict"
    )


    section_ids = fields.Many2many(
        "section.section",
        string = 'Sections'
    )
