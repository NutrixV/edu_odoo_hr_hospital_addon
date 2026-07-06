from datetime import date, datetime

from odoo.tests.common import TransactionCase


class TestVisitReportWizard(TransactionCase):
    def setUp(self):
        super().setUp()
        self.doctor = self.env['hr.hospital.doctor'].create({'name': 'Report Doctor'})
        self.patient = self.env['hr.hospital.patient'].create({'name': 'Report Patient'})
        self.done_visit = self.env['hr.hospital.visit'].create({
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id,
            'scheduled_date': datetime(2026, 5, 10, 10, 0),
            'state': 'done',
        })
        self.planned_visit = self.env['hr.hospital.visit'].create({
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id,
            'scheduled_date': datetime(2026, 5, 20, 15, 30),
        })
        self.Wizard = self.env['hr.hospital.visit.report']

    def test_default_get_fills_doctors(self):
        wizard = self.Wizard.with_context(
            active_model='hr.hospital.doctor',
            active_ids=[self.doctor.id],
        ).create({})
        self.assertEqual(wizard.doctor_ids, self.doctor)

    def test_default_get_fills_patients(self):
        wizard = self.Wizard.with_context(
            active_model='hr.hospital.patient',
            active_ids=[self.patient.id],
        ).create({})
        self.assertEqual(wizard.patient_ids, self.patient)

    def test_domain_filters_only_done(self):
        wizard = self.Wizard.create({'only_done': True})
        domain = wizard.action_show_visits()['domain']
        visits = self.env['hr.hospital.visit'].search(domain)
        self.assertIn(self.done_visit, visits)
        self.assertNotIn(self.planned_visit, visits)

    def test_domain_includes_last_day_of_period(self):
        wizard = self.Wizard.create({
            'date_from': date(2026, 5, 1),
            'date_to': date(2026, 5, 20),
        })
        domain = wizard.action_show_visits()['domain']
        visits = self.env['hr.hospital.visit'].search(domain)
        self.assertIn(self.done_visit, visits)
        # 2026-05-20 15:30 has to be included although date_to is 2026-05-20
        self.assertIn(self.planned_visit, visits)

    def test_action_returns_visit_list(self):
        wizard = self.Wizard.create({})
        action = wizard.action_show_visits()
        self.assertEqual(action['res_model'], 'hr.hospital.visit')
        self.assertEqual(action['type'], 'ir.actions.act_window')
