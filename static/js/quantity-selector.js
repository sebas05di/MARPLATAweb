(function() {
  'use strict';

  const input = document.getElementById('quantityInput');
  const minus = document.getElementById('qtyMinus');
  const plus = document.getElementById('qtyPlus');

  if (!input || !minus || !plus) return;

  const min = parseInt(input.min, 10) || 1;
  const max = parseInt(input.max, 10) || 99;

  function clamp(v) {
    v = parseInt(v, 10);
    if (isNaN(v) || v < min) v = min;
    if (v > max) v = max;
    return v;
  }

  minus.addEventListener('click', function() {
    input.value = clamp(parseInt(input.value, 10) - 1);
  });

  plus.addEventListener('click', function() {
    input.value = clamp(parseInt(input.value, 10) + 1);
  });

  input.addEventListener('change', function() {
    input.value = clamp(input.value);
  });

  input.addEventListener('blur', function() {
    input.value = clamp(input.value);
  });

  window.getProductQuantity = function() {
    return clamp(input.value);
  };
})();
