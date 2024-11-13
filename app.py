
# import os
# from flask import Flask, request, jsonify, send_from_directory
# from moviepy.editor import VideoFileClip
# from werkzeug.utils import secure_filename
# from flask_cors import CORS
# import yt_dlp  # Import yt-dlp for downloading videos

# app = Flask(__name__)
# CORS(app)

# UPLOAD_FOLDER = 'uploads'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# ALLOWED_EXTENSIONS = {'mp4', 'mkv', 'webm', 'mov'}

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/extract-audio', methods=['POST'])
# def extract_audio():
#     video_file = request.files.get('video')
#     video_url = request.form.get('url')

#     if video_file and allowed_file(video_file.filename):
#         filename = secure_filename(video_file.filename)
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         video_file.save(filepath)
#         audio_path = convert_to_audio(filepath)
#         return jsonify({'audio_url': f'http://localhost:5000/uploads/{os.path.basename(audio_path)}'})

#     elif video_url:
#         video_path = download_video(video_url)
#         if video_path:
#             audio_path = convert_to_audio(video_path)
#             return jsonify({'audio_url': f'http://localhost:5000/uploads/{os.path.basename(audio_path)}'})
#         else:
#             return jsonify({'error': 'Failed to download video from the provided URL'}), 400

#     return jsonify({'error': 'No video or URL provided'}), 400

# def download_video(url):
#     try:
#         # Define options for yt-dlp to download video
#         ydl_opts = {
#             'format': 'bestvideo+bestaudio',
#             'outtmpl': os.path.join(app.config['UPLOAD_FOLDER'], 'downloaded_video.%(ext)s'),
#             'merge_output_format': 'mp4'
#         }
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             info_dict = ydl.extract_info(url, download=True)
#             video_path = ydl.prepare_filename(info_dict)
#             return video_path
#     except Exception as e:
#         print("Error downloading video:", e)
#         return None

# def convert_to_audio(video_path):
#     audio_path = os.path.join(app.config['UPLOAD_FOLDER'], 'audio.mp3')
#     video_clip = VideoFileClip(video_path)
#     video_clip.audio.write_audiofile(audio_path)
#     video_clip.close()
#     return audio_path

# @app.route('/uploads/<path:filename>', methods=['GET'])
# def serve_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# if __name__ == '__main__':
#     app.run(debug=True)


import os
from flask import Flask, request, jsonify, send_from_directory
from moviepy.editor import VideoFileClip
from werkzeug.utils import secure_filename
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set up the folder to save uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# File type restrictions
ALLOWED_EXTENSIONS = {'mp4', 'mkv', 'webm', 'mov'}

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/extract-audio', methods=['POST'])
def extract_audio():
    video_file = request.files.get('video')
    video_url = request.form.get('url')

    if video_file and allowed_file(video_file.filename):
        filename = secure_filename(video_file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        video_file.save(filepath)

        # Extract audio from the video
        video_clip = VideoFileClip(filepath)
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], 'audio.mp3')
        video_clip.audio.write_audiofile(audio_path)

        # Return the backend URL for downloading the audio
        return jsonify({'audio_url': f'https://video-to-audio-backend.onrender.com/uploads/audio.mp3'})

    elif video_url:
        # Placeholder for video download functionality
        video_path = "downloaded_video.mp4"
        video_clip = VideoFileClip(video_path)
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], 'audio.mp3')
        video_clip.audio.write_audiofile(audio_path)

        # Return the backend URL for downloading the audio
        return jsonify({'audio_url': f'https://video-to-audio-backend.onrender.com/uploads/audio.mp3'})

    return jsonify({'error': 'No video or URL provided'}), 400

@app.route('/uploads/<path:filename>', methods=['GET'])
def serve_file(filename):
    # Serve the audio file from the 'uploads' directory
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
