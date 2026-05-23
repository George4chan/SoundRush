"""
Music Downloader - Streamlit Web Version
Python: 3.8, 3.9, 3.10, 3.11, 3.12
"""

import streamlit as st
import os
import yt_dlp
from pathlib import Path
import tempfile
import base64
from io import BytesIO
import time

# Page config
st.set_page_config(
    page_title="🎵 Music Downloader",
    page_icon="🎵",
    layout="centered"
)

# Title
st.title("🎵 Music Downloader Pro")
st.markdown("Download high-quality music from YouTube")

# Sidebar settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    quality = st.selectbox(
        "Audio Quality",
        ["128", "192", "256", "320"],
        index=1
    )
    
    format_type = st.selectbox(
        "Output Format",
        ["mp3", "m4a", "wav", "flac", "opus"],
        index=0
    )
    
    st.divider()
    st.markdown("### 📋 Requirements")
    st.markdown("- Python 3.8+")
    st.markdown("- FFmpeg installed")
    st.markdown("- Internet connection")

# Main interface
url = st.text_input(
    "Enter YouTube URL",
    placeholder="https://www.youtube.com/watch?v=..."
)

# Download button
if st.button("⬇️ Download Music", type="primary", use_container_width=True):
    if not url:
        st.error("❌ Please enter a valid URL")
    else:
        try:
            # Create temp directory
            with tempfile.TemporaryDirectory() as temp_dir:
                # Progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                def progress_hook(d):
                    if d['status'] == 'downloading':
                        try:
                            if 'total_bytes' in d and d['total_bytes']:
                                percent = d['downloaded_bytes'] / d['total_bytes']
                                progress_bar.progress(min(percent, 1.0))
                                status_text.text(f"Downloading... {percent*100:.1f}%")
                        except:
                            pass
                    elif d['status'] == 'finished':
                        progress_bar.progress(1.0)
                        status_text.text("Processing audio...")
                
                # yt-dlp options
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': format_type,
                        'preferredquality': quality,
                    }],
                    'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                    'progress_hooks': [progress_hook],
                    'quiet': True,
                    'no_warnings': True,
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # Get info
                    status_text.text("Fetching video information...")
                    info = ydl.extract_info(url, download=False)
                    title = info.get('title', 'Unknown')
                    duration = info.get('duration', 0)
                    
                    # Show info
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Title:** {title}")
                    with col2:
                        mins = duration // 60
                        secs = duration % 60
                        st.write(f"**Duration:** {mins}:{secs:02d}")
                    
                    # Download
                    status_text.text("Downloading...")
                    ydl.download([url])
                    
                    # Find downloaded file
                    downloaded_files = os.listdir(temp_dir)
                    if downloaded_files:
                        file_path = os.path.join(temp_dir, downloaded_files[0])
                        
                        # Read file
                        with open(file_path, 'rb') as f:
                            audio_bytes = f.read()
                        
                        # Create download button
                        status_text.text("✅ Download complete!")
                        st.success(f"✅ Successfully downloaded: {title}")
                        
                        # Download button
                        st.download_button(
                            label="📥 Click to Save File",
                            data=audio_bytes,
                            file_name=f"{title}.{format_type}",
                            mime=f"audio/{format_type}",
                            use_container_width=True
                        )
                        
                        # Audio player
                        st.audio(audio_bytes, format=f"audio/{format_type}")
                        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("💡 Make sure the URL is valid and the video is available")

# Footer
st.divider()
st.markdown("""
### 📝 Instructions
1. Paste a YouTube URL in the input field
2. Select audio quality and format in the sidebar
3. Click "Download Music"
4. Click "Click to Save File" to download

### ⚠️ Legal Notice
Only download content you have permission to download.
Respect copyright laws in your country.
""")

# Version info
st.caption("Music Downloader Pro v1.0 | Python 3.8+ | Streamlit")
