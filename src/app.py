from flask import Flask, render_template, request, jsonify, send_file
from utils.downloader import download_video, progress_data, fetch_video_title
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_title', methods=['POST'])
def fetch_title():
    data = request.json
    video_url = data.get('url')
    if not video_url:
        return jsonify({'error': 'Invalid input'}), 400

    try:
        title = fetch_video_title(video_url)
        return jsonify({'title': title})
    except Exception as e:
        app.logger.error(f"Error fetching title: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    video_url = data.get('url')
    quality = data.get('quality')
    audio = data.get('audio')
    if not video_url or not quality:
        return jsonify({'error': 'Invalid input'}), 400

    try:
        file_path = download_video(video_url, quality, audio)
        return jsonify({'file_path': file_path})
    except Exception as e:
        app.logger.error(f"Error during download: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/download_file', methods=['GET'])
def download_file():
    file_path = request.args.get('file_path')
    if not file_path:
        return jsonify({'error': 'Invalid file path'}), 400

    try:
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        app.logger.error(f"Error sending file: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/progress', methods=['GET'])
def progress():
    return jsonify(progress_data)

if __name__ == '__main__':
    app.run(debug=True)