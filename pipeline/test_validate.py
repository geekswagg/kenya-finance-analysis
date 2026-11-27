import unittest

from validate import render_csv, validate_observations, validate_sources


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.source = dict(
            id="fixture", title="Fixture", edition="Final", published_on="2026-01-01",
            url="https://example.org/report", sha256="a" * 64,
            redistribution_status="link_only",
        )
        self.row = dict(
            source_id="fixture", fiscal_year="2025/26", series="example",
            reported_label="Example", status="actual", unit="KES",
            scale="1000000", value="0.00", missing_reason="", locator="page 2, table 1, row 4",
        )

    def test_zero_preserves_precision_and_locator(self):
        validate_observations([self.row], validate_sources([self.source]))
        self.assertIn('0.00,,"page 2, table 1, row 4"', render_csv([self.row]))

    def test_missing_requires_reason(self):
        row = self.row | {"value": ""}
        with self.assertRaisesRegex(ValueError, "missing reason"):
            validate_observations([row], {"fixture"})
        validate_observations([row | {"missing_reason": "Suppressed"}], {"fixture"})

    def test_rejects_unknown_source_and_duplicates(self):
        with self.assertRaisesRegex(ValueError, "unknown source"):
            validate_observations([self.row], set())
        with self.assertRaisesRegex(ValueError, "duplicate"):
            validate_observations([self.row, self.row], {"fixture"})

    def test_preserves_vintages(self):
        later = self.row | {"source_id": "later", "value": "2.00"}
        validate_observations([self.row, later], {"fixture", "later"})
