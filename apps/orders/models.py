import uuid

from django.db import models
from django.db.models import F
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import CustomUser
from apps.catalog.models import ProductVariant


class WhatsAppOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Pendiente')),
        ('contacted', _('Contactado')),
        ('confirmed', _('Confirmado')),
        ('dispatched', _('Despachado')),
        ('delivered', _('Entregado')),
        ('cancelled', _('Cancelado')),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.CharField(
        _('número de orden'), max_length=20, unique=True
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='whatsapp_orders',
        verbose_name=_('usuario'),
    )
    customer_email = models.EmailField(_('correo del cliente'))
    customer_name = models.CharField(_('nombre del cliente'), max_length=200)
    customer_phone = models.CharField(_('teléfono del cliente'), max_length=30)
    status = models.CharField(
        _('estado'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
    )
    notes = models.TextField(_('notas'), blank=True)
    whatsapp_message_id = models.CharField(
        _('ID de mensaje WhatsApp'), max_length=100, blank=True
    )
    coupon_code = models.CharField(
        _('código de cupón'), max_length=50, blank=True,
    )
    discount_amount = models.DecimalField(
        _('descuento aplicado'),
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    shipping_address = models.CharField(
        _('dirección de envío'), max_length=255, blank=True,
    )
    shipping_city = models.CharField(
        _('ciudad de envío'), max_length=120, blank=True,
    )
    shipping_department = models.CharField(
        _('departamento/estado de envío'), max_length=120, blank=True,
    )
    shipping_notes = models.TextField(
        _('notas de envío'), blank=True,
        help_text=_('Referencias, edificio, apartamento, etc.'),
    )
    shipping_cost = models.DecimalField(
        _('costo de envío'),
        max_digits=10, decimal_places=2, default=0,
    )
    tracking_number = models.CharField(
        _('número de guía'), max_length=80, blank=True,
    )
    tracking_url = models.URLField(
        _('URL de rastreo'), max_length=500, blank=True,
    )
    shipping_carrier = models.CharField(
        _('transportadora'), max_length=80, blank=True,
        help_text=_('Ej: Servientrega, Coordinadora, Interrapidisimo'),
    )
    shipped_at = models.DateTimeField(
        _('despachado en'), null=True, blank=True,
    )
    delivered_at = models.DateTimeField(
        _('entregado en'), null=True, blank=True,
    )
    payment_method = models.CharField(
        _('método de pago'),
        max_length=40, blank=True,
        help_text=_('Ej: Transferencia, Contraentrega, Nequi'),
    )

    created_at = models.DateTimeField(_('creado en'), auto_now_add=True)
    updated_at = models.DateTimeField(_('actualizado en'), auto_now=True)

    class Meta:
        verbose_name = _('pedido por WhatsApp')
        verbose_name_plural = _('pedidos por WhatsApp')
        ordering = ['-created_at']

    @property
    def status_color_class(self):
        colors = {
            'pending': 'bg-amber-100 text-amber-800',
            'contacted': 'bg-blue-100 text-blue-800',
            'confirmed': 'bg-emerald-100 text-emerald-800',
            'dispatched': 'bg-marplata-primary-soft text-marplata-primary',
            'delivered': 'bg-emerald-100 text-emerald-800',
            'cancelled': 'bg-red-100 text-red-800',
        }
        return colors.get(self.status, 'bg-gray-100 text-gray-800')

    @property
    def total_amount(self):
        subtotal = sum(float(item.subtotal) for item in self.items.all())
        return max(0, subtotal - float(self.discount_amount or 0))

    @property
    def subtotal_amount(self):
        return sum(float(item.subtotal) for item in self.items.all())

    def __str__(self):
        return f"Orden {self.order_number} — {self.customer_name}"

    def save(self, *args, **kwargs):
        old_status = None
        if self.pk:
            try:
                old = WhatsAppOrder.objects.get(pk=self.pk)
                old_status = old.status
            except WhatsAppOrder.DoesNotExist:
                pass

        if not self.order_number:
            from datetime import datetime
            now = datetime.now()
            prefix = now.strftime('%Y%m%d')
            suffix = str(self.id)[:8].upper() if self.id else str(uuid.uuid4())[:8].upper()
            self.order_number = f"{prefix}-{suffix}"

        super().save(*args, **kwargs)

        if old_status and old_status != 'cancelled' and self.status == 'cancelled':
            for item in self.items.all():
                if item.variant:
                    item.variant.stock = F('stock') + item.quantity
                    item.variant.save(update_fields=['stock'])

        if old_status and old_status != self.status:
            from apps.core.emails import send_order_status_update
            try:
                send_order_status_update(self, old_status=old_status)
            except Exception:
                pass

        from django.utils import timezone
        if old_status and old_status != 'dispatched' and self.status == 'dispatched' and not self.shipped_at:
            self.shipped_at = timezone.now()
            WhatsAppOrder.objects.filter(pk=self.pk).update(shipped_at=self.shipped_at)
        if old_status and old_status != 'delivered' and self.status == 'delivered' and not self.delivered_at:
            self.delivered_at = timezone.now()
            WhatsAppOrder.objects.filter(pk=self.pk).update(delivered_at=self.delivered_at)


class WhatsAppOrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(
        WhatsAppOrder,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('pedido'),
    )
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.SET_NULL,
        null=True,
        related_name='order_items',
        verbose_name=_('variante'),
    )
    product_name_snapshot = models.CharField(
        _('nombre del producto (snapshot)'), max_length=200
    )
    variant_snapshot = models.CharField(
        _('variante (snapshot)'), max_length=200
    )
    quantity = models.PositiveIntegerField(_('cantidad'))
    unit_price = models.DecimalField(
        _('precio unitario'), max_digits=10, decimal_places=2
    )
    created_at = models.DateTimeField(_('creado en'), auto_now_add=True)

    class Meta:
        verbose_name = _('ítem de pedido')
        verbose_name_plural = _('ítems de pedido')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.quantity} x {self.product_name_snapshot}"

    @property
    def subtotal(self):
        if self.quantity is None or self.unit_price is None:
            return 0
        return self.quantity * self.unit_price
