# streamlit_app.py - For Streamlit Cloud ONLY

import streamlit as st
import yt_dlp
import tempfile
import os

st.set_page_config(page_title="YouTube Audio Downloader", page_icon="🎵")

st.title("🎵 YouTube Audio Downloader")
st.markdown("Download audio from YouTube videos")

# Input URL
url = st.text_input("Enter YouTube URL:", placeholder="https://www.youtube.com/watch?v=...")

# Options
col1, col2 = st.columns(2)
with col1:
    format_option = st.selectbox("Audio Format:", ["mp3", "m4a", "aac", "opus"])
with col2:
    quality_option = st.selectbox("Quality:", ["320", "256", "192", "128", "64"], index=2)

if st.button("Download Audio", type="primary"):
    if not url:
        st.error("Please enter a YouTube URL")
    else:
        with st.spinner("Processing... This may take a moment"):
            try:
                # Create temp directory
                temp_dir = tempfile.mkdtemp()
                
                # Download options
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': format_option,
                        'preferredquality': quality_option,
                    }],
                    'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                    'quiet': True,
                }
                
                # Download
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    
                    # Find the file
                    for file in os.listdir(temp_dir):
                        if file.endswith(f".{format_option}"):
                            file_path = os.path.join(temp_dir, file)
                            
                            # Read file
                            with open(file_path, 'rb') as f:
                                audio_data = f.read()
                            
                            # Show success
                            st.success(f"✅ Ready: {info.get('title', 'audio')}")
                            
                            # Download button
                            st.download_button(
                                label="💾 Save Audio File",
                                data=audio_data,
                                file_name=file,
                                mime=f"audio/{format_option}"
                            )
                            
                            # Clean up
                            os.remove(file_path)
                            os.rmdir(temp_dir)
                            break
                            
            except Exception as e:
                st.error(f"Download failed: {str(e)}")
                st.info("Try a different video or check the URL")

# Instructions
with st.expander("📖 How to use"):
    st.markdown("""
    1. Copy a YouTube video URL
    2. Choose audio format (MP3 recommended)
    3. Select quality
    4. Click download
    5. Wait for processing
    6. Click "Save Audio File"
    
    **Note:** Some videos may be restricted from downloading.
    """)
