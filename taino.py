# streamlit_youtube_downloader.py

import streamlit as st
import yt_dlp
import os
import tempfile
from pathlib import Path
import time

# Page configuration
st.set_page_config(
    page_title="YouTube Audio Downloader",
    page_icon="🎵",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF0000;
        text-align: center;
        margin-bottom: 1rem;
    }
    .success-message {
        padding: 1rem;
        background-color: #d4edda;
        color: #155724;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        background-color: #e7f3ff;
        border-left: 4px solid #2196F3;
        border-radius: 0.25rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">🎵 YouTube Audio Downloader</div>', unsafe_allow_html=True)

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Audio format selection
    audio_format = st.selectbox(
        "Audio Format",
        options=["mp3", "m4a", "webm", "aac", "flac", "wav"],
        help="Select the output audio format"
    )
    
    # Quality selection
    quality = st.select_slider(
        "Audio Quality (kbps)",
        options=["64", "128", "192", "256", "320", "best"],
        value="192",
        help="Higher quality = larger file size"
    )
    
    # Extract audio only option
    extract_audio = st.checkbox("Extract audio only", value=True, disabled=True)
    
    st.divider()
    
    # Information
    st.info("""
    **Supported Features:**
    - YouTube videos
    - YouTube Music
    - Playlists (coming soon)
    - High quality audio
    - Multiple formats
    """)
    
    st.warning("""
    ⚠️ **Legal Notice:**
    Only download content you have permission to download. Respect copyright laws.
    """)

# Main content area
url = st.text_input(
    "🔗 Enter YouTube URL",
    placeholder="https://www.youtube.com/watch?v=...",
    help="Paste any YouTube video URL here"
)

# Two columns for additional options
col1, col2 = st.columns(2)

with col1:
    custom_filename = st.text_input(
        "📝 Custom filename (optional)",
        placeholder="Leave empty to use video title"
    )

with col2:
    download_option = st.radio(
        "📥 Download option",
        options=["Download directly", "Get download link"],
        horizontal=True
    )

# Function to get video info
def get_video_info(url):
    """Extract video information without downloading"""
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info
    except Exception as e:
        return None

# Function to download audio
def download_audio(url, format_type, quality, custom_name=None):
    """Download audio from YouTube"""
    
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    
    # Set filename template
    if custom_name and custom_name.strip():
        filename_template = os.path.join(temp_dir, f"{custom_name.strip()}.%(ext)s")
    else:
        filename_template = os.path.join(temp_dir, "%(title)s.%(ext)s")
    
    # Configure yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': format_type,
            'preferredquality': quality if quality != 'best' else '192',
        }],
        'outtmpl': filename_template,
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'progress_hooks': [progress_hook],
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Download the audio
            info = ydl.extract_info(url, download=True)
            
            # Get the downloaded file path
            if custom_name and custom_name.strip():
                base_filename = custom_name.strip()
            else:
                base_filename = info.get('title', 'audio')
            
            # Find the downloaded file
            for file in os.listdir(temp_dir):
                if file.endswith(f".{format_type}"):
                    file_path = os.path.join(temp_dir, file)
                    return file_path, info
            return None, info
    except Exception as e:
        raise e

# Progress tracking
progress_bar = None
status_text = None

def progress_hook(d):
    """Update progress in Streamlit"""
    if d['status'] == 'downloading':
        if 'total_bytes' in d:
            percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
            if progress_bar:
                progress_bar.progress(percent / 100)
                status_text.text(f"Downloading: {percent:.1f}%")
        elif 'total_bytes_estimate' in d:
            percent = (d['downloaded_bytes'] / d['total_bytes_estimate']) * 100
            if progress_bar:
                progress_bar.progress(percent / 100)
                status_text.text(f"Downloading: {percent:.1f}%")
    elif d['status'] == 'finished':
        if status_text:
            status_text.text("Processing audio...")

# Download button
if st.button("🎵 Download Audio", type="primary", use_container_width=True):
    if not url:
        st.error("❌ Please enter a YouTube URL")
    else:
        # Check if URL is valid
        if not ('youtube.com/watch' in url or 'youtu.be/' in url or 'youtube.com/playlist' in url):
            st.warning("⚠️ Please enter a valid YouTube URL")
        else:
            # Get video info first
            with st.spinner("Fetching video information..."):
                video_info = get_video_info(url)
                
                if video_info:
                    # Display video information
                    col1, col2, col3 = st.columns([1, 2, 1])
                    
                    with col1:
                        if 'thumbnail' in video_info:
                            st.image(video_info['thumbnail'], use_column_width=True)
                    
                    with col2:
                        st.markdown(f"**Title:** {video_info.get('title', 'N/A')}")
                        st.markdown(f"**Channel:** {video_info.get('uploader', 'N/A')}")
                        st.markdown(f"**Duration:** {video_info.get('duration_string', 'N/A')}")
                        st.markdown(f"**Format:** {audio_format.upper()}")
                        st.markdown(f"**Quality:** {quality} kbps")
                    
                    # Confirm download
                    if st.button("✅ Confirm Download", use_container_width=True):
                        # Progress indicators
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        status_text.text("Starting download...")
                        
                        try:
                            # Download the audio
                            file_path, info = download_audio(
                                url, 
                                audio_format, 
                                quality,
                                custom_filename
                            )
                            
                            if file_path and os.path.exists(file_path):
                                progress_bar.progress(1.0)
                                status_text.text("Download complete!")
                                
                                # Read the file
                                with open(file_path, 'rb') as f:
                                    audio_bytes = f.read()
                                
                                # Create filename
                                if custom_filename:
                                    filename = f"{custom_filename}.{audio_format}"
                                else:
                                    filename = f"{info.get('title', 'audio')}.{audio_format}"
                                
                                # Remove invalid characters from filename
                                filename = "".join(c for c in filename if c.isalnum() or c in ' ._-')
                                
                                # Success message
                                st.markdown(f"""
                                <div class="success-message">
                                    ✅ Download successful!<br>
                                    File size: {len(audio_bytes) / (1024*1024):.2f} MB
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Provide download button
                                st.download_button(
                                    label="📥 Click to save audio file",
                                    data=audio_bytes,
                                    file_name=filename,
                                    mime=f"audio/{audio_format}",
                                    use_container_width=True
                                )
                                
                                # Clean up
                                os.remove(file_path)
                                os.rmdir(os.path.dirname(file_path))
                            else:
                                st.error("❌ Failed to download audio file")
                                
                        except Exception as e:
                            st.error(f"❌ Download failed: {str(e)}")
                            st.info("Try a different video or check your internet connection")
                else:
                    st.error("❌ Failed to fetch video information. Please check the URL and try again.")

# Additional features section
st.divider()
st.subheader("🎯 Tips & Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **🎵 Supported Formats**
    - MP3 (most compatible)
    - M4A (Apple)
    - FLAC (Lossless)
    - WAV (Uncompressed)
    - AAC (High quality)
    """)

with col2:
    st.markdown("""
    **⚡ Quality Options**
    - Best (variable)
    - 320 kbps (highest)
    - 192 kbps (good balance)
    - 128 kbps (small file)
    """)

with col3:
    st.markdown("""
    **📝 Pro Tips**
    - Use custom filenames
    - Check video length first
    - Stable internet required
    - Max file size: 200MB
    """)

# Footer
st.divider()
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 0.8rem;'>"
    "Built with Streamlit & yt-dlp | For personal use only"
    "</div>",
    unsafe_allow_html=True
)
