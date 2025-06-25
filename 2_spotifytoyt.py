import subprocess
import os

CREDENTIALS_FILE = "credentials.txt"
YTDLP_PATH = None

# Load existing credentials
if os.path.exists(CREDENTIALS_FILE):
    with open(CREDENTIALS_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("YTDLP_PATH"):
                YTDLP_PATH = line.split("=", 1)[1].strip()

# Ask user if not found
if not YTDLP_PATH or not os.path.exists(YTDLP_PATH):
    YTDLP_PATH = input("Enter full path to yt-dlp.exe: ").strip()
    if not os.path.exists(YTDLP_PATH):
        print("❌ Provided path does not exist.")
        exit(1)

    # Append YTDLP_PATH to credentials.txt
    with open(CREDENTIALS_FILE, "a", encoding="utf-8") as f:
        f.write(f"YTDLP_PATH = {YTDLP_PATH}\n")
    print("✅ Saved yt-dlp path to credentials.txt")

# Output files
available_file = open("available.txt", "w", encoding="utf-8")
not_found_file = open("not_found.txt", "w", encoding="utf-8")

# Read songs
with open("songs.txt", "r", encoding="utf-8") as f:
    songs = [line.strip() for line in f if line.strip()]

print(f"🔍 Starting search for {len(songs)} songs...\n")

# Main search loop
for idx, song in enumerate(songs, 1):
    print(f"[{idx}/{len(songs)}] Searching: {song}")
    try:
        result = subprocess.run(
            [
                YTDLP_PATH,
                f"ytsearch1:{song}",  # fetch only top 1 result
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
            print(f"   ✅ FOUND: {title}")
            available_file.write(entry + "\n")
        else:
            print(f"   ❌ NOT FOUND: {song}")
            not_found_file.write(f"{idx}. {song}\n")

    except subprocess.TimeoutExpired:
        print(f"   ⏱️ Timeout: {song}")
        not_found_file.write(f"{idx}. {song}\n")
    except Exception as e:
        print(f"   ❌ Error: {song} | {e}")
        not_found_file.write(f"{idx}. {song}\n")

    available_file.flush()
    not_found_file.flush()

# Close files
available_file.close()
not_found_file.close()

print("\n✅ Completed! Check available.txt and not_found.txt.")
