## ruff 文法エラーチェック例

```sh
(.venv) ➜  review-workshop-v2 git:(main) ✗ ruff check KPI.py 
KPI.py:2:8: F401 [*] `datetime` imported but unused
  |
1 | import pandas as pd
2 | import datetime
  |        ^^^^^^^^ F401
3 | import logging
4 | import argparse
  |
  = help: Remove unused import: `datetime`

KPI.py:3:8: F401 [*] `logging` imported but unused
  |
1 | import pandas as pd
2 | import datetime
3 | import logging
  |        ^^^^^^^ F401
4 | import argparse
5 | import json
  |
  = help: Remove unused import: `logging`

KPI.py:4:8: F401 [*] `argparse` imported but unused
  |
2 | import datetime
3 | import logging
4 | import argparse
  |        ^^^^^^^^ F401
5 | import json
  |
  = help: Remove unused import: `argparse`

KPI.py:33:5: F821 Undefined name `printr`
   |
31 |     purchase_df = None
32 | except Exception as e:
33 |     printr(f"エラー: '{purchase_file}' の読み込み中に予期しないエラーが発生しました: {e}")
   |     ^^^^^^ F821
34 |     purchase_df = None
   |

Found 4 errors.
[*] 3 fixable with the `--fix` option.
```