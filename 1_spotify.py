import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import re
import json
import sys

CREDENTIALS_FILE = "credentials.txt"

# Load credentials from JSON file
def load_credentials():
    if not os.path.exists(CREDENTIALS_FILE):
        print("❌ credentials.txt not found.")
        return None
    try:
        with open(CREDENTIALS_FILE, "r", encoding="utf-8") as f:
            creds = json.load(f)
            required = ["CLIENT_ID", "CLIENT_SECRET", "PLAYLIST_URL"]
            if not all(k in creds for k in required):
                raise ValueError("Missing required fields.")
            return creds
    except Exception as e:
        print(f"⚠️ Failed to load credentials: {e}")
        return None

# Prompt user for missing credentials
def prompt_for_credentials():
    print("🔑 Enter Spotify credentials:")
    client_id = input("CLIENT_ID: ").strip()
    client_secret = input("CLIENT_SECRET: ").strip()
    playlist_url = input("Playlist URL: ").strip()
    creds = {
        "CLIENT_ID": client_id,
        "CLIENT_SECRET": client_secret,
        "PLAYLIST_URL": playlist_url
    }
    with open(CREDENTIALS_FILE, "w", encoding="utf-8") as f:
        json.dump(creds, f, indent=2)
    print("✅ Credentials saved to credentials.txt")
    return creds

# Load or prompt
credentials = load_credentials() or prompt_for_credentials()

CLIENT_ID = credentials["CLIENT_ID"]
CLIENT_SECRET = credentials["CLIENT_SECRET"]
PLAYLIST_URL = credentials["PLAYLIST_URL"]

# Extract playlist ID
match = re.search(r"playlist/([a-zA-Z0-9]+)", PLAYLIST_URL)
if not match:
    print("❌ Invalid playlist URL.")
    sys.exit(1)

PLAYLIST_ID = match.group(1)

# Authenticate with Spotify
REDIRECT_URI = 'http://localhost:8888/callback'
SCOPE = 'playlist-read-private'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))

# Fetch tracks
def get_playlist_tracks(playlist_id):
    results = sp.playlist_items(playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    song_list = []
    for item in tracks:
        track = item['track']
        if track:
            name = track['name']
            artists = ', '.join([artist['name'] for artist in track['artists']])
            song_list.append(f"{name} - {artists}")
    return song_list

# Run and save
songs = get_playlist_tracks(PLAYLIST_ID)

if not songs:
    print("⚠️ No songs found in the playlist.")
    sys.exit(1)

for song in songs:
    print(song)

with open("songs.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(songs))

print("Saved to songs.txt")
