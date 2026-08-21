from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

class Admission(models.Model):
    _name = 'admission.admission'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Admission"

    name = fields.Char(
        string="Admission Number",
        readonly=True,
        default="New",
        copy=False
    )
    student_id = fields.Many2one(
        "student.student",
        string="Created Student",
        readonly=True,
        copy=False
    )

    academic_history_ids = fields.One2many(
        "academic_history.academic_history",
        "admission_id",
        string="Academic History Records",
    )

    # Fetch the specific ID string field directly from student.student model
    student_ref_display = fields.Char(
        related='student_id.code',
        string="Student ID",
        readonly=True
    )

    # for status showing student is created
    student_code = fields.Char(
        string="Student Code",
        related="student_id.code",
        readonly=True
    )

    uploaded_image = fields.Image(string="Upload Image", max_width=1024, max_height=768, copy=False)

    # Admission Application
    application_date = fields.Date(
        string="Application Date",
        default=fields.Date.today,
        readonly=True,
        copy=False
    )
    admission_type = fields.Selection(
        [
            ('new', 'New Admission'),
            ('transfer', 'Transfer'),
            ('readmission', 'Readmission'),
        ],
        string="Admission Type",
        default='new'
    )
    academic_year = fields.Char(string="Academic Year")
    applied_for_institute_id = fields.Many2one(
        "institute.institute",
        string="Applied for Institute",
        ondelete="restrict"
    )

    applied_for_branch_id = fields.Many2one(
        "branch.branch",
        string="Applied for Branch",
        ondelete="restrict"
    )

    applied_for_level_id = fields.Many2one(
        "level.level",
        string="Applied for Level",
        ondelete="restrict"
    )

    applied_for_grade_id = fields.Many2one(
        "grade.grade",
        string="Applied for Grade",
        ondelete="restrict"
    )

    # Student Core Information
    first_name = fields.Char(string='Student Name', copy=False)
    middle_name = fields.Char(string='Middle Name')
    last_name = fields.Char(string='Last Name')
    dob = fields.Date(string='Date of Birth', copy=False)
    age = fields.Integer(string='Age', compute='_compute_age', readonly=True)
    age_display = fields.Char(string="Age Display", compute='_compute_age', readonly=True)
    pob = fields.Char(string='Place of Birth')

    gender = fields.Selection(
        [
            ('male', 'Male'),
            ('female', 'Female')
        ],
        string="Gender"
    )

    cnic = fields.Char(string='CNIC/ B-Form Number', copy=False)
    nationality = fields.Char(string="Nationality")
    dual_nationality = fields.Boolean(string="Dual Nationality")
    dual_nationality_details = fields.Char(string="Dual Nationality Details")
    language_urdu = fields.Boolean(string="Urdu")
    language_english = fields.Boolean(string="English")
    language_other = fields.Boolean(string="Other")
    other_languages = fields.Char(string="Other Languages")
    religion = fields.Char(string="Religion")

    # Residential and Logistic Data
    permanent_address = fields.Char(string='Permanent Address')
    current_address = fields.Boolean(string="Same as Permanent Address")
    current_address_details = fields.Char(string="Current Address")
    commute_mode = fields.Selection(
        [
            ('school_transport', 'School Transport'),
            ('public_transport', 'Public Transport'),
            ('private_transport', 'Private Transport'),
            ('parents_drop_off', 'Parents Drop-off'),
            ('self_commute', 'Self-Commute')
        ],
        string="Commute Mode"
    )

    # Parental Information
    father_name = fields.Char(string='Father Name')
    father_is_alive = fields.Boolean(string="Father is Alive")
    father_mobile_number = fields.Char(string='Father Mobile Number')
    father_personal_email = fields.Char(string='Father Personal Email')
    father_home_address = fields.Char(string='Father Home Address')

    father_job_title = fields.Char(string='Father Job Title')
    father_office_address = fields.Char(string='Father Office Address')
    father_workplace_name = fields.Char(string='Father Workplace Name')
    father_workplace_landline = fields.Char(string='Father Workplace Landline')
    father_work_email = fields.Char(string='Father Work Email')

    father_marital_status = fields.Selection(
        [
            ('single', 'Single'),
            ('married', 'Married'),
            ('divorced', 'Divorced'),
            ('widowed', 'Widowed'),
            ('critical', 'Critical')
        ],
        string="Father Marital Status"
    )

    father_alumni = fields.Boolean(string="Father is Alumni")
    father_alumni_details = fields.Char(string="Father Alumni Details")

    # Mother Information
    mother_name = fields.Char(string='Mother Name')
    mother_is_alive = fields.Boolean(string="Mother is Alive")
    mother_mobile_number = fields.Char(string='Mother Mobile Number')
    mother_personal_email = fields.Char(string='Mother Personal Email')
    mother_home_address = fields.Char(string='Mother Home Address')

    mother_job_title = fields.Char(string='Mother Job Title')
    mother_office_address = fields.Char(string='Mother Office Address')
    mother_workplace_name = fields.Char(string='Mother Workplace Name')
    mother_workplace_landline = fields.Char(string='Mother Workplace Landline')
    mother_work_email = fields.Char(string='Mother Work Email')

    mother_alumni = fields.Boolean(string="Mother is Alumni")
    mother_alumni_details = fields.Char(string="Mother Alumni Details")

    # Guardian Information
    guardian_is_father = fields.Boolean(string="Guardian is Father")
    guardian_is_mother = fields.Boolean(string="Guardian is Mother")

    guardian_name = fields.Char(string='Guardian Name')
    guardian_relation = fields.Char(string='Guardian Relation')

    guardian_mobile_number = fields.Char(string='Guardian Mobile Number')
    guardian_personal_email = fields.Char(string='Guardian Personal Email')
    guardian_home_address = fields.Char(string='Guardian Home Address')

    guardian_job_title = fields.Char(string='Guardian Job Title')
    guardian_office_address = fields.Char(string='Guardian Office Address')
    guardian_workplace_name = fields.Char(string='Guardian Workplace Name')
    guardian_workplace_landline = fields.Char(string='Guardian Workplace Landline')
    guardian_work_email = fields.Char(string='Guardian Work Email')

    guardian_marital_status = fields.Selection(
        [
            ('single', 'Single'),
            ('married', 'Married'),
            ('divorced', 'Divorced'),
            ('widowed', 'Widowed'),
            ('critical', 'Critical')
        ],
        string="Guardian Marital Status"
    )

    guardian_alumni = fields.Boolean(string="Guardian is Alumni")
    guardian_alumni_details = fields.Char(string="Guardian Alumni Details")

    # Emergency Contact Non-Parents
    emergency_contact_name1 = fields.Char(string='Emergency Contact Names')
    emergency_contact_relation1 = fields.Char(string='Emergency Contact Relation')
    emergency_contact_number1 = fields.Char(string='Emergency Contact Number')

    authorised_pickup_name = fields.Char(string='Authorised Pickup Names')
    authorised_pickup_cnic = fields.Char(string='Authorised Pickup CNIC')
    authorised_pickup_number = fields.Char(string='Authorised Pickup Number')

    # Academic History Single Fields
    previous_school = fields.Char(string='Previous School')
    previous_school_address = fields.Char(string='Previous School Address')
    previous_school_class = fields.Char(string='Previous School Class')
    previous_school_year = fields.Char(string='Previous School Completion Year')
    previous_school_percentage = fields.Char(string='Previous School Percentage')
    previous_school_board = fields.Char(string='Previous School Board')
    disciplinary_record = fields.Boolean(string='Disciplinary Record')
    disciplinary_record_details = fields.Char(string='Disciplinary Record Details')

    # Medical
    blood_group = fields.Selection(
        [
            ('A+', 'A+'),
            ('A-', 'A-'),
            ('B+', 'B+'),
            ('B-', 'B-'),
            ('AB+', 'AB+'),
            ('AB-', 'AB-'),
            ('O+', 'O+'),
            ('O-', 'O-')
        ],
    )
    chronic_conditions = fields.Char(string='Chronic Conditions')
    has_allergies = fields.Boolean(string="Has Allergies")
    allergy_details = fields.Text(
        string="Allergy Details",
        help="Mention food, insect, medication, or other allergies."
    )
    allergy_severity = fields.Selection(
        [
            ('mild', 'Mild'),
            ('moderate', 'Moderate'),
            ('severe', 'Severe'),
        ],
        string="Allergy Severity"
    )

    requires_epipen = fields.Boolean(string="Requires Epipen")

    has_regular_medication = fields.Boolean(string="Takes Regular Medication")
    regular_medication_details = fields.Text(
        string="Regular Medication Details",
        help="Mention medicine names, dosages, and timings during school hours."
    )

    disability = fields.Boolean(string="Has Disability")
    disability_details = fields.Text(string="Disability Details", help="Mention any disabilities or conditions (e.g: blind, deaf, etc.).")
    learning_disability = fields.Boolean(string="Learning Disability")
    learning_disability_details = fields.Text(
        string="Learning Disability Details",
        help="Mention any learning disabilities or conditions (e.g: dyslexia, autism, etc.)."
    )

    family_doctors_name = fields.Char(string="Family Doctor's Name")
    family_doctors_contact = fields.Char(string="Family Doctor's Contact")
    family_doctors_email = fields.Char(string="Family Doctor's Email")
    family_doctors_clinic = fields.Char(string="Family Doctor's Clinic Address")

    # Administrative and Financial Information
    siblings_count = fields.Integer(string="Number of Siblings")
    siblings_name = fields.Char(string="Name of Siblings")
    siblings_age = fields.Char(string="Age of Siblings")
    siblings_education = fields.Char(string="Education of Siblings")
    siblings_enrolled = fields.Boolean(string="Enrolled in School")
    siblings_enrolled_details = fields.Char(string="Details of Grade Enrolled")
    siblings_occupation = fields.Char(string="Occupation of Siblings")
    siblings_income = fields.Char(string="Income of Siblings")

    # tuition-fee responsible person
    fee_payer_name = fields.Char(string="Name of Tuition-Fee Payer")
    fee_payer_cnic = fields.Char(string="CNIC of Payer")
    fee_payer_address = fields.Char(string="Billing Address of Payer")
    fee_payer_email = fields.Char(string="Billing Email of Payer")

    # Marketing Source
    marketing_source = fields.Selection(
        [
            ('advertisement', 'Advertisement'),
            ('social_media', 'Social Media'),
            ('friend', 'Friend'),
            ('newspaper', 'Newspaper'),
            ('billboard', 'Billboard'),
            ('tv', 'TV'),
            ('other', 'Other')
        ],
        string="Marketing Source"
    )
    marketing_source_details = fields.Char(string="Details of Marketing Source")

    # Legal Consent
    media_release = fields.Boolean(string="Consent to use student photos in school marketing and newsletters.")
    field_trip_permission = fields.Boolean(string="General consent for local, supervised school excursions.")
    medical_emergency_authorization = fields.Boolean(string="Authorization for the school to transport the child to a hospital in a critical emergency.")
    medical_emergency_signature = fields.Char(string="Medical Emergency Signature")
    medical_emergency_signature_date = fields.Date(string="Medical Emergency Signature Date")

    accuracy_declaration = fields.Boolean(string="I confirm that all provided information is accurate.")
    accuracy_signature = fields.Char(string="Accuracy Declaration Signature")
    accuracy_signature_date = fields.Date(string="Accuracy Declaration Date")

    # status bar and buttons
    status = fields.Selection(
        [
            ('draft', 'Draft'),
            ('pending', 'Pending'),
            ('accept', 'Accepted'),
            ('reject', 'Rejected')
        ],
        string="Status",
        default='draft',
        tracking=True,
        copy=False
    )
    

    def action_draft(self):
        for admission in self:
            admission.status = 'draft'

    def action_pending(self):
        for admission in self:
            admission.status = 'pending'

    def action_accept(self):
        for admission in self:
            admission.status = 'accept'

    def action_reject(self):
        for admission in self:
            admission.status = 'reject'

    def action_open_student(self):
        self.ensure_one()
        if not self.student_id:
            return

        return {
            'name': 'Student Profile',
            'type': 'ir.actions.act_window',
            'res_model': 'student.student',
            'res_id': self.student_id.id,
            'view_mode': 'form',
            'target': 'current',
        }

    # student creation
    def action_create_student(self):
        self.ensure_one()
        if self.student_id:
            raise UserError("Student is already created for this admission.")
        if self.dob and self.age < 2:
            raise UserError("Student must be at least 2 years old!")
        student_name = " ".join(filter(None, [
            self.first_name,
            self.middle_name,
            self.last_name
        ]))
        # Create student
        student = self.env['student.student'].create({
            'code': 'New',
            'name': student_name,
            'age': self.age,
            'dob': self.dob,
            'gender': self.gender,
            'cnic': self.cnic,
            'father_name': self.father_name,
            'guardian_name': self.guardian_name,
            'address': self.permanent_address,
            'disability': self.disability,
            'disability_details': self.disability_details,
            'institute_id': self.applied_for_institute_id.id,
            'branch_id': self.applied_for_branch_id.id,
            'level_id': self.applied_for_level_id.id,
            'grade_id': self.applied_for_grade_id.id,
            'admission_id': self.id,
            'uploaded_image': self.uploaded_image,
            'status': 'draft',
        })
        for history in self.academic_history_ids:
            history.student_id = student.id
        if self.previous_school:
            self.env['academic_history.academic_history'].create({
                'name': self.previous_school,
                'address': self.previous_school_address,
                'grade': self.previous_school_class,
                'year': self.previous_school_year,
                'percentage': self.previous_school_percentage,
                'board': self.previous_school_board,
                'disciplinary_record': self.disciplinary_record,
                'disciplinary_record_details': self.disciplinary_record_details,
                'student_id': student.id,
                'admission_id': self.id,
            })
        self.student_id = student.id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Student Profile',
            'res_model': 'student.student',
            'res_id': student.id,
            'view_mode': 'form',
            'target': 'current',
        }


    # sequence of admission number
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('admission.admission') or 'New'
        return super().create(vals_list)

    # on-changing institute, branch, level, grade
    @api.onchange('applied_for_institute_id')
    def _onchange_applied_for_institute_id(self):
        if self.applied_for_institute_id:
            self.applied_for_branch_id = False
            self.applied_for_level_id = False
            self.applied_for_grade_id = False

    @api.onchange('applied_for_branch_id')
    def _onchange_applied_for_branch_id(self):
        if self.applied_for_branch_id:
            self.applied_for_level_id = False
            self.applied_for_grade_id = False

    @api.onchange('applied_for_level_id')
    def _onchange_applied_for_level_id(self):
        if self.applied_for_level_id:
            self.applied_for_grade_id = False

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

    # no same cnic record
    @api.constrains('cnic')
    def _check_unique_cnic(self):
        for record in self:
            if record.cnic:
                clean_cnic = record.cnic.strip()

                duplicate_admission = self.search([
                    ('cnic', '=', clean_cnic),
                    ('id', '!=', record.id)
                ], limit=1)

                if duplicate_admission:
                    raise ValidationError(
                        f"An admission record with CNIC '{clean_cnic}' already exists "
                        f"({duplicate_admission.name} - {duplicate_admission.first_name})!"
                    )

                duplicate_student = self.env['student.student'].search([
                    ('cnic', '=', clean_cnic)
                ], limit=1)

                if duplicate_student:
                    raise ValidationError(
                        f"A student with CNIC '{clean_cnic}' is already enrolled "
                        f"(Student Code: {duplicate_student.code})!"
                    )