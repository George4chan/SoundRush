"""
🎵 Music & Video Downloader - Complete Web Version
Python: 3.8, 3.9, 3.10, 3.11, 3.12
Supports: MP3, M4A, WAV, FLAC, OPUS (Audio) | MP4 (Video)
"""

import streamlit as st
import os
import yt_dlp
import tempfile
from datetime import timedelta

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
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 15px 40px rgba(255, 107, 107, 0.6) !important;
    }
    
    .stButton > button::before {
        content: '✨';
        position: absolute;
        left: 20px;
        animation: sparkle 1.5s ease-in-out infinite;
    }
    
    .stButton > button::after {
        content: '✨';
        position: absolute;
        right: 20px;
        animation: sparkle 1.5s ease-in-out infinite 0.75s;
    }
    
    @keyframes sparkle {
        0%, 100% { opacity: 0; transform: scale(0); }
        50% { opacity: 1; transform: scale(1); }
    }
    
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 2px solid #FFD700 !important;
        border-radius: 25px !important;
        padding: 15px 20px !important;
        font-size: 1.1rem !important;
    }
    
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
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
        padding: 0.8rem 2rem !important;
        font-weight: 600 !important;
        border: none !important;
        box-shadow: 0 8px 25px rgba(76, 175, 80, 0.4) !important;
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
    <div style="text-align: center; margin-top: -20px;">
        <span style="font-size: 2rem;">🎧</span>
        <span style="font-size: 3rem;">🎶</span>
        <span style="font-size: 2rem;">🎧</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1>🎵 Music & Video Downloader 🎵</h1>", unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: white; font-size: 1.2rem;">Download Audio (MP3/M4A/WAV/FLAC/OPUS) & Video (MP4) 💖</p>', unsafe_allow_html=True)

# Tabs for Audio and Video
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
        placeholder="🔗 Paste YouTube or music URL here...",
        key="audio_url"
    )
    
    if st.button("🎵 Download Audio 🎵", use_container_width=True, key="audio_btn"):
        if not audio_url:
            st.error("❌ Please enter a URL first! 🥺")
        else:
            try:
                with tempfile.TemporaryDirectory() as temp_dir:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    def progress_hook(d):
                        if d['status'] == 'downloading':
                            try:
                                if 'total_bytes' in d and d['total_bytes']:
                                    percent = d['downloaded_bytes'] / d['total_bytes']
                                    progress_bar.progress(min(percent, 1.0))
                                    downloaded = d['downloaded_bytes'] / (1024*1024)
                                    total = d['total_bytes'] / (1024*1024)
                                    status_text.text(f"Downloading... {percent*100:.1f}% ({downloaded:.1f}/{total:.1f} MB)")
                            except:
                                pass
                        elif d['status'] == 'finished':
                            progress_bar.progress(1.0)
                            status_text.text("Processing audio...")
                    
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
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.info(f"🎵 **Title:** {title[:80]}")
                        with col2:
                            st.info(f"⏱️ **Duration:** {timedelta(seconds=duration)}")
                        
                        ydl.download([audio_url])
                        
                        files = [f for f in os.listdir(temp_dir) if f.endswith(audio_format)]
                        if files:
                            file_path = os.path.join(temp_dir, files[0])
                            size_mb = os.path.getsize(file_path) / (1024*1024)
                            
                            with open(file_path, 'rb') as f:
                                audio_bytes = f.read()
                            
                            st.balloons()
                            st.success(f"✅ Downloaded: {title}")
                            st.info(f"📦 Size: {size_mb:.1f} MB | 🎧 Format: {audio_format.upper()} | 🔊 Quality: {audio_quality}")
                            
                            st.download_button(
                                "💝 Download Audio File",
                                audio_bytes,
                                f"{title}.{audio_format}",
                                f"audio/{audio_format}",
                                use_container_width=True
                            )
                            
                            st.audio(audio_bytes, format=f"audio/{audio_format}")
            except Exception as e:
                st.error(f"Error: {str(e)}")

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
        st.info("📹 Format: MP4")
    
    video_url = st.text_input(
        "Enter URL for Video",
        placeholder="🔗 Paste YouTube or video URL here...",
        key="video_url"
    )
    
    if st.button("🎬 Download Video (MP4) 🎬", use_container_width=True, key="video_btn"):
        if not video_url:
            st.error("❌ Please enter a URL first! 🥺")
        else:
            try:
                with tempfile.TemporaryDirectory() as temp_dir:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    def progress_hook(d):
                        if d['status'] == 'downloading':
                            try:
                                if 'total_bytes' in d and d['total_bytes']:
                                    percent = d['downloaded_bytes'] / d['total_bytes']
                                    progress_bar.progress(min(percent, 1.0))
                                    downloaded = d['downloaded_bytes'] / (1024*1024)
                                    total = d['total_bytes'] / (1024*1024)
                                    status_text.text(f"Downloading... {percent*100:.1f}% ({downloaded:.1f}/{total:.1f} MB)")
                            except:
                                pass
                        elif d['status'] == 'finished':
                            progress_bar.progress(1.0)
                            status_text.text("Processing video...")
                    
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
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.info(f"🎬 **Title:** {title[:80]}")
                        with col2:
                            st.info(f"⏱️ **Duration:** {timedelta(seconds=duration)}")
                        
                        ydl.download([video_url])
                        
                        files = [f for f in os.listdir(temp_dir) if f.endswith('.mp4')]
                        if files:
                            file_path = os.path.join(temp_dir, files[0])
                            size_mb = os.path.getsize(file_path) / (1024*1024)
                            
                            with open(file_path, 'rb') as f:
                                video_bytes = f.read()
                            
                            st.balloons()
                            st.success(f"✅ Downloaded: {title}")
                            st.info(f"📦 Size: {size_mb:.1f} MB | 🎬 Format: MP4 | 📹 Quality: {video_quality}")
                            
                            st.download_button(
                                "💝 Download Video File (MP4)",
                                video_bytes,
                                f"{title}.mp4",
                                "video/mp4",
                                use_container_width=True
                            )
                            
                            st.video(video_bytes)
            except Exception as e:
                st.error(f"Error: {str(e)}")

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
            <li>Best quality</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <h4>📋 Requirements</h4>
        <ul>
            <li>🐍 Python 3.8+</li>
            <li>🎬 FFmpeg</li>
            <li>🌐 Internet</li>
        </ul>
    </div>
    """)

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    <p>Made with 💖 | Supports: MP3 | M4A | WAV | FLAC | OPUS | MP4</p>
    <p>🎵 🎀 🎵 🎀 🎵</p>
</div>
""", unsafe_allow_html=True)
