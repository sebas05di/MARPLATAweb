from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum, Q, F

from .models import Collection, Product, ProductVariant, VariantImage, Promotion


class StockLevelFilter(admin.SimpleListFilter):
    title = 'nivel de stock'
    parameter_name = 'stock_level'

    def lookups(self, request, model_admin):
        return (
            ('out', 'Agotados (stock = 0)'),
            ('low', 'Stock bajo'),
            ('ok', 'Stock OK'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'out':
            return queryset.filter(stock=0)
        if self.value() == 'low':
            return queryset.filter(stock__gt=0, stock__lte=F('low_stock_threshold'))
        if self.value() == 'ok':
            return queryset.filter(stock__gt=F('low_stock_threshold'))
        return queryset


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


class VariantImageInline(admin.TabularInline):
    model = VariantImage
    extra = 1


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['product', 'color', 'size', 'sku', 'stock_badge', 'low_stock_threshold', 'final_price', 'is_active']
    list_filter = ['is_active', 'color', 'size', 'product__collection', StockLevelFilter]
    search_fields = ['sku', 'product__name', 'color']
    list_editable = ['low_stock_threshold']
    actions = ['mark_active', 'mark_inactive']
    inlines = [VariantImageInline]

    @admin.display(description='Stock', ordering='stock')
    def stock_badge(self, obj):
        if obj.stock <= 0:
            color = '#d9534f'
            label = 'Agotado'
        elif obj.is_low_stock:
            color = '#f0ad4e'
            label = f'{obj.stock} (bajo)'
        else:
            color = '#5cb85c'
            label = str(obj.stock)
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: 600;">{}</span>',
            color, label,
        )

    @admin.action(description='Marcar como activas')
    def mark_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} variante(s) marcada(s) como activas.')

    @admin.action(description='Marcar como inactivas')
    def mark_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} variante(s) marcada(s) como inactivas.')


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ['color', 'color_slug', 'size', 'sku', 'stock', 'low_stock_threshold', 'price_override', 'is_active']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'collection', 'base_price', 'total_stock', 'is_active', 'created_at']
    list_filter = ['is_active', 'collection']
    search_fields = ['name', 'description', 'story', 'materials']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductVariantInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'collection', 'description', 'story', 'materials', 'base_price', 'is_active')
        }),
        ('Imagen y SEO', {
            'fields': ('cover_image', 'meta_title', 'meta_description'),
            'classes': ('collapse',),
        }),
    )

    @admin.display(description='Stock total')
    def total_stock(self, obj):
        total = sum(v.stock for v in obj.variants.all() if v.is_active)
        if total <= 0:
            color = '#d9534f'
            label = 'Agotado'
        else:
            low = sum(1 for v in obj.variants.all() if v.is_active and v.is_low_stock)
            if low > 0:
                color = '#f0ad4e'
                label = f'{total} ({low} bajo)'
            else:
                color = '#5cb85c'
                label = str(total)
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: 600;">{}</span>',
            color, label,
        )


@admin.register(VariantImage)
class VariantImageAdmin(admin.ModelAdmin):
    list_display = ['variant', 'is_primary', 'order', 'created_at']
    list_filter = ['is_primary']


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'discount_type', 'discount_value', 'min_purchase', 'usage_count', 'usage_limit', 'is_active', 'start_date', 'end_date']
    list_filter = ['is_active', 'discount_type']
    search_fields = ['name', 'code']
    filter_horizontal = ['applicable_collections']
    fieldsets = (
        (None, {
            'fields': ('name', 'code', 'is_active', 'discount_type', 'discount_value')
        }),
        ('Restricciones', {
            'fields': ('min_purchase', 'usage_limit', 'usage_count', 'start_date', 'end_date'),
        }),
        ('Aplicabilidad', {
            'fields': ('applicable_collections',),
            'classes': ('collapse',),
        }),
    )
