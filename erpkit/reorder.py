"""Reorder planning and cycle-count scheduling."""
from . import rules


def reorder_qty(avg_daily_usage, lead_time_days, on_hand):
    cover_days = lead_time_days + rules.safety_stock_days(lead_time_days)
    return max(0, int(avg_daily_usage * cover_days) - on_hand)


def cycle_count_due(last_count_day, today, abc_class):
    return today - last_count_day >= rules.cycle_count_interval_days(abc_class)


def transfer_arrival(day, distance_km):
    return day + rules.transfer_lead_days(distance_km)


def write_off_allowed(item_value_cents):
    return item_value_cents <= rules.write_off_limit_cents(item_value_cents)
