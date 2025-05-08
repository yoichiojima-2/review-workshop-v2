# 設計書

## 概要
飲食店の運営に関する会員顧客データ、仕入れデータ、売上データを読み込み、指定された期間における主要なKPI（Key Performance Indicators）を算出することを目的とする。これにより、店舗の概要を把握し、収益向上に向けた戦略立案の基礎情報を得る。

## 機能要件
- データ読み込み:customer_data.csv、purchase_data.csv、sales_data.csv を読み込む。
- ファイルが存在しない場合、エラー処理を行う。
- 期間指定: 集計対象の期間（開始日、終了日）を指定できるようにする。
- データクリーニングと変換:日付データを適切な型 (datetime オブジェクト) に変換する。
- 数値データ（数量、単価、割引率など）を適切な型 (float または int) に変換する。
- 必要に応じて、欠損値の処理（例：会員IDがNULLの場合は非会員として扱う）を行う。
- KPI算出: 以下のKPIを算出する。
- 売上関連
    - 総売上高
    - 商品別売上高
    - 会員売上高
- 顧客関連
    - リピート会員数
    - 平均購入頻度
- 仕入れ関連
    - 総仕入金額
    - サプライヤー別仕入れ金額

- 結果出力: 算出されたKPIを最後尾のセルで出力する。
- 進捗出力: 処理の開始、終了、エラー発生などの重要な情報を表示する。

## データ形式

### 仕入れデータ (purchase_data.csv)

| 項目名         | 型    | 説明                           |
| -------------- | ----- | ------------------------------ |
| purchase_id    | INT   | 仕入れID (一意の識別子)        |
| purchase_date  | TEXT  | 仕入れ日 (YYYY-MM-DD 形式)     |
| item_id        | INT   | 商品ID                         |
| item_name      | TEXT  | 商品名                         |
| quantity       | INT   | 仕入れ数量                     |
| unit_price     | REAL  | 仕入れ単価 (税抜)              |
| supplier_id    | INT   | サプライヤーID                 |
| supplier_name  | TEXT  | サプライヤー名                 |


### 売上データ (sales_data.csv)

| 項目名         | 型    | 説明                                 |
| -------------- | ----- | ------------------------------------ |
| sales_id       | INT   | 売上ID (一意の識別子)                |
| sales_date     | TEXT  | 売上日 (YYYY-MM-DD 形式)             |
| order_id       | INT   | 注文ID                               |
| customer_id    | INT   | 会員顧客ID (非会員の場合はNULL)       |
| item_id        | INT   | 販売商品ID                           |
| item_name      | TEXT  | 販売商品名                           |
| quantity       | INT   | 販売数量                             |
| unit_price     | REAL  | 販売単価 (税抜)                      |
| discount_rate  | REAL  | 割引率 (0〜1 の範囲)                 |
| total_amount   | REAL  | 合計金額 (税込)                      |


### 会員顧客データ (customer_data.csv)

| 項目名             | 型    | 説明                                   |
| ------------------ | ----- | -------------------------------------- |
| customer_id        | INT   | 会員ID (一意の識別子)                  |
| registration_date  | TEXT  | 会員登録日 (YYYY-MM-DD 形式)           |
| gender             | TEXT  | 性別 (例: Male, Female, Other, NULL)   |
| age                | INT   | 年齢                                   |
| birth_date         | TEXT  | 生年月日 (YYYY-MM-DD 形式、NULLの場合あり) |
| sales_date         | TEXT  | 購入日 (YYYY-MM-DD 形式)               |


## 実装に関する考慮事項
- データの読み込みには pandas ライブラリの利用を推奨する。
- 日付データの処理には datetime モジュールを利用する。
- 集計処理には pandas のgroupbyや集計関数を効果的に利用する。
- エラー処理を適切に行い、予期しないエラーでスクリプトが停止しないようにする。
- 設定ファイルやコマンドライン引数で、ファイルパスや集計期間などを指定できるようにする。