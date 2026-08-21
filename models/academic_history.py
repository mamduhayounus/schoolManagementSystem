from odoo import fields, models, api

class AcademicHistory(models.Model):
    _name = 'academic_history.academic_history'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Academic History"

    name = fields.Char(string='Previous School Name')
    address = fields.Char(string='Previous School Address')
    grade = fields.Char(string='Previous School Grade')
    year = fields.Char(string='Previous School Completion Year')
    percentage = fields.Char(string='Previous School Percentage')
    board = fields.Char(string='Previous School Board')
    disciplinary_record = fields.Boolean(string='Disciplinary Record')
    disciplinary_record_details = fields.Char(string='Disciplinary Record Details')

    student_id = fields.Many2one(
        'student.student',
        string='Student',
        ondelete='cascade'
    )

    admission_id = fields.Many2one(
        'admission.admission',
        string='Admission Application',
        ondelete='cascade'
    )