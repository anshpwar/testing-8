import unittest

from erpkit import reorder, rules


class ReorderTests(unittest.TestCase):
    def test_reorder_qty_covers_lead_time_plus_safety(self):
        cover = 10 + rules.safety_stock_days(10)
        self.assertEqual(reorder.reorder_qty(3, 10, 5), max(0, 3 * cover - 5))

    def test_no_reorder_when_stocked(self):
        self.assertEqual(reorder.reorder_qty(1, 1, 10 ** 6), 0)

    def test_cycle_count_interval(self):
        gap = rules.cycle_count_interval_days(2)
        self.assertTrue(reorder.cycle_count_due(0, gap, 2))
        self.assertFalse(reorder.cycle_count_due(0, gap - 1, 2))

    def test_transfer_arrival(self):
        self.assertEqual(reorder.transfer_arrival(10, 800), 10 + rules.transfer_lead_days(800))

    def test_write_off_limit(self):
        self.assertEqual(reorder.write_off_allowed(10), 10 <= rules.write_off_limit_cents(10))
