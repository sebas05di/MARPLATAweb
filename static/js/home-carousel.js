(function() {
  'use strict';

  function init() {
    const carousels = document.querySelectorAll('[data-carousel]');
    if (!carousels.length) return;

    carousels.forEach(function(carousel) {
      const section = carousel.closest('section');
      if (!section) return;

      const prevBtn = section.querySelector('[data-carousel-prev]');
      const nextBtn = section.querySelector('[data-carousel-next]');
      const track = carousel.querySelector('.flex');

      if (!track) return;

      function getStep() {
        const firstCard = track.querySelector('a, p');
        if (!firstCard) return 320;
        const style = window.getComputedStyle(track);
        const gap = parseFloat(style.gap) || 24;
        return firstCard.getBoundingClientRect().width + gap;
      }

      function scrollByStep(direction) {
        const step = getStep();
        carousel.scrollBy({ left: step * direction, behavior: 'smooth' });
      }

      if (prevBtn) {
        prevBtn.addEventListener('click', function() { scrollByStep(-1); });
      }
      if (nextBtn) {
        nextBtn.addEventListener('click', function() { scrollByStep(1); });
      }

      // Drag-to-scroll en desktop
      let isDown = false;
      let startX = 0;
      let scrollLeft = 0;
      let isDragging = false;

      carousel.addEventListener('mousedown', function(e) {
        if (e.target.closest('a')) return;
        isDown = true;
        isDragging = false;
        startX = e.pageX - carousel.offsetLeft;
        scrollLeft = carousel.scrollLeft;
        carousel.style.cursor = 'grabbing';
      });

      carousel.addEventListener('mouseleave', function() {
        isDown = false;
        carousel.style.cursor = '';
      });

      carousel.addEventListener('mouseup', function() {
        isDown = false;
        carousel.style.cursor = '';
      });

      carousel.addEventListener('mousemove', function(e) {
        if (!isDown) return;
        e.preventDefault();
        isDragging = true;
        const x = e.pageX - carousel.offsetLeft;
        const walk = (x - startX) * 1.4;
        carousel.scrollLeft = scrollLeft - walk;
      });

      // Prevenir click si hubo drag
      carousel.addEventListener('click', function(e) {
        if (isDragging) {
          e.preventDefault();
          isDragging = false;
        }
      }, true);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
