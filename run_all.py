import subprocess
import sys
import os

# Ensure terminal handles UTF-8 output
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    # For Python versions < 3.7 or when reconfigure isn't available
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("\n🎧 Step 1: Fetching songs from Spotify")
subprocess.run(["python", "1_spotify.py"], check=True)

print("\n🔍 Step 2: Searching songs on YouTube")
subprocess.run(["python", "2_spotifytoyt.py"], check=True)

print("\n⬇️ Step 3: Downloading songs")
subprocess.run(["python", "3_downloadfromlist.py"], check=True)

print("\n✅ All steps completed!")
