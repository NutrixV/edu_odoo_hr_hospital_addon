import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class HrHospitalDoctor(models.Model):
    _name = "hr.hospital.doctor"
    _description = "Doctor"

    name = fields.Char(string="Full Name", required=True)
    active = fields.Boolean(default=True)
    specialty = fields.Char(string="Specialty")
    phone = fields.Char(string="Phone")
    mentor_id = fields.Many2one(
        comodel_name="hr.hospital.doctor",
        string="Supervising Doctor",
    )
