import pathlib
import tempfile
import unittest

from django.conf import settings

from erpkit import ratetable, rules


class RateTableTests(unittest.TestCase):
    def test_fixture_loads(self):
        table = ratetable.load(settings.RATE_TABLE)
        self.assertEqual(table["version"], 1)
        self.assertEqual(table["rates"]["EU"], 1900)
        self.assertEqual(len(table["rates"]), 6)

    def test_round_trip(self):
        blob = ratetable.dump({"AA": 5, "BB": 9}, flags=7)
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "t.bin"
            path.write_bytes(blob)
            table = ratetable.load(path)
        self.assertEqual((table["flags"], table["rates"]), (7, {"AA": 5, "BB": 9}))

    def test_rejects_damaged_tables(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "t.bin"
            for blob in (b"", b"XXXX" + bytes(8), ratetable.dump({"A": 1})[:-1]):
                path.write_bytes(blob)
                with self.assertRaises(ratetable.BadRateTable):
                    ratetable.load(path)

    def test_freight_adds_weight_surcharge(self):
        table = ratetable.load(settings.RATE_TABLE)
        self.assertEqual(ratetable.freight_bp(table, "EU", 100), 1900 + rules.freight_surcharge_bp(100))
        self.assertEqual(ratetable.freight_bp(table, "??", 100), rules.freight_surcharge_bp(100))
