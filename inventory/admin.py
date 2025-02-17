from django.contrib import admin

from .models import Item, Lot, Warehouse

admin.site.register(Item)
admin.site.register(Warehouse)


@admin.register(Lot)
class LotAdmin(admin.ModelAdmin):
    list_display = ("item", "warehouse", "qty", "unit_cost_cents", "received_day")
