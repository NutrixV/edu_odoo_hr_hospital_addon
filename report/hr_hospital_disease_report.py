from odoo import api, models


class ReportDiseaseVisits(models.AbstractModel):
    _name = 'report.hr_hospital.report_disease_visits'
    _description = 'Disease Report PDF'

    @api.model
    def _get_report_values(self, docids, data=None):
        wizards = self.env['hr.hospital.disease.report'].browse(docids)
        reports = []
        for wizard in wizards:
            visits = self.env['hr.hospital.visit'].search(
                wizard._get_visit_domain(),
                order='disease_id, scheduled_date',
            )
            reports.append({
                'wizard': wizard,
                'disease_groups': [
                    {'disease': disease, 'visits': disease_visits}
                    for disease, disease_visits in visits.grouped('disease_id').items()
                ],
            })
        return {
            'doc_ids': docids,
            'doc_model': 'hr.hospital.disease.report',
            'docs': wizards,
            'reports': reports,
        }
