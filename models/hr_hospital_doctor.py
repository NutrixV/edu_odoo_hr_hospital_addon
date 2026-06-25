import logging

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class HrHospitalDoctor(models.Model):
    _name = "hr.hospital.doctor"
    _description = "Doctor"
    _order = "name"

    name = fields.Char(string="Full Name", required=True)
    active = fields.Boolean(default=True)
    specialty = fields.Char(string="Specialty")
    phone = fields.Char(string="Phone")
    mentor_id = fields.Many2one(
        comodel_name="hr.hospital.doctor",
        string="Supervising Doctor",
    )

    @api.constrains("mentor_id")
    def _check_mentor_id(self):
        if self._has_cycle("mentor_id"):
            raise ValidationError(
                _("A doctor cannot be their own supervisor (recursive chain).")
            )
