from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
import csv

from .models import CustomUser, NewsletterSubscriber, WishlistItem


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'first_name', 'last_name', 'phone', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active', 'date_joined']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Información personal'), {'fields': ('first_name', 'last_name', 'phone')}),
        (_('Permisos'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Fechas importantes'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone', 'password1', 'password2'),
        }),
    )
    search_fields = ['email', 'first_name', 'last_name', 'phone']
    ordering = ['email']


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'is_active', 'source', 'subscribed_at', 'unsubscribed_at']
    list_filter = ['is_active', 'source', 'subscribed_at']
    search_fields = ['email', 'first_name']
    readonly_fields = ['subscribed_at', 'unsubscribed_at']
    actions = ['export_csv', 'mark_active', 'mark_inactive']
    list_per_page = 50

    @admin.action(description='Exportar a CSV')
    def export_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="newsletter_subscribers.csv"'
        writer = csv.writer(response)
        writer.writerow(['Email', 'Nombre', 'Activo', 'Origen', 'Suscrito', 'Desuscrito'])
        for s in queryset:
            writer.writerow([
                s.email,
                s.first_name,
                'Sí' if s.is_active else 'No',
                s.source,
                s.subscribed_at.strftime('%Y-%m-%d %H:%M') if s.subscribed_at else '',
                s.unsubscribed_at.strftime('%Y-%m-%d %H:%M') if s.unsubscribed_at else '',
            ])
        return response

    @admin.action(description='Marcar como activos')
    def mark_active(self, request, queryset):
        updated = queryset.update(is_active=True, unsubscribed_at=None)
        self.message_user(request, f'{updated} suscriptor(es) reactivado(s).')

    @admin.action(description='Marcar como inactivos')
    def mark_inactive(self, request, queryset):
        for s in queryset:
            s.unsubscribe()
        self.message_user(request, f'{queryset.count()} suscriptor(es) desactivado(s).')


@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'added_at']
    list_filter = ['added_at']
    search_fields = ['user__email', 'product__name']
    readonly_fields = ['added_at']
    list_select_related = ['user', 'product']
