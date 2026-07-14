document.addEventListener('DOMContentLoaded', function () {
  var csrfToken = getCookie('csrftoken');

  document.querySelectorAll('.cart-item__remove').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var variantId = this.getAttribute('data-variant-id');
      removeFromCart(variantId, this.closest('.cart-item'));
    });
  });

  document.querySelectorAll('.cart-item__qty-btn--minus').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var variantId = this.getAttribute('data-variant-id');
      var input = this.parentElement.querySelector('.cart-item__qty-input');
      var currentQty = parseInt(input.value);
      if (currentQty > 1) {
        updateQuantity(variantId, currentQty - 1, input, this.closest('.cart-item'));
      } else {
        removeFromCart(variantId, this.closest('.cart-item'));
      }
    });
  });

  document.querySelectorAll('.cart-item__qty-btn--plus').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var variantId = this.getAttribute('data-variant-id');
      var input = this.parentElement.querySelector('.cart-item__qty-input');
      var maxQty = parseInt(input.getAttribute('max'));
      var currentQty = parseInt(input.value);
      if (currentQty < maxQty) {
        updateQuantity(variantId, currentQty + 1, input, this.closest('.cart-item'));
      }
    });
  });

  document.querySelectorAll('.cart-item__qty-input').forEach(function (input) {
    input.addEventListener('change', function () {
      var variantId = this.getAttribute('data-variant-id');
      var newQty = parseInt(this.value);
      if (isNaN(newQty) || newQty < 1) {
        removeFromCart(variantId, this.closest('.cart-item'));
      } else {
        updateQuantity(variantId, newQty, this, this.closest('.cart-item'));
      }
    });
  });

  var checkoutBtn = document.getElementById('checkoutBtn');
  if (checkoutBtn) {
    checkoutBtn.addEventListener('click', function (e) {
      e.preventDefault();
      redirectToWhatsApp();
    });
  }

  function updateQuantity(variantId, quantity, input, cartItem) {
    var formData = new FormData();
    formData.append('variant_id', variantId);
    formData.append('quantity', quantity);

    fetch('/carrito/api/update/', {
      method: 'POST',
      headers: { 'X-CSRFToken': csrfToken },
      body: formData,
    })
    .then(function (response) { return response.json(); })
    .then(function (data) {
      if (data.success) {
        var subtotalEl = cartItem.querySelector('.cart-item__subtotal-value');
        if (subtotalEl && data.subtotal !== undefined) {
          subtotalEl.textContent = '$' + Number(data.subtotal).toLocaleString('es-CO');
        }
        updateTotals(data.total_items, data.total, data.cart_subtotal, data.discount);
        updateCartCounter(data.total_items);
        input.value = quantity;
      } else if (data.error) {
        alert(data.error);
      }
    })
    .catch(function () { alert('Error al actualizar el carrito'); });
  }

  function removeFromCart(variantId, cartItem) {
    var formData = new FormData();
    formData.append('variant_id', variantId);

    fetch('/carrito/api/remove/', {
      method: 'POST',
      headers: { 'X-CSRFToken': csrfToken },
      body: formData,
    })
    .then(function (response) { return response.json(); })
    .then(function (data) {
      if (data.success) {
        cartItem.remove();
        updateTotals(data.total_items, data.total, data.subtotal, data.discount);
        updateCartCounter(data.total_items);

        if (data.total_items === 0) {
          window.location.reload();
        }
      }
    })
    .catch(function () { alert('Error al eliminar del carrito'); });
  }

  function updateTotals(totalItems, total, subtotal, discount) {
    var totalEl = document.getElementById('cartSubtotal');
    var totalFinalEl = document.getElementById('cartTotalFinal');
    if (totalEl && subtotal !== undefined) {
      totalEl.textContent = '$' + Number(subtotal).toLocaleString('es-CO');
    }
    if (totalFinalEl) {
      totalFinalEl.textContent = '$' + Number(total).toLocaleString('es-CO');
    }
  }

  function updateCartCounter(count) {
    var counter = document.getElementById('cartCount');
    if (counter) {
      counter.textContent = count;
    }
  }

  function redirectToWhatsApp() {
    fetch('/carrito/api/summary/')
      .then(function (response) { return response.json(); })
      .then(function (data) {
        var items = data.items;
        if (items.length === 0) return;

        var message = 'Hola MARPLATA! Me interesa realizar un pedido:\n\n';
        items.forEach(function (item) {
          message += '• ' + item.product_name + ' (' + item.color + ' / ' + item.size + ') x' + item.quantity + ' — $' + Number(item.subtotal).toLocaleString('es-CO') + '\n';
        });
        message += '\nTotal: $' + Number(data.total).toLocaleString('es-CO') + '\n\nMi nombre: \nMi correo: \nMi teléfono: ';

        fetch('/api/site-config/')
          .then(function (r) { return r.json(); })
          .then(function (config) {
            var phone = (config.whatsapp_number || '').replace(/\D/g, '') || '573001234567';
            var url = 'https://wa.me/' + phone + '?text=' + encodeURIComponent(message);
            window.open(url, '_blank');
          })
          .catch(function () {
            var url = 'https://wa.me/573001234567?text=' + encodeURIComponent(message);
            window.open(url, '_blank');
          });
      });
  }

  function getCookie(name) {
    var value = '; ' + document.cookie;
    var parts = value.split('; ' + name + '=');
    if (parts.length === 2) return parts.pop().split(';').shift();
    return '';
  }

  var couponForm = document.getElementById('couponForm');
  if (couponForm) {
    couponForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var input = couponForm.querySelector('input[name="code"]');
      var btn = couponForm.querySelector('button[type="submit"]');
      var msg = document.getElementById('couponMessage');
      var code = (input.value || '').trim();
      if (!code) return;

      btn.disabled = true;
      var original = btn.textContent;
      btn.textContent = 'Aplicando...';

      var formData = new FormData();
      formData.append('code', code);

      fetch('/carrito/api/coupon/apply/', {
        method: 'POST',
        headers: { 'X-CSRFToken': csrfToken },
        body: formData,
      })
      .then(function (response) { return response.json(); })
      .then(function (data) {
        if (data.success) {
          msg.className = 'mt-2 text-xs text-emerald-700';
          msg.textContent = data.message;
          msg.classList.remove('hidden');
          setTimeout(function () { window.location.reload(); }, 800);
        } else {
          msg.className = 'mt-2 text-xs text-marplata-danger';
          msg.textContent = data.error || 'No se pudo aplicar el cupón.';
          msg.classList.remove('hidden');
          btn.disabled = false;
          btn.textContent = original;
        }
      })
      .catch(function () {
        msg.className = 'mt-2 text-xs text-marplata-danger';
        msg.textContent = 'Error de conexión.';
        msg.classList.remove('hidden');
        btn.disabled = false;
        btn.textContent = original;
      });
    });
  }

  var couponRemove = document.getElementById('couponRemove');
  if (couponRemove) {
    couponRemove.addEventListener('click', function () {
      fetch('/carrito/api/coupon/remove/', {
        method: 'POST',
        headers: { 'X-CSRFToken': csrfToken },
      })
      .then(function (response) { return response.json(); })
      .then(function (data) {
        if (data.success) window.location.reload();
      });
    });
  }
});
