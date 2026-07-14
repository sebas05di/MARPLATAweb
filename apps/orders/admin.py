from django.contrib import admin
from django.utils.html import format_html

from .models import WhatsAppOrder, WhatsAppOrderItem


class WhatsAppOrderItemInline(admin.TabularInline):
    model = WhatsAppOrderItem
    extra = 0
    readonly_fields = ['subtotal', 'variant', 'product_name_snapshot', 'variant_snapshot', 'quantity', 'unit_price']
    can_delete = False
    fields = ['product_name_snapshot', 'variant_snapshot', 'quantity', 'unit_price', 'subtotal']


@admin.register(WhatsAppOrder)
class WhatsAppOrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_number', 'customer_name', 'status_badge',
        'tracking_display', 'shipping_carrier',
        'total_amount', 'created_at',
    ]
    list_filter = ['status', 'shipping_carrier', 'payment_method', 'created_at']
    search_fields = [
        'order_number', 'customer_name', 'customer_email', 'customer_phone',
        'tracking_number', 'coupon_code', 'shipping_address',
    ]
    readonly_fields = [
        'order_number', 'user', 'created_at', 'updated_at',
        'total_amount', 'subtotal_amount', 'shipped_at', 'delivered_at',
        'tracking_link',
    ]
    autocomplete_fields = ['user']
    inlines = [WhatsAppOrderItemInline]
    save_on_top = True
    list_per_page = 25

    fieldsets = (
        ('Información del pedido', {
            'fields': ('order_number', 'user', 'status', 'payment_method', 'created_at', 'updated_at')
        }),
        ('Cliente', {
            'fields': ('customer_name', 'customer_email', 'customer_phone')
        }),
        ('Envío', {
            'fields': (
                'shipping_address', 'shipping_city', 'shipping_department',
                'shipping_notes', 'shipping_cost',
            )
        }),
        ('Tracking', {
            'fields': (
                'shipping_carrier', 'tracking_number', 'tracking_url',
                'tracking_link', 'shipped_at', 'delivered_at',
            ),
            'description': 'Asigná la transportadora y el número de guía. El cliente recibirá un email automático.'
        }),
        ('Totales', {
            'fields': ('subtotal_amount', 'coupon_code', 'discount_amount', 'total_amount')
        }),
        ('Notas internas', {
            'fields': ('notes', 'whatsapp_message_id'),
            'classes': ('collapse',)
        }),
    )

    @admin.display(description='Subtotal')
    def subtotal_amount(self, obj):
        return f"${obj.subtotal_amount:,.0f}"

    @admin.display(description='Total')
    def total_amount(self, obj):
        return f"${obj.total_amount:,.0f}"

    @admin.display(description='Estado', ordering='status')
    def status_badge(self, obj):
        colors = {
            'pending': '#f0ad4e',
            'contacted': '#5bc0de',
            'confirmed': '#5cb85c',
            'dispatched': '#6B8BC8',
            'delivered': '#1e7e34',
            'cancelled': '#d9534f',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 10px; border-radius: 12px; font-size: 11px; text-transform: uppercase; font-weight: 600;">{}</span>',
            color,
            obj.get_status_display()
        )

    @admin.display(description='Tracking')
    def tracking_display(self, obj):
        if not obj.tracking_number:
            return '—'
        if obj.tracking_url:
            return format_html(
                '<a href="{}" target="_blank" style="color:#6B8BC8;text-decoration:underline;">{}</a>',
                obj.tracking_url, obj.tracking_number
            )
        return obj.tracking_number

    @admin.display(description='Enlace de rastreo')
    def tracking_link(self, obj):
        if not obj.tracking_url:
            return '—'
        return format_html(
            '<a href="{}" target="_blank">{}</a>',
            obj.tracking_url, obj.tracking_url
        )

    actions = ['mark_confirmed', 'mark_dispatched', 'mark_delivered', 'mark_cancelled']

    @admin.action(description='Marcar como confirmado')
    def mark_confirmed(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} pedido(s) marcado(s) como confirmado.')

    @admin.action(description='Marcar como despachado')
    def mark_dispatched(self, request, queryset):
        from django.utils import timezone
        updated = 0
        for order in queryset:
            order.status = 'dispatched'
            order.shipped_at = timezone.now()
            order.save()
            updated += 1
        self.message_user(request, f'{updated} pedido(s) marcado(s) como despachado.')

    @admin.action(description='Marcar como entregado')
    def mark_delivered(self, request, queryset):
        from django.utils import timezone
        updated = 0
        for order in queryset:
            order.status = 'delivered'
            order.delivered_at = timezone.now()
            order.save()
            updated += 1
        self.message_user(request, f'{updated} pedido(s) marcado(s) como entregado.')

    @admin.action(description='Marcar como cancelado (restaura stock)')
    def mark_cancelled(self, request, queryset):
        updated = 0
        for order in queryset:
            order.status = 'cancelled'
            order.save()
            updated += 1
        self.message_user(request, f'{updated} pedido(s) cancelado(s). Stock restaurado.')


@admin.register(WhatsAppOrderItem)
class WhatsAppOrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product_name_snapshot', 'variant_snapshot', 'quantity', 'unit_price', 'subtotal']
    list_filter = ['created_at']
    search_fields = ['product_name_snapshot', 'variant_snapshot', 'order__order_number']
    readonly_fields = ['subtotal']
