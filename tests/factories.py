from inventory.models import Item, Lot, Warehouse
from purchasing.models import Supplier


def make_item(sku="BOLT-8", name="Bolt M8"):
    return Item.objects.create(sku=sku, name=name)


def make_warehouse(code="WH1"):
    return Warehouse.objects.create(code=code, name=f"Warehouse {code}")


def make_lot(item, wh, qty, cost, day, expires=None):
    return Lot.objects.create(item=item, warehouse=wh, qty=qty, unit_cost_cents=cost, received_day=day, expires_day=expires)


def make_supplier(code="ACME", rating=2):
    return Supplier.objects.create(code=code, name=f"{code} Ltd", rating=rating)
