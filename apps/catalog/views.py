from django.db.models import Sum, Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Product, Collection


def product_list(request, collection_slug=None):
    collections = Collection.objects.filter(is_active=True)
    products = Product.objects.filter(is_active=True).select_related('collection').prefetch_related('variants', 'variants__images')

    collection = None
    if collection_slug:
        collection = get_object_or_404(Collection, slug=collection_slug, is_active=True)
        products = products.filter(collection=collection)

    products = products.annotate(
        available_stock=Sum('variants__stock', filter=Q(variants__is_active=True))
    ).order_by('-created_at')

    user_wishlist_ids = set()
    if request.user.is_authenticated:
        from apps.accounts.models import WishlistItem
        for pid in WishlistItem.objects.filter(
            user=request.user, product__in=products
        ).values_list('product_id', flat=True):
            user_wishlist_ids.add(str(pid))

    return render(request, 'catalog/product_list.html', {
        'products': products,
        'collections': collections,
        'collection': collection,
        'user_wishlist_ids': user_wishlist_ids,
        'page_title': collection.name if collection else 'Colección',
    })


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.prefetch_related('variants', 'variants__images'),
        slug=slug,
        is_active=True,
    )

    in_wishlist = False
    if request.user.is_authenticated:
        from apps.accounts.models import WishlistItem
        in_wishlist = WishlistItem.objects.filter(
            user=request.user, product=product
        ).exists()

    og_image = None
    if product.cover_image:
        og_image = request.build_absolute_uri(product.cover_image.url)
    elif product.primary_image:
        og_image = request.build_absolute_uri(product.primary_image.url)

    return render(request, 'catalog/product_detail.html', {
        'product': product,
        'in_wishlist': in_wishlist,
        'og_image': og_image,
        'page_title': product.name,
        'page_meta_title': product.meta_title or product.name,
        'page_meta_description': product.meta_description or product.description[:150],
    })


def search(request):
    query = (request.GET.get('q') or '').strip()
    products = Product.objects.none()
    collections = []

    if query:
        products = Product.objects.filter(
            is_active=True
        ).filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(story__icontains=query) |
            Q(materials__icontains=query) |
            Q(collection__name__icontains=query)
        ).select_related('collection').prefetch_related('variants', 'variants__images').annotate(
            available_stock=Sum('variants__stock', filter=Q(variants__is_active=True))
        ).distinct().order_by('-created_at')

        collections = Collection.objects.filter(
            is_active=True, name__icontains=query
        ).order_by('name')

    return render(request, 'catalog/search.html', {
        'products': products,
        'collections': collections,
        'query': query,
        'total_results': products.count(),
        'page_title': f'Búsqueda: {query}' if query else 'Buscar',
        'page_meta_title': f'Buscar "{query}"' if query else 'Buscar productos',
    })


def search_suggestions(request):
    """AJAX endpoint that returns product name suggestions."""
    from django.http import JsonResponse
    query = (request.GET.get('q') or '').strip()
    suggestions = []
    if len(query) >= 2:
        products = Product.objects.filter(
            is_active=True
        ).filter(
            Q(name__icontains=query) | Q(collection__name__icontains=query)
        ).select_related('collection')[:8]
        suggestions = [
            {
                'name': p.name,
                'slug': p.slug,
                'price': float(p.base_price),
                'collection': p.collection.name if p.collection else '',
            }
            for p in products
        ]
    return JsonResponse({'suggestions': suggestions})
