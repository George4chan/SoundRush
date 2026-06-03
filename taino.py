# youtube_audio_downloader.py

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import yt_dlp
import threading
import os
from pathlib import Path

class YouTubeAudioDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Audio Downloader")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Set icon (optional)
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
        
        # Variables
        self.download_path = tk.StringVar(value=str(Path.home() / "Downloads"))
        self.status_text = tk.StringVar(value="Ready")
        self.progress_var = tk.DoubleVar()
        
        # Create GUI
        self.create_widgets()
        
        # Configure styles
        style = ttk.Style()
        style.theme_use('clam')
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # URL Input
        ttk.Label(main_frame, text="YouTube URL:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.url_entry = ttk.Entry(main_frame, width=50, font=('Arial', 10))
        self.url_entry.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        # Format selection
        ttk.Label(main_frame, text="Audio Format:", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.format_var = tk.StringVar(value="mp3")
        format_frame = ttk.Frame(main_frame)
        format_frame.grid(row=1, column=1, columnspan=2, sticky=tk.W, pady=5, padx=(5, 0))
        
        ttk.Radiobutton(format_frame, text="MP3", variable=self.format_var, value="mp3").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(format_frame, text="M4A", variable=self.format_var, value="m4a").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(format_frame, text="WEBM", variable=self.format_var, value="webm").pack(side=tk.LEFT, padx=5)
        
        # Quality selection
        ttk.Label(main_frame, text="Audio Quality:", font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.quality_var = tk.StringVar(value="best")
        quality_frame = ttk.Frame(main_frame)
        quality_frame.grid(row=2, column=1, columnspan=2, sticky=tk.W, pady=5, padx=(5, 0))
        
        ttk.Radiobutton(quality_frame, text="Best", variable=self.quality_var, value="best").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(quality_frame, text="High (192k)", variable=self.quality_var, value="192").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(quality_frame, text="Medium (128k)", variable=self.quality_var, value="128").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(quality_frame, text="Low (64k)", variable=self.quality_var, value="64").pack(side=tk.LEFT, padx=5)
        
        # Download location
        ttk.Label(main_frame, text="Save to:", font=('Arial', 10, 'bold')).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.path_entry = ttk.Entry(main_frame, textvariable=self.download_path, width=40)
        self.path_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        ttk.Button(main_frame, text="Browse", command=self.browse_folder, width=10).grid(row=3, column=2, pady=5, padx=5)
        
        # Download button
        self.download_btn = ttk.Button(main_frame, text="Download Audio", command=self.start_download, width=20)
        self.download_btn.grid(row=4, column=0, columnspan=3, pady=20)
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Status label
        ttk.Label(main_frame, textvariable=self.status_text, font=('Arial', 9)).grid(row=6, column=0, columnspan=3, pady=5)
        
        # Information frame
        info_frame = ttk.LabelFrame(main_frame, text="Information", padding="10")
        info_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        info_text = """
• Supports YouTube, YouTube Music, and other yt-dlp compatible sites
• Downloads best available audio quality
• Files are saved with video title as filename
• MP3 format may require ffmpeg installation
        """
        ttk.Label(info_frame, text=info_text, justify=tk.LEFT, font=('Arial', 8)).grid(row=0, column=0, sticky=tk.W)
        
    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.download_path.get())
        if folder:
            self.download_path.set(folder)
    
    def progress_hook(self, d):
        if d['status'] == 'downloading':
            if 'total_bytes' in d:
                percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
                self.progress_var.set(percent)
                self.status_text.set(f"Downloading: {percent:.1f}%")
            elif 'total_bytes_estimate' in d:
                percent = (d['downloaded_bytes'] / d['total_bytes_estimate']) * 100
                self.progress_var.set(percent)
                self.status_text.set(f"Downloading: {percent:.1f}%")
        elif d['status'] == 'finished':
            self.status_text.set("Processing audio...")
            self.progress_var.set(100)
        elif d['status'] == 'error':
            self.status_text.set("Error occurred!")
    
    def start_download(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
        
        # Disable download button during download
        self.download_btn.config(state=tk.DISABLED)
        self.progress_var.set(0)
        
        # Start download in separate thread
        thread = threading.Thread(target=self.download_audio, args=(url,))
        thread.daemon = True
        thread.start()
    
    def download_audio(self, url):
        try:
            output_template = os.path.join(self.download_path.get(), '%(title)s.%(ext)s')
            
            # Configure yt-dlp options
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': self.format_var.get(),
                    'preferredquality': self.quality_var.get(),
                }],
                'outtmpl': output_template,
                'progress_hooks': [self.progress_hook],
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
            }
            
            # If quality is 'best', don't specify bitrate
            if self.quality_var.get() != 'best':
                ydl_opts['postprocessors'][0]['preferredquality'] = self.quality_var.get()
            
            self.status_text.set("Starting download...")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extract info for title
                info = ydl.extract_info(url, download=False)
                video_title = info.get('title', 'audio')
                self.status_text.set(f"Downloading: {video_title}")
                
                # Download the audio
                ydl.download([url])
            
            # Reset UI after download
            self.root.after(0, self.download_complete, True, video_title)
            
        except Exception as e:
            self.root.after(0, self.download_complete, False, str(e))
    
    def download_complete(self, success, message):
        self.download_btn.config(state=tk.NORMAL)
        self.progress_var.set(0)
        
        if success:
            messagebox.showinfo("Success", f"Audio downloaded successfully!\nFile: {message}")
            self.status_text.set("Download completed!")
            self.url_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", f"Download failed:\n{message}")
            self.status_text.set("Download failed!")

def main():
    root = tk.Tk()
    app = YouTubeAudioDownloader(root)
    root.mainloop()

if __name__ == "__main__":
    main()
