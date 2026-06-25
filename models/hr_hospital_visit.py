import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class HrHospitalVisit(models.Model):
    _name = 'hr.hospital.visit'
    _description = 'Patient Visit'
    _order = 'visit_date desc'

    name = fields.Char(
        string='Reference',
        compute='_compute_name',
        store=True,
    )
    active = fields.Boolean(default=True)
    visit_date = fields.Datetime(
        string='Visit Date',
        default=fields.Datetime.now,
    )
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
    disease_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string='Disease',
    )
    note = fields.Text(string='Note')

    @api.depends('patient_id', 'visit_date')
    def _compute_name(self):
        for visit in self:
            if visit.patient_id and visit.visit_date:
                visit.name = '%s — %s' % (
                    visit.patient_id.name,
                    fields.Datetime.to_string(visit.visit_date),
                )
            elif visit.patient_id:
                visit.name = visit.patient_id.name
            else:
                visit.name = _('New Visit')
