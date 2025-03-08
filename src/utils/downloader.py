import yt_dlp
import logging
import os
import tempfile

# Configure logging
logging.basicConfig(filename='download.log', level=logging.INFO, format='%(asctime)s - %(message)s')

progress_data = {}

def fetch_video_title(url):
    ydl_opts = {
        'quiet': True,
        'skip_download': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        return info_dict.get('title', 'Unknown Title')

def download_video(url, quality, audio):
    format_str = quality
    if audio:
        format_str += f'+bestaudio[abr<={audio}]'

    # Create a temporary directory to store the downloaded file
    temp_dir = tempfile.mkdtemp()
    ydl_opts = {
        'format': format_str,
        'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
        'progress_hooks': [progress_hook]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Get the downloaded file path
    downloaded_files = os.listdir(temp_dir)
    if downloaded_files:
        return os.path.join(temp_dir, downloaded_files[0])
    else:
        raise Exception("Download failed")

def progress_hook(d):
    if d['status'] == 'finished':
        progress_data['status'] = 'finished'
        progress_data['filename'] = d['filename']
        logging.info(f"Download finished: {d['filename']}")
    elif d['status'] == 'downloading':
        progress_data['status'] = 'downloading'
        progress_data['filename'] = d['filename']
        progress_data['percent'] = d['_percent_str']
        progress_data['eta'] = d['_eta_str']
        logging.info(f"Downloading: {d['filename']} - {d['_percent_str']} - ETA: {d['_eta_str']}")