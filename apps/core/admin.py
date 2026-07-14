from django.contrib import admin

from .models import SiteConfig, DataConsentLog, Page


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'whatsapp_number', 'contact_email', 'updated_at']
    fieldsets = (
        ('Información general', {
            'fields': ('site_name', 'site_tagline', 'whatsapp_number', 'whatsapp_message_template')
        }),
        ('Contacto', {
            'fields': ('contact_email', 'contact_phone', 'address', 'business_hours')
        }),
        ('Redes sociales', {
            'fields': ('instagram_url', 'facebook_url', 'tiktok_url', 'pinterest_url'),
            'classes': ('collapse',),
        }),
        ('Envíos', {
            'fields': ('shipping_cost', 'free_shipping_threshold'),
            'classes': ('collapse',),
        }),
    )

    def has_add_permission(self, request):
        if SiteConfig.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(DataConsentLog)
class DataConsentLogAdmin(admin.ModelAdmin):
    list_display = ['email', 'user', 'ip_address', 'consent_version', 'consented_at']
    list_filter = ['consent_version', 'consented_at']
    search_fields = ['email', 'user__email']
    readonly_fields = ['consented_at']


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'is_active', 'show_in_footer', 'footer_section', 'order', 'updated_at']
    list_filter = ['is_active', 'show_in_footer', 'footer_section', 'slug']
    list_editable = ['is_active', 'show_in_footer', 'order']
    search_fields = ['title', 'content']
    prepopulated_fields = {}
    fieldsets = (
        (None, {
            'fields': ('slug', 'title', 'subtitle', 'content', 'is_active')
        }),
        ('Footer', {
            'fields': ('show_in_footer', 'footer_section', 'order'),
            'classes': ('collapse',),
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',),
        }),
    )
