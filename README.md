# Kenya Finance Analysis

An open-source project to make Kenya's public finance and economic data traceable and queryable.

The first release targets FY 2021/22 through FY 2026/27. The foundational dataset and the intended set of 11 National Treasury documents are pending intake. No financial observations are published yet.

## Repository structure

| Path | Purpose |
| --- | --- |
| `data/` | Source inventory, reviewed observations and discrepancy records |
| `pipeline/` | Python extraction, transformation and validation |
| `docs/` | Methodology and release criteria |

Reviewed data will be available as CSV and JSON, with DuckDB for analytical queries. An ASP.NET Core API and a Blazor dashboard follow the data foundation.

See [Contributing](CONTRIBUTING.md) and the [v0.1.0 release criteria](docs/v0.1.0.md).
