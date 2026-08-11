from odoo import _, api, fields, models


class HrHospitalDoctorHistory(models.Model):
    """History line of a patient's personal doctor assignments."""

    _name = 'hr.hospital.doctor.history'
    _description = 'Personal Doctor History'
    _order = 'assign_date desc'

    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        string='Patient',
        required=True,
    )
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Doctor',
        required=True,
    )
    assign_date = fields.Date(
        string='Assignment Date',
        required=True,
        default=fields.Date.context_today,
    )
    change_date = fields.Date(string='Doctor Change Date')
    active = fields.Boolean(default=True)

    @api.onchange('assign_date', 'change_date')
    def _onchange_change_date(self):
        """Warn when the change date precedes the assignment date."""
        if self.assign_date and self.change_date and self.change_date < self.assign_date:
            return {
                'warning': {
                    'title': _('Invalid dates'),
                    'message': _('The doctor change date cannot be earlier than the assignment date.'),
                },
            }
        return None

    @api.depends('patient_id', 'doctor_id', 'doctor_id.category_id', 'assign_date')
    def _compute_display_name(self):
        """Format the name as patient - doctor (category) date."""
        for record in self:
            category = record.doctor_id.category_id.name or ''
            record.display_name = '%s - %s (%s) %s' % (
                record.patient_id.name or '',
                record.doctor_id.name or '',
                category,
                record.assign_date or '',
            )
