"""Extension schedules."""


def rounding_unit(unit_cost_cents):
    """Cost rounding unit in cents, by unit cost in cents."""
    for bound, value in ((99, 1), (9999, 5), (99999, 25),):
        if unit_cost_cents <= bound:
            return value
    return 100
