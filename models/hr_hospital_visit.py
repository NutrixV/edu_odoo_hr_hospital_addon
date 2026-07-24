from odoo import _, api, fields, models
from odoo.exceptions import UserError


class HrHospitalVisit(models.Model):
    """Patient visit to a doctor."""

    _name = 'hr.hospital.visit'
    _description = 'Patient Visit'
    _order = 'scheduled_date desc'

    name = fields.Char(
        string='Reference',
        compute='_compute_name',
        store=True,
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('planned', 'Planned'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='planned',
        required=True,
    )
    scheduled_date = fields.Datetime(
        string='Scheduled',
        default=fields.Datetime.now,
    )
    actual_date = fields.Datetime(string='Occurred At')
    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        required=True,
    )
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        required=True,
    )
    disease_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
    )
    summary = fields.Html(string='Summary / Epicrisis')
    note = fields.Text()

    same_disease_visit_count = fields.Integer(
        string='Same Disease Visits',
        compute='_compute_same_disease_visit_count',
    )

    @api.depends('disease_id.visit_ids')
    def _compute_same_disease_visit_count(self):
        """Count visits sharing this visit's disease."""
        for visit in self:
            visit.same_disease_visit_count = len(visit.disease_id.visit_ids)

    @api.model
    def _get_quick_visit_action(self, defaults):
        """Return an action opening a new visit form with defaults."""
        return {
            'type': 'ir.actions.act_window',
            'name': _('New Visit'),
            'res_model': 'hr.hospital.visit',
            'view_mode': 'form',
            'target': 'new',
            'context': defaults,
        }

    def action_view_same_disease_visits(self):
        """Open visits having the same disease."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Visits: %s') % self.disease_id.display_name,
            'res_model': 'hr.hospital.visit',
            'view_mode': 'list,form',
            'domain': [('disease_id', '=', self.disease_id.id)],
        }

    @api.depends('patient_id', 'scheduled_date')
    def _compute_name(self):
        """Compose the reference from the patient name and scheduled date."""
        for visit in self:
            if visit.patient_id and visit.scheduled_date:
                visit.name = '%s — %s' % (
                    visit.patient_id.name,
                    fields.Datetime.to_string(visit.scheduled_date),
                )
            elif visit.patient_id:
                visit.name = visit.patient_id.name
            else:
                visit.name = _('New Visit')

    def _is_done(self):
        """Return True when the visit is completed."""
        self.ensure_one()
        return self.state == 'done'

    def action_mark_done(self):
        """Mark planned visits as done, stamping the actual date if empty."""
        if any(visit.state != 'planned' for visit in self):
            raise UserError(_('Only a planned visit can be marked as done.'))
        without_date = self.filtered(lambda visit: not visit.actual_date)
        without_date.write({
            'state': 'done',
            'actual_date': fields.Datetime.now(),
        })
        (self - without_date).write({'state': 'done'})
        return True

    def action_cancel(self):
        """Cancel planned visits."""
        if any(visit.state != 'planned' for visit in self):
            raise UserError(_('Only a planned visit can be cancelled.'))
        self.write({'state': 'cancelled'})
        return True

    def action_reset_to_planned(self):
        """Return cancelled visits to the planned state."""
        if any(visit.state != 'cancelled' for visit in self):
            raise UserError(_('Only a cancelled visit can be reset to planned.'))
        self.write({'state': 'planned'})
        return True

    def write(self, vals):
        """Protect completed visits from date, doctor and archiving changes."""
        protected = {'scheduled_date', 'actual_date', 'doctor_id'}
        if protected & set(vals):
            for visit in self:
                if visit._is_done():
                    raise UserError(_('You cannot change date/time or doctor of a completed visit.'))
        if vals.get('active') is False or vals.get('state') == 'cancelled':
            for visit in self:
                if visit._is_done():
                    raise UserError(_('You cannot archive or cancel a completed visit.'))
        return super().write(vals)

    def unlink(self):
        """Forbid deleting completed visits."""
        for visit in self:
            if visit._is_done():
                raise UserError(_('You cannot delete a completed visit.'))
        return super().unlink()
