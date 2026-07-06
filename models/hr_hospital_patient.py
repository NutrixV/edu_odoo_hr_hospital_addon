from odoo import fields, models


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
