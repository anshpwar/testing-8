import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from erpkit import approvals
from inventory.models import Item

from .models import POLine, PurchaseOrder, Supplier


def _payload(po):
    lines = list(po.lines.all())
    total = approvals.order_total(lines)
    return {"ref": po.ref, "status": po.status, "total_cents": total,
            "due_day": approvals.payment_due_day(po.ordered_day, po.supplier.rating),
            "needs_approval": approvals.needs_approval(total, po.approver_grade)}


@csrf_exempt
@require_POST
def create(request):
    try:
        body = json.loads(request.body)
        supplier = Supplier.objects.get(code=body["supplier"])
        lines = [(Item.objects.get(sku=l["sku"]), int(l["qty"]), int(l["unit_cost_cents"])) for l in body["lines"]]
    except (KeyError, ValueError, TypeError):
        return JsonResponse({"error": "bad_request"}, status=400)
    except (Supplier.DoesNotExist, Item.DoesNotExist):
        return JsonResponse({"error": "unknown_reference"}, status=404)
    total = sum(q * c for _, q, c in lines)
    if not approvals.meets_minimum(total, supplier.rating):
        return JsonResponse({"error": "below_minimum_order", "total_cents": total}, status=422)
    po = PurchaseOrder.objects.create(ref=f"PO-{PurchaseOrder.objects.count() + 1:05d}", supplier=supplier,
                                      ordered_day=int(body.get("day", 0)), approver_grade=int(body.get("grade", 1)))
    for item, qty, cost in lines:
        POLine.objects.create(order=po, item=item, qty=qty, unit_cost_cents=cost)
    return JsonResponse(_payload(po), status=201)


@require_GET
def detail(request, ref):
    try:
        return JsonResponse(_payload(PurchaseOrder.objects.select_related("supplier").get(ref=ref)))
    except PurchaseOrder.DoesNotExist:
        return JsonResponse({"error": "not_found"}, status=404)
