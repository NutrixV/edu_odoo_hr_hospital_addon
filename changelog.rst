Changelog
=========

19.0.5.1.0 (2026-07)
--------------------

* Technical name changed from ``hr_hospital`` to ``hr_hospital_management``
  (``hr_hospital`` is reserved on the Odoo Apps Store by another account).
  Model names, database tables and the display name are unchanged.
* Relicensed from OPL-1 to LGPL-3.
* Odoo Apps packaging: ``website``, ``support`` and ``maintainer`` keys,
  ``Human Resources`` category, flagged as an application, banner as the
  primary store image.
* Report styles moved from inline attributes to a ``web.report_assets_common``
  asset bundle.
* New module icon and matching store banner.

19.0.5.0.0 (2026-07)
--------------------

* Hospital security groups (Patient, Intern, Doctor, Manager,
  Administrator) with ACLs and record rules on visits.
* System user link on patients, demo users per role.
* Translatable disease classifier, updated Ukrainian translation.
* Docstrings, README, changelog and module description page.

19.0.4.0.0 (2026-07)
--------------------

* Printable PDF report for doctors (print menu, one doctor per page).
* Extended doctor kanban card with qualification, interns and menu.

19.0.3.0.0 (2026-07)
--------------------

* Search views, pivot and graph views, kanban for doctors.
* Quick visit creation, mass doctor reassign wizard.
* Visit and disease report wizards with PDF output.

19.0.2.0.0 (2026-06)
--------------------

* Doctor categories, personal doctor history, medical info mixin.
* Visit workflow constraints and demo data.

19.0.1.0.0 (2026-06)
--------------------

* Initial module: doctors, patients, diseases, visits.
