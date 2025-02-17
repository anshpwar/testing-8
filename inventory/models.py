from django.db import models


class Item(models.Model):
    sku = models.CharField(max_length=24, unique=True)
    name = models.CharField(max_length=120)
    uom = models.CharField(max_length=8, default="ea")

    class Meta:
        db_table = "inv_item"
        ordering = ["sku"]

    def __str__(self):
        return self.sku


class Warehouse(models.Model):
    code = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=80)

    class Meta:
        db_table = "inv_warehouse"
        ordering = ["code"]

    def __str__(self):
        return self.code


class Lot(models.Model):
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name="lots")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name="lots")
    qty = models.IntegerField()
    unit_cost_cents = models.IntegerField()
    received_day = models.IntegerField()
    expires_day = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = "inv_lot"
        ordering = ["item", "received_day", "id"]
