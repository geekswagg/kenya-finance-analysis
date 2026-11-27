# Kenya Finance Analysis

An open-source project to make Kenya's public finance and economic data traceable and queryable.

The first release targets FY 2021/22 through FY 2026/27. The starter dataset and all 11 Treasury documents have been located and checked locally. The starter dataset is attributed to Kenya's National Treasury. The project code is MIT licensed. See the [M0 handover](docs/HANDOVER.md) for the baseline and issue sequence.

## Repository structure

| Path | Purpose |
| --- | --- |
| `data/` | Source inventory, reviewed observations and discrepancy records |
| `pipeline/` | Python extraction, transformation and validation |
| `docs/` | Methodology and release criteria |

Reviewed data will be available as CSV and JSON, with DuckDB for analytical queries. An ASP.NET Core API and a Blazor dashboard follow the data foundation.

See [Contributing](CONTRIBUTING.md) and the [v0.1.0 release criteria](docs/v0.1.0.md).

Rebuild the starter with `python scripts/build.py` and check it with `python scripts/validate.py`. See [data attribution and source handling](data/README.md).
