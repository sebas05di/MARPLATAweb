document.addEventListener('DOMContentLoaded', function () {
  var csrf = getCookie('csrftoken');

  function getCookie(name) {
    var v = '; ' + document.cookie;
    var parts = v.split('; ' + name + '=');
    if (parts.length === 2) return parts.pop().split(';').shift();
    return '';
  }

  document.querySelectorAll('.wishlist-toggle').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      var productId = btn.getAttribute('data-product-id');
      var inWishlist = btn.getAttribute('data-in-wishlist') === 'true';
      var original = btn.innerHTML;

      btn.disabled = true;

      var formData = new FormData();
      formData.append('product_id', productId);

      fetch('/cuenta/api/favoritos/toggle/', {
        method: 'POST',
        headers: { 'X-CSRFToken': csrf },
        body: formData,
        credentials: 'same-origin',
      })
      .then(function (r) {
        if (r.status === 403 || r.status === 401) {
          window.location.href = '/cuenta/login/?next=' + encodeURIComponent(window.location.pathname);
          return null;
        }
        return r.json();
      })
      .then(function (data) {
        if (!data) return;
        if (data.success) {
          if (data.in_wishlist) {
            btn.setAttribute('data-in-wishlist', 'true');
            btn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"></path></svg>';
            btn.classList.add('text-marplata-danger');
            btn.classList.remove('text-marplata-text-muted');
          } else {
            var card = btn.closest('.group');
            if (card) {
              card.style.transition = 'opacity 0.3s, transform 0.3s';
              card.style.opacity = '0';
              card.style.transform = 'scale(0.95)';
              setTimeout(function () { card.remove(); }, 300);
            } else {
              btn.setAttribute('data-in-wishlist', 'false');
              btn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"></path></svg>';
            }
          }
        } else {
          alert(data.error || 'Error');
          btn.innerHTML = original;
        }
        btn.disabled = false;
      })
      .catch(function () {
        btn.innerHTML = original;
        btn.disabled = false;
      });
    });
  });
});
