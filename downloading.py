import os
import sys
import subprocess

try:
    import yt_dlp
except ImportError:
    print("Installing yt-dlp...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
    import yt_dlp

def download():
    path = os.path.join(os.path.expanduser("~"), "Downloads")
    
    print("\n" + "="*50)
    print("AUDIO DOWNLOADER")
    print("="*50)
    
    url = input("\nURL: ").strip()
    if not url:
        print("No URL")
        return
    
    print("\n1. M4A (Best)")
    print("2. OPUS (Small)")
    choice = input("Choose (1-2): ").strip()
    
    if choice == "1":
        fmt = 'bestaudio[ext=m4a]/bestaudio'
        ext = 'm4a'
    else:
        fmt = 'bestaudio[ext=opus]/bestaudio'
        ext = 'opus'
    
    opts = {
        'format': fmt,
        'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
        'quiet': False,
    }
    
    print(f"\nSaving to: {path}")
    print("Downloading...\n")
    
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            print(f"\nDone: {info.get('title')}")
    except Exception as e:
        print(f"\nError: {e}")

while True:
    print("\n1. Download")
    print("2. Exit")
    c = input("\nChoice: ")
    if c == "1":
        download()
    elif c == "2":
        print("\nGoodbye!")
        break
