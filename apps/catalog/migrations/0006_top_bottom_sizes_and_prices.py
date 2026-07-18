# Generated manually for MARPLATA

from django.db import migrations, models


def fill_bottom_size(apps, schema_editor):
    ProductVariant = apps.get_model('catalog', 'ProductVariant')
    for variant in ProductVariant.objects.order_by('pk'):
        variant.bottom_size = variant.top_size
        variant.save(update_fields=['bottom_size'])


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_alter_productvariant_size'),
    ]

    operations = [
        # Product prices
        migrations.AddField(
            model_name='product',
            name='top_price',
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10,
                null=True, verbose_name='precio top',
                help_text='Precio de la parte superior del vestido de baño.',
            ),
        ),
        migrations.AddField(
            model_name='product',
            name='bottom_price',
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10,
                null=True, verbose_name='precio tanga',
                help_text='Precio de la parte inferior del vestido de baño.',
            ),
        ),
        migrations.AlterField(
            model_name='product',
            name='base_price',
            field=models.DecimalField(
                decimal_places=2, max_digits=10,
                help_text='Precio de venta. Si completás precio top y tanga, se calcula automáticamente.',
                verbose_name='precio total',
            ),
        ),
        # Variant sizes
        migrations.RenameField(
            model_name='productvariant',
            old_name='size',
            new_name='top_size',
        ),
        migrations.AddField(
            model_name='productvariant',
            name='bottom_size',
            field=models.CharField(
                choices=[('S', 'S'), ('M', 'M'), ('L', 'L')],
                default='S', max_length=4, verbose_name='talla tanga',
            ),
            preserve_default=False,
        ),
        migrations.AlterModelOptions(
            name='productvariant',
            options={
                'ordering': ['product', 'color', 'top_size', 'bottom_size'],
                'verbose_name': 'variante de producto',
                'verbose_name_plural': 'variantes de producto',
            },
        ),
        migrations.RunPython(fill_bottom_size, noop),
        migrations.AlterUniqueTogether(
            name='productvariant',
            unique_together={('product', 'color_slug', 'top_size', 'bottom_size')},
        ),
    ]
