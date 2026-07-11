from odoo import _, api, fields, models


class HrHospitalPatient(models.Model):
    _name = 'hr.hospital.patient'
    _inherit = ['hr.hospital.medic.mixin']
    _description = 'Patient'
    _order = 'name'

    name = fields.Char(string='Full Name', required=True)
    active = fields.Boolean(default=True)
    phone = fields.Char()
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Personal Doctor',
    )
    insurance_number = fields.Char(string='Insurance Policy No.', size=20)
    history_ids = fields.One2many(
        comodel_name='hr.hospital.doctor.history',
        inverse_name='patient_id',
        string='Doctor History',
    )
    visit_ids = fields.One2many(
        comodel_name='hr.hospital.visit',
        inverse_name='patient_id',
        string='Visits',
    )
    visit_count = fields.Integer(
        string='Visit Count',
        compute='_compute_visit_count',
    )

    @api.depends('visit_ids')
    def _compute_visit_count(self):
        for patient in self:
            patient.visit_count = len(patient.visit_ids)

    def action_view_visits(self):
        self.ensure_one()
        action = self.env['ir.actions.act_window']._for_xml_id(
            'hr_hospital.hr_hospital_visit_action',
        )
        action.update(
            name=_('Visits: %s') % self.name,
            domain=[('patient_id', '=', self.id)],
            context={'default_patient_id': self.id},
        )
        return action

    def action_create_quick_visit(self):
        self.ensure_one()
        return self.env['hr.hospital.visit']._get_quick_visit_action({
            'default_patient_id': self.id,
            'default_doctor_id': self.doctor_id.id,
        })
