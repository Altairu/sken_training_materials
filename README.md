# sken_training_materials
sken_講習資料

https://Altairu.github.io/sken_training_materials/

```bash
mkdocs gh-deploy
```

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

## 資料追加の手順

1. **資料ファイルを作成する**  
   `docs/training_materials` フォルダ内の適切なカテゴリに新しい資料ファイル（例: `new_material.md`）を作成します。

2. **`mkdocs.yml` にナビゲーションを追加する**  
   `mkdocs.yml` ファイルを編集し、新しい資料へのリンクをナビゲーションに追加します。例:
   ```yaml
   nav:
     - 新しい資料: training_materials/新しい資料/new_material.md
   ```

3. **ローカルで確認する**  
   以下のコマンドを実行してローカルサーバーを起動し、変更を確認します。
   ```bash
   mkdocs serve
   ```

4. **変更をコミットしてデプロイする**  
   変更を Git にコミットし、以下のコマンドでデプロイします。
   ```bash
   git add .
   git commit -m "新しい資料を追加"
   mkdocs gh-deploy
   ```

5. **公開されたサイトを確認する**  
   `https://Altairu.github.io/sken_training_materials/` にアクセスして、資料が正しく追加されていることを確認します。

## コントリビューションの手順

他の人がこのリポジトリに変更を加えるには、以下の手順を実行してください。

1. **リポジトリをフォークする**  
   GitHub 上でこのリポジトリをフォークします。

2. **ローカルにクローンする**  
   フォークしたリポジトリをローカル環境にクローンします。
   ```bash
   git clone https://github.com/<あなたのGitHubユーザー名>/sken_training_materials.git
   cd sken_training_materials
   ```

3. **変更を加える**  
   必要な資料を追加・編集し、`mkdocs.yml` にナビゲーションを追加します。

4. **変更をコミットする**  
   変更をステージングしてコミットします。
   ```bash
   git add .
   git commit -m "資料を追加/編集"
   ```

5. **プルリクエストを作成する**  
   GitHub 上でフォークしたリポジトリからオリジナルのリポジトリに対してプルリクエストを作成します。

6. **レビューを待つ**  
   プルリクエストが承認されるまで待ちます。必要に応じて修正を行ってください。

これにより、他の人も安全にコントリビューションを行うことができます。