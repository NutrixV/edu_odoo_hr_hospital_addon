from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestDisease(TransactionCase):
    def test_hierarchical_display_name(self):
        parent = self.env['hr.hospital.disease'].create({'name': 'Respiratory'})
        child = self.env['hr.hospital.disease'].create({
            'name': 'Flu',
            'parent_id': parent.id,
        })
        grandchild = self.env['hr.hospital.disease'].create({
            'name': 'H1N1',
            'parent_id': child.id,
        })
        self.assertEqual(child.display_name, 'Respiratory / Flu')
        self.assertEqual(grandchild.display_name, 'Respiratory / Flu / H1N1')

    def test_display_name_updates_on_parent_rename(self):
        parent = self.env['hr.hospital.disease'].create({'name': 'Old Name'})
        child = self.env['hr.hospital.disease'].create({
            'name': 'Child',
            'parent_id': parent.id,
        })
        parent.name = 'New Name'
        self.assertEqual(child.display_name, 'New Name / Child')

    def test_cycle_forbidden(self):
        parent = self.env['hr.hospital.disease'].create({'name': 'A'})
        child = self.env['hr.hospital.disease'].create({
            'name': 'B',
            'parent_id': parent.id,
        })
        with self.assertRaises(ValidationError):
            parent.parent_id = child
