import unittest
from types import SimpleNamespace as L

from erpkit import aging, rules


class AgingTests(unittest.TestCase):
    def test_bucket_edges_follow_policy(self):
        first = rules.aging_bucket_days(0)
        self.assertEqual(aging.bucket_for(0), f"0-{first}")
        self.assertEqual(aging.bucket_for(first), f"0-{first}")
        self.assertNotEqual(aging.bucket_for(first + 1), f"0-{first}")

    def test_old_lots_land_in_the_open_ended_bucket(self):
        self.assertTrue(aging.bucket_for(10 ** 6).endswith("+"))

    def test_report_totals_quantities(self):
        lots = [L(qty=4, received_day=0), L(qty=6, received_day=0), L(qty=1, received_day=10 ** 5)]
        report = aging.aging_report(lots, today=10 ** 5)
        self.assertEqual(sum(report.values()), 11)

    def test_expiring_window_uses_shelf_life_policy(self):
        horizon = rules.lot_expiry_warning_days(90)
        lots = [L(expires_day=100 + horizon), L(expires_day=100 + horizon + 1), L(expires_day=99), L(expires_day=None)]
        got = aging.expiring(lots, today=100, shelf_life_days=90)
        self.assertEqual([l.expires_day for l in got], [100 + horizon])
