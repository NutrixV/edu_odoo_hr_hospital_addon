from odoo.tests.common import TransactionCase


class TestDoctorReport(TransactionCase):
    def setUp(self):
        super().setUp()
        self.report = self.env['ir.actions.report']
        Patient = self.env['hr.hospital.patient']
        Visit = self.env['hr.hospital.visit']
        self.doctor_1 = self.env['hr.hospital.doctor'].create({
            'name': 'Alpha Doctor',
            'specialty': 'Cardiology',
        })
        self.doctor_2 = self.env['hr.hospital.doctor'].create({'name': 'Beta Doctor'})
        self.patient = Patient.create({
            'name': 'Gamma Patient',
            'doctor_id': self.doctor_1.id,
            'gender': 'female',
            'birthdate': '1990-05-01',
            'phone': '+380501112233',
        })
        self.visit_old = Visit.create({
            'doctor_id': self.doctor_1.id,
            'patient_id': self.patient.id,
            'scheduled_date': '2026-01-15 10:00:00',
        })
        self.visit_new = Visit.create({
            'doctor_id': self.doctor_1.id,
            'patient_id': self.patient.id,
            'scheduled_date': '2026-04-15 10:00:00',
        })
        self.visit_new.action_cancel()

    def _render(self, doctors):
        self.env.invalidate_all()
        html, _report_type = self.report._render_qweb_html(
            'hr_hospital_management.hr_hospital_doctor_report_pdf',
            doctors.ids,
        )
        return html.decode()

    def test_single_doctor_content(self):
        html = self._render(self.doctor_1)
        self.assertIn('Alpha Doctor', html)
        self.assertIn('Cardiology', html)
        self.assertIn('Gamma Patient', html)
        self.assertIn('+380501112233', html)

    def test_visits_newest_first(self):
        walkin = self.env['hr.hospital.patient'].create({'name': 'Zeta Walkin'})
        self.env['hr.hospital.visit'].create({
            'doctor_id': self.doctor_1.id,
            'patient_id': walkin.id,
            'scheduled_date': '2026-06-15 10:00:00',
        })
        html = self._render(self.doctor_1)
        self.assertLess(html.index('Zeta Walkin'), html.index('Gamma Patient'))

    def test_cancelled_state_colored(self):
        html = self._render(self.doctor_1)
        self.assertIn('o_hr_hospital_visit_state_cancelled', html)

    def test_multiple_doctors_one_article_each(self):
        html = self._render(self.doctor_1 | self.doctor_2)
        self.assertIn('Alpha Doctor', html)
        self.assertIn('Beta Doctor', html)
        self.assertEqual(html.count('class="article"'), 2)
