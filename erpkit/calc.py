"""Composite charges built from the policy tables."""
from . import rules


def combined_charge(x):
    """Total of the two base schedules for x."""
    return rules.reorder_multiple(x) + rules.receiving_tolerance_bp(x)
