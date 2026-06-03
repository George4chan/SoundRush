# flask_youtube_downloader.py

from flask import Flask, render_template_string, request, send_file
import yt_dlp
import tempfile
import os

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>YouTube Audio Downloader</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }
        input, select, button {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        button {
            background: #ff0000;
            color: white;
            border: none;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background: #cc0000;
        }
        h1 {
            color: #333;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎵 YouTube Audio Downloader</h1>
        <form method="POST">
            <input type="text" name="url" placeholder="Enter YouTube URL" required>
            <select name="format">
                <option value="mp3">MP3</option>
                <option value="m4a">M4A</option>
                <option value="wav">WAV</option>
            </select>
            <select name="quality">
                <option value="128">128 kbps</option>
                <option value="192">192 kbps</option>
                <option value="320">320 kbps</option>
            </select>
            <button type="submit">Download Audio</button>
        </form>
        {% if error %}
            <p style="color: red;">{{ error }}</p>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        audio_format = request.form.get('format', 'mp3')
        quality = request.form.get('quality', '192')
        
        try:
            temp_dir = tempfile.mkdtemp()
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': audio_format,
                    'preferredquality': quality,
                }],
                'outtmpl': f'{temp_dir}/%(title)s.%(ext)s',
                'quiet': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                
            for file in os.listdir(temp_dir):
                if file.endswith(f'.{audio_format}'):
                    file_path = os.path.join(temp_dir, file)
                    return send_file(
                        file_path,
                        as_attachment=True,
                        download_name=file
                    )
        except Exception as e:
            return render_template_string(HTML_TEMPLATE, error=str(e))
    
    return render_template_string(HTML_TEMPLATE, error=None)

if __name__ == '__main__':
    app.run(debug=True)
