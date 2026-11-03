# Saif Industries sales pipeline

## Start here

1. Complete `capability-sheet-template.md` and the workbook's Saif capabilities sheet. A partial factual profile is more useful than assumed capabilities.
2. Choose 2–3 candidate part families using actual sample costing and shop capacity.
3. Verify a small initial group of buyers. Previous prospect ranks are unverified hypotheses, not evidence of demand. Website verification remains blocked until the prepared environment access changes are applied.
4. Use the discovery questions and outreach drafts in `buyer-discovery-and-outreach.md`. Review facts before use; no messages have been sent.
5. Request a drawing/RFQ, perform technical review, cost a paid trial, and record the actual outcome.

The Setup tasks worksheet contains 10 concrete tasks with completion evidence. Owners and deadlines are intentionally unassigned.

## Stage gates

| Stage | Evidence required before advancing |
|---|---|
| Prospect | Identified business; demand and capabilities can remain unknown |
| Qualified buyer | Verified relevant buyer, confirmed CNC outsourcing need, and documented technical/commercial fit with Saif |
| Drawing/RFQ received | Actual drawing revision, material, quantity, tolerances, finish, inspection, delivery and sourcing requirements |
| Quote submitted | Submitted quote reference and date, cost estimate, price, lead time, validity and payment terms |
| Trial order | Actual accepted customer PO for a trial; a requested quote is not an order |
| Approved supplier | Customer-confirmed approval; shipping a trial does not automatically establish this |
| Repeat customer | Actual subsequent purchase, not an optimistic forecast |

Record On hold, Closed lost or Do not contact when appropriate. Respect company Do not contact status before outreach. Buyer verification, outsourcing confirmation and capability fit are independent gates; 0 means not confirmed, not disproved.

Pipeline stage and the Companies lifecycle status are separate summary fields. They are manually maintained. A company can have several part opportunities; use separate opportunity IDs, then link RFQs, quotes and orders. Company-level stages summarize the most relevant active relationship, not the status of every individual part.

## Cost a quote before offering a price

Include stock/material and waste, programming/setup, machine and operator time, tooling, inspection, finishing/subcontracting, packaging/shipping, and applicable manufacturing overhead. Allocate setup over the quoted quantity. Document assumptions and any separate nonrecurring charges. Avoid including sales tax as sales revenue.

Estimated gross margin = (quoted revenue − total estimated job cost) / quoted revenue. A 25% markup is not a 25% margin. The workbook contains no assumed minimum margin; an owner must choose the threshold.

Quotes are submitted records, not drafts. Use distinct quote references for revisions; mark replaced quotes Superseded so quote outcomes are not double-counted. If several orders fulfill one quote, record only each order's own revenue/cost/quantity; do not repeat the full quote value on every order.

## Record actual performance

- Quality: use one consolidated final inspection result per order for dashboard totals. Reworked units may overlap rejected units; never add the two percentages as a defect rate.
- Delivery: compare actual ship date with promised ship date. This is an on-time shipping measure, not proof of delivery. Separately inspect overdue unshipped orders.
- Capacity: enter available and booked machine hours per workcenter and week. Do not total multiple weeks or machines to claim a specific machine can meet a due date.
- Trial conversion: count unique companies with completed, non-cancelled trials and subsequent repeat orders; use a defined observation period. No conversion percentage is shown before observations exist.
- Concentration and margin: aggregate actual order revenue by customer and currency over a stated period. Do not mix currencies or use a simple average of job margin percentages as a revenue-weighted margin.

## Workbook dashboard

The dashboard counts prospects, qualified buyers, RFQs, quotes, open booked orders and repeat orders; it calculates quote win rate, on-time shipped rate and rejection rate. Empty activity produces zero counts and N/A rates. No results have been invented.

Excel calculates formulas when opened. A spreadsheet calculation engine was not available to evaluate the saved formulas here. When expanding Quotes or Orders, retain/copy the computed margin and on-time formula columns. Dashboard totals use Excel tables; add new records within those tables. For monthly reviews, filter/source a defined period; the initial dashboard is all-time, not a monthly report.

Use ISO date strings (`YYYY-MM-DD`) consistently for the workbook's comparisons. Quote and order currencies must match the intended transaction. Currency amounts require actual entered values; no currency has been assumed.

## Data files and scope

The Excel workbook and SQLite database are independent editable copies. Pick one as your source of truth; there is no automatic sync. The CSV remains the original company directory and does not include the new transaction tables. Backups were made before extending either file.

SQLite enforces IDs, foreign keys when enabled, statuses and basic quantity/value constraints. Stage gates, date consistency, commercial approval, duplicate PO review, and contact-to-company ownership still require review; this is not a fully automated ERP. No external CRM was updated and no outreach was sent.
