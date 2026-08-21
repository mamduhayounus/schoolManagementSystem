from odoo import models, fields, api

class Section(models.Model):
    _name = 'section.section'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Section"

    name = fields.Char(string='Section Name')
    code= fields.Char(string = 'Code')

    grade_ids = fields.Many2many(
        "grade.grade",
        string = 'Grade',
        ondelete="restrict"
    )
    student_ids = fields.One2many(
        "student.student",
        "section_id",
        string = 'Students'
    )