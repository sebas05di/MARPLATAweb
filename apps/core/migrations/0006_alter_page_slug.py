from django.db import migrations, models
import django.utils.translation


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_page_footer_section_alter_page_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='slug',
            field=models.SlugField(
                choices=[
                    ('nosotros', django.utils.translation.gettext_lazy('Nosotros')),
                    ('contacto', django.utils.translation.gettext_lazy('Contacto')),
                    ('envios-devoluciones', django.utils.translation.gettext_lazy('Envíos y devoluciones')),
                    ('politica-privacidad', django.utils.translation.gettext_lazy('Política de privacidad')),
                    ('terminos-condiciones', django.utils.translation.gettext_lazy('Términos y condiciones')),
                    ('cuidados-prenda', django.utils.translation.gettext_lazy('Cuidados de la prenda')),
                    ('cambios-devoluciones', django.utils.translation.gettext_lazy('Cambios y devoluciones')),
                ],
                help_text='Identificador de la URL. Una vez creado, no se puede cambiar.',
                max_length=100, unique=True, verbose_name='slug',
            ),
        ),
    ]