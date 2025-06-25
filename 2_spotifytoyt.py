import subprocess
import os
import json

CREDENTIALS_FILE = "credentials.txt"

# Load credentials
def load_credentials():
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r", encoding="utf-8") as f:
            try:
                creds = json.load(f)
                return creds.get("YTDLP_PATH", "").strip()
            except json.JSONDecodeError:
                print("[WARNING] Malformed credentials.txt")
    return ""

YTDLP_PATH = load_credentials()

if not YTDLP_PATH or not os.path.exists(YTDLP_PATH):
    print("[ERROR] yt-dlp path not found in credentials or the file does not exist.")
    exit(1)

available_file = open("available.txt", "w", encoding="utf-8")
not_found_file = open("not_found.txt", "w", encoding="utf-8")

# Read songs
with open("songs.txt", "r", encoding="utf-8") as f:
    songs = [line.strip() for line in f if line.strip()]

print(f"[INFO] Starting search for {len(songs)} songs...\n")

for idx, song in enumerate(songs, 1):
    print(f"[{idx}/{len(songs)}] Searching: {song}")
    try:
        result = subprocess.run(
            [
                YTDLP_PATH,
                f"ytsearch1:{song}",
                "--print", "%(title)s\n%(id)s",
                "--no-warnings", "--quiet"
            ],
            capture_output=True,
            text=True,
            timeout=20
        )

        output = result.stdout.strip().splitlines()
        if len(output) >= 2:
            title, video_id = output[0], output[1]
            url = f"https://www.youtube.com/watch?v={video_id}"
            entry = f"{idx}. {song} --> {title} | {url}"
            print(f"   [FOUND] {title}")
            available_file.write(entry + "\n")
            available_file.flush()
        else:
            print(f"   [NOT FOUND] {song}")
            not_found_file.write(f"{idx}. {song}\n")
            not_found_file.flush()

    except subprocess.TimeoutExpired:
        print(f"   [TIMEOUT] {song}")
        not_found_file.write(f"{idx}. {song}\n")
        not_found_file.flush()
    except Exception as e:
        print(f"   [ERROR] {song} | {e}")
        not_found_file.write(f"{idx}. {song}\n")
        not_found_file.flush()

available_file.close()
not_found_file.close()

print("\n[DONE] Search completed. Check available.txt and not_found.txt.")
