import json

from django.test import TestCase

from erpkit import approvals, rules

from .factories import make_item, make_supplier


class PurchasingApiTests(TestCase):
    def setUp(self):
        make_item("BOLT-8")
        make_supplier("ACME", rating=2)

    def post(self, body):
        return self.client.post("/purchasing/", json.dumps(body), content_type="application/json")

    def order(self, qty, cost):
        return {"supplier": "ACME", "day": 10, "grade": 1, "lines": [{"sku": "BOLT-8", "qty": qty, "unit_cost_cents": cost}]}

    def test_create_and_read(self):
        total = 100 * 500
        if not approvals.meets_minimum(total, 2):
            self.skipTest("minimum order exceeds this fixture under the current policy tables")
        resp = self.post(self.order(100, 500))
        self.assertEqual(resp.status_code, 201)
        body = resp.json()
        self.assertEqual(body["total_cents"], total)
        self.assertEqual(body["due_day"], 10 + rules.payment_terms_days(2))
        self.assertEqual(body["needs_approval"], approvals.needs_approval(total, 1))
        self.assertEqual(self.client.get(f"/purchasing/{body['ref']}/").json()["total_cents"], total)

    def test_below_minimum_is_rejected(self):
        floor = rules.min_order_value_cents(2)
        if floor == 0:
            self.skipTest("no minimum order under the current policy tables")
        self.assertEqual(self.post(self.order(1, max(1, floor - 2))).status_code, 422)

    def test_bad_requests(self):
        self.assertEqual(self.post({}).status_code, 400)
        self.assertEqual(self.post({"supplier": "NOPE", "lines": []}).status_code, 404)
        self.assertEqual(self.client.get("/purchasing/missing/").status_code, 404)
