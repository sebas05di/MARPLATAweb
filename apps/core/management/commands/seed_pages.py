from django.core.management.base import BaseCommand
from apps.core.models import Page


PAGES_DATA = [
    {
        "slug": "nosotros",
        "title": "Nuestra historia",
        "subtitle": "Inspiradas en el mar, creadas para vos.",
        "footer_section": "navegacion",
        "order": 1,
        "content": """<h2>Diseña tu estilo, resalta tu esencia</h2>
<p>Cada vestido de baño MARPLATA nace de la pasión por el diseño y la conexión con el mar. Creamos piezas que celebran la individualidad y la confianza de quien las lleva.</p>
<p>Inspirados en las costas de Mar del Plata, fusionamos siluetas atemporales con materiales de alta calidad para acompañarte en cada verano.</p>
<h3>Nuestra filosofía</h3>
<p>Creemos en la moda consciente: prendas duraderas, materiales seleccionados y procesos de producción respetuosos con el entorno y las personas que los hacen posible.</p>
<h3>Hecho con amor</h3>
<p>Cada pieza cuenta una historia. Desde el primer boceto hasta el envío a tu hogar, ponemos dedicación en cada detalle para que te sientas única.</p>""",
    },
    {
        "slug": "contacto",
        "title": "Contacto",
        "subtitle": "Estamos para ayudarte. Escribinos por el canal que prefieras.",
        "footer_section": "ayuda",
        "order": 1,
        "content": """<p>¿Tenés alguna pregunta sobre nuestros productos, tu pedido o querés asesoramiento personalizado? No dudes en escribirnos.</p>
<p>Atención personalizada por WhatsApp, donde podemos ayudarte con:</p>
<ul>
<li>Consultas sobre talles y colores</li>
<li>Estado de tu pedido</li>
<li>Asesoramiento para encontrar tu vestido ideal</li>
<li>Cambios y devoluciones</li>
</ul>
<h3>Horarios de atención</h3>
<p>Respondemos todos los mensajes en horario comercial. Si nos escribís fuera de horario, te contestaremos al siguiente día hábil.</p>""",
    },
    {
        "slug": "envios-devoluciones",
        "title": "Envíos y devoluciones",
        "subtitle": "Información sobre entregas, costos y política de cambios.",
        "footer_section": "ayuda",
        "order": 2,
        "content": """<h2>Envíos</h2>
<p>Realizamos envíos a toda Colombia. Una vez confirmado tu pedido por WhatsApp, te enviaremos el producto en un plazo de 3 a 5 días hábiles a ciudades principales, y de 5 a 8 días hábiles a otras zonas.</p>
<h3>Costos de envío</h3>
<p>El costo de envío depende de la ciudad de destino. Te lo confirmaremos por WhatsApp junto con el resto de los detalles de tu pedido antes de finalizar la compra.</p>
<h3>Tracking</h3>
<p>Te enviaremos el número de guía para que puedas rastrear tu pedido una vez despachado.</p>
<h2>Devoluciones y cambios</h2>
<p>Aceptamos cambios dentro de los 15 días posteriores a la recepción, siempre que la prenda esté en perfecto estado, con etiquetas y sin uso.</p>
<p>Para iniciar un cambio, escribinos por WhatsApp con tu número de orden.</p>""",
    },
    {
        "slug": "politica-privacidad",
        "title": "Política de privacidad",
        "subtitle": "Cómo cuidamos tus datos personales.",
        "footer_section": "legal",
        "order": 1,
        "content": """<h2>Información que recopilamos</h2>
<p>Recopilamos la información que nos proporcionas al registrarte, realizar un pedido o contactarnos: nombre, correo electrónico, teléfono y dirección de envío cuando corresponda.</p>
<h2>Uso de la información</h2>
<p>Usamos tus datos personales para:</p>
<ul>
<li>Procesar y enviar tus pedidos</li>
<li>Responder a tus consultas</li>
<li>Enviarte comunicaciones sobre tu cuenta o pedidos</li>
<li>Mejorar nuestros servicios</li>
</ul>
<h2>Protección de datos</h2>
<p>Implementamos medidas de seguridad técnicas y organizativas para proteger tu información personal contra acceso no autorizado, pérdida o alteración.</p>
<h2>Tus derechos</h2>
<p>Podés solicitar el acceso, rectificación o eliminación de tus datos personales en cualquier momento escribiéndonos a nuestro correo de contacto.</p>""",
    },
    {
        "slug": "terminos-condiciones",
        "title": "Términos y condiciones",
        "subtitle": "Las reglas que rigen el uso de nuestro sitio y la compra de nuestros productos.",
        "footer_section": "legal",
        "order": 2,
        "content": """<h2>Aceptación de los términos</h2>
<p>Al utilizar este sitio y realizar pedidos, aceptas los presentes términos y condiciones. Si no estás de acuerdo con alguno de ellos, te pedimos que no utilices el sitio.</p>
<h2>Proceso de compra</h2>
<p>Nuestras ventas se realizan a través de WhatsApp. Al confirmar tu pedido, te enviaremos los datos de pago y una vez confirmado el pago, procederemos al envío.</p>
<h2>Precios</h2>
<p>Todos los precios están expresados en pesos colombianos e incluyen IVA. Los gastos de envío se confirman por WhatsApp antes de finalizar la compra.</p>
<h2>Disponibilidad</h2>
<p>Nos reservamos el derecho de modificar precios, descripciones y disponibilidad de los productos sin previo aviso.</p>""",
    },
]


class Command(BaseCommand):
    help = "Seed default static pages (idempotent)"

    def handle(self, *args, **options):
        for data in PAGES_DATA:
            page, created = Page.objects.update_or_create(
                slug=data["slug"],
                defaults={k: v for k, v in data.items() if k != "slug"},
            )
            action = "Created" if created else "Updated"
            self.stdout.write(self.style.SUCCESS(f"{action}: {page.slug}"))
        self.stdout.write(self.style.SUCCESS("Done"))
