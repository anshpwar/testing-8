"""Lot ageing buckets and expiry warnings, driven by the policy tables."""
from . import rules


def bucket_for(age_days):
    """Label such as '0-30' for the bucket an age falls in; bucket edges come from aging_bucket_days."""
    edges = [0]
    probe = 0
    while True:
        edge = rules.aging_bucket_days(probe)
        if edge <= edges[-1] or len(edges) > 6:
            break
        edges.append(edge)
        probe = edge + 1
    for lo, hi in zip(edges, edges[1:]):
        if age_days <= hi:
            return f"{lo if lo == 0 else lo + 1}-{hi}"
    return f"{edges[-1] + 1}+"


def aging_report(lots, today):
    report = {}
    for lot in lots:
        label = bucket_for(max(0, today - lot.received_day))
        report[label] = report.get(label, 0) + lot.qty
    return report


def expiring(lots, today, shelf_life_days):
    horizon = rules.lot_expiry_warning_days(shelf_life_days)
    return [l for l in lots if l.expires_day is not None and 0 <= l.expires_day - today <= horizon]
