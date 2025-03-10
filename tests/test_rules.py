import unittest

from erpkit import rules


class RuleTests(unittest.TestCase):
    def test_reorder_multiple(self):
        self.assertEqual(rules.reorder_multiple(0), 10)
        self.assertEqual(rules.reorder_multiple(1), 10)
        self.assertEqual(rules.reorder_multiple(5), 10)
        self.assertEqual(rules.reorder_multiple(6), 50)
        self.assertEqual(rules.reorder_multiple(50), 50)
        self.assertEqual(rules.reorder_multiple(51), 250)
        self.assertEqual(rules.reorder_multiple(500), 250)
        self.assertEqual(rules.reorder_multiple(501), 1000)

    def test_receiving_tolerance_bp(self):
        self.assertEqual(rules.receiving_tolerance_bp(0), 500)
        self.assertEqual(rules.receiving_tolerance_bp(1), 500)
        self.assertEqual(rules.receiving_tolerance_bp(100000), 500)
        self.assertEqual(rules.receiving_tolerance_bp(100001), 300)
        self.assertEqual(rules.receiving_tolerance_bp(1000000), 300)
        self.assertEqual(rules.receiving_tolerance_bp(1000001), 150)
        self.assertEqual(rules.receiving_tolerance_bp(10000000), 150)
        self.assertEqual(rules.receiving_tolerance_bp(10000001), 50)

    def test_aging_bucket_days(self):
        self.assertEqual(rules.aging_bucket_days(0), 30)
        self.assertEqual(rules.aging_bucket_days(1), 30)
        self.assertEqual(rules.aging_bucket_days(30), 30)
        self.assertEqual(rules.aging_bucket_days(31), 60)
        self.assertEqual(rules.aging_bucket_days(60), 60)
        self.assertEqual(rules.aging_bucket_days(61), 90)
        self.assertEqual(rules.aging_bucket_days(90), 90)
        self.assertEqual(rules.aging_bucket_days(91), 180)

    def test_safety_stock_days(self):
        self.assertEqual(rules.safety_stock_days(0), 3)
        self.assertEqual(rules.safety_stock_days(1), 3)
        self.assertEqual(rules.safety_stock_days(7), 3)
        self.assertEqual(rules.safety_stock_days(8), 7)
        self.assertEqual(rules.safety_stock_days(21), 7)
        self.assertEqual(rules.safety_stock_days(22), 14)
        self.assertEqual(rules.safety_stock_days(60), 14)
        self.assertEqual(rules.safety_stock_days(61), 30)

    def test_cycle_count_interval_days(self):
        self.assertEqual(rules.cycle_count_interval_days(0), 27)
        self.assertEqual(rules.cycle_count_interval_days(1), 27)
        self.assertEqual(rules.cycle_count_interval_days(2), 79)
        self.assertEqual(rules.cycle_count_interval_days(3), 158)
        self.assertEqual(rules.cycle_count_interval_days(4), 320)

    def test_approval_limit_cents(self):
        self.assertEqual(rules.approval_limit_cents(0), 50000)
        self.assertEqual(rules.approval_limit_cents(1), 50000)
        self.assertEqual(rules.approval_limit_cents(2), 500000)
        self.assertEqual(rules.approval_limit_cents(3), 5000000)
        self.assertEqual(rules.approval_limit_cents(4), 50000000)

    def test_payment_terms_days(self):
        self.assertEqual(rules.payment_terms_days(0), 60)
        self.assertEqual(rules.payment_terms_days(1), 60)
        self.assertEqual(rules.payment_terms_days(2), 45)
        self.assertEqual(rules.payment_terms_days(3), 30)
        self.assertEqual(rules.payment_terms_days(4), 15)

    def test_write_off_limit_cents(self):
        self.assertEqual(rules.write_off_limit_cents(0), 500)
        self.assertEqual(rules.write_off_limit_cents(1), 500)
        self.assertEqual(rules.write_off_limit_cents(10000), 500)
        self.assertEqual(rules.write_off_limit_cents(10001), 2500)
        self.assertEqual(rules.write_off_limit_cents(100000), 2500)
        self.assertEqual(rules.write_off_limit_cents(100001), 10000)
        self.assertEqual(rules.write_off_limit_cents(1000000), 10000)
        self.assertEqual(rules.write_off_limit_cents(1000001), 50000)

    def test_min_order_value_cents(self):
        self.assertEqual(rules.min_order_value_cents(0), 0)
        self.assertEqual(rules.min_order_value_cents(1), 0)
        self.assertEqual(rules.min_order_value_cents(2), 25000)
        self.assertEqual(rules.min_order_value_cents(3), 100000)
        self.assertEqual(rules.min_order_value_cents(4), 500000)

    def test_lot_expiry_warning_days(self):
        self.assertEqual(rules.lot_expiry_warning_days(0), 7)
        self.assertEqual(rules.lot_expiry_warning_days(1), 7)
        self.assertEqual(rules.lot_expiry_warning_days(30), 7)
        self.assertEqual(rules.lot_expiry_warning_days(31), 30)
        self.assertEqual(rules.lot_expiry_warning_days(180), 30)
        self.assertEqual(rules.lot_expiry_warning_days(181), 90)
        self.assertEqual(rules.lot_expiry_warning_days(720), 90)
        self.assertEqual(rules.lot_expiry_warning_days(721), 180)

    def test_transfer_lead_days(self):
        self.assertEqual(rules.transfer_lead_days(0), 1)
        self.assertEqual(rules.transfer_lead_days(1), 1)
        self.assertEqual(rules.transfer_lead_days(100), 1)
        self.assertEqual(rules.transfer_lead_days(101), 3)
        self.assertEqual(rules.transfer_lead_days(1000), 3)
        self.assertEqual(rules.transfer_lead_days(1001), 10)
        self.assertEqual(rules.transfer_lead_days(5000), 10)
        self.assertEqual(rules.transfer_lead_days(5001), 21)

    def test_rounding_unit(self):
        self.assertEqual(rules.rounding_unit(0), 1)
        self.assertEqual(rules.rounding_unit(1), 1)
        self.assertEqual(rules.rounding_unit(99), 1)
        self.assertEqual(rules.rounding_unit(100), 5)
        self.assertEqual(rules.rounding_unit(9999), 5)
        self.assertEqual(rules.rounding_unit(10000), 25)
        self.assertEqual(rules.rounding_unit(99999), 25)
        self.assertEqual(rules.rounding_unit(100000), 100)

    def test_freight_surcharge_bp(self):
        self.assertEqual(rules.freight_surcharge_bp(0), 0)
        self.assertEqual(rules.freight_surcharge_bp(1), 0)
        self.assertEqual(rules.freight_surcharge_bp(50), 0)
        self.assertEqual(rules.freight_surcharge_bp(51), 250)
        self.assertEqual(rules.freight_surcharge_bp(500), 250)
        self.assertEqual(rules.freight_surcharge_bp(501), 600)
        self.assertEqual(rules.freight_surcharge_bp(5000), 600)
        self.assertEqual(rules.freight_surcharge_bp(5001), 1000)

    def test_backorder_hold_days(self):
        self.assertEqual(rules.backorder_hold_days(0), 2)
        self.assertEqual(rules.backorder_hold_days(1), 2)
        self.assertEqual(rules.backorder_hold_days(2), 7)
        self.assertEqual(rules.backorder_hold_days(3), 14)
        self.assertEqual(rules.backorder_hold_days(4), 30)

    def test_audit_sample_size(self):
        self.assertEqual(rules.audit_sample_size(0), 5)
        self.assertEqual(rules.audit_sample_size(1), 5)
        self.assertEqual(rules.audit_sample_size(20), 5)
        self.assertEqual(rules.audit_sample_size(21), 15)
        self.assertEqual(rules.audit_sample_size(200), 15)
        self.assertEqual(rules.audit_sample_size(201), 40)
        self.assertEqual(rules.audit_sample_size(2000), 40)
        self.assertEqual(rules.audit_sample_size(2001), 100)

    def test_depreciation_months(self):
        self.assertEqual(rules.depreciation_months(0), 11)
        self.assertEqual(rules.depreciation_months(1), 11)
        self.assertEqual(rules.depreciation_months(100000), 11)
        self.assertEqual(rules.depreciation_months(100001), 32)
        self.assertEqual(rules.depreciation_months(1000000), 32)
        self.assertEqual(rules.depreciation_months(1000001), 53)
        self.assertEqual(rules.depreciation_months(10000000), 53)
        self.assertEqual(rules.depreciation_months(10000001), 105)
