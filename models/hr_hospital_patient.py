import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class HrHospitalPatient(models.Model):
    _name = "hr.hospital.patient"
    _description = "Patient"

    name = fields.Char(string="Full Name", required=True)
    active = fields.Boolean(default=True)
    birthdate = fields.Date(string="Date of Birth")
    gender = fields.Selection(
        selection=[
            ("male", "Male"),
            ("female", "Female"),
            ("other", "Other"),
        ],
        string="Gender",
    )
    phone = fields.Char(string="Phone")
    doctor_id = fields.Many2one(
        comodel_name="hr.hospital.doctor",
        string="Personal Doctor",
    )
