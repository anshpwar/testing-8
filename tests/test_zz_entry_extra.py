from django.test import TestCase

from stockmoves import api_extra
from stockmoves.models import StockMove


class ExtraApiTests(TestCase):
    def test_total(self):
        StockMove.objects.create(ref="SM-300", amount_cents=5)
        resp = api_extra.total(None, "SM-300")
        self.assertEqual(resp.status_code, 200)
