from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class HrHospitalMedicMixin(models.AbstractModel):
    _name = 'hr.hospital.medic.mixin'
    _description = 'Medical Info (mixin)'

    blood_group = fields.Selection(
        selection=[
            ('o', 'O(I)'),
            ('a', 'A(II)'),
            ('b', 'B(III)'),
            ('ab', 'AB(IV)'),
        ],
        string='Blood Group',
    )
    rh_factor = fields.Selection(
        selection=[('plus', 'Rh+'), ('minus', 'Rh-')],
        string='Rh Factor',
    )
    gender = fields.Selection(
        selection=[('male', 'Male'), ('female', 'Female')],
    )
    birthdate = fields.Date(string='Date of Birth')
    age = fields.Integer(compute='_compute_age', string='Age')

    @api.depends('birthdate')
    def _compute_age(self):
        today = fields.Date.context_today(self)
        for record in self:
            if record.birthdate:
                record.age = relativedelta(today, record.birthdate).years
            else:
                record.age = 0
