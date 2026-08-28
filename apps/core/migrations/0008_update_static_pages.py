# Manual data migration to update static page contents.

from django.db import migrations


def update_static_pages(apps, schema_editor):
    Page = apps.get_model('core', 'Page')

    updates = {
        'cuidados-prenda': {
            'subtitle': 'Conoce las recomendaciones para el cuidado y uso adecuado de tus prendas.',
        },
        'contacto': {
            'content': """<p>¿Tienes alguna duda sobre nuestros productos, tu pedido o quieres asesoramiento personalizado? No dudes en escribirnos.</p>
<p>Atención personalizada por WhatsApp, donde podemos ayudarte con:</p>
<p>Consultas sobre tallas y colores</p>
<p>Estado de tu pedido</p>
<p>Asesoramiento personalizado para encontrar tu vestido de baño, ropa de playa y accesorios ideales.</p>
<p>Cambios y devoluciones</p>
<h3>Horarios de atención</h3>
<p>Brindamos asesoría personalizada y atención para compras a través de WhatsApp de <strong>lunes a sábado, de 8:00 a.m. a 6:00 p.m.</strong> Si nos escribes fuera de este horario, responderemos tu mensaje en el siguiente día hábil.</p>""",
        },
        'cambios-devoluciones': {
            'content': """<h2>Cambios y devoluciones</h2>
<p>Por razones de higiene, no aceptamos cambios por gusto personal, preferencias estéticas, color, diseño o referencia. Si la talla que elegiste no es la adecuada, puedes solicitar un cambio únicamente por la misma referencia y el mismo color, sujeto a disponibilidad de inventario. Para realizarlo, la prenda debe estar sin uso, en perfectas condiciones y conservar su etiqueta. Los costos de envío asociados al cambio de talla serán asumidos por el cliente. Asimismo, aceptamos cambios en caso de defectos de fabricación, imperfecciones de confección o errores en el producto enviado, siempre que sean informados dentro de las primeras 24 horas posteriores a la entrega.</p>""",
        },
    }

    for slug, fields in updates.items():
        Page.objects.filter(slug=slug).update(**fields)


def revert_static_pages(apps, schema_editor):
    Page = apps.get_model('core', 'Page')

    reverts = {
        'cuidados-prenda': {
            'subtitle': 'Cuidá tus piezas para que te acompañen más tiempo.',
        },
        'contacto': {
            'content': """<p>¿Tienes alguna duda sobre nuestros productos, tu pedido o quieres asesoramiento personalizado? No dudes en escribirnos.</p>
<p>Atención personalizada por WhatsApp, donde podemos ayudarte con:</p>
<p>Consultas sobre talles y colores</p>
<p>Estado de tu pedido</p>
<p>Asesoramiento personalizado para encontrar tu vestido de baño, ropa de playa y accesorios ideales.</p>
<p>Cambios y devoluciones</p>
<h3>Horarios de atención</h3>
<p>Brindamos asesoría personalizada y atención para compras a través de WhatsApp de <strong>lunes a viernes, de 8:00 a.m. a 6:00 p.m.</strong> Si nos escribes fuera de este horario, responderemos tu mensaje en el siguiente día hábil.</p>""",
        },
        'cambios-devoluciones': {
            'content': """<h2>Cambios y devoluciones</h2>
<p>Por razones de higiene, no aceptamos cambios por gusto personal, preferencias estéticas, color, referencia o cualquier motivo diferente al cambio de talla. Si necesitas cambiar la talla de tu prenda, el cambio solo podrá realizarse por la misma referencia y el mismo color, sujeto a disponibilidad de inventario. En caso de no contar con existencia de la misma referencia y el mismo color en la talla solicitada, no será posible realizar el cambio. Para ello, la prenda deberá encontrarse sin uso, en perfectas condiciones y conservar su etiqueta. Asimismo, solo se aceptarán cambios por defectos de fabricación, imperfecciones de confección o errores en el producto enviado, siempre que sean informados dentro de las primeras 24 horas posteriores a la entrega.</p>""",
        },
    }

    for slug, fields in reverts.items():
        Page.objects.filter(slug=slug).update(**fields)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_page_slug'),
    ]

    operations = [
        migrations.RunPython(update_static_pages, revert_static_pages),
    ]
