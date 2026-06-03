# simplified_downloader.py

import streamlit as st
import yt_dlp
import tempfile
import os

st.set_page_config(page_title="YouTube Audio Downloader", page_icon="🎵")

st.title("🎵 YouTube Audio Downloader")

url = st.text_input("Enter YouTube URL")

if st.button("Download"):
    if url:
        with st.spinner("Downloading..."):
            temp_dir = tempfile.mkdtemp()
            
            # Download best audio without conversion (keeps original format)
            ydl_opts = {
                'format': 'bestaudio',
                'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                'quiet': True,
            }
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    
                    # Find downloaded file
                    for file in os.listdir(temp_dir):
                        file_path = os.path.join(temp_dir, file)
                        with open(file_path, 'rb') as f:
                            audio_data = f.read()
                        
                        st.success(f"Downloaded: {info.get('title', 'audio')}")
                        st.download_button(
                            label="Save File",
                            data=audio_data,
                            file_name=file,
                            mime="audio/mpeg"
                        )
                        break
                        
                    # Cleanup
                    os.remove(file_path)
                    os.rmdir(temp_dir)
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")
