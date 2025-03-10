from django.http import Http404, JsonResponse

from .models import StockMove


def summary(request, ref):
    try:
        obj = StockMove.objects.get(ref=ref)
    except StockMove.DoesNotExist:
        raise Http404
    return JsonResponse({"ref": obj.ref, "amount_cents": obj.amount, "status": obj.status})
