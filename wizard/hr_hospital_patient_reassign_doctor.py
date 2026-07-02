from odoo import fields, models


class HrHospitalPatientReassignDoctor(models.TransientModel):
    _name = 'hr.hospital.patient.reassign.doctor'
    _description = 'Mass Reassign Personal Doctor'

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='New Doctor',
        required=True,
    )
    change_date = fields.Date(default=fields.Date.context_today)

    def action_apply(self):
        self.ensure_one()
        history_model = self.env['hr.hospital.doctor.history']
        patients = self.env['hr.hospital.patient'].browse(
            self.env.context.get('active_ids', []),
        )
        for patient in patients:
            if patient.doctor_id == self.doctor_id:
                continue
            open_lines = history_model.search([
                ('patient_id', '=', patient.id),
                ('change_date', '=', False),
            ])
            open_lines.change_date = self.change_date
            history_model.create({
                'patient_id': patient.id,
                'doctor_id': self.doctor_id.id,
                'assign_date': self.change_date,
            })
            patient.doctor_id = self.doctor_id
        return {'type': 'ir.actions.act_window_close'}
