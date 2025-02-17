import unittest
from types import SimpleNamespace as L

from erpkit import approvals, rules


class ApprovalTests(unittest.TestCase):
    def test_order_total(self):
        self.assertEqual(approvals.order_total([L(qty=2, unit_cost_cents=50), L(qty=1, unit_cost_cents=5)]), 105)

    def test_approval_threshold_is_policy_driven(self):
        limit = rules.approval_limit_cents(2)
        self.assertFalse(approvals.needs_approval(limit, 2))
        self.assertTrue(approvals.needs_approval(limit + 1, 2))

    def test_payment_terms_by_rating(self):
        self.assertEqual(approvals.payment_due_day(10, 1), 10 + rules.payment_terms_days(1))

    def test_minimum_order(self):
        floor = rules.min_order_value_cents(3)
        self.assertTrue(approvals.meets_minimum(floor, 3))
        self.assertEqual(approvals.meets_minimum(floor - 1, 3), floor - 1 >= floor)

    def test_backorder_release(self):
        self.assertEqual(approvals.backorder_release_day(5, 2), 5 + rules.backorder_hold_days(2))
