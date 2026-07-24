from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class HrHospitalDoctor(models.Model):
    """Doctor or intern practicing in the hospital."""

    _name = 'hr.hospital.doctor'
    _inherit = ['hr.hospital.medic.mixin']
    _description = 'Doctor'
    _order = 'name'

    name = fields.Char(string='Full Name', required=True)
    active = fields.Boolean(default=True)
    specialty = fields.Char()
    phone = fields.Char()
    category_id = fields.Many2one(
        comodel_name='hr.hospital.doctor.category',
        string='Category',
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='System User',
    )
    is_intern = fields.Boolean(
        string='Is Intern',
        compute='_compute_is_intern',
        store=True,
    )
    mentor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Mentor',
        domain="[('id', '!=', id), ('is_intern', '=', False)]",
    )
    intern_ids = fields.One2many(
        comodel_name='hr.hospital.doctor',
        inverse_name='mentor_id',
        string='Interns',
    )
    patient_ids = fields.One2many(
        comodel_name='hr.hospital.patient',
        inverse_name='doctor_id',
        string='Patients',
    )
    visit_ids = fields.One2many(
        comodel_name='hr.hospital.visit',
        inverse_name='doctor_id',
        string='Visits',
    )

    @api.depends('category_id')
    def _compute_is_intern(self):
        """Flag doctors whose category is the intern category."""
        intern = self.env.ref(
            'hr_hospital.hr_hospital_category_intern',
            raise_if_not_found=False,
        )
        for doctor in self:
            doctor.is_intern = bool(intern) and doctor.category_id == intern

    @api.constrains('mentor_id', 'category_id')
    def _check_mentor_id(self):
        """Validate mentor assignments between doctors and interns."""
        for doctor in self:
            if doctor.mentor_id and doctor.mentor_id.is_intern:
                raise ValidationError(_('An intern cannot be selected as a mentor.'))
            if doctor.is_intern and doctor.intern_ids:
                raise ValidationError(_('A doctor who mentors interns cannot become an intern.'))
        if self._has_cycle('mentor_id'):
            raise ValidationError(_('A doctor cannot be their own supervisor (recursive chain).'))

    def action_create_quick_visit(self):
        """Open a prefilled quick-visit form for the doctor."""
        self.ensure_one()
        return self.env['hr.hospital.visit']._get_quick_visit_action({
            'default_doctor_id': self.id,
        })
