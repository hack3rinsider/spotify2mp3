import subprocess

print("\n🎧 Step 1: Fetching songs from Spotify")
subprocess.run(["python", "1_spotify.py"], check=True)

print("\n🔍 Step 2: Searching songs on YouTube")
subprocess.run(["python", "2_spotifytoyt.py"], check=True)

print("\n⬇️ Step 3: Downloading songs")
subprocess.run(["python", "3_downloadfromlist.py"], check=True)

print("\n✅ All steps completed!")
