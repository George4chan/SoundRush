"""
MUSIC & VIDEO DOWNLOADER - ALL IN ONE
Save this file. Run it. It works.

Requirements:
- Python 3.8+
- FFmpeg installed

Install: pip install yt-dlp streamlit
Run: streamlit run music_downloader.py
"""

import streamlit as st
import os
import yt_dlp
import tempfile
from datetime import timedelta

# Check and install yt-dlp if needed
try:
    import yt_dlp
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
    import yt_dlp

st.set_page_config(page_title="Music Downloader", page_icon="🎵", layout="centered")

# CSS
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); }
h1 { color: #e94560; text-align: center; font-size: 3rem; }
.stButton>button {
    background: linear-gradient(135deg, #e94560, #c23152);
    color: white; border: none; border-radius: 25px;
    padding: 15px 30px; font-size: 1.2rem; font-weight: bold;
    width: 100%; cursor: pointer;
}
.stButton>button:hover { background: linear-gradient(135deg, #c23152, #e94560); transform: scale(1.02); }
.stDownloadButton>button {
    background: linear-gradient(135deg, #00b894, #00a381);
    color: white; border: 2px solid white; border-radius: 25px;
    padding: 15px 30px; font-size: 1.1rem; font-weight: bold;
    width: 100%; animation: glow 2s infinite;
}
@keyframes glow {
    0% { box-shadow: 0 0 10px #00b894; }
    50% { box-shadow: 0 0 30px #00b894; }
    100% { box-shadow: 0 0 10px #00b894; }
}
.stTextInput>div>div>input {
    background: rgba(255,255,255,0.1); border: 2px solid #e94560;
    border-radius: 25px; padding: 15px; color: white; font-size: 1.1rem;
}
.stSelectbox>div>div { background: rgba(255,255,255,0.1); border-radius: 10px; color: white; }
.stProgress>div>div>div { background: linear-gradient(90deg, #e94560, #00b894); }
div[data-testid="stTabs"] button { color: white !important; font-size: 1.2rem !important; }
div[data-testid="stTabs"] button[aria-selected="true"] { background: #e94560 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div style='text-align:center;font-size:5rem;'>🎵</div>", unsafe_allow_html=True)
st.markdown("<h1>Music & Video Downloader</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#aaa;'>Paste URL → Download → Save to Computer</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🎵 Audio", "🎬 Video MP4"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        q = st.selectbox("Quality", ["128", "192", "256", "320"], key="aq")
    with c2:
        f = st.selectbox("Format", ["mp3", "m4a", "wav", "flac", "opus"], key="af")
    
    url = st.text_input("YouTube URL", placeholder="https://youtube.com/watch?v=...", key="au")
    
    if st.button("Download Audio", key="ab"):
        if url:
            try:
                with tempfile.TemporaryDirectory() as tmp:
                    bar = st.progress(0)
                    txt = st.empty()
                    
                    def hook(d):
                        if d['status'] == 'downloading' and d.get('total_bytes'):
                            p = d['downloaded_bytes']/d['total_bytes']
                            bar.progress(min(p, 1.0))
                            txt.text(f"Downloading... {p*100:.0f}%")
                        elif d['status'] == 'finished':
                            bar.progress(1.0)
                            txt.text("Processing...")
                    
                    opts = {
                        'format': 'bestaudio/best',
                        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': f, 'preferredquality': q}],
                        'outtmpl': os.path.join(tmp, '%(title)s.%(ext)s'),
                        'progress_hooks': [hook], 'quiet': True
                    }
                    
                    with yt_dlp.YoutubeDL(opts) as ydl:
                        info = ydl.extract_info(url, download=False)
                        title = info['title']
                        st.info(f"🎵 {title} | ⏱️ {timedelta(seconds=info.get('duration',0))}")
                        ydl.download([url])
                    
                    files = [x for x in os.listdir(tmp) if x.endswith(f)]
                    if files:
                        fp = os.path.join(tmp, files[0])
                        with open(fp, 'rb') as file:
                            data = file.read()
                        st.balloons()
                        st.success(f"Done! {os.path.getsize(fp)/1024/1024:.1f}MB")
                        st.download_button(f"💾 SAVE: {title[:40]}.{f}", data, f"{title}.{f}", f"audio/{f}")
                        st.audio(data)
            except Exception as e:
                st.error(str(e))
        else:
            st.warning("Enter a URL")

with tab2:
    c1, c2 = st.columns(2)
    with c1:
        vq = st.selectbox("Quality", ["Best", "1080p", "720p", "480p", "360p"], key="vq")
    with c2:
        st.markdown("<p style='color:white;margin-top:30px;'>Format: <b>MP4</b></p>", unsafe_allow_html=True)
    
    url2 = st.text_input("YouTube URL", placeholder="https://youtube.com/watch?v=...", key="vu")
    
    if st.button("Download Video MP4", key="vb"):
        if url2:
            try:
                with tempfile.TemporaryDirectory() as tmp:
                    bar = st.progress(0)
                    txt = st.empty()
                    
                    def hook(d):
                        if d['status'] == 'downloading' and d.get('total_bytes'):
                            p = d['downloaded_bytes']/d['total_bytes']
                            bar.progress(min(p, 1.0))
                            txt.text(f"Downloading... {p*100:.0f}%")
                        elif d['status'] == 'finished':
                            bar.progress(1.0)
                            txt.text("Processing...")
                    
                    if vq == "Best":
                        fmt = 'bestvideo+bestaudio/best'
                    else:
                        h = vq.replace('p','')
                        fmt = f'bestvideo[height<={h}]+bestaudio/best[height<={h}]'
                    
                    opts = {
                        'format': fmt, 'merge_output_format': 'mp4',
                        'outtmpl': os.path.join(tmp, '%(title)s.%(ext)s'),
                        'progress_hooks': [hook], 'quiet': True
                    }
                    
                    with yt_dlp.YoutubeDL(opts) as ydl:
                        info = ydl.extract_info(url2, download=False)
                        title = info['title']
                        st.info(f"🎬 {title} | ⏱️ {timedelta(seconds=info.get('duration',0))}")
                        ydl.download([url2])
                    
                    files = [x for x in os.listdir(tmp) if x.endswith('.mp4')]
                    if files:
                        fp = os.path.join(tmp, files[0])
                        with open(fp, 'rb') as file:
                            data = file.read()
                        st.balloons()
                        st.success(f"Done! {os.path.getsize(fp)/1024/1024:.1f}MB")
                        st.download_button(f"💾 SAVE: {title[:40]}.mp4", data, f"{title}.mp4", "video/mp4")
                        if os.path.getsize(fp)/1024/1024 < 50:
                            st.video(data)
            except Exception as e:
                st.error(str(e))
        else:
            st.warning("Enter a URL")
