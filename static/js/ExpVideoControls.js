document.addEventListener('DOMContentLoaded', function() {
    const video = document.getElementById('myVideo');
    const playPauseBtn = document.getElementById('playPauseBtn');
    const playIcon = playPauseBtn.querySelector('.play-icon');
    const pauseIcon = playPauseBtn.querySelector('.pause-icon');

    // Check if video and button exist
    if (!video || !playPauseBtn) {
        console.warn('Video or play/pause button not found');
        return;
    }

    // Function to toggle play/pause
    function togglePlayPause() {
        if (video.paused || video.ended) {
            video.play();
            playIcon.style.display = 'none';
            pauseIcon.style.display = 'block';
        } else {
            video.pause();
            playIcon.style.display = 'block';
            pauseIcon.style.display = 'none';
        }
    }

    // Add click event listener to the button
    playPauseBtn.addEventListener('click', togglePlayPause);

    // Update button state when video ends
    video.addEventListener('ended', function() {
        playIcon.style.display = 'block';
        pauseIcon.style.display = 'none';
    });

    // Update button state when video is paused/played via other means
    video.addEventListener('pause', function() {
        playIcon.style.display = 'block';
        pauseIcon.style.display = 'none';
    });

    video.addEventListener('play', function() {
        playIcon.style.display = 'none';
        pauseIcon.style.display = 'block';
    });

    // Optional: Hide button when video is not ready
    playPauseBtn.style.display = 'none';
    
    video.addEventListener('loadedmetadata', function() {
        playPauseBtn.style.display = 'block';
    });

    // Handle video load errors
    video.addEventListener('error', function() {
        console.error('Error loading video');
        playPauseBtn.style.display = 'none';
    });
});
