"""Purchase approvals and payment terms."""
from . import rules


def order_total(lines):
    return sum(l.qty * l.unit_cost_cents for l in lines)


def needs_approval(total_cents, approver_grade):
    return total_cents > rules.approval_limit_cents(approver_grade)


def payment_due_day(ordered_day, supplier_rating):
    return ordered_day + rules.payment_terms_days(supplier_rating)


def meets_minimum(total_cents, supplier_tier):
    return total_cents >= rules.min_order_value_cents(supplier_tier)


def backorder_release_day(day, priority):
    return day + rules.backorder_hold_days(priority)
