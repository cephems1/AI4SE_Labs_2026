# Library Management Reporting and Analytics System - Software Requirements Specification

*Generated on 2026-10-20 by the LangGraph requirements-refinement network from 20 input documents.*

## 1. Introduction

A centralized management reporting, analytics, collection-management, and administrative system for a large library consortium. Library staff, managers, directors, local and global administrators, and indirectly patrons use it to report on collections, circulation, patrons, finances, holds, transfers, capacity, and operational performance; manage collection and item workflows; administer access and configurations; and support planning, compliance, and board reporting across hundreds of library locations. The system integrates with an enterprise library automation platform and OPAC while protecting production operations and patron privacy.

This document consolidates **142 requirements** (34 × P1, 64 × P2, 44 × P3, 0 × P4) derived from **629 candidate statements** extracted from the corpus. Semantically duplicate statements were merged; **5 statements were discarded** and are listed with reasons in Section 8. Every requirement has a unique identifier `REQ-<AREA>-<NNN>` and lists the input documents it was derived from (Sections 6 and 7).

## 2. Source Documents

| Doc ID | File | Date | Requirements traced |
|---|---|---|---|
| D01 | `conversations/conv_pines014_material_volume.eml` | 2009-04-06 | 1 |
| D02 | `conversations/conv_pines015_capacity_interface.eml` | 2009-04-08 | 2 |
| D03 | `conversations/conv_pines016_shelf_space.eml` | 2009-04-13 | 1 |
| D04 | `conversations/conv_pines018_item_transfer.eml` | 2009-05-11 | 11 |
| D05 | `conversations/conv_pines019_020_missing_intransit.eml` | 2009-04-16 | 5 |
| D06 | `conversations/conv_pines021_item_purging.eml` | 2009-04-21 | 8 |
| D07 | `conversations/conv_pines022_deletions.eml` | 2009-04-24 | 3 |
| D08 | `conversations/conv_pines023_patron_characteristics.eml` | 2009-04-29 | 2 |
| D09 | `conversations/conv_pines024_inactive_patrons.eml` | 2009-05-05 | 3 |
| D10 | `early_draft_srs_galecia.txt` | 2009-01-27 | 92 |
| D11 | `email_financial_reports.eml` | 2009-07-13 | 10 |
| D12 | `email_report_features.eml` | 2009-07-27 | 11 |
| D13 | `email_staff_login.eml` | 2009-04-09 | 5 |
| D14 | `evergreen_reference_2009.txt` | 2009-03-15 | 37 |
| D15 | `interview_cataloging_2009-05-08.txt` | 2009-05-08 | 22 |
| D16 | `interview_sysadmin_2009-05-10.txt` | 2009-05-10 | 11 |
| D17 | `meeting_minutes/meeting_2009-03-15_minutes.txt` | 2009-03-15 | 15 |
| D18 | `meeting_minutes/meeting_2009-07-20_minutes.txt` | 2009-07-20 | 31 |
| D19 | `meeting_tech_subcommittee_2009-06-30.txt` | 2009-06-30 | 21 |
| D20 | `survey_results_2009.txt` | 2009-04-01 | 37 |

## 3. Priority Scale

| Priority | Label | Meaning | Assigned when |
|---|---|---|---|
| **P1** | Must have | Essential for the system to be acceptable; without it the system fails its core purpose. | Explicitly marked as high priority / critical / mandatory by stakeholders, legally or financially mandated, requested independently by several sources, or a prerequisite for other requirements. |
| **P2** | Should have | Important and high value, but the system remains usable without it for a limited time or a workaround exists. | Clearly requested and justified by stakeholders, used regularly in daily work, or supported by a large share of survey respondents, without being marked critical. |
| **P3** | Could have | Desirable improvement of usability, efficiency or insight. | Mentioned by a single source, framed as nice-to-have, or affecting a narrow user group. |
| **P4** | Future consideration | Acknowledged but deferred; not planned for the first release. | Explicitly deferred by stakeholders, speculative ideas, or items that depend on undecided external factors. |

## 4. Glossary

All requirements use the canonical terms below; the listed synonyms found in the source documents were normalised to them.

| Term | Definition | Replaces |
|---|---|---|
| **library location** | A branch, facility, or other organizational place at which library materials, staff, or transactions are associated. | branch, facility |
| **library system** | A consortium or administrative network comprising multiple library locations. | system-level |
| **library material** | A physical or uncataloged library resource tracked by the system. | collection item |
| **item record** | The record representing an individual copy or physical library material. | copy record |
| **bibliographic record** | The descriptive catalog record associated with one or more item records. | bib record, bib |
| **patron** | A person who uses or is registered with library services. | borrower |
| **staff member** | An employee or authorized worker performing library operations. | staff user |
| **report template** | A reusable, named definition of report criteria, fields, and presentation. | report definition |
| **saved query** | A stored query definition that can be reused or scheduled. | stored query, reusable query |
| **in-transit item** | An item that has departed one library location and has not yet arrived at its destination. |  |
| **last copy** | The only remaining item record for a bibliographic work within a specified scope. | final copy |
| **check-in** | The transaction that records the return of an item. | checkin |
| **checkout** | The transaction that records lending an item to a patron. | check-out, check out |
| **hold request** | A patron request to reserve or retrieve a library material. |  |
| **role** | A named set of permissions assigned to a staff member or group. | security group |
| **report queue** | The ordered set of submitted reports awaiting or undergoing execution. | queue of reports |
| **personally identifiable information** | Information that can identify a specific patron. | personally identifying information, PII |
| **reporting warehouse** | A data store containing historical information for reporting across dates or periods. | report warehouse, historical warehouse |

## 5. Requirements Overview

| Area | Name | Requirements |
|---|---|---|
| RPT | Reporting and Querying | 37 |
| COL | Collection and Inventory Management | 24 |
| PAT | Patron and Demographic Analytics | 6 |
| FIN | Financial Management | 11 |
| TRN | Circulation, Holds, and Transactions | 14 |
| SEC | Security, Auditing, and Administration | 14 |
| ARC | Architecture, Performance, and Technical Constraints | 21 |
| DOC | Documentation, Scope, and Governance | 15 |

| ID | Name | Priority | Type |
|---|---|---|---|
| [REQ-RPT-001](#req-rpt-001) | Material Volume Reporting | P1 | functional |
| [REQ-RPT-002](#req-rpt-002) | Library Location Capacity Reporting | P2 | functional |
| [REQ-RPT-003](#req-rpt-003) | Shelf Space Utilization Reporting | P2 | functional |
| [REQ-RPT-004](#req-rpt-004) | Ad Hoc Query Builder | P2 | functional |
| [REQ-RPT-005](#req-rpt-005) | Saved Queries | P2 | functional |
| [REQ-RPT-006](#req-rpt-006) | Report Template Management | P2 | functional |
| [REQ-RPT-007](#req-rpt-007) | Organize Report Templates | P3 | functional |
| [REQ-RPT-008](#req-rpt-008) | Existing Query Tool Integration | P3 | constraint |
| [REQ-RPT-009](#req-rpt-009) | Reporting Interfaces | P2 | functional |
| [REQ-RPT-010](#req-rpt-010) | Operational And Collection Report Catalog | P2 | functional |
| [REQ-RPT-011](#req-rpt-011) | Board And Executive Reports | P2 | functional |
| [REQ-RPT-012](#req-rpt-012) | Report Specification Coverage | P1 | constraint |
| [REQ-RPT-013](#req-rpt-013) | Report Queue Status | P1 | functional |
| [REQ-RPT-014](#req-rpt-014) | Report Queue Prioritization | P1 | functional |
| [REQ-RPT-015](#req-rpt-015) | Report Scheduling | P2 | functional |
| [REQ-RPT-016](#req-rpt-016) | Combined Report Runs | P3 | functional |
| [REQ-RPT-017](#req-rpt-017) | Report Output Formats | P2 | functional |
| [REQ-RPT-018](#req-rpt-018) | Email Report Delivery | P2 | functional |
| [REQ-RPT-019](#req-rpt-019) | Recurring Report Editing | P3 | functional |
| [REQ-RPT-020](#req-rpt-020) | Comparative Report Columns | P3 | functional |
| [REQ-RPT-021](#req-rpt-021) | Uploaded File Report Filters | P3 | functional |
| [REQ-RPT-022](#req-rpt-022) | Pivot Table Output | P3 | functional |
| [REQ-RPT-023](#req-rpt-023) | Report Cancellation | P2 | functional |
| [REQ-RPT-024](#req-rpt-024) | Null And Blank Result Inclusion | P2 | functional |
| [REQ-RPT-025](#req-rpt-025) | Current-State Reporting | P2 | functional |
| [REQ-RPT-026](#req-rpt-026) | Historical Reporting Warehouse | P2 | functional |
| [REQ-RPT-027](#req-rpt-027) | Report Criteria Display | P2 | functional |
| [REQ-RPT-028](#req-rpt-028) | Report Quick Access And Descriptions | P3 | functional |
| [REQ-RPT-029](#req-rpt-029) | Accurate Report Row Presentation | P2 | functional |
| [REQ-RPT-030](#req-rpt-030) | Survey Name Filtering | P3 | functional |
| [REQ-RPT-031](#req-rpt-031) | Transaction Audit Filtering | P3 | functional |
| [REQ-RPT-032](#req-rpt-032) | Item Usage Reporting | P2 | functional |
| [REQ-RPT-033](#req-rpt-033) | Status Conversion Support Report | P3 | functional |
| [REQ-RPT-034](#req-rpt-034) | Custom Local Reporting | P2 | functional |
| [REQ-RPT-035](#req-rpt-035) | Patron Demographic Reporting | P2 | functional |
| [REQ-RPT-036](#req-rpt-036) | Report Display Support | P3 | functional |
| [REQ-RPT-037](#req-rpt-037) | Cross-Location Comparison Reports | P3 | functional |
| [REQ-COL-001](#req-col-001) | Batch Item Transfers | P1 | functional |
| [REQ-COL-002](#req-col-002) | Select Transfer Candidates | P2 | functional |
| [REQ-COL-003](#req-col-003) | Reuse Transfer Queries | P1 | functional |
| [REQ-COL-004](#req-col-004) | Revert Temporary Transfers | P2 | functional |
| [REQ-COL-005](#req-col-005) | Preview Transfers | P3 | functional |
| [REQ-COL-006](#req-col-006) | Undo Transfers | P3 | functional |
| [REQ-COL-007](#req-col-007) | Track Transfer History | P2 | functional |
| [REQ-COL-008](#req-col-008) | Notify Staff Of Transfer Delays | P3 | functional |
| [REQ-COL-009](#req-col-009) | Report Missing And Damaged Items | P1 | functional |
| [REQ-COL-010](#req-col-010) | Analyze Missing And Damaged Patterns | P2 | functional |
| [REQ-COL-011](#req-col-011) | Report In-Transit Items | P1 | functional |
| [REQ-COL-012](#req-col-012) | Identify Items For Purging | P2 | functional |
| [REQ-COL-013](#req-col-013) | Convert Item Statuses In Batch | P1 | functional |
| [REQ-COL-014](#req-col-014) | Identify Last Copies | P1 | functional |
| [REQ-COL-015](#req-col-015) | Support WorldCat Cataloging Workflows | P1 | functional |
| [REQ-COL-016](#req-col-016) | Delete Unneeded Catalog Records | P2 | functional |
| [REQ-COL-017](#req-col-017) | Schedule Purging Operations | P3 | functional |
| [REQ-COL-018](#req-col-018) | Confirm Deletions | P2 | functional |
| [REQ-COL-019](#req-col-019) | Track Uncataloged Materials | P2 | functional |
| [REQ-COL-023](#req-col-023) | Distinguish Edit And Circulation Dates | P2 | functional |
| [REQ-COL-025](#req-col-025) | Query Items By Status | P3 | functional |
| [REQ-COL-026](#req-col-026) | Mark Items Missing | P3 | functional |
| [REQ-COL-027](#req-col-027) | Support Collection Batch Operations | P3 | functional |
| [REQ-COL-028](#req-col-028) | Alert On Holds Purchase Activity | P3 | functional |
| [REQ-PAT-001](#req-pat-001) | Patron Demographic Analytics | P1 | functional |
| [REQ-PAT-002](#req-pat-002) | Inactive Patron Identification | P1 | functional |
| [REQ-PAT-005](#req-pat-005) | Privacy-Protected Transaction Archive | P1 | constraint |
| [REQ-PAT-006](#req-pat-006) | Patron Interest Analysis | P3 | functional |
| [REQ-PAT-007](#req-pat-007) | Patron Renewal Statistics | P3 | functional |
| [REQ-PAT-008](#req-pat-008) | Inactive Patron Cleanup Assignment | P3 | functional |
| [REQ-FIN-001](#req-fin-001) | Financial Transaction Ledger | P1 | functional |
| [REQ-FIN-002](#req-fin-002) | Item Value Reports | P2 | functional |
| [REQ-FIN-003](#req-fin-003) | Financial Audit Compliance | P1 | constraint |
| [REQ-FIN-004](#req-fin-004) | Financial Activity Record Associations | P2 | functional |
| [REQ-FIN-005](#req-fin-005) | Financial Information Updates | P3 | functional |
| [REQ-FIN-006](#req-fin-006) | High Balance Account Queries | P3 | functional |
| [REQ-FIN-007](#req-fin-007) | Financial Reports | P2 | functional |
| [REQ-FIN-008](#req-fin-008) | Location Financial Activity Tracking | P2 | functional |
| [REQ-FIN-009](#req-fin-009) | Bill And Aged Debt Reports | P2 | functional |
| [REQ-FIN-010](#req-fin-010) | Historical Snapshot Bills Report | P3 | functional |
| [REQ-FIN-011](#req-fin-011) | Immediate Front Desk Payment Updates | P2 | functional |
| [REQ-TRN-001](#req-trn-001) | Transaction Activity Statistics | P3 | functional |
| [REQ-TRN-002](#req-trn-002) | Transaction Cross-Tabulation | P2 | functional |
| [REQ-TRN-004](#req-trn-004) | Transaction History Retention | P2 | constraint |
| [REQ-TRN-005](#req-trn-005) | Circulation Behavior Analytics | P2 | functional |
| [REQ-TRN-006](#req-trn-006) | Transaction Type Queries | P2 | functional |
| [REQ-TRN-007](#req-trn-007) | Check-In Counts By Method | P2 | functional |
| [REQ-TRN-008](#req-trn-008) | Checkout And Renewal Counts | P2 | functional |
| [REQ-TRN-009](#req-trn-009) | Hold Request Placement Metrics | P2 | functional |
| [REQ-TRN-010](#req-trn-010) | Patron Transaction Summary Reports | P2 | functional |
| [REQ-TRN-011](#req-trn-011) | Circulation Reports | P2 | functional |
| [REQ-TRN-012](#req-trn-012) | Hold Reports | P2 | functional |
| [REQ-TRN-013](#req-trn-013) | In-House Use Reports | P3 | functional |
| [REQ-TRN-015](#req-trn-015) | Claims Returned Report | P3 | functional |
| [REQ-TRN-016](#req-trn-016) | Separate Check-In Timestamps | P2 | functional |
| [REQ-SEC-001](#req-sec-001) | Staff Authentication Methods | P2 | functional |
| [REQ-SEC-002](#req-sec-002) | Staff Login Accountability | P2 | functional |
| [REQ-SEC-003](#req-sec-003) | Role-Based Access Governance | P3 | functional |
| [REQ-SEC-004](#req-sec-004) | Report Access Controls | P1 | functional |
| [REQ-SEC-005](#req-sec-005) | Report Template Restrictions | P2 | functional |
| [REQ-SEC-007](#req-sec-007) | Table And Field Access | P2 | functional |
| [REQ-SEC-008](#req-sec-008) | Item Transfer Authorization | P2 | functional |
| [REQ-SEC-009](#req-sec-009) | Administrative Responsibilities | P2 | functional |
| [REQ-SEC-010](#req-sec-010) | Deletion Audit Records | P1 | constraint |
| [REQ-SEC-011](#req-sec-011) | Deletion Reports | P1 | functional |
| [REQ-SEC-012](#req-sec-012) | Denied Deletion Attempts | P2 | functional |
| [REQ-SEC-013](#req-sec-013) | Deletion Safeguards | P2 | functional |
| [REQ-SEC-014](#req-sec-014) | Staff Account Security Report | P2 | functional |
| [REQ-SEC-015](#req-sec-015) | Staff Session Security | P2 | non-functional |
| [REQ-ARC-001](#req-arc-001) | Consortium Capacity | P1 | non-functional |
| [REQ-ARC-002](#req-arc-002) | Location Overview Capacity | P3 | non-functional |
| [REQ-ARC-003](#req-arc-003) | Large Batch Update Processing | P3 | non-functional |
| [REQ-ARC-004](#req-arc-004) | Inactive Patron Report Performance | P3 | non-functional |
| [REQ-ARC-005](#req-arc-005) | Centralized Multi-Location Service | P1 | constraint |
| [REQ-ARC-006](#req-arc-006) | Server Platform Compatibility | P1 | constraint |
| [REQ-ARC-007](#req-arc-007) | Relational Database Compatibility | P1 | constraint |
| [REQ-ARC-008](#req-arc-008) | Reporting Performance Isolation | P1 | non-functional |
| [REQ-ARC-009](#req-arc-009) | Browser And Client Access | P1 | constraint |
| [REQ-ARC-010](#req-arc-010) | Accessibility And Assistive Technology | P1 | non-functional |
| [REQ-ARC-011](#req-arc-011) | Standards-Compliant HTML | P1 | constraint |
| [REQ-ARC-012](#req-arc-012) | Separate Environments And Configuration Migration | P2 | functional |
| [REQ-ARC-013](#req-arc-013) | OPAC Functional Independence | P1 | constraint |
| [REQ-ARC-014](#req-arc-014) | Enterprise Automation System Dependency | P1 | constraint |
| [REQ-ARC-015](#req-arc-015) | Vendor Data Interfaces | P3 | functional |
| [REQ-ARC-016](#req-arc-016) | Read-Only OPAC Data Access | P2 | functional |
| [REQ-ARC-017](#req-arc-017) | Actionable Error Feedback | P2 | functional |
| [REQ-ARC-018](#req-arc-018) | Data Retention Policies | P1 | constraint |
| [REQ-ARC-019](#req-arc-019) | Login Without Specialized Infrastructure | P3 | constraint |
| [REQ-ARC-020](#req-arc-020) | Secondary-Site Disaster Recovery | P3 | non-functional |
| [REQ-ARC-021](#req-arc-021) | Optional Vendor EDI Data | P3 | functional |
| [REQ-DOC-001](#req-doc-001) | Data Specifications | P1 | functional |
| [REQ-DOC-002](#req-doc-002) | Major Process Descriptions | P2 | functional |
| [REQ-DOC-003](#req-doc-003) | Online Help | P1 | functional |
| [REQ-DOC-004](#req-doc-004) | Management Reporting And Analysis | P1 | functional |
| [REQ-DOC-005](#req-doc-005) | Management Scope | P1 | constraint |
| [REQ-DOC-006](#req-doc-006) | Iterative Development And Review | P2 | constraint |
| [REQ-DOC-007](#req-doc-007) | SRS Readability And Detail | P2 | constraint |
| [REQ-DOC-008](#req-doc-008) | Requirements Foundation | P3 | constraint |
| [REQ-DOC-009](#req-doc-009) | Staff Report Content Creation | P3 | functional |
| [REQ-DOC-010](#req-doc-010) | Reports Testing Governance | P2 | constraint |
| [REQ-DOC-011](#req-doc-011) | Reports Requirements Inventory | P2 | functional |
| [REQ-DOC-012](#req-doc-012) | SRS Requirement Contributions | P3 | functional |
| [REQ-DOC-013](#req-doc-013) | Library Manager Responsibilities | P3 | functional |
| [REQ-DOC-014](#req-doc-014) | Separate Missing And In-Transit Requirements | P3 | constraint |
| [REQ-DOC-015](#req-doc-015) | Management Of Library Services | P3 | functional |

## 6. Detailed Requirements

### 6.1 Reporting and Querying (RPT)

Report types, report templates, ad hoc queries, filtering, aggregation, scheduling, queuing, output formats, delivery, dashboards, and report usability.

<a id="req-rpt-001"></a>
#### REQ-RPT-001: Material Volume Reporting

- **Priority:** P1 (Must have) - Accurate material-volume reporting is an essential reporting capability and retains its existing P1 priority.
- **Type:** functional
- **Derived from:** D01 (`conversations/conv_pines014_material_volume.eml`), D10 (`early_draft_srs_galecia.txt`), D15 (`interview_cataloging_2009-05-08.txt`)

The system shall provide a consolidated material volume report for a selected library location and date. The report shall count active item records assigned to that location as of the selected date, excluding deleted or withdrawn records; shelf count shall include available items not checked out, and circulation count shall include checked-out items. Total count shall equal shelf count plus circulation count, while new acquisitions shall be a separately reported subset added during the selected acquisition period. Deleted records shall not contribute to current material counts, including current last-copy counts; historical last-copy events may be shown separately and labeled as historical. The system shall support historical dates, date-range comparisons, 30-, 60-, and 90-day acquisition periods, configurable grouping and filtering, and monthly board reporting.

<details><summary>Evidence (14 source statements)</summary>

- D01: "The system should provide the ability to report on the volume of material in a given library at any point in time, based on:"
- D01: "The volume should include: 1. New acquisitions (items recently added) 2. Items on the shelf (checked in) 3. Items out in circulation (checked out)  I think Maria is asking for all three counts separately plus a total."
- D01: "The report should allow breaking down volume in categories such as: - Total items in library - Number of holds - Number of adult fiction - Number of board books - Other customizable categories"
- D01: "Can we make the categories customizable? Different libraries might want different breakdowns."
- D01: "I assume items that are checked out still count toward your total volume, right?"
- D01: "Counts all items with a location = your library"
- D01: "Groups by categories (fiction/non-fiction, format, etc.)"
- D01: "Shows breakdowns with holds count per category"
- D01: "We can also add date filters - volume at any point in time, not just current. This would be useful for historical comparisons."
- D01: "It would be helpful to see how much volume has been added in the last 30/60/90 days."
- D01: "I'm currently pulling it manually from three different screens. :("
- D01: "We need this for our monthly board report"
- D10: "Ability to report on the volume of material in a given library at any point in time, based on new acquisitions, items on the shelf, and items out in circulation. The report should allow breaking down volume in categories such as: total items in library, number of holds, number of adult fiction, number of board books, etc."
- D15: "The material volume report helps me understand how much we have. I need to report on volume based on acquisitions, items on shelf, and items in circulation, broken down by categories like total items, holds, adult fiction, board books, etc."

</details>

<a id="req-rpt-002"></a>
#### REQ-RPT-002: Library Location Capacity Reporting

- **Priority:** P2 (Should have) - Capacity reporting is a clear, high-value staff need for regular collection monitoring, but is not marked critical.
- **Type:** functional
- **Derived from:** D02 (`conversations/conv_pines015_capacity_interface.eml`), D10 (`early_draft_srs_galecia.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`)
- **Merged with:** REQ-COL-020 (during review)

The system shall provide an aggregated capacity overview across library locations in a library system and allow staff to drill down to each associated library location for daily monitoring. Authorized administrators shall configure the applicable capacity measure for each location, such as item count against shelf-space capacity, physical items against a limit, or circulation volume against processing capacity. For percentage-based measures, under capacity shall be below 80%, getting full shall be from 80% to below 100%, and at or over capacity shall be 100% or greater; for absolute-limit measures, the configured limit shall define the same status boundaries. The system shall identify the location and measure, show the value and status, support grouping, sorting, filtering, trends, and CSV export, and recalculate status when the underlying count or configured limit changes.

<details><summary>Evidence (13 source statements)</summary>

- D02: "As a branch manager, I need to see the capacity of all branches in our system, not just my own."
- D02: "1. A high-level summary view (all branches, key metrics)"
- D02: "2. Ability to drill down into individual branches"
- D02: "Maybe color-coding - green for under capacity, yellow for getting full, red for at/over capacity"
- D02: "The data is centralized in our database, so we can build queries that aggregate across all branches."
- D02: "Also, what specific metrics define "capacity"? Is it: - Number of items vs. shelf space? - Number of physical items vs. a configured limit? - Circulation volume vs. processing capacity?"
- D02: "I'd want to be able to sort and filter. By region, by library type, by current load..."
- D02: "And export to CSV for the directors who want spreadsheets."
- D02: "One more thing - can the capacity interface also show trends? Like, is this branch growing or shrinking?"
- D02: "Maybe we should group by system/region? Or allow filtering?"
- D10: "Analyzing branch capacity and optimal distribution of the collection."
- D10: "The system should provide an interface showing the capacity of all branches."
- D18: "Inventory and capacity reports are used daily"

</details>

<a id="req-rpt-003"></a>
#### REQ-RPT-003: Shelf Space Utilization Reporting

- **Priority:** P2 (Should have) - Shelf-space analysis is an important collection-management aid used to inform redistribution decisions.
- **Type:** functional
- **Derived from:** D03 (`conversations/conv_pines016_shelf_space.eml`), D10 (`early_draft_srs_galecia.txt`), D15 (`interview_cataloging_2009-05-08.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`)
- **Merged with:** REQ-COL-021 (during review)

The system shall provide shelf-space utilization reports comparing, for each genre and format, circulation share, collection share, and share of total shelf space. It shall calculate collection share from item counts, circulation share from checkout totals for the selected period, and shelf-space share from item dimensions or item count as an explicitly identified proxy. Reports shall support comparisons by library location and across a library system, date-range comparisons, and the library system average. Results shall support staff decisions about redistribution without automatically moving materials, and reports shall support quarterly generation for directors.

<details><summary>Evidence (15 source statements)</summary>

- D03: "for each genre and format of material, the ability to compare: - The percentage of total circulations - The percentage of the collection - The percentage of total shelf space"
- D03: "The report should be able to run per library and per system."
- D03: "Can we also filter by date range? Like, what was the shelf space utilization in Q1 vs. Q2?"
- D03: "Also, can we include a "comparison" view that shows each library's breakdown side by side?"
- D03: "Count items per genre/format (this is the "percentage of collection")"
- D03: "Sum checkouts per genre/format (this is the "percentage of circulations")"
- D03: "Estimate shelf space per genre/format (this is the "percentage of shelf space")"
- D03: "Shelf space isn't directly tracked in the database. We'd need to estimate based on item dimensions or use item count as a proxy."
- D03: "Currently I pull reports manually and make spreadsheets. It's tedious."
- D03: "This way branch managers can see their local situation AND see how they compare to the system average."
- D03: "Being able to redistribute based on data would help."
- D03: "Our directors review this data quarterly and need both views."
- D10: "For each genre and format of material, ability to compare:   - The percentage of total circulations   - The percentage of the collection   - The percentage of total shelf space  The report should be able to run per library and per system."
- D15: "The shelf space report is important for collection management. For each genre and format, I need to compare: - Percentage of total circulations - Percentage of the collection - Percentage of total shelf space"
- D18: "Shelf space utilization reports are important"

</details>

<a id="req-rpt-004"></a>
#### REQ-RPT-004: Ad Hoc Query Builder

- **Priority:** P2 (Should have) - Ad hoc querying is a valuable reporting capability, but preset reports and templates provide a workaround for many users.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D12 (`email_report_features.eml`), D14 (`evergreen_reference_2009.txt`), D20 (`survey_results_2009.txt`)

The system shall provide staff members with a query builder for bibliographic records, item records, patrons, transactions, and financial data. For each supported data domain, the builder shall present the reporting fields available to the user, including field names and data types, and allow selection of fields, values, and criteria for inclusion in a report. It shall support ECMAScript regular-expression criteria, AND and OR operators, and parentheses; parentheses shall take precedence, followed by AND and then OR. Where values have selectable names, the interface shall allow selection by displayed name without requiring an internal identifier. Acceptance testing shall verify field selection, value selection, filtering, and each supported operator against known test data.

<details><summary>Evidence (13 source statements)</summary>

- D10: "The system should provide a user-friendly interface for designing queries against all record types (bibliographic, item, patron, transaction, financial)."
- D10: "The system should provide a user-friendly interface for designing queries against all record types (bibliographic, item, patron, transaction, financial)."
- D10: "Staff should be able to: - Select fields to query"
- D10: "Staff should be able to: - Select values from a picklist of possible values"
- D10: "Staff should be able to: - Select regular expressions from a drop-down menu"
- D10: "Staff should be able to: - Use a full range of Boolean operators"
- D10: "Check off any part of data you want"
- D12: "QUERY TOOL: We need a user-friendly interface for designing queries against all record types. Staff should be able to select fields to query, select values from picklists, use regular expressions from a dropdown, and use Boolean operators."
- D14: "No Boolean operators (AND/OR) beyond simple filters"
- D14: "Complex queries are difficult to construct"
- D14: "Limited field selection (not all database fields are available)"
- D14: "No regular expression support"
- D20: ""Can't filter by some fields that should be available""

</details>

<a id="req-rpt-005"></a>
#### REQ-RPT-005: Saved Queries

- **Priority:** P2 (Should have) - Saved queries are a clearly requested efficiency improvement for recurring work, but manual query creation remains a workaround.
- **Type:** functional
- **Derived from:** D15 (`interview_cataloging_2009-05-08.txt`), D20 (`survey_results_2009.txt`)

The system shall allow authorized staff members to create and save a named saved query containing its criteria, selected fields, and output settings, then run it again without rebuilding those elements. The creator or an authorized administrator shall be able to share access with specified staff members or roles, and the system shall enforce those permissions when a saved query is viewed, changed, run, or scheduled. Authorized users shall be able to schedule a saved query for periodic execution, including monthly reporting, and review its execution results.

<details><summary>Evidence (3 source statements)</summary>

- D20: "Ability to save and reuse queries: 73%"
- D20: "Save queries for repeated use: 58%"
- D15: "Second, we need to save these queries for repeated use - we do this monthly."

</details>

<a id="req-rpt-006"></a>
#### REQ-RPT-006: Report Template Management

- **Priority:** P2 (Should have) - Reusable and shared report templates are an important, regularly useful reporting capability, but reporting remains possible through other interfaces.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D12 (`email_report_features.eml`), D14 (`evergreen_reference_2009.txt`), D17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), D20 (`survey_results_2009.txt`)

The system shall allow administrators to create, name, and make report templates available to staff members, including templates intended for all library locations. A report template shall be a reusable definition of report criteria, fields, and presentation; running a template as-is shall preserve its saved criteria, while permitted edits shall apply only to the current run unless explicitly saved by an authorized user. Authorized users shall be able to clone an existing template into a new template. Template configuration shall identify which criteria and display fields may be changed and which staff roles may make those changes. Staff members shall be able to add permitted display fields, including shelving location, to a template, but shall not change a template to display deleted items unless authorized. The system shall support shared templates for standard reports such as a weeding report.

<details><summary>Evidence (16 source statements)</summary>

- D10: "System administrators should be able to create report templates that are available to staff."
- D10: "These templates should be runnable as-is or modifiable for individual needs."
- D10: "Changes to templates should not compromise the accuracy of results."
- D10: "For example, front-line staff could set a call number range for a weeding report or add/remove display fields from a pick list, but they should not be able to alter the template to display deleted items."
- D10: "Ability to edit canned report for display purposes such as adding shelving   location as a display"
- D12: "REPORT TEMPLATES: Admins need to create report templates that are available to staff."
- D12: "Templates should be runnable as-is or modified. Changes shouldn't compromise results."
- D12: "We also need the ability to "clone" reports - take an existing template and create a new one based on it."
- D12: "We want to make sure that when the director asks for "the weeding report," everyone runs the same report with the same criteria. Templates ensure this."
- D14: "No ability to edit canned report display options"
- D14: "No report template management system"
- D17: "Determine and create templates needed for all PINES libraries."
- D18: "Determine and create templates needed for all PINES libraries."
- D20: "Ability to create report templates: 81%"
- D20: "Report templates can be created by administrators and run as-is or modified."
- D20: "Report templates can be created by administrators and run as-is or modified."

</details>

<a id="req-rpt-007"></a>
#### REQ-RPT-007: Organize Report Templates

- **Priority:** P3 (Could have) - Folder organization improves discoverability but is a usability enhancement rather than a core reporting capability.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`)

The system shall allow administrators to create shared folders to organize report templates by an administrator-defined name and hierarchy. Administrators shall be able to move report templates between folders and assign descriptive folder names. Folder organization shall not grant permission to run a report; report execution permissions and ad hoc reporting access shall be controlled by REQ-SEC-006. Authorized staff members shall be able to browse the folders available to them.

<details><summary>Evidence (3 source statements)</summary>

- D10: "System administrators should be able to create shared folders to allow or disallow staff from running specific reports, and/or to run ad hoc reports on specific sets of data."
- D10: "System administrators should be able to create shared folders to allow or disallow staff from running specific reports, and/or to run ad hoc reports on specific sets of data."
- D14: "No shared folders concept"

</details>

<a id="req-rpt-008"></a>
#### REQ-RPT-008: Existing Query Tool Integration

- **Priority:** P3 (Could have) - Integration improves consistency and usability, but the reporting system can remain usable with another supported selection workflow.
- **Type:** constraint
- **Derived from:** D04 (`conversations/conv_pines018_item_transfer.eml`)

The system shall make the existing report query tool available from the report-design workflow used to select candidate records. The query tool shall create selection criteria for the report rather than duplicating that function in a separate query mechanism. The system shall pass the criteria selected in the tool to the report and apply them to the specified report data. Acceptance testing shall verify that a known set of criteria selects the same records when applied through this workflow as when applied directly in the existing query tool.

<details><summary>Evidence (1 source statements)</summary>

- D04: "Query builder for candidate selection - we can reuse the report query tool for this."

</details>

<a id="req-rpt-009"></a>
#### REQ-RPT-009: Reporting Interfaces

- **Priority:** P2 (Should have) - Multiple reporting options are important for regular work, while the system remains usable with a subset of these interfaces.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`)

The system shall provide fixed reports, report templates, and ad hoc reports as distinct reporting options. A fixed report shall use system-defined criteria and fields; staff members may run it immediately or schedule recurring execution but shall not modify its definition. A report template shall provide a reusable, named definition of criteria, fields, and presentation that authorized staff members may run or modify within its configured permissions. An ad hoc report shall allow staff members to define selection criteria and display fields for a single report run. The system shall provide starting report templates for circulation, patrons, item records, bills, and bibliographic records, and identify the report option and its permitted modifications in the interface.

<details><summary>Evidence (8 source statements)</summary>

- D10: "Three interfaces are needed:   a) Canned reports - generic reports set to run by the individual either ASAP      or recurring   b) Noncanned or On Demand Reports - preset but have the ability to edit      selection criteria and display options   c) Open Template Reporting - all attributes associated with circulation,      items, patrons, bills, and bibs to select from for filtering and display"
- D10: "Canned reports are generic reports set to run by the individual either ASAP or recurring."
- D10: "There should be a certain set of templates that are pre-written and delivered with the product."
- D10: "On Demand Reports would be for pre-selected criteria but for things like maintenance reports or collections development and would be set to run on demand."
- D10: "Noncanned or On Demand Reports - preset but have the ability to edit selection criteria and display options"
- D10: "Open template would have all attributes associated with say circulation, patrons, items, bills, and bibs to select from for filtering and the same attributes for displaying."
- D14: "Three interfaces (canned, on-demand, open template) - only basic canned exists"
- D14: "Open Template Reporting - does not exist"

</details>

<a id="req-rpt-010"></a>
#### REQ-RPT-010: Operational And Collection Report Catalog

- **Priority:** P2 (Should have) - A broad catalog of operational and collection reports is important for regular work, but individual reports can be delivered incrementally.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`), D15 (`interview_cataloging_2009-05-08.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), D20 (`survey_results_2009.txt`)
- **Merged with:** REQ-COL-022, REQ-COL-024 (during review)

The system shall provide an authoritative catalog of fixed reports, report templates, and supported ad hoc reporting capabilities for operational, collection, and data-quality use. A fixed report shall have system-defined criteria and fields; a report template shall provide reusable criteria, fields, and presentation that authorized users may modify only as permitted; ad hoc reporting shall allow users to define criteria and fields for a report run. The catalog shall include the specified circulation, item, patron, financial, hold, custom-report, and data-quality topics, including invalid item types, long call numbers, bibliographic records without item records, missing MARC fields, item counts and statuses, item additions, edits and deletions, checkout and overdue activity, claims returned, use-count thresholds, last copies, items to convert, and in-transit items with outstanding holds or excessive transit duration. It shall also include the specified weeding, bibliographic-record content, age and price by call number or shelving location, fines-stopped reasons, circulation modifier, Dewey classification, MARC field, circulation location by patron county, overdue contact information, sent notice, bibliographic-record count and change, and missing-item topics. Each catalog entry shall identify its report option, purpose, criteria, fields, output, and whether its definition is fixed or modifiable.

<details><summary>Evidence (26 source statements)</summary>

- D10: "These should include basic statistics like those required by the Georgia Annual Report and Application for State Aid."
- D10: "Examples of periodic reports include:   - Bibliographic records with holds   - Items that have not been checked out in X days   - Item-level holds   - Items with invalid item type   - In-transit items with outstanding hold   - Items that have been in-transit for more than X days   - Items that are the last copy in the system   - Items with a long call number   - Missing items   - Bibliographic records with no item records   - Patrons with invalid home library"
- D10: "Examples of periodic reports include:   - Bibliographic records with holds   - Items that have not been checked out in X days   - Item-level holds   - Items with invalid item type   - In-transit items with outstanding hold   - Items that have been in-transit for more than X days   - Items that are the last copy in the system   - Items with a long call number   - Missing items   - Bibliographic records with no item records   - Patrons with invalid home library"
- D10: "ITEMS REPORTS: - Items Added Count - Items Deleted Count - List of Items Added - Items Edited Count - Items Count - List of Items by Fines Stopped Reason - Items Currently Checked Out - Items more than XX days overdue (Overdue Materials Report) - Items marked longoverdue by system - List of Items with a > Total Use Count - List of Items with a < Total Use Count [Weeding Report] - Last Copy Report (last copy owned by a library system that was deleted) - List of Items by Creation Date Range - List of Items with a status of Missing - List of Items in Transit by both sending library and destination library - Claims returned - List of Long Overdue - Weeding report (date of last circulation and number of circs) - List of items with XXX in bib record - Age of collection by call number or shelving location - Price value of collection by call number or shelving location - Items to be Converted (batch converting items from one status to another)"
- D10: "BIB RECORDS REPORTS: - Bib Records Count - Bib Records Edited Count - Bib Records Added by user by library Count - Bib Records with No Volumes attached - Bib Records missing specific MARC fields"
- D10: "Ability to run reports for pre-overdue, overdue, and holds notices sent"
- D14: "The management processes reporting system needs to:  1. Expand the available report types to cover all identified gaps"
- D14: "Circulation Count by Circ Modifier (partially available)"
- D14: "Circulation Count by Dewey (not available)"
- D14: "Circulation Count by MARC fields (not available)"
- D14: "Circulation Count by Circ Location broken down by Patron County (not available)"
- D14: "Items Edited Count (not available)"
- D14: "List of Items by Fines Stopped Reason (not available)"
- D14: "Items more than XX days overdue with patron contact info (not available)"
- D14: "List of Items with specific Total Use Count (not available)"
- D14: "List of Items by Creation Date Range (not available)"
- D14: "Weeding report with date of last circulation (partially available)"
- D14: "Age of collection by call number (not available)"
- D14: "Price value of collection by call number (not available)"
- D14: "Bib Records Edited Count (not available)"
- D14: "Bib Records Added by user by library Count (not available)"
- D14: "Bib Records missing specific MARC fields (not available)"
- D15: "Data quality reports - items with invalid item type, items with long call numbers, bibliographic records with no item records."
- D18: "Data quality reports are needed"
- D18: "Weeding reports are frequently used"
- D20: "- Circulation reports (checkouts, check-ins, renewals): 78%   - Item reports (inventory, weeding, missing): 65%   - Patron reports (demographics, inactive accounts): 52%   - Financial reports (fines, payments): 34%   - Hold reports (placed, filled, stale): 41%   - Custom/on-demand reports: 29%"

</details>

<a id="req-rpt-011"></a>
#### REQ-RPT-011: Board And Executive Reports

- **Priority:** P2 (Should have) - Board and executive reporting is requested in D10, D12, D17, and D18, but no explicit critical marker or survey percentage is provided for this specific report group.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D12 (`email_report_features.eml`), D17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`)

The system shall provide predefined board and executive reports for library managers, library administrators, library boards, and other intended external consumers. It shall include basic statistics required by the Georgia Annual Report and Application for State Aid, plus activity measures for checkouts, check-ins, holds placed, and holds filled. It shall support cross-tabulation by terminal, library location, library system, hour, age range, patron type, and patron location. It shall provide an Executive Reports Interface and aggregated high-level outputs suitable for strategic planning, evaluation, and board presentations.

<details><summary>Evidence (8 source statements)</summary>

- D10: "They use reports for planning and evaluation."
- D10: "They require aggregated, high-level reports for strategic planning and board presentations."
- D10: "The system should provide pre-defined reports for consumption by library boards and other external consumers."
- D10: "These should include basic statistics like those required by the Georgia Annual Report and Application for State Aid."
- D12: "BOARD REPORTS: Pre-defined reports for library boards with basic statistics (Georgia Annual Report requirements). Activity reports showing traffic and volume of use - checkouts, check-ins, holds placed, holds filled. Cross-tabulated per terminal, per branch, per system, per hour, per age range, per patron type, per patron location."
- D17: "Compile a list of reports needed for an Executive Reports Interface."
- D18: "Board/executive reports need to be pre-defined"
- D18: "Compile a list of reports needed for an Executive Reports Interface."

</details>

<a id="req-rpt-012"></a>
#### REQ-RPT-012: Report Specification Coverage

- **Priority:** P1 (Must have) - The approved report baseline is a prerequisite for acceptance testing, so it is P1 under the stated priority scale.
- **Type:** constraint
- **Derived from:** D10 (`early_draft_srs_galecia.txt`)

The system shall maintain a controlled, versioned report-specification baseline for the required reports and outputs. Before acceptance testing begins, the requirements owner shall attach Appendix A and Appendix B or an approved manifest that enumerates every required report and output, its criteria, fields, and expected results, and records the baseline version, approval authority, and approval date. The requirements owner shall approve manifest changes through documented change control, issue a new version, and identify any affected acceptance tests. The system shall support every report and output in the approved baseline. Acceptance testing shall execute each enumerated report against its stated criteria and verify its fields and outputs against the approved manifest; acceptance shall not begin until the baseline is approved.

<details><summary>Evidence (2 source statements)</summary>

- D10: "The system must be able to support the reporting definitions as described in the attached report examples (see Appendix A)."
- D10: "The system must be able to support the fine-grained reports requirements as described in the attached specification (see Appendix B)."

</details>

<a id="req-rpt-013"></a>
#### REQ-RPT-013: Report Queue Status

- **Priority:** P1 (Must have) - Queue visibility is essential to the operation and monitoring of report execution.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D12 (`email_report_features.eml`), D14 (`evergreen_reference_2009.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), D20 (`survey_results_2009.txt`)

The system shall show staff members the position and status of each report they submitted in the report queue, including the number of reports ahead and the submission time. Permitted statuses shall be waiting, running, completed, failed, and cancelled. A queued report cancelled before execution shall transition to cancelled without running; a running report shall transition to cancelled only after execution has stopped in response to an accepted cancellation request. The system shall update and display status changes in the reporting interface.

<details><summary>Evidence (10 source statements)</summary>

- D10: "Staff should be able to see where their report is in the queue of reports waiting to run."
- D12: "Ability to see where your report is in the queue."
- D12: "- How many reports are ahead of theirs"
- D12: "- When their report was submitted"
- D12: "- Status (waiting, running, completed, failed)"
- D14: "3. Add report queue visibility and status indicators"
- D14: "No report queue visibility (staff can't see where their report is in queue)"
- D18: "Report queue visibility is important"
- D20: "Report queue visibility (where my report is in the queue): 68%"
- D20: ""I can't see if my report is still processing""

</details>

<a id="req-rpt-014"></a>
#### REQ-RPT-014: Report Queue Prioritization

- **Priority:** P1 (Must have) - The July feature request calls prioritization crucial and gives a board report jumping ahead of an ad hoc query as the explicit example; D10 and D14 also request it.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D12 (`email_report_features.eml`), D14 (`evergreen_reference_2009.txt`)

The system shall allow authorized users or configured report rules to prioritize reports in the report queue. It shall allow high-priority reports, such as a director's board report, to be moved ahead of lower-priority reports such as ad hoc queries. It shall display each report's priority with its queue status and position so staff members can understand the execution order. It shall retain the queue ordering according to the assigned priorities when reports are submitted or reprioritized.

<details><summary>Evidence (5 source statements)</summary>

- D10: "Ability to prioritize certain types of reports so they will pop to the top of   the queue over resource-consuming reports"
- D12: "Also, the ability to prioritize certain reports is crucial. A director's board report should be able to jump ahead of a staff member's ad-hoc query."
- D14: "No ability to prioritize certain types of reports"
- D12: "7. REPORTS QUEING: See position in queue, status, priority."
- D12: "Also, the ability to prioritize certain reports is crucial. A director's board report should be able to jump ahead of a staff member's ad-hoc query."

</details>

<a id="req-rpt-015"></a>
#### REQ-RPT-015: Report Scheduling

- **Priority:** P2 (Should have) - Recurring report scheduling received 52% support in the survey, and hourly scheduling and multiple execution frequencies are specified in D10 and D14.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`), D20 (`survey_results_2009.txt`)

The system shall allow staff members to schedule reports to run immediately, hourly, daily, weekly, monthly, or yearly. It shall support recurring reports and allow a report to use a selected relative period such as yesterday, last week, last month, or last year. It shall allow saved queries and canned reports to be scheduled for repeated execution. It shall support scheduling options for reports intended for routine operational and collection-management work.

<details><summary>Evidence (7 source statements)</summary>

- D10: "Canned reports are generic reports set to run by the individual either ASAP or recurring."
- D10: "Will have the ability for it to run by yesterday's data, last week's, last month's, or last year's."
- D10: "Ability to select Run ASAP, Hourly, Daily, Weekly, Monthly, Yearly"
- D14: "No hourly scheduling"
- D14: "No ability to select Run ASAP, Hourly, Daily, Weekly, Monthly, Yearly"
- D20: "Ability to schedule recurring reports: 52%"
- D20: "Ability to schedule recurring reports: 52%"

</details>

<a id="req-rpt-016"></a>
#### REQ-RPT-016: Combined Report Runs

- **Priority:** P3 (Could have) - Running multiple reports together is requested in D10 and identified as a gap in D14, with no priority marker or survey percentage.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`)

The system shall allow staff members to select multiple canned reports and submit them to run at the same time. It shall make the results of the selected reports available together in one document. It shall preserve the individual report results and their identifying information within the combined output. It shall support this workflow from the report selection interface.

<details><summary>Evidence (2 source statements)</summary>

- D10: "Canned reports can be checked off from a list to run at the same time and will be viewed within one document."
- D14: "No ability to check multiple reports to run at the same time"

</details>

<a id="req-rpt-017"></a>
#### REQ-RPT-017: Report Output Formats

- **Priority:** P2 (Should have) - Multiple output formats received 61% support in the survey, and Excel, HTML, and CSV are explicitly required by the technical subcommittee.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`), D20 (`survey_results_2009.txt`)

The system shall produce report output in Excel, HTML, and CSV formats. It shall allow staff members to choose an available format when viewing or exporting report results. It shall preserve report data in the selected output so that it can be used for spreadsheet analysis, web viewing, or data exchange. It shall offer these formats for reports generated through the reporting interfaces.

<details><summary>Evidence (5 source statements)</summary>

- D10: "Output would be in Excel, HTML, and CSV format"
- D14: "4. Provide multiple output formats and scheduling options"
- D19: "Excel, HTML, and CSV formats are required."
- D20: "Multiple output formats (Excel, CSV, HTML): 61%"
- D20: "Multiple output formats (Excel, CSV, HTML): 61%"

</details>

<a id="req-rpt-018"></a>
#### REQ-RPT-018: Email Report Delivery

- **Priority:** P2 (Should have) - Email delivery received 45% support in the survey and is independently requested in the early draft and D14.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`), D20 (`survey_results_2009.txt`)

The system shall allow staff members to deliver report results by email to entered email addresses. It shall provide an address book for regularly used report recipients. It shall allow recipients to be associated with scheduled reports so that generated results can be sent without entering the addresses each time. It shall support updating the address book and recipient list when report delivery needs change.

<details><summary>Evidence (5 source statements)</summary>

- D10: "Ability to enter email addresses for report to be sent to - would be great to   have an address book of regularly used addresses"
- D14: "No email delivery (reports can only be downloaded from the web interface)"
- D14: "No address book for report delivery"
- D20: "Email delivery of reports: 45%"
- D20: "Email delivery of reports: 45%"

</details>

<a id="req-rpt-019"></a>
#### REQ-RPT-019: Recurring Report Editing

- **Priority:** P3 (Could have) - Editing recurring report selections and recipients is stated once in the early draft and has no independent priority evidence.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`)

The system shall allow users to edit a recurring report after it has been scheduled. It shall allow users to add or remove report selections and to change the email addresses associated with the recurring report. It shall apply the updated selections and recipients to subsequent executions without changing completed report results. It shall make the current schedule and delivery settings available for review before changes are saved.

<details><summary>Evidence (1 source statements)</summary>

- D10: "Ability to edit recurring reports by adding or removing report selections   as well as editing the email addresses"

</details>

<a id="req-rpt-020"></a>
#### REQ-RPT-020: Comparative Report Columns

- **Priority:** P3 (Could have) - The comparative output columns are described in the early draft alone and are not marked as critical or broadly prioritized.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`)

The system shall allow report output to include selected comparison columns for current and prior periods. It shall support columns for last month's circulation, the preceding month's circulation, the previous year's corresponding month, and percentage differences between the compared periods. It shall allow staff members to select the comparison fields appropriate to the report. It shall label the period and percentage calculations in the output so results can be interpreted.

<details><summary>Evidence (2 source statements)</summary>

- D10: "Ability to determine the output results in a way such that a result could have   one column for last month's circs, another for previous month's circ, a percent   difference column, previous year's month column, a percent difference from   last month to last year's month column"
- D10: "Ability to determine the output results in a way such that a result could have one column for last month's circs, another for previous month's circ, a percent difference column, previous year's month column, a percent difference from last month to last year's month column"

</details>

<a id="req-rpt-021"></a>
#### REQ-RPT-021: Uploaded File Report Filters

- **Priority:** P3 (Could have) - Uploading filter values is a desirable efficiency improvement for a narrow reporting workflow; users can enter criteria through the report interface as a workaround.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`)

The system shall allow staff members to upload a text file and use its contents as values for supported report filters. The system shall accept one identifier value per line, including barcodes and other identifier fields supported by the selected report, and shall show the accepted file format and the supported identifier fields before upload. It shall validate the file and report invalid lines with their line numbers without silently treating them as valid values. The system shall apply valid uploaded values to the selected report criteria and return matching records, allowing staff members to review validation results before running the report.

<details><summary>Evidence (2 source statements)</summary>

- D10: "Ability to upload a text file such as barcodes or TCN to use for filtering   on a report"
- D14: "No ability to upload text files for filtering (barcodes, TCNs)"

</details>

<a id="req-rpt-022"></a>
#### REQ-RPT-022: Pivot Table Output

- **Priority:** P3 (Could have) - Pivot table output is described as desirable in the survey and is also listed in the early draft and D14, but no critical marker is present.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`), D20 (`survey_results_2009.txt`)

The system shall provide pivot table output as an option for report results. It shall allow staff members to use the available report fields to summarize and arrange results in a pivot table presentation. It shall make pivot table output available alongside other supported report output formats. It shall preserve the underlying report data represented by the pivot table.

<details><summary>Evidence (4 source statements)</summary>

- D10: "Pivot table output"
- D14: "No pivot table output"
- D20: ""Pivot table output would be great""
- D10: "Pivot table output"

</details>

<a id="req-rpt-023"></a>
#### REQ-RPT-023: Report Cancellation

- **Priority:** P2 (Should have) - Cancellation is requested in D10, D14, D19, and the survey; the technical subcommittee confirms the processing approach is feasible.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`), D20 (`survey_results_2009.txt`)

The system shall allow users to cancel a report that is scheduled but has not started or is currently running. It shall check for cancellation signals during report processing and stop execution when cancellation is accepted. It shall update the report's status in the report queue to reflect cancellation. It shall make cancellation available for both scheduled and actively processing reports.

<details><summary>Evidence (5 source statements)</summary>

- D10: "Ability to cancel a report that has already been scheduled to run or is   currently running"
- D14: "No ability to cancel a running report"
- D19: "The ability to cancel a scheduled or running report is technically feasible, but requires the system to check for cancellation signals during report processing."
- D20: ""Ability to cancel a scheduled or running report""
- D10: "Ability to cancel a report that has already been scheduled to run or is currently running"

</details>

<a id="req-rpt-024"></a>
#### REQ-RPT-024: Null And Blank Result Inclusion

- **Priority:** P2 (Should have) - The requirement is independently repeated in D10, D14, D19, and the survey, including an explicit statement that nulls and blanks must be included.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`), D20 (`survey_results_2009.txt`)

The system shall include null and blank fields in report results, including when report criteria or display settings are applied. It shall not silently remove records from results solely because a selected field has a null or blank value. It shall retain the distinction between a missing value and a populated value in the report output. It shall apply this behavior consistently across report types and supported output formats.

<details><summary>Evidence (5 source statements)</summary>

- D10: "All nulls and blank fields must be included in the results no matter what is   being filtered or displayed"
- D14: "All nulls and blank fields included in results - current system may filter some nulls"
- D19: "All nulls and blank fields must be included in the results,"
- D20: ""All nulls and blank fields must be included in results""
- D10: "All nulls and blank fields must be included in the results no matter what is   being filtered or displayed"

</details>

<a id="req-rpt-025"></a>
#### REQ-RPT-025: Current-State Reporting

- **Priority:** P2 (Should have) - Timely operational reporting is important for daily work, though a limited delay has a workable alternative.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`), D20 (`survey_results_2009.txt`)

The system shall provide current-state reports for operational data, including items overdue today, by querying the applicable transaction and item data sources when the report runs. For data sources that cannot be queried live, the system shall refresh the reporting data at least once every five minutes and display the last refresh time. A report shall not be labeled current-state if its source data is older than five minutes, and historical-date reports shall use the selected past-date data rather than current values.

<details><summary>Evidence (4 source statements)</summary>

- D10: "Ability to have real time reporting"
- D14: "No real-time reporting (all reports are run on current data)"
- D19: "Some reports need to be real-time - like 'what's overdue today,' Others are historical - 'what was the bill amount on June 30th?'"
- D20: ""Real-time reporting for busy periods""

</details>

<a id="req-rpt-026"></a>
#### REQ-RPT-026: Historical Reporting Warehouse

- **Priority:** P2 (Should have) - Historical reporting is requested in D10, D14, D19, and the survey, including a specific need to retrieve past values after data changes.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`), D20 (`survey_results_2009.txt`)

The system shall provide a reporting warehouse that retains historical information for reporting across dates and periods. It shall allow staff members to retrieve what data looked like on a specified past date or date range, including historical values that have since changed, such as shelving location. It shall support historical comparisons and examples such as retrieving a bill amount on a specified date. It shall provide historical reporting separately from reports of current data.

<details><summary>Evidence (5 source statements)</summary>

- D10: "Ability to have historical reporting - a reporting warehouse such that data   can be acquired on a given date or date range"
- D14: "No historical reporting warehouse"
- D19: "Some reports need to be real-time - like 'what's overdue today,' Others are historical - 'what was the bill amount on June 30th?'"
- D19: "We probably need a reporting warehouse for historical data."
- D20: ""Historical reporting - I want to see what the data looked like on a specific date in the past, even if the shelving location has changed""

</details>

<a id="req-rpt-027"></a>
#### REQ-RPT-027: Report Criteria Display

- **Priority:** P2 (Should have) - Displaying report criteria is independently requested in D10, D12, and D14 to help users understand the results and selections applied.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D12 (`email_report_features.eml`), D14 (`evergreen_reference_2009.txt`)

The system shall display the query selections and date selection criteria used to generate a report alongside its results. It shall identify the report by name and show the selected date range at the top or bottom of the output. It shall make the criteria available to staff members reviewing, sharing, or interpreting the results. It shall present the criteria in a clear form that identifies the selections applied to the report.

<details><summary>Evidence (5 source statements)</summary>

- D10: "The system should provide the query selections along with the results, so users can see what criteria were used to generate the report."
- D12: "QUERY SELECTIONS: System provides query selections along with results."
- D14: "No selection criteria display in report results"
- D10: "Report results would include the date selection criteria at the top or bottom   to quickly see date range selected along with the name of the report"
- D10: "Selection criteria is clearly defined"

</details>

<a id="req-rpt-028"></a>
#### REQ-RPT-028: Report Quick Access And Descriptions

- **Priority:** P3 (Could have) - Improved report discovery is a usability enhancement and is not essential to report execution.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`), D20 (`survey_results_2009.txt`)

The system shall let staff members find and open an available report template in no more than three selections from the reporting landing page. The interface shall provide text search and filters by report category and library location where applicable. Before execution, each report entry shall display its name, purpose, required inputs, and last-modified date; selecting or focusing a report shall display its description without running it.

<details><summary>Evidence (6 source statements)</summary>

- D10: "================================================================================ 15. FINE-GRAINED REPORTING REQUIREMENTS"
- D10: "Ability to hover over each title of canned report/template with pop-up box   with description"
- D10: "15.5 Quick Access Interface"
- D14: "No quick access interface with pop-up descriptions"
- D14: "No hover tooltips for report titles"
- D20: ""The interface is confusing - I can't find the reports I need""

</details>

<a id="req-rpt-029"></a>
#### REQ-RPT-029: Accurate Report Row Presentation

- **Priority:** P2 (Should have) - Duplicate-row and MARC-field presentation problems are both reported by survey respondents as concrete obstacles to using report output.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D20 (`survey_results_2009.txt`)

The system shall export report data to Excel without introducing duplicate rows. It shall allow selected MARC fields to appear together on a single row of report output rather than being spread across multiple rows. It shall provide an output presentation that preserves the selected record relationships and fields. It shall make report results usable for staff members reviewing or analyzing the exported data.

<details><summary>Evidence (4 source statements)</summary>

- D10: "Ability to pull MARC record fields so that they appear on a single row of data"
- D20: ""I need to export to Excel but the data has too many duplicate rows""
- D20: ""Need to pull specific MARC fields but they're spread across multiple rows""
- D20: ""I need to export to Excel but the data has too many duplicate rows""

</details>

<a id="req-rpt-030"></a>
#### REQ-RPT-030: Survey Name Filtering

- **Priority:** P3 (Could have) - Selecting a survey by name is a usability improvement for a limited reporting workflow; users can use other supported filtering methods as a workaround.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`)

The system shall allow staff members to filter reports by selecting a survey name from the surveys available to the report, rather than requiring entry of an internal identifier. The system shall apply the filter to records associated with the selected survey and display the selected survey name in the query criteria presented with the results. If the selected survey is unavailable when the report runs, the system shall notify the user and shall not silently substitute a different survey.

<details><summary>Evidence (2 source statements)</summary>

- D10: "Ability to select the survey name and not have to enter the survey id for   filtering"
- D19: "The ability to filter by survey name rather than survey ID requires the system to resolve names to IDs internally."

</details>

<a id="req-rpt-031"></a>
#### REQ-RPT-031: Transaction Audit Filtering

- **Priority:** P3 (Could have) - The transaction filtering capability is specified once in the early draft and has no additional priority or usage evidence.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`)

The system shall allow staff members to report on transactions using a specified date and time, workstation, or staff member as selection criteria. It shall support combining those criteria when narrowing transaction results. It shall display the selected criteria with the report results. It shall make the resulting transaction details available through the report output.

<details><summary>Evidence (1 source statements)</summary>

- D10: "Ability to run a report on transactions that occurred on x date and time on x   workstation or by x staff"

</details>

<a id="req-rpt-032"></a>
#### REQ-RPT-032: Item Usage Reporting

- **Priority:** P2 (Should have) - Item use reporting appears in the early draft and as a specific missing report type in D14, with no explicit critical marker.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`)

The system shall report total use counts for items and allow use counts to be broken down by a selected date range. It shall support period groupings such as a fiscal year or individual month. It shall provide an item list filtered by a specified total use count. It shall allow staff members to use these results for item review and collection-management reporting.

<details><summary>Evidence (2 source statements)</summary>

- D10: "Ability to have a total use count on items as well as a use count broken down   by usage date range such as an FY use count or monthly use count"
- D14: "List of Items with specific Total Use Count (not available)"

</details>

<a id="req-rpt-033"></a>
#### REQ-RPT-033: Status Conversion Support Report

- **Priority:** P3 (Could have) - Status-conversion report support appears only in the early draft and has no stated priority or corroborating evidence.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`)

The system shall provide a report that assists staff members with batch conversion of statuses. It shall identify the records relevant to the selected status-conversion work. It shall make the report results available for use in the associated operational workflow. It shall provide report output that allows staff members to review the records before carrying out the batch conversion.

<details><summary>Evidence (2 source statements)</summary>

- D10: "The system provides a report to assist in the batch conversion of statuses"
- D10: "Ability to upload a text file such as barcodes or TCN to use for filtering on a report"

</details>

<a id="req-rpt-034"></a>
#### REQ-RPT-034: Custom Local Reporting

- **Priority:** P2 (Should have) - The survey identifies custom/local reports and gives specific use cases, while the early draft also describes collection-use analysis and staff productivity reporting.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D20 (`survey_results_2009.txt`)

The system shall support custom or local reports for collection development, program attendance tracking, and staff productivity analysis, including time spent per transaction. It shall allow staff members to select data and criteria appropriate to these report needs through ad hoc queries or report templates. It shall support analysis of library material use and staff workflow for planning and evaluation. It shall allow report users to review the resulting measures for their authorized data scope.

<details><summary>Evidence (3 source statements)</summary>

- D10: "Analyzing the Library collection and its use by patrons."
- D10: "Analyzing staff productivity and workflow."
- D20: "Among those who use custom reports, the most common are:   - Collection development reports   - Program attendance tracking   - Staff productivity reports (time spent per transaction)"

</details>

<a id="req-rpt-035"></a>
#### REQ-RPT-035: Patron Demographic Reporting

- **Priority:** P2 (Should have) - The survey supports patron reports at 52% and separately identifies age ranges and postal codes as useful demographic dimensions.
- **Type:** functional
- **Derived from:** D20 (`survey_results_2009.txt`)

The system shall provide patron demographic reports that support programming and planning. It shall include age ranges and postal codes as available demographic dimensions. It shall allow demographic results to be used in reports alongside patron report categories such as inactive accounts. It shall limit demographic output to the data and access permitted for the report user.

<details><summary>Evidence (1 source statements)</summary>

- D20: ""I use demographic data to plan programming. Age ranges and zip codes are most useful.""

</details>

<a id="req-rpt-036"></a>
#### REQ-RPT-036: Report Display Support

- **Priority:** P3 (Could have) - Indirect patron interaction through library displays is noted once in the March meeting minutes and is not presented as a critical requirement.
- **Type:** functional
- **Derived from:** D17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`)

The system shall allow report results to be presented on displays or screens at library locations for indirect patron interaction. It shall support staff members using reports to provide information through those displays without requiring patrons to operate the reporting interface. It shall make report output suitable for display in the relevant presentation context. It shall preserve the report's selected content when results are shown.

<details><summary>Evidence (1 source statements)</summary>

- D17: "[Note from Katherine: Patrons interact through OPAC; they may use reports indirectly through displays/screens at libraries]"

</details>

<a id="req-rpt-037"></a>
#### REQ-RPT-037: Cross-Location Comparison Reports

- **Priority:** P3 (Could have) - P3: The request for cross-location comparison reports appears in one set of meeting minutes from LaToya Davidson and has no stated critical-priority marker or supporting survey percentage.
- **Type:** functional
- **Derived from:** D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`)

The system shall provide reports that compare selected measures across library locations. It shall present results for multiple library locations in a form that enables staff members and managers to identify differences between locations. It shall support comparisons across the locations selected for a report and clearly identify each location in the output. It shall make these comparison reports available to authorized report users.

<details><summary>Evidence (1 source statements)</summary>

- D18: "Need for cross-branch comparison reports"

</details>

### 6.2 Collection and Inventory Management (COL)

Collection analysis, capacity, shelf space, item transfers, transit tracking, missing and damaged items, weeding, purging, last-copy workflows, uncataloged materials, and cataloging-related collection operations.

<a id="req-col-001"></a>
#### REQ-COL-001: Batch Item Transfers

- **Priority:** P1 (Must have) - The transfer utility was marked crucial by the senior cataloger, and batch transfer needs appear in the early draft and later interview.
- **Type:** functional
- **Derived from:** D04 (`conversations/conv_pines018_item_transfer.eml`), D10 (`early_draft_srs_galecia.txt`), D15 (`interview_cataloging_2009-05-08.txt`), D20 (`survey_results_2009.txt`)

The system shall support batch transfers of library materials between library locations and to destinations such as mobile libraries, outreach programs, and temporary event locations. Authorized staff members shall be able to update the selected item records to the destination and produce pull lists and printable transit labels with barcodes. Batch location updates shall be transaction-safe, and the transfer workflow shall support moving selected materials in one operation. This capability shall support collection operations such as moving a group of biographies to a community location for a workshop.

<details><summary>Evidence (10 source statements)</summary>

- D04: "I need a utility for transferring batches of items between branches."
- D04: "We often need to move books to a mobile library, to an outreach program, or to a "just-in-time" warehouse."
- D04: "Change records of selected items to new location"
- D04: "Batch update of location field - straightforward database update with transaction safety."
- D04: "Pull list generation - create a printable list of items to be moved."
- D04: "Also, can we generate transit labels? Like, printable barcodes for the items being transferred?"
- D10: "System should provide a utility for transferring batches of items between branches. Uses include: moving books into a mobile library, an outreach program collection, or a "just-in-time" warehouse.  The utility should include:   - Ability to query for candidate materials   - Ability to save queries for repeated use   - Ability to manually select titles from query results   - Ability to change records of selected items to move to new location   - Mechanisms for moving items: changing location field, generating pull lists   - Ability to revert items to original location after a set period of time"
- D15: "The item transfer utility is crucial for us. We often need to move batches of items between branches - for example, sending books to a mobile library unit or to an outreach program collection."
- D15: "Fourth, we need to change records of selected items to move them to a new location."
- D20: "Change records to move items to new location: 31%"

</details>

<a id="req-col-002"></a>
#### REQ-COL-002: Select Transfer Candidates

- **Priority:** P2 (Should have) - Candidate queries and manual selection were requested by multiple sources, and the survey reported 44% support for queries and 39% for manual selection.
- **Type:** functional
- **Derived from:** D04 (`conversations/conv_pines018_item_transfer.eml`), D15 (`interview_cataloging_2009-05-08.txt`), D20 (`survey_results_2009.txt`)

The system shall let staff members identify library materials that are candidates for transfer by querying on collection criteria. Query criteria shall include examples such as a section or collection area and circulation history, including items that have not circulated in six months. Staff members shall be able to select particular titles from query results, using individual selections such as check boxes, before taking transfer action. The results and selection shall make the chosen materials clear for review.

<details><summary>Evidence (7 source statements)</summary>

- D04: "Query for candidate materials"
- D04: "Manually select titles from query results"
- D04: "I should be able to check boxes and select which ones to include."
- D15: "First, we need to query for candidate materials. Maybe we want all items in the children's section that haven't circulated in 6 months."
- D15: "Third, we need to manually select titles from query results if we want to be more targeted."
- D20: "Query for candidate materials: 44%"
- D20: "Manually select from query results: 39%"

</details>

<a id="req-col-003"></a>
#### REQ-COL-003: Reuse Transfer Queries

- **Priority:** P1 (Must have) - Recurring transfer selection is an explicit operational need and supports collection-transfer work.
- **Type:** functional
- **Derived from:** D04 (`conversations/conv_pines018_item_transfer.eml`), D15 (`interview_cataloging_2009-05-08.txt`)

The system shall let authorized staff members use a saved query, as defined in REQ-RPT-005, to select collection-transfer candidates. The query shall retain its selection criteria so staff members can run it for recurring transfer work without rebuilding those criteria. The system shall enforce the saved query’s access permissions when it is used for transfer selection and shall identify the selected candidates before transfer processing begins.

<details><summary>Evidence (3 source statements)</summary>

- D04: "The 'save queries for repeated use' is crucial."
- D04: "Save/share queries - similar to report templates."
- D15: "Second, we need to save these queries for repeated use - we do this monthly."

</details>

<a id="req-col-004"></a>
#### REQ-COL-004: Revert Temporary Transfers

- **Priority:** P2 (Should have) - This is a clearly requested operational capability, but the system remains usable without automated transfer reversion because staff can manage transfers manually.
- **Type:** functional
- **Derived from:** D04 (`conversations/conv_pines018_item_transfer.eml`), D15 (`interview_cataloging_2009-05-08.txt`), D20 (`survey_results_2009.txt`)

The system shall return transferred item records to their original library location when an authorized staff member configures a qualifying date or event criterion. Date criteria shall specify a positive number of days after transfer, with reversion occurring when that number of days has elapsed. Event criteria shall include checkout at the destination or a configured status change, including returned or sold. Staff members shall be able to associate a transfer with an event or program and configure reversion when that event ends. The system shall evaluate eligible transfers once daily when automatic reversion is enabled, record the criterion and time of each reversion, and leave transfers unchanged when no configured criterion is met.

<details><summary>Evidence (8 source statements)</summary>

- D04: "Revert items to original location after a set period of time"
- D04: "- Revert after X days (date-based)"
- D04: "- Revert when item status changes to "returned" (event-based) - Revert when item is checked out at the destination (event-based)"
- D04: "Can we also revert "based on other criteria"? Like, if the item's status changes to "sold" at the book sale, automatically revert it?"
- D04: "Auto-revert mechanism - a scheduled task that checks transferred items and reverts them based on time or status criteria."
- D04: "Also, for the outreach program use case - can we transfer items to a temporary location for a specific event or program? Like, move 20 biographies to the community center for their genealogy workshop, then revert them after the event."
- D15: "And there should be mechanisms for reverting items back to their original location after a set period of time - like when a mobile library returns to base."
- D20: "Revert items to original location: 18%"

</details>

<a id="req-col-005"></a>
#### REQ-COL-005: Preview Transfers

- **Priority:** P3 (Could have) - The preview and confirmation workflow was requested by one stakeholder and has no stated critical marker or broader support.
- **Type:** functional
- **Derived from:** D04 (`conversations/conv_pines018_item_transfer.eml`)

The system shall show staff members a preview of the proposed transfer before applying changes to item records. The preview shall identify the number of items to be moved, their originating library location, and the destination library location. The system shall require staff confirmation before carrying out the transfer. For example, the preview shall be able to state that 25 items will move from one named library location to a named mobile library unit.

<details><summary>Evidence (1 source statements)</summary>

- D04: "Also, the utility should show a preview before making changes. "If you run this now, 25 items will be moved from Dalton-Whitman to Mobile Library Unit 3. Confirm?""

</details>

<a id="req-col-006"></a>
#### REQ-COL-006: Undo Transfers

- **Priority:** P3 (Could have) - The undo capability was requested by one stakeholder and was not given a critical priority marker.
- **Type:** functional
- **Derived from:** D04 (`conversations/conv_pines018_item_transfer.eml`)

The system shall provide staff members with a way to undo a mistaken transfer. Undo shall reverse the transfer's effect on the affected item records and restore their prior library location. The system shall make clear which transfer is being reversed and which item records it affects before applying the undo. The undo capability shall be available as a distinct action from automatic reversion rules.

<details><summary>Evidence (1 source statements)</summary>

- D04: "And we need an undo function!"

</details>

<a id="req-col-007"></a>
#### REQ-COL-007: Track Transfer History

- **Priority:** P2 (Should have) - Transfer logging was requested for audit purposes and transfer counts were separately requested by stakeholders, demonstrating operational value without a critical marker.
- **Type:** functional
- **Derived from:** D04 (`conversations/conv_pines018_item_transfer.eml`)

The system shall retain and present the transfer history associated with an item record for authorized staff members. The history shall allow staff to review prior transfers and determine how many times an item was transferred during a specified period. The system shall also log transfers for audit purposes so that transfer activity can be reviewed after the operation. For example, the history shall be able to report five transfers during the past year.

<details><summary>Evidence (2 source statements)</summary>

- D04: "Logging - track all transfers for audit purposes."
- D04: "Can we track transfer history? Like, "this item has been transferred 5 times in the past year.""

</details>

<a id="req-col-008"></a>
#### REQ-COL-008: Notify Staff Of Transfer Delays

- **Priority:** P3 (Could have) - This is a desirable improvement for a limited operational situation; staff can still identify and manage delayed transfers through reports.
- **Type:** functional
- **Derived from:** D04 (`conversations/conv_pines018_item_transfer.eml`)

The system shall notify configured staff members when an in-transit item has not arrived by its expected arrival time plus a configured grace period, or when its transfer enters a configured issue state. Authorized staff members shall configure the expected-arrival rule, a nonnegative grace period, issue states, recipients, and one or more notification channels enabled for the library system. The system shall evaluate these conditions at least hourly, send one notification per triggering condition, and include the affected transfer, item record, trigger, and detection time. If delivery fails, the system shall retry three times at 15-minute intervals and record the delivery outcome.

<details><summary>Evidence (1 source statements)</summary>

- D04: "And can we set up alerts? If an item transfer is delayed or has issues, notify me."

</details>

<a id="req-col-009"></a>
#### REQ-COL-009: Report Missing And Damaged Items

- **Priority:** P1 (Must have) - The per-location report was marked crucial for accountability and is independently requested in the early draft, interview, and later meeting minutes.
- **Type:** functional
- **Derived from:** D05 (`conversations/conv_pines019_020_missing_intransit.eml`), D10 (`early_draft_srs_galecia.txt`), D15 (`interview_cataloging_2009-05-08.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`)

The system shall provide reports of missing and damaged library materials by library location. Reports shall include item condition notes, such as water damage or vandalism, and shall support date ranges such as the last 30 days or the last quarter. Staff members shall be able to use the reports for accountability and auditing, including counts of items reported missing or damaged. The reports shall be accessible for routine collection review and operational follow-up.

<details><summary>Evidence (8 source statements)</summary>

- D05: "I want the missing/damaged report to be per branch. That's crucial for accountability."
- D05: "Also, can the report include item condition notes? Like "water damage" or "vandalism"?"
- D05: "The missing/damaged report can include date ranges (e.g., last 30 days, last quarter, etc.) which would be useful for trending."
- D05: "Auditing - showing how many items went missing/were damaged"
- D05: "Right now I have no easy way to generate a report of all these items per branch."
- D10: "The system should provide reports of missing and damaged items per branch."
- D15: "I need a report that shows all missing and damaged items per branch."
- D18: "Missing/damaged item reports are needed per branch"

</details>

<a id="req-col-010"></a>
#### REQ-COL-010: Analyze Missing And Damaged Patterns

- **Priority:** P2 (Should have) - This reporting capability is useful for regular collection-management work, but it is not essential to core system operation.
- **Type:** functional
- **Derived from:** D05 (`conversations/conv_pines019_020_missing_intransit.eml`), D15 (`interview_cataloging_2009-05-08.txt`)

The system shall report missing and damaged item records grouped by library location, title, and shelving location for a user-selected reporting period. Authorized staff members shall configure a positive minimum occurrence count, a positive time window, and a nonnegative comparison percentage. The system shall calculate each location's rate as distinct item records reported missing or damaged during the selected period divided by active item records at that location on the report date. It shall flag a location when its rate is greater than the library system average multiplied by one plus the configured comparison percentage. An occurrence count equal to the configured minimum shall qualify as repeated.

<details><summary>Evidence (3 source statements)</summary>

- D05: "if we keep losing the same titles, maybe we need different copies or to move them to a different location"
- D05: "If we see patterns (certain branches losing more items), we can investigate processes."
- D15: "This helps me track collection health and identify patterns - if the same shelf always has missing items, we might need to relocate it."

</details>

<a id="req-col-011"></a>
#### REQ-COL-011: Report In-Transit Items

- **Priority:** P1 (Must have) - This preserves the P1 priority of the existing requirement; monitoring in-transit items is an essential circulation and transfer operation.
- **Type:** functional
- **Derived from:** D05 (`conversations/conv_pines019_020_missing_intransit.eml`), D10 (`early_draft_srs_galecia.txt`), D15 (`interview_cataloging_2009-05-08.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`)
- **Merged with:** REQ-TRN-014 (during review)

The system shall provide a unified report of in-transit items, including views by sending library location and destination library location, and a view across the library system. The report shall identify items whose departure date is more than the configured number of days before the report date and whose arrival date is null; the default threshold shall be seven days, and an item exactly at the threshold shall not qualify as delayed. Staff members shall be able to filter by sending location, destination location, or both, and sort by departure date ascending or descending, with ascending order placing the oldest departures first. The report shall present items still in transit when it is run and support transfer coordination and investigation of delayed items.

<details><summary>Evidence (14 source statements)</summary>

- D05: ""System generates a list of items in-transit for more than X days (X configurable), per branch and per system.""
- D05: "(X should be configurable, probably 7 days default)."
- D05: "(X should be configurable, probably 7 days default)."
- D05: "And the report should merge transit-to and transit-from so front-line staff don't have to run two reports."
- D05: "System generates a list of items in-transit for more than X days (X configurable), per branch and per system."
- D05: "can we sort by due date? Front-line staff need to chase the oldest items first."
- D05: "For in-transit items, we need to check the transit table for items where the arrival date is null and the departure date is more than X days ago."
- D10: "The system should generate a list of items that have been in-transit for more than X days (X configurable), per branch and per system."
- D10: "The report should merge the transit-to and transit-from into one report for ease of front-line staff use."
- D10: "TRANSITS REPORTS: - Items In Transit to Destination Library - Items In Transit by Sending Library"
- D15: "The report should show items that have been in-transit for more than X days (configurable), per branch and per system."
- D15: "The report should show items that have been in-transit for more than X days (configurable), per branch and per system."
- D15: "It should merge the transit-to and transit-from into one report for ease of use."
- D18: "In-transit item reports are critical for delivery coordination"

</details>

<a id="req-col-012"></a>
#### REQ-COL-012: Identify Items For Purging

- **Priority:** P2 (Should have) - Customizable purge and weeding criteria appear in the early draft, interview, and stakeholder discussion, but no source marks this requirement critical.
- **Type:** functional
- **Derived from:** D06 (`conversations/conv_pines021_item_purging.eml`), D10 (`early_draft_srs_galecia.txt`), D15 (`interview_cataloging_2009-05-08.txt`)

The system shall identify item records that meet staff-defined criteria for purging and provide a read-only report of the resulting candidates. Criteria shall support item status, elapsed time in a status, and circulation activity, and staff shall be able to combine criteria using logical conditions. Examples shall include items missing for more than six months and not circulated for two years, or items marked discard/weed. Staff members shall be able to review the candidates before any deletion occurs.

<details><summary>Evidence (5 source statements)</summary>

- D06: "I need to identify item records to purge based on customizable criteria.    For example:    - Item has been in status "missing" for more than X months    - Item has status "discard/weed""
- D06: "I want the customizable criteria for purging to include: - Status-based criteria (missing, discard/weed, damaged) - Time-based criteria (in status for X months/years) - Activity-based criteria (last circulated X days/months/years)  Can we combine these? Like "items with status 'missing' for more than 6 months AND haven't circulated in 2 years"?"
- D06: "Reports show candidates for purging (read-only)"
- D10: "The system should provide a utility and reports for identifying item records to purge, based on customizable criteria such as:   - An item has been in status "missing" for more than X months   - An item has status "discard/weed""
- D15: "I need to identify items for purging based on customizable criteria. For example: - Item has been in status "missing" for more than X months - Item has status "discard/weed""

</details>

<a id="req-col-013"></a>
#### REQ-COL-013: Convert Item Statuses In Batch

- **Priority:** P1 (Must have) - A stakeholder described batch status conversion as huge for the collection management workflow, and the need is repeated in the early draft and cataloging interview.
- **Type:** functional
- **Derived from:** D06 (`conversations/conv_pines021_item_purging.eml`), D10 (`early_draft_srs_galecia.txt`), D15 (`interview_cataloging_2009-05-08.txt`)

The system shall let authorized staff members change the status of multiple item records in a batch operation. Staff members shall be able to identify the items to change, select a target status, and review the affected items before applying the conversion. The workflow shall support examples such as changing 100 items from missing to discard/weed. The system shall provide reporting that assists staff in identifying items for conversion and confirming the resulting work.

<details><summary>Evidence (4 source statements)</summary>

- D06: "The system should: - Provide a report to assist in the conversion of items from one status to   another"
- D06: "I need a report to help convert items from one status to another in batch.    Like changing 100 items from "missing" to "discard/weed" at once."
- D10: "The system should have a report to assist in the conversion of items from one status to another."
- D15: "Sometimes I need to change 100 items from "missing" to "discard/weed" in batch."

</details>

<a id="req-col-014"></a>
#### REQ-COL-014: Identify Last Copies

- **Priority:** P1 (Must have) - Identifying last copies is an essential collection-management capability and retains the requirement's existing P1 priority.
- **Type:** functional
- **Derived from:** D06 (`conversations/conv_pines021_item_purging.eml`), D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`), D15 (`interview_cataloging_2009-05-08.txt`)

The system shall provide a last copy report that identifies the only remaining item record for a bibliographic work within a selected scope. Staff members shall be able to run the report for an individual library location or the library system, and the report shall identify the scope used. Current last-copy counts shall include only non-deleted item records. The report may include deleted item records that were the last copy as separately labeled historical last-copy events, but shall not count those records as current last copies. The report shall support catalogers reviewing records for possible WorldCat updates.

<details><summary>Evidence (8 source statements)</summary>

- D06: "For the last copy report - is this per library or per system? I think we need both views."
- D06: "This is all great. One more thing - the "last copy report" should definitely be available per system, not just per library."
- D06: "For the last copy report, the system would check: for each item record, is this the only copy in the specified scope (library or system)? If yes, flag it."
- D10: "The system should provide a last copy report that singles out a library system's last copies, to assist catalogers who need to edit WorldCat entries."
- D10: "Ability to get a list of items deleted that was the last copy owned by the   library system in order to update WorldCat"
- D10: "Ability to run a report on deleted items that were the last copy in the   facility"
- D14: "Last Copy Report (partially available, needs enhancement)"
- D15: "The last copy report is CRITICAL. This singles out a library system's last copies, to assist catalogers who need to edit WorldCat entries."

</details>

<a id="req-col-015"></a>
#### REQ-COL-015: Support WorldCat Cataloging Workflows

- **Priority:** P1 (Must have) - The cataloging interview marked support for the WorldCat-related workflow critical, although it allows either integration or another form of assistance.
- **Type:** functional
- **Derived from:** D15 (`interview_cataloging_2009-05-08.txt`)

The system shall support catalogers performing WorldCat-related work by making last-copy information available in a form that can be used to update WorldCat entries. The workflow shall let catalogers identify the relevant bibliographic work and its last copy within the library system. The system shall support this cataloging task without requiring staff to determine last-copy status manually. This requirement covers the cataloging workflow and does not prescribe a particular WorldCat integration method.

<details><summary>Evidence (1 source statements)</summary>

- D15: "This singles out a library system's last copies, to assist catalogers who need to edit WorldCat entries."

</details>

<a id="req-col-016"></a>
#### REQ-COL-016: Delete Unneeded Catalog Records

- **Priority:** P2 (Should have) - This is a useful collection-cleanup function, but manual catalog maintenance provides a workaround if the function is unavailable.
- **Type:** functional
- **Derived from:** D06 (`conversations/conv_pines021_item_purging.eml`), D10 (`early_draft_srs_galecia.txt`), D15 (`interview_cataloging_2009-05-08.txt`)

The system shall let authorized staff members delete selected item records and delete a bibliographic record only when it has no item records attached. Before deletion, the workflow shall identify each affected record and show the relationship between the item records and bibliographic record. The system shall prevent deletion of a bibliographic record that still has an attached item record, and shall confirm completion or report why a requested deletion could not be performed. Staff members shall be able to use the function for collection cleanup and cataloging operations.

<details><summary>Evidence (3 source statements)</summary>

- D06: "We also need a quick way to delete volume entries along with copy entries, and delete records with no items attached."
- D10: "The system should provide a quick effective method of deleting volume entries along with copy entries, as well as records with no items attached."
- D15: "There also needs to be a quick, effective method for deleting volume entries along with copy entries, as well as records with no items attached."

</details>

<a id="req-col-017"></a>
#### REQ-COL-017: Schedule Purging Operations

- **Priority:** P3 (Could have) - Scheduled purging is a desirable efficiency improvement; manual operation provides a workable alternative.
- **Type:** functional
- **Derived from:** D06 (`conversations/conv_pines021_item_purging.eml`)

The system shall let authorized staff members run the purging and cleanup utility manually or schedule it for a specified date and time, including an annual schedule. A scheduled run shall apply the configured purge criteria and prepare a list of candidate records for review, but shall not delete records without the separate confirmation required by REQ-COL-018. The system shall record the schedule, criteria, run results, and confirming staff member, and shall support manual operation when scheduling is not appropriate.

<details><summary>Evidence (2 source statements)</summary>

- D06: "can the purging utility be scheduled? Like, run automatically at the end of each year?"
- D06: ""Should it be automated or manual?""

</details>

<a id="req-col-018"></a>
#### REQ-COL-018: Confirm Deletions

- **Priority:** P2 (Should have) - A separate deletion safeguard is important for preventing accidental loss of catalog or item data.
- **Type:** functional
- **Derived from:** D06 (`conversations/conv_pines021_item_purging.eml`)

The system shall require an authorized staff member to review and separately confirm each deletion operation before deleting item records or catalog records identified by the purging or cleanup workflow. The system shall display the records and count selected for deletion, and shall record the confirming staff member, confirmation time, and deletion outcome. A scheduled or configured operation shall stop at candidate preparation until this confirmation is provided; viewing a report or scheduling a run shall not constitute confirmation.

<details><summary>Evidence (1 source statements)</summary>

- D06: "A separate confirmation step for actual deletions"

</details>

<a id="req-col-019"></a>
#### REQ-COL-019: Track Uncataloged Materials

- **Priority:** P2 (Should have) - Tracking uncataloged materials is a clearly requested inventory and transaction-capture capability, though it is not essential to core cataloged circulation.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D15 (`interview_cataloging_2009-05-08.txt`)

The system shall track uncataloged library materials as inventory even when they do not have individual bibliographic records. Staff members shall be able to record each material's type, quantity, library location, and use transactions, and identify those transactions without requiring an item record for each material. The system shall make the captured transactions available to circulation reporting, where they shall be counted as non-cataloged activity and included in applicable total circulation measures. Incoming-material workflows shall support quick distribution while minimizing staff labor at each library location, including for paperback books and children's board books.

<details><summary>Evidence (6 source statements)</summary>

- D10: "Ability to control inventory of uncataloged material, such as paperback books and children's board books. Support needed for:   - Quick distribution   - Minimal branch labor   - Ability to identify how the material is being used  Ability to count transactions and include in circulation statistics and reports."
- D15: "We need to be able to track these as inventory even though they're not fully cataloged."
- D15: "The requirements are: quick distribution (we need to process these fast)"
- D15: "minimal branch labor (we can't spend a lot of time per item)"
- D15: "and ability to identify how the material is being used."
- D15: "We also need to be able to identify how the material is being used."

</details>

<a id="req-col-023"></a>
#### REQ-COL-023: Distinguish Edit And Circulation Dates

- **Priority:** P2 (Should have) - The cataloging interview requires separate edit and circulation dates, and a survey response and reference entry also request a distinct last-circulation date.
- **Type:** functional
- **Derived from:** D14 (`evergreen_reference_2009.txt`), D15 (`interview_cataloging_2009-05-08.txt`), D20 (`survey_results_2009.txt`)

The system shall present the item record's last edit date separately from its last circulation date in item reports. The last edit date shall reflect when the item record was edited and shall not be changed merely because the item circulated. Staff members shall be able to view the separate last circulation date when reviewing item activity and weeding candidates. The dates shall be clearly labeled so that users can distinguish editing activity from circulation activity.

<details><summary>Evidence (3 source statements)</summary>

- D14: "Ability to indicate last circulation date - not available as separate field"
- D15: "I need to be able to see the last edit date on reports, but it should be only when the item is edited and not include the last circulation. The current system combines these dates."
- D20: ""Ability to indicate last circulation date on item reports""

</details>

<a id="req-col-025"></a>
#### REQ-COL-025: Query Items By Status

- **Priority:** P3 (Could have) - Status-based querying was raised by one stakeholder and was not assigned a critical priority marker.
- **Type:** functional
- **Derived from:** D05 (`conversations/conv_pines019_020_missing_intransit.eml`)

The system shall let staff members query and group item records by item status. Status values shall include examples such as missing, lost, and long overdue, as applicable to the configured status set. The resulting groups shall support review of collection records and selection of materials for related reporting or operational work. The system shall present the status associated with each returned item record.

<details><summary>Evidence (1 source statements)</summary>

- D05: "The system currently tracks item status as "missing" or "long overdue" or various other statuses."

</details>

<a id="req-col-026"></a>
#### REQ-COL-026: Mark Items Missing

- **Priority:** P3 (Could have) - Marking items missing during monthly shelf reading was described in one interview and was not given a critical marker.
- **Type:** functional
- **Derived from:** D15 (`interview_cataloging_2009-05-08.txt`)

The system shall let authorized staff members mark item records as missing during collection operations such as shelf reading. The status change shall be recorded on the affected item record so that the item can be included in missing-item reports and subsequent collection workflows. Staff members shall be able to identify which item records they are updating. This capability shall support recurring shelf-reading work, including monthly reviews.

<details><summary>Evidence (1 source statements)</summary>

- D15: "We do monthly shelf reading and mark items as missing."

</details>

<a id="req-col-027"></a>
#### REQ-COL-027: Support Collection Batch Operations

- **Priority:** P3 (Could have) - Batch operations were emphasized in one cataloging interview, but the statement is broad and no critical priority marker is provided.
- **Type:** functional
- **Derived from:** D15 (`interview_cataloging_2009-05-08.txt`)

The system shall support batch operations for cataloging and collection management tasks. Authorized staff members shall be able to apply an operation to a selected set of item records where the specific workflow permits batch processing. The batch operation shall identify the affected records and the action to be performed. This capability shall support recurring work such as bulk status changes and other collection operations without requiring each record to be handled individually.

<details><summary>Evidence (1 source statements)</summary>

- D15: "He emphasized the importance of batch operations and data quality"

</details>

<a id="req-col-028"></a>
#### REQ-COL-028: Alert On Holds Purchase Activity

- **Priority:** P3 (Could have) - This is a desirable monitoring enhancement, but staff can review holds-purchase activity using the report without automated alerts.
- **Type:** functional
- **Derived from:** D14 (`evergreen_reference_2009.txt`)

The system shall provide a holds-purchase report showing the measures available from system data for a selected reporting period. Authorized staff members shall configure each alert with a measure, a nonnegative threshold, a reporting period, recipients, and one or more notification channels enabled for the library system. The system shall evaluate configured alerts hourly, trigger when the measure is greater than or equal to the threshold, and send the alert within one hour of detection. Each alert shall identify the measure, threshold, reporting period, and affected library location when available. If delivery fails, the system shall retry three times at 15-minute intervals and record the delivery outcome.

<details><summary>Evidence (1 source statements)</summary>

- D14: "Holds Purchase Alert (not available)"

</details>

### 6.3 Patron and Demographic Analytics (PAT)

Patron characteristics, inactivity analysis, demographic reporting, outreach lists, patron activity, privacy-aware demographic statistics, and patron-focused reports.

<a id="req-pat-001"></a>
#### REQ-PAT-001: Patron Demographic Analytics

- **Priority:** P1 (Must have) - Demographic reporting is explicitly requested and supports program planning and library service decisions.
- **Type:** functional
- **Derived from:** D08 (`conversations/conv_pines023_patron_characteristics.eml`), D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), D20 (`survey_results_2009.txt`)

The system shall allow users to filter, group, and report on patrons using age range, postal code, county of residence, home library location, patron type, and preferred language. Users shall be able to combine filters with AND and OR logic, include records with null values for optional fields, and produce patron counts and activity metrics such as circulation or checkout counts by characteristic. The system shall calculate age from birth_date at query time, support configurable age brackets such as 0–5 or 13–18, and provide results suitable for program planning; reporting fields shall be obtained from the patron table, subject to REQ-PAT-005.

<details><summary>Evidence (20 source statements)</summary>

- D08: "I need to run reports on patrons grouped by characteristics."
- D08: "- Age range - Zip code - County of residence - Home branch - Patron type - Preferred language"
- D08: "Can we also GROUP BY these fields? Like, show me circulation by age range, or patron count by home branch?"
- D08: "I need to be able to both LIMIT and GROUP BY patron characteristics."
- D08: "- Limit: Show me only patrons in zip code 30501"
- D08: "- Group By: Show me checkout counts grouped by age range"
- D08: "The age ranges need to be configurable too. Like, 0-5, 6-10, 11-15, etc. Or 0-6, 7-12, 13-17, 18-24, 25-34... Whatever makes sense for the report."
- D08: ""patron type" is important - adult, juvenile, senior, student, etc."
- D08: "We can support both AND and OR logic."
- D08: "We should include them in the report (with null values) rather than excluding them, because excluding data silently can lead to misleading results."
- D08: "The "age range" is calculated from the birth_date field, which means we need to compute it at query time. We can create age brackets in the query."
- D08: "Last month we targeted a summer reading program for teenagers, so we ran a report on patrons aged 13-18 in our zip code."
- D08: "Like, show me circulation by age range, or patron count by home branch?"
- D08: "All the fields mentioned (age range, zip code, county, home branch, patron type, preferred language) exist in the patron table."
- D10: "The system should produce useful demographic statistics, including transactions by geographical regions, age ranges, etc."
- D10: "Queries and reports can be limited or grouped by various patron characteristics, including:   - age range   - zip code   - county of residence   - home branch   - patron type   - preferred language"
- D14: "Circulation Count by Age Demographic (not available)"
- D18: "Demographic analysis for program planning"
- D20: "Transactions by geographical regions   - Transactions by age ranges"
- D20: ""Age ranges and zip codes are most useful.""

</details>

<a id="req-pat-002"></a>
#### REQ-PAT-002: Inactive Patron Identification

- **Priority:** P1 (Must have) - This retains P1 because inactive-patron identification is an essential requested operational capability; the address controls clarify its permitted use without weakening the privacy requirement.
- **Type:** functional
- **Derived from:** D08 (`conversations/conv_pines023_patron_characteristics.eml`), D09 (`conversations/conv_pines024_inactive_patrons.eml`), D10 (`early_draft_srs_galecia.txt`)

The system shall generate an inactive-patron report for patrons with no circulation or electronic activity during a configurable number of days, with presets of 30, 90, 180, and 365 days and support for any positive user-specified number of days. The activity calculation shall consider the most recent activity across relevant records, including checkouts, online account access, online hold requests and renewals, and digital collection access when integrated. Users shall be able to filter by demographic criteria, choose library system, home library location, or county scope, view comparative inactivity counts by library location, distinguish patrons with outstanding fines, and apply exclusions including do-not-disturb, VIP, staff member, and communication opt-out status. Mailing addresses may appear only in the current-state operational report for staff members assigned the inactive-patron address-report permission; they shall not appear in the privacy-protected archive or aggregate historical outputs. Viewing or exporting addresses shall require the corresponding permission and be audited, and address-bearing report data shall be retained only for the configured operational retention period. The report shall be exportable as CSV by authorized staff and schedulable for periodic execution, including quarterly runs.

<details><summary>Evidence (20 source statements)</summary>

- D08: ""show me all Juvenile patrons in zip code 30505 who haven't checked anything out in 6 months""
- D08: ""show me all Juvenile patrons in zip code 30505 who haven't checked anything out in 6 months""
- D09: "We need a report that shows patrons with no circulation or electronic activity in the last X days."
- D09: "X should be configurable - we usually use 365 days but it would be nice to adjust."
- D09: "- 30 days (monthly check) - 90 days (quarterly check) - 180 days (semi-annual) - 365 days (annual)  Can we make it fully customizable? Like any number of days?"
- D09: ""Electronic activity" should include: 1. Logging into OPAC/patron account 2. Placing holds online 3. Renewing items online 4. Accessing digital collections (if integrated)"
- D09: "We mail postcards to inactive patrons, so the report needs to include current mailing addresses."
- D09: "And yes, we should track inactive patrons who still owe fines separately. Those accounts need different handling."
- D09: "One more thing - we should be able to EXCLUDE certain patrons from the inactive report. For example: - Patrons with "do not disturb" flags - VIP patrons - Staff members - Patrons who have opted out of communications"
- D09: "Exportable format (CSV)"
- D09: "These are stored in different tables, so we'd need a combined query."
- D09: "Technically, this is straightforward. We query the transaction table for the most recent activity per patron, and filter for those whose last activity is more than X days ago."
- D09: "The list should be configurable to different levels - System, Home Library, County, etc."
- D09: "At the system level, I can see which branches have the most inactive patrons."
- D09: "Can we also include "electronic activity"? That means online account access, not just physical checkouts."
- D10: "The system should generate a list of patrons with no circulation or electronic activity in the last X days (X configurable). The list should be configurable to System, Home Library, County, etc."
- D09: "We run this quarterly to clean up our patron database."
- D09: "- Patrons who have opted out of communications"
- D09: "The list should be configurable to different levels - System, Home Library, County, etc."
- D09: "- Staff members"

</details>

<a id="req-pat-005"></a>
#### REQ-PAT-005: Privacy-Protected Transaction Archive

- **Priority:** P1 (Must have) - Protecting patron privacy and complying with applicable law are essential constraints on transaction archiving and reporting.
- **Type:** constraint
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D12 (`email_report_features.eml`), D20 (`survey_results_2009.txt`)
- **Merged with:** REQ-PAT-004, REQ-TRN-003 (during review)

The system shall archive transaction data for historical and demographic analysis without retaining direct identifiers that can identify a specific patron in reporting outputs. Before archiving, the system shall remove or de-identify personally identifiable information and retain only the transaction attributes needed for approved aggregate analysis. Access to identifiable source transaction data shall be restricted to authorized roles and logged. The archive and its use shall comply with applicable State Law, as configured and documented by the authorized compliance owner.

<details><summary>Evidence (7 source statements)</summary>

- D10: "Transactions should be archived in a form that protects patron privacy as defined by State Law, while providing useful demographic statistics."
- D10: "Transactions should be archived in a form that protects patron privacy as defined by State Law, while providing useful demographic statistics."
- D10: "The data used to produce these statistics must be anonymized - information that could be used to identify a patron is deleted."
- D10: "The data used to produce these statistics must be anonymized - information that could be used to identify a patron is deleted."
- D12: "TRANSACTION ARCHIVE: Transactions archived protecting patron privacy per State Law, while providing useful demographic statistics."
- D20: "Demographic statistics (must be anonymized - no personally identifiable info)"
- D20: "Demographic statistics (must be anonymized - no personally identifiable info)"

</details>

<a id="req-pat-006"></a>
#### REQ-PAT-006: Patron Interest Analysis

- **Priority:** P3 (Could have) - Interest analysis is a desirable planning aid affecting a narrower use case and is specified here as descriptive reporting.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`)

The system shall provide descriptive, aggregate analysis of patron interests using recorded circulation and hold request activity grouped by bibliographic record subject, format, and reporting period. Users shall be able to select a date range and library location and view counts and percentages for each group. The system shall not infer individual interests or make forecasts under this requirement, and outputs shall exclude personally identifiable information in accordance with REQ-PAT-005.

<details><summary>Evidence (1 source statements)</summary>

- D10: "Analyzing the demographics and interests of patrons."

</details>

<a id="req-pat-007"></a>
#### REQ-PAT-007: Patron Renewal Statistics

- **Priority:** P3 (Could have) - Aggregate renewal statistics are a useful analytical improvement, while predictive modeling is not sufficiently specified or required.
- **Type:** functional
- **Derived from:** D20 (`survey_results_2009.txt`)

The system shall report aggregate historical checkout and renewal counts and calculate the renewal percentage as renewal transactions divided by eligible checkout transactions for a user-selected reporting period. Users shall be able to group results by library location and library material category. The system shall present these measures as descriptive statistics and shall not claim to predict future behavior or renewal likelihood under this requirement. Outputs shall exclude personally identifiable information in accordance with REQ-PAT-005.

<details><summary>Evidence (1 source statements)</summary>

- D20: ""We need to predict patron behavior. How likely is a book to be renewed? What percent of check-outs are renewals?""

</details>

<a id="req-pat-008"></a>
#### REQ-PAT-008: Inactive Patron Cleanup Assignment

- **Priority:** P3 (Could have) - P3 is appropriate because cleanup-task assignment is requested by one stakeholder and the source describes no criticality or detailed workflow.
- **Type:** functional
- **Derived from:** D09 (`conversations/conv_pines024_inactive_patrons.eml`)

The system shall allow authorized users to assign cleanup tasks to specific library locations based on results from the inactive-patron report. The assignment shall identify the library location responsible for the cleanup work and relate the task to the applicable inactive-patron results. The source request does not specify task status, due-date, or notification behavior.

<details><summary>Evidence (1 source statements)</summary>

- D09: "At the home library level, I can assign cleanup tasks to specific branches."

</details>

### 6.4 Financial Management (FIN)

Item valuation, fines, charges, waivers, payments, balances, financial ledgers, reconciliation, and financial reporting.

<a id="req-fin-001"></a>
#### REQ-FIN-001: Financial Transaction Ledger

- **Priority:** P1 (Must have) - D11 marks the payment-ledger requirement CRITICAL, and D10 independently requests a ledger that maps payments to charges for reconciliation.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D11 (`email_financial_reports.eml`)

The system shall record and verify financial transactions in an auditable ledger. The ledger shall record patron payments and identify the charges to which each payment is applied, supporting reconciliation. It shall support staff members responsible for financial operations and retain transaction details needed to verify financial activity.

<details><summary>Evidence (3 source statements)</summary>

- D10: "Tracking and verifying financial transactions."
- D10: "The system maintains a ledger of patron payments, including which charges payments are applied to, to facilitate reconciliation."
- D11: "The system maintains a ledger of patron payments, including which charges payments are applied to, to facilitate reconciliation."

</details>

<a id="req-fin-002"></a>
#### REQ-FIN-002: Item Value Reports

- **Priority:** P2 (Should have) - D10 and D11 both request value-of-items reporting, and D11 supplies specific report examples and identifies the purchase-price field as the data source.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D11 (`email_financial_reports.eml`)

The system shall generate reports calculating the value of library materials from purchase-price data in item records. Staff members shall be able to report on the entire collection or a selected portion, including all items with a specified status, such as long overdue, or all DVDs in a children's collection. The system shall support querying and aggregating the purchase-price field for these calculations.

<details><summary>Evidence (3 source statements)</summary>

- D10: "The system can generate a report of the value of items (based on data in item record) in the entire collection or a portion."
- D11: "System can generate a report of the value of items (based on data in item record) in the entire collection or a portion. Examples: value of all items with status of "longoverdue", value of all DVDs in children's collection, value of entire collection."
- D11: "the data is already in the item records (purchase price field). We just need the system to be able to query and aggregate this."

</details>

<a id="req-fin-003"></a>
#### REQ-FIN-003: Financial Audit Compliance

- **Priority:** P1 (Must have) - Financial auditing and accounting compliance are explicitly required for responsible financial operations.
- **Type:** constraint
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D11 (`email_financial_reports.eml`)

The system shall retain financial reports and archived financial data in a form that supports the accounting and audit requirements adopted by the applicable state, county, and municipal authorities. Before production use, the authorized finance compliance owner shall record the applicable authorities, standards, jurisdiction, and effective versions in the system’s compliance configuration. The system shall preserve relevant report outputs and change history for the retention period required by those authorities.

<details><summary>Evidence (2 source statements)</summary>

- D10: "All reports and data archiving must comply with standard accounting practice and state, county, and municipal auditing requirements."
- D11: "All reports and data archiving must comply with standard accounting practice and state, county, and municipal auditing requirements."

</details>

<a id="req-fin-004"></a>
#### REQ-FIN-004: Financial Activity Record Associations

- **Priority:** P2 (Should have) - D10 and D11 both explicitly request that fines, charges, waivers, and electronic commerce transactions be associated with patron records and item records.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D11 (`email_financial_reports.eml`)

The system shall associate fines, charges, waivers, and electronic commerce transactions with patron records and item records. Staff members shall be able to identify the related patron and library material when reviewing these financial activities. The associations shall be available for financial account review and reporting.

<details><summary>Evidence (2 source statements)</summary>

- D10: "Fines, charges, waivers, and ecommerce transactions are attached to patron and item records."
- D11: "Fines, charges, waivers, and ecommerce transactions are attached to patron and item records."

</details>

<a id="req-fin-005"></a>
#### REQ-FIN-005: Financial Information Updates

- **Priority:** P3 (Could have) - Financial updates are useful for maintaining accurate records, but the source does not establish this capability as critical.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D11 (`email_financial_reports.eml`)

The system shall allow staff members assigned an authorized financial role to update financial account codes, budget allocations, fee and fine amounts, and payment adjustments. The system shall validate required fields, numeric ranges, and effective dates before saving changes, and shall prevent invalid updates. It shall record the prior and new values, acting staff member, timestamp, and reason for each change, and apply changes from their configured effective date.

<details><summary>Evidence (2 source statements)</summary>

- D10: "Financial information can be updated easily."
- D11: "Financial information needs to be easily updatable."

</details>

<a id="req-fin-006"></a>
#### REQ-FIN-006: High Balance Account Queries

- **Priority:** P3 (Could have) - D10 and D11 both mention querying accounts above a specified balance, but provide no critical marker or evidence of broad operational dependence.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D11 (`email_financial_reports.eml`)

The system shall allow staff members to query patron accounts whose balances exceed a specified dollar threshold. Staff members shall be able to supply the threshold, represented in the source examples as X dollars, and retrieve matching accounts. The results shall identify the patron accounts meeting the threshold condition.

<details><summary>Evidence (2 source statements)</summary>

- D10: "As an example, a staff user can easily query patron accounts with balances greater than X dollars."
- D11: "A staff user can easily query patron accounts with balances greater than X dollars."

</details>

<a id="req-fin-007"></a>
#### REQ-FIN-007: Financial Reports

- **Priority:** P2 (Should have) - D10 and D11 specify multiple financial report dimensions, D11 contributors add joining and payment-instrument needs, and D18 records director-level reporting needs.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D11 (`email_financial_reports.eml`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`)

The system shall provide financial reports for staff members, including reports suitable for library directors. Reports shall show patron account balances by patron, associated library location, and library system, and fines and charges by time period and charge type. Reports shall also show fines waived by time period and library location, and payments by time period, payment method, and payment instrument, including staff desk, self-check station, OPAC, cash, credit card, and check. The system shall allow financial data associated with patron records and item records to be joined when querying these reports.

<details><summary>Evidence (5 source statements)</summary>

- D10: "The system provides financial reports including:   - patron account balances by patron, home library, and system   - fines and charges accrued per time period (e.g., last twelve months, YTD, last month) and per type of charge (overdue fines, damaged item charges, lost item charges, etc.)   - fines waived per time period and per branch   - payments made per time period and per payment method (e.g., staff desk, self-check station, OPAC)"
- D11: "The system provides financial reports including:    - Patron account balances by patron, home library, and system    - Fines and charges accrued per time period (last 12 months, YTD, last month) and per type of charge (overdue fines, damaged item charges, lost item charges, etc.)    - Fines waived per time period and per branch    - Payments made per time period and per payment method (staff desk, self-check station, OPAC)"
- D11: "The financial data is attached to patron records AND item records. So when we query for financial reports, we need to be able to join these data sources."
- D11: "The financial reports need to show payments by method - cash, credit card, check, etc."
- D18: "Financial report needs are understood at the director level"

</details>

<a id="req-fin-008"></a>
#### REQ-FIN-008: Location Financial Activity Tracking

- **Priority:** P2 (Should have) - D11 states that location-level payment tracking is important for end-of-month reports and that waived fines must be associated with each location's budget; D10 also requests tracking payments and waived fines per library.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D11 (`email_financial_reports.eml`)

The system shall track payments made and fines waived by library location. Staff members at each library location shall be able to view payments collected at that location, and reports shall support end-of-month review of those collections. The system shall associate waived fines with the library location whose budget they affect.

<details><summary>Evidence (3 source statements)</summary>

- D10: "System tracks fines waived and payments made per library."
- D11: "Payments tracking by library is important for our end-of-month reports. Each branch needs to be able to see what payments were collected at their location."
- D11: "Fines waived should be tracked per library because each library has its own budget for waived fines."

</details>

<a id="req-fin-009"></a>
#### REQ-FIN-009: Bill And Aged Debt Reports

- **Priority:** P2 (Should have) - D10 lists the required bill reports, and D14 identifies the aged debt detailed report as partially available and in need of enhancement.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`)

The system shall provide reports for bills currently owed by patrons, detailed payments received, detailed forgive, work, and goods payments received, detailed voids, and aged debt. Staff members shall be able to use the aged debt report in detailed form. The reports shall present the listed billing and payment information for financial review.

<details><summary>Evidence (2 source statements)</summary>

- D10: "BILLS REPORTS: - Bills currently Owed by Patrons - Detailed Payments Received - Detailed Forgive, Work, and Goods Payments Received - Detailed Voids - Aged Debt"
- D14: "Aged Debt detailed report (partially available, needs enhancement)"

</details>

<a id="req-fin-010"></a>
#### REQ-FIN-010: Historical Snapshot Bills Report

- **Priority:** P3 (Could have) - D14 notes that a snapshot bills report going back in time does not exist, and D20 records a survey request for it, but neither source marks it critical.
- **Type:** functional
- **Derived from:** D14 (`evergreen_reference_2009.txt`), D20 (`survey_results_2009.txt`)

The system shall provide a snapshot bills report that allows staff members to review bills as they stood at a past point in time. The report shall support retrieving historical bill information for a selected prior date or period. This capability shall provide access to bill snapshots beyond the current state of patron accounts.

<details><summary>Evidence (2 source statements)</summary>

- D14: "Snapshot bills report going back in time - does not exist"
- D20: ""Need a snapshot bills report going back in time""

</details>

<a id="req-fin-011"></a>
#### REQ-FIN-011: Immediate Front Desk Payment Updates

- **Priority:** P2 (Should have) - D11 explicitly requests immediate reflection of front desk payments, indicating a meaningful operational timeliness need, though no critical marker is provided.
- **Type:** functional
- **Derived from:** D11 (`email_financial_reports.eml`)

The system shall reflect a patron's front desk payment immediately after the payment is made. The updated financial information shall be available to staff members without waiting for a later batch update. The change shall appear in the patron's financial account information following the transaction.

<details><summary>Evidence (1 source statements)</summary>

- D11: "When a patron makes a payment at the front desk, we need the system to reflect that immediately."

</details>

### 6.5 Circulation, Holds, and Transactions (TRN)

Transaction capture, circulation statistics, check-ins, checkouts, renewals, holds, in-house use, transaction history, and transaction-based analytics.

<a id="req-trn-001"></a>
#### REQ-TRN-001: Transaction Activity Statistics

- **Priority:** P3 (Could have) - The activity-report need is stated in one early-draft source, D10, with no explicit priority marker or evidence of broader support.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`)

The system shall provide activity reports showing circulation traffic and volume of use. Reports shall include counts of checkouts, check-ins, hold requests placed, and hold requests filled. Authorized users shall be able to review these measures as activity statistics for library operations.

<details><summary>Evidence (2 source statements)</summary>

- D10: "Activity reports should indicate traffic and volume of use, displaying statistics on check-outs, check-ins, holds placed, and holds filled."
- D10: "Activity reports should indicate traffic and volume of use, displaying statistics on check-outs, check-ins, holds placed, and holds filled."

</details>

<a id="req-trn-002"></a>
#### REQ-TRN-002: Transaction Cross-Tabulation

- **Priority:** P2 (Should have) - The early draft and survey both request grouping by hour, terminal, library location, and library system, while the draft adds patron demographic dimensions; the independent support warrants P2.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D20 (`survey_results_2009.txt`)

The system shall allow transaction statistics to be grouped and cross-tabulated by hour, terminal, library location, and library system. Reports shall also support grouping by patron age range, patron type, and patron location. Staff members shall be able to combine applicable dimensions to examine transaction volume across these categories.

<details><summary>Evidence (3 source statements)</summary>

- D10: "It should be possible to cross-tabulate per terminal, per branch, per library system, per hour, per patron age range, per patron type, and per patron location."
- D10: "Transactions can be grouped by hour, terminal, branch, and system."
- D20: "Transactions can be grouped by hour, terminal, branch, and system."

</details>

<a id="req-trn-004"></a>
#### REQ-TRN-004: Transaction History Retention

- **Priority:** P2 (Should have) - The retention policy is stated in both the early draft and the survey, including configurable detailed history and indefinite aggregate retention, indicating independently supported operational value.
- **Type:** constraint
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D20 (`survey_results_2009.txt`)

The system shall retain transaction history for a configurable number of days and retain monthly and annual aggregate transaction information indefinitely. Authorized staff members shall be able to use the retained information for reporting over the applicable period. The retention setting shall define the history period without changing the indefinite retention of the aggregates.

<details><summary>Evidence (3 source statements)</summary>

- D10: "Transaction history is maintained for X days (X is configurable)."
- D10: "Monthly and annual aggregate information is maintained indefinitely."
- D20: "Transaction history maintained for X days (configurable), with monthly and annual aggregates retained indefinitely."

</details>

<a id="req-trn-005"></a>
#### REQ-TRN-005: Circulation Behavior Analytics

- **Priority:** P2 (Should have) - Circulation analytics are useful for staff review, but they are not required for the system's core circulation transactions.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D20 (`survey_results_2009.txt`)

The system shall produce statistics that help staff members analyze patron behavior and use of library materials. For a selected date range and library location, the system shall report average return time as the mean number of calendar days from checkout to check-in for checkouts with a recorded check-in during that range; missing check-in data shall be excluded, and each completed checkout shall be counted once. The system shall report historical renewal percentage as the number of eligible checkouts renewed at least once divided by all eligible checkouts, expressed as a percentage for the same date range and location. Renewals shall not be counted as separate checkouts in the denominator. Reports shall identify the date range, location, numerator, and denominator used for each percentage.

<details><summary>Evidence (3 source statements)</summary>

- D10: "The system should produce statistics that can be used to understand and predict patron behavior and use of materials."
- D10: "For example:   - How quickly is a particular book returned, on average?   - How likely is a particular book to be renewed?   - What percent of check-outs at a particular branch are renewals?"
- D20: "Patron behavior analysis (how quickly books are returned, renewal rates)"

</details>

<a id="req-trn-006"></a>
#### REQ-TRN-006: Transaction Type Queries

- **Priority:** P2 (Should have) - The early draft and survey both call for reports covering multiple transaction types, including check-ins, checkouts, fines, and registrations, providing independent support for P2.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D20 (`survey_results_2009.txt`)

The system shall allow authorized users to query transaction records across all transaction types or filter them by transaction type. The supported types shall include check-ins, checkouts, fines collected, and patron registrations, as well as other transaction types captured by the system. Results shall be usable for transaction reporting and operational review.

<details><summary>Evidence (2 source statements)</summary>

- D10: "Transactions include check-ins, check-outs, fines collected, patron registrations, etc., and can be queried by all transactions or by type of transaction."
- D20: "Transactions include check-ins, check-outs, fines collected, patron registrations, etc."

</details>

<a id="req-trn-007"></a>
#### REQ-TRN-007: Check-In Counts By Method

- **Priority:** P2 (Should have) - The early draft and survey both request separate check-in counts by method, including book drop and self-service, so this is independently supported rather than a single-source enhancement.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D20 (`survey_results_2009.txt`)

The system shall count check-ins individually and cumulatively by check-in method. The supported breakdown shall distinguish book-drop check-ins, terminal check-ins, and self-service check-ins, and shall permit results to be reviewed by terminal and by staff member or self-service operation where applicable. Staff members shall be able to use these counts in circulation statistics.

<details><summary>Evidence (2 source statements)</summary>

- D10: "The system counts all types of check-in individually and cumulatively:   - book-drop   - by terminal   - by user or self-service"
- D20: ""I need to see check-in counts broken down by method - book drop vs terminal vs self-service""

</details>

<a id="req-trn-008"></a>
#### REQ-TRN-008: Checkout And Renewal Counts

- **Priority:** P2 (Should have) - The early draft and survey independently specify the same six checkout and renewal categories, making this a consistently supported reporting need.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D20 (`survey_results_2009.txt`)

The system shall count checkout and renewal transactions individually and cumulatively by transaction method. The breakdown shall distinguish staff checkouts, self-service checkouts, staff renewals, self-service renewals, online renewals, and OPAC renewals. Staff members shall be able to review the counts as circulation statistics and compare the recorded transaction types.

<details><summary>Evidence (2 source statements)</summary>

- D10: "The system counts all types of check-out individually and cumulatively:   - staff check-out   - self check-out   - staff renewal   - self checkout renewal   - online renewal   - OPAC renewal"
- D20: ""Check-out types should be counted separately - staff checkout, self checkout, staff renewal, self checkout renewal, online renewal, OPAC renewal""

</details>

<a id="req-trn-009"></a>
#### REQ-TRN-009: Hold Request Placement Metrics

- **Priority:** P2 (Should have) - The early draft and survey both request hold-request counts and the placement method, including staff desk, public computer, and remote placement.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D20 (`survey_results_2009.txt`)

The system shall count hold requests and record the method by which each request was placed. The recorded methods shall distinguish placement at a staff desk, at a public computer inside a library location, and remotely. Staff members shall be able to review counts by placement method in hold reports and transaction statistics.

<details><summary>Evidence (2 source statements)</summary>

- D10: "The system counts all hold requests, including how the hold was placed:   - at a staff desk   - at a public computer inside the library   - remotely"
- D20: ""Holds reports should show how the hold was placed - at staff desk, at public computer, or remotely""

</details>

<a id="req-trn-010"></a>
#### REQ-TRN-010: Patron Transaction Summary Reports

- **Priority:** P2 (Should have) - The early draft and survey both specify reports of holds and checkouts across patron and organizational scopes, and the survey additionally requests total transactions per patron, library, and system.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D20 (`survey_results_2009.txt`)

The system shall provide transaction reports showing hold requests placed, hold requests filled, and checkouts, with totals available per patron, library location, selected group of library locations, library system, and county. Reports shall show the number of checkouts and hold requests placed per patron and shall subtotal hold requests by status, including active, frozen, and frozen-until. Staff members shall be able to select the applicable reporting scope for review.

<details><summary>Evidence (3 source statements)</summary>

- D10: "The system can generate a report of transactions (holds placed, holds filled, and check-outs) per patron, per library, per selected group of libraries, per system, per county. The system displays the number of check-outs and placed holds per patron. Holds are subtotaled by type, e.g., active, frozen, and frozen-until holds."
- D20: ""Need total transactions report - per patron, per library, per system""
- D20: "Transactions report can show holds placed, holds filled, and check-outs per patron, per library, per group of libraries, per system, per county."

</details>

<a id="req-trn-011"></a>
#### REQ-TRN-011: Circulation Reports

- **Priority:** P2 (Should have) - Circulation reports are important for daily work, but the system remains usable if some reporting breakdowns are temporarily unavailable.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D15 (`interview_cataloging_2009-05-08.txt`)
- **Merged with:** REQ-TRN-017 (during review)

The system shall provide circulation reports for check-in counts, checkout counts, overdue library materials by a specified number of days, renewals, non-cataloged circulation, and total circulation. Reports shall support breakdowns by circulation modifier, category values, Dewey classification, shelving location, MARC data, circulation location, patron county, patron home library location, and age demographic. Total circulation shall combine cataloged and non-cataloged activity and display its checkout, renewal, and non-cataloged components; each non-cataloged transaction captured under REQ-COL-019 shall be counted once in the applicable non-cataloged measure and total. Overdue reports shall support daily review, shelf reading, and patron contact information.

<details><summary>Evidence (3 source statements)</summary>

- D10: "CIRCULATION REPORTS: - Check in Count - Checkout Count (includes checkouts only) - Items overdue by X days (daily, shelf reading, patron contact info) - Circulation Count by Circ Modifier, Cat1, and Cat2 (Adult, YA, Juv...) - Renewals Count - Non-Cat Count - Circulation Count - total circ including checkouts, renewals, and noncats - Total Circulation Count (Merging both Cat and Non-Cat circulation data) - Circulation Count by Dewey - Circulation Count by Circ Modifier - Circulation Count by Shelving Location - Circulation Count by MARC - Circulation Count by Circ Location broken down by Patron County - Circulation Count by Circ Location broken down by Patron Home Library - Circulation Count by Age Demographic"
- D10: "Ability to retrieve total circ including checkouts, renewals, and noncats   with a breakdown displaying those circ types"
- D15: "We also need to count transactions and include them in circulation statistics and reports."

</details>

<a id="req-trn-012"></a>
#### REQ-TRN-012: Hold Reports

- **Priority:** P2 (Should have) - The early draft requests a range of operational hold reports, while the reference document identifies unfilled and stale hold reports as unavailable, supporting a clear reporting need without a critical marker.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`)

The system shall provide reports for hold requests, including unfilled and stale holds, annual counts of requests placed, and hold-related purchase alerts. Reports shall identify library materials sent or received for holds and support intra-library-system loan reporting for all locations and by library system or library location. Staff members shall be able to use these reports to monitor hold fulfillment and materials awaiting patron pickup.

<details><summary>Evidence (3 source statements)</summary>

- D10: "HOLDS REPORTS: - Holds Purchase Alert - Items Sent for Holds - Items Received for Holds - IntraPINES Loans for all Systems - IntraPINES Loans for all Facilities - IntraPINES Loans by System - IntraPINES Loans by Facility - Unfilled Holds - Annual # of holds placed - Stale Holds (holds sitting on hold shelf waiting for pickup for too long)"
- D14: "Unfilled Holds (not available)"
- D14: "Stale Holds (not available)"

</details>

<a id="req-trn-013"></a>
#### REQ-TRN-013: In-House Use Reports

- **Priority:** P3 (Could have) - The specific in-house use reports are listed in one early-draft source with no additional priority marker or independent supporting candidate, so P3 is appropriate.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`)

The system shall provide reports of in-house use for cataloged and non-cataloged library materials. The reports shall include a monthly count for non-cataloged in-house use and a count for cataloged in-house use. Staff members shall be able to use the counts to review use that does not result in a checkout.

<details><summary>Evidence (1 source statements)</summary>

- D10: "IN HOUSE USE REPORTS: - NonCat In House Use Count by Month - Cataloged In House Use Count"

</details>

<a id="req-trn-015"></a>
#### REQ-TRN-015: Claims Returned Report

- **Priority:** P3 (Could have) - A single reference-document candidate identifies a claims returned report as unavailable, with no additional priority evidence, supporting P3.
- **Type:** functional
- **Derived from:** D14 (`evergreen_reference_2009.txt`)

The system shall provide a report of items that patrons have claimed to have returned. Staff members shall be able to use the report to review and follow up on claims returned during circulation operations. The report shall identify the relevant transaction or item record where that information is available.

<details><summary>Evidence (1 source statements)</summary>

- D14: "Claims Returned report (not available)"

</details>

<a id="req-trn-016"></a>
#### REQ-TRN-016: Separate Check-In Timestamps

- **Priority:** P2 (Should have) - The need to exclude renewals from check-in date and time is stated in both the reference document and the survey, demonstrating independent support.
- **Type:** functional
- **Derived from:** D14 (`evergreen_reference_2009.txt`), D20 (`survey_results_2009.txt`)

The system shall provide check-in date and time values that exclude renewal transactions. Transaction records and reports shall distinguish a check-in timestamp from a renewal timestamp even when both are stored with circulation history. Staff members shall be able to use the check-in values without renewal activity being counted as a return.

<details><summary>Evidence (2 source statements)</summary>

- D14: "Checkin Date/time not including renewals - checkin and renewal timestamps are stored together"
- D20: ""Checkin date/time should not include renewals""

</details>

### 6.6 Security, Auditing, and Administration (SEC)

Authentication, authorization, roles, permissions, deletion auditing, accountability, administrative controls, and access governance.

<a id="req-sec-001"></a>
#### REQ-SEC-001: Staff Authentication Methods

- **Priority:** P2 (Should have) - Staff login was requested in D10, D13, and the later D18 meeting minutes, with D13 explicitly requiring both methods and an optional swipe method; this is a regular operational need, but no candidate marks it critical.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D13 (`email_staff_login.eml`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`)

The system shall authenticate staff members using either an employee ID badge swipe or individual username and password credentials. Badge-swipe authentication shall be optional, and username and password authentication shall remain available as a fallback for staff members without ID cards. A badge swipe shall log in the identified staff member, and both authentication methods shall identify the staff member to the system.

<details><summary>Evidence (8 source statements)</summary>

- D10: "The system should support streamlined methods of logging into terminals. For example, a staff member could swipe a card (like an RFID employee badge) to log in, or alternatively use individual login credentials (username and password)."
- D10: "The system should not REQUIRE card-based login - traditional username/password should also be available as a fallback."
- D13: "The system should support BOTH methods - streamlined login (e.g. card swipe) AND traditional login (individual login and password)."
- D13: "The streamlined method should be optional but available."
- D13: "The staff member simply swipes their employee ID badge and is logged in immediately."
- D13: "However, we also need to support the traditional username/password method - not all staff may have ID cards, and we need a fallback."
- D18: "Staff login needs (card swipe) - already discussed via email"
- D10: "For example, a staff member could swipe a card (like an RFID employee badge) to log in, or alternatively use individual login credentials (username and password). The system should not REQUIRE card-based login - traditional username/password should also be available as a fallback."

</details>

<a id="req-sec-002"></a>
#### REQ-SEC-002: Staff Login Accountability

- **Priority:** P2 (Should have) - D13 explicitly states that identifying the logged-in staff member is required for audit purposes; the request is direct and operationally important, though it appears in one source.
- **Type:** functional
- **Derived from:** D13 (`email_staff_login.eml`)

The system shall associate each authenticated session with the staff member who logged in. This identification shall be retained for audit purposes regardless of whether the staff member used badge-swipe or username and password authentication. Audit records shall identify the individual staff member rather than only the authentication method or terminal.

<details><summary>Evidence (1 source statements)</summary>

- D13: "The system must track WHICH staff member is logged in for audit purposes."

</details>

<a id="req-sec-003"></a>
#### REQ-SEC-003: Role-Based Access Governance

- **Priority:** P3 (Could have) - P3 is appropriate because this usability improvement is stated in one early draft, has no explicit priority marker, and is not supported by additional source evidence.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D12 (`email_report_features.eml`), D13 (`email_staff_login.eml`), D14 (`evergreen_reference_2009.txt`), D16 (`interview_sysadmin_2009-05-10.txt`), D17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`)

The system shall control access through roles that can be assigned to staff members and groups and that determine permissions for individuals, workgroups, and other staff groups. Administrators shall be able to create and manage roles and permissions through controls that are easy to administer. Changing a staff member's role assignment shall update that person's permissions without requiring individual permission edits. Supported role capabilities shall include Global Admin access to all functions, Local Admin access to configuration and reporting for an assigned library location, Library Manager access to approved reports and limited template changes, Staff access within assigned permissions, and Patron access through public-facing displays.

<details><summary>Evidence (21 source statements)</summary>

- D10: "User rights and privileges will be controlled through security groups and or "roles" that allow access control for individuals, workgroups, and arbitrary staff groups."
- D10: "All permissions should be easy to administer."
- D12: "If I change someone from "Staff" to "Manager," their report permissions should update automatically based on the role."
- D12: "The permissions need to be easy to administer."
- D13: "when a staff member logs in (by any method), their permissions should be determined by their assigned security group/role."
- D13: "Administrators should be able to create and manage these groups."
- D13: "we need user rights and privileges to be controlled through security groups and/or "roles." This would allow access control for individuals, workgroups, and arbitrary staff groups."
- D13: "- Front desk staff (can run basic reports, limited filters) - Department heads (can create and modify templates) - System administrators (full access to all reports and permissions)"
- D13: "changing someone's permissions should be a simple matter of changing their role assignment, not modifying individual permissions."
- D14: "2. Implement fine-grained permissions and template management"
- D16: "PINES uses a role-based system."
- D16: "We have different levels of access:  - Patron (public access through OPAC)  - Staff (basic circulation functions)  - Local Admin (branch manager - can run reports, configure local settings)  - Global Admin (IT staff - full system access)"
- D16: "The permission system needs to be controlled through security groups and/or "roles.""
- D16: "This allows access control for individuals, workgroups, and arbitrary staff groups."
- D16: "The system needs to make it easy to administer these roles."
- D16: "Changing someone's permissions should be a simple matter of changing their role assignment."
- D17: "The group discussed the different types of users who would interact with Management Processes:    Patron: ...   Staff: ...   Local System Administrators: ...   Library Managers: ...   Library Directors: ...   Global System Administrator: ..."
- D18: "User rights and privileges will be controlled through security groups and/or "roles" that allow access control for individuals, workgroups, and arbitrary staff groups."
- D19: "We need security groups and/or 'roles' that allow access control for individuals, workgroups, and arbitrary staff groups."
- D19: "The system should make it easy to change someone's permissions by simply changing their role assignment."
- D19: "Key points: - Global Admin: Full system access - Local Admin: Branch-level reporting and configuration - Library Manager: Run approved reports, limited template modification - Staff: Run reports within assigned permissions - Patron: Indirect access through OPAC displays"

</details>

<a id="req-sec-004"></a>
#### REQ-SEC-004: Report Access Controls

- **Priority:** P1 (Must have) - Report authorization is a prerequisite for protecting report data and controlling access to reporting capabilities; the retained requirement is P1.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D12 (`email_report_features.eml`), D14 (`evergreen_reference_2009.txt`), D20 (`survey_results_2009.txt`)
- **Merged with:** REQ-SEC-006 (during review)

The system shall allow administrators to assign permissions through roles or other administrative controls for accessing the query tool, creating or cloning reports, adding fixed reports, and running reports or report templates. Permissions shall distinguish creation from execution and shall be configurable for individual reports, report templates, and specified data sets used by ad hoc reports. The system shall enforce permissions when a report or template is opened or executed, deny unauthorized access, and record permission changes and denied execution attempts for review. Folder placement shall not grant access.

<details><summary>Evidence (10 source statements)</summary>

- D10: "The system should provide distinct, fine-grained permission levels that limit who can create and clone reports."
- D10: "Ability to add more canned reports via permission level"
- D12: "Admin controls access."
- D12: "PERMISSIONS: We need distinct, fine-grained permission levels limiting who can create and clone reports."
- D12: "Admins can create shared folders to allow or disallow staff from running specific reports, and/or to run ad hoc reports on specific sets of data."
- D14: "2. Implement fine-grained permissions and template management"
- D14: "No fine-grained control over who can create vs. run reports"
- D20: "Fine-grained permissions (who can create/run what): 76%"
- D20: "Fine-grained permissions limit who can create and clone reports."
- D20: "Shared folders to allow/disallow staff from running specific reports."

</details>

<a id="req-sec-005"></a>
#### REQ-SEC-005: Report Template Restrictions

- **Priority:** P2 (Should have) - Template restrictions and configurable filters were requested by administrators and report users in D10, D12, and D14, but no candidate marks this specific capability critical or provides a survey percentage.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D12 (`email_report_features.eml`), D14 (`evergreen_reference_2009.txt`)

The system shall let administrators restrict which filters and display fields staff members may change in a report template. Authorized staff members shall be able to set permitted parameters, such as a call number range, or select display fields from an approved list. Restricted template elements shall remain protected, including controls that prevent a report from displaying deleted records when that display is not authorized.

<details><summary>Evidence (4 source statements)</summary>

- D10: "Administrators should be able to limit which filters and display fields can be altered, to certify a dependable output."
- D12: "Admins should be able to limit which filters and display fields can be altered."
- D12: "Example: Front-line staff can set a call number range for a weeding report or add/remove display fields from a pick list, but can't alter the template to display deleted items."
- D14: "No ability to limit which filters staff can use"

</details>

<a id="req-sec-007"></a>
#### REQ-SEC-007: Table And Field Access

- **Priority:** P2 (Should have) - D10 identifies administrator control over table and field access as a specific security need, but the capability is stated in one source without an explicit critical marker.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`)

The system shall allow administrators to control staff access to data tables and individual fields. These controls shall determine which tables and fields staff members may access through system functions, including reporting and query capabilities. Administrators shall be able to apply access decisions according to the staff member's assigned permissions.

<details><summary>Evidence (1 source statements)</summary>

- D10: "Administrators should control staff access to tables and fields."

</details>

<a id="req-sec-008"></a>
#### REQ-SEC-008: Item Transfer Authorization

- **Priority:** P2 (Should have) - D04 requests restricting transfers to specified roles, including managers, administrators, and transfer coordinators; the need is explicit but appears in one source.
- **Type:** functional
- **Derived from:** D04 (`conversations/conv_pines018_item_transfer.eml`)

The system shall restrict transfers of library materials between library locations to staff members with authorized roles. Authorized roles shall include managers, administrators, and transfer coordinators, or other roles explicitly granted transfer permission. Staff members without that permission shall not be able to initiate or perform a transfer.

<details><summary>Evidence (1 source statements)</summary>

- D04: "This should be limited to certain roles (managers, administrators, transfer coordinators)."

</details>

<a id="req-sec-009"></a>
#### REQ-SEC-009: Administrative Responsibilities

- **Priority:** P2 (Should have) - Local and global administrative duties are described in D10 and D17, including configuration and reporting responsibilities; these are clearly requested operational capabilities but are not marked critical.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`)

The system shall provide local administrators with controls to configure settings for their assigned library location and run system reports. The system shall provide global administrators with controls to implement system-wide software changes and configurations and generate statistical reports for the library system. Administrative capabilities shall be limited according to the administrator's assigned role and scope.

<details><summary>Evidence (4 source statements)</summary>

- D10: "They can configure local settings and run system reports."
- D10: "The individual(s) who manage the ILS at the consortium level, implementing software changes and configurations, and generating statistical reports for the entire system."
- D17: "Local System Administrators: Management staff who oversee Library processes. They configure the system locally."
- D17: "Global System Administrator: Manages PINES at the consortium level, implementing software changes and configurations, and generating statistical reports for PINES as a whole."

</details>

<a id="req-sec-010"></a>
#### REQ-SEC-010: Deletion Audit Records

- **Priority:** P1 (Must have) - Deletion auditing is requested by multiple stakeholders in D06, D07, and D15 for accountability and compliance, with D07 specifying audit fields and D06 requiring purge attribution.
- **Type:** constraint
- **Derived from:** D06 (`conversations/conv_pines021_item_purging.eml`), D07 (`conversations/conv_pines022_deletions.eml`)

The system shall record an audit entry for each deleted record and purge, capturing the record type, record identifier, staff member responsible, deletion timestamp, and associated library location. The audit entry shall capture the prior status or reason for deletion when that information is available, and the audit history shall support tracing deleted records for accountability and troubleshooting. Deletion events shall be recorded in an audit table by a database trigger.

<details><summary>Evidence (11 source statements)</summary>

- D06: "We need to track who purged what and when."
- D07: "Is there a way to track when records are deleted?"
- D07: "- What type of record was deleted (item/patron/bib)"
- D07: "Tracking should include: - Timestamp"
- D07: "- Who deleted it"
- D07: "- Where they were located (which branch)"
- D07: "Fields: record_type, record_id, deleted_by, deleted_at, location"
- D07: "A trigger in the database that logs deletions to an audit table"
- D07: "If we accidentally delete something we shouldn't have, we need to be able to trace it."
- D07: "This is for auditing purposes."
- D07: "Possibly why (status before deletion?)"

</details>

<a id="req-sec-011"></a>
#### REQ-SEC-011: Deletion Reports

- **Priority:** P1 (Must have) - Deletion counts and reporting were requested independently in D07, D10, and D15, and D20 reports 27% survey support; multiple stakeholders specifically cite auditing and director reporting needs.
- **Type:** functional
- **Derived from:** D07 (`conversations/conv_pines022_deletions.eml`), D10 (`early_draft_srs_galecia.txt`), D15 (`interview_cataloging_2009-05-08.txt`), D20 (`survey_results_2009.txt`)

The system shall provide a report interface for querying deletion audit records and reporting deletion counts by date range, staff member, record type, library location, and library system. Reports shall support totals by month, quarter, or year, counts for a particular date, and summaries such as the staff members responsible for the highest number of deletions. Reported record types shall include item records, patron records, and other applicable types.

<details><summary>Evidence (14 source statements)</summary>

- D07: "We need to be able to count and track record deletions (item records, patron records) per location and per system."
- D07: "A report interface to query this audit table"
- D07: "We can aggregate by date range, by user, by record type."
- D07: "Total deletions per period (month, quarter, year)"
- D07: "Deletions by type (item vs patron vs other)"
- D07: "Deletions by location"
- D07: "Top users who delete the most records"
- D07: "Being able to show "we deleted 500 patron records on X date" is important for audits."
- D07: "The report should show deletions per location and per system."
- D10: "Ability to count and track record deletions (e.g., item records, patron records) per location and per system."
- D15: "we need to count and track record deletions per location and per system. This is important for auditing - our directors want to know how many records we've deleted and why."
- D20: "Count and track record deletions: 27%"
- D20: "Count and track record deletions: 27%"
- D20: "Count and track record deletions: 27%"

</details>

<a id="req-sec-012"></a>
#### REQ-SEC-012: Denied Deletion Attempts

- **Priority:** P2 (Should have) - D07 contains a direct request to track denied deletion attempts, but the requirement is supported by one stakeholder and has no explicit priority marker.
- **Type:** functional
- **Derived from:** D07 (`conversations/conv_pines022_deletions.eml`)

The system shall log attempts to delete records when the attempt is denied. Each logged attempt shall identify the staff member, the record or record type involved when available, the time of the attempt, and the denial outcome. Authorized administrators shall be able to review these events for security monitoring and accountability.

<details><summary>Evidence (1 source statements)</summary>

- D07: "Can we also track attempted deletions that were denied?"

</details>

<a id="req-sec-013"></a>
#### REQ-SEC-013: Deletion Safeguards

- **Priority:** P2 (Should have) - D06 explicitly identifies accidental deletion of an entire collection as a safety concern, but the safeguard is requested in one source without a critical priority marker.
- **Type:** functional
- **Derived from:** D06 (`conversations/conv_pines021_item_purging.eml`)

The system shall provide safeguards to prevent an accidental operation from deleting an entire collection of library materials. Before a deletion operation with that scope is completed, the system shall require a deliberate confirmation or equivalent protective action. The safeguard shall distinguish a whole-collection deletion from routine record deletion.

<details><summary>Evidence (1 source statements)</summary>

- D06: "we need to make sure the system is safe - we don't want someone accidentally deleting their entire collection."

</details>

<a id="req-sec-014"></a>
#### REQ-SEC-014: Staff Account Security Report

- **Priority:** P2 (Should have) - This consolidates two overlapping requests for staff-account password reporting. The capability is useful for regular administration, but the system remains usable with other account-management controls.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`)
- **Merged with:** REQ-PAT-003 (during review)

The system shall provide authorized staff members with a report of staff accounts that identifies each account, its most recent password-change date, and its password-expiration date. The report shall display both dates for each account where available and clearly identify a missing or unavailable date rather than presenting it as current. Access to the report shall be restricted according to assigned permissions, and the report shall allow administrators to review account password status.

<details><summary>Evidence (7 source statements)</summary>

- D10: "PATRONS REPORTS: - Patron Count - Patron Added Count by Month - New Patron Count (patrons added the previous month by Demographic Category) - Patron Count by Age Demographic - Patron Count by County - Patron Count by County, City, and Zip Code - Patron Count by Home Library - Patron Count by Profile Group - Patron Count by survey answer - List of patrons by survey answer - Voter Survey Responses County by Week - List of Patrons by Expiration Date - Voter Reg Survey Responses Count by Week - List of patrons who are BARRED - List of Patrons with inactive status - List of Staff Accounts with date of last password change and account expiration - List of Patrons with specific wording in notes"
- D14: "Patron Count by Age Demographic (not available)"
- D14: "Patron Count by County (not available)"
- D14: "Patron Count by County, City, & Zip Code (not available)"
- D14: "Voter Survey Responses (not available)"
- D14: "List of Patrons with inactive status (not available)"
- D14: "Staff Accounts with date of last password change (not available)"

</details>

<a id="req-sec-015"></a>
#### REQ-SEC-015: Staff Session Security

- **Priority:** P2 (Should have) - D13 raises password sharing and unattended logged-in terminals as concrete security risks, but the concern appears in one source and does not specify a required control mechanism.
- **Type:** non-functional
- **Derived from:** D13 (`email_staff_login.eml`)

The system shall provide controls that reduce security risks caused by staff members sharing passwords or leaving terminals authenticated and unattended. The controls shall support preventing unauthorized use of an active session and shall preserve accountability for actions performed under an authenticated staff account. The system shall make these controls available to administrators for operational use.

<details><summary>Evidence (1 source statements)</summary>

- D13: "It leads to security issues - staff get in a hurry and sometimes share passwords or leave terminals logged in."

</details>

### 6.7 Architecture, Performance, and Technical Constraints (ARC)

Deployment, databases, scalability, availability, performance isolation, accessibility, browser and platform compatibility, environments, disaster recovery, and technical architecture.

<a id="req-arc-001"></a>
#### REQ-ARC-001: Consortium Capacity

- **Priority:** P1 (Must have) - D10 marks this scale requirement High Priority, and the later D18 meeting minutes confirm the same consortium volumes.
- **Type:** non-functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`)

The system shall support the operational scale of a library consortium comprising 286 library locations. It shall accommodate 17 million annual circulations and the purchasing and processing of more than 900,000 library materials per year. These values shall define the minimum scale used to assess the system’s capacity.

<details><summary>Evidence (2 source statements)</summary>

- D10: "The system must support a library consortium with 286 locations, 17 million annual circulations, and purchasing/processing over 900,000 items per year."
- D18: "the system must support a library consortium with 286 locations, 17 million annual circulations, purchasing and processing over 900,000 items per year"

</details>

<a id="req-arc-002"></a>
#### REQ-ARC-002: Location Overview Capacity

- **Priority:** P3 (Could have) - The overview is a desirable usability improvement and is not identified as essential to the system’s core purpose.
- **Type:** non-functional
- **Derived from:** D02 (`conversations/conv_pines015_capacity_interface.eml`)

The system shall display a single overview of up to 286 library locations, with each location represented by a labeled entry and no location omitted at that scale. The overview shall show capacity status and load for each library location, and shall load within five seconds for at least 95% of requests under the agreed production load. Users shall be able to open an individual library location from its overview entry.

<details><summary>Evidence (1 source statements)</summary>

- D02: "One consideration: with 286 locations, the overview might get crowded."

</details>

<a id="req-arc-003"></a>
#### REQ-ARC-003: Large Batch Update Processing

- **Priority:** P3 (Could have) - D04 identifies a performance and database-locking concern in one source but provides no explicit priority marker.
- **Type:** non-functional
- **Derived from:** D04 (`conversations/conv_pines018_item_transfer.eml`)

The system shall process batch updates for datasets containing up to 9.6 million library materials without locking the database for the duration of the full batch. It shall divide large updates into smaller batches. Processing shall preserve database availability for other system operations while the update is underway.

<details><summary>Evidence (1 source statements)</summary>

- D04: "One concern: with 9.6 million items, batch updates need to be efficient. We should process in smaller batches to avoid locking the database."

</details>

<a id="req-arc-004"></a>
#### REQ-ARC-004: Inactive Patron Report Performance

- **Priority:** P3 (Could have) - The three D09 candidates describe one report’s performance needs, raised by one stakeholder without a priority marker.
- **Type:** non-functional
- **Derived from:** D09 (`conversations/conv_pines024_inactive_patrons.eml`)

The system shall generate the inactive patrons report for a dataset of 3.5 million patrons. It shall optimize the report query and run the report as a background process when needed to avoid delaying interactive operations. The system shall cache report results to support subsequent access without repeating the full query.

<details><summary>Evidence (3 source statements)</summary>

- D09: "One performance note: for 3.5 million patrons, this query could be slow. We should run it as a background report and cache results."
- D09: "One performance note: for 3.5 million patrons, this query could be slow."
- D09: "For 3.5 million patrons, this query could be slow."

</details>

<a id="req-arc-005"></a>
#### REQ-ARC-005: Centralized Multi-Location Service

- **Priority:** P1 (Must have) - The same central-service architecture is stated in D10, D18, and D19 and is a prerequisite for serving multiple library locations.
- **Type:** constraint
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`)

The system shall provide centrally consolidated management processes that accept input from and provide services to multiple library locations. The central service shall support the consortium’s distributed operations rather than requiring each location to operate an independent instance. The system shall make its services available to the participating locations.

<details><summary>Evidence (3 source statements)</summary>

- D10: "The Management Processes are consolidated at a central location and accept input from and provide services to multiple library locations."
- D18: "Management Processes are consolidated at a central location, and accept input and provide services to multiple locations."
- D19: "AS-2: Management Processes are consolidated at a central location, and accept input and provide services to multiple locations."

</details>

<a id="req-arc-006"></a>
#### REQ-ARC-006: Server Platform Compatibility

- **Priority:** P1 (Must have) - D10 marks Linux or Solaris operation High Priority, while D16 and D18 confirm the supported operating systems and D16 provides the server profile.
- **Type:** constraint
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D16 (`interview_sysadmin_2009-05-10.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`)

The system shall operate on Linux and Solaris server environments, including Red Hat Enterprise Linux 5 and Solaris 10 on SPARC hardware. It shall be deployable on the stated primary-server profile of dual quad-core processors and 32 GB of RAM. These environments shall be supported for the system’s reporting and management functions.

<details><summary>Evidence (5 source statements)</summary>

- D10: "The system must operate on a Linux or Solaris server environment."
- D16: "any reporting system needs to work on both Linux and Solaris."
- D18: "Management Processes shall operate on a Linux or Solaris server."
- D16: "So any reporting system needs to work on both Linux and Solaris."
- D16: "Our main server is a Red Hat Enterprise Linux 5 box with dual quad-core processors and 32GB of RAM."

</details>

<a id="req-arc-007"></a>
#### REQ-ARC-007: Relational Database Compatibility

- **Priority:** P1 (Must have) - D10 marks use of a fully relational database High Priority, and D16, D18, and D19 confirm the relational design and its use for reporting.
- **Type:** constraint
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D16 (`interview_sysadmin_2009-05-10.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`)

The system shall use and work with a fully relational database structure, including PostgreSQL 8.3 compatibility. Reporting queries shall support complex joins against that structure and shall not require denormalized reporting schemas. The database design shall preserve the relational model used by the system’s existing data structures.

<details><summary>Evidence (8 source statements)</summary>

- D10: "The system must use a fully relational database back-end."
- D16: "It runs PostgreSQL 8.3 for the database."
- D16: "We're using PostgreSQL now, which is a fully relational database. That's good - it means we can write complex joins. The reporting system needs to work with the relational structure, not fight against it."
- D16: "Some systems try to use denormalized reporting schemas, but that creates sync issues. I'd prefer to keep everything in the main relational database."
- D18: "Management Processes shall use a fully relational database back-end."
- D19: "Robert confirmed that the system must use a fully relational database back-end."
- D19: "The reporting system must work WITH the relational structure, not against it."
- D19: "I strongly recommend against denormalization for reporting,"

</details>

<a id="req-arc-008"></a>
#### REQ-ARC-008: Reporting Performance Isolation

- **Priority:** P1 (Must have) - D10 marks operation during open hours High Priority, D16 calls it a key requirement and a major concern, and D14, D18, D19, and D20 also identify reporting isolation or performance needs.
- **Type:** non-functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`), D16 (`interview_sysadmin_2009-05-10.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`), D20 (`survey_results_2009.txt`)

The system shall support queued and background execution of long-running reports and searches so that they can run during open hours without disrupting other system functions. Reporting shall be isolated from production operations through a separate reporting database or a read-only reporting replica, and reports shall not slow the OPAC or patron catalog access. The system shall provide background processing for reports that would otherwise take too long during busy hours.

<details><summary>Evidence (11 source statements)</summary>

- D10: "It is highly desirable that searches and reports can be processed during open hours without disrupting other system functions."
- D14: "6. Separate reporting from production operations"
- D14: "No separate reporting database/replica (reports run on production database)"
- D14: "No background processing for long-running reports"
- D16: "We need to make sure reports can be queued and processed in the background."
- D16: "Or we need read-only reporting replicas."
- D16: "The key requirement is that searches and reports can be processed during open hours without disrupting other system functions."
- D16: "If the reporting system is doing a big query, it should NOT slow down the OPAC."
- D18: "It is highly desirable that searches and reports can be processed during open hours without disrupting other system functions."
- D19: "If a report is running, it should not slow down the OPAC."
- D20: ""Reports take too long to run during busy hours""

</details>

<a id="req-arc-009"></a>
#### REQ-ARC-009: Browser And Client Access

- **Priority:** P1 (Must have) - D10 marks browser or Windows-client access High Priority, and D18 later marks access Critical while specifying the same browser versions.
- **Type:** constraint
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D16 (`interview_sysadmin_2009-05-10.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`)

The system shall be accessible through a web browser or a Windows-compatible client. If the system is web-browser based, it shall support Microsoft Internet Explorer version 6.0 and later and Mozilla Firefox version 2.0 and later. These access options and browser versions shall be supported for system users.

<details><summary>Evidence (5 source statements)</summary>

- D10: "The system must be accessible through a web browser or a Windows-compatible client."
- D10: "If web-browser based, the system must be accessible through Microsoft Internet Explorer (version 6.0 and later) and Mozilla Firefox (version 2.0 and later)."
- D16: "So we need to support IE 6.0+ and Firefox 2.0+."
- D18: "Management Processes shall be accessible through a web-browser or a Windows-compatible client."
- D18: "If web-browser based, Management Processes shall be accessible through Microsoft Internet Explorer (v.6.0 and later) and Mozilla Firefox (v.2.0 and later)."

</details>

<a id="req-arc-010"></a>
#### REQ-ARC-010: Accessibility And Assistive Technology

- **Priority:** P1 (Must have) - D16 explicitly marks properly structured, accessible HTML output as MUST, supporting P1.
- **Type:** non-functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`), D16 (`interview_sysadmin_2009-05-10.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`)

The system shall comply with Section 508 accessibility requirements and support staff members using screen readers, screen-magnification software, and other assistive technologies. Supported examples shall include JAWS, NVDA, and ZoomText, and blind staff members shall be able to run reports. The online help system shall be accessible to screen readers, and accessible HTML output shall be properly structured using semantic HTML, alt text, and ARIA labels. Accessibility shall apply across system output and be verifiable using the supported assistive technologies and output structure.

<details><summary>Evidence (9 source statements)</summary>

- D10: "The system must be accessible with screen-reading software, screen-magnification software, and other assistive technology programs designed to increase accessibility."
- D14: "5. Implement accessibility compliance"
- D16: "The HTML output needs to be properly structured with alt tags, ARIA labels, and proper semantic HTML."
- D16: "This is non-negotiable. As a public institution, we MUST comply with Section 508 accessibility requirements."
- D16: "The system needs to work with:  - Screen readers like JAWS and NVDA  - Screen magnification software like ZoomText  - Other assistive technology programs"
- D16: "The HTML output needs to be properly structured with alt tags, ARIA labels, and proper semantic HTML."
- D16: "We can't have blind staff members unable to run reports."
- D18: "Management Processes shall be accessible with screen-reading software, screen-magnification software, and other software programs designed to increase accessibility. ... We need to support JAWS, NVDA, ZoomText, and other assistive technologies. Section 508 compliance is mandatory."
- D19: "This has to be accessible too. The help system needs to work with screen readers."

</details>

<a id="req-arc-011"></a>
#### REQ-ARC-011: Standards-Compliant HTML

- **Priority:** P1 (Must have) - D16 marks standards-compliant HTML Must, and D10, D18, and D19 independently include standards-compliant HTML requirements.
- **Type:** constraint
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D16 (`interview_sysadmin_2009-05-10.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`)

The system shall produce standards-compliant HTML for all web-based components and web output. The generated HTML shall be valid against W3C standards. This requirement shall apply to HTML produced by the system’s web components and shall be verifiable through HTML validation.

<details><summary>Evidence (5 source statements)</summary>

- D10: "The system must produce standards-compliant HTML output for web-based components."
- D16: "And the system needs to produce standards-compliant HTML."
- D18: "Management Processes shall produce standards-compliant HTML."
- D19: "The system must produce standards-compliant HTML."
- D19: "We need to make sure all HTML output validates against W3C standards,"

</details>

<a id="req-arc-012"></a>
#### REQ-ARC-012: Separate Environments And Configuration Migration

- **Priority:** P2 (Should have) - D16 calls configuration migration a key requirement, and D10, D14, D18, and D19 also identify environment separation or migration needs.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`), D16 (`interview_sysadmin_2009-05-10.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`)

The system shall provide separate development, training, and production environments. Staff members shall be able to practice and experiment in training without risking production data, and developers shall be able to test reports without affecting production. The system shall support migrating configurations between environments, including export and import of report templates, permission settings, saved queries, and other configuration.

<details><summary>Evidence (12 source statements)</summary>

- D10: "The system must provide a development and training environment with the ability to migrate configurations to a production environment."
- D14: "7. Provide a development/training environment with migration capability"
- D14: "No development/training environment separation"
- D14: "No configuration migration between environments"
- D16: "Developers need a place to test new reports without affecting production. And new staff members need a training environment where they can practice running reports without worrying about making mistakes."
- D16: "The key is that configurations developed in training/dev need to be migratable to production."
- D16: "We need export/import functionality for report templates, permission settings, and other configuration."
- D18: "Management Processes shall provide a development and training environment with the ability to migrate configurations to a production environment."
- D18: "We need to make sure report templates and configurations can be exported/imported."
- D19: "The need for separate development, training, and production environments was discussed."
- D19: "What we need is a way to migrate configurations between them. Export/import of templates, permission settings, and saved queries."
- D19: "And the training environment needs to be safe - staff should be able to experiment without risking production data."

</details>

<a id="req-arc-013"></a>
#### REQ-ARC-013: OPAC Functional Independence

- **Priority:** P1 (Must have) - D16 explicitly states that the system must not constrain the OPAC, and D10 and D18 repeat this constraint in their requirements.
- **Type:** constraint
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D16 (`interview_sysadmin_2009-05-10.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`)

The system shall not constrain the functionality or features of the OPAC. The OPAC shall remain a separate concern from the management reporting functions, preserving responsive patron access to the catalog. The system’s requirements and operation shall not limit OPAC functionality.

<details><summary>Evidence (4 source statements)</summary>

- D10: "These requirements must not constrain functionality or features of the Online Public Access Catalog (OPAC) module."
- D16: "The management reporting system must not constrain the OPAC in any way."
- D18: "These requirements shall not constrain functionality or features of the Online Public Access Catalog (OPAC) module."
- D16: "The management reporting system must not constrain the OPAC in any way. These are separate concerns. Patrons need fast, responsive access to the catalog."

</details>

<a id="req-arc-014"></a>
#### REQ-ARC-014: Enterprise Automation System Dependency

- **Priority:** P1 (Must have) - D10, D18, and D19 state the enterprise-system dependency, which D19 identifies as an architectural assumption and prerequisite for relying on shared infrastructure.
- **Type:** constraint
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`)

The system shall operate as part of an enterprise-level Library Automation System and rely on its data structures and functionality, including its Acquisitions and Cataloging modules. It shall be able to rely on established enterprise infrastructure such as redundant servers, backup systems, and network connectivity. These dependencies shall be taken into account in the system’s architecture.

<details><summary>Evidence (6 source statements)</summary>

- D10: "Management Processes rely on the data structures and functionality of an enterprise-level Library Automation System, including Acquisitions and Cataloging modules."
- D18: "Management Processes are part of an enterprise-level Library Automation System."
- D18: "Management Processes rely on the data structures and functionality of an enterprise-level Library Automation System, including Acquisitions and Cataloging modules."
- D19: "AS-1: Management Processes are part of an enterprise-level Library Automation System.  Robert: "This means we can rely on the infrastructure - redundant servers, backup systems, network connectivity.""
- D19: "DE-1: Management Processes rely on the data structures and functionality of an enterprise-level Library Automation System, including Acquisitions and Cataloging modules."
- D10: "AS-1: Management Processes are part of an enterprise-level Library Automation       System."

</details>

<a id="req-arc-015"></a>
#### REQ-ARC-015: Vendor Data Interfaces

- **Priority:** P3 (Could have) - The vendor-interface need appears in D10, D18, and D19, but none marks it critical or provides a specific operational priority.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`)

The system shall interface with vendor websites through published APIs or automated transfer of standard-format data files. Supported file-format examples shall include USMARC21 and EDIFACT. These interfaces shall support the system’s exchange of data with vendors.

<details><summary>Evidence (3 source statements)</summary>

- D10: "Management Processes rely on ... a variety of vendor websites, via published APIs and/or automated transfer of standard-format data files (e.g., USMARC21, EDIFACT)."
- D18: "Management Processes interface with a variety of vendor websites, via published APIs and/or automated transfer of standard-format data files (e.g., USMARC21, EDIFACT)."
- D19: "DE-2: Management Processes interface with a variety of vendor websites, via published APIs and/or automated transfer of standard-format data files (e.g., USMARC21, EDIFACT)."

</details>

<a id="req-arc-016"></a>
#### REQ-ARC-016: Read-Only OPAC Data Access

- **Priority:** P2 (Should have) - D18 identifies the OPAC data needed for queries, and D19 explicitly confirms that the system shall query this data without modifying it.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`)

The system shall interact with the patron interface, including the OPAC, to query data such as hold requests and circulation information. It shall not modify OPAC data through this interaction. The interface shall therefore provide the reporting system with query access while preserving the OPAC data as read-only to this system.

<details><summary>Evidence (3 source statements)</summary>

- D10: "Management Processes interact with a patron interface, also known as an Online Public Access Catalog (OPAC)."
- D18: "Management Processes interact with a patron interface, also known as an Online Public Access Catalog (OPAC)."
- D19: "The reporting system queries this data, but doesn't modify it."

</details>

<a id="req-arc-017"></a>
#### REQ-ARC-017: Actionable Error Feedback

- **Priority:** P2 (Should have) - Actionable error feedback is important for routine report and query troubleshooting, but the system remains usable with a workaround.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`)

The system shall display a user-facing error category and a corrective message when a report or query fails. For report failures, the system shall identify the affected table, field, and error type whenever that information is available. Administrators shall be able to access diagnostic details that include the operation, timestamp, and error identifier, without exposing personally identifiable information to unauthorized users.

<details><summary>Evidence (4 source statements)</summary>

- D10: "The system must provide thorough high-level error reporting and feedback, and shall allow low-level query-specific feedback for Local and Global System Administrators from the front-end interface."
- D18: "The system shall provide thorough high-level error reporting and feedback and shall allow low-level query-specific feedback for Local and Global System Administrators from the front-end interface."
- D19: "The system shall provide thorough high-level error reporting and feedback, and shall allow low-level query-specific feedback for administrators."
- D19: "When a report fails, we need to know WHY," Robert said. "Generic error messages like 'query failed' are useless. We need specifics - which table, which field, what kind of error."

</details>

<a id="req-arc-018"></a>
#### REQ-ARC-018: Data Retention Policies

- **Priority:** P1 (Must have) - Audit retention is explicitly specified, and statutory transaction retention is a legal obligation and prerequisite for compliant operation.
- **Type:** constraint
- **Derived from:** D11 (`email_financial_reports.eml`), D12 (`email_report_features.eml`)

The system shall retain audit records for seven years and transaction records for the retention period required by applicable State Law. Before production use, an authorized compliance administrator shall configure the transaction-retention period and record the governing law, jurisdiction, and effective date. The system shall apply retention periods by data category, prevent deletion before the applicable period expires, and log authorized retention changes and resulting deletions.

<details><summary>Evidence (2 source statements)</summary>

- D11: "Some data needs to be retained for 7 years for audit purposes. The system needs to enforce retention policies."
- D12: "State law requires us to retain transaction data for X years"

</details>

<a id="req-arc-019"></a>
#### REQ-ARC-019: Login Without Specialized Infrastructure

- **Priority:** P3 (Could have) - D13 raises this access constraint in one stakeholder email and provides no explicit priority marker.
- **Type:** constraint
- **Derived from:** D13 (`email_staff_login.eml`)

The system shall operate without requiring streamlined-login infrastructure at a library location. Examples of infrastructure that shall not be mandatory include card readers. Staff members shall be able to use the system even where such specialized login equipment is not available.

<details><summary>Evidence (1 source statements)</summary>

- D13: "the system should not REQUIRE the streamlined login."

</details>

<a id="req-arc-020"></a>
#### REQ-ARC-020: Secondary-Site Disaster Recovery

- **Priority:** P3 (Could have) - D16 identifies secondary-site disaster recovery and reporting as a need but provides no priority marker or recovery-time target.
- **Type:** non-functional
- **Derived from:** D16 (`interview_sysadmin_2009-05-10.txt`)

The system shall support operation at a secondary site for disaster recovery and reporting. The supported secondary-site environment shall include Solaris 10 on SPARC hardware. This capability shall allow the system’s reporting functions to be available from the stated secondary site.

<details><summary>Evidence (1 source statements)</summary>

- D16: "We also have a secondary site that runs Solaris 10 on SPARC hardware for disaster recovery and reporting."

</details>

<a id="req-arc-021"></a>
#### REQ-ARC-021: Optional Vendor EDI Data

- **Priority:** P3 (Could have) - D19 presents this as a specific vendor-data need without a priority marker and notes that the data is not available at every library location.
- **Type:** functional
- **Derived from:** D19 (`meeting_tech_subcommittee_2009-06-30.txt`)

The system shall handle EDI ordering data when a vendor provides it. The system shall not require EDI ordering data to be present for every library location. Absence of that data shall not prevent the system from operating with other available ordering information.

<details><summary>Evidence (1 source statements)</summary>

- D19: "We have some vendors that provide EDI ordering data," Robert explained. "The reporting system needs to handle this data, but we can't rely on it being present at every library."

</details>

### 6.8 Documentation, Scope, and Governance (DOC)

Documentation, help, requirements governance, development methodology, testing governance, system scope, management-process context, and stakeholder responsibilities.

<a id="req-doc-001"></a>
#### REQ-DOC-001: Data Specifications

- **Priority:** P1 (Must have) - D10 explicitly marks complete data specifications High Priority, and the requirement is repeated in D18 and D19, including a specific request for field names, data types, and relationships.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`)

The system shall provide complete data specifications for the data it maintains or accesses through Management Processes. The specifications shall cover authority, bibliographic, order, item, and hold/request records, as well as other relevant records. The data dictionaries shall identify field names, data types, and relationships. The software developer shall deliver these specifications for use by library managers, administrators, staff members, and developers.

<details><summary>Evidence (4 source statements)</summary>

- D10: "The developer must provide complete data specifications for authority records, bibliographic records, order records, item records, hold/request records, and other records maintained or accessed by the Management Processes."
- D18: "The software developer shall provide complete data specifications for authority records, bibliographic records, order records, item records, hold/request records, and other records maintained or accessed by Management Processes."
- D19: "The developer must provide complete data specifications for: - Authority records - Bibliographic records - Order records - Item records - Hold/request records - Other records maintained or accessed by Management Processes"
- D19: "We need data dictionaries - field names, data types, relationships."

</details>

<a id="req-doc-002"></a>
#### REQ-DOC-002: Major Process Descriptions

- **Priority:** P2 (Should have) - Process documentation is important to implementation and daily operation, but is not itself a core system function.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`)

The system shall include process documentation with separate sections for bibliographic record import, bibliographic record export, validation against internal authority sources, validation against external authority sources, and standard reports. Each section shall identify its purpose, inputs, outputs, responsible roles, main process steps, and error or exception handling. The documentation shall be reviewed by a library manager and a technical reviewer, who shall confirm that every listed section is present.

<details><summary>Evidence (3 source statements)</summary>

- D10: "The developer must provide a thorough high-level description of major processes, including bibliographic record import and export, validation of bibliographic records against internal and external authority sources, and standard reports."
- D18: "The software developer shall provide a thorough high-level description of major processes, including bibliographic record import and export, validation of bibliographic records against internal and external authority sources, and standard reports."
- D19: "The developer must provide a thorough high-level description of major processes, including: - Bibliographic record import and export - Validation of bibliographic records against internal and external authority sources - Standard reports"

</details>

<a id="req-doc-003"></a>
#### REQ-DOC-003: Online Help

- **Priority:** P1 (Must have) - D10 explicitly marks online help High Priority, D16 and D19 also request help capabilities, and D18 states that context-sensitive help is critical.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D14 (`evergreen_reference_2009.txt`), D16 (`interview_sysadmin_2009-05-10.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`), D19 (`meeting_tech_subcommittee_2009-06-30.txt`)

The system shall provide searchable, navigable online help in HTML that is hierarchical, cross-linked, and integrated with the reports interface. The help shall describe and illustrate system functions, explain how staff members run reports, and be available as context-sensitive guidance so users do not need to leave the system or contact information technology staff for routine instructions. The help shall support library staff members using reports and other system functions.

<details><summary>Evidence (8 source statements)</summary>

- D10: "The system must provide an online, hierarchical, and cross-linked help system in HTML that describes and illustrates all system functions."
- D14: "No online help system integrated with reports"
- D16: "the help system needs to be online, hierarchical, and cross-linked."
- D16: "The HTML help needs to be searchable and easy to navigate."
- D16: "Staff shouldn't have to call IT every time they want to know how to run a report."
- D18: "The system shall provide an online, hierarchical, and cross-linked help system in HTML that describes and illustrates all system functions."
- D18: "Context-sensitive help is critical. Staff shouldn't have to leave the system to find documentation."
- D19: "The system shall provide an online, hierarchical, and cross-linked help system in HTML."

</details>

<a id="req-doc-004"></a>
#### REQ-DOC-004: Management Reporting And Analysis

- **Priority:** P1 (Must have) - D10 identifies analysis, collection management, and data-driven decisions as the component's purpose, while the D17 meeting records group agreement on five specific management analysis areas.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`), D17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`)

The system shall provide reports and analysis tools that help library managers, administrators, and staff members analyze operations, manage library materials, and make data-informed decisions. The tools shall support analysis of library material and its use by patrons, capacity and distribution across library locations, patron demographics and interests, staff member productivity and workflow, and financial transactions. Users shall be able to use these capabilities for planning, evaluation, and oversight.

<details><summary>Evidence (3 source statements)</summary>

- D17: "Management Processes - that is, reports and analysis tools used by library managers, administrators, and staff for planning, evaluation, and oversight purposes."
- D17: "The following scope items were identified:    - Analyzing the Library collection and its use by patrons   - Analyzing branch capacity and optimal distribution of the collection   - Analyzing demographics and interests of patrons   - Analyzing staff productivity and workflow   - Tracking and verifying financial transactions"
- D10: "The Management Processes component of an ILS provides the tools needed for library administrators, managers, and staff to analyze operations, manage collections, and make data-driven decisions."

</details>

<a id="req-doc-005"></a>
#### REQ-DOC-005: Management Scope

- **Priority:** P1 (Must have) - The D17 group explicitly agreed to limit the specification to management activities, identified patron-facing exclusions, and noted that Acquisitions and Cataloging were being specified separately.
- **Type:** constraint
- **Derived from:** D17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`)

The system shall limit its reporting specification to requirements that directly or indirectly support management activities. It shall exclude day-to-day patron-facing OPAC and circulation client functions, as well as Acquisitions and Cataloging modules that are specified separately. The scope shall address management reporting rather than replacing those separate functions or specifications.

<details><summary>Evidence (3 source statements)</summary>

- D17: "She clarified that this does NOT include day-to-day patron-facing functions (those are part of the OPAC and circulation client)."
- D17: "She said PINES is currently working on separate specifications for Acquisitions and Cataloging modules. The group agreed to specify only those requirements that directly or indirectly relate to management activities."
- D17: "The group agreed to specify only those requirements that directly or indirectly relate to management activities."

</details>

<a id="req-doc-006"></a>
#### REQ-DOC-006: Iterative Development And Review

- **Priority:** P2 (Should have) - Stakeholder review is important to producing a usable system, but a documented review process can be adjusted without preventing system use.
- **Type:** constraint
- **Derived from:** D17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`)

The system shall be developed through iterative reviews that include library end users. The development process shall provide at least two prototype reviews: one after initial functional requirements are agreed and one after the first interface prototype is available. Each review shall record attendees, feedback, decisions, and resulting changes. Reviewers shall be able to confirm that functional requirements are addressed before detailed interface and data-structure refinements are approved.

<details><summary>Evidence (2 source statements)</summary>

- D17: "for now the focus should be on functional requirements. She mentioned that UI and data structures would require further specification using an iterative, prototype-oriented methodology."
- D17: "The group discussed the development approach. It was noted that development would likely happen in a highly collaborative and iterative environment where end-users have multiple opportunities to review prototypes."

</details>

<a id="req-doc-007"></a>
#### REQ-DOC-007: SRS Readability And Detail

- **Priority:** P2 (Should have) - A complete, readable SRS is important for implementation and review, but it is a documentation quality requirement rather than a core user function.
- **Type:** constraint
- **Derived from:** D17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`)

The system shall be specified in SRS documents containing requirement identifiers, names, descriptions, types, priorities, acceptance criteria, dependencies, and source references. Each requirement shall be understandable to readers familiar with library services and sufficiently precise for implementation and verification. A completeness review shall check that every requirement has the listed fields, uses defined glossary terms consistently, and contains testable acceptance criteria before the SRS is approved.

<details><summary>Evidence (2 source statements)</summary>

- D17: "She emphasized the need to aim for a high level of readability for a non-technical audience while providing enough specificity for developers."
- D17: "It was assumed that readers have a general understanding of Library services and processes and do not require definition of common Library terminology."

</details>

<a id="req-doc-008"></a>
#### REQ-DOC-008: Requirements Foundation

- **Priority:** P3 (Could have) - D17 records a single stakeholder statement that PINES staff decided to use the King County and Galecia Group draft as the foundation and adapt it to their needs.
- **Type:** constraint
- **Derived from:** D17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`)

The system shall have requirements documentation based on the King County Library System and Galecia Group draft Software Requirements Specification, adapted to the needs of the library system. The adapted specification shall serve as a foundation rather than a substitute for requirements identified for this system. Library stakeholders shall use the resulting documentation to communicate the agreed system needs to project managers and developers.

<details><summary>Evidence (1 source statements)</summary>

- D17: "Katherine explained that King County Library System (WA) had previously worked with Galecia Group to develop a comprehensive Software Requirements Specification for a reports interface. PINES staff decided to use that as a foundation and adapt it for our specific needs."

</details>

<a id="req-doc-009"></a>
#### REQ-DOC-009: Staff Report Content Creation

- **Priority:** P3 (Could have) - D17 identifies staff members as the primary report content creators, but the request appears in one meeting source and has no explicit critical or high-priority marker.
- **Type:** functional
- **Derived from:** D17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`)

The system shall allow staff members employed by PINES member libraries to create report content. Staff members shall be supported as the primary content creators for reports. This requirement applies to report creation within the management reporting capabilities and distinguishes content creation from the system's implementation and maintenance responsibilities.

<details><summary>Evidence (1 source statements)</summary>

- D17: "[Jenny: Staff are our primary content creators for reports]"

</details>

<a id="req-doc-010"></a>
#### REQ-DOC-010: Reports Testing Governance

- **Priority:** P2 (Should have) - Report review and testing are important quality controls, but do not prevent system use when a report is temporarily unavailable.
- **Type:** constraint
- **Derived from:** D17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`), D18 (`meeting_minutes/meeting_2009-07-20_minutes.txt`)

The system shall require the Reports Working Group or its designated reports testing group to review and test each new report before that report is accepted for production use. The review shall record the report version, test cases, test results, defects, and approval decision. A report with an unresolved critical defect or without recorded approval shall not be accepted. This process shall apply to new reports and material changes to existing reports.

<details><summary>Evidence (3 source statements)</summary>

- D17: "Become the Reports testing group, through which all new Reports development would be filtered."
- D18: "Become the Reports testing group, through which all new Reports development would be filtered."
- D17: "- Become the Reports testing group, through which all new Reports development      would be filtered."

</details>

<a id="req-doc-011"></a>
#### REQ-DOC-011: Reports Requirements Inventory

- **Priority:** P2 (Should have) - The inventory supports planning and review and is important to stakeholders, but is not required for routine system use.
- **Type:** functional
- **Derived from:** D17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`)

The system shall maintain requirements documentation listing the reports needed for management processes and the desired reports functionality for a future Evergreen release. The inventory shall identify each report or capability by name, requirement identifier, purpose, users, required inputs, and expected outputs, and shall link each entry to its associated requirement. Library managers, staff members, and the Reports Working Group shall be able to review the inventory for planning and assessment.

<details><summary>Evidence (3 source statements)</summary>

- D17: "- Document optimal Reports functionality within a future Evergreen release and develop a list of requirements."
- D17: "- Compile a list of reports needed for an Executive Reports Interface."
- D17: "- Document optimal Reports functionality within a future Evergreen release      and develop a list of requirements."

</details>

<a id="req-doc-012"></a>
#### REQ-DOC-012: SRS Requirement Contributions

- **Priority:** P3 (Could have) - Ongoing stakeholder contributions are beneficial but are a process enhancement rather than an essential system capability.
- **Type:** functional
- **Derived from:** D17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`)

The system shall provide a documented process through which library managers and staff members can submit proposed requirements for consideration in the SRS. Each submission shall capture its submitter, date, description, rationale, and review disposition. The requirements owner shall acknowledge submissions and record whether each is accepted, deferred, or rejected, including the decision rationale, so project managers and developers can track requirements input.

<details><summary>Evidence (1 source statements)</summary>

- D17: "this SRS would be intended both for library managers and staff who may contribute additional requirements, and for software project managers and developers who will implement the requirements."

</details>

<a id="req-doc-013"></a>
#### REQ-DOC-013: Library Manager Responsibilities

- **Priority:** P3 (Could have) - D17 describes the responsibilities of library managers in one stakeholder-role statement, with no explicit high-priority marker or evidence of repeated requests.
- **Type:** functional
- **Derived from:** D17 (`meeting_minutes/meeting_2009-03-15_minutes.txt`)

The system shall support library managers in supervising one organizational unit and providing input to the design and implementation of library services. The system's management capabilities shall accommodate this supervisory and service-planning role. Library managers shall be supported as stakeholders who contribute operational insight to service decisions.

<details><summary>Evidence (1 source statements)</summary>

- D17: "Library Managers: Supervise a single organizational unit and provide input to design and implementation of Library services."

</details>

<a id="req-doc-014"></a>
#### REQ-DOC-014: Separate Missing And In-Transit Requirements

- **Priority:** P3 (Could have) - Separating these documentation items supports clear review but does not affect the system’s core operation.
- **Type:** constraint
- **Derived from:** D05 (`conversations/conv_pines019_020_missing_intransit.eml`)

The system shall maintain separate requirement records for the missing or damaged report and the in-transit report. Each record shall have its own identifier, description, acceptance criteria, and review disposition. The requirements documentation may cross-reference related needs, but shall not combine these reports into one requirement or use one report’s acceptance results as evidence that the other report meets its criteria.

<details><summary>Evidence (1 source statements)</summary>

- D05: "These are two separate but related requirements. Let's track them separately in our documentation."

</details>

<a id="req-doc-015"></a>
#### REQ-DOC-015: Management Of Library Services

- **Priority:** P3 (Could have) - The need appears in one early draft with no explicit priority marker, and no additional evidence establishes it as essential or regularly used.
- **Type:** functional
- **Derived from:** D10 (`early_draft_srs_galecia.txt`)

The system shall facilitate the management of library services, programs, and policies through its Management Processes. These capabilities shall support the management activities of the library system. Library managers and other responsible stakeholders shall be able to use them to manage services, programs, and policies. The system shall not imply specific workflows or controls beyond this stated scope.

<details><summary>Evidence (1 source statements)</summary>

- D10: "The Management Processes facilitate the management of Library services, programs, and policies."

</details>

## 7. Traceability Matrix

| Doc ID | File | Requirements |
|---|---|---|
| D01 | `conversations/conv_pines014_material_volume.eml` | REQ-RPT-001 |
| D02 | `conversations/conv_pines015_capacity_interface.eml` | REQ-RPT-002, REQ-ARC-002 |
| D03 | `conversations/conv_pines016_shelf_space.eml` | REQ-RPT-003 |
| D04 | `conversations/conv_pines018_item_transfer.eml` | REQ-RPT-008, REQ-COL-001, REQ-COL-002, REQ-COL-003, REQ-COL-004, REQ-COL-005, REQ-COL-006, REQ-COL-007, REQ-COL-008, REQ-SEC-008, REQ-ARC-003 |
| D05 | `conversations/conv_pines019_020_missing_intransit.eml` | REQ-COL-009, REQ-COL-010, REQ-COL-011, REQ-COL-025, REQ-DOC-014 |
| D06 | `conversations/conv_pines021_item_purging.eml` | REQ-COL-012, REQ-COL-013, REQ-COL-014, REQ-COL-016, REQ-COL-017, REQ-COL-018, REQ-SEC-010, REQ-SEC-013 |
| D07 | `conversations/conv_pines022_deletions.eml` | REQ-SEC-010, REQ-SEC-011, REQ-SEC-012 |
| D08 | `conversations/conv_pines023_patron_characteristics.eml` | REQ-PAT-001, REQ-PAT-002 |
| D09 | `conversations/conv_pines024_inactive_patrons.eml` | REQ-PAT-002, REQ-PAT-008, REQ-ARC-004 |
| D10 | `early_draft_srs_galecia.txt` | REQ-RPT-001, REQ-RPT-002, REQ-RPT-003, REQ-RPT-004, REQ-RPT-006, REQ-RPT-007, REQ-RPT-009, REQ-RPT-010, REQ-RPT-011, REQ-RPT-012, REQ-RPT-013, REQ-RPT-014, REQ-RPT-015, REQ-RPT-016, REQ-RPT-017, REQ-RPT-018, REQ-RPT-019, REQ-RPT-020, REQ-RPT-021, REQ-RPT-022, REQ-RPT-023, REQ-RPT-024, REQ-RPT-025, REQ-RPT-026, REQ-RPT-027, REQ-RPT-028, REQ-RPT-029, REQ-RPT-030, REQ-RPT-031, REQ-RPT-032, REQ-RPT-033, REQ-RPT-034, REQ-COL-001, REQ-COL-009, REQ-COL-011, REQ-COL-012, REQ-COL-013, REQ-COL-014, REQ-COL-016, REQ-COL-019, REQ-PAT-001, REQ-PAT-002, REQ-PAT-005, REQ-PAT-006, REQ-FIN-001, REQ-FIN-002, REQ-FIN-003, REQ-FIN-004, REQ-FIN-005, REQ-FIN-006, REQ-FIN-007, REQ-FIN-008, REQ-FIN-009, REQ-TRN-001, REQ-TRN-002, REQ-TRN-004, REQ-TRN-005, REQ-TRN-006, REQ-TRN-007, REQ-TRN-008, REQ-TRN-009, REQ-TRN-010, REQ-TRN-011, REQ-TRN-012, REQ-TRN-013, REQ-SEC-001, REQ-SEC-003, REQ-SEC-004, REQ-SEC-005, REQ-SEC-007, REQ-SEC-009, REQ-SEC-011, REQ-SEC-014, REQ-ARC-001, REQ-ARC-005, REQ-ARC-006, REQ-ARC-007, REQ-ARC-008, REQ-ARC-009, REQ-ARC-010, REQ-ARC-011, REQ-ARC-012, REQ-ARC-013, REQ-ARC-014, REQ-ARC-015, REQ-ARC-016, REQ-ARC-017, REQ-DOC-001, REQ-DOC-002, REQ-DOC-003, REQ-DOC-004, REQ-DOC-015 |
| D11 | `email_financial_reports.eml` | REQ-FIN-001, REQ-FIN-002, REQ-FIN-003, REQ-FIN-004, REQ-FIN-005, REQ-FIN-006, REQ-FIN-007, REQ-FIN-008, REQ-FIN-011, REQ-ARC-018 |
| D12 | `email_report_features.eml` | REQ-RPT-004, REQ-RPT-006, REQ-RPT-011, REQ-RPT-013, REQ-RPT-014, REQ-RPT-027, REQ-PAT-005, REQ-SEC-003, REQ-SEC-004, REQ-SEC-005, REQ-ARC-018 |
| D13 | `email_staff_login.eml` | REQ-SEC-001, REQ-SEC-002, REQ-SEC-003, REQ-SEC-015, REQ-ARC-019 |
| D14 | `evergreen_reference_2009.txt` | REQ-RPT-004, REQ-RPT-006, REQ-RPT-007, REQ-RPT-009, REQ-RPT-010, REQ-RPT-013, REQ-RPT-014, REQ-RPT-015, REQ-RPT-016, REQ-RPT-017, REQ-RPT-018, REQ-RPT-021, REQ-RPT-022, REQ-RPT-023, REQ-RPT-024, REQ-RPT-025, REQ-RPT-026, REQ-RPT-027, REQ-RPT-028, REQ-RPT-032, REQ-COL-014, REQ-COL-023, REQ-COL-028, REQ-PAT-001, REQ-FIN-009, REQ-FIN-010, REQ-TRN-012, REQ-TRN-015, REQ-TRN-016, REQ-SEC-003, REQ-SEC-004, REQ-SEC-005, REQ-SEC-014, REQ-ARC-008, REQ-ARC-010, REQ-ARC-012, REQ-DOC-003 |
| D15 | `interview_cataloging_2009-05-08.txt` | REQ-RPT-001, REQ-RPT-003, REQ-RPT-005, REQ-RPT-010, REQ-COL-001, REQ-COL-002, REQ-COL-003, REQ-COL-004, REQ-COL-009, REQ-COL-010, REQ-COL-011, REQ-COL-012, REQ-COL-013, REQ-COL-014, REQ-COL-015, REQ-COL-016, REQ-COL-019, REQ-COL-023, REQ-COL-026, REQ-COL-027, REQ-TRN-011, REQ-SEC-011 |
| D16 | `interview_sysadmin_2009-05-10.txt` | REQ-SEC-003, REQ-ARC-006, REQ-ARC-007, REQ-ARC-008, REQ-ARC-009, REQ-ARC-010, REQ-ARC-011, REQ-ARC-012, REQ-ARC-013, REQ-ARC-020, REQ-DOC-003 |
| D17 | `meeting_minutes/meeting_2009-03-15_minutes.txt` | REQ-RPT-006, REQ-RPT-011, REQ-RPT-036, REQ-SEC-003, REQ-SEC-009, REQ-DOC-004, REQ-DOC-005, REQ-DOC-006, REQ-DOC-007, REQ-DOC-008, REQ-DOC-009, REQ-DOC-010, REQ-DOC-011, REQ-DOC-012, REQ-DOC-013 |
| D18 | `meeting_minutes/meeting_2009-07-20_minutes.txt` | REQ-RPT-002, REQ-RPT-003, REQ-RPT-006, REQ-RPT-010, REQ-RPT-011, REQ-RPT-013, REQ-RPT-037, REQ-COL-009, REQ-COL-011, REQ-PAT-001, REQ-FIN-007, REQ-SEC-001, REQ-SEC-003, REQ-ARC-001, REQ-ARC-005, REQ-ARC-006, REQ-ARC-007, REQ-ARC-008, REQ-ARC-009, REQ-ARC-010, REQ-ARC-011, REQ-ARC-012, REQ-ARC-013, REQ-ARC-014, REQ-ARC-015, REQ-ARC-016, REQ-ARC-017, REQ-DOC-001, REQ-DOC-002, REQ-DOC-003, REQ-DOC-010 |
| D19 | `meeting_tech_subcommittee_2009-06-30.txt` | REQ-RPT-017, REQ-RPT-023, REQ-RPT-024, REQ-RPT-025, REQ-RPT-026, REQ-RPT-030, REQ-SEC-003, REQ-ARC-005, REQ-ARC-007, REQ-ARC-008, REQ-ARC-010, REQ-ARC-011, REQ-ARC-012, REQ-ARC-014, REQ-ARC-015, REQ-ARC-016, REQ-ARC-017, REQ-ARC-021, REQ-DOC-001, REQ-DOC-002, REQ-DOC-003 |
| D20 | `survey_results_2009.txt` | REQ-RPT-004, REQ-RPT-005, REQ-RPT-006, REQ-RPT-010, REQ-RPT-013, REQ-RPT-015, REQ-RPT-017, REQ-RPT-018, REQ-RPT-022, REQ-RPT-023, REQ-RPT-024, REQ-RPT-025, REQ-RPT-026, REQ-RPT-028, REQ-RPT-029, REQ-RPT-034, REQ-RPT-035, REQ-COL-001, REQ-COL-002, REQ-COL-004, REQ-COL-023, REQ-PAT-001, REQ-PAT-005, REQ-PAT-007, REQ-FIN-010, REQ-TRN-002, REQ-TRN-004, REQ-TRN-005, REQ-TRN-006, REQ-TRN-007, REQ-TRN-008, REQ-TRN-009, REQ-TRN-010, REQ-TRN-016, REQ-SEC-004, REQ-SEC-011, REQ-ARC-008 |

## 8. Discarded Requirements (Blacklist)

Statements identified as requirements in the input documents but not included in the specification.

| Category | Meaning |
|---|---|
| conflict | Contradicts another (kept) requirement; the conflict was resolved in favour of the other one. |
| superseded | Replaced by a later or more authoritative decision in the corpus. |
| nonsensical | Not meaningful, infeasible, or clearly not intended as a serious requirement. |
| out_of_scope | Concerns something outside the system described by the corpus. |
| not_a_requirement | Context, opinion or observation that does not express a need for the system. |

| ID | Discarded statement | Category | Explanation | Related requirement | Sources |
|---|---|---|---|---|---|
| BL-001 | The system shall provide tested and proven output. | nonsensical | The phrase does not define what output must be tested, what 'proven' means, or any verifiable acceptance condition. It is too vague to form a meaningful requirement and is not retained as a substitute for the specific output and accuracy requirements. | - | D10 |
| BL-002 | The system shall provide a last edit date that includes last circulation. | conflict | This conflicts with the later cataloging interview, which states that the last edit date shall reflect only item-record edits and not circulation, and with the compatible request for a separate last-circulation field. The later, explicit interview statement is retained in Distinguish Edit And Circulation Dates. | REQ-COL-023 (Distinguish Edit And Circulation Dates) | D14 |
| BL-003 | The system shall support reporting decisions for missing demographic fields by either showing nulls for missing data or excluding those records. | conflict | This candidate offers exclusion of records with missing demographic values as an alternative, while the kept requirement, Patron Demographic Analytics, requires optional-field null values to be included rather than silently excluded. The explicit recommendation to include nulls won over this suspiciously phrased alternative, which is framed as a question rather than a settled requirement. | REQ-PAT-001 (Patron Demographic Analytics) | D08 |
| BL-004 | The system shall adhere to architectural constraints to be determined by a technical subcommittee. | superseded | This preliminary statement defers the actual constraints to a future technical subcommittee. The later D19 technical subcommittee meeting specifies architectural constraints, which are represented in the retained requirements. | REQ-ARC-007 (Relational Database Compatibility) | D17 |
| BL-005 | The system shall treat Patrons as residents of the State of Georgia, either possessing a library card or not, utilizing the resources of a PINES member library. | not_a_requirement | This statement defines the term patron for the SRS; it does not express a system capability, constraint, or other system need. | - | D17 |

## Appendix A. Generation Report

| Role | Model | Calls | Input tokens | Output tokens |
|---|---|---|---|---|
| extract | gpt-5-mini | 46 | 127437 | 227344 |
| completeness | gpt-5.4-nano | 46 | 114103 | 5543 |
| taxonomy | gpt-5.6-luna | 1 | 22740 | 12392 |
| consolidate | gpt-6-luna | 13 | 100665 | 56132 |
| review | gpt-5.6-luna | 3 | 45763 | 11461 |
| revise | gpt-6-luna | 2 | 13091 | 14218 |

- Extraction rounds: 3, consolidation patch rounds: 1, review rounds: 3
- Review round 0: 25 issues, approved=False. The requirements contain several duplicate capabilities, a few internal conflicts, inconsistent terminology, and requirements whose acceptance criteria are not sufficiently testable. The four format issues identified by automated checks also remain.
- Review round 1: 14 issues, approved=False. The requirements are generally well structured, but several significant overlaps, terminology inconsistencies, unresolved dependencies, and testability gaps should be fixed before approval.
- Review round 2: 12 issues, approved=False. Significant issues remain involving overlapping reporting requirements, an unresolved query-tool architecture, conflicting retention rules, incomplete specification governance, and several requirements whose behavior is not sufficiently testable.

Open findings of the last review round (not fixed within the iteration limit):

- [conflict] REQ-RPT-004, REQ-RPT-008: REQ-RPT-004 requires a query builder covering multiple data domains, while REQ-RPT-008 requires use of the existing query tool and explicitly prohibits duplicating that function in a separate query mechanism. The requirements do not establish whether these are one shared capability or two different tools.
- [duplicate] REQ-PAT-007, REQ-TRN-005: Both requirements define aggregate checkout renewal statistics and a renewal percentage for a selected reporting period. Their denominators and grouping options differ slightly, but the core calculation is the same.
- [duplicate] REQ-FIN-010, REQ-RPT-026: Both requirements require retrieving historical bill information as it existed at a prior date or period. REQ-RPT-026 already explicitly includes historical bill amounts.
- [duplicate] REQ-PAT-001, REQ-RPT-035: Both requirements provide patron demographic reporting, including age and postal-code dimensions and use for planning. REQ-PAT-001 is broader, but REQ-RPT-035 does not define a clearly separate reporting outcome.
- [duplicate] REQ-RPT-011, REQ-TRN-001, REQ-TRN-002: REQ-RPT-011 requires activity measures and cross-tabulation dimensions that are also required by REQ-TRN-001 and REQ-TRN-002. The overlapping requirements could produce inconsistent definitions of the same statistics.
- [conflict] REQ-TRN-004, REQ-ARC-018: REQ-TRN-004 permits transaction history to be retained for a configurable number of days, while REQ-ARC-018 requires retention for the period required by applicable law. A configured period shorter than the legal minimum would satisfy one requirement and violate the other.
- [format] REQ-DOC-007: REQ-DOC-007 requires every SRS requirement to contain acceptance criteria, dependencies, and source references, but the supplied requirements generally provide only an identifier, name, priority, type, and description. The specification therefore does not meet its own required format and cannot support the mandated completeness review.
- [vague] REQ-RPT-010, REQ-RPT-012, REQ-DOC-011: The required report catalog and baseline refer to “specified” topics, Appendix A, Appendix B, or an approved manifest, but those artifacts are not supplied. Consequently, the required reports, fields, criteria, and expected outputs cannot be determined or tested from the requirements.
- [vague] REQ-RPT-002: The status boundaries are precise for percentage measures but ambiguous for absolute-limit measures. “The configured limit shall define the same status boundaries” does not specify how 80% and 100% thresholds are calculated, rounded, or applied when the measure is an absolute count or volume.
- [vague] REQ-PAT-002: The inactivity calculation depends on undefined terms such as “electronic activity,” “relevant records,” and “when integrated.” It is therefore unclear which events reset inactivity and how an unavailable digital integration affects results.
- [vague] REQ-SEC-015: The requirement asks for controls that “reduce security risks” and “support preventing unauthorized use,” but it does not require any specific behavior or measurable control. It cannot be verified consistently.
- [vague] REQ-RPT-025: The terms “applicable transaction and item data sources” and “query live” are not defined, so implementations may classify the same report differently or claim current-state status using different refresh guarantees.
