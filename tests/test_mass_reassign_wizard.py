from datetime import date

from odoo.tests.common import TransactionCase


class TestMassReassignWizard(TransactionCase):
    def setUp(self):
        super().setUp()
        self.old_doctor = self.env['hr.hospital.doctor'].create({'name': 'Old Doctor'})
        self.new_doctor = self.env['hr.hospital.doctor'].create({'name': 'New Doctor'})
        self.patient_1 = self.env['hr.hospital.patient'].create({
            'name': 'Patient One',
            'doctor_id': self.old_doctor.id,
        })
        self.history_line = self.env['hr.hospital.doctor.history'].create({
            'patient_id': self.patient_1.id,
            'doctor_id': self.old_doctor.id,
            'assign_date': date(2026, 1, 1),
        })
        self.patient_2 = self.env['hr.hospital.patient'].create({'name': 'Patient Two'})

    def _run_wizard(self, patients, **vals):
        wizard_model = self.env['hr.hospital.patient.reassign.doctor']
        wizard = wizard_model.with_context(active_ids=patients.ids).create({
            'doctor_id': self.new_doctor.id,
            'change_date': date(2026, 7, 1),
            **vals,
        })
        return wizard.action_apply()

    def test_reassigns_doctor(self):
        self._run_wizard(self.patient_1 | self.patient_2)
        self.assertEqual(self.patient_1.doctor_id, self.new_doctor)
        self.assertEqual(self.patient_2.doctor_id, self.new_doctor)

    def test_closes_open_history_line(self):
        self._run_wizard(self.patient_1)
        self.assertEqual(self.history_line.change_date, date(2026, 7, 1))

    def test_creates_new_active_history_line(self):
        self._run_wizard(self.patient_1)
        new_line = self.env['hr.hospital.doctor.history'].search([
            ('patient_id', '=', self.patient_1.id),
            ('change_date', '=', False),
        ])
        self.assertEqual(len(new_line), 1)
        self.assertEqual(new_line.doctor_id, self.new_doctor)
        self.assertEqual(new_line.assign_date, date(2026, 7, 1))

    def test_skips_patient_with_same_doctor(self):
        self.patient_2.doctor_id = self.new_doctor
        history_before = self.env['hr.hospital.doctor.history'].search_count([
            ('patient_id', '=', self.patient_2.id),
        ])
        self._run_wizard(self.patient_2)
        history_after = self.env['hr.hospital.doctor.history'].search_count([
            ('patient_id', '=', self.patient_2.id),
        ])
        self.assertEqual(history_before, history_after)
