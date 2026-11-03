# Saif Industries customer and membership management

The database contains 45 unique prospective businesses from the conversation: the original 25 and 20 additional businesses identified as outside California. All records are unverified. Websites and recorded locations were transcribed, not checked online. Suggested contact roles are not verified individuals. Potential CNC work is a sales hypothesis, not evidence of outsourcing demand.

## Files

- `saif_customer_management.xlsx`: editable workbook with filterable company records, clickable websites, status dropdowns, and separate Contacts, Interactions, Follow-ups, and Memberships sheets. Start here for spreadsheet use.
- `saif_customer_management.sqlite`: relational database for use with SQLite-compatible tools. Includes company records and empty tables for contacts, interactions, follow-ups, and memberships.
- `companies.csv`: spreadsheet/CRM import of the initial 45 company records, encoded as UTF-8 with a BOM.
- `build_database.py`: generation script. Requires Python 3 and openpyxl for Excel output. Refuses to overwrite an existing database so it cannot silently erase edits.

These are separate copies of the initial dataset. Editing the spreadsheet, database, or CSV does not update the other files automatically. Choose one as your working source of truth.

## What is populated

Company name, website, original cohort and rank, estimated prospect tier, any previously supplied city/state, suggested contact role, and potential CNC work. Ranks apply within each cohort; a combined 1–45 strength ranking was never established. Unknown names, phones, emails, street addresses, postal codes, and dates are blank/NULL. All companies start as `Prospect` and `Not enrolled`. No outreach or membership has been invented.

## Updating records

1. Verify each company's website and location before outreach. Record the source and verification date when adding contacts.
2. Keep company IDs stable; use them to connect entries across tables or worksheets.
3. Record actual calls, emails, and meetings in Interactions. Record due dates and owners in Follow-ups.
4. Create a Memberships record only after actual enrollment terms exist. Membership fees, plans, and renewal dates are intentionally empty.
5. Maintain company summary fields (`last_contact_date`, `next_follow_up`, `lifecycle_status`, `membership_status`) when related records change. They are manually maintained, not automatically synchronized.
6. Use ISO dates (`YYYY-MM-DD`). Back up the working file before bulk edits.

## SQLite use

Enable `PRAGMA foreign_keys = ON` for every editing connection. Tables use company IDs as foreign keys. `prospect_directory` displays the company lists in their original order; `open_follow_ups` shows outstanding follow-up tasks ordered by due date.

Example read-only Python query:

```python
import sqlite3
db = sqlite3.connect('file:saif_customer_management.sqlite?mode=ro', uri=True)
for row in db.execute('SELECT company_name, website_url, state FROM prospect_directory'):
    print(row)
db.close()
```

This is a local database and workbook, not a hosted multi-user service. No external CRM was updated and no messages were sent.

## Sales pipeline extension

The workbook now includes Pipeline, Opportunities, RFQs, Quotes, Orders, Quality, Capacity, Setup tasks and Dashboard. The SQLite database has corresponding relational tables and quote/order calculation views. All 45 companies remain at Prospect; transaction tables are empty. See [pipeline-playbook.md](pipeline-playbook.md) for stage gates, metric definitions and operating instructions, [capability-sheet-template.md](capability-sheet-template.md) for the factual capability profile, and [buyer-discovery-and-outreach.md](buyer-discovery-and-outreach.md) for unsent drafts. Complete the 10 Setup tasks with actual evidence before advancing stages.
