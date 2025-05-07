import os
import subprocess
import requests
from dotenv import load_dotenv

# .envファイルから環境変数をロード
load_dotenv()
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

if not DISCORD_WEBHOOK_URL:
    raise EnvironmentError("Discord Webhook URLが設定されていません。")

# 最新のコミットメッセージを取得
def get_latest_commit_message():
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--pretty=%h %s - %an"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise RuntimeError("Gitログの取得に失敗しました。")
        return result.stdout.strip()
    except Exception as e:
        raise RuntimeError(f"Gitログ取得中にエラーが発生しました: {e}")

# Discordに通知を送信
def send_to_discord(commit_message):
    try:
        payload = {
            "embeds": [
                {
                    "title": "📝 Webサイトに重要な変更がありました！",
                    "description": commit_message,
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
        print("通知内容: ", commit_message)

# メイン処理
def main():
    try:
        commit_message = get_latest_commit_message()
        print(f"最新のコミットメッセージ: {commit_message}")  # デバッグ用
        send_to_discord(commit_message)
        print("通知が送信されました。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    main()