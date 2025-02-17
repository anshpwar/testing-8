"""Stock valuation over lot rows (anything with qty, unit_cost_cents, received_day)."""
from . import rules


class InsufficientStock(Exception):
    pass


def round_cost(cents):
    unit = max(1, rules.rounding_unit(cents))
    return (cents + unit // 2) // unit * unit


def on_hand(lots):
    return sum(l.qty for l in lots)


def fifo_issue(lots, qty):
    """Cost of issuing `qty` oldest-first. Returns (total_cents, [(lot, taken), ...])."""
    if qty > on_hand(lots):
        raise InsufficientStock(f"need {qty}, have {on_hand(lots)}")
    remaining, total, taken = qty, 0, []
    for lot in sorted(lots, key=lambda l: (l.received_day, getattr(l, "id", 0))):
        if remaining == 0:
            break
        use = min(lot.qty, remaining)
        total += use * lot.unit_cost_cents
        taken.append((lot, use))
        remaining -= use
    return total, taken


def average_unit_cost(lots):
    qty = on_hand(lots)
    if qty == 0:
        return 0
    return round_cost(sum(l.qty * l.unit_cost_cents for l in lots) // qty)


def stock_value(lots):
    return sum(l.qty * l.unit_cost_cents for l in lots)
