"""
PROFESSIONAL AUDIO DOWNLOADER v4.0
Enterprise-grade audio download solution
Save as: professional_audio_downloader.py
Run: python professional_audio_downloader.py
"""

import os
import sys
import json
import time
import threading
import queue
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import subprocess

# Auto-install dependencies
def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", package])

try:
    import yt_dlp
except ImportError:
    print("📦 Installing yt-dlp...")
    install_package("yt-dlp")
    import yt_dlp

try:
    from tqdm import tqdm
except ImportError:
    install_package("tqdm")
    from tqdm import tqdm

try:
    import colorama
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    install_package("colorama")
    import colorama
    from colorama import Fore, Style, init
    init(autoreset=True)

class AudioDownloaderConfig:
    """Configuration management for the downloader"""
    
    CONFIG_FILE = Path.home() / ".audio_downloader_config.json"
    
    DEFAULT_CONFIG = {
        "default_download_path": str(Path.home() / "Music" / "Downloads"),
        "default_format": "mp3",
        "default_quality": "192",
        "max_concurrent_downloads": 3,
        "retry_attempts": 3,
        "timeout_seconds": 300,
        "embed_metadata": True,
        "embed_thumbnail": True,
        "create_playlist_folder": True,
        "keep_original_files": False,
        "proxy_settings": None,
        "cookies_file": None,
        "log_level": "INFO"
    }
    
    @classmethod
    def load(cls) -> Dict:
        """Load configuration from file"""
        if cls.CONFIG_FILE.exists():
            with open(cls.CONFIG_FILE, 'r') as f:
                config = json.load(f)
                # Merge with defaults for new keys
                for key, value in cls.DEFAULT_CONFIG.items():
                    if key not in config:
                        config[key] = value
                return config
        return cls.DEFAULT_CONFIG.copy()
    
    @classmethod
    def save(cls, config: Dict):
        """Save configuration to file"""
        with open(cls.CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)

class DownloadQueue:
    """Manage concurrent downloads"""
    
    def __init__(self, max_concurrent: int = 3):
        self.queue = queue.Queue()
        self.active_downloads = []
        self.completed_downloads = []
        self.failed_downloads = []
        self.max_concurrent = max_concurrent
        self.lock = threading.Lock()
    
    def add(self, item: Dict):
        """Add item to download queue"""
        self.queue.put(item)
    
    def get_progress(self) -> Dict:
        """Get current progress statistics"""
        with self.lock:
            return {
                "queued": self.queue.qsize(),
                "active": len(self.active_downloads),
                "completed": len(self.completed_downloads),
                "failed": len(self.failed_downloads)
            }

class ProfessionalAudioDownloader:
    """Main downloader class with professional features"""
    
    def __init__(self):
        self.config = AudioDownloaderConfig.load()
        self.download_queue = DownloadQueue(self.config["max_concurrent_downloads"])
        self.setup_directories()
        self.setup_logging()
        
    def setup_directories(self):
        """Create necessary directories"""
        self.download_path = Path(self.config["default_download_path"])
        self.download_path.mkdir(parents=True, exist_ok=True)
        
        self.temp_path = self.download_path / ".temp"
        self.temp_path.mkdir(exist_ok=True)
        
        self.logs_path = self.download_path / ".logs"
        self.logs_path.mkdir(exist_ok=True)
    
    def setup_logging(self):
        """Setup logging system"""
        from logging import getLogger, FileHandler, StreamHandler, Formatter, INFO
        
        self.logger = getLogger("AudioDownloader")
        self.logger.setLevel(INFO)
        
        # File handler
        log_file = self.logs_path / f"downloader_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = FileHandler(log_file)
        file_handler.setFormatter(Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(file_handler)
        
        # Console handler
        console_handler = StreamHandler()
        console_handler.setFormatter(Formatter('%(message)s'))
        self.logger.addHandler(console_handler)
    
    def display_banner(self):
        """Display professional banner"""
        print(Fore.CYAN + "=" * 70)
        print(Fore.YELLOW + """
   ╔══════════════════════════════════════════════════════════════╗
   ║     PROFESSIONAL AUDIO DOWNLOADER v4.0 - Enterprise Grade    ║
   ║            High Quality Audio Extraction System              ║
   ╚══════════════════════════════════════════════════════════════╝
        """)
        print(Fore.CYAN + "=" * 70)
        print(Fore.WHITE + f"📁 Download Path: {self.download_path}")
        print(Fore.WHITE + f"🎵 Default Format: {self.config['default_format'].upper()}")
        print(Fore.WHITE + f"⚡ Max Concurrent: {self.config['max_concurrent_downloads']}")
        print(Fore.CYAN + "=" * 70)
    
    def get_video_info(self, url: str) -> Optional[Dict]:
        """Extract video information without downloading"""
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return info
        except Exception as e:
            self.logger.error(f"Failed to extract info: {e}")
            return None
    
    def select_format(self) -> Tuple[str, str, str]:
        """Interactive format selection with recommendations"""
        print(Fore.GREEN + "\n🎵 AUDIO FORMAT SELECTION")
        print(Fore.WHITE + "-" * 40)
        
        formats = {
            "1": {"codec": "mp3", "name": "MP3", "quality": "192", "desc": "Universal compatibility", "bitrate": "32-320k"},
            "2": {"codec": "m4a", "name": "M4A", "quality": "256", "desc": "Apple optimized", "bitrate": "64-256k"},
            "3": {"codec": "flac", "name": "FLAC", "quality": "0", "desc": "Lossless (studio quality)", "bitrate": "900-1200k"},
            "4": {"codec": "wav", "name": "WAV", "quality": "0", "desc": "Uncompressed PCM", "bitrate": "1411k"},
            "5": {"codec": "opus", "name": "OPUS", "quality": "128", "desc": "Modern compression", "bitrate": "64-160k"},
            "6": {"codec": "aac", "name": "AAC", "quality": "192", "desc": "Advanced coding", "bitrate": "96-320k"},
            "7": {"codec": "alac", "name": "ALAC", "quality": "0", "desc": "Apple Lossless", "bitrate": "800-1000k"}
        }
        
        for key, fmt in formats.items():
            print(Fore.WHITE + f"  {key}. {fmt['name']:4} - {fmt['desc']:<25} [{fmt['bitrate']}]")
        
        choice = input(Fore.YELLOW + f"\n👉 Select format [1-7] (default: {self.config['default_format']}): ").strip()
        if not choice:
            choice = next(k for k, v in formats.items() if v['codec'] == self.config['default_format'])
        
        selected = formats.get(choice, formats["1"])
        
        # Quality selection for lossy formats
        if selected["codec"] not in ["flac", "wav", "alac"]:
            print(Fore.GREEN + f"\n🎚️ QUALITY SETTINGS - {selected['name']}")
            print(Fore.WHITE + "-" * 40)
            
            if selected["codec"] == "opus":
                qualities = {"1": "64", "2": "96", "3": "128", "4": "160"}
                print("  1. 64k  - Podcast/Spoken word (small file)")
                print("  2. 96k  - Good for casual listening")
                print("  3. 128k - Best balance (RECOMMENDED)")
                print("  4. 160k - Premium quality")
                default = "3"
            else:
                qualities = {"1": "128", "2": "192", "3": "256", "4": "320"}
                print("  1. 128k - Standard quality")
                print("  2. 192k - High quality")
                print("  3. 256k - Very high quality (RECOMMENDED)")
                print("  4. 320k - Maximum quality")
                default = "3"
            
            q_choice = input(Fore.YELLOW + f"\n👉 Select quality [1-{len(qualities)}] (default: {default}): ").strip()
            if not q_choice:
                q_choice = default
            quality = qualities.get(q_choice, qualities[default])
        else:
            quality = "0"  # Lossless
        
        return selected["codec"], quality, selected["name"]
    
    def download_with_progress(self, url: str, output_path: Path, format_codec: str, quality: str):
        """Download with progress bar"""
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': format_codec,
                'preferredquality': quality,
            }],
            'outtmpl': str(output_path / '%(title)s.%(ext)s'),
            'progress_hooks': [self.progress_hook],
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'retries': self.config["retry_attempts"],
            'continuedl': True,
            'ignoreerrors': False,
            'nooverwrites': False,
        }
        
        # Add metadata embedding
        if self.config["embed_metadata"]:
            ydl_opts['postprocessors'].append({
                'key': 'FFmpegMetadata',
                'add_metadata': True,
            })
        
        # Add thumbnail embedding
        if self.config["embed_thumbnail"] and format_codec in ['mp3', 'm4a']:
            ydl_opts['postprocessors'].append({
                'key': 'EmbedThumbnail',
                'already_have_thumbnail': False,
            })
        
        # Add cookies if provided
        if self.config["cookies_file"]:
            ydl_opts['cookiefile'] = self.config["cookies_file"]
        
        # Add proxy if provided
        if self.config["proxy_settings"]:
            ydl_opts['proxy'] = self.config["proxy_settings"]
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                self.logger.info(f"✅ Downloaded: {info.get('title', 'Unknown')}")
                return True, info.get('title', 'Unknown')
        except Exception as e:
            self.logger.error(f"❌ Failed: {e}")
            return False, None
    
    def progress_hook(self, d):
        """Progress hook for download status"""
        if d['status'] == 'downloading':
            if 'total_bytes' in d:
                percent = d['downloaded_bytes'] / d['total_bytes'] * 100
                bar_length = 40
                filled = int(bar_length * percent // 100)
                bar = '█' * filled + '░' * (bar_length - filled)
                speed = d.get('speed', 0)
                speed_mb = speed / 1024 / 1024 if speed else 0
                eta = d.get('eta', 0)
                
                print(Fore.CYAN + f"\r   {bar} {percent:.1f}% | {speed_mb:.1f} MB/s | ETA: {eta}s", end='')
        elif d['status'] == 'finished':
            print(Fore.GREEN + f"\r   ✅ Processing audio...", end='')
    
    def download_single(self, url: str):
        """Download single audio file"""
        print(Fore.GREEN + "\n🔍 ANALYZING URL...")
        
        # Get video info
        info = self.get_video_info(url)
        if not info:
            print(Fore.RED + "❌ Failed to fetch video information")
            return
        
        # Display video info
        print(Fore.WHITE + "\n📋 VIDEO INFORMATION")
        print(Fore.CYAN + "-" * 40)
        print(Fore.WHITE + f"🎬 Title: {info.get('title', 'Unknown')}")
        print(Fore.WHITE + f"⏱️  Duration: {info.get('duration', 0) // 60}:{info.get('duration', 0) % 60:02d}")
        print(Fore.WHITE + f"👤 Uploader: {info.get('uploader', 'Unknown')}")
        print(Fore.WHITE + f"📅 Date: {info.get('upload_date', 'Unknown')}")
        print(Fore.WHITE + f"👍 Views: {info.get('view_count', 0):,}")
        print(Fore.CYAN + "-" * 40)
        
        # Select format
        format_codec, quality, format_name = self.select_format()
        
        # Confirm download
        print(Fore.YELLOW + f"\n📥 Ready to download:")
        print(Fore.WHITE + f"   Format: {format_name.upper()}")
        print(Fore.WHITE + f"   Quality: {quality}{'k' if format_codec not in ['flac','wav','alac'] else ' (Lossless)'}")
        print(Fore.WHITE + f"   Location: {self.download_path}")
        
        confirm = input(Fore.GREEN + "\n👉 Start download? (y/n): ").lower()
        if confirm != 'y':
            print(Fore.YELLOW + "Download cancelled")
            return
        
        # Download
        print(Fore.GREEN + "\n🚀 DOWNLOADING...")
        success, title = self.download_with_progress(url, self.download_path, format_codec, quality)
        
        if success:
            print(Fore.GREEN + f"\n✅ SUCCESS! Downloaded: {title}")
            self.logger.info(f"Downloaded: {title}")
        else:
            print(Fore.RED + f"\n❌ FAILED to download: {url}")
    
    def download_playlist(self, url: str):
        """Download entire playlist"""
        print(Fore.GREEN + "\n🔍 ANALYZING PLAYLIST...")
        
        info = self.get_video_info(url)
        if not info or 'entries' not in info:
            print(Fore.RED + "❌ No playlist found")
            return
        
        entries = info['entries']
        total = len(entries)
        
        print(Fore.WHITE + f"\n📋 PLAYLIST INFORMATION")
        print(Fore.CYAN + "-" * 40)
        print(Fore.WHITE + f"📝 Title: {info.get('title', 'Unknown')}")
        print(Fore.WHITE + f"🎵 Total videos: {total}")
        print(Fore.WHITE + f"👤 Uploader: {info.get('uploader', 'Unknown')}")
        print(Fore.CYAN + "-" * 40)
        
        # Select format once for all videos
        format_codec, quality, format_name = self.select_format()
        
        # Range selection
        print(Fore.GREEN + "\n📊 DOWNLOAD RANGE OPTIONS")
        print(Fore.WHITE + "  1. Download all videos")
        print(Fore.WHITE + "  2. Download range (e.g., 1-10)")
        print(Fore.WHITE + "  3. Download specific (e.g., 1,3,5,7)")
        
        range_choice = input(Fore.YELLOW + "\n👉 Select option: ").strip()
        
        if range_choice == "2":
            range_str = input(Fore.YELLOW + "Enter range (e.g., 1-10): ").strip()
            start, end = map(int, range_str.split('-'))
            indices = range(start-1, min(end, total))
        elif range_choice == "3":
            range_str = input(Fore.YELLOW + "Enter numbers (e.g., 1,3,5): ").strip()
            indices = [int(x)-1 for x in range_str.split(',') if 1 <= int(x) <= total]
        else:
            indices = range(total)
        
        indices = list(indices)
        
        print(Fore.YELLOW + f"\n📊 Will download {len(indices)} videos")
        confirm = input(Fore.GREEN + "👉 Start download? (y/n): ").lower()
        
        if confirm != 'y':
            print(Fore.YELLOW + "Download cancelled")
            return
        
        # Create playlist folder
        if self.config["create_playlist_folder"]:
            playlist_name = "".join(c for c in info.get('title', 'Playlist') if c.isalnum() or c in ' ._-')
            download_folder = self.download_path / playlist_name
            download_folder.mkdir(exist_ok=True)
        else:
            download_folder = self.download_path
        
        # Download each video
        success_count = 0
        for i, idx in enumerate(indices, 1):
            print(Fore.CYAN + f"\n{'='*50}")
            print(Fore.WHITE + f"📥 [{i}/{len(indices)}] Processing: {entries[idx].get('title', 'Unknown')[:50]}")
            print(Fore.CYAN + "=" * 50)
            
            video_url = entries[idx].get('webpage_url')
            if video_url:
                success, title = self.download_with_progress(video_url, download_folder, format_codec, quality)
                if success:
                    success_count += 1
            
            time.sleep(1)  # Rate limiting
        
        print(Fore.GREEN + f"\n✅ PLAYLIST DOWNLOAD COMPLETE!")
        print(Fore.WHITE + f"📊 Success: {success_count}/{len(indices)}")
    
    def search_and_download(self):
        """Search YouTube and download"""
        print(Fore.GREEN + "\n🔍 SEARCH MODE")
        print(Fore.WHITE + "-" * 40)
        
        query = input(Fore.YELLOW + "👉 Search for: ").strip()
        if not query:
            return
        
        # Search
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
            'default_search': 'ytsearch',
            'max_results': 15
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                results = ydl.extract_info(f"ytsearch15:{query}", download=False)
                
                print(Fore.GREEN + f"\n📋 SEARCH RESULTS")
                print(Fore.CYAN + "-" * 70)
                
                for i, entry in enumerate(results['entries'], 1):
                    title = entry.get('title', 'Unknown')[:60]
                    duration = entry.get('duration', 0)
                    minutes = duration // 60
                    seconds = duration % 60
                    uploader = entry.get('uploader', 'Unknown')[:20]
                    
                    print(Fore.WHITE + f"{i:2}. {Fore.CYAN}{title:<60} {Fore.YELLOW}[{minutes:02d}:{seconds:02d}]")
                    print(Fore.WHITE + f"    👤 {uploader}")
                
                print(Fore.CYAN + "-" * 70)
                choice = input(Fore.YELLOW + f"\n👉 Select video (1-15) or 'a' for all, 'c' to cancel: ").strip()
                
                if choice.lower() == 'a':
                    for entry in results['entries']:
                        self.download_single(entry.get('webpage_url'))
                elif choice.isdigit() and 1 <= int(choice) <= 15:
                    selected = results['entries'][int(choice)-1]
                    self.download_single(selected.get('webpage_url'))
                else:
                    print(Fore.YELLOW + "Cancelled")
                    
            except Exception as e:
                self.logger.error(f"Search failed: {e}")
                print(Fore.RED + f"❌ Search failed: {e}")
    
    def batch_download_from_file(self):
        """Batch download from text file"""
        print(Fore.GREEN + "\n📦 BATCH DOWNLOAD MODE")
        print(Fore.WHITE + "-" * 40)
        
        file_path = input(Fore.YELLOW + "👉 Enter path to URL list file: ").strip()
        
        if not os.path.exists(file_path):
            print(Fore.RED + "❌ File not found")
            return
        
        with open(file_path, 'r') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        if not urls:
            print(Fore.RED + "❌ No URLs found in file")
            return
        
        print(Fore.GREEN + f"\n📊 Found {len(urls)} URLs")
        
        # Select format once for all
        format_codec, quality, format_name = self.select_format()
        
        confirm = input(Fore.YELLOW + f"\n👉 Download {len(urls)} files? (y/n): ").lower()
        if confirm != 'y':
            return
        
        success_count = 0
        for i, url in enumerate(urls, 1):
            print(Fore.CYAN + f"\n{'='*50}")
            print(Fore.WHITE + f"📥 [{i}/{len(urls)}] URL: {url[:80]}")
            print(Fore.CYAN + "=" * 50)
            
            success, title = self.download_with_progress(url, self.download_path, format_codec, quality)
            if success:
                success_count += 1
            
            time.sleep(0.5)
        
        print(Fore.GREEN + f"\n✅ BATCH DOWNLOAD COMPLETE!")
        print(Fore.WHITE + f"📊 Success: {success_count}/{len(urls)}")
    
    def show_settings(self):
        """Display and modify settings"""
        print(Fore.GREEN + "\n⚙️ SETTINGS")
        print(Fore.CYAN + "-" * 40)
        
        for key, value in self.config.items():
            if key not in ["proxy_settings", "cookies_file"]:
                print(Fore.WHITE + f"  {key.replace('_', ' ').title()}: {value}")
        
        print(Fore.YELLOW + "\n  To modify settings, edit config file:")
        print(Fore.WHITE + f"  {AudioDownloaderConfig.CONFIG_FILE}")
        
        input(Fore.GREEN + "\n👉 Press Enter to continue...")
    
    def run(self):
        """Main application loop"""
        self.display_banner()
        
        while True:
            print(Fore.GREEN + "\n" + "=" * 70)
            print(Fore.YELLOW + "MAIN MENU")
            print(Fore.GREEN + "=" * 70)
            print(Fore.WHITE + """
  1. 🎵 Download Single Audio
  2. 📋 Download Playlist
  3. 🔍 Search & Download
  4. 📦 Batch Download (from file)
  5. ⚙️  Settings
  6. ℹ️  About
  7. 🚪 Exit
            """)
            print(Fore.GREEN + "=" * 70)
            
            choice = input(Fore.YELLOW + "👉 Select option (1-7): ").strip()
            
            if choice == "1":
                url = input(Fore.YELLOW + "🔗 Enter URL: ").strip()
                if url:
                    self.download_single(url)
                else:
                    print(Fore.RED + "❌ No URL provided")
            
            elif choice == "2":
                url = input(Fore.YELLOW + "🔗 Enter playlist URL: ").strip()
                if url:
                    self.download_playlist(url)
                else:
                    print(Fore.RED + "❌ No URL provided")
            
            elif choice == "3":
                self.search_and_download()
            
            elif choice == "4":
                self.batch_download_from_file()
            
            elif choice == "5":
                self.show_settings()
            
            elif choice == "6":
                print(Fore.CYAN + """
╔══════════════════════════════════════════════════════════════╗
║                    PROFESSIONAL AUDIO DOWNLOADER              ║
║                          Version 4.0                          ║
╠══════════════════════════════════════════════════════════════╣
║  Features:                                                   ║
║  ✓ High-quality audio extraction (up to 320kbps/FLAC)       ║
║  ✓ Batch processing & queue management                      ║
║  ✓ Playlist support with smart organization                 ║
║  ✓ Metadata & thumbnail embedding                           ║
║  ✓ Resume interrupted downloads                             ║
║  ✓ Multi-format support (MP3, FLAC, WAV, M4A, OPUS, AAC)   ║
║  ✓ Professional logging system                              ║
║  ✓ Configurable settings                                    ║
╠══════════════════════════════════════════════════════════════╣
║  Supported: YouTube, SoundCloud, Vimeo, and 1000+ sites     ║
╚══════════════════════════════════════════════════════════════╝
                """)
                input(Fore.GREEN + "Press Enter to continue...")
            
            elif choice == "7":
                print(Fore.GREEN + "\n👋 Thank you for using Professional Audio Downloader!")
                print(Fore.WHITE + f"📊 Logs saved to: {self.logs_path}")
                sys.exit(0)
            
            else:
                print(Fore.RED + "❌ Invalid option")

def main():
    """Main entry point"""
    try:
        downloader = ProfessionalAudioDownloader()
        downloader.run()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n⚠️ Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(Fore.RED + f"\n❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
