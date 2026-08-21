from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Student(models.Model):
    _name = 'student.student'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Student"

    code = fields.Char(
        string='Code',
        default='New',
        readonly=True,
        copy=False
    )
    std_id = fields.Char(string='Student ID')
    name = fields.Char(string='Student Name')
    uploaded_image = fields.Image(string='Student Image', max_height=1024, max_width=1024)
    cnic = fields.Char(string='CNIC/ B-Form Number', copy=False)
    dob = fields.Date(string='Date of Birth')
    age = fields.Integer(string='Age', compute='_compute_age', store=True, readonly=True)
    age_display = fields.Char(string="Age Display", compute='_compute_age', readonly=True)

    father_name = fields.Char(string='Father Name')
    guardian_name = fields.Char(string='Guardian Name')
    previous_school = fields.Char(string='Previous School')
    previous_school_address = fields.Char(string='Previous School Address')
    previous_school_class = fields.Char(string='Previous School Class')
    previous_school_year = fields.Char(string='Previous School Completion Year')
    previous_school_percentage = fields.Char(string='Previous School Percentage')
    previous_school_board = fields.Char(string='Previous School Board')
    disciplinary_record = fields.Boolean(string='Disciplinary Record')
    disciplinary_record_details = fields.Char(string='Disciplinary Record Details')
    gender = fields.Selection(
        [
            ('male', 'Male'),
            ('female', 'Female')
        ],
        string="Gender"
    )
    address = fields.Char(string='Home Address')
    disability = fields.Boolean(string="Has Disability")
    disability_details = fields.Text(string="Disability Details")

    institute_id = fields.Many2one(
        "institute.institute",
        string="Institute",
        ondelete="restrict"
    )
    branch_id = fields.Many2one(
        "branch.branch",
        string="Branch",
        ondelete="restrict"
    )
    level_id = fields.Many2one(
        "level.level",
        string="Level",
        ondelete="restrict"
    )
    grade_id = fields.Many2one(
        "grade.grade",
        string="Grade",
        ondelete="restrict"
    )
    section_id = fields.Many2one(
        "section.section",
        string="Section",
        ondelete="restrict"
    )

    admission_id = fields.Many2one(
        "admission.admission",
        string="Admission Application",
        ondelete="set null"
    )

    academic_history_ids = fields.One2many(
        "academic_history.academic_history",
        "student_id",
        string="Academic History",
    )

    # statusbar
    status = fields.Selection(
        [
            ('draft', 'Draft'),
            ('accept', 'Enrolled'),
            ('reject', 'Rejected')
        ],
        string="Status",
        default='draft',
        tracking=True
    )



    def action_draft(self):
        for student in self:
            student.status = 'draft'

    def action_accept(self):
        for student in self:
            student.status = 'accept'

    def action_reject(self):
        for student in self:
            student.status = 'reject'

    # sequence generator
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('code', 'New') == 'New':
                institute = False
                if vals.get('institute_id'):
                    institute = self.env['institute.institute'].browse(vals['institute_id'])

                if institute and institute.code:
                    clean_code = institute.code.strip().upper()
                    seq_code = f"student.sequence.{clean_code.lower()}"
                    generated_code = self.env['ir.sequence'].next_by_code(seq_code)

                    if not generated_code:
                        self.env['ir.sequence'].sudo().create({
                            'name': f"Student Sequence - {clean_code}",
                            'code': seq_code,
                            'prefix': f"{clean_code}-",
                            'padding': 4,
                            'number_next': 1000,
                            'number_increment': 1,
                            'company_id': False,
                        })
                        generated_code = self.env['ir.sequence'].next_by_code(seq_code)

                    vals['code'] = generated_code
                else:
                    vals['code'] = self.env['ir.sequence'].next_by_code('student.student') or 'New'

        return super().create(vals_list)

    #student id is not same
    @api.constrains('std_id')
    def _check_unique_std_id(self):
        for record in self:
            if record.std_id:
                clean_std_id = record.std_id.strip()

                # Look for another student with the exact same Student ID
                duplicate = self.search([
                    ('std_id', '=', clean_std_id),
                    ('id', '!=', record.id)
                ], limit=1)

                if duplicate:
                    raise ValidationError(
                        f"Student ID '{clean_std_id}' is already assigned to "
                        f"{duplicate.name} (Student Code: {duplicate.code})!"
                    )

    # age calculator
    @api.depends('dob')
    def _compute_age(self):
        for record in self:
            if record.dob:
                days = (fields.Date.today() - record.dob).days
                calculated_age = max(0, int(days / 365.25))
                record.age = calculated_age
                record.age_display = f"{calculated_age} years"
            else:
                record.age = 0
                record.age_display = ""

    @api.constrains('dob')
    def _check_student_age(self):
        for record in self:
            if record.dob and record.age < 2:
                raise ValidationError("Student must be at least 2 years old!")

    # on-changing institute, branch, level, grade
    @api.onchange('institute_id')
    def _onchange_institute_id(self):
        if self.institute_id:
            self.branch_id = False
            self.level_id = False
            self.grade_id = False
            self.section_id = False

    @api.onchange('branch_id')
    def _onchange_branch(self):
        if self.branch_id:
            self.level_id = False
            self.grade_id = False
            self.section_id = False

    @api.onchange('level_id')
    def _onchange_level(self):
        if self.level_id:
            self.grade_id = False
            self.section_id = False

    @api.onchange('grade_id')
    def _onchange_grade(self):
        if self.grade_id:
            self.section_id = False

    # no student with same cnic
    @api.constrains('cnic', 'admission_id')
    def _check_unique_cnic(self):
        for record in self:
            if record.cnic:
                clean_cnic = record.cnic.strip()

                duplicate_student = self.search([
                    ('cnic', '=', clean_cnic),
                    ('id', '!=', record.id)
                ], limit=1)

                if duplicate_student:
                    raise ValidationError(
                        f"Another student with CNIC '{clean_cnic}' already exists "
                        f"(Student Code: {duplicate_student.code} - {duplicate_student.name})!"
                    )

                admission_domain = [('cnic', '=', clean_cnic)]
                if record.admission_id:
                    admission_domain.append(('id', '!=', record.admission_id.id))

                duplicate_admission = self.env['admission.admission'].search(admission_domain, limit=1)

                if duplicate_admission:
                    raise ValidationError(
                        f"An admission application with CNIC '{clean_cnic}' already exists "
                        f"(Admission No: {duplicate_admission.name})!"
                    )
