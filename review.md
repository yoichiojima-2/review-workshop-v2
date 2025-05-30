## 最小限レビュー
### 直さないと動かない

1. ミスタイプ: `printr()`

2. `pd.DataFrame.sort()`の第一引数がない
    - 最終データは`dict`
    - `dict`に順番はないので, `sort()`は不要

3. `print(json.dumps(results, indent=4, ensure_ascii=False))`にて、datetime.dateをパースできない
    - date型を事前に文字列に変換する
    - (`dict`を綺麗に標準出力したいだけなら`pprint(results)`でいいかも)


### 仕様を満たしていない

1. パラメータの渡し方

    "設定ファイルやコマンドライン引数で、ファイルパスや集計期間などを指定できるようにする"
    
    -> parametersタグを付与する

2. エラー処理

    "エラー処理を適切に行い、予期しないエラーでスクリプトが停止しないようにする"

    読み込み部分ではエラーハンドリングしているが、他の箇所でエラーが起きたらスクリプトは停止する

    -> 読み込み以外の箇所にもエラー処理を追加する

3. 日付の処理

    "日付データの処理には datetime モジュールを利用する"

    -> 明記されているので`pd.to_datetime`を使わず`datetime.strptime()`を使った方が良さそう



## 締め切りに余裕があれば直したい

1. 使わないライブラリはimportしない

2. 長すぎるワンライナーを読みやすくしたい

3. 結果出力部分のprint("\n--分析結果--")の改行は不要

4. 結果出力部分の数値がnp.floatで表示されるので`int` / `float`などのネイティブの型に変換する



[補足]

1, 2はコミット前に静的解析ツール / フォーマッターを使うフローにすると悩まない

以下のようなbashスクリプトを持っておいて、コミット前に実行するようにする運用にする?

```sh
#!/bin/bash

# importの並び替えと未使用ライブラリの削除
ruff isort . 

# 文法エラーチェック
ruff check --fix .

# フォーマット
ruff format .
```


## さらに余裕があれば

1. 変数名の改善
    
    sales_dfをディープコピーしたものがdf_salesになる (...etc)

    とりあえず動くものの, 一見違いがわかりづらく以後のメンテで嵌りそう

2. DRYにしたい

    似たコードが繰り返し使用されているので、共通処理は関数化してDRY(don't repeat yourself)にしたい

    - 読み込み & エラー処理
    - 日付型変換 -> 日付でフィルター

3. ネストを浅くしたい

    ifのネストが読みづらい. 

    -> 1.ifのネストが目的の達成に必要なら関数化して責任分離 / ネスト不要なら消す

        今回のロジック(売上の例):
        1. `sales_df`が`None`でなくかつ空でなければ、`df_sales`にコピーする. なければ処理をスキップ
        2. `df_sales`に`sales_date`カラムがあれば、集計する. なければ処理をスキップ

    今回のケースは1, 2を分ける必要がないので、後者が良さそう

4. 手続型の処理を関数化して責任分離したい

    責任分離/関数化のメリット
    - ユニットテストができる
    - エラー処理もシンプルに書ける
        - try-exceptを書いて回るしかない
    - 意味のまとまりができる
    - 複数人で改修しやすい

    責任分離/関数化のデメリット
    - 構造化することで逆にメンバーが読みづらいと感じることもある. セオリーにとらわれず柔軟性と匙加減を考えることは重要?
