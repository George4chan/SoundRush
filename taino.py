"""
PERFECT AUDIO DOWNLOADER - Professional Edition
Save as: audio_downloader.py
Run: python audio_downloader.py
"""

import os
import sys
import subprocess
import re
from pathlib import Path

# Auto-install yt-dlp if missing
try:
    import yt_dlp
except ImportError:
    print("📦 Installing yt-dlp...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
    import yt_dlp

def sanitize_filename(filename):
    """Remove invalid characters from filename"""
    return re.sub(r'[<>:"/\\|?*]', '', filename)

def get_download_path():
    """Get download path with custom option"""
    default_path = os.path.join(os.path.expanduser("~"), "Music", "Downloads")
    
    print("\n📁 Download Location:")
    print(f"1. Default: {default_path}")
    print("2. Custom location")
    choice = input("Choose (1-2): ")
    
    if choice == "2":
        custom = input("Enter full path: ").strip()
        if os.path.exists(custom):
            return custom
        else:
            print(f"⚠️ Path doesn't exist. Creating: {custom}")
            os.makedirs(custom, exist_ok=True)
            return custom
    else:
        os.makedirs(default_path, exist_ok=True)
        return default_path

def download_audio():
    """Main audio download function"""
    print("\n" + "=" * 70)
    print("🎵 PROFESSIONAL AUDIO DOWNLOADER")
    print("=" * 70)
    
    # Get URL
    url = input("\n🔗 Enter YouTube URL or playlist URL: ").strip()
    if not url:
        print("❌ No URL provided!")
        return
    
    # Get download location
    download_path = get_download_path()
    
    # Format selection
    print("\n🎵 Audio Format:")
    formats = {
        "1": {"name": "MP3", "codec": "mp3", "desc": "Universal compatibility"},
        "2": {"name": "M4A", "codec": "m4a", "desc": "Apple devices, smaller size"},
        "3": {"name": "FLAC", "codec": "flac", "desc": "Lossless, highest quality"},
        "4": {"name": "WAV", "codec": "wav", "desc": "Uncompressed, huge files"},
        "5": {"name": "OPUS", "codec": "opus", "desc": "Best compression, modern"},
        "6": {"name": "AAC", "codec": "aac", "desc": "Good quality, small size"}
    }
    
    for key, fmt in formats.items():
        print(f"  {key}. {fmt['name']:4} - {fmt['desc']}")
    
    fmt_choice = input("\nChoose (1-6): ").strip()
    selected_format = formats.get(fmt_choice, formats["1"])
    fmt = selected_format["codec"]
    
    # Quality selection with recommended settings
    print(f"\n🎚️ Quality Settings for {selected_format['name'].upper()}:")
    
    if fmt in ["flac", "wav"]:
        # Lossless formats
        qualities = {"1": "0", "2": "5", "3": "8"}
        print("  1. Best (Slow encoding)")
        print("  2. Normal (Recommended)")
        print("  3. Fast (Lower compression)")
        default_quality = "2"
    elif fmt == "opus":
        qualities = {"1": "64", "2": "96", "3": "128", "4": "160"}
        print("  1. 64k  - Small file")
        print("  2. 96k  - Good quality")
        print("  3. 128k - Best for most (Recommended)")
        print("  4. 160k - Excellent quality")
        default_quality = "3"
    else:
        # MP3, M4A, AAC
        qualities = {"1": "128", "2": "192", "3": "256", "4": "320"}
        print("  1. 128k - Small file")
        print("  2. 192k - Good quality")
        print("  3. 256k - Very good (Recommended)")
        print("  4. 320k - Best quality")
        default_quality = "3"
    
    q_choice = input(f"\nChoose (1-{len(qualities)}), or Enter for default: ").strip()
    if not q_choice:
        q_choice = default_quality
    quality = qualities.get(q_choice, qualities[default_quality])
    
    # Additional options
    print("\n⚙️ Additional Options:")
    print("  1. Download single video/playlist")
    print("  2. Download specific range (e.g., 1-5, 1,3,5)")
    print("  3. Download all")
    range_choice = input("\nChoose (1-3): ").strip()
    
    # Extract playlist info
    ydl_opts_base = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts_base) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            is_playlist = 'entries' in info
            
            if is_playlist:
                total_videos = len(info['entries'])
                print(f"\n📋 Playlist detected: {info.get('title', 'Unknown')}")
                print(f"📊 Total videos: {total_videos}")
                
                if range_choice == "2":
                    range_str = input("Enter range (e.g., 1-5 or 1,3,5): ").strip()
                    if '-' in range_str:
                        start, end = map(int, range_str.split('-'))
                        indices = range(start-1, end)
                    else:
                        indices = [int(x)-1 for x in range_str.split(',')]
                elif range_choice == "1":
                    indices = [int(input(f"Enter video number (1-{total_videos}): ")) - 1]
                else:
                    indices = range(total_videos)
            else:
                indices = [0]
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return
    
    # Build options
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': fmt,
            'preferredquality': quality,
        }],
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'progress_hooks': [progress_hook],
        'ignoreerrors': True,
        'nooverwrites': True,
        'continuedl': True,
        'writethumbnail': True,
        'postprocessor_args': [
            '-metadata', f'comment=Downloaded by Perfect Audio Downloader',
        ],
    }
    
    # Add thumbnail embedding for supported formats
    if fmt in ['mp3', 'm4a']:
        ydl_opts['postprocessors'].append({
            'key': 'EmbedThumbnail',
            'already_have_thumbnail': False,
        })
    
    print(f"\n📥 Downloading to: {download_path}")
    print(f"🎵 Format: {selected_format['name']} | Quality: {quality}{'k' if fmt != 'flac' else ''}")
    print(f"📊 Files: {len(indices) if indices else 1}\n")
    
    # Download
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        if is_playlist and len(indices) > 1:
            for i, video_idx in enumerate(indices, 1):
                try:
                    video_url = info['entries'][video_idx]['url']
                    print(f"\n🎬 [{i}/{len(indices)}] Downloading: {info['entries'][video_idx].get('title', 'Unknown')}")
                    ydl.download([video_url])
                except Exception as e:
                    print(f"❌ Failed: {e}")
        else:
            ydl.download([url])
    
    print(f"\n✅ Download complete! Files saved to: {download_path}")

def progress_hook(d):
    """Display download progress"""
    if d['status'] == 'downloading':
        if 'total_bytes' in d:
            percent = d['downloaded_bytes'] / d['total_bytes'] * 100
            bar_length = 30
            filled = int(bar_length * percent // 100)
            bar = '█' * filled + '░' * (bar_length - filled)
            speed = d.get('speed', 0)
            speed_mb = speed / 1024 / 1024 if speed else 0
            print(f"\r📥 {bar} {percent:.1f}% | {speed_mb:.1f} MB/s", end='')
    elif d['status'] == 'finished':
        print(f"\n✅ Processing...")

def batch_download():
    """Batch download from text file"""
    print("\n" + "=" * 70)
    print("📦 BATCH DOWNLOAD MODE")
    print("=" * 70)
    
    file_path = input("\n📄 Enter path to URL list file (one URL per line): ").strip()
    
    if not os.path.exists(file_path):
        print("❌ File not found!")
        return
    
    with open(file_path, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]
    
    print(f"\n📊 Found {len(urls)} URLs")
    confirm = input("Start batch download? (y/n): ").lower()
    
    if confirm == 'y':
        for i, url in enumerate(urls, 1):
            print(f"\n{'='*70}")
            print(f"🎵 [{i}/{len(urls)}] Processing: {url}")
            print('='*70)
            # Temporarily override URL and call download function
            globals()['_temp_url'] = url
            download_audio()
    
    print("\n✅ Batch download complete!")

def search_and_download():
    """Search YouTube and download"""
    print("\n" + "=" * 70)
    print("🔍 SEARCH & DOWNLOAD")
    print("=" * 70)
    
    query = input("\n🔎 Search for: ").strip()
    if not query:
        return
    
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
        'default_search': 'ytsearch',
        'max_results': 10
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            results = ydl.extract_info(f"ytsearch10:{query}", download=False)
            
            print("\n📋 Search Results:")
            for i, entry in enumerate(results['entries'], 1):
                title = entry.get('title', 'Unknown')[:60]
                duration = entry.get('duration', 0)
                minutes = duration // 60
                seconds = duration % 60
                print(f"{i:2}. {title} [{minutes}:{seconds:02d}]")
            
            choice = input(f"\nSelect number (1-10) or 'a' for all: ").strip()
            
            if choice.lower() == 'a':
                for entry in results['entries']:
                    download_audio_single(entry['url'])
            elif choice.isdigit() and 1 <= int(choice) <= 10:
                selected = results['entries'][int(choice)-1]
                download_audio_single(selected['url'])
            else:
                print("❌ Invalid choice!")
        except Exception as e:
            print(f"❌ Search failed: {e}")

def download_audio_single(url):
    """Helper function to download single audio"""
    globals()['_temp_url'] = url
    download_audio()

def main():
    """Main menu"""
    while True:
        print("\n" + "=" * 70)
        print("🎵 PERFECT AUDIO DOWNLOADER v3.0")
        print("=" * 70)
        print("1. 🎵 Download Audio (Single/Playlist)")
        print("2. 🔍 Search & Download")
        print("3. 📦 Batch Download (from file)")
        print("4. ⚙️ Settings")
        print("5. ❌ Exit")
        
        choice = input("\n👉 Choose (1-5): ").strip()
        
        if choice == "1":
            download_audio()
        elif choice == "2":
            search_and_download()
        elif choice == "3":
            batch_download()
        elif choice == "4":
            print("\n⚙️ Settings coming soon!")
            input("Press Enter to continue...")
        elif choice == "5":
            print("\n👋 Goodbye! Thanks for using Perfect Audio Downloader!")
            break
        else:
            print("\n❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Download cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please report this issue.")
