"""
🎵 Music & Video Downloader - Complete Web Version
Python: 3.8, 3.9, 3.10, 3.11, 3.12
Supports: MP3, M4A, WAV, FLAC, OPUS (Audio) | MP4 (Video)
"""

import streamlit as st
import os
import yt_dlp
import tempfile
import base64
from datetime import timedelta
import time

# Page config
st.set_page_config(
    page_title="🎵 Music & Video Downloader",
    page_icon="🎵",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    h1 {
        font-family: 'Poppins', sans-serif !important;
        font-size: 3rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #FFD700, #FFA500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
    }
    
    .logo-container {
        text-align: center;
        margin: 20px 0;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #FF6B6B, #FF8E53) !important;
        color: white !important;
        font-size: 1.4rem !important;
        font-weight: 700 !important;
        padding: 1.2rem 2.5rem !important;
        border-radius: 50px !important;
        border: none !important;
        box-shadow: 0 10px 30px rgba(255, 107, 107, 0.4) !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 15px 40px rgba(255, 107, 107, 0.6) !important;
    }
    
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 2px solid #FFD700 !important;
        border-radius: 25px !important;
        padding: 15px 20px !important;
        font-size: 1.1rem !important;
    }
    
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #FFD700, #FFA500, #FF6B6B) !important;
        border-radius: 10px !important;
    }
    
    .info-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .stDownloadButton > button {
        background: linear-gradient(135deg, #4CAF50, #45a049) !important;
        color: white !important;
        border-radius: 30px !important;
        padding: 1rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        border: none !important;
        box-shadow: 0 8px 25px rgba(76, 175, 80, 0.4) !important;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 8px 25px rgba(76, 175, 80, 0.4); }
        50% { box-shadow: 0 8px 40px rgba(76, 175, 80, 0.8); }
        100% { box-shadow: 0 8px 25px rgba(76, 175, 80, 0.4); }
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 35px rgba(76, 175, 80, 0.6) !important;
    }
    
    .footer {
        text-align: center;
        color: white;
        opacity: 0.7;
        margin-top: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: white !important;
        font-size: 1.1rem !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #FF6B6B, #FF8E53) !important;
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# Logo
st.markdown("""
<div class="logo-container">
    <div style="font-size: 5rem; text-align: center;">
        🎵🎀🎵
    </div>
</div>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1>🎵 Music & Video Downloader 🎵</h1>", unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: white; font-size: 1.2rem;">Download Audio & Video (MP4) 💖</p>', unsafe_allow_html=True)

# Session state to store downloaded file
if 'download_file' not in st.session_state:
    st.session_state.download_file = None
    st.session_state.download_filename = None
    st.session_state.download_mime = None

# Tabs
tab1, tab2 = st.tabs(["🎵 Audio Download", "🎬 Video Download (MP4)"])

with tab1:
    st.markdown("### 🎧 Download Audio Files")
    
    col1, col2 = st.columns(2)
    with col1:
        audio_quality = st.selectbox(
            "Audio Quality",
            ["128 kbps", "192 kbps", "256 kbps", "320 kbps"],
            key="audio_quality"
        )
    with col2:
        audio_format = st.selectbox(
            "Audio Format",
            ["mp3", "m4a", "wav", "flac", "opus"],
            key="audio_format"
        )
    
    audio_url = st.text_input(
        "Enter URL for Audio",
        placeholder="🔗 https://www.youtube.com/watch?v=...",
        key="audio_url"
    )
    
    if st.button("🎵 Download Audio 🎵", use_container_width=True, key="audio_btn"):
        if not audio_url:
            st.error("❌ Please enter a URL first!")
        else:
            try:
                with tempfile.TemporaryDirectory() as temp_dir:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    status_text.text("Starting download...")
                    
                    def progress_hook(d):
                        if d['status'] == 'downloading':
                            try:
                                if 'total_bytes' in d and d['total_bytes'] and d['total_bytes'] > 0:
                                    percent = d['downloaded_bytes'] / d['total_bytes']
                                    progress_bar.progress(min(percent, 1.0))
                                    status_text.text(f"Downloading... {percent*100:.1f}%")
                            except:
                                pass
                        elif d['status'] == 'finished':
                            progress_bar.progress(1.0)
                            status_text.text("Processing audio... Please wait")
                    
                    quality_val = audio_quality.replace(" kbps", "")
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': audio_format,
                            'preferredquality': quality_val,
                        }],
                        'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                        'progress_hooks': [progress_hook],
                        'quiet': True,
                        'no_warnings': True,
                    }
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(audio_url, download=False)
                        title = info.get('title', 'Unknown')
                        duration = info.get('duration', 0)
                        
                        st.info(f"🎵 **Title:** {title}")
                        st.info(f"⏱️ **Duration:** {timedelta(seconds=duration)}")
                        
                        ydl.download([audio_url])
                        
                        files = [f for f in os.listdir(temp_dir) if f.endswith(audio_format)]
                        if files:
                            file_path = os.path.join(temp_dir, files[0])
                            size_mb = os.path.getsize(file_path) / (1024*1024)
                            
                            with open(file_path, 'rb') as f:
                                file_data = f.read()
                            
                            st.balloons()
                            st.success(f"✅ Downloaded Successfully!")
                            st.info(f"📦 Size: {size_mb:.1f} MB | 🎧 {audio_format.upper()} | 🔊 {audio_quality}")
                            
                            # Download button
                            st.download_button(
                                label=f"💝 Click Here to Download - {title[:50]}.{audio_format} 💝",
                                data=file_data,
                                file_name=f"{title}.{audio_format}",
                                mime=f"audio/{audio_format}",
                                use_container_width=True,
                                key="audio_download"
                            )
                            
                            st.audio(file_data, format=f"audio/{audio_format}")
                        else:
                            st.error("No file found after download")
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Make sure the URL is valid")

with tab2:
    st.markdown("### 🎬 Download Video Files (MP4)")
    
    col1, col2 = st.columns(2)
    with col1:
        video_quality = st.selectbox(
            "Video Quality",
            ["Best Available", "1080p", "720p", "480p", "360p"],
            key="video_quality"
        )
    with col2:
        st.markdown("📹 **Format: MP4**")
    
    video_url = st.text_input(
        "Enter URL for Video",
        placeholder="🔗 https://www.youtube.com/watch?v=...",
        key="video_url"
    )
    
    if st.button("🎬 Download Video (MP4) 🎬", use_container_width=True, key="video_btn"):
        if not video_url:
            st.error("❌ Please enter a URL first!")
        else:
            try:
                with tempfile.TemporaryDirectory() as temp_dir:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    status_text.text("Starting video download...")
                    
                    def progress_hook(d):
                        if d['status'] == 'downloading':
                            try:
                                if 'total_bytes' in d and d['total_bytes'] and d['total_bytes'] > 0:
                                    percent = d['downloaded_bytes'] / d['total_bytes']
                                    progress_bar.progress(min(percent, 1.0))
                                    status_text.text(f"Downloading... {percent*100:.1f}%")
                            except:
                                pass
                        elif d['status'] == 'finished':
                            progress_bar.progress(1.0)
                            status_text.text("Processing video... Please wait")
                    
                    if video_quality == "Best Available":
                        format_str = 'bestvideo+bestaudio/best'
                    elif video_quality == "1080p":
                        format_str = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
                    elif video_quality == "720p":
                        format_str = 'bestvideo[height<=720]+bestaudio/best[height<=720]'
                    elif video_quality == "480p":
                        format_str = 'bestvideo[height<=480]+bestaudio/best[height<=480]'
                    else:
                        format_str = 'bestvideo[height<=360]+bestaudio/best[height<=360]'
                    
                    ydl_opts = {
                        'format': format_str,
                        'merge_output_format': 'mp4',
                        'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                        'progress_hooks': [progress_hook],
                        'quiet': True,
                        'no_warnings': True,
                    }
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(video_url, download=False)
                        title = info.get('title', 'Unknown')
                        duration = info.get('duration', 0)
                        
                        st.info(f"🎬 **Title:** {title}")
                        st.info(f"⏱️ **Duration:** {timedelta(seconds=duration)}")
                        
                        ydl.download([video_url])
                        
                        files = [f for f in os.listdir(temp_dir) if f.endswith('.mp4')]
                        if files:
                            file_path = os.path.join(temp_dir, files[0])
                            size_mb = os.path.getsize(file_path) / (1024*1024)
                            
                            with open(file_path, 'rb') as f:
                                file_data = f.read()
                            
                            st.balloons()
                            st.success(f"✅ Video Downloaded Successfully!")
                            st.info(f"📦 Size: {size_mb:.1f} MB | 🎬 MP4 | 📹 {video_quality}")
                            
                            # Download button with clear label
                            st.download_button(
                                label=f"💝 CLICK HERE TO DOWNLOAD - {title[:50]}.mp4 💝",
                                data=file_data,
                                file_name=f"{title}.mp4",
                                mime="video/mp4",
                                use_container_width=True,
                                key="video_download"
                            )
                            
                            if size_mb < 50:  # Only show preview for files under 50MB
                                st.video(file_data)
                            else:
                                st.info("📹 Video preview not available for large files. Click download button above.")
                        else:
                            st.error("No video file found after download")
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Make sure the URL is valid and FFmpeg is installed")

# Sidebar
with st.sidebar:
    st.markdown("### 🎀 About")
    
    st.markdown("""
    <div class="info-card">
        <h4>🎵 Audio Formats</h4>
        <ul>
            <li>MP3 - Universal</li>
            <li>M4A - Apple</li>
            <li>WAV - Lossless</li>
            <li>FLAC - Hi-Fi</li>
            <li>OPUS - Modern</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <h4>🎬 Video Format</h4>
        <ul>
            <li>MP4 - Universal</li>
            <li>Up to 1080p</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <h4>📋 How to Download</h4>
        <ol>
            <li>Paste URL</li>
            <li>Click Download</li>
            <li>Wait for processing</li>
            <li>Click green download button</li>
            <li>Check Downloads folder</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    <p>💖 Made with love | Audio: MP3 M4A WAV FLAC OPUS | Video: MP4</p>
    <p>🎵 🎀 🎵 🎀 🎵</p>
</div>
""", unsafe_allow_html=True)
