"""
🎵 Music & Video Downloader - Complete Working Version
Python: 3.8, 3.9, 3.10, 3.11, 3.12
Supports: MP3, M4A, WAV, FLAC, OPUS, MP4
"""

import streamlit as st
import os
import yt_dlp
import tempfile
from datetime import timedelta

# Page config
st.set_page_config(
    page_title="🎵 Music Downloader",
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
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        padding: 1rem 2rem !important;
        border-radius: 50px !important;
        border: none !important;
        box-shadow: 0 10px 30px rgba(255, 107, 107, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 15px 40px rgba(255, 107, 107, 0.6) !important;
    }
    
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 2px solid #FFD700 !important;
        border-radius: 25px !important;
        padding: 12px 20px !important;
        font-size: 1rem !important;
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
        color: white;
    }
    
    .stDownloadButton > button {
        background: linear-gradient(135deg, #4CAF50, #45a049) !important;
        color: white !important;
        border-radius: 30px !important;
        padding: 1rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        border: 3px solid white !important;
        box-shadow: 0 8px 25px rgba(76, 175, 80, 0.4) !important;
        animation: pulse 2s infinite !important;
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
    
    .success-box {
        background: rgba(76, 175, 80, 0.2);
        border: 2px solid #4CAF50;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Logo
st.markdown("""
<div class="logo-container">
    <div style="font-size: 4rem; text-align: center;">🎵🎀🎵</div>
</div>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1>🎵 Music & Video Downloader 🎵</h1>", unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: white; font-size: 1.1rem;">Download Audio & Video with Love 💖</p>', unsafe_allow_html=True)

# Tabs
tab1, tab2 = st.tabs(["🎵 Audio", "🎬 Video (MP4)"])

# ==================== AUDIO TAB ====================
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        audio_quality = st.selectbox("🔊 Quality", ["128", "192", "256", "320"], index=1, key="q")
    with col2:
        audio_format = st.selectbox("🎧 Format", ["mp3", "m4a", "wav", "flac", "opus"], key="f")
    
    audio_url = st.text_input("🔗 Enter URL", placeholder="https://www.youtube.com/watch?v=...", key="au")
    
    if st.button("🎵 Download Audio 🎵", use_container_width=True, key="abtn"):
        if not audio_url:
            st.warning("⚠️ Please enter a URL")
        else:
            try:
                with tempfile.TemporaryDirectory() as tmp:
                    progress = st.progress(0)
                    status = st.empty()
                    
                    def hook(d):
                        if d['status'] == 'downloading':
                            if d.get('total_bytes'):
                                pct = d['downloaded_bytes'] / d['total_bytes']
                                progress.progress(min(pct, 1.0))
                                status.text(f"Downloading... {pct*100:.0f}%")
                        elif d['status'] == 'finished':
                            progress.progress(1.0)
                            status.text("Processing audio...")
                    
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': audio_format,
                            'preferredquality': audio_quality,
                        }],
                        'outtmpl': os.path.join(tmp, '%(title)s.%(ext)s'),
                        'progress_hooks': [hook],
                        'quiet': True,
                    }
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(audio_url, download=False)
                        title = info['title']
                        duration = info.get('duration', 0)
                        
                        st.info(f"🎵 **{title}** | ⏱️ {timedelta(seconds=duration)}")
                        
                        ydl.download([audio_url])
                    
                    files = [f for f in os.listdir(tmp) if f.endswith(audio_format)]
                    if files:
                        filepath = os.path.join(tmp, files[0])
                        size_mb = os.path.getsize(filepath) / (1024*1024)
                        
                        with open(filepath, 'rb') as f:
                            data = f.read()
                        
                        st.balloons()
                        
                        st.markdown(f"""
                        <div class="success-box">
                            <h3>✅ Download Complete!</h3>
                            <p>📦 Size: {size_mb:.1f} MB | 🎧 {audio_format.upper()} | 🔊 {audio_quality}kbps</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.download_button(
                            label=f"💝 DOWNLOAD: {title[:50]}.{audio_format} 💝",
                            data=data,
                            file_name=f"{title}.{audio_format}",
                            mime=f"audio/{audio_format}",
                            use_container_width=True,
                        )
                        
                        st.audio(data)
                    else:
                        st.error("No file generated")
            except Exception as e:
                st.error(f"❌ Error: {e}")

# ==================== VIDEO TAB ====================
with tab2:
    col1, col2 = st.columns(2)
    with col1:
        video_quality = st.selectbox("📹 Quality", ["Best", "1080p", "720p", "480p", "360p"], key="vq")
    with col2:
        st.markdown('<p style="color:white; margin-top:30px;">📼 <b>Format: MP4</b></p>', unsafe_allow_html=True)
    
    video_url = st.text_input("🔗 Enter URL", placeholder="https://www.youtube.com/watch?v=...", key="vu")
    
    if st.button("🎬 Download Video (MP4) 🎬", use_container_width=True, key="vbtn"):
        if not video_url:
            st.warning("⚠️ Please enter a URL")
        else:
            try:
                with tempfile.TemporaryDirectory() as tmp:
                    progress = st.progress(0)
                    status = st.empty()
                    
                    def hook(d):
                        if d['status'] == 'downloading':
                            if d.get('total_bytes'):
                                pct = d['downloaded_bytes'] / d['total_bytes']
                                progress.progress(min(pct, 1.0))
                                status.text(f"Downloading... {pct*100:.0f}%")
                        elif d['status'] == 'finished':
                            progress.progress(1.0)
                            status.text("Processing video...")
                    
                    if video_quality == "Best":
                        fmt_str = 'bestvideo+bestaudio/best'
                    else:
                        h = video_quality.replace('p', '')
                        fmt_str = f'bestvideo[height<={h}]+bestaudio/best[height<={h}]'
                    
                    ydl_opts = {
                        'format': fmt_str,
                        'merge_output_format': 'mp4',
                        'outtmpl': os.path.join(tmp, '%(title)s.%(ext)s'),
                        'progress_hooks': [hook],
                        'quiet': True,
                    }
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(video_url, download=False)
                        title = info['title']
                        duration = info.get('duration', 0)
                        
                        st.info(f"🎬 **{title}** | ⏱️ {timedelta(seconds=duration)}")
                        
                        ydl.download([video_url])
                    
                    files = [f for f in os.listdir(tmp) if f.endswith('.mp4')]
                    if files:
                        filepath = os.path.join(tmp, files[0])
                        size_mb = os.path.getsize(filepath) / (1024*1024)
                        
                        with open(filepath, 'rb') as f:
                            data = f.read()
                        
                        st.balloons()
                        
                        st.markdown(f"""
                        <div class="success-box">
                            <h3>✅ Download Complete!</h3>
                            <p>📦 Size: {size_mb:.1f} MB | 🎬 MP4 | 📹 {video_quality}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.download_button(
                            label=f"💝 DOWNLOAD: {title[:50]}.mp4 💝",
                            data=data,
                            file_name=f"{title}.mp4",
                            mime="video/mp4",
                            use_container_width=True,
                        )
                        
                        if size_mb < 50:
                            st.video(data)
                        else:
                            st.info("📹 File too large for preview. Click download button above.")
                    else:
                        st.error("No video file generated")
            except Exception as e:
                st.error(f"❌ Error: {e}")

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("### 🎀 Info")
    
    st.markdown("""
    <div class="info-card">
        <h4>🎵 Audio</h4>
        MP3 | M4A | WAV | FLAC | OPUS
    </div>
    <div class="info-card">
        <h4>🎬 Video</h4>
        MP4 (Up to 1080p)
    </div>
    <div class="info-card">
        <h4>📋 Steps</h4>
        1. Paste URL<br>
        2. Click Download<br>
        3. Click green button to save
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    <p>💖 Made with love | Audio & Video Downloader</p>
    <p>🎵 🎀 🎵</p>
</div>
""", unsafe_allow_html=True)
