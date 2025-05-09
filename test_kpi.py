"""KPI.pyのテストコード"""

import pandas as pd
from datetime import date
from KPI import (
    calc_sales_kpi,
    calc_customer_kpis,
    calc_purchase_kpis,
    filter_by_date,
)


def test_filter_by_date():
    df = pd.DataFrame({"date": pd.to_datetime(["2025-01-01", "2025-06-01", "2026-01-01"])})
    filtered = filter_by_date(df, "date", date(2025, 1, 1), date(2025, 12, 31))
    assert len(filtered) == 2


def test_calc_sales_kpi():
    df = pd.DataFrame(
        {
            "sales_date": ["2025-01-10", "2025-01-11"],
            "total_amount": [1000, 2000],
            "customer_id": [1, None],
        }
    )
    kpi = calc_sales_kpi(df)
    assert kpi["total_revenue"] == 3000
    assert "2025-01-10" in kpi["daily_revenue"]
    assert kpi["member_sales"] == 1000


def test_calc_customer_kpis():
    sales = pd.DataFrame(
        {
            "sales_date": ["2025-01-10", "2025-01-11", "2025-01-10"],
            "customer_id": [1, 1, 2],
        }
    )
    kpi = calc_customer_kpis(sales)
    assert kpi["repeat_customers"] == 1
    assert kpi["average_purchase_frequency"] > 0


def test_calc_purchase_kpis():
    df = pd.DataFrame(
        {
            "purchase_date": ["2025-01-01", "2025-01-02"],
            "item_name": ["A", "A"],
            "quantity": [10, 5],
            "unit_price": [100, 200],
        }
    )
    kpi = calc_purchase_kpis(df)
    assert kpi["total_purchase_amount"] == 10 * 100 + 5 * 200
    assert kpi["product_purchase_amount"]["A"] == 10 * 100 + 5 * 200
