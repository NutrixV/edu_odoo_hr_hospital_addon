{
    "name": "HR Hospital",
    "summary": "Hospital management: doctors, patients, diseases and visits",
    "description": """
HR Hospital
===========

Module for hospital automation. Keeps records of:

* Doctors (with a supervising doctor)
* Patients
* Disease types
* Patient visits
""",
    "author": "Vitalii Sorokolit",
    "version": "19.0.1.0.0",
    "category": "Customization",
    "license": "OPL-1",
    "depends": ["base"],
    "external_dependencies": {"python": []},
    "data": [
        "security/ir.model.access.csv",
        "data/hr_hospital_disease_data.xml",
        "views/hr_hospital_menu.xml",
        "views/hr_hospital_doctor_views.xml",
        "views/hr_hospital_patient_views.xml",
        "views/hr_hospital_disease_views.xml",
        "views/hr_hospital_visit_views.xml",
    ],
    "demo": [
        "demo/hr_hospital_doctor_demo.xml",
        "demo/hr_hospital_patient_demo.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": [],
}
