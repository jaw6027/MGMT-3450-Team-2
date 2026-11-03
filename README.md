# Saif Industries customer management and sales pipeline

Customer and membership management files for 45 prospective automotive businesses, with sales qualification, RFQ, quote, order, quality, and capacity tracking.

## Start here

- [Excel workbook](customer-management/saif_customer_management.xlsx): editable company directory, qualification and evidence sheets, sales pipeline, dashboard, and setup tasks.
- [SQLite database](customer-management/saif_customer_management.sqlite): relational version of the company and sales records.
- [Company CSV](customer-management/companies.csv): initial company directory for import.
- [Capability-sheet template](customer-management/capability-sheet-template.md).
- [Buyer discovery questions and outreach drafts](customer-management/buyer-discovery-and-outreach.md).
- [Pipeline playbook](customer-management/pipeline-playbook.md).
- [Database documentation](customer-management/README.md).

## Current status

All 45 businesses are unverified prospects. Earlier rankings are preliminary estimates, not confirmed purchasing demand. Contact names, phones, emails and street addresses are unknown unless later verified and entered. No CNC outsourcing arrangements, RFQs, quotes, orders, memberships or customer outreach have been represented as completed.

Saif's actual machining capabilities and accessible source evidence are needed to qualify prospects. See the [qualification status report](customer-management/qualification-status.md) for the current blockers and evidence standards. Environment access draft settings referenced in that report belong to the cloud setup, not a configuration automatically applied by this repository.

The workbook, SQLite database, and CSV are separate copies; edits do not synchronize automatically. Select one working source of truth. Excel calculates workbook formulas when opened.

## Reproduction

The checked-in artifacts are ready to open. To reproduce the initial versions in a **new, empty output directory**, copy the three Python scripts there, install `openpyxl` in your chosen Python environment, and run:

```sh
python3 build_database.py
python3 prepare_qualification.py
python3 extend_sales_pipeline.py
```

Python's standard library supplies SQLite support. The scripts refuse to overwrite key existing artifacts. Do not run them in the checked-in data directory expecting them to refresh customer edits. Local backup folders and SQLite temporary files are ignored.
