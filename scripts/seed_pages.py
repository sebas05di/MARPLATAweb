import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

import django
django.setup()
from apps.core.models import Page

pages_data = [
    {
        'slug': 'nosotros',
        'title': 'Nuestra historia',
        'subtitle': 'Inspiradas en el mar, creadas para vos.',
        'footer_section': 'navegacion',
        'order': 1,
        'content': """<h2>Diseña tu estilo, resalta tu esencia</h2>
<p>Cada vestido de banio MARPLATA nace de la pasion por el diseno y la conexion con el mar. Creamos piezas que celebran la individualidad y la confianza de quien las lleva.</p>
<p>Inspirados en las costas de Mar del Plata, fusionamos siluetas atemporales con materiales de alta calidad para acompanarte en cada verano.</p>
<h3>Nuestra filosofia</h3>
<p>Creemos en la moda consciente: prendas duraderas, materiales seleccionados y procesos de produccion respetuosos con el entorno y las personas que los hacen posible.</p>
<h3>Hecho con amor</h3>
<p>Cada pieza cuenta una historia. Desde el primer boceto hasta el envio a tu hogar, ponemos dedicacion en cada detalle para que te sientas unica.</p>""",
    },
    {
        'slug': 'contacto',
        'title': 'Contacto',
        'subtitle': 'Estamos para ayudarte. Escribinos por el canal que prefieras.',
        'footer_section': 'ayuda',
        'order': 1,
        'content': """<p>Tenes alguna pregunta sobre nuestros productos, tu pedido o queres asesoramiento personalizado? No dudes en escribirnos.</p>
<p>Atencion personalizada por WhatsApp, donde podemos ayudarte con:</p>
<ul>
<li>Consultas sobre talles y colores</li>
<li>Estado de tu pedido</li>
<li>Asesoramiento para encontrar tu vestido ideal</li>
<li>Cambios y devoluciones</li>
</ul>
<h3>Horarios de atencion</h3>
<p>Respondemos todos los mensajes en horario comercial. Si nos escribis fuera de horario, te contestaremos al siguiente dia habil.</p>""",
    },
    {
        'slug': 'envios-devoluciones',
        'title': 'Envios y devoluciones',
        'subtitle': 'Informacion sobre entregas, costos y politica de cambios.',
        'footer_section': 'ayuda',
        'order': 2,
        'content': """<h2>Envios</h2>
<p>Realizamos envios a toda Colombia. Una vez confirmado tu pedido por WhatsApp, te enviaremos el producto en un plazo de 3 a 5 dias habiles a ciudades principales, y de 5 a 8 dias habiles a otras zonas.</p>
<h3>Costos de envio</h3>
<p>El costo de envio depende de la ciudad de destino. Te lo confirmaremos por WhatsApp junto con el resto de los detalles de tu pedido antes de finalizar la compra.</p>
<h3>Tracking</h3>
<p>Te enviaremos el numero de guia para que puedas rastrear tu pedido una vez despachado.</p>
<h2>Devoluciones y cambios</h2>
<p>Aceptamos cambios dentro de los 15 dias posteriores a la recepcion, siempre que la prenda este en perfecto estado, con etiquetas y sin uso.</p>
<p>Para iniciar un cambio, escribinos por WhatsApp con tu numero de orden.</p>""",
    },
    {
        'slug': 'politica-privacidad',
        'title': 'Politica de privacidad',
        'subtitle': 'Como cuidamos tus datos personales.',
        'footer_section': 'legal',
        'order': 1,
        'content': """<h2>Informacion que recopilamos</h2>
<p>Recopilamos la informacion que nos proporcionas al registrarte, realizar un pedido o contactarnos: nombre, correo electronico, telefono y direccion de envio cuando corresponda.</p>
<h2>Uso de la informacion</h2>
<p>Usamos tus datos personales para:</p>
<ul>
<li>Procesar y enviar tus pedidos</li>
<li>Responder a tus consultas</li>
<li>Enviarte comunicaciones sobre tu cuenta o pedidos</li>
<li>Mejorar nuestros servicios</li>
</ul>
<h2>Proteccion de datos</h2>
<p>Implementamos medidas de seguridad tecnicas y organizativas para proteger tu informacion personal contra acceso no autorizado, perdida o alteracion.</p>
<h2>Tus derechos</h2>
<p>Podes solicitar el acceso, rectificacion o eliminacion de tus datos personales en cualquier momento escribiendonos a nuestro correo de contacto.</p>""",
    },
    {
        'slug': 'terminos-condiciones',
        'title': 'Terminos y condiciones',
        'subtitle': 'Las reglas que rigen el uso de nuestro sitio y la compra de nuestros productos.',
        'footer_section': 'legal',
        'order': 2,
        'content': """<h2>Aceptacion de los terminos</h2>
<p>Al utilizar este sitio y realizar pedidos, aceptas los presentes terminos y condiciones. Si no estas de acuerdo con alguno de ellos, te pedimos que no utilices el sitio.</p>
<h2>Proceso de compra</h2>
<p>Nuestras ventas se realizan a traves de WhatsApp. Al confirmar tu pedido, te enviaremos los datos de pago y una vez confirmado el pago, procederemos al envio.</p>
<h2>Precios</h2>
<p>Todos los precios estan expresados en pesos colombianos e incluyen IVA. Los gastos de envio se confirman por WhatsApp antes de finalizar la compra.</p>
<h2>Disponibilidad</h2>
<p>Nos reservamos el derecho de modificar precios, descripciones y disponibilidad de los productos sin previo aviso.</p>""",
    },
]

for data in pages_data:
    page, created = Page.objects.update_or_create(
        slug=data['slug'],
        defaults={k: v for k, v in data.items() if k != 'slug'},
    )
    print(f"{'Created' if created else 'Updated'}: {page.slug}")

print("Done")
