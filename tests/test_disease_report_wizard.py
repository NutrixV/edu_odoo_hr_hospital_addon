from datetime import date

from odoo import Command
from odoo.tests.common import TransactionCase


class TestDiseaseReportWizard(TransactionCase):
    def setUp(self):
        super().setUp()
        self.doctor = self.env['hr.hospital.doctor'].create({'name': 'Report Doc'})
        self.wizard_model = self.env['hr.hospital.disease.report']

    def test_default_get_fills_doctors_from_context(self):
        wizard = self.wizard_model.with_context(
            active_model='hr.hospital.doctor',
            active_ids=[self.doctor.id],
        ).create({})
        self.assertEqual(wizard.doctor_ids, self.doctor)

    def test_empty_doctors_means_all(self):
        wizard = self.wizard_model.create({
            'date_from': False,
            'date_to': False,
        })
        action = wizard.action_show_visits()
        self.assertEqual(action['domain'], [])
        self.assertEqual(action['context'], {'group_by': 'disease_id'})

    def test_domain_filters_period_and_disease(self):
        disease = self.env['hr.hospital.disease'].create({'name': 'Report Disease'})
        wizard = self.wizard_model.create({
            'disease_ids': [Command.link(disease.id)],
            'date_from': date(2026, 7, 1),
            'date_to': date(2026, 7, 31),
        })
        domain = wizard.action_show_visits()['domain']
        self.assertIn(('disease_id', 'in', [disease.id]), domain)
        self.assertIn(('scheduled_date', '>=', date(2026, 7, 1)), domain)
        self.assertIn(('scheduled_date', '<', date(2026, 8, 1)), domain)

    def test_report_values_grouped_by_disease(self):
        patient = self.env['hr.hospital.patient'].create({'name': 'PDF Patient'})
        disease_a = self.env['hr.hospital.disease'].create({'name': 'PDF Disease A'})
        disease_b = self.env['hr.hospital.disease'].create({'name': 'PDF Disease B'})
        self.env['hr.hospital.visit'].create([
            {
                'patient_id': patient.id,
                'doctor_id': self.doctor.id,
                'disease_id': disease.id,
            }
            for disease in (disease_a, disease_a, disease_b)
        ])
        wizard = self.wizard_model.create({
            'disease_ids': [Command.set((disease_a | disease_b).ids)],
            'date_from': False,
            'date_to': False,
        })
        values = self.env[
            'report.hr_hospital_management.report_disease_visits'
        ]._get_report_values(wizard.ids)
        self.assertEqual(values['docs'], wizard)
        groups = values['reports'][0]['disease_groups']
        counts = {group['disease']: len(group['visits']) for group in groups}
        self.assertEqual(counts, {disease_a: 2, disease_b: 1})
