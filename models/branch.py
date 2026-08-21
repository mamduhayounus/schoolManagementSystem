from odoo import models, fields, api

class Branch(models.Model):
    _name = 'branch.branch'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Branch"

    name = fields.Char(string='Branch Name')
    location= fields.Char(string='Location')
    contact_number = fields.Char(string='Contact Number')
    code = fields.Char(string = 'Code')

    institute_id = fields.Many2one(
        "institute.institute",
        string="Institution",
        ondelete="restrict"
    )

    level_ids = fields.Many2many(
        "level.level",
        # "branch_id",
        string="Levels"
    )