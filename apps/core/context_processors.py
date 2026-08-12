from django.core.cache import cache
from django.templatetags.static import static

from .models import SiteConfig, Page

CUIDADOS_CACHE_KEY = 'cuidados_page'
CUIDADOS_CACHE_TTL = 300  # 5 minutes
CAMBIOS_CACHE_KEY = 'cambios_page'
CAMBIOS_CACHE_TTL = 300  # 5 minutes
ENVIOS_CACHE_KEY = 'envios_page'
ENVIOS_CACHE_TTL = 300  # 5 minutes


def _get_cuidados_page():
    """Return the 'cuidados-prenda' Page, cached for CUIDADOS_CACHE_TTL seconds."""
    page = cache.get(CUIDADOS_CACHE_KEY)
    if page is None:
        page = Page.objects.filter(slug='cuidados-prenda', is_active=True).first()
        cache.set(CUIDADOS_CACHE_KEY, page, CUIDADOS_CACHE_TTL)
    return page


def _get_cambios_page():
    """Return the 'cambios-devoluciones' Page, cached for CAMBIOS_CACHE_TTL seconds."""
    page = cache.get(CAMBIOS_CACHE_KEY)
    if page is None:
        page = Page.objects.filter(slug='cambios-devoluciones', is_active=True).first()
        cache.set(CAMBIOS_CACHE_KEY, page, CAMBIOS_CACHE_TTL)
    return page


def _get_envios_page():
    """Return the 'envios-devoluciones' Page, cached for ENVIOS_CACHE_TTL seconds."""
    page = cache.get(ENVIOS_CACHE_KEY)
    if page is None:
        page = Page.objects.filter(slug='envios-devoluciones', is_active=True).first()
        cache.set(ENVIOS_CACHE_KEY, page, ENVIOS_CACHE_TTL)
    return page


def site_config(request):
    """Make SiteConfig, footer pages and care page available in all templates."""
    pages = Page.objects.filter(
        is_active=True, show_in_footer=True
    ).order_by('footer_section', 'order', 'title')

    footer_pages = {
        'historia': [],
        'legal': [],
        'envios': [],
        'cuidados': [],
        'ayuda': [],
    }
    for page in pages:
        section = page.footer_section or 'legal'
        footer_pages.setdefault(section, []).append(page)

    return {
        'site_config': SiteConfig.load(),
        'footer_pages': footer_pages,
        'cuidados_page': _get_cuidados_page(),
        'cambios_page': _get_cambios_page(),
        'envios_page': _get_envios_page(),
        'default_og_image': request.build_absolute_uri(static('img/branding/og-image.png')),
    }
