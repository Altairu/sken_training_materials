# Python3講習　第4回目　エラーハンドリング

## 環境

* **Python バージョン**: 3.9, 3.10, 3.11
* **開発マシン**:

  * ThinkPad L380 (Ubuntu 22.04.3 LTS)
  * ThinkPad P1 Gen 3 (Windows 10)


## 1. はじめに

プログラムを実行する際、想定外の状況（ファイルが見つからない、ネットワーク切断、ゼロ除算など）に遭遇することがあります。これらの状況に対し適切に対処しないと、プログラムは予期せぬ終了（クラッシュ）を起こし、ユーザー体験やシステムの安定性に悪影響を及ぼします。

この回では、Python におけるエラー（エラーコード）と例外（Exceptions）の違いを理解し、組み込み例外の種類、`try`/`except` 構文の使い方、カスタム例外の定義、さらにはロギングやコンテキストマネージャと組み合わせた総合的なエラーハンドリング技術を解説します。


## 2. エラーと例外の概要

* **エラー (Error)**

  * 文法エラー（`SyntaxError`）: コードの書き間違いなどで、実行前に検出される。
  * システムエラー: OS 依存のエラー。Python レベルでは `OSError` や `IOError` にマッピングされる。

* **例外 (Exception)**

  * 実行時エラー: プログラム実行中に検出され、通常は `Exception` を継承したクラスとして表現される。
  * 例外は `raise` 文で意図的に発生させることも可能。

例外をキャッチし、適切に対処することで、プログラムの安定性と可観測性が向上します。


## 3. 組み込み例外の種類と階層

Python 標準ライブラリには多くの例外クラスが定義されています。主なものを以下に示します。

| 例外クラス                 | 説明                                   |
| -------------------------- | -------------------------------------- |
| `BaseException`            | 全例外の基底クラス                     |
| └─ `Exception`             | 通常の例外基底クラス                   |
| ├─ `ArithmeticError`       | 算術演算のエラー基底                   |
| │   ├─ `ZeroDivisionError` | ゼロ除算                               |
| │   ├─ `OverflowError`     | 算術演算でオーバーフロー               |
| ├─ `LookupError`           | シーケンスやマッピングの参照エラー基底 |
| │   ├─ `IndexError`        | シーケンスの範囲外アクセス             |
| │   └─ `KeyError`          | 辞書にないキーアクセス                 |
| ├─ `ValueError`            | 値の型や範囲が不正                     |
| ├─ `TypeError`             | 型が不正                               |
| ├─ `IOError` / `OSError`   | ファイル/入出力関連                    |
| └─ `ImportError`           | モジュールのインポート失敗             |


## 4. `try` / `except` 構文

例外をキャッチする基本形:

```python
try:
    # 例外が発生する可能性のある処理
    result = 10 / x
except ZeroDivisionError:
    print("Error: ゼロ除算が発生しました。")
    result = None
```

* **複数例外のキャッチ**:

  ```python
  try:
      data = my_dict[key]
  except (KeyError, IndexError) as e:
      print(f"参照エラー: {e}")
  ```

* **例外オブジェクトへのアクセス** (`as`):

  * 例外クラスの属性（`args`, `__str__()` など）を利用して詳細な情報を取得可能。

## 5. `else` と `finally` 節の活用

* **`else` 節**: 例外が発生しなかった場合に実行。

  ```python
  try:
      f = open('data.txt')
  except IOError:
      print("ファイルが開けませんでした。")
  else:
      print("ファイルを正常に開きました。読み込み処理を開始します。")
      content = f.read()
  ```

* **`finally` 節**: 例外の有無に関わらず必ず実行。

  ```python
  try:
      conn = open_connection()
      process(conn)
  except Exception as e:
      logging.error(f"処理中に例外発生: {e}")
  finally:
      conn.close()
      print("コネクションをクローズしました。")
  ```


## 6. カスタム例外クラスの定義

独自のエラー条件を表現するために、例外クラスを定義することができます。

```python
class ApplicationError(Exception):
    """アプリケーション全体で共通の例外基底クラス"""
    pass

class ValidationError(ApplicationError):
    """入力検証エラー"""
    def __init__(self, field: str, message: str):
        super().__init__(f"{field} の検証に失敗: {message}")
        self.field = field
        self.message = message

# 発生例
raise ValidationError('age', '負の値は許可されていません')
```

* **カスタム例外を使うメリット**:

  * エラーの意味を明確化
  * 上流でまとめてキャッチできる


## 7. コンテキストマネージャと例外処理

`with` 構文を使うと、リソース確保・解放のパターンを簡潔に扱えます。

```python
from contextlib import contextmanager

@contextmanager
def managed_resource(name):
    print(f"[{name}] リソースを確保")
    try:
        yield name
    except Exception as e:
        print(f"[{name}] 処理で例外発生: {e}")
        raise
    finally:
        print(f"[{name}] リソースを解放")

# 利用例
ingest_data = 'input.csv'
with managed_resource(ingest_data) as res:
    # res に対する処理
    process_csv(res)
```

* **標準ライブラリ例**: ファイル操作 (`open`)、スレッドロック (`threading.Lock`) など


## 8. ロギングを組み合わせた例外ハンドリング

例外情報をログに残すことで、障害解析が容易になります。

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(name)s: %(message)s'
)
logger = logging.getLogger(__name__)

try:
    result = compute()
except Exception as e:
    logger.exception("compute() で予期せぬ例外が発生しました。")
    # logger.exception はスタックトレース付きでエラーを記録
```

## 9. ベストプラクティスとアンチパターン

### ベストプラクティス

* 捕捉しない例外は上位に伝播させる
* 必要最小限の例外をキャッチする (`except Exception:` は避ける)
* ロギングと組み合わせる
* カスタム例外を定義し、意味のある名前を付ける
* ドキュメンテーションに例外仕様を明示する

### アンチパターン

* `except:` で全例外を丸呑みする
* エラー時に `pass` して無視する
* 例外から正常系にこっそり移行する


## 11. 参考資料

* 『Effective Python 第2版』Brett Slatkin
* Python ドキュメント: [Errors and Exceptions](https://docs.python.org/ja/3/tutorial/errors.html)
* PEP 343: The `with` statement
* 公式 logging モジュールドキュメント

