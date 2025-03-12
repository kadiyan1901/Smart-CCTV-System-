// scripts.js
function toggleVideo() {
    const videoStream = document.getElementById('video-stream');
    if (videoStream.style.display === 'none') {
        videoStream.style.display = 'block';
    } else {
        videoStream.style.display = 'none';
    }
}
