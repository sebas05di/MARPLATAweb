import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import CustomUser


class SiteConfig(models.Model):
    """Singleton model for site-wide configuration."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    site_name = models.CharField(
        _('nombre del sitio'), max_length=100, default='MARPLATA'
    )
    site_tagline = models.CharField(
        _('eslogan'), max_length=200,
        default='Diseña tu estilo, resalta tu esencia',
    )
    contact_email = models.EmailField(_('correo de contacto'), blank=True)
    contact_phone = models.CharField(
        _('teléfono de contacto'), max_length=30, blank=True,
    )
    address = models.TextField(_('dirección física'), blank=True)
    business_hours = models.CharField(
        _('horario de atención'), max_length=200, blank=True,
        help_text='Ej: Lun-Vie 9am-6pm, Sáb 9am-1pm',
    )
    whatsapp_number = models.CharField(
        _('número de WhatsApp'), max_length=30,
        help_text=_('Incluir código de país, ej: +573001234567'),
    )
    instagram_url = models.URLField(_('Instagram'), blank=True)
    facebook_url = models.URLField(_('Facebook'), blank=True)
    tiktok_url = models.URLField(_('TikTok'), blank=True)
    pinterest_url = models.URLField(_('Pinterest'), blank=True)
    whatsapp_message_template = models.TextField(
        _('plantilla de mensaje WhatsApp'),
        default=(
            "Hola MARPLATA! Me interesa realizar un pedido. "
            "Mis datos son:\nNombre: {customer_name}\n"
            "Correo: {customer_email}\nTeléfono: {customer_phone}\n"
            "Productos:\n{products}"
        ),
    )
    shipping_cost = models.DecimalField(
        _('costo de envío'), max_digits=10, decimal_places=2, null=True, blank=True
    )
    free_shipping_threshold = models.DecimalField(
        _('umbral de envío gratis'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    updated_at = models.DateTimeField(_('actualizado en'), auto_now=True)

    class Meta:
        verbose_name = _('configuración del sitio')
        verbose_name_plural = _('configuración del sitio')

    def __str__(self):
        return 'Configuración del sitio'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        default_whatsapp = getattr(
            settings, 'MARPLATA_WHATSAPP_NUMBER', '+573001234567'
        )
        obj, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                'whatsapp_number': default_whatsapp,
                'site_name': getattr(settings, 'SITE_NAME', 'MARPLATA'),
            },
        )
        return obj


class DataConsentLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='consent_logs',
        verbose_name=_('usuario'),
    )
    email = models.EmailField(_('correo'), blank=True)
    ip_address = models.GenericIPAddressField(
        _('dirección IP'), blank=True, null=True
    )
    consented_at = models.DateTimeField(_('fecha de consentimiento'), auto_now_add=True)
    consent_version = models.CharField(_('versión de política'), max_length=20)

    class Meta:
        verbose_name = _('registro de consentimiento')
        verbose_name_plural = _('registros de consentimiento')
        ordering = ['-consented_at']

    def __str__(self):
        return f"Consentimiento {self.consent_version} — {self.email or self.user}"


class Page(models.Model):
    """Static page editable from the admin (about, contact, terms, etc)."""

    SLUG_CHOICES = [
        ('nosotros', _('Nosotros')),
        ('contacto', _('Contacto')),
        ('envios-devoluciones', _('Envíos y devoluciones')),
        ('politica-privacidad', _('Política de privacidad')),
        ('terminos-condiciones', _('Términos y condiciones')),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(
        _('slug'), max_length=100, unique=True, choices=SLUG_CHOICES,
        help_text=_('Identificador de la URL. Una vez creado, no se puede cambiar.'),
    )
    title = models.CharField(_('título'), max_length=200)
    subtitle = models.CharField(_('subtítulo'), max_length=300, blank=True)
    content = models.TextField(
        _('contenido'),
        help_text=_('Contenido de la página. Soporta HTML básico.'),
    )
    is_active = models.BooleanField(_('activa'), default=True)
    show_in_footer = models.BooleanField(
        _('mostrar en footer'),
        default=True,
        help_text=_('Si está activo, se muestra automáticamente en el footer.'),
    )
    footer_section = models.CharField(
        _('sección del footer'),
        max_length=50,
        blank=True,
        choices=[
            ('', _('Sin sección específica')),
            ('navegacion', _('Navegación')),
            ('legal', _('Legal')),
            ('ayuda', _('Ayuda')),
        ],
        default='legal',
    )
    order = models.PositiveIntegerField(_('orden'), default=0)
    meta_title = models.CharField(_('meta título'), max_length=200, blank=True)
    meta_description = models.CharField(
        _('meta descripción'), max_length=300, blank=True,
    )
    created_at = models.DateTimeField(_('creado en'), auto_now_add=True)
    updated_at = models.DateTimeField(_('actualizado en'), auto_now=True)

    class Meta:
        verbose_name = _('página')
        verbose_name_plural = _('páginas')
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.meta_title:
            self.meta_title = self.title
        super().save(*args, **kwargs)
