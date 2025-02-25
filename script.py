import os
import sys
import json
import datetime

LOG_FILE = os.path.join(os.path.dirname(__file__), "python_log.txt")

def log_to_file(message):
    """ログをファイルに出力"""
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as log_file:
            log_file.write(f"{datetime.datetime.now()} - {message}\n")
            log_file.flush()
        print(f"📝 ログ出力: {message}", flush=True)
    except Exception as e:
        print(f"❌ ログ書き込みエラー: {e}", flush=True)

def main():
    try:
        log_to_file("🚀 Python スクリプトが実行されました。")

        # ✅ JSON データの受け取り
        json_data = sys.argv[1]
        data = json.loads(json_data)

        log_to_file(f"受け取ったデータ: {json_data}")

        operation = data.get("operation")
        room_name = data.get("room_name")
        password = data.get("password")

        if operation == 1:
            log_to_file(f"ルーム作成: {room_name} (パスワード: {password})")
        elif operation == 2:
            log_to_file(f"ルーム参加: {room_name} (パスワード: {password})")
        else:
            log_to_file("不明な操作です")

        # ✅ Python の標準出力にデータを確実に送信
        print("📩 Python: 処理完了", flush=True)

    except Exception as e:
        log_to_file(f"❌ エラー: {str(e)}")
        print(f"❌ エラー: {str(e)}", flush=True)

if __name__ == "__main__":
    main()
