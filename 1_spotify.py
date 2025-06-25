import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Your Spotify Developer credentials
CLIENT_ID = # You must copy this from your dashboard
CLIENT_SECRET =  # You must copy this from your dashboard
REDIRECT_URI = 'http://localhost:8888/callback'
SCOPE = 'playlist-read-private'

# Replace with your Spotify playlist ID (e.g., from https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M)
PLAYLIST_ID = # You must copy this from your dashboard

# Authenticate and create Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))

# Function to fetch all tracks from playlist
def get_playlist_tracks(playlist_id):
    results = sp.playlist_items(playlist_id)
    tracks = results['items']

    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    song_list = []
    for item in tracks:
        track = item['track']
        if track:  # Handle cases where track is None
            name = track['name']
            artists = ', '.join([artist['name'] for artist in track['artists']])
            song_list.append(f"{name} - {artists}")

    return song_list

# Run and print songs
songs = get_playlist_tracks(PLAYLIST_ID)
for song in songs:
    print(song)

# Add this block to save to file
with open("songs.txt", "w", encoding="utf-8") as file:
    file.write("\n".join(songs))
