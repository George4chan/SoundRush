import streamlit as st
import os
import tempfile
import yt_dlp
from datetime import timedelta

st.set_page_config(page_title="Music Downloader", page_icon="🎵", layout="centered")

st.title("🎵 Music Downloader")
st.write("Download audio and video from YouTube")

tab1, tab2 = st.tabs(["Audio", "Video (MP4)"])

with tab1:
    url = st.text_input("YouTube URL", key="url1")
    col1, col2 = st.columns(2)
    with col1:
        quality = st.selectbox("Quality", ["128", "192", "256", "320"], key="q1")
    with col2:
        fmt = st.selectbox("Format", ["mp3", "m4a", "wav"], key="f1")
    
    if st.button("Download Audio", key="btn1"):
        if url:
            with tempfile.TemporaryDirectory() as tmp:
                with st.spinner("Downloading..."):
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': fmt, 'preferredquality': quality}],
                        'outtmpl': os.path.join(tmp, '%(title)s.%(ext)s'),
                        'quiet': True
                    }
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=False)
                        ydl.download([url])
                    
                    files = os.listdir(tmp)
                    if files:
                        with open(os.path.join(tmp, files[0]), 'rb') as f:
                            data = f.read()
                        st.success(f"Downloaded: {info['title']}")
                        st.download_button("Save File", data, f"{info['title']}.{fmt}", f"audio/{fmt}")
                        st.audio(data)

with tab2:
    url2 = st.text_input("YouTube URL", key="url2")
    quality2 = st.selectbox("Quality", ["Best", "1080p", "720p", "480p", "360p"], key="q2")
    
    if st.button("Download Video (MP4)", key="btn2"):
        if url2:
            with tempfile.TemporaryDirectory() as tmp:
                with st.spinner("Downloading..."):
                    if quality2 == "Best":
                        fmt_str = 'best'
                    else:
                        h = quality2.replace('p','')
                        fmt_str = f'best[height<={h}]'
                    
                    ydl_opts = {
                        'format': fmt_str,
                        'merge_output_format': 'mp4',
                        'outtmpl': os.path.join(tmp, '%(title)s.%(ext)s'),
                        'quiet': True
                    }
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url2, download=False)
                        ydl.download([url2])
                    
                    files = [f for f in os.listdir(tmp) if f.endswith('.mp4')]
                    if files:
                        with open(os.path.join(tmp, files[0]), 'rb') as f:
                            data = f.read()
                        st.success(f"Downloaded: {info['title']}")
                        st.download_button("Save File", data, f"{info['title']}.mp4", "video/mp4")
                        st.video(data)
