(function () {
  'use strict';

  function updateCartCounter(count) {
    var counters = document.querySelectorAll('#cartCount');
    counters.forEach(function (el) {
      el.textContent = count;
    });
  }

  function loadCartCount() {
    fetch('/carrito/api/summary/')
      .then(function (response) { return response.json(); })
      .then(function (data) {
        if (data && typeof data.total_items === 'number') {
          updateCartCounter(data.total_items);
        }
      })
      .catch(function () {});
  }

  document.addEventListener('DOMContentLoaded', loadCartCount);

  window.updateCartCounter = updateCartCounter;
  window.loadCartCount = loadCartCount;
})();
