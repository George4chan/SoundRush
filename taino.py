"""
MUSIC & VIDEO DOWNLOADER - ALL IN ONE
Save as: download.py
Run: python download.py
"""

import os
import sys
import subprocess

# Auto-install yt-dlp if missing
try:
    import yt_dlp
except ImportError:
    print("Installing yt-dlp...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
    import yt_dlp

def download_audio():
    download_path = os.path.join(os.path.expanduser("~"), "Downloads")
    
    print("=" * 60)
    print("🎵 AUDIO DOWNLOADER")
    print("=" * 60)
    
    url = input("\nEnter YouTube URL: ").strip()
    
    print("\nFormat:")
    print("1. MP3  2. M4A  3. WAV  4. FLAC  5. OPUS")
    fmt_choice = input("Choose (1-5): ")
    formats = {"1": "mp3", "2": "m4a", "3": "wav", "4": "flac", "5": "opus"}
    fmt = formats.get(fmt_choice, "mp3")
    
    print("\nQuality: 1. 128k  2. 192k  3. 256k  4. 320k")
    q_choice = input("Choose (1-4): ")
    qualities = {"1": "128", "2": "192", "3": "256", "4": "320"}
    quality = qualities.get(q_choice, "192")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': fmt, 'preferredquality': quality}],
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
    }
    
    print(f"\nDownloading to: {download_path}\n")
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        print(f"Title: {info['title']}")
        ydl.download([url])
    
    print(f"\nDone! File saved to Downloads folder")

def download_video():
    download_path = os.path.join(os.path.expanduser("~"), "Downloads")
    
    print("=" * 60)
    print("🎬 VIDEO DOWNLOADER (MP4)")
    print("=" * 60)
    
    url = input("\nEnter YouTube URL: ").strip()
    
    print("\nQuality: 1. Best  2. 1080p  3. 720p  4. 480p  5. 360p")
    q_choice = input("Choose (1-5): ")
    heights = {"1": "best", "2": "1080", "3": "720", "4": "480", "5": "360"}
    height = heights.get(q_choice, "best")
    
    if height == "best":
        fmt_str = 'bestvideo+bestaudio/best'
    else:
        fmt_str = f'bestvideo[height<={height}]+bestaudio/best[height<={height}]'
    
    ydl_opts = {
        'format': fmt_str,
        'merge_output_format': 'mp4',
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
    }
    
    print(f"\nDownloading to: {download_path}\n")
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        print(f"Title: {info['title']}")
        ydl.download([url])
    
    print(f"\nDone! File saved to Downloads folder")

# Main menu
while True:
    print("\n" + "=" * 60)
    print("🎵 MUSIC & VIDEO DOWNLOADER")
    print("=" * 60)
    print("1. Download Audio (MP3/M4A/WAV/FLAC/OPUS)")
    print("2. Download Video (MP4)")
    print("3. Exit")
    
    choice = input("\nChoose (1-3): ")
    
    if choice == "1":
        download_audio()
    elif choice == "2":
        download_video()
    elif choice == "3":
        print("\nGoodbye!")
        break
    else:
        print("\nInvalid choice. Try again.")
