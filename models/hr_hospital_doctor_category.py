from odoo import fields, models


class HrHospitalDoctorCategory(models.Model):
    _name = 'hr.hospital.doctor.category'
    _description = 'Doctor Category'
    _order = 'sequence, name'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)
    doctor_ids = fields.One2many(
        comodel_name='hr.hospital.doctor',
        inverse_name='category_id',
        string='Doctors',
    )

    _name_uniq = models.Constraint(
        'unique (name)',
        'A doctor category with this name already exists.',
    )
