from django.test import TestCase

from stockmoves.models import StockMove


class StockMoveModelTests(TestCase):
    def test_defaults(self):
        obj = StockMove.objects.create(ref="SM-100", amount_cents=500)
        self.assertEqual(obj.status, "open")
        self.assertEqual(str(obj), "SM-100")

    def test_ref_is_unique(self):
        StockMove.objects.create(ref="SM-101", amount_cents=1)
        with self.assertRaises(Exception):
            StockMove.objects.create(ref="SM-101", amount_cents=2)
