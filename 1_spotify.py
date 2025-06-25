import spotipy
from spotipy.oauth2 import SpotifyOAuth
import re
import os

CREDENTIALS_FILE = "credentials.txt"
CLIENT_ID = CLIENT_SECRET = PLAYLIST_URL = None

# Load credentials if they exist
if os.path.exists(CREDENTIALS_FILE):
    with open(CREDENTIALS_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        try:
            CLIENT_ID = lines[0].split("=", 1)[1].strip()
            CLIENT_SECRET = lines[1].split("=", 1)[1].strip()
            PLAYLIST_URL = lines[2].split("=", 1)[1].strip()
            print("🔐 Loaded credentials from credentials.txt")
        except Exception:
            print("⚠️ Malformed credentials.txt — will prompt for fresh credentials.")

# If any credential is missing, prompt user
if not CLIENT_ID or not CLIENT_SECRET or not PLAYLIST_URL:
    CLIENT_ID = input("Enter your Spotify CLIENT_ID: ").strip()
    CLIENT_SECRET = input("Enter your Spotify CLIENT_SECRET: ").strip()
    PLAYLIST_URL = input("Enter your Spotify playlist URL: ").strip()

    # Save to credentials.txt
    with open(CREDENTIALS_FILE, "w", encoding="utf-8") as cred_file:
        cred_file.write(f"CLIENT_ID = {CLIENT_ID}\n")
        cred_file.write(f"CLIENT_SECRET = {CLIENT_SECRET}\n")
        cred_file.write(f"PLAYLIST_URL = {PLAYLIST_URL}\n")
    print("✅ Saved credentials to credentials.txt")

# Extract playlist ID
match = re.search(r"playlist\/([a-zA-Z0-9]+)", PLAYLIST_URL)
if not match:
    print("❌ Invalid playlist URL.")
    exit(1)
PLAYLIST_ID = match.group(1)

# Set up Spotify client
REDIRECT_URI = 'http://localhost:8888/callback'
SCOPE = 'playlist-read-private'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))

# Fetch all songs from playlist
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

# Fetch and save
songs = get_playlist_tracks(PLAYLIST_ID)
for song in songs:
    print(song)

with open("songs.txt", "w", encoding="utf-8") as file:
    file.write("\n".join(songs))

print("🎶 Saved to songs.txt")
