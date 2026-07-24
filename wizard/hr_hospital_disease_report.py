from odoo import _, fields, models


class HrHospitalDiseaseReport(models.TransientModel):
    """Wizard reporting visits grouped by disease for a period."""

    _name = 'hr.hospital.disease.report'
    _inherit = ['hr.hospital.visit.report.mixin']
    _description = 'Disease Report'

    doctor_ids = fields.Many2many(
        help='Leave empty to include all doctors.',
    )
    disease_ids = fields.Many2many(
        comodel_name='hr.hospital.disease',
        string='Diseases',
        help='Leave empty to include all diseases.',
    )
    date_from = fields.Date(
        default=lambda self: fields.Date.context_today(self).replace(day=1),
    )
    date_to = fields.Date(
        default=fields.Date.context_today,
    )

    def _get_visit_domain(self):
        """Extend the domain with the disease filter."""
        domain = super()._get_visit_domain()
        if self.disease_ids:
            domain.append(('disease_id', 'in', self.disease_ids.ids))
        return domain

    def action_show_visits(self):
        """Open the filtered visit list grouped by disease."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Visits by Disease'),
            'res_model': 'hr.hospital.visit',
            'view_mode': 'list,form',
            'domain': self._get_visit_domain(),
            'context': {'group_by': 'disease_id'},
        }

    def action_print_pdf(self):
        """Render the disease report as PDF."""
        self.ensure_one()
        return self.env.ref(
            'hr_hospital.hr_hospital_disease_report_pdf',
        ).report_action(self)
