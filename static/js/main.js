document.addEventListener('DOMContentLoaded', function () {
  /* Mobile navigation toggle & interactions */
  const navToggle = document.getElementById('navToggle');
  const navClose = document.getElementById('navClose');
  const navMenu = document.getElementById('navMenu');

  function openMenu() {
    if (!navMenu || !navToggle) return;
    var navRect = navToggle.getBoundingClientRect();
    navMenu.style.paddingTop = (navRect.bottom + 16) + 'px';
    navMenu.classList.remove('opacity-0', 'pointer-events-none');
    navMenu.classList.add('opacity-100', 'pointer-events-auto');
    if (navToggle) navToggle.setAttribute('aria-label', 'Cerrar menú');
    document.body.style.overflow = 'hidden';
  }

  function closeMenu() {
    if (!navMenu) return;
    navMenu.classList.remove('opacity-100', 'pointer-events-auto');
    navMenu.classList.add('opacity-0', 'pointer-events-none');
    if (navToggle) navToggle.setAttribute('aria-label', 'Abrir menú');
    document.body.style.overflow = '';
  }

  if (navToggle && navMenu) {
    navToggle.addEventListener('click', function () {
      if (navMenu.classList.contains('opacity-100')) {
        closeMenu();
      } else {
        openMenu();
      }
    });
  }

  if (navClose && navMenu) {
    navClose.addEventListener('click', closeMenu);
  }

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeMenu();
  });

  /* Swipe down to close */
  if (navMenu) {
    var touchStartY = 0;
    navMenu.addEventListener('touchstart', function (e) {
      touchStartY = e.changedTouches[0].screenY;
    }, { passive: true });
    navMenu.addEventListener('touchend', function (e) {
      var touchEndY = e.changedTouches[0].screenY;
      if (touchEndY - touchStartY > 80) {
        closeMenu();
      }
    }, { passive: true });
  }

  /* Lazy loading fade-in */
  const lazyImages = document.querySelectorAll('img[loading="lazy"]');
  lazyImages.forEach(function (img) {
    if (img.complete && img.naturalHeight !== 0) {
      img.classList.add('opacity-100');
      img.classList.remove('opacity-0');
    } else {
      img.classList.add('opacity-0', 'transition-opacity', 'duration-500');
      img.addEventListener('load', function () {
        img.classList.remove('opacity-0');
        img.classList.add('opacity-100');
      });
    }
  });

  /* Scroll reveal animations */
  const revealElements = document.querySelectorAll('.reveal');
  if (revealElements.length && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('animate-fade-in-up');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    revealElements.forEach(function (el) {
      observer.observe(el);
    });
  }

  /* Footer registration form */
  const footerRegisterForm = document.getElementById('footerRegisterForm');
  const registerExtraFields = document.getElementById('registerExtraFields');
  const footerEmailInput = footerRegisterForm ? footerRegisterForm.querySelector('input[name="email"]') : null;

  if (footerEmailInput && registerExtraFields) {
    footerEmailInput.addEventListener('input', function () {
      if (footerEmailInput.value.trim().length > 0) {
        registerExtraFields.classList.remove('hidden');
        registerExtraFields.classList.add('grid');
      }
    });
  }

  if (footerRegisterForm) {
    footerRegisterForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var submitBtn = footerRegisterForm.querySelector('button[type="submit"]');
      var originalText = submitBtn.textContent;
      submitBtn.textContent = 'Procesando...';
      submitBtn.disabled = true;

      var formData = new FormData(footerRegisterForm);
      var data = {
        email: formData.get('email'),
        first_name: formData.get('first_name'),
        last_name: formData.get('last_name'),
        phone: formData.get('phone'),
        password: formData.get('password')
      };

      fetch('/cuenta/api/registro/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify(data)
      })
      .then(function (response) { return response.json(); })
      .then(function (result) {
        if (result.success) {
          submitBtn.textContent = '¡Registrado!';
          submitBtn.classList.remove('bg-marplata-primary', 'hover:bg-marplata-primary-dark');
          submitBtn.classList.add('bg-emerald-600');
          setTimeout(function () {
            window.location.reload();
          }, 1200);
        } else {
          var errorMsg = result.errors ? result.errors.join('\n') : (result.error || 'Error al registrarse');
          alert(errorMsg);
          submitBtn.textContent = originalText;
          submitBtn.disabled = false;
        }
      })
      .catch(function () {
        alert('Error de conexión');
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
      });
    });
  }

  function getCsrfToken() {
    var cookie = document.cookie.match(/csrftoken=([^;]+)/);
    if (cookie) return cookie[1];
    var input = document.querySelector('input[name="csrfmiddlewaretoken"]');
    if (input) return input.value;
    var meta = document.querySelector('meta[name="csrf-token"]');
    if (meta) return meta.getAttribute('content');
    return '';
  }

  /* Search overlay */
  var searchToggle = document.getElementById('searchToggle');
  var searchOverlay = document.getElementById('searchOverlay');
  var searchInput = document.getElementById('searchInput');
  var searchClose = document.getElementById('searchClose');
  var searchBackdrop = document.getElementById('searchBackdrop');
  var searchSuggestions = document.getElementById('searchSuggestions');
  var searchDebounce;

  function openSearch() {
    if (!searchOverlay) return;
    searchOverlay.classList.remove('hidden');
    setTimeout(function () { if (searchInput) searchInput.focus(); }, 50);
  }
  function closeSearch() {
    if (!searchOverlay) return;
    searchOverlay.classList.add('hidden');
    if (searchInput) searchInput.value = '';
    if (searchSuggestions) {
      searchSuggestions.classList.add('hidden');
      searchSuggestions.innerHTML = '';
    }
  }

  if (searchToggle) {
    searchToggle.addEventListener('click', openSearch);
  }
  if (searchClose) {
    searchClose.addEventListener('click', closeSearch);
  }
  if (searchBackdrop) {
    searchBackdrop.addEventListener('click', closeSearch);
  }
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && searchOverlay && !searchOverlay.classList.contains('hidden')) {
      closeSearch();
    }
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
      e.preventDefault();
      if (searchOverlay.classList.contains('hidden')) openSearch();
      else closeSearch();
    }
  });

  if (searchInput) {
    searchInput.addEventListener('input', function () {
      clearTimeout(searchDebounce);
      var q = searchInput.value.trim();
      if (q.length < 2) {
        searchSuggestions.classList.add('hidden');
        searchSuggestions.innerHTML = '';
        return;
      }
      searchDebounce = setTimeout(function () {
        fetch('/coleccion/api/sugerencias/?q=' + encodeURIComponent(q))
          .then(function (r) { return r.json(); })
          .then(function (data) {
            if (!data.suggestions || data.suggestions.length === 0) {
              searchSuggestions.innerHTML = '<div class="px-6 py-4 text-sm text-marplata-text-muted">No se encontraron sugerencias.</div>';
            } else {
              var html = '<a href="/coleccion/buscar/?q=' + encodeURIComponent(q) + '" class="block px-6 py-3 text-xs uppercase tracking-wide-custom text-marplata-text-muted hover:bg-marplata-neutral border-b border-marplata-secondary-light">Ver todos los resultados para &quot;' + q + '&quot;</a>';
              data.suggestions.forEach(function (s) {
                html += '<a href="/producto/' + s.slug + '/" class="flex items-center justify-between px-6 py-3 hover:bg-marplata-neutral border-b border-marplata-secondary-light last:border-b-0">';
                html += '<div><p class="text-sm font-medium text-marplata-text">' + s.name + '</p>';
                if (s.collection) html += '<p class="text-xs text-marplata-text-muted">' + s.collection + '</p>';
                html += '</div><p class="text-sm text-marplata-text-light">$' + Number(s.price).toLocaleString('es-CO') + '</p>';
                html += '</a>';
              });
              searchSuggestions.innerHTML = html;
            }
            searchSuggestions.classList.remove('hidden');
          })
          .catch(function () { searchSuggestions.classList.add('hidden'); });
      }, 200);
    });
  }

  /* Footer newsletter (logged-in users) */
  var newsletterForm = document.getElementById('footerNewsletterForm');
  if (newsletterForm) {
    newsletterForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var emailInput = newsletterForm.querySelector('input[name="email"]');
      var btn = newsletterForm.querySelector('button[type="submit"]');
      var msg = document.getElementById('newsletterMessage');
      var csrf = getCsrfToken();
      if (!csrf) return;
      btn.disabled = true;
      var original = btn.textContent;
      btn.textContent = 'Enviando...';
      var formData = new FormData(newsletterForm);
      fetch('/cuenta/api/newsletter/', {
        method: 'POST',
        headers: { 'X-CSRFToken': csrf },
        body: formData,
      })
      .then(function (r) { return r.json(); })
      .then(function (data) {
        if (data.success) {
          msg.className = 'mt-4 text-xs text-emerald-400';
          msg.textContent = data.message;
          msg.classList.remove('hidden');
          emailInput.value = '';
        } else {
          msg.className = 'mt-4 text-xs text-red-400';
          msg.textContent = data.error || 'No se pudo suscribir.';
          msg.classList.remove('hidden');
        }
        btn.disabled = false;
        btn.textContent = original;
      })
      .catch(function () {
        msg.className = 'mt-4 text-xs text-red-400';
        msg.textContent = 'Error de conexión.';
        msg.classList.remove('hidden');
        btn.disabled = false;
        btn.textContent = original;
      });
    });
  }
});
