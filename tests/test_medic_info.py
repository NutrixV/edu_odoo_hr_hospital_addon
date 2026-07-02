from odoo.tests.common import TransactionCase


class TestMedicMixin(TransactionCase):
    def test_mixin_registered(self):
        self.assertIn('hr.hospital.medic.mixin', self.env)
        self.assertTrue(self.env['hr.hospital.medic.mixin']._abstract)
