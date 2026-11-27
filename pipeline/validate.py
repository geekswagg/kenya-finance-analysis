"""Validate reviewed data and check or regenerate its CSV projection."""

import argparse
import csv
from datetime import date
from decimal import Decimal
import io
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

DATA = Path(__file__).resolve().parents[1] / "data"
SOURCE_FIELDS = (
    "id", "title", "edition", "published_on", "url", "sha256",
    "redistribution_status",
)
FIELDS = (
    "source_id", "fiscal_year", "series", "reported_label", "status",
    "unit", "scale", "value", "missing_reason", "locator",
)
STATUSES = {"actual", "projection", "revised_estimate"}
DECIMAL = re.compile(r"[+-]?[0-9]+(?:\.[0-9]+)?")


def read_rows(path, fields):
    rows = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(rows, list):
        raise ValueError(f"{path.name} must contain an array")
    for index, row in enumerate(rows, 1):
        if not isinstance(row, dict) or row.keys() != set(fields):
            raise ValueError(f"{path.name} row {index} must have fields {fields}")
        for field, value in row.items():
            if not isinstance(value, str) or value != value.strip():
                raise ValueError(f"{path.name} row {index}: {field} must be a trimmed string")
    return rows


def validate_sources(rows):
    sources = set()
    for index, row in enumerate(rows, 1):
        source_id = row["id"]
        if not all(row.values()) or source_id in sources:
            raise ValueError(f"sources.json row {index}: blank field or duplicate ID")
        if not re.fullmatch(r"[0-9a-f]{64}", row["sha256"]):
            raise ValueError(f"sources.json row {index}: invalid SHA-256")
        if date.fromisoformat(row["published_on"]).isoformat() != row["published_on"]:
            raise ValueError(f"sources.json row {index}: use YYYY-MM-DD")
        url = urlsplit(row["url"])
        if url.scheme != "https" or not url.hostname or url.username or url.password:
            raise ValueError(f"sources.json row {index}: expected an HTTPS source URL without credentials")
        if row["redistribution_status"] not in {"unreviewed", "link_only", "permitted"}:
            raise ValueError(f"sources.json row {index}: invalid redistribution status")
        sources.add(source_id)
    return sources


def validate_observations(rows, sources):
    seen = set()
    for index, row in enumerate(rows, 1):
        context = f"observations.json row {index}"
        if any(not row[field] for field in FIELDS if field not in {"value", "missing_reason"}):
            raise ValueError(f"{context}: blank required field")
        if row["source_id"] not in sources:
            raise ValueError(f"{context}: unknown source")
        fiscal_year = re.fullmatch(r"(20[0-9]{2})/([0-9]{2})", row["fiscal_year"])
        if not fiscal_year or (int(fiscal_year[1]) + 1) % 100 != int(fiscal_year[2]):
            raise ValueError(f"{context}: invalid fiscal year, expected YYYY/YY")
        if row["status"] not in STATUSES:
            raise ValueError(f"{context}: invalid observation status")
        if not DECIMAL.fullmatch(row["scale"]) or Decimal(row["scale"]) <= 0:
            raise ValueError(f"{context}: scale must be a positive decimal")
        value = row["value"]
        if bool(value) == bool(row["missing_reason"]) or (value and not DECIMAL.fullmatch(value)):
            raise ValueError(f"{context}: provide a decimal value or a missing reason")
        key = tuple(row[field] for field in ("source_id", "locator", "fiscal_year", "series", "status"))
        if key in seen:
            raise ValueError(f"{context}: duplicate observation")
        seen.add(key)


def render_csv(rows):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=DATA)
    parser.add_argument("--write-csv", action="store_true")
    args = parser.parse_args()
    try:
        sources = validate_sources(read_rows(args.data_dir / "sources.json", SOURCE_FIELDS))
        rows = read_rows(args.data_dir / "observations.json", FIELDS)
        validate_observations(rows, sources)
        csv_path = args.data_dir / "observations.csv"
        expected = render_csv(rows)
        if args.write_csv:
            csv_path.write_text(expected, encoding="utf-8", newline="\n")
        elif csv_path.read_text(encoding="utf-8") != expected:
            raise ValueError("observations.csv differs from JSON. Regenerate with --write-csv.")
    except (OSError, ValueError) as error:
        parser.exit(1, f"Data validation failed: {error}\n")
    print(f"Validated {len(sources)} sources and {len(rows)} observations.")


if __name__ == "__main__":
    main()
