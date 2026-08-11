from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class HrHospitalDisease(models.Model):
    """Hierarchical disease classifier."""

    _name = 'hr.hospital.disease'
    _description = 'Disease'
    _parent_name = 'parent_id'
    _order = 'name'

    name = fields.Char(required=True, translate=True)
    active = fields.Boolean(default=True)
    description = fields.Text(translate=True)
    parent_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string='Parent Disease',
    )
    complete_name = fields.Char(
        string='Complete Name',
        compute='_compute_complete_name',
        recursive=True,
        store=True,
    )
    visit_ids = fields.One2many(
        comodel_name='hr.hospital.visit',
        inverse_name='disease_id',
        string='Visits',
    )

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        """Build the full path name from the parent chain."""
        for disease in self:
            if disease.parent_id:
                disease.complete_name = '%s / %s' % (disease.parent_id.complete_name, disease.name)
            else:
                disease.complete_name = disease.name or ''

    @api.depends('complete_name')
    def _compute_display_name(self):
        """Use the hierarchical complete name as display name."""
        for disease in self:
            disease.display_name = disease.complete_name

    @api.constrains('parent_id')
    def _check_parent_id(self):
        """Forbid cycles in the disease hierarchy."""
        if self._has_cycle():
            raise ValidationError(_('A disease cannot be its own parent (recursive hierarchy).'))
