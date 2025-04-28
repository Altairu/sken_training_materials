# Wiki の使い方と運営方法

この Wiki は、Sken の講習資料や課題を効率的に管理・共有するためのプラットフォームです。以下に、資料の追加方法や運営に関する決まり事を記載します。

## 必要な環境構築

1. **Python のインストール**  
   Python 3.8 以上が必要です。以下のコマンドでインストールを確認してください。
   ```bash
   python3 --version
   ```

2. **`pip` のインストール**  
   Python パッケージマネージャー `pip` をインストールします。
   ```bash
   sudo apt update
   sudo apt install python3-pip
   ```

3. **`mkdocs` とテーマのインストール**  
   MkDocs と Material for MkDocs をインストールします。
   ```bash
   pip install mkdocs
   pip install mkdocs-material
   ```

4. **必要なパッケージのバージョン確認**  
   以下のバージョンがインストールされていることを確認してください。
   ```
   python                       3.9.5
   mkdocs                       1.4.2
   mkdocs-material              8.5.11
   mkdocs-material-extentions   1.1.1
   pymdown-extensions           9.9
   ```

5. **ローカルサーバーの起動**  
   以下のコマンドでローカルサーバーを起動し、サイトを確認できます。
   ```bash
   mkdocs serve
   ```

## 資料追加方法

1. **資料ファイルを作成する**  
   適切なカテゴリフォルダ内に新しい資料ファイルを作成してください。  
   例: `docs/training_materials/講習資料/新しい資料.md`

2. **資料のフォーマット**  
   資料の末尾に以下の形式で著者情報を記載してください。
   ```markdown
   ??? Note
       著者:Shion Noguchi
   ```
??? Note
    著者:Shion Noguchi

3. **ナビゲーションの更新**  
   `mkdocs.yml` ファイルを編集し、新しい資料へのリンクをナビゲーションに追加します。  
   例:
   ```yaml
   nav:
     - 新しい資料: training_materials/講習資料/新しい資料.md
   ```

4. **ローカルで確認する**  
   以下のコマンドでローカルサーバーを起動し、変更を確認してください。
   ```bash
   mkdocs serve
   ```

5. **変更をコミットしてデプロイする**  
   変更を Git にコミットし、以下のコマンドでデプロイします。
   ```bash
   git add .
   git commit -m "新しい資料を追加"

   mkdocs gh-deploy　%ubuntuの場合はこちら

   & "$env:USERPROFILE\AppData\Roaming\Python\Python311\Scripts\mkdocs.exe" gh-deploy　%winの場合はこちら
   ```

## 運営に関する決まり事

1. **資料のフォーマット統一**  
   - 資料の末尾に必ず著者情報を記載してください。
   - 画像やコードブロックを使用する場合は適切な説明を付けてください。

2. **ファイル名の命名規則**  
   - ファイル名は英数字とアンダースコア（_）のみを使用してください。
   - 拡張子は `.md` を使用してください。

3. **ナビゲーションの整理**  
   - `mkdocs.yml` のナビゲーションはカテゴリごとに整理してください。
   - 不要なリンクや重複を避けるように注意してください。


## 問い合わせ

運営に関する質問や提案がある場合は、[こちら](https://x.com/Flying___eagle) の DM までご連絡ください。

??? Note
    著者:Shion Noguchi