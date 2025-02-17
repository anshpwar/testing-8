import unittest
from types import SimpleNamespace as L

from erpkit import rules, valuation


def lot(qty, cost, day, id_=0):
    return L(qty=qty, unit_cost_cents=cost, received_day=day, id=id_)


class ValuationTests(unittest.TestCase):
    LOTS = [lot(10, 100, 5, 1), lot(10, 120, 1, 2), lot(5, 200, 9, 3)]

    def test_fifo_issues_oldest_first(self):
        total, taken = valuation.fifo_issue(self.LOTS, 12)
        self.assertEqual(total, 10 * 120 + 2 * 100)
        self.assertEqual([(l.id, n) for l, n in taken], [(2, 10), (1, 2)])

    def test_issue_more_than_on_hand_raises(self):
        with self.assertRaises(valuation.InsufficientStock):
            valuation.fifo_issue(self.LOTS, 26)

    def test_exact_issue_empties_stock(self):
        total, taken = valuation.fifo_issue(self.LOTS, 25)
        self.assertEqual(total, valuation.stock_value(self.LOTS))
        self.assertEqual(sum(n for _, n in taken), 25)

    def test_average_cost_is_rounded_by_policy(self):
        raw = valuation.stock_value(self.LOTS) // valuation.on_hand(self.LOTS)
        self.assertEqual(valuation.average_unit_cost(self.LOTS), valuation.round_cost(raw))
        self.assertEqual(valuation.average_unit_cost([]), 0)

    def test_round_cost_uses_policy_unit(self):
        unit = max(1, rules.rounding_unit(1234))
        self.assertEqual(valuation.round_cost(1234) % unit, 0)
