from django.contrib import admin

from .models import POLine, PurchaseOrder, Supplier

admin.site.register(Supplier)


class POLineInline(admin.TabularInline):
    model = POLine
    extra = 0


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    inlines = [POLineInline]
