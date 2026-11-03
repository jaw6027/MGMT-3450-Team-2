"""Add an evidence-based qualification workspace without altering prospect facts."""
from pathlib import Path
import csv
import sqlite3
from datetime import datetime, timezone
from urllib.parse import urlsplit
from openpyxl import load_workbook
from openpyxl.worksheet.table import Table, TableStyleInfo

root = Path(__file__).resolve().parent
stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
backup = root / 'backups' / stamp
backup.mkdir(parents=True)
db = sqlite3.connect(root / 'saif_customer_management.sqlite')
db.execute('PRAGMA foreign_keys=ON')
with sqlite3.connect(backup / 'saif_customer_management.sqlite') as copy:
    db.backup(copy)
for filename in ('saif_customer_management.xlsx', 'companies.csv'):
    (backup / filename).write_bytes((root / filename).read_bytes())

db.executescript('''
CREATE TABLE IF NOT EXISTS qualification (
 company_id INTEGER PRIMARY KEY REFERENCES companies(company_id),
 capability_fit_status TEXT NOT NULL DEFAULT 'Pending Saif capabilities',
 contact_verification_status TEXT NOT NULL DEFAULT 'Not checked',
 outsourcing_status TEXT NOT NULL DEFAULT 'Unknown',
 supplier_requirements TEXT, source_urls TEXT, evidence_summary TEXT,
 evidence_based_rank INTEGER UNIQUE, research_status TEXT NOT NULL,
 next_action TEXT NOT NULL, reviewed_at_utc TEXT
);
CREATE TABLE IF NOT EXISTS qualification_evidence (
 evidence_id INTEGER PRIMARY KEY,
 company_id INTEGER NOT NULL REFERENCES companies(company_id),
 checked_at_utc TEXT NOT NULL, source_url TEXT NOT NULL,
 evidence_type TEXT NOT NULL, observation TEXT NOT NULL,
 supports_outsourcing INTEGER NOT NULL DEFAULT 0 CHECK(supports_outsourcing IN (0,1))
);
CREATE TABLE IF NOT EXISTS saif_capabilities (
 capability TEXT PRIMARY KEY, supplied_value TEXT, verification_source TEXT,
 status TEXT NOT NULL DEFAULT 'Not supplied'
);
''')
now = datetime.now(timezone.utc).isoformat(timespec='seconds')
companies = db.execute('SELECT company_id,company_name,website_url FROM companies ORDER BY company_id').fetchall()
db.executemany('''INSERT OR IGNORE INTO qualification
 (company_id,research_status,next_action) VALUES (?,?,?)''', [
 (cid,'Pending website access and Saif capabilities',
  'Verify current company/contact details and explicit outsourcing evidence; compare with supplied Saif capabilities.')
 for cid, name, url in companies])
for capability in ('Machine brands/models and axes','Maximum part dimensions and travels',
                   'Materials and machining processes','Tolerances and surface finishes',
                   'Inspection equipment and measurement capability','Quality certifications and traceability',
                   'Business location and shipping coverage','Typical batch size and minimum order',
                   'Available capacity and lead times','Target pricing/margin and payment terms'):
    db.execute('INSERT OR IGNORE INTO saif_capabilities(capability) VALUES (?)',(capability,))
for cid in (1,26):
    url = next(url for key,name,url in companies if key==cid)
    db.execute('''INSERT INTO qualification_evidence
        (company_id,checked_at_utc,source_url,evidence_type,observation)
        VALUES (?,?,?,?,?)''',(cid,now,url,'Access attempt',
        'Configured proxy rejected HTTPS connection: Tunnel connection failed: 403 Forbidden. No website content retrieved. This is not evidence of company inactivity or outsourcing.'))
    db.execute('UPDATE qualification SET research_status=?, reviewed_at_utc=? WHERE company_id=?',
               ('Website access blocked by environment policy; capabilities pending',now,cid))
db.execute('INSERT OR REPLACE INTO metadata VALUES (?,?)',('qualification_status',
    '0 capability-qualified; 0 verified business contacts; 0 confirmed CNC outsourcing buyers; no evidence-backed top 10 established.'))
db.commit()
assert db.execute('SELECT COUNT(*) FROM qualification').fetchone()[0]==45
assert db.execute('SELECT COUNT(*) FROM companies').fetchone()[0]==45
assert db.execute('SELECT COUNT(*) FROM qualification WHERE evidence_based_rank IS NOT NULL').fetchone()[0]==0
assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
assert not db.execute('PRAGMA foreign_key_check').fetchall()

workbook = load_workbook(root / 'saif_customer_management.xlsx')
for sheetname in ('Qualification','Evidence','Saif capabilities'):
    if sheetname in workbook.sheetnames:
        raise SystemExit('Existing qualification worksheet detected; refusing to replace manual edits.')
queries = [
 ('Qualification','QualificationTable','''SELECT c.company_id,c.company_name,q.capability_fit_status,
 q.contact_verification_status,q.outsourcing_status,q.supplier_requirements,q.source_urls,
 q.evidence_summary,q.evidence_based_rank,q.research_status,q.next_action,q.reviewed_at_utc
 FROM qualification q JOIN companies c USING(company_id) ORDER BY c.company_id'''),
 ('Evidence','EvidenceTable','SELECT * FROM qualification_evidence'),
 ('Saif capabilities','SaifCapabilitiesTable','SELECT * FROM saif_capabilities')]
for name,tablename,sql in queries:
    cursor=db.execute(sql)
    headers=[col[0] for col in cursor.description]
    rows=cursor.fetchall()
    ws=workbook.create_sheet(name)
    ws.append(headers)
    for row in rows: ws.append(row)
    ws.freeze_panes='C2'
    for column in ws.columns:
        ws.column_dimensions[column[0].column_letter].width=36
    table=Table(displayName=tablename,ref=ws.dimensions)
    table.tableStyleInfo=TableStyleInfo(name='TableStyleMedium2',showRowStripes=True)
    ws.add_table(table)
    if name=='Qualification':
        with (root/'qualification.csv').open('w',newline='',encoding='utf-8-sig') as f:
            w=csv.writer(f);w.writerow(headers);w.writerows(rows)
workbook['Read me'].append(('Qualification update',
    'Qualification, Evidence and Saif capabilities sheets added. No verified contacts, confirmed outsourcing, capability fit, or evidence-based rank yet. Earlier prospect tiers remain unverified estimates.'))
workbook.save(root/'saif_customer_management.xlsx')
reopened=load_workbook(root/'saif_customer_management.xlsx')
assert reopened['Companies'].max_row==46
assert reopened['Qualification'].max_row==46
hosts=set()
for cid,name,url in companies:
    host=urlsplit(url).hostname.removeprefix('www.')
    hosts.update((host,'www.'+host))
(root/'required-research-domains.txt').write_text('\n'.join(sorted(hosts))+'\n')
db.close()
print('Preserved backups:',backup)
print('Validated 45 qualification records, 2 access-attempt observations, 10 missing capability fields; existing company data retained.')
