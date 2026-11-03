# Qualification status

All 45 companies remain prospective leads, not qualified buyers. The original tiers and ranks are preserved as preliminary estimates; they are not evidence-backed rankings.

## Completed

- Preserved all 45 company records and backed up the database, workbook, and company CSV before changes.
- Added a qualification record for every company, an evidence log, and a Saif capability profile in the SQLite database.
- Added matching Qualification, Evidence, and Saif capabilities worksheets to the Excel workbook and exported qualification.csv.
- Checked the database integrity, foreign keys, company count, and workbook record counts.
- Attempted to retrieve the TOTAL CHAOS and Rock Krawler websites. Both requests were rejected by the configured proxy with `Tunnel connection failed: 403 Forbidden`; no website content was retrieved. Other company sites have not been checked in this pass.
- Saved a configuration draft adding only the 45 listed company website hostnames and their www/non-www counterparts (90 hosts). Existing package-manager presets were preserved. This save does not apply runtime access or publish the environment.

## Findings supported by evidence

- Capability-qualified companies: **0**. Saif's actual machine and inspection capabilities have not been supplied.
- Verified business contacts: **0**.
- Companies confirmed to outsource CNC machining: **0**. This means none have been confirmed, not that none outsource.
- Evidence-backed top 10: **not established**.

## What is needed

1. Saif's machine brands/models/axes, maximum part dimensions, materials, tolerances, inspection equipment, certifications, location, batch sizes, lead times, and available capacity. Unknown fields can stay unknown while supplied capabilities are assessed.
2. Review and save the website access changes in environment settings, then publish the environment as required by the configuration tool. Actual connectivity must be rechecked afterward. Hostnames are recorded in required-research-domains.txt; additional third-party contact or supplier portals, if needed, are not covered by these company-host rules.

## Qualification method once prerequisites are available

For each company, record source URLs, the date checked, and the precise fact each source supports. Verify headquarters versus factory, mailing, or shipping locations separately. A named employee's role must be verified before treating that person as the purchasing contact.

Classify outsourcing evidence as Unknown, Indirect evidence only, Confirmed outsourcing, or Confirmed current CNC opportunity. Selling machined parts, having a vendor list, or using contract manufacturing generally does not by itself prove a current CNC purchasing need. In-house machining does not prove the company never outsources.

Compare actual part requirements with Saif's known capabilities. Mark unknown requirements explicitly rather than giving speculative fit scores. Rank only after evidence is collected, favoring demonstrated CNC purchasing needs, technical fit, suitable quantities/lead times, an accessible purchasing route, and commercially workable supplier requirements. If fewer than 10 are supported, report the smaller qualified set rather than filling the list with guesses.

No businesses were contacted and no supplier applications were submitted.
