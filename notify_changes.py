import os
import subprocess
import requests
import google.generativeai as genai
from dotenv import load_dotenv

# .envファイルから環境変数をロード
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

if not GOOGLE_API_KEY or not DISCORD_WEBHOOK_URL:
    raise EnvironmentError("Google APIキーまたはDiscord Webhook URLが設定されていません。")

# Google Generative AIのAPIキーを設定
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    raise RuntimeError(f"Google Generative AIの初期化に失敗しました: {e}")

# Gitの差分を取得
def get_git_diff():
    try:
        result = subprocess.run(["git", "diff", "--name-only"], capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError("Git diffの取得に失敗しました。")
        return result.stdout.strip().split("\n")
    except Exception as e:
        raise RuntimeError(f"Gitの差分取得中にエラーが発生しました: {e}")

# Google Generative AIを使用して重要性を判定
def is_change_important(file_changes):
    try:
        prompt = (
            "この変更が「実質的な情報の追加・更新（＝利用者が読む内容の変化）」を含んでいるかどうかを判定してください。\n"
            "以下のような変更は重要ではありません：\n"
            "- ウェブサイトの構造やHTMLレイアウトの変更\n"
            "- ナビゲーションやCSS、デザイン変更\n"
            "- MkDocs等の自動生成によるインデックス・フッター等の作成\n"
            "- 改行、スペース、フォーマット、句読点の修正\n"
            "これらに該当する場合は、「この変更は重要ではありません」とだけ答えてください。\n"
            "逆に、記事の内容に新しい説明や資料が追加された場合のみ、要約して答えてください。\n"
            f"変更内容:\n{file_changes}"
        )
        print(f"AIに送信するプロンプト:\n{prompt}")  # デバッグ用にプロンプトを出力
        response = model.generate_content(prompt)
        result = response.text.strip()
        print(f"AIからの応答: {result}")  # デバッグ用にAIの応答を出力
        if not result:
            raise ValueError("AIからの応答が空です。")
        if result == "この変更は重要ではありません":
            return False, None
        return True, result
    except Exception as e:
        print(f"AI応答の取得中にエラーが発生しました: {e}")
        return False, "AI応答の取得に失敗しました。変更内容を確認してください。"

# Discordに通知を送信
def send_to_discord(summary):
    try:
        payload = {
            "embeds": [
                {
                    "title": "📝 Webサイトに重要な変更がありました！",
                    "description": "このWebサイトの更新では、以下の変更が加えられました。\n\n" + summary,
                    "color": 5814783,
                    "url": "https://altairu.github.io/sken_training_materials/"
                }
            ]
        }
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        if response.status_code != 204:
            raise RuntimeError(f"Discord通知の送信に失敗しました: {response.status_code}")
    except Exception as e:
        print(f"Discord通知の送信中にエラーが発生しました: {e}")
        print("通知内容: ", summary)

# メイン処理
def main():
    try:
        changes = get_git_diff()
        if not changes:
            print("変更は検出されませんでした。")
            return

        changes_text = "\n".join(changes)
        is_important, summary = is_change_important(changes_text)
        if not is_important:
            print("変更は重要ではありません。通知を送信しません。")
            return

        send_to_discord(summary)
        print("通知が送信されました。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    main()