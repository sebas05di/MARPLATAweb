from django.templatetags.static import static

from .models import SiteConfig, Page


def site_config(request):
    """Make SiteConfig and footer pages available in all templates."""
    pages = Page.objects.filter(
        is_active=True, show_in_footer=True
    ).order_by('footer_section', 'order', 'title')

    footer_pages = {
        'navegacion': [],
        'legal': [],
        'ayuda': [],
    }
    for page in pages:
        section = page.footer_section or 'legal'
        footer_pages.setdefault(section, []).append(page)

    return {
        'site_config': SiteConfig.load(),
        'footer_pages': footer_pages,
        'default_og_image': request.build_absolute_uri(static('img/branding/og-image.png')),
    }
