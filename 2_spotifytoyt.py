import subprocess

YTDLP_PATH = # You must copy this from your path

available_file = open("available.txt", "w", encoding="utf-8")
not_found_file = open("not_found.txt", "w", encoding="utf-8")

# Read songs
with open("songs.txt", "r", encoding="utf-8") as f:
    songs = [line.strip() for line in f if line.strip()]

print(f"🔍 Starting search for {len(songs)} songs...\n")

for idx, song in enumerate(songs, 1):
    print(f"[{idx}/{len(songs)}] Searching: {song}")
    try:
        result = subprocess.run(
            [
                YTDLP_PATH,
                f"ytsearch1:{song}",  # Only fetch top 1 result
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
            available_file.flush()
        else:
            print(f"   ❌ NOT FOUND: {song}")
            not_found_file.write(f"{idx}. {song}\n")
            not_found_file.flush()

    except subprocess.TimeoutExpired:
        print(f"   ⏱️ Timeout: {song}")
        not_found_file.write(f"{idx}. {song}\n")
        not_found_file.flush()
    except Exception as e:
        print(f"   ❌ Error: {song} | {e}")
        not_found_file.write(f"{idx}. {song}\n")
        not_found_file.flush()

# Close files
available_file.close()
not_found_file.close()

print("\n✅ Completed! Check available.txt and not_found.txt.")
