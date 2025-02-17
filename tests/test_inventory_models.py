from django.db import connection
from django.test import TestCase

from inventory.models import Lot

from .factories import make_item, make_lot, make_warehouse


class InventoryModelTests(TestCase):
    def test_lots_order_by_item_then_received_day(self):
        item, wh = make_item(), make_warehouse()
        make_lot(item, wh, 1, 10, day=9)
        make_lot(item, wh, 1, 10, day=2)
        self.assertEqual([l.received_day for l in Lot.objects.all()], [2, 9])

    def test_tables_come_from_the_sql_migration(self):
        names = set(connection.introspection.table_names())
        self.assertTrue({"inv_item", "inv_warehouse", "inv_lot", "pur_supplier", "pur_order", "pur_line"} <= names)

    def test_lot_index_exists(self):
        with connection.cursor() as cur:
            cur.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='inv_lot_item_received'")
            self.assertIsNotNone(cur.fetchone())

    def test_item_sku_unique(self):
        make_item("X1")
        with self.assertRaises(Exception):
            make_item("X1")
