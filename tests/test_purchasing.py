from django.test import TestCase

from purchasing.models import POLine, PurchaseOrder

from .factories import make_item, make_supplier


class PurchaseOrderTests(TestCase):
    def test_lines_cascade_with_order(self):
        sup, item = make_supplier(), make_item()
        po = PurchaseOrder.objects.create(ref="PO-1", supplier=sup, ordered_day=1)
        POLine.objects.create(order=po, item=item, qty=2, unit_cost_cents=10)
        po.delete()
        self.assertEqual(POLine.objects.count(), 0)

    def test_supplier_cannot_be_deleted_with_orders(self):
        sup = make_supplier()
        PurchaseOrder.objects.create(ref="PO-2", supplier=sup, ordered_day=1)
        with self.assertRaises(Exception):
            sup.delete()
