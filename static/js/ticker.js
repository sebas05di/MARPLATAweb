(function() {
  'use strict';

  function init() {
    const ticker = document.querySelector('[data-ticker]');
    const track = document.querySelector('[data-ticker-track]');
    if (!ticker || !track) return;

    // Ensure there is enough content to loop seamlessly by duplicating the track once more if needed.
    const originalHTML = track.innerHTML;
    if (track.scrollWidth < ticker.clientWidth * 2) {
      track.insertAdjacentHTML('beforeend', originalHTML);
    }

    let scrollPos = 0;
    let isPaused = false;
    const speed = 0.5; // pixels per frame
    const halfWidth = () => track.scrollWidth / 2;

    function step() {
      if (!isPaused) {
        scrollPos += speed;
        if (scrollPos >= halfWidth()) {
          scrollPos = 0;
        }
        ticker.scrollLeft = scrollPos;
      }
      requestAnimationFrame(step);
    }

    requestAnimationFrame(step);

    ticker.addEventListener('mouseenter', function() { isPaused = true; });
    ticker.addEventListener('mouseleave', function() { isPaused = false; });
    ticker.addEventListener('touchstart', function() { isPaused = true; }, { passive: true });
    ticker.addEventListener('touchend', function() { isPaused = false; });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
