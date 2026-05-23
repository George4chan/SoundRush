"""
🎵 Music Downloader - Cute & Beautiful Web Version
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

# Custom CSS for beautiful styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Main container */
    .main > div {
        padding: 2rem;
    }
    
    /* Title styling */
    h1 {
        font-family: 'Poppins', sans-serif !important;
        font-size: 3rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #FFD700, #FFA500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Subtitle */
    .subtitle {
        text-align: center;
        color: #ffffff;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        opacity: 0.9;
    }
    
    /* Logo container */
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
    
    /* Cute download button */
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
        background: linear-gradient(135deg, #FF8E53, #FF6B6B) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-2px) !important;
    }
    
    /* Sparkle effect on button */
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
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
    }
    
    /* Input field */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 2px solid #FFD700 !important;
        border-radius: 25px !important;
        padding: 15px 20px !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #FF6B6B !important;
        box-shadow: 0 0 20px rgba(255, 107, 107, 0.3) !important;
    }
    
    /* Success message */
    .stAlert {
        border-radius: 15px !important;
        border: none !important;
        background: linear-gradient(135deg, #4CAF50, #45a049) !important;
        color: white !important;
    }
    
    /* Download button for file */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #4CAF50, #45a049) !important;
        color: white !important;
        border-radius: 30px !important;
        padding: 0.8rem 2rem !important;
        font-weight: 600 !important;
        border: none !important;
        box-shadow: 0 8px 25px rgba(76, 175, 80, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 35px rgba(76, 175, 80, 0.6) !important;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #FFD700, #FFA500, #FF6B6B) !important;
        border-radius: 10px !important;
    }
    
    /* Card styling */
    .info-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: white;
        opacity: 0.7;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Cute Logo
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

# Title with hearts
st.markdown("<h1>🎵 Music Downloader Pro 🎵</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">Download high-quality music with love 💖</p>', unsafe_allow_html=True)

# Sidebar with cute styling
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; font-size: 2rem;">
        🎀 ⚙️ 🎀
    </div>
    """, unsafe_allow_html=True)
    
    st.header("⚙️ Settings")
    
    quality = st.selectbox(
        "🎧 Audio Quality",
        ["128 kbps", "192 kbps", "256 kbps", "320 kbps"],
        index=1
    )
    
    format_type = st.selectbox(
        "🎵 Output Format",
        ["mp3", "m4a", "wav", "flac", "opus"],
        index=0
    )
    
    st.markdown("---")
    
    # Cute info cards
    st.markdown("""
    <div class="info-card">
        <h4>🌟 Features</h4>
        <ul>
            <li>🎵 High Quality Audio</li>
            <li>⚡ Fast Downloads</li>
            <li>💝 Multiple Formats</li>
            <li>🎀 Easy to Use</li>
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
    """, unsafe_allow_html=True)

# Main interface with card
st.markdown("""
<div class="info-card" style="margin-bottom: 30px;">
    <h3 style="text-align: center; color: white;">🎤 Enter Your Music URL</h3>
""", unsafe_allow_html=True)

url = st.text_input(
    "",
    placeholder="🔗 Paste YouTube URL here... https://www.youtube.com/watch?v=..."
)

st.markdown("</div>", unsafe_allow_html=True)

# Centered download button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    download_clicked = st.button("🎵 Download Music 🎵", type="primary", use_container_width=True)

# Download logic
if download_clicked:
    if not url:
        st.error("❌ Oopsie! Please enter a valid URL first! 🥺")
    else:
        try:
            # Create temp directory
            with tempfile.TemporaryDirectory() as temp_dir:
                # Progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Cute status messages
                cute_messages = [
                    "🔍 Finding your music...",
                    "🎵 Getting ready to download...",
                    "🌟 Almost there...",
                    "💝 Preparing your audio..."
                ]
                
                def progress_hook(d):
                    if d['status'] == 'downloading':
                        try:
                            if 'total_bytes' in d and d['total_bytes']:
                                percent = d['downloaded_bytes'] / d['total_bytes']
                                progress_bar.progress(min(percent, 1.0))
                                status_text.markdown(f"""
                                    <div style="text-align: center; color: white;">
                                        <h3>🎵 Downloading your music... {percent*100:.1f}%</h3>
                                        <p style="opacity: 0.8;">Please wait while we work our magic ✨</p>
                                    </div>
                                """, unsafe_allow_html=True)
                        except:
                            pass
                    elif d['status'] == 'finished':
                        progress_bar.progress(1.0)
                        status_text.markdown("""
                            <div style="text-align: center; color: white;">
                                <h3>🎨 Processing audio...</h3>
                                <p style="opacity: 0.8;">Making it perfect for you 💖</p>
                            </div>
                        """, unsafe_allow_html=True)
                
                # yt-dlp options
                quality_value = quality.replace(" kbps", "")
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': format_type,
                        'preferredquality': quality_value,
                    }],
                    'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                    'progress_hooks': [progress_hook],
                    'quiet': True,
                    'no_warnings': True,
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # Get info
                    status_text.markdown(f"<div style='text-align: center; color: white;'><h3>{cute_messages[0]}</h3></div>", unsafe_allow_html=True)
                    info = ydl.extract_info(url, download=False)
                    title = info.get('title', 'Unknown')
                    duration = info.get('duration', 0)
                    
                    # Show info in cute cards
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(f"""
                        <div class="info-card" style="text-align: center;">
                            <h4>🎵 Title</h4>
                            <p>{title[:50]}...</p>
                        </div>
                        """, unsafe_allow_html=True)
                    with col2:
                        mins = duration // 60
                        secs = duration % 60
                        st.markdown(f"""
                        <div class="info-card" style="text-align: center;">
                            <h4>⏱️ Duration</h4>
                            <p>{mins}:{secs:02d}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    with col3:
                        st.markdown(f"""
                        <div class="info-card" style="text-align: center;">
                            <h4>🎧 Quality</h4>
                            <p>{quality} - {format_type.upper()}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Download
                    ydl.download([url])
                    
                    # Find downloaded file
                    downloaded_files = os.listdir(temp_dir)
                    if downloaded_files:
                        file_path = os.path.join(temp_dir, downloaded_files[0])
                        
                        # Read file
                        with open(file_path, 'rb') as f:
                            audio_bytes = f.read()
                        
                        # Success message
                        st.balloons()
                        st.success(f"🎉 Yay! Successfully downloaded: {title}")
                        
                        # Cute download section
                        st.markdown("""
                        <div class="info-card" style="text-align: center;">
                            <h3>🌟 Your Music is Ready! 🌟</h3>
                            <p>Click the button below to save your file 💾</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Beautiful download button
                        col1, col2, col3 = st.columns([1, 2, 1])
                        with col2:
                            st.download_button(
                                label="💝 Save My Music 💝",
                                data=audio_bytes,
                                file_name=f"{title}.{format_type}",
                                mime=f"audio/{format_type}",
                                use_container_width=True
                            )
                        
                        # Audio player
                        st.markdown("### 🎧 Preview Your Music:")
                        st.audio(audio_bytes, format=f"audio/{format_type}")
                        
        except Exception as e:
            st.error(f"😢 Oops! Something went wrong: {str(e)}")
            st.info("💡 Tip: Make sure the URL is valid and the video is available")

# Cute footer
st.markdown("---")
st.markdown("""
<div class="footer">
    <p style="font-size: 1.2rem;">Made with 💖 using Python & Streamlit</p>
    <p style="font-size: 0.9rem;">
        🎵 🎀 🎵 🎀 🎵 🎀 🎵
    </p>
</div>
""", unsafe_allow_html=True)

# Version info
st.caption("🌸 Music Downloader Pro v1.0 | Python 3.8+ | Streamlit 🌸")
