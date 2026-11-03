"""Add sales operations to the existing CRM without inventing buyer activity."""
from pathlib import Path
from datetime import datetime, timezone
import sqlite3
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.worksheet.datavalidation import DataValidation

root=Path(__file__).resolve().parent
db=sqlite3.connect(root/'saif_customer_management.sqlite')
db.execute('PRAGMA foreign_keys=ON')
wb=load_workbook(root/'saif_customer_management.xlsx')
names=['Pipeline','Opportunities','RFQs','Quotes','Orders','Quality','Capacity','Setup tasks','Dashboard']
if any(name in wb.sheetnames for name in names):
    raise SystemExit('Pipeline sheets already exist. Refusing to overwrite edits.')
stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
backup=root/'backups'/('pipeline-'+stamp)
backup.mkdir(parents=True)
with sqlite3.connect(backup/'saif_customer_management.sqlite') as copy:
    db.backup(copy)
(backup/'saif_customer_management.xlsx').write_bytes((root/'saif_customer_management.xlsx').read_bytes())
original=db.execute('SELECT * FROM companies ORDER BY company_id').fetchall()
db.executescript('''
CREATE TABLE IF NOT EXISTS sales_pipeline (
 company_id INTEGER PRIMARY KEY REFERENCES companies(company_id),
 stage TEXT NOT NULL DEFAULT 'Prospect' CHECK(stage IN
 ('Prospect','Qualified buyer','Drawing/RFQ received','Quote submitted','Trial order','Approved supplier','Repeat customer','On hold','Closed lost','Do not contact')),
 buyer_verified INTEGER NOT NULL DEFAULT 0 CHECK(buyer_verified IN (0,1)),
 cnc_outsourcing_confirmed INTEGER NOT NULL DEFAULT 0 CHECK(cnc_outsourcing_confirmed IN (0,1)),
 capability_fit_confirmed INTEGER NOT NULL DEFAULT 0 CHECK(capability_fit_confirmed IN (0,1)),
 evidence_reference TEXT, owner TEXT, next_action TEXT, next_action_date TEXT, notes TEXT
);
CREATE TABLE IF NOT EXISTS opportunities (
 opportunity_id INTEGER PRIMARY KEY, company_id INTEGER NOT NULL REFERENCES companies(company_id),
 part_family TEXT NOT NULL, part_description TEXT, expected_quantity INTEGER CHECK(expected_quantity>0),
 annual_quantity INTEGER CHECK(annual_quantity>=0), currency TEXT, estimated_value REAL CHECK(estimated_value>=0),
 decision_date TEXT, reorder_potential TEXT, status TEXT NOT NULL DEFAULT 'Open'
 CHECK(status IN ('Open','Won','Lost','On hold')), loss_reason TEXT, owner TEXT, next_action TEXT, next_action_date TEXT, notes TEXT
);
CREATE TABLE IF NOT EXISTS rfqs (
 rfq_id INTEGER PRIMARY KEY, opportunity_id INTEGER NOT NULL REFERENCES opportunities(opportunity_id),
 received_date TEXT NOT NULL, due_date TEXT, drawing_reference TEXT NOT NULL,
 drawing_revision TEXT, material TEXT NOT NULL, quantity INTEGER NOT NULL CHECK(quantity>0),
 critical_tolerances TEXT, surface_finish TEXT, finishing_requirements TEXT,
 inspection_requirements TEXT, delivery_required TEXT, supplier_requirements TEXT,
 technical_review_status TEXT NOT NULL DEFAULT 'Pending'
 CHECK(technical_review_status IN ('Pending','Clarification needed','Accepted','Declined')), notes TEXT
);
CREATE TABLE IF NOT EXISTS quotes (
 quote_id INTEGER PRIMARY KEY, rfq_id INTEGER NOT NULL REFERENCES rfqs(rfq_id),
 quote_reference TEXT NOT NULL UNIQUE, sent_date TEXT NOT NULL, valid_until TEXT,
 currency TEXT NOT NULL, quantity INTEGER NOT NULL CHECK(quantity>0),
 total_quoted_revenue REAL NOT NULL CHECK(total_quoted_revenue>0),
 total_estimated_cost REAL NOT NULL CHECK(total_estimated_cost>=0),
 lead_time_business_days INTEGER CHECK(lead_time_business_days>=0), payment_terms TEXT,
 status TEXT NOT NULL DEFAULT 'Submitted' CHECK(status IN ('Submitted','Won','Lost','Expired','Withdrawn','Superseded')),
 decision_date TEXT, loss_reason TEXT, notes TEXT
);
CREATE TABLE IF NOT EXISTS orders (
 order_id INTEGER PRIMARY KEY, quote_id INTEGER NOT NULL REFERENCES quotes(quote_id),
 po_reference TEXT NOT NULL, order_type TEXT NOT NULL CHECK(order_type IN ('Trial','Production','Repeat')),
 ordered_date TEXT NOT NULL, promised_ship_date TEXT NOT NULL, actual_ship_date TEXT,
 quantity INTEGER NOT NULL CHECK(quantity>0), currency TEXT NOT NULL,
 revenue REAL NOT NULL CHECK(revenue>=0), actual_total_cost REAL CHECK(actual_total_cost>=0),
 estimated_machine_hours REAL CHECK(estimated_machine_hours>=0),
 status TEXT NOT NULL DEFAULT 'Booked' CHECK(status IN ('Booked','In production','Shipped','Cancelled')), notes TEXT
);
CREATE TABLE IF NOT EXISTS quality_results (
 quality_id INTEGER PRIMARY KEY, order_id INTEGER NOT NULL REFERENCES orders(order_id),
 inspected_date TEXT NOT NULL, units_inspected INTEGER NOT NULL CHECK(units_inspected>0),
 units_rejected INTEGER NOT NULL CHECK(units_rejected>=0 AND units_rejected<=units_inspected),
 units_reworked INTEGER NOT NULL CHECK(units_reworked>=0 AND units_reworked<=units_inspected),
 customer_feedback TEXT, corrective_action TEXT, notes TEXT
);
CREATE TABLE IF NOT EXISTS capacity_plan (
 capacity_id INTEGER PRIMARY KEY, week_start TEXT NOT NULL, machine_or_workcenter TEXT NOT NULL,
 available_hours REAL NOT NULL CHECK(available_hours>=0),
 booked_hours REAL NOT NULL CHECK(booked_hours>=0), notes TEXT,
 UNIQUE(week_start,machine_or_workcenter)
);
CREATE TABLE IF NOT EXISTS setup_tasks (
 task_id INTEGER PRIMARY KEY, sequence INTEGER NOT NULL UNIQUE, task TEXT NOT NULL,
 completion_evidence TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'Not started'
 CHECK(status IN ('Not started','In progress','Blocked','Done')), owner TEXT, due_date TEXT, dependency TEXT
);
CREATE VIEW IF NOT EXISTS quote_economics AS
 SELECT *, (total_quoted_revenue-total_estimated_cost)/total_quoted_revenue AS estimated_gross_margin
 FROM quotes;
CREATE VIEW IF NOT EXISTS order_performance AS
 SELECT *, CASE WHEN revenue>0 AND actual_total_cost IS NOT NULL THEN
 (revenue-actual_total_cost)/revenue END AS actual_gross_margin,
 CASE WHEN status='Shipped' AND actual_ship_date IS NOT NULL THEN
 CASE WHEN actual_ship_date<=promised_ship_date THEN 1 ELSE 0 END END AS shipped_on_time
 FROM orders;
''')
db.executemany('INSERT OR IGNORE INTO sales_pipeline(company_id,next_action,notes) VALUES (?,?,?)',[
 (row[0],'Verify buyer and outsourcing evidence; compare RFQ requirements with Saif capabilities.',
 'Preliminary prospect only. Earlier rank is not evidence of qualification.') for row in original])
tasks=[
 ('Confirm Saif capability profile','Machine model/axes, part envelope, materials, tolerances, inspection, certifications, location, capacity and lead times recorded.','Not started','Saif input'),
 ('Select 2-3 candidate part families','Owner-approved families supported by capability and cost evidence; no product performance claims assumed.','Not started','Capability profile'),
 ('Verify company and buyer contacts','Current business contact, role, phone/email, address and dated source for each selected prospect.','Blocked','Website access or supplied source documents'),
 ('Confirm CNC outsourcing demand','Buyer statement or explicit documented CNC sourcing evidence, with date and reference.','Blocked','Verified contact or accessible sourcing evidence'),
 ('Prepare capability sheet and sample portfolio','Completed factual sheet plus permission-cleared part photos and inspection examples.','Not started','Capability profile and approved examples'),
 ('Conduct buyer discovery','Recorded part requirements, sourcing problem, buying process and agreed next step.','Not started','Verified contact; outreach authorization'),
 ('Obtain and review an RFQ','Drawing revision, quantity, material, tolerances, finish, inspection, delivery and terms captured.','Not started','Buyer response'),
 ('Cost and submit suitable trial quote','Documented cost, margin, delivery and payment terms; technical review accepted.','Not started','Accepted RFQ; authorization to submit'),
 ('Deliver and review paid trial','Actual PO, shipment, inspection results, margin and buyer feedback recorded.','Not started','Accepted order'),
 ('Agree repeat-order process','Supplier approval, forecast limits, reorder triggers and lead times documented.','Not started','Successful trial and buyer agreement')]
db.executemany('INSERT OR IGNORE INTO setup_tasks(sequence,task,completion_evidence,status,dependency) VALUES (?,?,?,?,?)',
 [(i,*task) for i,task in enumerate(tasks,1)])
db.commit()

def sheet(name,headers,rows,table_name):
    ws=wb.create_sheet(name)
    ws.append(headers)
    for row in rows: ws.append(row)
    if not rows: ws.append([None]*len(headers))
    ws.freeze_panes='C2'
    for col in ws.columns:
        ws.column_dimensions[col[0].column_letter].width=28
    for cell in ws[1]:
        cell.font=Font(bold=True,color='FFFFFF')
        cell.fill=PatternFill('solid',fgColor='17365D')
    t=Table(displayName=table_name,ref=ws.dimensions)
    t.tableStyleInfo=TableStyleInfo(name='TableStyleMedium2',showRowStripes=True)
    ws.add_table(t)
    return ws

def dropdown(ws,header,choices):
    col=[c.value for c in ws[1]].index(header)+1
    dv=DataValidation(type='list',formula1='"'+','.join(choices)+'"')
    dv.showErrorMessage=True
    dv.error='Select a listed value.'
    ws.add_data_validation(dv)
    letter=ws.cell(1,col).column_letter
    dv.add(f'{letter}2:{letter}10000')

cursor=db.execute('SELECT c.company_id,c.company_name,p.stage,p.buyer_verified,p.cnc_outsourcing_confirmed,p.capability_fit_confirmed,p.evidence_reference,p.owner,p.next_action,p.next_action_date,p.notes FROM sales_pipeline p JOIN companies c USING(company_id) ORDER BY c.company_id')
ws=sheet('Pipeline',[c[0] for c in cursor.description],cursor.fetchall(),'SalesPipelineTable')
dropdown(ws,'stage',['Prospect','Qualified buyer','Drawing/RFQ received','Quote submitted','Trial order','Approved supplier','Repeat customer','On hold','Closed lost','Do not contact'])
for field in ('buyer_verified','cnc_outsourcing_confirmed','capability_fit_confirmed'): dropdown(ws,field,['0','1'])
for name,table in [('Opportunities','opportunities'),('RFQs','rfqs'),('Quotes','quotes'),('Orders','orders'),('Quality','quality_results'),('Capacity','capacity_plan'),('Setup tasks','setup_tasks')]:
    cursor=db.execute('SELECT * FROM '+table)
    headers=[c[0] for c in cursor.description]
    rows=cursor.fetchall()
    if name=='Quotes': headers+=['estimated_gross_margin']
    if name=='Orders': headers+=['actual_gross_margin','shipped_on_time']
    ws=sheet(name,headers,rows,table.replace('_','').title()+'SalesTable')
    if name=='Quotes':
        ws['P2']='=IF(OR(H2="",I2="",H2=0),"",(H2-I2)/H2)'
        ws['P2'].number_format='0.0%'
        dropdown(ws,'status',['Submitted','Won','Lost','Expired','Withdrawn','Superseded'])
    if name=='Orders':
        ws['O2']='=IF(OR(J2="",K2="",J2=0),"",(J2-K2)/J2)'
        ws['O2'].number_format='0.0%'
        ws['P2']='=IF(OR(M2<>"Shipped",F2="",G2=""),"",IF(G2<=F2,1,0))'
        dropdown(ws,'status',['Booked','In production','Shipped','Cancelled'])
        dropdown(ws,'order_type',['Trial','Production','Repeat'])
    if name=='Opportunities': dropdown(ws,'status',['Open','Won','Lost','On hold'])
    if name=='Setup tasks': dropdown(ws,'status',['Not started','In progress','Blocked','Done'])
    if name=='RFQs': dropdown(ws,'technical_review_status',['Pending','Clarification needed','Accepted','Declined'])

dash=wb.create_sheet('Dashboard')
dash.append(['Metric','Value','Definition / limits'])
metrics=[
 ('Prospects','=COUNTA(CompaniesTable[company_name])','All company records, not confirmed buyers.'),
 ('Qualified buyers','=COUNTIFS(SalesPipelineTable[buyer_verified],1,SalesPipelineTable[cnc_outsourcing_confirmed],1,SalesPipelineTable[capability_fit_confirmed],1)','All three evidence gates must be confirmed.'),
 ('RFQs received','=COUNT(RfqsSalesTable[rfq_id])','Count only actual RFQs.'),
 ('Quotes recorded','=COUNT(QuotesSalesTable[quote_id])','Exclude drafts; submitted quote records.'),
 ('Quote win rate','=IF(COUNTIF(QuotesSalesTable[status],"Won")+COUNTIF(QuotesSalesTable[status],"Lost")=0,"N/A",COUNTIF(QuotesSalesTable[status],"Won")/(COUNTIF(QuotesSalesTable[status],"Won")+COUNTIF(QuotesSalesTable[status],"Lost")))','Won / (Won + Lost); pending, expired and superseded versions excluded. Select a reporting period before comparing months.'),
 ('Open booked orders','=COUNTIF(OrdersSalesTable[status],"Booked")+COUNTIF(OrdersSalesTable[status],"In production")','Actual orders awaiting shipment; no speculative opportunities.'),
 ('Shipped on-time rate','=IF(COUNT(OrdersSalesTable[shipped_on_time])=0,"N/A",AVERAGE(OrdersSalesTable[shipped_on_time]))','Shipped orders with actual dates only. Review overdue unshipped orders separately.'),
 ('Inspected units','=SUM(QualityresultsSalesTable[units_inspected])','Use one consolidated final inspection record per order to avoid double counting.'),
 ('Rejected unit rate','=IF(SUM(QualityresultsSalesTable[units_inspected])=0,"N/A",SUM(QualityresultsSalesTable[units_rejected])/SUM(QualityresultsSalesTable[units_inspected]))','Rejected / inspected; rework is tracked separately.'),
 ('Repeat orders','=COUNTIF(OrdersSalesTable[order_type],"Repeat")-COUNTIFS(OrdersSalesTable[order_type],"Repeat",OrdersSalesTable[status],"Cancelled")','Non-cancelled repeat orders; not the same as trial-to-repeat conversion.'),
 ('Status','Setup in progress','No contacts, RFQs, quotes, orders or memberships have been fabricated.')]
for row in metrics: dash.append(row)
for i in (6,8,10): dash.cell(i,2).number_format='0.0%'
dash.column_dimensions['A'].width=30
dash.column_dimensions['B'].width=25
dash.column_dimensions['C'].width=115
dash.freeze_panes='A2'
wb['Read me'].append(('Sales pipeline','New pipeline and sales worksheets track actual work. Company lifecycle and pipeline stages are manually maintained separately. See pipeline-playbook.md for gates and metric definitions.'))
wb['Read me'].append(('Dashboard','Excel calculates formulas when opened. N/A means no observations. Formulas have not been evaluated by a spreadsheet engine here. Workbook and SQLite remain separate copies.'))
wb.save(root/'saif_customer_management.xlsx')
assert original==db.execute('SELECT * FROM companies ORDER BY company_id').fetchall()
assert db.execute('SELECT COUNT(*) FROM sales_pipeline').fetchone()[0]==45
assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
assert not db.execute('PRAGMA foreign_key_check').fetchall()
db.close()
reopened=load_workbook(root/'saif_customer_management.xlsx')
table_names={t for ws in reopened for t in ws.tables}
import re
for row in reopened['Dashboard']:
    for cell in row:
        if cell.data_type=='f':
            for table in re.findall(r'([A-Za-z][A-Za-z0-9_]*)\[',cell.value):
                assert table in table_names,table
assert reopened['Pipeline'].max_row==46
print('Validated: 45 preserved companies; 45 prospect pipeline records; 10 setup tasks; empty transaction tables; database integrity; workbook table references.')
print('Backup:',backup)
