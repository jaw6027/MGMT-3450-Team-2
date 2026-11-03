from pathlib import Path
import csv
import json
import sqlite3
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = Path(__file__).resolve().parent
# Data transcribed from this conversation. No live contact verification performed.
DATA = '''TOTAL CHAOS Fabrication|https://www.chaosfab.com/|Corona|California|Purchasing / production|Suspension spacers, sleeves, mounting hardware, prototypes
Solo Motorsports|https://solomotorsports.com/|Covina|California|Owner / shop manager|Long-travel suspension spacers, adapters, mounting components
JD Fabrication|https://jdfabrication.com/|Escondido|California|Owner / production|Suspension kit components and custom-build parts
Baja Kits|https://www.bajakits.com/|||Purchasing / manufacturing|Suspension bushings, spacers, adapters, prototypes
Metal Tech 4x4|https://metaltech4x4.com/|||Owner / product development|Suspension adapters, mounting blocks, accessory hardware
WFO Concepts|https://www.wfoconcepts.com/|||Owner / shop manager|Steering adapters, suspension sleeves, spacers
Front Range Off-Road Fabrication|https://frontrangeoffroadfab.com/|||Owner / operations|Drivetrain adapters, sleeves, specialty Toyota components
4x Innovations|https://www.4xinnovations.com/|||Owner / production|Machined inserts, mounting components, off-road hardware
Clayton Off Road|https://www.claytonoffroad.com/|||Purchasing / operations|Suspension sleeves, spacers, adapters, prototypes
JKS Manufacturing|https://jksmfg.com/|||Supplier sourcing|Suspension bushings, sleeves, spacers, mounting hardware
Camburg Engineering|https://camburg.com/|Huntington Beach|California|Purchasing / manufacturing|Suspension components, spacers, overflow machining
Carli Suspension|https://www.carlisuspension.com/|||Purchasing / production|Suspension hardware, adapters, prototypes
Synergy Manufacturing|https://www.synergymfg.com/|||Purchasing / manufacturing|Steering and suspension sleeves, spacers, adapters
ICON Vehicle Dynamics|https://www.iconvehicledynamics.com/|Riverside|California|Supply chain / sourcing|Shock components, mounting hardware, development parts
Currie Enterprises|https://www.currieenterprises.com/|Corona|California|Purchasing / manufacturing|Driveline spacers, adapters, fixtures, prototypes
CST Performance Suspension|https://cstsuspension.com/|Moreno Valley|California|Purchasing / operations|Lift-kit spacers, sleeves, mounting components
Supreme Suspensions|https://supremesuspensions.com/|Los Angeles area|California|Product sourcing|Aluminum spacers, leveling-kit components, adapters
ReadyLIFT|https://www.readylift.com/|||Supplier sourcing|Leveling components, spacers, prototypes
Fabtech|https://fabtechmotorsports.com/|||Purchasing / production|Suspension spacers, sleeves, mounting hardware, fixtures
BDS Suspension|https://bds-suspension.com/|||Supplier sourcing|Suspension hardware, development parts, fixtures
McGaughy's Suspension|https://mcgaughys.com/|Fresno|California|Manufacturing / purchasing|Overflow machining, fixtures, prototypes
BuiltRight Industries|https://builtrightind.com/|||Operations / manufacturing|Accessory mounting adapters, development parts, overflow
Billet Specialties|https://www.billetspecialties.com/|||Manufacturing / purchasing|Specialized overflow machining and tooling
Mishimoto|https://www.mishimoto.com/|||Supplier sourcing / product engineering|Cooling adapters, sensor fittings, prototype housings
Holley|https://www.holley.com/|||Strategic sourcing|Prototype brackets, adapters, fixtures, specialty parts
Rock Krawler Suspension|https://rockkrawler.com/||New York|Purchasing / production|Suspension sleeves, spacers, adapters, prototypes
Iron Rock Off Road|https://www.ironrockoffroad.com/||Minnesota|Purchasing / production|Suspension hardware, bushings, spacers, adapters
Rusty's Off-Road|https://www.rustysoffroad.com/||Alabama|Owner / purchasing|Suspension sleeves, steering adapters, mounting components
CavFab|https://cavfab.com/||Kentucky|Owner / production|Machined inserts, suspension spacers, steering components
Wide Open Design|https://www.wideopendesign.com/||Tennessee|Owner / production|Drivetrain adapters, suspension hardware, prototypes
Mountain Off Road Enterprises (M.O.R.E.)|https://mountainoffroad.com/||Colorado|Purchasing / production|Mounting blocks, spacers, sleeves, specialty hardware
Offroad Design|https://www.offroaddesign.com/||Colorado|Owner / purchasing|Drivetrain adapters, suspension bushings, hardware
Motobilt|https://motobilt.com/||Alabama|Purchasing / manufacturing|Components for fabricated assemblies, fixtures, overflow
Barnes 4WD|https://barnes4wd.com/||North Carolina|Purchasing / production|Suspension inserts, threaded adapters, sleeves, spacers
Artec Industries|https://www.artecindustries.com/||Utah|Purchasing / manufacturing|Machined inserts, mounting components, fixtures
Rock Hard 4x4|https://www.rockhard4x4.com/||Nebraska|Purchasing / production|Accessory hardware, spacers, machined inserts
JcrOffroad|https://www.jcroffroad.com/||Michigan|Purchasing / manufacturing|Accessory adapters, mounting blocks, fixtures
Ballistic Fabrication|https://www.ballisticfabrication.com/||Arizona|Purchasing / manufacturing|Suspension adapters, threaded inserts, overflow
Novak Conversions|https://www.novak-adapt.com/||Utah|Purchasing / manufacturing|Drivetrain adapters, housings, conversion prototypes
JB Conversions|https://www.jbconversions.com/||Louisiana|Purchasing / manufacturing|Drivetrain components, adapters, tooling
UMI Performance|https://www.umiperformance.com/||Pennsylvania|Purchasing / manufacturing|Suspension sleeves, spacers, mounting components, fixtures
BMR Suspension|https://www.bmrsuspension.com/||Florida|Purchasing / manufacturing|Suspension bushings, spacers, hardware, prototypes
TeraFlex|https://teraflex.com/||Utah|Supplier sourcing / manufacturing|Suspension hardware, prototypes, overflow machining
Detroit Speed|https://www.detroitspeed.com/||North Carolina|Purchasing / manufacturing|Suspension development parts, adapters, fixtures
American Expedition Vehicles (AEV)|https://www.aev-conversions.com/||Michigan|Supplier sourcing / engineering|Accessory adapters, mounting components, development parts'''

records = []
for i, line in enumerate(DATA.splitlines(), 1):
    name, url, city, state, role, opportunity = line.split('|')
    original = i <= 25
    tier = ('Extremely strong' if i <= 10 else 'Strong' if i <= 15 else
            'Likely fit' if i <= 20 else 'Additional') if original else 'Additional - outside California'
    records.append(dict(company_id=i, company_name=name, cohort='Original 25' if original else 'Additional outside California',
        cohort_rank=i if original else i-25, prospect_tier=tier, website_url=url,
        street_address=None, city=city or None, state=state or None, postal_code=None, country='United States',
        phone=None, contact_name=None, contact_role_to_request=role, email=None,
        potential_cnc_work=opportunity, lifecycle_status='Prospect', membership_status='Not enrolled',
        assigned_to=None, last_contact_date=None, next_follow_up=None, verification_status='Unverified',
        source='Conversation prospect list; not independently verified',
        notes='Ranking is preliminary product fit, not confirmed demand. Role is suggested, not a verified person.'))

db_path = ROOT / 'saif_customer_management.sqlite'
if db_path.exists():
    raise SystemExit('Database already exists. Refusing to overwrite customer edits.')
con = sqlite3.connect(db_path)
con.execute('PRAGMA foreign_keys = ON')
con.executescript('''
CREATE TABLE companies (
 company_id INTEGER PRIMARY KEY, company_name TEXT NOT NULL UNIQUE,
 cohort TEXT NOT NULL, cohort_rank INTEGER NOT NULL CHECK(cohort_rank > 0),
 prospect_tier TEXT NOT NULL, website_url TEXT, street_address TEXT, city TEXT,
 state TEXT, postal_code TEXT, country TEXT, phone TEXT, contact_name TEXT,
 contact_role_to_request TEXT, email TEXT, potential_cnc_work TEXT,
 lifecycle_status TEXT NOT NULL DEFAULT 'Prospect'
 CHECK(lifecycle_status IN ('Prospect','Contacted','Qualified','Quoted','Customer','Not a fit','Do not contact')),
 membership_status TEXT NOT NULL DEFAULT 'Not enrolled'
 CHECK(membership_status IN ('Not enrolled','Pending','Active','Paused','Expired','Cancelled')),
 assigned_to TEXT, last_contact_date TEXT, next_follow_up TEXT,
 verification_status TEXT NOT NULL DEFAULT 'Unverified'
 CHECK(verification_status IN ('Unverified','Partially verified','Verified')),
 source TEXT, notes TEXT, UNIQUE(cohort, cohort_rank)
);
CREATE TABLE contacts (
 contact_id INTEGER PRIMARY KEY, company_id INTEGER NOT NULL REFERENCES companies(company_id),
 full_name TEXT NOT NULL, job_title TEXT, email TEXT, phone TEXT,
 is_primary INTEGER NOT NULL DEFAULT 0 CHECK(is_primary IN (0,1)),
 verification_status TEXT NOT NULL DEFAULT 'Unverified', source_url TEXT, verified_on TEXT, notes TEXT
);
CREATE TABLE interactions (
 interaction_id INTEGER PRIMARY KEY, company_id INTEGER NOT NULL REFERENCES companies(company_id),
 contact_id INTEGER REFERENCES contacts(contact_id), occurred_at TEXT NOT NULL,
 channel TEXT CHECK(channel IN ('Phone','Email','Meeting','Website','Other')),
 summary TEXT NOT NULL, outcome TEXT, recorded_by TEXT
);
CREATE TABLE follow_ups (
 follow_up_id INTEGER PRIMARY KEY, company_id INTEGER NOT NULL REFERENCES companies(company_id),
 due_date TEXT NOT NULL, task TEXT NOT NULL, assigned_to TEXT,
 status TEXT NOT NULL DEFAULT 'Open' CHECK(status IN ('Open','Completed','Cancelled')),
 completed_at TEXT, notes TEXT
);
CREATE TABLE memberships (
 membership_id INTEGER PRIMARY KEY, company_id INTEGER NOT NULL REFERENCES companies(company_id),
 plan_name TEXT NOT NULL, status TEXT NOT NULL CHECK(status IN ('Pending','Active','Paused','Expired','Cancelled')),
 start_date TEXT, renewal_date TEXT, end_date TEXT, fee_amount REAL CHECK(fee_amount >= 0),
 currency TEXT, notes TEXT
);
CREATE TABLE metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE INDEX idx_companies_state ON companies(state);
CREATE INDEX idx_companies_follow_up ON companies(next_follow_up);
CREATE INDEX idx_follow_ups_due ON follow_ups(status, due_date);
CREATE VIEW prospect_directory AS SELECT * FROM companies ORDER BY
 CASE cohort WHEN 'Original 25' THEN 0 ELSE 1 END, cohort_rank;
CREATE VIEW open_follow_ups AS SELECT f.*, c.company_name FROM follow_ups f
 JOIN companies c USING(company_id) WHERE f.status='Open' ORDER BY f.due_date;
''')
columns = list(records[0])
con.executemany('INSERT INTO companies (' + ','.join(columns) + ') VALUES (' + ','.join('?' for _ in columns) + ')',
                [[r[c] for c in columns] for r in records])
con.executemany('INSERT INTO metadata VALUES (?,?)', [
    ('source','User conversation; websites, locations, rankings and demand not independently verified'),
    ('missing_data','NULL means unknown, not verified, or not yet recorded'),
    ('ranking','Ranks apply within each cohort; the two lists were not jointly ranked'),
    ('membership','No enrollment, purchases, outreach, or active memberships have been recorded')])
con.commit()

with (ROOT / 'companies.csv').open('w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=columns)
    writer.writeheader()
    writer.writerows(records)

wb = Workbook()
intro = wb.active
intro.title = 'Read me'
instructions = [
    ('Saif Industries - customer and membership management', ''),
    ('Records', '45 unique prospective businesses: original 25 plus 20 additional outside California.'),
    ('Verification', 'All records are unverified. No live website or contact verification was available.'),
    ('Missing contacts', 'Names, phones, emails, street addresses and postal codes are blank because they are unknown.'),
    ('Suggested roles', 'Contact roles are outreach suggestions, not verified employees or departments.'),
    ('Ranking', 'Cohort ranks preserve the two separate lists. They are not one combined strongest-to-weakest ranking.'),
    ('Memberships', 'All companies start as Prospect / Not enrolled. No membership plan, fee or purchase is assumed.'),
    ('Use', 'Filter Companies by tier, state or status; record verified contacts, interactions, follow-ups and enrollments in the other sheets.'),
    ('Dates', 'Use YYYY-MM-DD for dates. Record verification source and date when confirming contact information.'),
    ('Source of truth', 'SQLite and this workbook are separate editable copies. Changes do not synchronize automatically.'),
    ('Company IDs', 'Keep company_id stable and use it to connect records across sheets.'),
    ('Status updates', 'Update the company summary fields when recording contact activity or membership changes.'),
    ('Privacy', 'Store only appropriate business contact information. Do not store payment-card details here.')]
for row in instructions:
    intro.append(row)
intro.column_dimensions['A'].width = 32
intro.column_dimensions['B'].width = 110
for row in intro:
    for cell in row:
        cell.alignment = Alignment(wrap_text=True, vertical='top')
    intro.row_dimensions[row[0].row].height = 42

def sheet(name, headers, rows, table_name):
    ws = wb.create_sheet(name)
    ws.append(headers)
    for row in rows:
        ws.append(row)
    if not rows:
        ws.append([None] * len(headers))
    ws.freeze_panes = 'C2'
    for cell in ws[1]:
        cell.font = Font(bold=True, color='FFFFFF')
        cell.fill = PatternFill('solid', fgColor='17365D')
    for col in ws.columns:
        header = str(col[0].value)
        width = 45 if header in ('notes','source','potential_cnc_work','summary','task') else 30 if header in ('website_url','company_name','contact_role_to_request') else 20
        ws.column_dimensions[col[0].column_letter].width = width
    table = Table(displayName=table_name, ref=ws.dimensions)
    table.tableStyleInfo = TableStyleInfo(name='TableStyleMedium2', showRowStripes=True)
    ws.add_table(table)
    return ws

ws = sheet('Companies', columns, [[r[c] for c in columns] for r in records], 'CompaniesTable')
for row in ws.iter_rows(min_row=2):
    row[columns.index('website_url')].hyperlink = row[columns.index('website_url')].value
    row[columns.index('website_url')].style = 'Hyperlink'
for field, choices in {
    'lifecycle_status':'Prospect,Contacted,Qualified,Quoted,Customer,Not a fit,Do not contact',
    'membership_status':'Not enrolled,Pending,Active,Paused,Expired,Cancelled',
    'verification_status':'Unverified,Partially verified,Verified'
}.items():
    dv = DataValidation(type='list', formula1='"'+choices+'"')
    dv.errorTitle = 'Choose a listed status'
    dv.error = 'Please select one of the available statuses.'
    dv.showErrorMessage = True
    ws.add_data_validation(dv)
    letter = ws.cell(1, columns.index(field)+1).column_letter
    dv.add(f'{letter}2:{letter}10000')
for name, table in [('Contacts','contacts'),('Interactions','interactions'),('Follow-ups','follow_ups'),('Memberships','memberships')]:
    headers = [r[1] for r in con.execute('PRAGMA table_info('+table+')')]
    sheet(name, headers, [], table.replace('_','').title()+'Table')
wb.save(ROOT / 'saif_customer_management.xlsx')

assert con.execute('SELECT COUNT(*) FROM companies').fetchone()[0] == 45
assert con.execute('SELECT COUNT(DISTINCT company_name) FROM companies').fetchone()[0] == 45
assert con.execute("SELECT COUNT(*) FROM companies WHERE cohort='Additional outside California'").fetchone()[0] == 20
assert con.execute("SELECT COUNT(*) FROM companies WHERE cohort='Additional outside California' AND (state IS NULL OR state='California')").fetchone()[0] == 0
assert con.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
assert not con.execute('PRAGMA foreign_key_check').fetchall()
con.close()
print('Created and validated SQLite database, Excel workbook and CSV: 45 unique prospects.')
