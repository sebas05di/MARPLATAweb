document.addEventListener('DOMContentLoaded', function () {
  var productData = window.productData || {};
  var variants = productData.variants || [];
  var basePrice = productData.basePrice || 0;
  var coverImage = productData.coverImage || null;

  if (!variants.length) {
    console.warn('[MARPLATA] No variants available');
  }

  var selectedColor = null;
  var selectedTopSize = null;
  var selectedBottomSize = null;
  var currentImages = [];
  var currentImageIndex = 0;

  var mainImage = document.getElementById('mainImage');
  var mainImageContainer = document.getElementById('mainImageContainer');
  var zoomLens = document.getElementById('zoomLens');
  var thumbnailContainer = document.getElementById('thumbnailContainer');
  var colorOptionsContainer = document.getElementById('colorOptions');
  var topSizeOptionsContainer = document.getElementById('topSizeOptions');
  var bottomSizeOptionsContainer = document.getElementById('bottomSizeOptions');
  var productPrice = document.getElementById('productPrice');
  var stockStatus = document.querySelector('.product-detail__stock-status');
  var addToCartBtn = document.getElementById('addToCartBtn');
  var buyWhatsappBtn = document.getElementById('buyWhatsappBtn');
  var imageCounter = document.getElementById('imageCounter');
  var openLightboxBtn = document.getElementById('openLightboxBtn');
  var lightbox = document.getElementById('imageLightbox');
  var lightboxImage = document.getElementById('lightboxImage');
  var lightboxCounter = document.getElementById('lightboxCounter');
  var lightboxThumbs = document.getElementById('lightboxThumbs');
  var closeLightboxBtn = document.getElementById('closeLightboxBtn');
  var lightboxPrevBtn = document.getElementById('lightboxPrevBtn');
  var lightboxNextBtn = document.getElementById('lightboxNextBtn');

  if (!mainImage || !colorOptionsContainer || !topSizeOptionsContainer || !bottomSizeOptionsContainer || !addToCartBtn) {
    console.error('[MARPLATA] Required DOM elements missing');
    return;
  }

  var csrfToken = getCsrfToken();

  function getCsrfToken() {
    var cookie = getCookie('csrftoken');
    if (cookie) return cookie;
    var input = document.querySelector('input[name="csrfmiddlewaretoken"]');
    if (input) return input.value;
    var meta = document.querySelector('meta[name="csrf-token"]');
    if (meta) return meta.getAttribute('content');
    return '';
  }

  function getCookie(name) {
    var value = '; ' + document.cookie;
    var parts = value.split('; ' + name + '=');
    if (parts.length === 2) return parts.pop().split(';').shift();
    return '';
  }

  function getUniqueColors() {
    var colors = [];
    var seen = new Set();
    variants.forEach(function (v) {
      if (!seen.has(v.color_slug)) {
        seen.add(v.color_slug);
        colors.push({ color: v.color, color_slug: v.color_slug });
      }
    });
    return colors;
  }

  function sortSizes(sizes) {
    var order = { S: 1, M: 2, L: 3 };
    return sizes.slice().sort(function (a, b) {
      return (order[a] || 99) - (order[b] || 99);
    });
  }

  function getTopSizesForColor(colorSlug) {
    var seen = new Set();
    var sizes = variants
      .filter(function (v) { return v.color_slug === colorSlug; })
      .map(function (v) { return v.top_size; })
      .filter(function (s) { if (seen.has(s)) return false; seen.add(s); return true; });
    return sortSizes(sizes);
  }

  function getBottomSizesForColor(colorSlug) {
    var seen = new Set();
    var sizes = variants
      .filter(function (v) { return v.color_slug === colorSlug; })
      .map(function (v) { return v.bottom_size; })
      .filter(function (s) { if (seen.has(s)) return false; seen.add(s); return true; });
    return sortSizes(sizes);
  }

  function getVariant(colorSlug, topSize, bottomSize) {
    return variants.find(function (v) {
      return v.color_slug === colorSlug && v.top_size === topSize && v.bottom_size === bottomSize;
    });
  }

  function getImagesForColor(colorSlug) {
    var colorVariants = variants.filter(function (v) { return v.color_slug === colorSlug; });
    var images = [];
    var seen = new Set();
    colorVariants.forEach(function (v) {
      (v.images || []).forEach(function (img) {
        if (!seen.has(img.url)) {
          seen.add(img.url);
          images.push(img);
        }
      });
    });
    return images;
  }

  function getFallbackImage() {
    if (coverImage) return coverImage;
    return '/static/img/placeholder-product.jpg';
  }

  function preloadImage(src) {
    var img = new Image();
    img.src = src;
  }

  function setImage(src, alt) {
    mainImage.style.opacity = '0';
    preloadImage(src);
    setTimeout(function () {
      mainImage.src = src;
      mainImage.alt = alt || '';
      mainImage.onload = function () {
        mainImage.classList.add('loaded');
        mainImage.style.opacity = '1';
      };
      if (mainImage.complete) {
        mainImage.classList.add('loaded');
        mainImage.style.opacity = '1';
      }
    }, 150);
  }

  function renderColors() {
    colorOptionsContainer.innerHTML = '';
    var colors = getUniqueColors();
    if (colors.length === 0) {
      colorOptionsContainer.innerHTML = '<span class="text-sm text-marplata-muted">No hay colores disponibles</span>';
      return;
    }
    colors.forEach(function (c) {
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'group relative w-12 h-12 rounded-full p-1 border border-marplata-secondary transition-all duration-300 hover:border-marplata-primary focus:outline-none focus:ring-2 focus:ring-marplata-primary/30';
      btn.setAttribute('data-color', c.color_slug);
      btn.setAttribute('title', c.color);
      btn.setAttribute('aria-label', 'Color ' + c.color);

      var swatch = document.createElement('span');
      swatch.className = 'block w-full h-full rounded-full border border-black/5 shadow-inner';
      swatch.style.backgroundColor = cssColor(c.color_slug);

      var label = document.createElement('span');
      label.className = 'absolute -bottom-7 left-1/2 -translate-x-1/2 text-[10px] font-medium uppercase tracking-wide text-marplata-text-muted opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap';
      label.textContent = c.color;

      btn.appendChild(swatch);
      btn.appendChild(label);

      btn.addEventListener('click', function () {
        selectColor(c.color_slug);
      });

      colorOptionsContainer.appendChild(btn);
    });
  }

  function cssColor(colorSlug) {
    var map = {
      'negro': '#1a1a1a',
      'blanco': '#f8f8f8',
      'azul-marino': '#1a3a5c',
      'azul': '#4a7fc9',
      'rojo': '#c0392b',
      'rosa': '#d8a7b1',
      'verde': '#5a8f7b',
      'beige': '#d9cbb6',
      'gris': '#7f8c8d',
      'amarillo': '#f1c40f',
      'naranja': '#e67e22',
      'morado': '#8e44ad',
      'cafe': '#6e4c35',
      'turquesa': '#1abc9c',
      'coral': '#ff7f50'
    };
    return map[colorSlug] || '#C8D8E6';
  }

  function renderSizeOptions(container, sizes, selectedSize, prefix) {
    container.innerHTML = '';
    if (!selectedColor) return;

    if (sizes.length === 0) {
      container.innerHTML = '<span class="text-sm text-marplata-muted">No hay tallas disponibles</span>';
      return;
    }

    sizes.forEach(function (size) {
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'min-w-[52px] h-12 px-4 border border-marplata-secondary text-sm font-medium text-marplata-text transition-all duration-300 hover:border-marplata-primary focus:outline-none';
      btn.textContent = size;
      btn.setAttribute('data-size', size);
      btn.setAttribute('aria-label', prefix + ' ' + size);

      var variant = getVariant(selectedColor, prefix === 'Top' ? size : selectedTopSize, prefix === 'Tanga' ? size : selectedBottomSize);
      if (variant && variant.stock <= 0) {
        btn.classList.add('opacity-40', 'cursor-not-allowed', 'line-through');
        btn.title = 'Agotado';
      }

      btn.addEventListener('click', function () {
        if (!btn.classList.contains('cursor-not-allowed')) {
          if (prefix === 'Top') {
            selectTopSize(size);
          } else {
            selectBottomSize(size);
          }
        }
      });

      container.appendChild(btn);
    });
  }

  function renderSizes() {
    if (!selectedColor) {
      topSizeOptionsContainer.innerHTML = '';
      bottomSizeOptionsContainer.innerHTML = '';
      return;
    }
    renderSizeOptions(topSizeOptionsContainer, getTopSizesForColor(selectedColor), selectedTopSize, 'Top');
    renderSizeOptions(bottomSizeOptionsContainer, getBottomSizesForColor(selectedColor), selectedBottomSize, 'Tanga');
  }

  function selectColor(colorSlug) {
    selectedColor = colorSlug;
    selectedTopSize = null;
    selectedBottomSize = null;

    document.querySelectorAll('#colorOptions button').forEach(function (btn) {
      var isActive = btn.getAttribute('data-color') === colorSlug;
      btn.classList.toggle('border-marplata-primary', isActive);
      btn.classList.toggle('ring-2', isActive);
      btn.classList.toggle('ring-marplata-primary/30', isActive);
      btn.classList.toggle('border-marplata-secondary', !isActive);
    });

    renderSizes();
    updateSelection();
  }

  function selectTopSize(size) {
    selectedTopSize = size;
    markSelectedSize(topSizeOptionsContainer, size);
    updateSelection();
  }

  function selectBottomSize(size) {
    selectedBottomSize = size;
    markSelectedSize(bottomSizeOptionsContainer, size);
    updateSelection();
  }

  function markSelectedSize(container, size) {
    if (!container) return;
    container.querySelectorAll('button').forEach(function (btn) {
      var isActive = btn.getAttribute('data-size') === size && !btn.classList.contains('cursor-not-allowed');
      btn.classList.toggle('bg-marplata-primary', isActive);
      btn.classList.toggle('text-white', isActive);
      btn.classList.toggle('border-marplata-primary', isActive);
      btn.classList.toggle('bg-white', !isActive);
      btn.classList.toggle('text-marplata-text', !isActive);
      btn.classList.toggle('border-marplata-secondary', !isActive);
    });
  }

  function formatPrice(value) {
    var num = Number(value) || 0;
    return '$' + Math.round(num).toLocaleString('es-CO');
  }

  function updateSelection() {
    var variant = null;
    if (selectedColor && selectedTopSize && selectedBottomSize) {
      variant = getVariant(selectedColor, selectedTopSize, selectedBottomSize);
    }

    if (variant) {
      var price = variant.price_override || basePrice;
      productPrice.textContent = formatPrice(price);

      if (variant.stock > 0) {
        stockStatus.innerHTML = '<span class="w-2 h-2 rounded-full bg-emerald-500"></span> Disponible (' + variant.stock + ' unidades)';
        stockStatus.className = 'product-detail__stock-status inline-flex items-center gap-2 text-sm font-medium text-emerald-600';
        addToCartBtn.disabled = false;
        if (buyWhatsappBtn) buyWhatsappBtn.classList.remove('hidden');
      } else {
        stockStatus.innerHTML = '<span class="w-2 h-2 rounded-full bg-marplata-danger"></span> Agotado';
        stockStatus.className = 'product-detail__stock-status inline-flex items-center gap-2 text-sm font-medium text-marplata-danger';
        addToCartBtn.disabled = true;
        if (buyWhatsappBtn) buyWhatsappBtn.classList.add('hidden');
      }

      renderImagesForColor(selectedColor);
    } else {
      productPrice.textContent = formatPrice(basePrice);
      if (!selectedColor) {
        stockStatus.innerHTML = 'Selecciona color y tallas';
      } else if (!selectedTopSize || !selectedBottomSize) {
        stockStatus.innerHTML = 'Selecciona talla top y tanga';
      } else {
        stockStatus.innerHTML = 'Combinación no disponible';
      }
      stockStatus.className = 'product-detail__stock-status inline-flex items-center gap-2 text-sm font-medium text-marplata-text-muted';
      addToCartBtn.disabled = true;

      renderImagesForColor(selectedColor);
    }
  }

  function renderImagesForColor(colorSlug) {
    thumbnailContainer.innerHTML = '';
    currentImageIndex = 0;

    var colorImages = colorSlug ? getImagesForColor(colorSlug) : [];
    if (colorImages.length > 0) {
      currentImages = colorImages;
    } else if (coverImage) {
      currentImages = [{ url: coverImage, alt: '' }];
    } else {
      currentImages = [];
    }

    if (currentImages.length > 0) {
      setImage(currentImages[0].url, currentImages[0].alt || '');

      currentImages.forEach(function (img, index) {
        var thumb = document.createElement('img');
        thumb.src = img.url;
        thumb.alt = img.alt || '';
        thumb.loading = 'lazy';
        thumb.className = 'w-16 h-16 lg:w-20 lg:h-20 object-cover border-2 cursor-pointer transition-all duration-300 opacity-60 hover:opacity-100 flex-shrink-0 ' + (index === 0 ? 'border-marplata-primary opacity-100' : 'border-transparent');
        thumb.addEventListener('click', function () {
          selectImage(index);
        });
        thumbnailContainer.appendChild(thumb);
      });

      if (imageCounter) {
        imageCounter.textContent = '1 / ' + currentImages.length;
        imageCounter.classList.remove('hidden');
      }
    } else {
      setImage(getFallbackImage(), 'Sin imagen');
      if (imageCounter) imageCounter.classList.add('hidden');
    }
  }

  function selectImage(index) {
    if (!currentImages.length) return;
    currentImageIndex = (index + currentImages.length) % currentImages.length;
    var img = currentImages[currentImageIndex];
    setImage(img.url, img.alt || '');

    document.querySelectorAll('#thumbnailContainer img').forEach(function (t, i) {
      var isActive = i === currentImageIndex;
      t.classList.toggle('border-marplata-primary', isActive);
      t.classList.toggle('opacity-100', isActive);
      t.classList.toggle('border-transparent', !isActive);
      t.classList.toggle('opacity-60', !isActive);
    });

    if (imageCounter) {
      imageCounter.textContent = (currentImageIndex + 1) + ' / ' + currentImages.length;
    }
  }

  function openLightbox(index) {
    if (!lightbox || !currentImages.length) return;
    currentImageIndex = index || 0;
    lightboxImage.src = currentImages[currentImageIndex].url;
    lightboxImage.alt = currentImages[currentImageIndex].alt || '';
    lightboxCounter.textContent = (currentImageIndex + 1) + ' / ' + currentImages.length;
    lightboxThumbs.innerHTML = '';
    currentImages.forEach(function (img, i) {
      var t = document.createElement('img');
      t.src = img.url;
      t.alt = img.alt || '';
      t.className = 'w-12 h-12 object-cover cursor-pointer opacity-50 hover:opacity-100 border-2 ' + (i === currentImageIndex ? 'border-white opacity-100' : 'border-transparent');
      t.addEventListener('click', function (e) {
        e.stopPropagation();
        lightboxShow(i);
      });
      lightboxThumbs.appendChild(t);
    });
    lightbox.classList.remove('hidden');
    lightbox.classList.add('flex');
    document.body.style.overflow = 'hidden';
  }

  function closeLightbox() {
    if (!lightbox) return;
    lightbox.classList.add('hidden');
    lightbox.classList.remove('flex');
    document.body.style.overflow = '';
  }

  function lightboxShow(index) {
    if (!currentImages.length) return;
    currentImageIndex = (index + currentImages.length) % currentImages.length;
    lightboxImage.style.opacity = '0';
    setTimeout(function () {
      lightboxImage.src = currentImages[currentImageIndex].url;
      lightboxImage.alt = currentImages[currentImageIndex].alt || '';
      lightboxImage.style.opacity = '1';
    }, 100);
    lightboxCounter.textContent = (currentImageIndex + 1) + ' / ' + currentImages.length;
    Array.from(lightboxThumbs.children).forEach(function (t, i) {
      var isActive = i === currentImageIndex;
      t.classList.toggle('border-white', isActive);
      t.classList.toggle('opacity-100', isActive);
      t.classList.toggle('border-transparent', !isActive);
      t.classList.toggle('opacity-50', !isActive);
    });
  }

  if (openLightboxBtn) {
    openLightboxBtn.addEventListener('click', function () {
      openLightbox(currentImageIndex);
    });
  }
  if (mainImage) {
    mainImage.addEventListener('click', function () {
      openLightbox(currentImageIndex);
    });
  }
  if (closeLightboxBtn) closeLightboxBtn.addEventListener('click', closeLightbox);
  if (lightboxPrevBtn) lightboxPrevBtn.addEventListener('click', function () { lightboxShow(currentImageIndex - 1); });
  if (lightboxNextBtn) lightboxNextBtn.addEventListener('click', function () { lightboxShow(currentImageIndex + 1); });
  if (lightbox) {
    lightbox.addEventListener('click', function (e) {
      if (e.target === lightbox) closeLightbox();
    });
  }

  document.addEventListener('keydown', function (e) {
    if (!lightbox || lightbox.classList.contains('hidden')) return;
    if (e.key === 'Escape') closeLightbox();
    if (e.key === 'ArrowLeft') lightboxShow(currentImageIndex - 1);
    if (e.key === 'ArrowRight') lightboxShow(currentImageIndex + 1);
  });

  var touchStartX = 0;
  var touchEndX = 0;
  if (lightbox) {
    lightbox.addEventListener('touchstart', function (e) {
      touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });
    lightbox.addEventListener('touchend', function (e) {
      touchEndX = e.changedTouches[0].screenX;
      var diff = touchStartX - touchEndX;
      if (Math.abs(diff) < 50) return;
      if (diff > 0) lightboxShow(currentImageIndex + 1);
      else lightboxShow(currentImageIndex - 1);
    }, { passive: true });
  }

  if (mainImageContainer && zoomLens) {
    mainImageContainer.addEventListener('mousemove', function (e) {
      var rect = mainImageContainer.getBoundingClientRect();
      var x = e.clientX - rect.left;
      var y = e.clientY - rect.top;
      var lensSize = 120;
      var lensX = x - lensSize / 2;
      var lensY = y - lensSize / 2;

      lensX = Math.max(0, Math.min(lensX, rect.width - lensSize));
      lensY = Math.max(0, Math.min(lensY, rect.height - lensSize));

      zoomLens.style.left = lensX + 'px';
      zoomLens.style.top = lensY + 'px';
    });

    mainImageContainer.addEventListener('mouseleave', function () {
      zoomLens.style.opacity = '0';
    });

    mainImageContainer.addEventListener('mouseenter', function () {
      zoomLens.style.opacity = '1';
    });
  }

  addToCartBtn.addEventListener('click', function () {
    var variant = getVariant(selectedColor, selectedTopSize, selectedBottomSize);
    if (!variant) return;

    addToCartBtn.disabled = true;
    var originalText = addToCartBtn.textContent;
    addToCartBtn.textContent = 'Agregando...';

    var formData = new FormData();
    formData.append('variant_id', variant.id);
    formData.append('quantity', window.getProductQuantity ? String(window.getProductQuantity()) : '1');

    fetch('/carrito/api/add/', {
      method: 'POST',
      headers: { 'X-CSRFToken': csrfToken },
      body: formData,
    })
    .then(function (response) {
      if (!response.ok) throw new Error('HTTP ' + response.status);
      return response.json();
    })
    .then(function (data) {
      if (data.success) {
        updateCartCounter(data.total_items);
        addToCartBtn.textContent = 'Agregado';
        addToCartBtn.classList.remove('bg-marplata-primary', 'hover:bg-marplata-primary-dark');
        addToCartBtn.classList.add('bg-emerald-600');
        setTimeout(function () {
          addToCartBtn.textContent = originalText;
          addToCartBtn.disabled = false;
          addToCartBtn.classList.remove('bg-emerald-600');
          addToCartBtn.classList.add('bg-marplata-primary', 'hover:bg-marplata-primary-dark');
        }, 1500);
      } else {
        addToCartBtn.textContent = data.error || 'No se pudo agregar';
        setTimeout(function () {
          addToCartBtn.textContent = originalText;
          addToCartBtn.disabled = false;
        }, 2500);
      }
    })
    .catch(function (err) {
      console.error('[MARPLATA] Add to cart error:', err);
      addToCartBtn.textContent = 'Error de conexión';
      setTimeout(function () {
        addToCartBtn.textContent = originalText;
        addToCartBtn.disabled = false;
      }, 2500);
    });
  });

  function updateCartCounter(count) {
    var cartCountEl = document.getElementById('cartCount');
    if (cartCountEl) {
      cartCountEl.textContent = count;
    }
  }

  function loadCartCount() {
    fetch('/carrito/api/summary/')
      .then(function (response) { return response.json(); })
      .then(function (data) {
        updateCartCounter(data.total_items);
      })
      .catch(function () {});
  }

  renderColors();
  loadCartCount();

  if (variants.length > 0) {
    selectColor(variants[0].color_slug);
    var topSizes = getTopSizesForColor(selectedColor);
    var bottomSizes = getBottomSizesForColor(selectedColor);
    if (topSizes.length) selectTopSize(topSizes[0]);
    if (bottomSizes.length) selectBottomSize(bottomSizes[0]);
  } else {
    if (coverImage) {
      setImage(coverImage, '');
    } else {
      setImage(getFallbackImage(), 'Sin imagen');
    }
    addToCartBtn.disabled = true;
    addToCartBtn.textContent = 'Sin stock';
  }
});
