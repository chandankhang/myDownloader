document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('fetch-title-button').addEventListener('click', fetchTitle);
    document.getElementById('download-button').addEventListener('click', downloadVideo);
});

function fetchTitle() {
    const videoUrl = document.getElementById('video-url').value;

    fetch('/fetch_title', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: videoUrl })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            document.getElementById('video-title').innerText = `Title: ${data.title}`;
            document.getElementById('quality').disabled = false;
            document.getElementById('audio').disabled = false;
            document.getElementById('download-button').disabled = false;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to fetch video title');
    });
}

function downloadVideo() {
    const videoUrl = document.getElementById('video-url').value;
    const quality = document.getElementById('quality').value;
    const audio = document.getElementById('audio').value;

    fetch('/download', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: videoUrl, quality: quality, audio: audio })
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => { throw new Error(text) });
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            const filePath = data.file_path;
            window.location.href = `/download_file?file_path=${encodeURIComponent(filePath)}`;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to start download');
    });
}