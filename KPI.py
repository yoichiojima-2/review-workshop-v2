import pandas as pd
import datetime
import logging
import argparse
import json

customer_file = 'data/customer_data.csv'
purchase_file = 'data/purchase_data.csv'
sales_file = 'data/sales_data.csv'
start_date_str = '2025-01-01'
end_date_str = '2025-12-31'

start_date = pd.to_datetime(start_date_str).date() if start_date_str else None
end_date = pd.to_datetime(end_date_str).date() if end_date_str else None

try:
    customer_df = pd.read_csv(customer_file)
    print(f"'{customer_file}' を読み込みました。")
except FileNotFoundError:
    print(f"エラー: ファイル '{customer_file}' が見つかりません。")
    customer_df = None
except Exception as e:
    print(f"エラー: '{customer_file}' の読み込み中に予期しないエラーが発生しました: {e}")
    customer_df = None

try:
    purchase_df = pd.read_csv(purchase_file)
    print(f"'{purchase_file}' を読み込みました。")
except FileNotFoundError:
    print(f"エラー: ファイル '{purchase_file}' が見つかりません。")
    purchase_df = None
except Exception as e:
    printr(f"エラー: '{purchase_file}' の読み込み中に予期しないエラーが発生しました: {e}")
    purchase_df = None

try:
    sales_df = pd.read_csv(sales_file)
    print(f"'{sales_file}' を読み込みました。")
except FileNotFoundError:
    print(f"エラー: ファイル '{sales_file}' が見つかりません。")
    sales_df = None
except Exception as e:
    print(f"エラー: '{sales_file}' の読み込み中に予期しないエラーが発生しました: {e}")
    sales_df = None

sales_kpis = {}
if sales_df is not None and not sales_df.empty:
    print("売上KPIを算出します。")
    df_sales = sales_df.copy()

    if 'sales_date' in df_sales.columns:
        df_sales['sales_date'] = pd.to_datetime(df_sales['sales_date']).dt.date
        if start_date:
            df_sales = df_sales[df_sales['sales_date'] >= start_date]
        if end_date:
            df_sales = df_sales[df_sales['sales_date'] <= end_date]

        total_revenue = df_sales['total_amount'].sum()
        daily_revenue = df_sales.groupby('sales_date')['total_amount'].sum().to_dict()

        member_sales = df_sales[df_sales['customer_id'].notna()]['total_amount'].sum()

        sales_kpis = {
            "total_revenue": total_revenue,
            "daily_revenue": daily_revenue,
            "member_sales": member_sales,
        }
    else:
        print("売上データに 'sales_date' 列が存在しません。")
else:
    print("売上データが空です。売上KPIの算出をスキップします。")

customer_kpis = {}
if customer_df is not None and not customer_df.empty and sales_df is not None and not sales_df.empty and 'customer_id' in sales_df.columns and 'sales_date' in sales_df.columns:
    print("顧客KPIを算出します。")
    df_sales_customer = sales_df.copy()
    df_sales_customer['sales_date'] = pd.to_datetime(df_sales_customer['sales_date']).dt.date
    if start_date:
        df_sales_customer = df_sales_customer[df_sales_customer['sales_date'] >= start_date]
    if end_date:
        df_sales_customer = df_sales_customer[df_sales_customer['sales_date'] <= end_date]

    repeat_customers = df_sales_customer.groupby('customer_id')['sales_date'].nunique()[df_sales_customer.groupby('customer_id')['sales_date'].nunique() > 1].count() if not df_sales_customer.empty else 0
    average_purchase_frequency = df_sales_customer.groupby('customer_id')['sales_date'].nunique().mean() if not df_sales_customer.empty and df_sales_customer['customer_id'].nunique() > 0 else 0

    customer_kpis = {
        "repeat_customers": repeat_customers,
        "average_purchase_frequency": average_purchase_frequency
    }
else:
    print("顧客データまたは売上データが不十分なため、顧客KPIの算出をスキップします。")

purchase_kpis = {}
if purchase_df is not None and not purchase_df.empty:
    print("仕入れKPIを算出します。")
    df_purchase = purchase_df.copy()

    if 'purchase_date' in df_purchase.columns:
        df_purchase['purchase_date'] = pd.to_datetime(df_purchase['purchase_date']).dt.date
        if start_date:
            df_purchase = df_purchase[df_purchase['purchase_date'] >= start_date]
        if end_date:
            df_purchase = df_purchase[df_purchase['purchase_date'] <= end_date]

        total_purchase_amount = (df_purchase['quantity'] * df_purchase['unit_price']).sum()
        product_purchase_amount = df_purchase.groupby('item_name')[['quantity', 'unit_price']].apply(lambda x: (x['quantity'] * x['unit_price']).sum()).sort_values(ascending=False).to_dict()

        purchase_kpis = {
            "total_purchase_amount": total_purchase_amount,
            "product_purchase_amount": product_purchase_amount,
        }
    else:
        print("仕入れデータに 'purchase_date' 列が存在しません。")
else:
    print("仕入れデータが空です。仕入れKPIの算出をスキップします。")

results = {
    "sales_kpis": sales_kpis,
    "customer_kpis": customer_kpis,
    "purchase_kpis": purchase_kpis
}

print("\n--- 分析結果 ---")
print(json.dumps(results, indent=4, ensure_ascii=False))
print("データ分析を完了しました。")
