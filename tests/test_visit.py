from datetime import datetime

from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestVisit(TransactionCase):
    def setUp(self):
        super().setUp()
        self.patient = self.env['hr.hospital.patient'].create({'name': 'Visit Patient'})
        self.doctor = self.env['hr.hospital.doctor'].create({'name': 'Visit Doctor'})
        self.visit = self.env['hr.hospital.visit'].create({
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id,
            'scheduled_date': datetime(2026, 1, 1, 10, 0),
            'state': 'done',
        })

    def test_cannot_change_doctor_of_done_visit(self):
        other_doctor = self.env['hr.hospital.doctor'].create({'name': 'Other Doctor'})
        with self.assertRaises(UserError):
            self.visit.doctor_id = other_doctor

    def test_cannot_change_dates_of_done_visit(self):
        with self.assertRaises(UserError):
            self.visit.scheduled_date = datetime(2026, 2, 1, 10, 0)

    def test_cannot_delete_done_visit(self):
        with self.assertRaises(UserError):
            self.visit.unlink()

    def test_cannot_archive_done_visit(self):
        with self.assertRaises(UserError):
            self.visit.active = False

    def test_cannot_cancel_done_visit(self):
        with self.assertRaises(UserError):
            self.visit.state = 'cancelled'

    def test_planned_visit_editable_and_deletable(self):
        visit = self.env['hr.hospital.visit'].create({
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id,
            'scheduled_date': datetime(2026, 3, 1, 12, 0),
        })
        visit.scheduled_date = datetime(2026, 3, 2, 12, 0)
        visit.unlink()

    def test_name_computed_from_patient_and_date(self):
        self.assertIn('Visit Patient', self.visit.name)
        self.assertIn('2026-01-01', self.visit.name)

    def _create_planned_visit(self):
        return self.env['hr.hospital.visit'].create({
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id,
            'scheduled_date': datetime(2026, 4, 1, 9, 0),
        })

    def test_mark_done_sets_state_and_actual_date(self):
        visit = self._create_planned_visit()
        visit.action_mark_done()
        self.assertEqual(visit.state, 'done')
        self.assertTrue(visit.actual_date)

    def test_mark_done_keeps_existing_actual_date(self):
        visit = self._create_planned_visit()
        visit.actual_date = datetime(2026, 4, 1, 9, 30)
        visit.action_mark_done()
        self.assertEqual(visit.actual_date, datetime(2026, 4, 1, 9, 30))

    def test_cancel_planned_visit(self):
        visit = self._create_planned_visit()
        visit.action_cancel()
        self.assertEqual(visit.state, 'cancelled')

    def test_cannot_mark_done_cancelled_visit(self):
        visit = self._create_planned_visit()
        visit.action_cancel()
        with self.assertRaises(UserError):
            visit.action_mark_done()

    def test_reset_cancelled_to_planned(self):
        visit = self._create_planned_visit()
        visit.action_cancel()
        visit.action_reset_to_planned()
        self.assertEqual(visit.state, 'planned')

    def test_cannot_reset_done_visit(self):
        with self.assertRaises(UserError):
            self.visit.action_reset_to_planned()

    def test_same_disease_count_and_action(self):
        disease = self.env['hr.hospital.disease'].create({'name': 'Test Disease'})
        self.env['hr.hospital.visit'].create([
            {
                'patient_id': self.patient.id,
                'doctor_id': self.doctor.id,
                'disease_id': disease.id,
            }
            for _dummy in range(2)
        ])
        visit = self.env['hr.hospital.visit'].create({
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id,
            'disease_id': disease.id,
        })
        self.assertEqual(visit.same_disease_visit_count, 3)
        action = visit.action_view_same_disease_visits()
        self.assertEqual(action['domain'], [('disease_id', '=', disease.id)])
