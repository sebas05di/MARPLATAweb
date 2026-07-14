from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from apps.catalog.models import Product
from apps.core.models import SiteConfig, Page


def home(request):
    featured_products = (
        Product.objects
        .filter(is_active=True, collection__slug='esencia')
        .select_related('collection')
        .prefetch_related('variants', 'variants__images')
        .order_by('name')[:8]
    )

    return render(request, 'pages/home.html', {
        'featured_products': featured_products,
    })


def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug, is_active=True)
    return render(request, 'pages/page_detail.html', {
        'page': page,
        'page_title': page.title,
        'page_meta_title': page.meta_title or page.title,
        'page_meta_description': page.meta_description or page.subtitle or '',
    })


def site_config_api(request):
    config = SiteConfig.load()
    return JsonResponse({
        'whatsapp_number': config.whatsapp_number,
        'site_name': config.site_name,
        'site_tagline': config.site_tagline,
        'contact_email': config.contact_email,
        'contact_phone': config.contact_phone,
        'address': config.address,
        'business_hours': config.business_hours,
        'instagram_url': config.instagram_url,
        'facebook_url': config.facebook_url,
        'tiktok_url': config.tiktok_url,
        'pinterest_url': config.pinterest_url,
        'shipping_cost': float(config.shipping_cost) if config.shipping_cost else None,
        'free_shipping_threshold': float(config.free_shipping_threshold) if config.free_shipping_threshold else None,
    })


def health_check(request):
    """Health check endpoint for monitoring (used by Render, Railway, etc.)."""
    from django.http import JsonResponse
    from django.db import connection
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
        return JsonResponse({'status': 'ok', 'database': 'ok'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'database': str(e)}, status=500)


def robots_txt(request):
    lines = [
        'User-agent: *',
        'Disallow: /admin/',
        'Disallow: /cuenta/',
        'Disallow: /carrito/',
        'Disallow: /pedido/',
        'Disallow: /api/',
        'Allow: /',
        '',
        f'Sitemap: {request.scheme}://{request.get_host()}/sitemap.xml',
    ]
    return HttpResponse('\n'.join(lines), content_type='text/plain')


def sitemap_xml(request):
    from apps.catalog.models import Collection
    from django.utils import timezone

    host = f"{request.scheme}://{request.get_host()}"
    urls = []

    def add(path, lastmod=None, changefreq='weekly', priority='0.8'):
        if lastmod is None:
            lastmod = timezone.now()
        urls.append(f"""  <url>
    <loc>{host}{path}</loc>
    <lastmod>{lastmod.strftime('%Y-%m-%d')}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>""")

    add('', changefreq='daily', priority='1.0')
    add('/coleccion/', changefreq='daily', priority='0.9')
    add('/pagina/nosotros/', changefreq='monthly', priority='0.6')
    add('/pagina/contacto/', changefreq='monthly', priority='0.6')
    add('/pagina/envios-devoluciones/', changefreq='monthly', priority='0.5')
    add('/pagina/politica-privacidad/', changefreq='monthly', priority='0.4')
    add('/pagina/terminos-condiciones/', changefreq='monthly', priority='0.4')

    for col in Collection.objects.filter(is_active=True):
        add(f"/coleccion/{col.slug}/", changefreq='weekly', priority='0.7')

    for product in Product.objects.filter(is_active=True).only('slug', 'updated_at'):
        add(f"/producto/{product.slug}/", lastmod=product.updated_at, changefreq='weekly', priority='0.8')

    body = '\n'.join(urls)
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{body}
</urlset>"""
    return HttpResponse(xml, content_type='application/xml')
