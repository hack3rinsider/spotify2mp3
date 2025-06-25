import os
import re
import subprocess
import glob

# Files
CREDENTIALS_FILE = "credentials.txt"
INPUT_FILE = "available.txt"
OUTPUT_DIR = os.path.join(os.getcwd(), "downloads")
LOG_FILE = "logss.txt"
FAILED_FILE = "failed.txt"

# Load or prompt for yt-dlp path
YTDLP_PATH = None
if os.path.exists(CREDENTIALS_FILE):
    with open(CREDENTIALS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("YTDLP_PATH"):
                YTDLP_PATH = line.split("=", 1)[1].strip()
                break

if not YTDLP_PATH or not os.path.exists(YTDLP_PATH):
    YTDLP_PATH = input("Enter full path to yt-dlp.exe: ").strip().strip("'\"")
    if not os.path.exists(YTDLP_PATH):
        print("❌ Provided yt-dlp path does not exist. Exiting.")
        exit(1)
    with open(CREDENTIALS_FILE, "a", encoding="utf-8") as f:
        f.write(f"YTDLP_PATH = {YTDLP_PATH}\n")
    print("✅ Saved yt-dlp path to credentials.txt")

# Ensure output folder exists
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

# Download loop
failed = []
with open(LOG_FILE, "w", encoding="utf-8") as logf:
    for idx, (title, url) in enumerate(songs, start=1):
        existing = glob.glob(os.path.join(OUTPUT_DIR, f"*{title[:80]}*.mp3"))
        if existing:
            print(f"[SKIPPED] Already downloaded: {title}")
            continue

        print(f"\n[DOWNLOAD] ({idx}/{len(songs)}) {title}")
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
                print(f"[FAILED] {title}")
                logf.write(f"[FAILED] {title}\n")
                for file in glob.glob(os.path.join(OUTPUT_DIR, f"*{title[:80]}*")):
                    os.remove(file)
                failed.append((title, url))
        except subprocess.TimeoutExpired:
            print(f"[TIMEOUT] {title}")
            logf.write(f"[TIMEOUT] {title}\n")
            failed.append((title, url))

# Save failed downloads
if failed:
    with open(FAILED_FILE, "w", encoding="utf-8") as f:
        for title, url in failed:
            f.write(f"{title}\n{url}\n\n")
    print(f"\n[WARNING] {len(failed)} downloads failed. See '{FAILED_FILE}'.")

print(f"\n✅ All downloads completed. Files saved to: {OUTPUT_DIR}")
