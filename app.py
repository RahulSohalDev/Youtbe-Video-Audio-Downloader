from flask import Flask, Response, request, render_template_string
from pytube import YouTube
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_url = request.form['video_url']
        download_type = request.form.get('download_type')
        if download_type == 'audio':
            return download_stream(video_url, audio_only=True)
        elif download_type == 'high_quality':
            return download_stream(video_url, high_quality=True)
        else:
            return download_stream(video_url, high_quality=False)
    return render_template_string("""
        <body style="display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background-color: #f7f7f7;">
            <form method="post" style="background-color: #fff; padding: 20px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);">
                <label for="video_url" style="margin-bottom: 10px; display: block; font-family: 'Arial', sans-serif;">YouTube video URL:</label>
                <input placeholder="Enter Your URL" type="text" id="video_url" name="video_url" style="padding: 10px; margin-bottom: 10px; border: 1px solid #ddd; border-radius: 4px; width: 300px; display: block;">
                <input type="submit" name="download_type" value="audio" style="padding: 10px 20px; border: none; border-radius: 4px; background-color: #007bff; color: white; cursor: pointer; margin-right: 5px;">
                <input type="submit" name="download_type" value="high_quality" style="padding: 10px 20px; border: none; border-radius: 4px; background-color: #28a745; color: white; cursor: pointer; margin-right: 5px; margin-top: 5px;">
                <input type="submit" name="download_type" value="low_quality" style="padding: 10px 20px; border: none; border-radius: 4px; background-color: #dc3545; color: white; cursor: pointer; margin-top: 5px;">
            </form>
        </body>
    """)

def download_stream(video_url, audio_only=False, high_quality=False):
    try:
        yt = YouTube(video_url)
        if audio_only:
            stream = yt.streams.filter(only_audio=True).first()
            filename = stream.default_filename.replace(".mp4", ".mp3")
            content_type = 'audio/mp3'
        else:
            if high_quality:
                stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            else:
                stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').asc().first()
            filename = stream.default_filename
            content_type = 'video/mp4'
        
        # Create an in-memory bytes buffer
        buffer = io.BytesIO()
        stream.stream_to_buffer(buffer)
        buffer.seek(0)
        
        return Response(buffer, mimetype=content_type, headers={"Content-Disposition": f"attachment;filename={filename}"})
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)