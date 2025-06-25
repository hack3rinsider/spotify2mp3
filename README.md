PYTHON tool to download your spotify playlist to mp3

Requirements:
		1. yt-dlp 
		2. ffmpeg
		3. spotify developer credentials
How to run:
		1. edit the python script 1_spotify.py
		2. add CLIENT_ID CLIENT_SECRET PLAYLIST_ID 
		3. edit 2_spotifytoyt.py and 3_downloadfromfile.py
		4. add your path to yt-dlp in YTDLP_PATH
		5. run the python scripts serially
Notes: in the end you will get all logs and list of available songs not found songs failed songs in specific txt files you can check there.