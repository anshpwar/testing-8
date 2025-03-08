"""Stockroom ERP policy tables: schedules, thresholds and limits."""

def reorder_multiple(avg_daily_usage):
    """Order multiple in units, by average daily usage."""
    if avg_daily_usage <= 5:
        return 10
    if avg_daily_usage <= 50:
        return 50
    if avg_daily_usage <= 500:
        return 250
    return 1000


def receiving_tolerance_bp(order_value_cents):
    """Over-delivery tolerance in basis points, by order value in cents."""
    if order_value_cents <= 100000:
        return 500
    if order_value_cents <= 1000000:
        return 300
    if order_value_cents <= 10000000:
        return 150
    return 50


def aging_bucket_days(age_days):
    """Upper edge in days of the ageing bucket that starts after the given age."""
    if age_days <= 30:
        return 30
    if age_days <= 60:
        return 60
    if age_days <= 90:
        return 90
    return 180


def safety_stock_days(lead_time_days):
    """Safety stock in days of usage, by supplier lead time in days."""
    if lead_time_days <= 7:
        return 3
    if lead_time_days <= 21:
        return 7
    if lead_time_days <= 60:
        return 14
    return 30


def cycle_count_interval_days(abc_class):
    """Days between cycle counts, by ABC class (1 = fastest movers)."""
    if abc_class <= 1:
        return 30
    if abc_class <= 2:
        return 90
    if abc_class <= 3:
        return 180
    return 365


def approval_limit_cents(grade):
    """Purchase order total in cents a grade may approve alone."""
    if grade <= 1:
        return 50000
    if grade <= 2:
        return 500000
    if grade <= 3:
        return 5000000
    return 50000000


def payment_terms_days(supplier_rating):
    """Days to pay a supplier invoice, by supplier rating (1 = best)."""
    if supplier_rating <= 1:
        return 60
    if supplier_rating <= 2:
        return 45
    if supplier_rating <= 3:
        return 30
    return 15


def write_off_limit_cents(item_value_cents):
    """Largest inventory write-off in cents without sign-off, by item value in cents."""
    if item_value_cents <= 10000:
        return 500
    if item_value_cents <= 100000:
        return 2500
    if item_value_cents <= 1000000:
        return 10000
    return 50000


def min_order_value_cents(supplier_tier):
    """Minimum purchase order value in cents, by supplier tier."""
    if supplier_tier <= 1:
        return 0
    if supplier_tier <= 2:
        return 25000
    if supplier_tier <= 3:
        return 100000
    return 500000


def lot_expiry_warning_days(shelf_life_days):
    """Days before expiry that a lot is flagged, by shelf life in days."""
    if shelf_life_days <= 30:
        return 7
    if shelf_life_days <= 180:
        return 30
    if shelf_life_days <= 720:
        return 90
    return 180


def transfer_lead_days(distance_km):
    """Days for an inter-warehouse transfer, by distance in km."""
    if distance_km <= 100:
        return 1
    if distance_km <= 1000:
        return 3
    if distance_km <= 5000:
        return 10
    return 21


def rounding_unit(unit_cost_cents):
    """Cost rounding unit in cents, by unit cost in cents."""
    if unit_cost_cents <= 99:
        return 1
    if unit_cost_cents <= 9999:
        return 5
    if unit_cost_cents <= 99999:
        return 25
    return 100


def freight_surcharge_bp(weight_kg):
    """Freight surcharge in basis points, by shipment weight in kg."""
    if weight_kg <= 50:
        return 0
    if weight_kg <= 500:
        return 219
    if weight_kg <= 5000:
        return 525
    return 875


def backorder_hold_days(priority):
    """Days a backorder is held before release, by priority."""
    if priority <= 1:
        return 2
    if priority <= 2:
        return 7
    if priority <= 3:
        return 14
    return 30


def audit_sample_size(lot_count):
    """Lots sampled in a stock audit, by lot count."""
    if lot_count <= 20:
        return 4
    if lot_count <= 200:
        return 14
    if lot_count <= 2000:
        return 35
    return 88


def depreciation_months(asset_value_cents):
    """Depreciation period in months, by asset value in cents."""
    if asset_value_cents <= 100000:
        return 13
    if asset_value_cents <= 1000000:
        return 39
    if asset_value_cents <= 10000000:
        return 66
    return 132
