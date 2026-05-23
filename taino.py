# music_downloader.py
import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import yt_dlp
from PIL import Image, ImageTk
import requests
from io import BytesIO
import re
from datetime import datetime

class MusicDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎵 Music Downloader Pro")
        self.root.geometry("800x600")
        self.root.configure(bg='#1e1e1e')
        self.root.resizable(True, True)
        
        # Set icon (optional)
        try:
            self.root.iconbitmap('music_icon.ico')
        except:
            pass
        
        # Variables
        self.download_path = tk.StringVar(value=str(Path.home() / "Music"))
        self.status_text = tk.StringVar(value="Ready to download...")
        self.progress_value = tk.DoubleVar(value=0)
        self.quality_var = tk.StringVar(value="192")
        self.format_var = tk.StringVar(value="mp3")
        
        # Create GUI elements
        self.create_widgets()
        
        # Create download directory if it doesn't exist
        Path(self.download_path.get()).mkdir(parents=True, exist_ok=True)
        
    def create_widgets(self):
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        bg_color = '#1e1e1e'
        fg_color = '#ffffff'
        accent_color = '#0078d4'
        entry_bg = '#2d2d2d'
        
        style.configure('TFrame', background=bg_color)
        style.configure('TLabel', background=bg_color, foreground=fg_color, font=('Arial', 10))
        style.configure('TButton', background=accent_color, foreground=fg_color, font=('Arial', 10, 'bold'))
        style.configure('TEntry', fieldbackground=entry_bg, foreground=fg_color)
        style.configure('TCombobox', fieldbackground=entry_bg, foreground=fg_color)
        style.configure('TProgressbar', background=accent_color)
        
        # Title Frame
        title_frame = tk.Frame(self.root, bg=bg_color)
        title_frame.pack(pady=(20, 10))
        
        title_label = tk.Label(
            title_frame, 
            text="🎵 Music Downloader Pro", 
            font=('Arial', 24, 'bold'),
            bg=bg_color,
            fg=accent_color
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Download your favorite music in high quality",
            font=('Arial', 10),
            bg=bg_color,
            fg='#999999'
        )
        subtitle_label.pack()
        
        # Main Frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # URL Input
        url_frame = ttk.Frame(main_frame)
        url_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(url_frame, text="Video/Playlist URL:").pack(anchor=tk.W)
        
        url_input_frame = ttk.Frame(main_frame)
        url_input_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.url_entry = ttk.Entry(url_input_frame, font=('Arial', 11))
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
        self.url_entry.insert(0, "https://youtube.com/watch?v=...")
        self.url_entry.bind('<FocusIn>', self.clear_placeholder)
        self.url_entry.bind('<FocusOut>', self.add_placeholder)
        
        # Options Frame
        options_frame = ttk.Frame(main_frame)
        options_frame.pack(fill=tk.X, pady=10)
        
        # Left options
        left_options = ttk.Frame(options_frame)
        left_options.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Download Path
        ttk.Label(left_options, text="Save Location:").pack(anchor=tk.W)
        path_frame = ttk.Frame(left_options)
        path_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.path_entry = ttk.Entry(path_frame, textvariable=self.download_path, state='readonly')
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
        
        browse_btn = ttk.Button(path_frame, text="📁 Browse", command=self.browse_folder)
        browse_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Right options
        right_options = ttk.Frame(options_frame)
        right_options.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(20, 0))
        
        # Quality selection
        quality_frame = ttk.Frame(right_options)
        quality_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(quality_frame, text="Audio Quality:").pack(side=tk.LEFT)
        quality_combo = ttk.Combobox(
            quality_frame, 
            textvariable=self.quality_var,
            values=["128", "192", "256", "320"],
            state='readonly',
            width=8
        )
        quality_combo.pack(side=tk.RIGHT)
        
        # Format selection
        format_frame = ttk.Frame(right_options)
        format_frame.pack(fill=tk.X)
        
        ttk.Label(format_frame, text="Format:").pack(side=tk.LEFT)
        format_combo = ttk.Combobox(
            format_frame,
            textvariable=self.format_var,
            values=["mp3", "m4a", "wav", "flac", "opus"],
            state='readonly',
            width=8
        )
        format_combo.pack(side=tk.RIGHT)
        
        # Download Button
        self.download_btn = ttk.Button(
            main_frame,
            text="⬇️ Download Music",
            command=self.start_download,
            style='TButton'
        )
        self.download_btn.pack(pady=20, ipady=10, fill=tk.X)
        
        # Progress Frame
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=10)
        
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_value,
            mode='indeterminate',
            length=100
        )
        self.progress_bar.pack(fill=tk.X)
        
        # Status Label
        self.status_label = ttk.Label(
            main_frame,
            textvariable=self.status_text,
            font=('Arial', 9),
            foreground='#999999'
        )
        self.status_label.pack()
        
        # History Frame
        history_frame = ttk.LabelFrame(main_frame, text="Download History", padding="10")
        history_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        # Create Treeview for history
        self.history_tree = ttk.Treeview(
            history_frame,
            columns=("Title", "Status", "Time"),
            show="headings",
            height=8
        )
        
        self.history_tree.heading("Title", text="Title")
        self.history_tree.heading("Status", text="Status")
        self.history_tree.heading("Time", text="Time")
        
        self.history_tree.column("Title", width=400)
        self.history_tree.column("Status", width=100)
        self.history_tree.column("Time", width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Credits
        credit_label = tk.Label(
            self.root,
            text="Made with ❤️ using Python | For personal use only",
            font=('Arial', 8),
            bg=bg_color,
            fg='#666666'
        )
        credit_label.pack(side=tk.BOTTOM, pady=5)
        
    def clear_placeholder(self, event):
        if self.url_entry.get() == "https://youtube.com/watch?v=...":
            self.url_entry.delete(0, tk.END)
            self.url_entry.configure(foreground='white')
            
    def add_placeholder(self, event):
        if not self.url_entry.get():
            self.url_entry.insert(0, "https://youtube.com/watch?v=...")
            self.url_entry.configure(foreground='gray')
            
    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.download_path.get())
        if folder:
            self.download_path.set(folder)
            
    def progress_hook(self, d):
        if d['status'] == 'downloading':
            try:
                # Extract percentage from download progress
                if 'downloaded_bytes' in d and 'total_bytes' in d:
                    percentage = (d['downloaded_bytes'] / d['total_bytes']) * 100
                    self.progress_value.set(percentage)
                    self.status_text.set(f"Downloading: {d.get('filename', 'Unknown')} - {percentage:.1f}%")
            except:
                pass
        elif d['status'] == 'finished':
            self.progress_value.set(100)
            self.status_text.set("Processing audio...")
            
    def download_music(self):
        url = self.url_entry.get().strip()
        
        if not url or url == "https://youtube.com/watch?v=...":
            self.show_error("Please enter a valid URL")
            return
            
        try:
            # Configure yt-dlp options
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': self.format_var.get(),
                    'preferredquality': self.quality_var.get(),
                }],
                'outtmpl': os.path.join(
                    self.download_path.get(),
                    '%(title)s.%(ext)s'
                ),
                'progress_hooks': [self.progress_hook],
                'quiet': True,
                'no_warnings': True,
            }
            
            self.status_text.set("Starting download...")
            self.progress_bar['mode'] = 'determinate'
            self.progress_value.set(0)
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Get video info first
                self.status_text.set("Fetching video information...")
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'Unknown Title')
                
                # Add to history
                self.add_to_history(title, "Downloading...", datetime.now().strftime("%H:%M:%S"))
                
                # Download the video
                self.status_text.set(f"Downloading: {title}")
                ydl.download([url])
                
            self.status_text.set(f"✅ Successfully downloaded: {title}")
            self.update_history_status(title, "Completed")
            messagebox.showinfo("Success", f"Music downloaded successfully!\n\n{title}")
            
        except Exception as e:
            error_msg = str(e)
            self.status_text.set(f"❌ Error: {error_msg[:50]}...")
            self.update_history_status("", "Failed")
            self.show_error(f"Download failed: {error_msg}")
            
        finally:
            self.progress_bar['mode'] = 'indeterminate'
            self.progress_value.set(0)
            self.download_btn['state'] = 'normal'
            
    def start_download(self):
        self.download_btn['state'] = 'disabled'
        thread = threading.Thread(target=self.download_music)
        thread.daemon = True
        thread.start()
        
    def add_to_history(self, title, status, time):
        self.history_tree.insert("", 0, values=(title[:50], status, time))
        
    def update_history_status(self, title, status):
        # Update the most recent entry
        items = self.history_tree.get_children()
        if items:
            values = list(self.history_tree.item(items[0])['values'])
            values[1] = status
            self.history_tree.item(items[0], values=values)
            
    def show_error(self, message):
        messagebox.showerror("Error", message)

def main():
    # Check if yt-dlp is installed
    try:
        import yt_dlp
    except ImportError:
        print("Installing required packages...")
        os.system("pip install yt-dlp")
        
    # Check if PIL is installed
    try:
        from PIL import Image
    except ImportError:
        os.system("pip install Pillow")
        
    root = tk.Tk()
    app = MusicDownloaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
