from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from apps.core.views import home, site_config_api, page_detail, robots_txt, sitemap_xml, health_check
from apps.catalog.views import product_detail
from apps.orders.dashboard import dashboard

urlpatterns = [
    path('admin/dashboard/', dashboard, name='admin_dashboard'),
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('cuenta/', include('apps.accounts.urls')),
    path('coleccion/', include('apps.catalog.urls')),
    path('producto/<slug:slug>/', product_detail, name='product_detail'),
    path('carrito/', include('apps.cart.urls')),
    path('pedido/', include('apps.orders.urls')),
    path('pagina/<slug:slug>/', page_detail, name='page_detail'),
    path('api/site-config/', site_config_api, name='site_config_api'),
    path('health/', health_check, name='health_check'),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap_xml, name='sitemap_xml'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
