import uuid

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Custom user model manager where email is the unique identifier."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('El correo electrónico es obligatorio'))
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """Custom User model with email as the unique identifier."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(_('correo electrónico'), unique=True)
    phone = models.CharField(_('teléfono'), max_length=30, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('usuario')
        verbose_name_plural = _('usuarios')

    def __str__(self):
        return self.email


class NewsletterSubscriber(models.Model):
    """Email list for marketing communications."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('correo electrónico'), unique=True)
    first_name = models.CharField(_('nombre'), max_length=100, blank=True)
    is_active = models.BooleanField(_('activo'), default=True)
    user = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='newsletter_subscriptions',
        verbose_name=_('usuario'),
    )
    subscribed_at = models.DateTimeField(_('suscrito en'), auto_now_add=True)
    unsubscribed_at = models.DateTimeField(_('desuscrito en'), null=True, blank=True)
    source = models.CharField(
        _('origen'),
        max_length=50,
        blank=True,
        help_text=_('Cómo se suscribió (footer, registro, etc.)'),
    )

    class Meta:
        verbose_name = _('suscriptor al newsletter')
        verbose_name_plural = _('suscriptores al newsletter')
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email

    def unsubscribe(self):
        self.is_active = False
        self.unsubscribed_at = timezone.now()
        self.save(update_fields=['is_active', 'unsubscribed_at'])


class WishlistItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='wishlist_items',
        verbose_name=_('usuario'),
    )
    product = models.ForeignKey(
        'catalog.Product',
        on_delete=models.CASCADE,
        related_name='wishlisted_by',
        verbose_name=_('producto'),
    )
    added_at = models.DateTimeField(_('añadido en'), auto_now_add=True)

    class Meta:
        verbose_name = _('ítem de favoritos')
        verbose_name_plural = _('ítems de favoritos')
        unique_together = [['user', 'product']]
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user.email} → {self.product.name}"
