import os, requests, subprocess, time

BOT_TOKEN = os.getenv("BOT_TOKEN")  # will be set in Railway later
URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"

user_downloads = {}
unlocked_users = set()

def send_message(chat_id, text):
    requests.post(URL + "sendMessage", data={"chat_id": chat_id, "text": text})

def send_video(chat_id, file_path):
    with open(file_path, "rb") as f:
        requests.post(URL + "sendVideo", files={"video": f}, data={"chat_id": chat_id})

def download_video(insta_url, filename="video.mp4"):
    try:
        subprocess.run(["yt-dlp", "-f", "mp4", "-o", filename, insta_url], check=True)
        return os.path.exists(filename)
    except:
        return False

def main():
    print("🤖 Bot started...")
    last_update_id = None

    while True:
        try:
            response = requests.get(URL + "getUpdates", params={"offset": last_update_id})
            data = response.json()

            for update in data["result"]:
                if "message" not in update:
                    continue

                msg = update["message"]
                chat_id = msg["chat"]["id"]
                text = msg.get("text", "").strip()
                user_id = str(chat_id)
                last_update_id = update["update_id"] + 1

                if text == "/start":
                    send_message(chat_id, "👋 Welcome to Insta Downloader Bot!\n\n📥 Send public Instagram video/reel links.\n🔓 You get 2 free downloads.\n🔐 To unlock unlimited use:\n1️⃣ Follow: https://instagram.com/pungesh_420\n2️⃣ Send screenshot\n3️⃣ Type: om")
                    continue

                if text.lower() == "om":
                    unlocked_users.add(user_id)
                    send_message(chat_id, "✅ Unlocked! Send Insta links now.")
                    continue

                if "instagram.com" in text:
                    if user_id in unlocked_users or user_downloads.get(user_id, 0) < 2:
                        send_message(chat_id, "📥 Downloading your video...")
                        success = download_video(text)
                        if success:
                            send_video(chat_id, "video.mp4")
                            os.remove("video.mp4")
                            user_downloads[user_id] = user_downloads.get(user_id, 0) + 1
                        else:
                            send_message(chat_id, "❌ Failed. Make sure the link is public.")
                    else:
                        send_message(chat_id, "🔒 2 free uses over!\nFollow Instagram and reply with: om")
                else:
                    send_message(chat_id, "📎 Send a valid Instagram reel/video link.")
            time.sleep(1)
        except:
            time.sleep(5)

if __name__ == "__main__":
    main()
