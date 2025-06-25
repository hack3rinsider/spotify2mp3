🎧 spotify2mp3 — v1.2 Update (GUI Version)
This version introduces a user-friendly graphical interface and real-time progress tracking to simplify the entire download process.

✅ What's New in v1.2
🖥️ Graphical User Interface (GUI)
Built with Tkinter for easy interaction.

Single window to manage the entire workflow:

Enter credentials and playlist URL.

Run full process with one click.

View real-time logs and status updates within the GUI.

🔄 Automated End-to-End Workflow
Combines all steps:

Fetch songs from Spotify playlist.

Search songs on YouTube.

Download MP3 files.

No need to run multiple scripts separately.

🔐 Persistent Credentials
Prompts for Spotify API credentials, playlist URL, and yt-dlp path once.

Saves them securely for reuse in future runs.

📡 Real-Time Status Updates
Logs and progress streamed live in the GUI status panel.

Helps track which song is currently processed and download progress.

How to Use

You need to first install yt-dl and ffmpeg and note down their paths

Run spotify_gui.py.

Enter your Spotify CLIENT_ID, CLIENT_SECRET, playlist URL, and full path to yt-dlp.exe (first time only).

Click Run to start the complete process.

Watch live updates and logs directly in the GUI.
