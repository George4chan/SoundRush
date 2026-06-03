from flask import Flask, render_template_string, request, jsonify, send_file
import yt_dlp
import re
import os
import threading
import time
from datetime import datetime

app = Flask(__name__)

# HTML Template with CSS and JavaScript
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Audio Downloader - YouTube to MP3</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
        }
        
        .input-group {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        
        input[type="text"] {
            flex: 1;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            transition: all 0.3s;
        }
        
        input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
        }
        
        button {
            padding: 15px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        button:hover {
            transform: translateY(-2px);
        }
        
        button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        
        .options {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }
        
        .option-group {
            margin-bottom: 15px;
        }
        
        .option-group label {
            display: inline-block;
            width: 120px;
            font-weight: bold;
            color: #555;
        }
        
        select {
            padding: 8px 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
            margin-left: 10px;
        }
        
        .result {
            margin-top: 30px;
            padding: 20px;
            background: #e8f5e9;
            border-radius: 10px;
            display: none;
        }
        
        .result.show {
            display: block;
            animation: slideIn 0.5s ease;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .video-info {
            display: flex;
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .video-thumbnail img {
            border-radius: 10px;
            width: 120px;
        }
        
        .video-details {
            flex: 1;
        }
        
        .video-title {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .video-meta {
            color: #666;
            margin-bottom: 5px;
        }
        
        .download-btn {
            width: 100%;
            background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
            margin-top: 10px;
        }
        
        .error {
            background: #ffebee;
            color: #c62828;
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
            display: none;
        }
        
        .error.show {
            display: block;
        }
        
        .loading {
            text-align: center;
            margin-top: 20px;
            display: none;
        }
        
        .loading.show {
            display: block;
        }
        
        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        @media (max-width: 600px) {
            .container {
                padding: 20px;
            }
            
            .input-group {
                flex-direction: column;
            }
            
            .video-info {
                flex-direction: column;
            }
            
            .video-thumbnail img {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎵 YouTube Audio Downloader</h1>
        <p class="subtitle">Download audio from YouTube in high quality</p>
        
        <div class="input-group">
            <input type="text" id="url" placeholder="Paste YouTube URL here..." />
            <button onclick="getVideoInfo()">Analyze</button>
        </div>
        
        <div class="options">
            <div class="option-group">
                <label>Format:</label>
                <select id="format">
                    <option value="mp3">MP3 (Most compatible)</option>
                    <option value="m4a">M4A (Apple)</option>
                    <option value="aac">AAC (High quality)</option>
                    <option value="opus">Opus (Small size)</option>
                </select>
            </div>
            
            <div class="option-group">
                <label>Quality:</label>
                <select id="quality">
                    <option value="320">320 kbps (Best)</option>
                    <option value="256">256 kbps (Very High)</option>
                    <option value="192" selected>192 kbps (High)</option>
                    <option value="128">128 kbps (Medium)</option>
                    <option value="64">64 kbps (Low)</option>
                </select>
            </div>
        </div>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p style="margin-top: 10px;">Processing your request...</p>
        </div>
        
        <div class="result" id="result"></div>
        <div class="error" id="error"></div>
    </div>
    
    <script>
        async function getVideoInfo() {
            const url = document.getElementById('url').value;
            if (!url) {
                showError('Please enter a YouTube URL');
                return;
            }
            
            // Hide previous results
            document.getElementById('result').classList.remove('show');
            document.getElementById('error').classList.remove('show');
            document.getElementById('loading').classList.add('show');
            
            try {
                const response = await fetch('/get_info', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({url: url})
                });
                
                const data = await response.json();
                
                if (data.error) {
                    showError(data.error);
                } else {
                    showVideoInfo(data);
                }
            } catch (error) {
                showError('Network error. Please try again.');
            } finally {
                document.getElementById('loading').classList.remove('show');
            }
        }
        
        function showVideoInfo(info) {
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = `
                <div class="video-info">
                    <div class="video-thumbnail">
                        <img src="${info.thumbnail}" alt="Thumbnail">
                    </div>
                    <div class="video-details">
                        <div class="video-title">${escapeHtml(info.title)}</div>
                        <div class="video-meta">📺 Channel: ${escapeHtml(info.channel)}</div>
                        <div class="video-meta">⏱️ Duration: ${info.duration}</div>
                        <div class="video-meta">👁️ Views: ${formatNumber(info.views)}</div>
                    </div>
                </div>
                <button class="download-btn" onclick="downloadAudio()">
                    ⬇️ Download Audio
                </button>
            `;
            resultDiv.classList.add('show');
            
            // Store video info for download
            window.videoInfo = info;
        }
        
        async function downloadAudio() {
            const format = document.getElementById('format').value;
            const quality = document.getElementById('quality').value;
            const url = document.getElementById('url').value;
            
            document.getElementById('loading').classList.add('show');
            
            try {
                const response = await fetch('/download', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        url: url,
                        format: format,
                        quality: quality
                    })
                });
                
                if (response.ok) {
                    const blob = await response.blob();
                    const contentDisposition = response.headers.get('Content-Disposition');
                    let filename = 'audio.mp3';
                    if (contentDisposition) {
                        const match = contentDisposition.match(/filename="(.+?)"/);
                        if (match) filename = match[1];
                    }
                    
                    const link = document.createElement('a');
                    link.href = URL.createObjectURL(blob);
                    link.download = filename;
                    link.click();
                    URL.revokeObjectURL(link.href);
                } else {
                    const error = await response.json();
                    showError(error.error || 'Download failed');
                }
            } catch (error) {
                showError('Download failed. Please try again.');
            } finally {
                document.getElementById('loading').classList.remove('show');
            }
        }
        
        function showError(message) {
            const errorDiv = document.getElementById('error');
            errorDiv.innerHTML = `❌ ${message}`;
            errorDiv.classList.add('show');
        }
        
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        
        function formatNumber(num) {
            if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
            if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
            return num.toString();
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/get_info', methods=['POST'])
def get_video_info():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'No URL provided'})
    
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Format duration
            duration = info.get('duration', 0)
            duration_str = f"{duration // 60}:{duration % 60:02d}"
            
            return jsonify({
                'title': info.get('title', 'Unknown'),
                'channel': info.get('uploader', 'Unknown'),
                'duration': duration_str,
                'views': info.get('view_count', 0),
                'thumbnail': info.get('thumbnail', ''),
            })
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/download', methods=['POST'])
def download_audio():
    data = request.json
    url = data.get('url')
    audio_format = data.get('format', 'mp3')
    quality = data.get('quality', '192')
    
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    # Create temporary directory
    temp_dir = 'downloads'
    os.makedirs(temp_dir, exist_ok=True)
    
    # Clean old files (older than 1 hour)
    for filename in os.listdir(temp_dir):
        filepath = os.path.join(temp_dir, filename)
        if os.path.isfile(filepath):
            age = time.time() - os.path.getctime(filepath)
            if age > 3600:  # 1 hour
                os.remove(filepath)
    
    output_template = os.path.join(temp_dir, '%(title)s.%(ext)s')
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': audio_format,
            'preferredquality': quality,
        }],
        'outtmpl': output_template,
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            
            # Find the downloaded file
            for file in os.listdir(temp_dir):
                if file.endswith(f".{audio_format}"):
                    file_path = os.path.join(temp_dir, file)
                    
                    # Send file
                    return send_file(
                        file_path,
                        as_attachment=True,
                        download_name=file,
                        mimetype=f'audio/{audio_format}'
                    )
            
            return jsonify({'error': 'File not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create downloads folder
    os.makedirs('downloads', exist_ok=True)
    print("\n" + "="*50)
    print("🎵 YouTube Audio Downloader is running!")
    print("="*50)
    print("\n👉 Open your browser and go to: http://localhost:5000")
    print("\n⚠️  Make sure ffmpeg is installed for audio conversion")
    print("="*50 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
