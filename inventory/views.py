from django.http import JsonResponse
from django.views.decorators.http import require_GET

from erpkit import aging, valuation

from .models import Item, Lot


@require_GET
def valuation_report(request):
    rows = []
    for item in Item.objects.all():
        lots = list(Lot.objects.filter(item=item, qty__gt=0))
        rows.append({"sku": item.sku, "on_hand": valuation.on_hand(lots), "value_cents": valuation.stock_value(lots),
                     "avg_unit_cost_cents": valuation.average_unit_cost(lots)})
    return JsonResponse({"items": rows})


@require_GET
def aging_report(request):
    try:
        today = int(request.GET["today"])
    except (KeyError, ValueError):
        return JsonResponse({"error": "today is required"}, status=400)
    lots = list(Lot.objects.filter(qty__gt=0))
    return JsonResponse({"today": today, "buckets": aging.aging_report(lots, today)})
