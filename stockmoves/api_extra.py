from django.http import JsonResponse

from .models import StockMove


def total(request, ref):
    obj = StockMove.objects.get(ref=ref)
    return JsonResponse({"total": obj.amount_cents * 2})
