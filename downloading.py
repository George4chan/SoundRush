
"""
SIMPLE AUDIO DOWNLOADER - WORKING VERSION
Save as: audio_downloader.py
Run: python audio_downloader.py
"""

import os
import sys
import subprocess

# Auto-install yt-dlp
try:
    import yt_dlp
except ImportError:
    print("Installing yt-dlp...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
    import yt_dlp

def check_ffmpeg():
    """Check if FFmpeg is installed"""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except:
        return False

def download_audio():
    """Download audio from YouTube"""
    
    # Set download path
    download_path = os.path.join(os.path.expanduser("~"), "Downloads")
    
    print("\n" + "=" * 50)
    print("🎵 AUDIO DOWNLOADER")
    print("=" * 50)
    
    # Get URL
    url = input("\n📎 YouTube URL: ").strip()
    if not url:
        print("❌ No URL provided!")
        return
    
    # Format selection
    print("\n📀 Audio Format:")
    print("1. MP3 (Best compatibility)")
    print("2. M4A (Apple devices)")
    print("3. OPUS (Smallest size)")
    
    fmt_choice = input("Choose (1-3): ").strip()
    formats = {"1": "mp3", "2": "m4a", "3": "opus"}
    fmt = formats.get(fmt_choice, "mp3")
    
    # Quality selection
    print("\n⚡ Quality:")
    print("1. 128k (Small file)")
    print("2. 192k (Good)")
    print("3. 256k (Best)")
    
    q_choice = input("Choose (1-3): ").strip()
    qualities = {"1": "128", "2": "192", "3": "256"}
    quality = qualities.get(q_choice, "192")
    
    # Simple options that work
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': fmt,
            'preferredquality': quality,
        }],
        'quiet': False,
        'no_warnings': False,
    }
    
    print(f"\n📁 Saving to: {download_path}")
    print(f"🎵 Format: {fmt.upper()} | Quality: {quality}k")
    print("\n⏳ Downloading...\n")
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            print(f"\n✅ Downloaded: {info.get('title', 'Unknown')}")
            print(f"📍 Location: {download_path}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Troubleshooting:")
        print("1. Install FFmpeg (required): https://ffmpeg.org/download.html")
        print("2. Make sure URL is correct")
        print("3. Try a different video")

def main():
    """Main menu"""
    # Check FFmpeg
    if not check_ffmpeg():
        print("\n⚠️  WARNING: FFmpeg not found!")
        print("FFmpeg is required for audio conversion.")
        print("\n📥 Install FFmpeg:")
        print("  Windows: https://www.gyan.dev/ffmpeg/builds/")
        print("  Mac: brew install ffmpeg")
        print("  Linux: sudo apt install ffmpeg")
        print("\nContinue anyway? (Audio may not convert properly)")
        input("Press Enter to continue...")
    
    while True:
        print("\n" + "=" * 50)
        print("🎵 AUDIO DOWNLOADER")
        print("=" * 50)
        print("1. Download Audio")
        print("2. Exit")
        
        choice = input("\nChoose (1-2): ").strip()
        
        if choice == "1":
            download_audio()
        elif choice == "2":
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
