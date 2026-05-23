"""
Music Downloader Pro - Complete All-in-One Application
Includes logo generation and full music downloader functionality
"""

import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ====================================================================
# LOGO GENERATOR SECTION
# ====================================================================

def generate_logo():
    """Generate the application logo automatically"""
    try:
        from PIL import Image, ImageDraw, ImageFont, ImageFilter
        
        print("Generating application logo...")
        
        size = 512
        logo = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(logo)
        
        # Color scheme
        gradient_start = (33, 150, 243, 255)
        gradient_end = (0, 120, 212, 255)
        white = (255, 255, 255, 255)
        accent_blue = (0, 120, 212, 255)
        
        center = size // 2
        radius = 200
        
        # Create gradient background circle
        print("  Creating gradient background...")
        for i in range(radius, 0, -1):
            ratio = i / radius
            r = int(gradient_start[0] * ratio + gradient_end[0] * (1 - ratio))
            g = int(gradient_start[1] * ratio + gradient_end[1] * (1 - ratio))
            b = int(gradient_start[2] * ratio + gradient_end[2] * (1 - ratio))
            draw.ellipse([center - i, center - i, center + i, center + i], 
                        fill=(r, g, b, 255))
        
        # Add outer glow effect
        print("  Adding glow effects...")
        glow = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow)
        
        for i in range(15):
            glow_radius = radius + i * 2
            glow_opacity = int(60 - i * 4)
            glow_color = (33, 150, 243, max(0, glow_opacity))
            glow_draw.ellipse(
                [center - glow_radius, center - glow_radius,
                 center + glow_radius, center + glow_radius],
                outline=glow_color,
                width=4
            )
        
        logo = Image.alpha_composite(glow, logo)
        
        # Draw main music note
        print("  Drawing music notes...")
        note_x = center - 40
        note_y = center - 80
        
        # Note head
        draw.ellipse([note_x - 35, note_y + 30, note_x + 35, note_y + 100], 
                    fill=white)
        
        # Note stem
        draw.rectangle([note_x + 25, note_y - 60, note_x + 35, note_y + 30], 
                      fill=white)
        
        # Note flag
        flag_points = [
            (note_x + 35, note_y - 60),
            (note_x + 35, note_y - 25),
            (note_x + 75, note_y - 42),
        ]
        draw.polygon(flag_points, fill=white)
        
        # Additional smaller notes
        # Second note
        note2_x = center + 60
        note2_y = center - 90
        draw.ellipse([note2_x - 22, note2_y + 15, note2_x + 22, note2_y + 59], 
                    fill=white)
        draw.rectangle([note2_x + 14, note_y - 45, note2_x + 22, note2_y + 15], 
                      fill=white)
        
        # Third note
        note3_x = center - 90
        note3_y = center + 30
        draw.ellipse([note3_x - 20, note3_y + 12, note3_x + 20, note3_y + 52], 
                    fill=white)
        draw.rectangle([note3_x + 12, note3_y - 38, note3_x + 20, note3_y + 12], 
                      fill=white)
        
        # Sound waves
        print("  Adding sound waves...")
        wave_x = center + 50
        wave_y = center - 30
        
        for i in range(3):
            wave_size = 35 + i * 30
            wave_opacity = 200 - i * 50
            wave_color = (*white[:3], wave_opacity)
            
            bbox = [wave_x - wave_size, wave_y - wave_size,
                   wave_x + wave_size, wave_y + wave_size]
            
            if i == 0:
                draw.arc(bbox, start=265, end=325, fill=wave_color, width=5)
            elif i == 1:
                draw.arc(bbox, start=270, end=320, fill=wave_color, width=4)
            else:
                draw.arc(bbox, start=275, end=315, fill=wave_color, width=3)
        
        # Download arrow
        print("  Adding download indicator...")
        arrow_x = center
        arrow_y = center + 70
        
        # Arrow body
        draw.rectangle([arrow_x - 8, arrow_y - 35, arrow_x + 8, arrow_y + 10], 
                      fill=white)
        
        # Arrow head
        arrow_points = [
            (arrow_x - 22, arrow_y - 8),
            (arrow_x, arrow_y + 18),
            (arrow_x + 22, arrow_y - 8),
        ]
        draw.polygon(arrow_points, fill=white)
        
        # Download bar
        draw.rectangle([arrow_x - 30, arrow_y + 18, arrow_x + 30, arrow_y + 24], 
                      fill=white)
        
        # Add text
        print("  Adding text...")
        try:
            # Try multiple font options
            font_options = [
                "arialbd.ttf", "Arial Bold.ttf", "arial.ttf", "Arial.ttf",
                "DejaVuSans-Bold.ttf", "DejaVuSans.ttf"
            ]
            
            music_font = None
            downloader_font = None
            
            for font_name in font_options:
                try:
                    if music_font is None and "bold" in font_name.lower():
                        music_font = ImageFont.truetype(font_name, 38)
                    elif downloader_font is None:
                        downloader_font = ImageFont.truetype(font_name, 30)
                except:
                    continue
            
            if music_font is None:
                music_font = ImageFont.load_default()
            if downloader_font is None:
                downloader_font = ImageFont.load_default()
                
        except:
            music_font = ImageFont.load_default()
            downloader_font = ImageFont.load_default()
        
        # Create text layer
        text_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        text_draw = ImageDraw.Draw(text_img)
        
        # "MUSIC" text
        music_text = "MUSIC"
        bbox = text_draw.textbbox((0, 0), music_text, font=music_font)
        text_width = bbox[2] - bbox[0]
        text_x = center - text_width // 2
        text_y = center + 120
        
        # Shadow
        text_draw.text((text_x + 2, text_y + 2), music_text, 
                      font=music_font, fill=(0, 0, 0, 100))
        # Main text
        text_draw.text((text_x, text_y), music_text, font=music_font, fill=white)
        
        # "DOWNLOADER" text
        down_text = "DOWNLOADER"
        bbox = text_draw.textbbox((0, 0), down_text, font=downloader_font)
        down_width = bbox[2] - bbox[0]
        down_x = center - down_width // 2
        down_y = text_y + 48
        
        # Shadow
        text_draw.text((down_x + 1, down_y + 1), down_text, 
                      font=downloader_font, fill=(0, 0, 0, 100))
        # Main text
        text_draw.text((down_x, down_y), down_text, 
                      font=downloader_font, fill=(255, 255, 255, 220))
        
        # Composite text onto logo
        logo = Image.alpha_composite(logo, text_img)
        
        # Add decorative dots
        print("  Adding finishing touches...")
        dot_positions = [
            (center - 110, center - 140),
            (center + 110, center - 110),
            (center - 130, center + 110),
            (center + 140, center + 90),
        ]
        
        for pos in dot_positions:
            for r in range(4, 0, -1):
                opacity = int(180 - (4 - r) * 40)
                draw.ellipse([pos[0] - r, pos[1] - r, 
                            pos[0] + r, pos[1] + r], 
                           fill=(255, 255, 255, opacity))
        
        # Save logos in different sizes
        print("  Saving logo files...")
        logo_256 = logo.resize((256, 256), Image.Resampling.LANCZOS)
        logo_128 = logo.resize((128, 128), Image.Resampling.LANCZOS)
        logo_64 = logo.resize((64, 64), Image.Resampling.LANCZOS)
        logo_32 = logo.resize((32, 32), Image.Resampling.LANCZOS)
        
        logo_256.save('app_logo.png', 'PNG')
        logo_128.save('app_logo_128.png', 'PNG')
        logo_64.save('app_logo_64.png', 'PNG')
        logo_32.save('app_logo_32.png', 'PNG')
        
        # Save ICO for Windows
        try:
            logo_256.save('app_logo.ico', 'ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32)])
        except:
            logo_256.save('app_logo.ico', 'ICO')
        
        print("  ✅ Logo generated successfully!")
        return True
        
    except ImportError as e:
        print(f"  ⚠️ PIL/Pillow not installed. Skipping logo generation.")
        print(f"  Install with: pip install Pillow")
        return False
    except Exception as e:
        print(f"  ⚠️ Could not generate logo: {e}")
        return False


# ====================================================================
# MUSIC DOWNLOADER APP SECTION
# ====================================================================

class MusicDownloaderApp:
    """Main Music Downloader Application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🎵 Music Downloader Pro")
        self.root.geometry("900x650")
        self.root.configure(bg='#1e1e1e')
        self.root.minsize(800, 600)
        
        # Set window icon
        self.set_app_icon()
        
        # Variables
        self.download_path = tk.StringVar(value=str(Path.home() / "Music"))
        self.status_text = tk.StringVar(value="Ready to download...")
        self.progress_value = tk.DoubleVar(value=0)
        self.quality_var = tk.StringVar(value="192")
        self.format_var = tk.StringVar(value="mp3")
        
        # Create GUI
        self.create_widgets()
        
        # Create download directory
        Path(self.download_path.get()).mkdir(parents=True, exist_ok=True)
        
        # Check for FFmpeg
        self.check_ffmpeg()
        
    def set_app_icon(self):
        """Set application icon"""
        try:
            # Try different icon files
            icon_files = ['app_logo.ico', 'app_logo.png', 'app_logo_64.png']
            for icon_file in icon_files:
                if os.path.exists(icon_file):
                    if icon_file.endswith('.ico'):
                        self.root.iconbitmap(icon_file)
                    else:
                        from PIL import Image, ImageTk
                        img = Image.open(icon_file)
                        photo = ImageTk.PhotoImage(img)
                        self.root.iconphoto(True, photo)
                    print(f"  ✅ Icon loaded: {icon_file}")
                    return
        except Exception as e:
            print(f"  ⚠️ Could not set icon: {e}")
    
    def check_ffmpeg(self):
        """Check if FFmpeg is installed"""
        import subprocess
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        except:
            messagebox.showwarning(
                "FFmpeg Not Found",
                "FFmpeg is required for audio conversion.\n\n"
                "Please install FFmpeg:\n"
                "• Windows: Download from ffmpeg.org\n"
                "• macOS: brew install ffmpeg\n"
                "• Linux: sudo apt install ffmpeg"
            )
    
    def create_widgets(self):
        """Create all GUI widgets"""
        bg_color = '#1e1e1e'
        fg_color = '#ffffff'
        accent_color = '#0078d4'
        entry_bg = '#2d2d2d'
        secondary_bg = '#252525'
        
        # Custom styles
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background=bg_color)
        style.configure('TLabel', background=bg_color, foreground=fg_color, font=('Segoe UI', 10))
        style.configure('TLabelframe', background=bg_color, foreground=fg_color)
        style.configure('TLabelframe.Label', background=bg_color, foreground=fg_color, font=('Segoe UI', 10, 'bold'))
        style.configure('TEntry', fieldbackground=entry_bg, foreground=fg_color, insertcolor=fg_color)
        style.configure('TCombobox', fieldbackground=entry_bg, foreground=fg_color)
        style.configure('TProgressbar', background=accent_color, troughcolor=secondary_bg)
        style.configure('Accent.TButton', background=accent_color, foreground=fg_color, 
                       font=('Segoe UI', 10, 'bold'), borderwidth=0)
        style.map('Accent.TButton', background=[('active', '#005a9e')])
        
        # ===== HEADER =====
        header_frame = tk.Frame(self.root, bg=bg_color, height=100)
        header_frame.pack(fill=tk.X, pady=(20, 10))
        header_frame.pack_propagate(False)
        
        # Try to load and display logo
        logo_displayed = False
        try:
            from PIL import Image, ImageTk
            logo_files = ['app_logo_128.png', 'app_logo.png']
            for logo_file in logo_files:
                if os.path.exists(logo_file):
                    img = Image.open(logo_file)
                    img = img.resize((80, 80), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    logo_label = tk.Label(header_frame, image=photo, bg=bg_color)
                    logo_label.image = photo
                    logo_label.pack(side=tk.LEFT, padx=(20, 10))
                    logo_displayed = True
                    break
        except:
            pass
        
        # Title
        title_container = tk.Frame(header_frame, bg=bg_color)
        title_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        title_label = tk.Label(
            title_container, 
            text="Music Downloader Pro", 
            font=('Segoe UI', 28, 'bold'),
            bg=bg_color,
            fg=accent_color
        )
        title_label.pack(anchor=tk.W)
        
        subtitle_label = tk.Label(
            title_container,
            text="Download high-quality music from your favorite platforms",
            font=('Segoe UI', 10),
            bg=bg_color,
            fg='#999999'
        )
        subtitle_label.pack(anchor=tk.W)
        
        # ===== MAIN CONTENT =====
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # URL Input Section
        url_section = ttk.LabelFrame(main_frame, text=" URL Input ", padding="15")
        url_section.pack(fill=tk.X, pady=(0, 15))
        
        self.url_entry = ttk.Entry(url_section, font=('Segoe UI', 11))
        self.url_entry.pack(fill=tk.X, ipady=8)
        self.url_entry.insert(0, "Paste YouTube or music URL here...")
        self.url_entry.bind('<FocusIn>', self.clear_placeholder)
        self.url_entry.bind('<FocusOut>', self.add_placeholder)
        self.url_entry.configure(foreground='gray')
        
        # Options Section
        options_frame = ttk.Frame(main_frame)
        options_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Left column - Save location
        left_options = ttk.LabelFrame(options_frame, text=" Save Location ", padding="10")
        left_options.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        path_frame = ttk.Frame(left_options)
        path_frame.pack(fill=tk.X)
        
        self.path_entry = ttk.Entry(path_frame, textvariable=self.download_path, 
                                    state='readonly', font=('Segoe UI', 9))
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
        
        browse_btn = tk.Button(
            path_frame, text="📁 Browse", command=self.browse_folder,
            bg=accent_color, fg=fg_color, font=('Segoe UI', 9),
            relief=tk.FLAT, padx=15, pady=5, cursor='hand2'
        )
        browse_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Right column - Quality settings
        right_options = ttk.LabelFrame(options_frame, text=" Audio Settings ", padding="10")
        right_options.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        settings_grid = ttk.Frame(right_options)
        settings_grid.pack(fill=tk.X)
        
        # Quality
        ttk.Label(settings_grid, text="Quality:", font=('Segoe UI', 10)).grid(row=0, column=0, sticky=tk.W, pady=5)
        quality_combo = ttk.Combobox(
            settings_grid, textvariable=self.quality_var,
            values=["128 kbps", "192 kbps", "256 kbps", "320 kbps"],
            state='readonly', width=12
        )
        quality_combo.set("192 kbps")
        quality_combo.grid(row=0, column=1, padx=(10, 20), pady=5)
        
        # Format
        ttk.Label(settings_grid, text="Format:", font=('Segoe UI', 10)).grid(row=0, column=2, sticky=tk.W, pady=5)
        format_combo = ttk.Combobox(
            settings_grid, textvariable=self.format_var,
            values=["mp3", "m4a", "wav", "flac", "opus"],
            state='readonly', width=12
        )
        format_combo.set("mp3")
        format_combo.grid(row=0, column=3, padx=(10, 0), pady=5)
        
        # Download Button
        self.download_btn = tk.Button(
            main_frame,
            text="⬇️  DOWNLOAD MUSIC",
            command=self.start_download,
            bg=accent_color,
            fg=fg_color,
            font=('Segoe UI', 12, 'bold'),
            relief=tk.FLAT,
            padx=30,
            pady=12,
            cursor='hand2'
        )
        self.download_btn.pack(pady=15, fill=tk.X)
        
        # Progress Section
        progress_section = ttk.LabelFrame(main_frame, text=" Progress ", padding="10")
        progress_section.pack(fill=tk.X, pady=(0, 15))
        
        self.progress_bar = ttk.Progressbar(
            progress_section,
            variable=self.progress_value,
            mode='indeterminate',
            length=100
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))
        
        self.status_label = ttk.Label(
            progress_section,
            textvariable=self.status_text,
            font=('Segoe UI', 9),
            foreground='#00cc00'
        )
        self.status_label.pack()
        
        # History Section
        history_frame = ttk.LabelFrame(main_frame, text=" Download History ", padding="10")
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create Treeview with scrollbar
        tree_container = ttk.Frame(history_frame)
        tree_container.pack(fill=tk.BOTH, expand=True)
        
        self.history_tree = ttk.Treeview(
            tree_container,
            columns=("#", "Title", "Format", "Status", "Time"),
            show="headings",
            height=10
        )
        
        # Configure columns
        self.history_tree.heading("#", text="#")
        self.history_tree.heading("Title", text="Title")
        self.history_tree.heading("Format", text="Format")
        self.history_tree.heading("Status", text="Status")
        self.history_tree.heading("Time", text="Time")
        
        self.history_tree.column("#", width=40, anchor='center')
        self.history_tree.column("Title", width=350)
        self.history_tree.column("Format", width=80, anchor='center')
        self.history_tree.column("Status", width=100, anchor='center')
        self.history_tree.column("Time", width=150, anchor='center')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_container, orient=tk.VERTICAL, 
                                 command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure tag for completed downloads
        self.history_tree.tag_configure('completed', foreground='#00cc00')
        self.history_tree.tag_configure('failed', foreground='#ff4444')
        
        # Counter for history
        self.download_counter = 0
        
        # ===== FOOTER =====
        footer_frame = tk.Frame(self.root, bg=bg_color, height=30)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=5)
        
        footer_text = tk.Label(
            footer_frame,
            text="Made with ❤️ in Python | For personal use only | Respect copyright laws",
            font=('Segoe UI', 8),
            bg=bg_color,
            fg='#666666'
        )
        footer_text.pack()
    
    def clear_placeholder(self, event):
        if self.url_entry.get() == "Paste YouTube or music URL here...":
            self.url_entry.delete(0, tk.END)
            self.url_entry.configure(foreground='white')
    
    def add_placeholder(self, event):
        if not self.url_entry.get():
            self.url_entry.insert(0, "Paste YouTube or music URL here...")
            self.url_entry.configure(foreground='gray')
    
    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.download_path.get())
        if folder:
            self.download_path.set(folder)
            Path(folder).mkdir(parents=True, exist_ok=True)
    
    def progress_hook(self, d):
        """Handle download progress updates"""
        if d['status'] == 'downloading':
            try:
                if 'total_bytes' in d and d['total_bytes']:
                    percentage = (d['downloaded_bytes'] / d['total_bytes']) * 100
                    self.progress_value.set(percentage)
                    
                    # Format file size
                    downloaded_mb = d['downloaded_bytes'] / (1024 * 1024)
                    total_mb = d['total_bytes'] / (1024 * 1024)
                    
                    self.status_text.set(
                        f"Downloading... {downloaded_mb:.1f}MB / {total_mb:.1f}MB ({percentage:.1f}%)"
                    )
                elif 'downloaded_bytes' in d:
                    downloaded_mb = d['downloaded_bytes'] / (1024 * 1024)
                    self.status_text.set(f"Downloading... {downloaded_mb:.1f}MB downloaded")
            except Exception as e:
                self.status_text.set("Downloading...")
                
        elif d['status'] == 'finished':
            self.progress_value.set(100)
            self.status_text.set("Processing and converting audio...")
    
    def download_music(self):
        """Main download function"""
        url = self.url_entry.get().strip()
        
        if not url or url == "Paste YouTube or music URL here...":
            self.show_error("Please enter a valid URL")
            self.download_btn.configure(state=tk.NORMAL, bg='#0078d4')
            return
        
        try:
            # Import yt-dlp
            import yt_dlp
            
            # Extract quality value
            quality = self.quality_var.get().replace(" kbps", "")
            
            # Configure options
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': self.format_var.get(),
                    'preferredquality': quality,
                }],
                'outtmpl': os.path.join(
                    self.download_path.get(),
                    '%(title)s.%(ext)s'
                ),
                'progress_hooks': [self.progress_hook],
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
            }
            
            self.progress_bar['mode'] = 'determinate'
            self.progress_value.set(0)
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Get info first
                self.status_text.set("Fetching video information...")
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'Unknown Title')[:50]
                
                # Add to history
                self.download_counter += 1
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                
                item_id = self.history_tree.insert(
                    "", 0,
                    values=(self.download_counter, title, 
                           self.format_var.get().upper(), "Downloading...", current_time)
                )
                
                # Download
                self.status_text.set(f"Downloading: {title}")
                ydl.download([url])
            
            # Success
            self.status_text.set(f"✅ Successfully downloaded: {title}")
            self.status_label.configure(foreground='#00cc00')
            
            # Update history
            self.history_tree.set(item_id, "Status", "✅ Complete")
            self.history_tree.item(item_id, tags=('completed',))
            
            messagebox.showinfo(
                "Download Complete",
                f"✅ Music downloaded successfully!\n\n"
                f"📁 Location: {self.download_path.get()}\n"
                f"🎵 Title: {title}\n"
                f"🎧 Format: {self.format_var.get().upper()}\n"
                f"🔊 Quality: {quality} kbps"
            )
            
        except ImportError:
            self.status_text.set("❌ yt-dlp not installed")
            self.show_error(
                "yt-dlp is required. Install with:\n"
                "pip install yt-dlp"
            )
            self.history_tree.set(item_id, "Status", "❌ Failed")
            self.history_tree.item(item_id, tags=('failed',))
            
        except Exception as e:
            error_msg = str(e)[:100]
            self.status_text.set(f"❌ Error: {error_msg}")
            self.status_label.configure(foreground='#ff4444')
            
            if 'item_id' in locals():
                self.history_tree.set(item_id, "Status", "❌ Failed")
                self.history_tree.item(item_id, tags=('failed',))
            
            self.show_error(f"Download failed:\n\n{error_msg}")
        
        finally:
            self.progress_bar['mode'] = 'indeterminate'
            self.progress_value.set(0)
            self.download_btn.configure(state=tk.NORMAL, bg='#0078d4')
    
    def start_download(self):
        """Start download in separate thread"""
        self.download_btn.configure(state=tk.DISABLED, bg='#005a9e')
        thread = threading.Thread(target=self.download_music, daemon=True)
        thread.start()
    
    def show_error(self, message):
        """Show error message"""
        messagebox.showerror("Error", message)


# ====================================================================
# SETUP AND LAUNCH
# ====================================================================

def check_dependencies():
    """Check and install required dependencies"""
    missing_packages = []
    
    # Check yt-dlp
    try:
        import yt_dlp
        print("✅ yt-dlp found")
    except ImportError:
        missing_packages.append('yt-dlp')
    
    # Check Pillow
    try:
        from PIL import Image
        print("✅ Pillow found")
    except ImportError:
        missing_packages.append('Pillow')
    
    if missing_packages:
        print(f"\n⚠️ Missing packages: {', '.join(missing_packages)}")
        print("Installing required packages...")
        
        import subprocess
        import sys
        
        for package in missing_packages:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ Installed {package}")
            except:
                print(f"❌ Failed to install {package}")
                print(f"   Please install manually: pip install {package}")
    
    # Check FFmpeg
    try:
        import subprocess
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        print("✅ FFmpeg found")
    except:
        print("⚠️ FFmpeg not found - required for audio conversion")
        print("   Windows: Download from https://ffmpeg.org/download.html")
        print("   macOS: brew install ffmpeg")
        print("   Linux: sudo apt install ffmpeg")
    
    return len(missing_packages) == 0

def main():
    """Main entry point"""
    print("=" * 60)
    print("🎵 Music Downloader Pro - Complete Application")
    print("=" * 60)
    print()
    
    # Step 1: Check dependencies
    print("Checking dependencies...")
    check_dependencies()
    print()
    
    # Step 2: Generate logo
    print("Setting up application logo...")
    logo_success = generate_logo()
    print()
    
    # Step 3: Launch GUI
    print("Launching Music Downloader Pro...")
    print("=" * 60)
    
    root = tk.Tk()
    app = MusicDownloaderApp(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()
