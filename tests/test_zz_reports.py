import json

from django.test import TestCase

from erpkit import aging, valuation

from .factories import make_item, make_lot, make_warehouse


class ReportEndpointTests(TestCase):
    def setUp(self):
        self.item, wh = make_item(), make_warehouse()
        make_lot(self.item, wh, 10, 100, day=0)
        make_lot(self.item, wh, 5, 200, day=90)

    def test_valuation_matches_the_library(self):
        data = json.loads(self.client.get("/inventory/valuation/").content)
        row = data["items"][0]
        lots = list(self.item.lots.all())
        self.assertEqual(row["on_hand"], 15)
        self.assertEqual(row["value_cents"], 10 * 100 + 5 * 200)
        self.assertEqual(row["avg_unit_cost_cents"], valuation.average_unit_cost(lots))

    def test_aging_endpoint(self):
        data = json.loads(self.client.get("/inventory/aging/?today=120").content)
        self.assertEqual(data["buckets"], aging.aging_report(list(self.item.lots.all()), 120))
        self.assertEqual(self.client.get("/inventory/aging/").status_code, 400)
