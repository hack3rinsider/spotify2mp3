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

===============================
REQUIREMENTS
1. Spotify Developer Account
You need a Spotify Developer Account to get your CLIENT_ID and CLIENT_SECRET.

Sign up and create an app here:
https://developer.spotify.com/dashboard/

After creating your app, you'll find CLIENT_ID and CLIENT_SECRET on the app’s dashboard.

2. yt-dlp.exe
yt-dlp.exe is a command-line program to download videos and audio from YouTube.

Download the latest Windows executable from:
https://github.com/yt-dlp/yt-dlp/releases/latest

Save yt-dlp.exe somewhere on your computer, e.g., C:\Tools\yt-dlp.exe.

3. ffmpeg
ffmpeg is required for audio and video processing during downloads.

Download the Windows build here:
https://ffmpeg.org/download.html#build-windows

Extract the ffmpeg folder and add its bin directory (which contains ffmpeg.exe) to your system PATH environment variable, so it can be called from anywhere.

How to Get the Full Path of yt-dlp.exe
Locate where you saved yt-dlp.exe on your PC.

Right-click the file → Properties → copy the Location path.

Add \yt-dlp.exe at the end.

Example:
If location is C:\Tools, full path is

makefile
Copy
Edit
C:\Tools\yt-dlp.exe
Use this full path when the GUI asks for the yt-dlp executable location.
===============================

How to Use

You need to first install yt-dl and ffmpeg and note down their paths

Run spotify_gui.py.

Enter your Spotify CLIENT_ID, CLIENT_SECRET, playlist URL, and full path to yt-dlp.exe (first time only).

Click Run to start the complete process.

Watch live updates and logs directly in the GUI.
