from odoo import _, api, fields, models


class HrHospitalVisitReport(models.TransientModel):
    _name = 'hr.hospital.visit.report'
    _inherit = ['hr.hospital.visit.report.mixin']
    _description = 'Visit Report'

    patient_ids = fields.Many2many(
        comodel_name='hr.hospital.patient',
        string='Patients',
    )
    only_done = fields.Boolean(string='Only Completed Visits')
    disease_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string='Disease',
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if (
            'patient_ids' in fields_list
            and self.env.context.get('active_model') == 'hr.hospital.patient'
        ):
            res['patient_ids'] = [
                fields.Command.set(self.env.context.get('active_ids', [])),
            ]
        return res

    def _get_visit_domain(self):
        domain = super()._get_visit_domain()
        if self.patient_ids:
            domain.append(('patient_id', 'in', self.patient_ids.ids))
        if self.disease_id:
            domain.append(('disease_id', '=', self.disease_id.id))
        if self.only_done:
            domain.append(('state', '=', 'done'))
        return domain

    def action_show_visits(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Visits'),
            'res_model': 'hr.hospital.visit',
            'view_mode': 'list,form',
            'domain': self._get_visit_domain(),
        }
