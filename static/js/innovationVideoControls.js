document.addEventListener('DOMContentLoaded', function() {
    const video = document.getElementById('aNewCourseVideo');
    const playPauseButton = document.getElementById('playPauseButton');
    const playPauseIcon = playPauseButton.querySelector('.fas');
    const innovationVideoContainer = document.querySelector('.innovation-video');

    /**
     * Updates the play/pause button's icon and visibility based on video state.
     * @param {boolean} isPaused - True if the video is currently paused, false otherwise.
     */
    function updatePlayPauseButton(isPaused) {
        if (isPaused) {
            playPauseIcon.classList.remove('fa-pause');
            playPauseIcon.classList.add('fa-play');
            playPauseButton.classList.add('force-show'); // Always show button when paused
        } else {
            playPauseIcon.classList.remove('fa-play');
            playPauseIcon.classList.add('fa-pause');
            playPauseButton.classList.remove('force-show'); // Hide when playing (unless hovered)
        }
    }

    // Initial state check
    if (video.autoplay && !video.paused) {
        updatePlayPauseButton(false); // Video is playing, hide button
    } else {
        updatePlayPauseButton(true); // Video is paused, show button
    }

    // Click handler for the play/pause button
    playPauseButton.addEventListener('click', function() {
        if (video.paused) {
            video.play();
        } else {
            video.pause();
        }
    });

    // Event listeners to update button state when video playback changes
    video.addEventListener('play', function() {
        updatePlayPauseButton(false);
    });

    video.addEventListener('pause', function() {
        // Only force-show if video is actually paused and not just ended
        updatePlayPauseButton(true);
    });

    video.addEventListener('ended', function() {
        // When video ends, it automatically pauses, so update as paused
        updatePlayPauseButton(true);
    });
});