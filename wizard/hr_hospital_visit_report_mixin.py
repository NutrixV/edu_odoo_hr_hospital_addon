from datetime import timedelta

from odoo import api, fields, models


class HrHospitalVisitReportMixin(models.AbstractModel):
    _name = 'hr.hospital.visit.report.mixin'
    _description = 'Visit Report Mixin'

    doctor_ids = fields.Many2many(
        comodel_name='hr.hospital.doctor',
        string='Doctors',
    )
    date_from = fields.Date(string='Period Start')
    date_to = fields.Date(string='Period End')

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if (
            'doctor_ids' in fields_list
            and self.env.context.get('active_model') == 'hr.hospital.doctor'
        ):
            res['doctor_ids'] = [
                fields.Command.set(self.env.context.get('active_ids', [])),
            ]
        return res

    def _get_visit_domain(self):
        self.ensure_one()
        domain = []
        if self.doctor_ids:
            domain.append(('doctor_id', 'in', self.doctor_ids.ids))
        if self.date_from:
            domain.append(('scheduled_date', '>=', self.date_from))
        if self.date_to:
            domain.append(('scheduled_date', '<', self.date_to + timedelta(days=1)))
        return domain
