"""
Music & Video Downloader - Professional Edition
Python 3.8+ | FFmpeg Required
"""

import streamlit as st
import os
import tempfile
import yt_dlp
from datetime import timedelta

# Page configuration
st.set_page_config(
    page_title="Music & Video Downloader",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    }
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        color: #ffffff;
        margin-bottom: 0;
    }
    .subtitle {
        text-align: center;
        color: #a8a8b3;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    .stButton > button {
        background: linear-gradient(90deg, #e94560, #c23152);
        color: white;
        font-weight: 600;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        border: none;
        width: 100%;
        font-size: 1.1rem;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #c23152, #a02040);
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(233, 69, 96, 0.3);
    }
    .stDownloadButton > button {
        background: linear-gradient(90deg, #00b894, #00a381);
        color: white;
        font-weight: 600;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        border: none;
        width: 100%;
        font-size: 1.1rem;
    }
    .stDownloadButton > button:hover {
        background: linear-gradient(90deg, #00a381, #008f6b);
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(0, 184, 148, 0.3);
    }
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e94560;
        padding: 0.75rem 1rem;
        font-size: 1rem;
    }
    .stTextInput > div > div > input:focus {
        border-color: #00b894;
        box-shadow: 0 0 0 3px rgba(0, 184, 148, 0.2);
    }
    .stSelectbox > div > div {
        border-radius: 8px;
    }
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #e94560, #00b894);
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 1.1rem;
        font-weight: 600;
        padding: 0.75rem 2rem;
    }
    .stTabs [aria-selected="true"] {
        background-color: #e94560;
    }
    .success-box {
        background: linear-gradient(135deg, rgba(0,184,148,0.1), rgba(0,184,148,0.05));
        border: 1px solid #00b894;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
    }
    .sidebar-content {
        background: rgba(255,255,255,0.03);
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-title">🎵 Music & Video Downloader</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Professional YouTube Audio & Video Downloader</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 📋 Requirements")
    st.markdown("""
    <div class="sidebar-content">
        <p>✅ Python 3.8 or higher</p>
        <p>✅ FFmpeg installed</p>
        <p>✅ Internet connection</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("## 📝 How to Use")
    st.markdown("""
    <div class="sidebar-content">
        <p>1️⃣ Paste YouTube URL</p>
        <p>2️⃣ Select quality & format</p>
        <p>3️⃣ Click Download button</p>
        <p>4️⃣ Click Save to download file</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("## ⚠️ Note")
    st.markdown("""
    <div class="sidebar-content">
        <p>Only download content you have permission to download. Respect copyright laws.</p>
    </div>
    """, unsafe_allow_html=True)

# Main content
tab1, tab2 = st.tabs(["🎵 Audio Download", "🎬 Video Download (MP4)"])

# Audio Download Tab
with tab1:
    st.markdown("### Download Audio from YouTube")
    
    col1, col2 = st.columns(2)
    with col1:
        audio_quality = st.selectbox(
            "Audio Quality",
            options=["128 kbps", "192 kbps", "256 kbps", "320 kbps"],
            index=1,
            key="audio_quality"
        )
    with col2:
        audio_format = st.selectbox(
            "Audio Format",
            options=["mp3", "m4a", "wav", "flac", "opus"],
            index=0,
            key="audio_format"
        )
    
    audio_url = st.text_input(
        "YouTube URL",
        placeholder="https://www.youtube.com/watch?v=...",
        key="audio_url_input"
    )
    
    if st.button("Download Audio", key="download_audio_btn"):
        if not audio_url:
            st.warning("Please enter a YouTube URL")
        else:
            try:
                with tempfile.TemporaryDirectory() as temp_dir:
                    progress_bar = st.progress(0)
                    status_display = st.empty()
                    
                    def progress_tracker(d):
                        if d['status'] == 'downloading':
                            if d.get('total_bytes') and d['total_bytes'] > 0:
                                percentage = d['downloaded_bytes'] / d['total_bytes']
                                progress_bar.progress(min(percentage, 1.0))
                                downloaded = d['downloaded_bytes'] / (1024 * 1024)
                                total = d['total_bytes'] / (1024 * 1024)
                                status_display.info(f"Downloading: {percentage*100:.1f}% ({downloaded:.1f}MB / {total:.1f}MB)")
                        elif d['status'] == 'finished':
                            progress_bar.progress(1.0)
                            status_display.info("Processing audio file...")
                    
                    quality_value = audio_quality.replace(" kbps", "")
                    
                    download_options = {
                        'format': 'bestaudio/best',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': audio_format,
                            'preferredquality': quality_value,
                        }],
                        'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                        'progress_hooks': [progress_tracker],
                        'quiet': True,
                        'no_warnings': True,
                    }
                    
                    with yt_dlp.YoutubeDL(download_options) as downloader:
                        video_info = downloader.extract_info(audio_url, download=False)
                        video_title = video_info.get('title', 'Unknown Title')
                        video_duration = video_info.get('duration', 0)
                        
                        st.markdown(f"**Title:** {video_title}")
                        st.markdown(f"**Duration:** {timedelta(seconds=video_duration)}")
                        
                        downloader.download([audio_url])
                    
                    downloaded_files = [f for f in os.listdir(temp_dir) if f.endswith(audio_format)]
                    
                    if downloaded_files:
                        file_path = os.path.join(temp_dir, downloaded_files[0])
                        file_size = os.path.getsize(file_path) / (1024 * 1024)
                        
                        with open(file_path, 'rb') as file:
                            file_data = file.read()
                        
                        st.balloons()
                        
                        st.markdown(f"""
                        <div class="success-box">
                            <h3>✅ Download Complete</h3>
                            <p><strong>File:</strong> {video_title}</p>
                            <p><strong>Size:</strong> {file_size:.1f} MB | <strong>Format:</strong> {audio_format.upper()} | <strong>Quality:</strong> {audio_quality}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.download_button(
                            label=f"💾 Save File - {video_title[:40]}.{audio_format}",
                            data=file_data,
                            file_name=f"{video_title}.{audio_format}",
                            mime=f"audio/{audio_format}",
                            key="audio_save_btn"
                        )
                        
                        st.audio(file_data, format=f"audio/{audio_format}")
                    else:
                        st.error("Download failed. No file was created.")
                        
            except Exception as error:
                st.error(f"Error: {str(error)}")

# Video Download Tab
with tab2:
    st.markdown("### Download Video from YouTube (MP4)")
    
    col1, col2 = st.columns(2)
    with col1:
        video_quality = st.selectbox(
            "Video Quality",
            options=["Best Available", "1080p", "720p", "480p", "360p"],
            index=0,
            key="video_quality"
        )
    with col2:
        st.markdown("**Output Format:** MP4")
    
    video_url = st.text_input(
        "YouTube URL",
        placeholder="https://www.youtube.com/watch?v=...",
        key="video_url_input"
    )
    
    if st.button("Download Video (MP4)", key="download_video_btn"):
        if not video_url:
            st.warning("Please enter a YouTube URL")
        else:
            try:
                with tempfile.TemporaryDirectory() as temp_dir:
                    progress_bar = st.progress(0)
                    status_display = st.empty()
                    
                    def progress_tracker(d):
                        if d['status'] == 'downloading':
                            if d.get('total_bytes') and d['total_bytes'] > 0:
                                percentage = d['downloaded_bytes'] / d['total_bytes']
                                progress_bar.progress(min(percentage, 1.0))
                                downloaded = d['downloaded_bytes'] / (1024 * 1024)
                                total = d['total_bytes'] / (1024 * 1024)
                                status_display.info(f"Downloading: {percentage*100:.1f}% ({downloaded:.1f}MB / {total:.1f}MB)")
                        elif d['status'] == 'finished':
                            progress_bar.progress(1.0)
                            status_display.info("Processing video file...")
                    
                    if video_quality == "Best Available":
                        format_selection = 'bestvideo+bestaudio/best'
                    else:
                        height = video_quality.replace('p', '')
                        format_selection = f'bestvideo[height<={height}]+bestaudio/best[height<={height}]'
                    
                    download_options = {
                        'format': format_selection,
                        'merge_output_format': 'mp4',
                        'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                        'progress_hooks': [progress_tracker],
                        'quiet': True,
                        'no_warnings': True,
                    }
                    
                    with yt_dlp.YoutubeDL(download_options) as downloader:
                        video_info = downloader.extract_info(video_url, download=False)
                        video_title = video_info.get('title', 'Unknown Title')
                        video_duration = video_info.get('duration', 0)
                        
                        st.markdown(f"**Title:** {video_title}")
                        st.markdown(f"**Duration:** {timedelta(seconds=video_duration)}")
                        
                        downloader.download([video_url])
                    
                    downloaded_files = [f for f in os.listdir(temp_dir) if f.endswith('.mp4')]
                    
                    if downloaded_files:
                        file_path = os.path.join(temp_dir, downloaded_files[0])
                        file_size = os.path.getsize(file_path) / (1024 * 1024)
                        
                        with open(file_path, 'rb') as file:
                            file_data = file.read()
                        
                        st.balloons()
                        
                        st.markdown(f"""
                        <div class="success-box">
                            <h3>✅ Download Complete</h3>
                            <p><strong>File:</strong> {video_title}</p>
                            <p><strong>Size:</strong> {file_size:.1f} MB | <strong>Format:</strong> MP4 | <strong>Quality:</strong> {video_quality}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.download_button(
                            label=f"💾 Save File - {video_title[:40]}.mp4",
                            data=file_data,
                            file_name=f"{video_title}.mp4",
                            mime="video/mp4",
                            key="video_save_btn"
                        )
                        
                        if file_size < 50:
                            st.video(file_data)
                        else:
                            st.info("File too large for preview. Click the save button to download.")
                    else:
                        st.error("Download failed. No file was created.")
                        
            except Exception as error:
                st.error(f"Error: {str(error)}")

# Footer
st.markdown("---")
st.markdown("<p style='text-align:center;color:#a8a8b3;'>Professional Music & Video Downloader | For personal use only</p>", unsafe_allow_html=True)
