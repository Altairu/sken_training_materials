import os
import subprocess
import requests
import openai

# 環境変数からAPIキーとWebhook URLを取得
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

if not GOOGLE_API_KEY or not DISCORD_WEBHOOK_URL:
    raise EnvironmentError("Google APIキーまたはDiscord Webhook URLが設定されていません。")

# Gitの差分を取得
def get_git_diff():
    result = subprocess.run(["git", "diff", "--name-only"], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError("Git diffの取得に失敗しました。")
    return result.stdout.strip().split("\n")

# Google Generative AIを使用して要約を生成
def generate_summary(file_changes):
    openai.api_key = GOOGLE_API_KEY
    prompt = f"以下のファイル変更内容を要約してください:\n{file_changes}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )
    return response.choices[0].text.strip()

# Discordに通知を送信
def send_to_discord(summary):
    payload = {
        "content": f"重要な変更が検出されました:\n{summary}"
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    if response.status_code != 204:
        raise RuntimeError(f"Discord通知の送信に失敗しました: {response.status_code}")

# メイン処理
def main():
    try:
        changes = get_git_diff()
        if not changes:
            print("変更は検出されませんでした。")
            return

        summary = generate_summary("\n".join(changes))
        send_to_discord(summary)
        print("通知が送信されました。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    main()