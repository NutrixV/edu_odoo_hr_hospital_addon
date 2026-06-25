import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class HrHospitalDisease(models.Model):
    _name = "hr.hospital.disease"
    _description = "Disease"

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(default=True)
    description = fields.Text(string="Description")
    parent_id = fields.Many2one(
        comodel_name="hr.hospital.disease",
        string="Parent Disease",
    )
