"""
飲食店の運営に関する会員顧客データ, 仕入れデータ, 売上データを読み込み,
指定された期間における主要なKPI (Key Performance Indicators) を算出する
parameters:
    start_date_str (str): 開始日 (YYYY-MM-DD)
    end_date_str (str): 終了日 (YYYY-MM-DD)
"""

import pandas as pd
from datetime import datetime, date
from pprint import pprint

# parameters
start_date_str = "2025-01-01"
end_date_str = "2025-12-31"

# グローバル変数は大文字で定義する
PURCHASE_PATH = "data/purchase_data.csv"
SALES_PATH = "data/sales_data.csv"

START_DATE = datetime.strptime(start_date_str, "%Y-%m-%d").date() if start_date_str else None
END_DATE = datetime.strptime(end_date_str, "%Y-%m-%d").date() if end_date_str else None


def read_csv(path: str) -> pd.DataFrame | None:
    """
    csvファイルを読み込む. データが存在しない場合はNoneを返す
    args:
        path (str): csvファイルのパス
    returns:
        pd.DataFrame | None: 読み込んだDataFrameまたはNone
    """
    try:
        df = pd.read_csv(path)
        print(f"'{path}' を読み込みました。")
    except FileNotFoundError:
        print(f"エラー: ファイル '{path}' が見つかりません。")
        df = None
    except Exception as e:
        print(f"エラー: '{path}' の読み込み中に予期しないエラーが発生しました: {e}")
        df = None
    return df


def filter_by_date(df: pd.DataFrame, date_col: str, start_date: date | None, end_date: date | None) -> pd.DataFrame:
    """
    dataframeを日付で絞り込む
    args:
        df: pd.DataFrame
        date_col (str): 日付列の名前
        start_date (date | None): 開始日
        end_date (date | None): 終了日
    returns:
        pd.DataFrame: 日付で絞り込まれたDataFrame
    """
    df[date_col] = pd.to_datetime(df[date_col]).dt.date
    if start_date:
        df = df[df[date_col] >= start_date]
    if end_date:
        df = df[df[date_col] <= end_date]
    return df


def calc_sales_kpi(sales_df: pd.DataFrame) -> dict:
    """
    売上KPIを算出する
    - 総売上高
    - 商品別売上高
    - 日別売上高

    args:
        sales_df (pd.DataFrame): 売上データ
    returns:
        dict: 売上KPI
    """
    # [START: 入力バリデーション: 早く関数から返してネストを浅くする]
    if sales_df is None or sales_df.empty:
        print("売上データが空です。売上KPIの算出をスキップします。")
        return {}

    if "sales_date" not in sales_df.columns:
        print("売上データに 'sales_date' 列が存在しません。")
        return {}
    # [END: 入力バリデーション]

    try:
        print("売上KPIを算出します。")
        # 明確な変数名に
        df_filtered = filter_by_date(sales_df.copy(), "sales_date", START_DATE, END_DATE)

        # 総売上高を算出
        total_revenue = int(df_filtered["total_amount"].sum())

        # 商品別売上高を算出
        daily_revenue_df = df_filtered.groupby("sales_date")["total_amount"].sum().astype(int)
        daily_revenue_df.index = [i.strftime("%Y-%m-%d") for i in daily_revenue_df.index]
        daily_revenue = daily_revenue_df.to_dict()

        # 会員売上高を算出
        member_sales = int(df_filtered[df_filtered["customer_id"].notna()]["total_amount"].sum())

        return {
            "total_revenue": total_revenue,
            "daily_revenue": daily_revenue,
            "member_sales": member_sales,
        }
    except Exception as e:
        print(f"エラー: 売上KPIの算出中に予期しないエラーが発生しました: {e}")
        return {}


def calc_customer_kpis(sales_df: pd.DataFrame) -> dict:
    """
    顧客KPIを算出する
    - リピート会員数
    - 平均購入頻度

    args:
        sales_df (pd.DataFrame): 売上データ
    returns:
        dict: 顧客KPI
    """
    # [START: 入力バリデーション: 早く関数から返してネストを浅くする]
    if sales_df is None or sales_df.empty:
        print("売上データが空です。顧客KPIの算出をスキップします。")
        return {}

    if "customer_id" not in sales_df.columns or "sales_date" not in sales_df.columns:
        print("売上データに 'customer_id' または 'sales_date' 列が存在しません。")
        return {}
    # [END: 入力バリデーション]

    try:
        print("顧客KPIを算出します。")
        df_filtered = filter_by_date(sales_df.copy(), "sales_date", START_DATE, END_DATE)

        # リピート会員数を算出
        # if notとせずシンプルに
        if df_filtered.empty:
            repeat_customers = 0
        else:
            repeat_customers = int(
                df_filtered.groupby("customer_id")["sales_date"]
                .nunique()[df_filtered.groupby("customer_id")["sales_date"].nunique() > 1]
                .count()
            )

        # 平均購入頻度を算出
        # if notとせずシンプルに
        if df_filtered.empty or df_filtered["customer_id"].nunique() == 0:
            average_purchase_frequency = 0
        else:
            average_purchase_frequency = float(df_filtered.groupby("customer_id")["sales_date"].nunique().mean())

        return {
            "repeat_customers": repeat_customers,
            "average_purchase_frequency": average_purchase_frequency,
        }
    except Exception as e:
        print(f"エラー: 顧客KPIの算出中に予期しないエラーが発生しました: {e}")
        return {}


def calc_purchase_kpis(purchase_df: pd.DataFrame) -> dict:
    """
    仕入れKPIを算出する
    - 総仕入れ金額
    - 商品別仕入れ金額
    args:
        purchase_df (pd.DataFrame): 仕入れデータ
    returns:
        dict: 仕入れKPI
    """
    # [START: 入力バリデーション: 早く関数から返してネストを浅くする]
    if purchase_df is None or purchase_df.empty:
        print("仕入れデータが空です。仕入れKPIの算出をスキップします。")
        return {}

    if "purchase_date" not in purchase_df.columns:
        print("仕入れデータに 'purchase_date' 列が存在しません。")
        return {}
    # [END: 入力バリデーション]

    try:
        print("仕入れKPIを算出します。")
        df_filtered = filter_by_date(purchase_df.copy(), "purchase_date", START_DATE, END_DATE)

        # 総仕入れ金額を算出
        total_purchase_amount = int((df_filtered["quantity"] * df_filtered["unit_price"]).sum())

        # 商品別仕入れ金額を算出
        product_purchase_amount = (
            df_filtered.groupby("item_name")[["quantity", "unit_price"]]
            .apply(lambda x: (x["quantity"] * x["unit_price"]).sum())
            .astype(int)
            .to_dict()
        )

        return {
            "total_purchase_amount": total_purchase_amount,
            "product_purchase_amount": product_purchase_amount,
        }

    except Exception as e:
        print(f"エラー: 仕入れKPIの算出中に予期しないエラーが発生しました: {e}")
        return {}


def print_result(sales_kpis: dict, customer_kpis: dict, purchase_kpis: dict) -> None:
    """
    分析結果を出力する
    args:
        sales_kpis (dict): 売上KPI
        customer_kpis (dict): 顧客KPI
        purchase_kpis (dict): 仕入れKPI
    """
    try:
        results = {
            "sales_kpis": sales_kpis,
            "customer_kpis": customer_kpis,
            "purchase_kpis": purchase_kpis,
        }
        print("--- 分析結果 ---")
        pprint(results)
        print("データ分析を完了しました。")
    except Exception as e:
        print(f"エラー: 分析結果の出力中に予期しないエラーが発生しました: {e}")


def main():
    try:
        # データ読み込み
        purchase_df = read_csv(PURCHASE_PATH)
        sales_df = read_csv(SALES_PATH)

        # KPI算出
        sales_kpis = calc_sales_kpi(sales_df)
        customer_kpis = calc_customer_kpis(sales_df)
        purchase_kpis = calc_purchase_kpis(purchase_df)

        # 結果出力
        print_result(sales_kpis, customer_kpis, purchase_kpis)

    except Exception as e:
        print(f"エラー: メイン処理中に予期しないエラーが発生しました: {e}")


if __name__ == "__main__":
    main()
