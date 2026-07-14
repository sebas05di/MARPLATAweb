import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import CustomUser
from apps.catalog.models import ProductVariant


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session_key = models.CharField(
        _('clave de sesión'), max_length=100, blank=True, null=True
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='carts',
        verbose_name=_('usuario'),
    )
    created_at = models.DateTimeField(_('creado en'), auto_now_add=True)
    updated_at = models.DateTimeField(_('actualizado en'), auto_now=True)

    class Meta:
        verbose_name = _('carrito')
        verbose_name_plural = _('carritos')
        ordering = ['-updated_at']

    def __str__(self):
        if self.user:
            return f"Carrito de {self.user.email}"
        return f"Carrito anónimo ({self.session_key[:8] if self.session_key else 'sin sesión'})"


class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('carrito'),
    )
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name=_('variante'),
    )
    quantity = models.PositiveIntegerField(_('cantidad'), default=1)
    created_at = models.DateTimeField(_('creado en'), auto_now_add=True)
    updated_at = models.DateTimeField(_('actualizado en'), auto_now=True)

    class Meta:
        verbose_name = _('ítem de carrito')
        verbose_name_plural = _('ítems de carrito')
        unique_together = [['cart', 'variant']]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.quantity} x {self.variant}"

    @property
    def subtotal(self):
        return self.quantity * self.variant.final_price
