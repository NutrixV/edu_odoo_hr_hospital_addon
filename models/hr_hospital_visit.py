import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class HrHospitalVisit(models.Model):
    _name = "hr.hospital.visit"
    _description = "Patient Visit"

    name = fields.Char(string="Reference")
    active = fields.Boolean(default=True)
    visit_date = fields.Datetime(
        string="Visit Date",
        default=fields.Datetime.now,
    )
    patient_id = fields.Many2one(
        comodel_name="hr.hospital.patient",
        string="Patient",
        required=True,
    )
    doctor_id = fields.Many2one(
        comodel_name="hr.hospital.doctor",
        string="Doctor",
        required=True,
    )
    disease_id = fields.Many2one(
        comodel_name="hr.hospital.disease",
        string="Disease",
    )
    note = fields.Text(string="Note")
