import unittest

from erpkit import calc


class CalcTests(unittest.TestCase):
    def test_combined_charge(self):
        self.assertEqual(calc.combined_charge(0), 510)
        self.assertEqual(calc.combined_charge(1), 510)
        self.assertEqual(calc.combined_charge(5), 510)
        self.assertEqual(calc.combined_charge(6), 550)
