import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import os
import json
import subprocess
import threading

CREDENTIALS_FILE = "credentials.txt"

def load_credentials():
    if os.path.exists(CREDENTIALS_FILE):
        try:
            with open(CREDENTIALS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Invalid JSON in credentials.txt")
            return {}
    return {}

def save_credentials(data):
    with open(CREDENTIALS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

class SpotifyToMP3GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🎷 Spotify to MP3 Downloader")
        self.geometry("600x580")
        self.resizable(False, False)

        self.credentials = load_credentials()

        self.client_id_var = tk.StringVar(value=self.credentials.get("CLIENT_ID", ""))
        self.client_secret_var = tk.StringVar(value=self.credentials.get("CLIENT_SECRET", ""))
        self.playlist_url_var = tk.StringVar(value=self.credentials.get("PLAYLIST_URL", ""))
        self.ytdlp_path_var = tk.StringVar(value=self.credentials.get("YTDLP_PATH", ""))

        self.create_widgets()
        self.step_count = 0

    def create_widgets(self):
        tk.Label(self, text="Spotify CLIENT_ID:").pack(anchor="w", padx=20)
        tk.Entry(self, textvariable=self.client_id_var, width=70).pack(padx=20)

        tk.Label(self, text="Spotify CLIENT_SECRET:").pack(anchor="w", padx=20, pady=(10, 0))
        tk.Entry(self, textvariable=self.client_secret_var, width=70).pack(padx=20)

        tk.Label(self, text="Spotify Playlist URL:").pack(anchor="w", padx=20, pady=(10, 0))
        tk.Entry(self, textvariable=self.playlist_url_var, width=70).pack(padx=20)

        tk.Label(self, text="Path to yt-dlp.exe:").pack(anchor="w", padx=20, pady=(10, 0))
        path_frame = tk.Frame(self)
        path_frame.pack(padx=20)
        tk.Entry(path_frame, textvariable=self.ytdlp_path_var, width=56).pack(side="left")
        tk.Button(path_frame, text="Browse", command=self.browse_ytdlp).pack(side="left", padx=5)

        tk.Button(self, text="📂 Save Credentials", command=self.save_cred).pack(pady=10)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="🎵 Fetch Songs", width=15, command=self.fetch_songs).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="🔍 Search on YouTube", width=18, command=self.search_youtube).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="⬇️ Download MP3s", width=15, command=self.download_mp3s).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="▶️ Run Full Process", width=18, command=self.run_all).grid(row=1, column=0, columnspan=3, pady=5)

        self.progress = ttk.Progressbar(self, orient="horizontal", length=500, mode="determinate", maximum=3)
        self.progress.pack(pady=5)

        tk.Label(self, text="📝 Status:").pack(anchor="w", padx=20)
        self.status_text = tk.Text(self, height=12, width=70)
        self.status_text.pack(padx=20)

    def browse_ytdlp(self):
        path = filedialog.askopenfilename(title="Select yt-dlp.exe", filetypes=[("yt-dlp", "*.exe")])
        if path:
            self.ytdlp_path_var.set(path)

    def save_cred(self):
        data = {
            "CLIENT_ID": self.client_id_var.get().strip(),
            "CLIENT_SECRET": self.client_secret_var.get().strip(),
            "PLAYLIST_URL": self.playlist_url_var.get().strip(),
            "YTDLP_PATH": self.ytdlp_path_var.get().strip()
        }
        save_credentials(data)
        self.status("✅ Credentials saved.")

    def status(self, msg):
        self.status_text.insert("end", msg + "\n")
        self.status_text.see("end")

    def update_progress(self):
        self.progress["value"] = self.step_count

    def stream_subprocess(self, cmd, label="", step=None):
        def run():
            try:
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding="utf-8",
                    errors="replace"
                )
                for line in process.stdout:
                    self.after(0, self.status, line.rstrip())
                process.wait()
                if process.returncode == 0:
                    self.after(0, self.status, f"✅ {label} completed.")
                else:
                    self.after(0, self.status, f"❌ {label} failed with code {process.returncode}")
            except Exception as e:
                self.after(0, self.status, f"❌ Error during {label}: {e}")
            finally:
                if step is not None:
                    self.step_count += 1
                    self.after(0, self.update_progress)

        threading.Thread(target=run, daemon=True).start()

    def fetch_songs(self):
        self.status("🔁 Fetching songs...")
        self.stream_subprocess(["python", "1_spotify.py"], label="Fetch Songs")

    def search_youtube(self):
        self.status("🔍 Searching YouTube...")
        self.stream_subprocess(["python", "2_spotifytoyt.py"], label="Search YouTube")

    def download_mp3s(self):
        self.status("⬇️ Downloading MP3s...")
        self.stream_subprocess(["python", "3_downloadfromlist.py"], label="Download MP3s")

    def run_all(self):
        self.status("🚀 Running full process...")
        self.step_count = 0
        self.progress["value"] = 0
        self.stream_subprocess(["python", "1_spotify.py"], label="Fetch Songs", step=1)
        self.after(2000, lambda: self.stream_subprocess(["python", "2_spotifytoyt.py"], label="Search YouTube", step=1))
        self.after(4000, lambda: self.stream_subprocess(["python", "3_downloadfromlist.py"], label="Download MP3s", step=1))

if __name__ == "__main__":
    app = SpotifyToMP3GUI()
    app.mainloop()
