"""
Auto-install all requirements for Audio Downloader
Run: python install_requirements.py
"""

import subprocess
import sys
import platform

def install_requirements():
    print("=" * 60)
    print("📦 Installing Audio Downloader Requirements")
    print("=" * 60)
    
    # Install yt-dlp
    print("\n1️⃣ Installing yt-dlp...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"])
    
    # Check FFmpeg
    print("\n2️⃣ Checking FFmpeg...")
    
    system = platform.system()
    
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        print("✅ FFmpeg is already installed!")
    except:
        print("⚠️ FFmpeg not found!")
        
        if system == "Windows":
            print("\n📥 To install FFmpeg on Windows:")
            print("   1. Download from: https://github.com/BtbN/FFmpeg-Builds/releases")
            print("   2. Extract to C:\\ffmpeg")
            print("   3. Add C:\\ffmpeg\\bin to System PATH")
            print("   4. Restart command prompt")
            
        elif system == "Darwin":  # macOS
            print("\n📥 Install FFmpeg on macOS:")
            print("   Run: brew install ffmpeg")
            print("   (Install Homebrew first if needed: /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\")")
            
        elif system == "Linux":
            print("\n📥 Install FFmpeg on Linux:")
            print("   Ubuntu/Debian: sudo apt-get install ffmpeg")
            print("   Fedora: sudo dnf install ffmpeg")
            print("   Arch: sudo pacman -S ffmpeg")
    
    print("\n" + "=" * 60)
    print("✅ Installation complete!")
    print("=" * 60)

if __name__ == "__main__":
    install_requirements()
