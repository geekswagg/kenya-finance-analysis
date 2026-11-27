# Kenya Finance Analysis handover

## Research objective

Build a reproducible, source-linked study of Kenyan public finance. Start with borrowing, debt stocks, debt service, fiscal performance and risk. Use the eventual dashboard to teach budgeting, liquidity, capital allocation and refinancing, with explicit limits on sovereign comparisons to households or businesses.

## M0 baseline

The public repository is `geekswagg/kenya-finance-analysis`. GitHub reports `main` as default, MIT on the existing scaffold, and admin access for the authenticated `geekswagg` account. The supplied handover describes MIT as proposed. The owner confirmed MIT for the incoming code and identified the data as publicly sourced. The repository includes attributed derived observations. Original Treasury PDFs are kept in local intake.

Merged PR #8 contains the earlier empty schema and checks. Keep the branch and reconcile its schema with the supplied starter before making either contract authoritative. The starter distinguishes actual, preliminary and provisional actual, comparator, revised target, published plan and projection. Preserve these distinctions, source-specific units and notes during migration.

The supplied starter is staged under the ignored `data/incoming/starter-v0.1/` directory. The original handover is available under `data/incoming/handover/`. The tracked `data/metadata/source-inventory.json` records all eleven filenames, fiscal years, SHA-256 hashes and ingestion status. The seven starter PDFs match the Drive originals and starter registry. The four additional PDFs are present and hashed. Confirm their official editions and URLs before extraction.

| Fiscal year | Annual borrowing plan | Annual debt report |
| --- | --- | --- |
| 2021/22 | abp21, partial | dm22, pending |
| 2022/23 | abp22, partial | dm23, pending |
| 2023/24 | abp23, partial | dm24, pending |
| 2024/25 | abp24, partial | dm25, pending |
| 2025/26 | abp25, partial | dm26, partial |
| 2026/27 | abp26, partial | Outside this corpus |

## Validation

A fresh local rebuild yielded 259 observations, 259 unique source keys and six review flags. All 19 processed and metadata artifacts matched by bytes or parsed JSON. Nine JSON files differed in formatting. All eight CSV/JSON pairs agreed, and the seven domain exports matched subsets of the master file. The macro projections extend through FY 2029/30.

The rebuild uses manual transcriptions. Independently verify printed pages and source table cells, especially in scanned PDFs. The present flagger groups by identical metric and status. It misses comparisons where statuses or metric IDs differ, including the June 2026 plan/report debt stock and the FY 2021/22 external debt cited under two metric IDs. Preserve both observations and review scope and publication vintage before reconciliation. Some reported magnitudes already have simplified signs. Check the PDFs before claiming original sign preservation.

## Incremental backlog

Use the existing [Foundation milestone](https://github.com/geekswagg/kenya-finance-analysis/milestone/1). Keep the issue, verification results and source decisions together in each PR. Keep original Treasury PDFs outside Git while verifying document-specific redistribution terms.

| Order | Issue | Acceptance evidence |
| --- | --- | --- |
| 1 | [Source intake](https://github.com/geekswagg/kenya-finance-analysis/issues/1) | Confirm code and data licensing, register eleven official editions with checksums and URLs, and document attribution and PDF redistribution terms. |
| 2 | [Starter import](https://github.com/geekswagg/kenya-finance-analysis/issues/2) | Import the approved starter files with reproducible rebuild, reconcile schemas without losing statuses, and record source coverage by year, table and metric. |
| 3 | [Extraction](https://github.com/geekswagg/kenya-finance-analysis/issues/3) | Start with one historical debt-stock table, verify its cells visually, test the debt identity using source precision, then extend to the other reports. |
| 4 | [Data quality](https://github.com/geekswagg/kenya-finance-analysis/issues/4) | Check CSV/JSON parity, source integrity and accounting identities. Add a discrepancy comparison across metric aliases and publication statuses. Re-run Actions after the billing lock is resolved. |
| 5 | [Foundation release](https://github.com/geekswagg/kenya-finance-analysis/issues/5) | Verify DuckDB queries, document known discrepancies and gaps, and confirm release rights before tagging. |

Later work extends historical debt coverage, fiscal actuals and macro indicators. ASP.NET Core and Blazor are scheduled after the data foundation.
