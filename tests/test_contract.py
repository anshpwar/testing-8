import unittest

from erpkit import contract


class ContractTests(unittest.TestCase):
    def test_build_summary(self):
        rec = contract.Record("SM-1", 1250, "open")
        self.assertEqual(
            contract.build_summary(rec),
            {"ref": "SM-1", "amount_cents": 1250, "state": "open", "currency": "USD"},
        )

    def test_describe(self):
        summary = {"ref": "SM-2", "status": "closed", "amount_cents": 99, "currency": "EUR"}
        self.assertEqual(contract.describe(summary), "SM-2 closed 99 EUR")
