# Data intake

Place the foundational dataset and source copies in `data/incoming/` for review. The source register will record the title, official URL, edition, publication date, covered periods, SHA-256 and redistribution status for each of the 11 documents.

Published observations will preserve source locators, reported units and scale, fiscal period, status and publication vintage. Data corrections that differ from the source will have a documented discrepancy record.

## Machine-readable files

- `sources.json` identifies each document edition by a unique ID and checksum.
- `observations.json` is the curated input. Its CSV projection is `observations.csv`.
- `value` and `scale` are decimal strings. Multiply a reported value by its scale to express it in the base unit. Use a blank value and a source-backed `missing_reason` when a value is unavailable.
- `locator` identifies the precise page, table and line item as applicable. The source ID preserves publication vintage.

## Treasury starter

The 259 starter observations are derived from public reports issued by the [National Treasury of Kenya](https://www.treasury.go.ke/). Look up each source ID in the [source inventory](metadata/source-inventory.json) and use the printed source location in each row. The repository MIT license covers project code. The Treasury publications retain their original terms. The inventory includes the hashes of locally retained copies and lists the four reports awaiting extraction.

Use one format from `data/processed/`. The domain files are subsets of the master observations file. The root-level observation files belong to the bootstrap schema, which awaits reconciliation with the starter.
