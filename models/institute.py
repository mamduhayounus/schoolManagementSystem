from odoo import models, fields, api

class Institute(models.Model):
    _name = 'institute.institute'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Institute"

    name = fields.Char(string='Institute Name')
    contact_number = fields.Char(string='Contact Number')
    code = fields.Char(string = 'Code', required=True)

    branch_ids = fields.One2many(
        "branch.branch",
        "institute_id",
        string="Branches"    )