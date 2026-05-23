"""
🎵 MUSIC & VIDEO DOWNLOADER - COMPLETE APP
Save as: app.py
Run: streamlit run app.py
"""

import streamlit as st
import os
import yt_dlp
import tempfile
from datetime import timedelta

# Try to install yt-dlp if missing
try:
    import yt_dlp
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
    import yt_dlp

# Page setup
st.set_page_config(page_title="🎵 Music Downloader", page_icon="🎵", layout="wide")

# Custom CSS for beautiful design
st.markdown("""
<style>
    /* Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    }
    
    /* Title */
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #f093fb, #f5576c, #fda085);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    
    /* Subtitle */
    .subtitle {
        text-align: center;
        color: #b8b8d0;
        font-size: 1.2rem;
        margin-top: 0;
    }
    
    /* Cards */
    .card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Download button */
    .stButton > button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        font-size: 1.3rem;
        font-weight: 700;
        padding: 18px 40px;
        border-radius: 50px;
        border: none;
        width: 100%;
        cursor: pointer;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 2px;
        box-shadow: 0 10px 30px rgba(245, 87, 108, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(245, 87, 108, 0.5);
        background: linear-gradient(135deg, #f5576c 0%, #f093fb 100%);
    }
    
    /* Save button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #00b894, #00cec9);
        color: white;
        font-size: 1.2rem;
        font-weight: 700;
        padding: 18px 40px;
        border-radius: 50px;
        border: 2px solid white;
        width: 100%;
        cursor: pointer;
        animation: pulse 2s infinite;
        box-shadow: 0 10px 30px rgba(0, 184, 148, 0.3);
    }
    
    @keyframes pulse {
        0%, 100% { box-shadow: 0 0 20px rgba(0, 184, 148, 0.4); }
        50% { box-shadow: 0 0 40px rgba(0, 184, 148, 0.8); }
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.1);
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 15px;
        padding: 15px 20px;
        color: white;
        font-size: 1.1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #f5576c;
        box-shadow: 0 0 15px rgba(245, 87, 108, 0.3);
    }
    
    /* Select boxes */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #f093fb, #f5576c, #fda085);
        border-radius: 10px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab"] {
        font-size: 1.3rem;
        font-weight: 600;
        color: white;
        padding: 15px 30px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #f093fb, #f5576c);
        border-radius: 12px;
    }
    
    /* Success message */
    .success-msg {
        background: rgba(0, 184, 148, 0.2);
        border: 2px solid #00b894;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        color: white;
    }
    
    /* Info text */
    .info-text {
        color: #b8b8d0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div style="text-align:center;font-size:6rem;">🎵</div>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">Music Downloader Pro</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Download Audio & Video in High Quality ✨</p>', unsafe_allow_html=True)
st.markdown('<br>', unsafe_allow_html=True)

# Tabs
tab1, tab2 = st.tabs(["🎵 AUDIO DOWNLOAD", "🎬 VIDEO DOWNLOAD (MP4)"])

# ========== AUDIO TAB ==========
with tab1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        audio_quality = st.selectbox(
            "🔊 QUALITY",
            ["128 kbps", "192 kbps", "256 kbps", "320 kbps"],
            key="audio_quality"
        )
    with col2:
        audio_format = st.selectbox(
            "🎧 FORMAT",
            ["mp3", "m4a", "wav", "flac", "opus"],
            key="audio_format"
        )
    with col3:
        st.markdown('<br>', unsafe_allow_html=True)
        st.markdown(f'<p class="info-text">✅ Selected: <b>{audio_quality}</b> • <b>{audio_format.upper()}</b></p>', unsafe_allow_html=True)
    
    audio_url = st.text_input(
        "🔗 YOUTUBE URL",
        placeholder="https://www.youtube.com/watch?v=...",
        key="audio_url"
    )
    
    if st.button("🎵 DOWNLOAD AUDIO", key="audio_btn"):
        if not audio_url:
            st.warning("⚠️ Please enter a YouTube URL")
        else:
            try:
                with tempfile.TemporaryDirectory() as tmp:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    def progress_hook(d):
                        if d['status'] == 'downloading':
                            if d.get('total_bytes'):
                                percent = d['downloaded_bytes'] / d['total_bytes']
                                progress_bar.progress(min(percent, 1.0))
                                mb = d['downloaded_bytes'] / (1024*1024)
                                total_mb = d['total_bytes'] / (1024*1024)
                                status_text.markdown(f'<p class="info-text">📥 Downloading... {percent*100:.0f}% ({mb:.1f}/{total_mb:.1f} MB)</p>', unsafe_allow_html=True)
                        elif d['status'] == 'finished':
                            progress_bar.progress(1.0)
                            status_text.markdown('<p class="info-text">🔄 Processing audio...</p>', unsafe_allow_html=True)
                    
                    quality_val = audio_quality.replace(" kbps", "")
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': audio_format,
                            'preferredquality': quality_val,
                        }],
                        'outtmpl': os.path.join(tmp, '%(title)s.%(ext)s'),
                        'progress_hooks': [progress_hook],
                        'quiet': True,
                    }
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(audio_url, download=False)
                        title = info.get('title', 'Unknown')
                        duration = info.get('duration', 0)
                        
                        st.info(f"🎵 **{title}** | ⏱️ **{timedelta(seconds=duration)}**")
                        
                        ydl.download([audio_url])
                    
                    files = [f for f in os.listdir(tmp) if f.endswith(audio_format)]
                    if files:
                        filepath = os.path.join(tmp, files[0])
                        size_mb = os.path.getsize(filepath) / (1024*1024)
                        
                        with open(filepath, 'rb') as f:
                            file_data = f.read()
                        
                        st.balloons()
                        
                        st.markdown(f"""
                        <div class="success-msg">
                            <h2>✅ DOWNLOAD COMPLETE!</h2>
                            <p>📁 File: {title[:60]}</p>
                            <p>📦 Size: {size_mb:.1f} MB | 🎧 {audio_format.upper()} | 🔊 {audio_quality}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.download_button(
                            label=f"💾 CLICK TO SAVE: {title[:40]}.{audio_format}",
                            data=file_data,
                            file_name=f"{title}.{audio_format}",
                            mime=f"audio/{audio_format}",
                        )
                        
                        st.audio(file_data, format=f"audio/{audio_format}")
                    else:
                        st.error("❌ No file was generated")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ========== VIDEO TAB ==========
with tab2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        video_quality = st.selectbox(
            "📹 QUALITY",
            ["Best Available", "1080p", "720p", "480p", "360p"],
            key="video_quality"
        )
    with col2:
        st.markdown('<br>', unsafe_allow_html=True)
        st.markdown('<p class="info-text">📼 <b>Format: MP4</b></p>', unsafe_allow_html=True)
    with col3:
        st.markdown('<br>', unsafe_allow_html=True)
        st.markdown(f'<p class="info-text">✅ Selected: <b>{video_quality}</b> • <b>MP4</b></p>', unsafe_allow_html=True)
    
    video_url = st.text_input(
        "🔗 YOUTUBE URL",
        placeholder="https://www.youtube.com/watch?v=...",
        key="video_url"
    )
    
    if st.button("🎬 DOWNLOAD VIDEO (MP4)", key="video_btn"):
        if not video_url:
            st.warning("⚠️ Please enter a YouTube URL")
        else:
            try:
                with tempfile.TemporaryDirectory() as tmp:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    def progress_hook(d):
                        if d['status'] == 'downloading':
                            if d.get('total_bytes'):
                                percent = d['downloaded_bytes'] / d['total_bytes']
                                progress_bar.progress(min(percent, 1.0))
                                mb = d['downloaded_bytes'] / (1024*1024)
                                total_mb = d['total_bytes'] / (1024*1024)
                                status_text.markdown(f'<p class="info-text">📥 Downloading... {percent*100:.0f}% ({mb:.1f}/{total_mb:.1f} MB)</p>', unsafe_allow_html=True)
                        elif d['status'] == 'finished':
                            progress_bar.progress(1.0)
                            status_text.markdown('<p class="info-text">🔄 Processing video...</p>', unsafe_allow_html=True)
                    
                    if video_quality == "Best Available":
                        format_str = 'bestvideo+bestaudio/best'
                    else:
                        height = video_quality.replace('p', '')
                        format_str = f'bestvideo[height<={height}]+bestaudio/best[height<={height}]'
                    
                    ydl_opts = {
                        'format': format_str,
                        'merge_output_format': 'mp4',
                        'outtmpl': os.path.join(tmp, '%(title)s.%(ext)s'),
                        'progress_hooks': [progress_hook],
                        'quiet': True,
                    }
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(video_url, download=False)
                        title = info.get('title', 'Unknown')
                        duration = info.get('duration', 0)
                        
                        st.info(f"🎬 **{title}** | ⏱️ **{timedelta(seconds=duration)}**")
                        
                        ydl.download([video_url])
                    
                    files = [f for f in os.listdir(tmp) if f.endswith('.mp4')]
                    if files:
                        filepath = os.path.join(tmp, files[0])
                        size_mb = os.path.getsize(filepath) / (1024*1024)
                        
                        with open(filepath, 'rb') as f:
                            file_data = f.read()
                        
                        st.balloons()
                        
                        st.markdown(f"""
                        <div class="success-msg">
                            <h2>✅ DOWNLOAD COMPLETE!</h2>
                            <p>📁 File: {title[:60]}</p>
                            <p>📦 Size: {size_mb:.1f} MB | 🎬 MP4 | 📹 {video_quality}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.download_button(
                            label=f"💾 CLICK TO SAVE: {title[:40]}.mp4",
                            data=file_data,
                            file_name=f"{title}.mp4",
                            mime="video/mp4",
                        )
                        
                        if size_mb < 50:
                            st.video(file_data)
                        else:
                            st.info("📹 File too large for preview. Use the download button above.")
                    else:
                        st.error("❌ No video file was generated")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🎀 ABOUT")
    
    st.markdown("""
    <div style="background:rgba(255,255,255,0.05);padding:20px;border-radius:15px;margin:10px 0;">
        <h3 style="color:#f5576c;">🎵 Audio Formats</h3>
        <p>MP3 • M4A • WAV • FLAC • OPUS</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background:rgba(255,255,255,0.05);padding:20px;border-radius:15px;margin:10px 0;">
        <h3 style="color:#f5576c;">🎬 Video Format</h3>
        <p>MP4 (up to 1080p)</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background:rgba(255,255,255,0.05);padding:20px;border-radius:15px;margin:10px 0;">
        <h3 style="color:#f5576c;">📋 Steps</h3>
        <ol>
            <li>Paste YouTube URL</li>
            <li>Choose quality & format</li>
            <li>Click Download</li>
            <li>Click green Save button</li>
            <li>File saves to Downloads</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background:rgba(255,255,255,0.05);padding:20px;border-radius:15px;margin:10px 0;">
        <h3 style="color:#f5576c;">⚠️ Requirements</h3>
        <p>Python 3.8+ • FFmpeg • Internet</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align:center;color:#b8b8d0;">
    <p>💖 Made with love | Audio: MP3 M4A WAV FLAC OPUS | Video: MP4</p>
    <p>🎵 🎀 🎵 🎀 🎵</p>
</div>
""", unsafe_allow_html=True)
