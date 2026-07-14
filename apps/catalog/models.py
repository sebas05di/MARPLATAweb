import uuid

from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Collection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_('nombre'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)
    description = models.TextField(_('descripción'), blank=True)
    is_active = models.BooleanField(_('activo'), default=True)
    created_at = models.DateTimeField(_('creado en'), auto_now_add=True)
    updated_at = models.DateTimeField(_('actualizado en'), auto_now=True)

    class Meta:
        verbose_name = _('colección')
        verbose_name_plural = _('colecciones')
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_('nombre'), max_length=200)
    slug = models.SlugField(_('slug'), unique=True)
    description = models.TextField(_('descripción'))
    story = models.TextField(_('historia'), blank=True)
    materials = models.CharField(_('materiales'), max_length=200, blank=True)
    base_price = models.DecimalField(
        _('precio base'), max_digits=10, decimal_places=2
    )
    cover_image = models.ImageField(
        _('imagen de portada'),
        upload_to='products/covers/',
        blank=True,
        null=True,
        help_text=_('Imagen principal que se muestra en catálogos y listados.')
    )
    collection = models.ForeignKey(
        Collection,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name=_('colección'),
    )
    is_active = models.BooleanField(_('activo'), default=True)
    meta_title = models.CharField(_('meta título'), max_length=200, blank=True)
    meta_description = models.CharField(
        _('meta descripción'), max_length=300, blank=True
    )
    created_at = models.DateTimeField(_('creado en'), auto_now_add=True)
    updated_at = models.DateTimeField(_('actualizado en'), auto_now=True)

    class Meta:
        verbose_name = _('producto')
        verbose_name_plural = _('productos')
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def primary_image(self):
        """Return primary image for listings."""
        if self.cover_image:
            return self.cover_image
        primary = VariantImage.objects.filter(
            variant__product=self, is_primary=True
        ).select_related('variant').first()
        if primary:
            return primary.image
        first = VariantImage.objects.filter(
            variant__product=self
        ).select_related('variant').first()
        if first:
            return first.image
        return None


class ProductVariant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variants',
        verbose_name=_('producto'),
    )
    color = models.CharField(_('color'), max_length=50)
    color_slug = models.SlugField(_('slug de color'))
    SIZE_CHOICES = [
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
    ]
    size = models.CharField(_('talla'), max_length=4, choices=SIZE_CHOICES)
    sku = models.CharField(_('SKU'), max_length=50, unique=True)
    stock = models.PositiveIntegerField(_('stock'), default=0)
    low_stock_threshold = models.PositiveIntegerField(
        _('umbral de stock bajo'),
        default=3,
        help_text=_('Se notificará cuando el stock sea igual o menor a este número.'),
    )
    price_override = models.DecimalField(
        _('precio especial'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(_('activo'), default=True)
    created_at = models.DateTimeField(_('creado en'), auto_now_add=True)
    updated_at = models.DateTimeField(_('actualizado en'), auto_now=True)

    class Meta:
        verbose_name = _('variante de producto')
        verbose_name_plural = _('variantes de producto')
        unique_together = [['product', 'color_slug', 'size']]
        ordering = ['product', 'color', 'size']

    def __str__(self):
        return f"{self.product.name} — {self.color} / {self.size}"

    def save(self, *args, **kwargs):
        if not self.color_slug:
            self.color_slug = slugify(self.color)
        super().save(*args, **kwargs)

    @property
    def final_price(self):
        if self.price_override is not None:
            return self.price_override
        return self.product.base_price

    @property
    def is_low_stock(self):
        return 0 < self.stock <= self.low_stock_threshold

    @property
    def is_out_of_stock(self):
        return self.stock <= 0


class VariantImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name=_('variante'),
    )
    image = models.ImageField(_('imagen'), upload_to='products/variants/')
    alt_text = models.CharField(_('texto alternativo'), max_length=200, blank=True)
    is_primary = models.BooleanField(_('imagen principal'), default=False)
    order = models.PositiveIntegerField(_('orden'), default=0)
    created_at = models.DateTimeField(_('creado en'), auto_now_add=True)

    class Meta:
        verbose_name = _('imagen de variante')
        verbose_name_plural = _('imágenes de variantes')
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"Imagen de {self.variant}"


class Promotion(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', _('Porcentaje')),
        ('fixed', _('Monto fijo')),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_('nombre'), max_length=200)
    code = models.CharField(
        _('código'), max_length=50, unique=True, blank=True
    )
    discount_type = models.CharField(
        _('tipo de descuento'),
        max_length=20,
        choices=DISCOUNT_TYPE_CHOICES,
    )
    discount_value = models.DecimalField(
        _('valor de descuento'), max_digits=10, decimal_places=2
    )
    min_purchase = models.DecimalField(
        _('compra mínima'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_('Monto mínimo del carrito para que el cupón sea válido.'),
    )
    usage_limit = models.PositiveIntegerField(
        _('límite de usos'),
        null=True,
        blank=True,
        help_text=_('Número máximo de veces que el cupón puede ser usado. Vacío = ilimitado.'),
    )
    usage_count = models.PositiveIntegerField(
        _('usos realizados'), default=0,
    )
    start_date = models.DateTimeField(_('fecha de inicio'))
    end_date = models.DateTimeField(_('fecha de fin'))
    is_active = models.BooleanField(_('activo'), default=True)
    applicable_collections = models.ManyToManyField(
        Collection,
        blank=True,
        related_name='promotions',
        verbose_name=_('colecciones aplicables'),
    )
    created_at = models.DateTimeField(_('creado en'), auto_now_add=True)

    class Meta:
        verbose_name = _('promoción')
        verbose_name_plural = _('promociones')
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def is_valid(self, cart_total=None):
        from django.utils import timezone
        now = timezone.now()
        if not self.is_active:
            return False, 'El cupón está inactivo.'
        if now < self.start_date:
            return False, 'El cupón aún no está disponible.'
        if now > self.end_date:
            return False, 'El cupón ha expirado.'
        if self.usage_limit and self.usage_count >= self.usage_limit:
            return False, 'El cupón ha alcanzado su límite de usos.'
        if cart_total is not None and self.min_purchase and cart_total < self.min_purchase:
            return False, f'Necesitas una compra mínima de ${self.min_purchase:,.0f}.'
        return True, None

    def calculate_discount(self, cart_total):
        if self.discount_type == 'percentage':
            return cart_total * (self.discount_value / 100)
        return min(self.discount_value, cart_total)


class CouponRedemption(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    promotion = models.ForeignKey(
        Promotion,
        on_delete=models.CASCADE,
        related_name='redemptions',
        verbose_name=_('promoción'),
    )
    user = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='coupon_redemptions',
        verbose_name=_('usuario'),
    )
    order = models.ForeignKey(
        'orders.WhatsAppOrder',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='coupon_redemptions',
        verbose_name=_('orden'),
    )
    code_used = models.CharField(_('código usado'), max_length=50)
    discount_applied = models.DecimalField(
        _('descuento aplicado'), max_digits=10, decimal_places=2,
    )
    redeemed_at = models.DateTimeField(_('canjeado en'), auto_now_add=True)

    class Meta:
        verbose_name = _('canje de cupón')
        verbose_name_plural = _('canjes de cupón')
        ordering = ['-redeemed_at']

    def __str__(self):
        return f"{self.code_used} — ${self.discount_applied}"
