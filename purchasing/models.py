from django.db import models

from inventory.models import Item


class Supplier(models.Model):
    code = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=120)
    rating = models.PositiveSmallIntegerField(default=2)

    class Meta:
        db_table = "pur_supplier"
        ordering = ["code"]

    def __str__(self):
        return self.code


class PurchaseOrder(models.Model):
    ref = models.CharField(max_length=16, unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name="orders")
    status = models.CharField(max_length=12, default="draft")
    ordered_day = models.IntegerField()
    approver_grade = models.PositiveSmallIntegerField(default=1)

    class Meta:
        db_table = "pur_order"
        ordering = ["ref"]


class POLine(models.Model):
    order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name="lines")
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    qty = models.IntegerField()
    unit_cost_cents = models.IntegerField()

    class Meta:
        db_table = "pur_line"
