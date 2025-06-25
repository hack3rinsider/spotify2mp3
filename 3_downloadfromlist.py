import sys
import os
import json
import subprocess
import glob

# Enable UTF-8 printing for emojis on Windows
if os.name == 'nt':
    sys.stdout.reconfigure(encoding='utf-8')

CREDENTIALS_FILE = "credentials.txt"

def load_ytdlp_path():
    """Load yt-dlp path from credentials.txt (JSON format)."""
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r", encoding="utf-8") as f:
            try:
                creds = json.load(f)
                return creds.get("YTDLP_PATH", "").strip()
            except json.JSONDecodeError:
                print("⚠️ Malformed credentials.txt")
    return ""

YTDLP_PATH = load_ytdlp_path()

if not YTDLP_PATH or not os.path.exists(YTDLP_PATH):
    print("❌ yt-dlp path not found or invalid in credentials.txt")
    exit(1)

# File paths
INPUT_FILE = "available.txt"
OUTPUT_DIR = os.path.join(os.getcwd(), "downloads")
LOG_FILE = "logss.txt"
FAILED_FILE = "failed.txt"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Parse available.txt
songs = []
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line or "-->" not in line or "|" not in line:
            continue
        try:
            _, right = line.split("-->", 1)
            title_part, url = right.rsplit("|", 1)
            title = title_part.strip()
            url = url.strip()
            songs.append((title, url))
        except ValueError:
            continue

failed = []

with open(LOG_FILE, "w", encoding="utf-8") as logf:
    for idx, (title, url) in enumerate(songs, start=1):
        # Skip already downloaded
        existing = glob.glob(os.path.join(OUTPUT_DIR, f"*{title[:80]}*.mp3"))
        if existing:
            print(f"[SKIPPED] Already downloaded: {title}")
            continue

        print(f"\n🎧 [DOWNLOAD] ({idx}/{len(songs)}) {title}")
        logf.write(f"\n--- Downloading: {title} ---\n")

        output_template = os.path.join(OUTPUT_DIR, f"%(title).100s.%(ext)s")

        cmd = [
            YTDLP_PATH,
            url,
            "--cookies", "cookies.txt",
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", "0",
            "--embed-thumbnail",
            "--embed-metadata",
            "--add-metadata",
            "--no-playlist",
            "--no-call-home",
            "--no-overwrites",
            "--no-part",
            "--skip-unavailable-fragments",
            "--abort-on-unavailable-fragment",
            "--fragment-retries", "3",
            "--format", "bestaudio[ext=m4a]/bestaudio[protocol^=http]",
            "--force-ipv4",
            "-o", output_template
        ]

        try:
            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
            )
            for line in process.stdout:
                print(line, end="")
                logf.write(line)

            process.wait()
            downloaded = glob.glob(os.path.join(OUTPUT_DIR, f"*{title[:80]}*.mp3"))

            if process.returncode != 0 or not downloaded:
                print(f"❌ [FAILED] {title}")
                logf.write(f"[FAILED] {title}\n")
                for file in glob.glob(os.path.join(OUTPUT_DIR, f"*{title[:80]}*")):
                    os.remove(file)
                failed.append((title, url))
        except subprocess.TimeoutExpired:
            print(f"⏱️ [TIMEOUT] {title}")
            logf.write(f"[TIMEOUT] {title}\n")
            failed.append((title, url))

# Save failed downloads
if failed:
    with open(FAILED_FILE, "w", encoding="utf-8") as f:
        for title, url in failed:
            f.write(f"{title}\n{url}\n\n")
    print(f"\n⚠️ {len(failed)} downloads failed. See '{FAILED_FILE}'.")

print(f"\n✅ All downloads completed. Files saved to: {OUTPUT_DIR}")
