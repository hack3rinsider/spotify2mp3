# 🎧 spotify2mp3 — v1.1 Update

This version focuses on automation and usability improvements to the original flow.

---

## ✅ What's New in v1.1

### 🔁 Automated Workflow

- Introduced `run_all.py` to execute all 3 scripts in order:
  1. Fetch songs from Spotify
  2. Search them on YouTube
  3. Download MP3s

### 🔐 First-time Credential Prompt

- Prompts user only once for:
  - Spotify `CLIENT_ID`
  - Spotify `CLIENT_SECRET`
  - Spotify Playlist URL
  - Full path to `yt-dlp.exe`
- Saves them in `credentials.txt` for future runs.

### 💾 Reusability

- All future runs automatically read from `credentials.txt` without asking again.

---

## 🔧 Usage

```bash
python run_all.py
