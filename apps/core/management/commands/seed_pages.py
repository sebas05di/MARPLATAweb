from django.core.management.base import BaseCommand
from apps.core.models import Page


PAGES_DATA = [
    {
        "slug": "ropa-de-playa",
        "title": "Ropa de playa",
        "subtitle": "Próximamente.",
        "footer_section": "",
        "show_in_footer": False,
        "order": 0,
        "content": """<p>Estamos preparando una selección especial de ropa de playa para acompañarte antes, durante y después del mar.</p>
<p>Volvé pronto para descubrir las nuevas piezas.</p>""",
    },
    {
        "slug": "nosotros",
        "title": "Nuestra historia",
        "subtitle": "",
        "footer_section": "historia",
        "order": 1,
        "content": """<h2>Nuestra historia</h2>
<p>Soy Ana María la fundadora de Mar Plata y todo nace con el propósito de crear un universo de prendas y complementos donde cada mujer encuentre piezas que le permitan resaltar su esencia con autenticidad.</p>
<p>Diseñamos colecciones cápsula de edición limitada, con prendas atemporales y versátiles que pueden combinarse entre sí. Cada diseño cobra vida gracias al trabajo de mujeres apasionadas por su oficio.</p>
<p>Seleccionamos telas de alta calidad provenientes de procesos de fabricación más responsables con el medio ambiente, porque creemos que el diseño también puede ser consciente.</p>""",
    },
    {
        "slug": "contacto",
        "title": "Contacto",
        "subtitle": "Estamos para ayudarte.",
        "footer_section": "ayuda",
        "order": 1,
        "content": """<p>¿Tienes alguna duda sobre nuestros productos, tu pedido o quieres asesoramiento personalizado? No dudes en escribirnos.</p>
<p>Atención personalizada por WhatsApp, donde podemos ayudarte con:</p>
<p>Consultas sobre talles y colores</p>
<p>Estado de tu pedido</p>
<p>Asesoramiento personalizado para encontrar tu vestido de baño, ropa de playa y accesorios ideales.</p>
<p>Cambios y devoluciones</p>
<h3>Horarios de atención</h3>
<p>Brindamos asesoría personalizada y atención para compras a través de WhatsApp de <strong>lunes a viernes, de 8:00 a.m. a 6:00 p.m.</strong> Si nos escribes fuera de este horario, responderemos tu mensaje en el siguiente día hábil.</p>""",
    },
    {
        "slug": "envios-devoluciones",
        "title": "Envíos",
        "subtitle": "Información sobre entregas, costos y tiempos de envío.",
        "footer_section": "envios",
        "order": 2,
        "content": """<h2>Envíos</h2>
<p>En Mar Plata realizamos envíos a todo Colombia a través de transportadoras aliadas.</p>
<p>El costo del envío será asumido por el cliente y se calculará automáticamente al finalizar la compra, antes de realizar el pago.</p>
<p>Todos los pedidos son procesados en días hábiles (lunes a viernes) y despachados al siguiente día hábil una vez se confirme el pago. El tiempo estimado de entrega es de 2 a 5 días hábiles, dependiendo del destino. En temporadas de alta demanda, eventos promocionales o fechas especiales, los tiempos de entrega pueden extenderse.</p>
<p>Una vez el pedido sea entregado a la empresa transportadora, el cliente recibirá la información necesaria para realizar el seguimiento de su envío.</p>
<p>Mar Plata no se hace responsable por retrasos, pérdidas o daños ocasionados durante el transporte, ya que estos procesos dependen directamente de la empresa transportadora. En caso de presentarse alguna novedad, el cliente podrá contactarnos y lo acompañaremos en la gestión correspondiente con la transportadora.</p>
<p>No manejamos la modalidad de pago contra entrega. Todos los pedidos deben ser pagados en su totalidad antes de ser procesados y despachados.</p>
<p>Una vez el pedido haya sido confirmado y el pago validado, no será posible cancelarlo.</p>""",
    },
    {
        "slug": "cambios-devoluciones",
        "title": "Cambios y devoluciones",
        "subtitle": "Política de cambios y devoluciones.",
        "footer_section": "ayuda",
        "order": 2,
        "content": """<h2>Cambios y devoluciones</h2>
<p>Por razones de higiene, no aceptamos cambios por gusto personal, preferencias estéticas, color, referencia o cualquier motivo diferente al cambio de talla. Si necesitas cambiar la talla de tu prenda, el cambio solo podrá realizarse por la misma referencia y el mismo color, sujeto a disponibilidad de inventario. En caso de no contar con existencia de la misma referencia y el mismo color en la talla solicitada, no será posible realizar el cambio. Para ello, la prenda deberá encontrarse sin uso, en perfectas condiciones y conservar su etiqueta. Asimismo, solo se aceptarán cambios por defectos de fabricación, imperfecciones de confección o errores en el producto enviado, siempre que sean informados dentro de las primeras 24 horas posteriores a la entrega.</p>""",
    },
    {
        "slug": "cuidados-prenda",
        "title": "Cuidados de la prenda",
        "subtitle": "Cuidá tus piezas para que te acompañen más tiempo.",
        "footer_section": "cuidados",
        "order": 1,
        "content": """<h2>Cuidados de la prenda</h2>
<ul>
<li>Lavar a mano únicamente con agua fría.</li>
<li>Enjuagar inmediatamente después de cada uso para eliminar residuos de sal, cloro, arena y protector solar.</li>
<li>No utilizar jabón, detergentes, blanqueadores ni suavizantes.</li>
<li>No utilizar lavadora ni secadora.</li>
<li>No retorcer ni arrugar la prenda para escurrirla. Retirar el exceso de agua presionando suavemente con una toalla.</li>
<li>Secar a la sombra y evitar la exposición prolongada al sol.</li>
<li>Evitar el contacto con superficies ásperas que puedan ocasionar enganches o desgaste en la tela.</li>
<li>No planchar ni lavar en seco.</li>
<li>Guardar la prenda únicamente cuando esté completamente seca. Utiliza la bolsa de empaque para protegerla del polvo y el roce con otras prendas, ayudando a conservar su calidad y prolongar su vida útil.</li>
</ul>""",
    },
    {
        "slug": "politica-privacidad",
        "title": "Política de privacidad",
        "subtitle": "Cómo cuidamos tus datos personales.",
        "footer_section": "legal",
        "order": 1,
        "content": """<h2>Política de Privacidad</h2>
<p>En Mar Plata valoramos la confianza de nuestros clientes y entendemos la importancia de proteger su información personal. Los datos que nos proporcionas a través de nuestro sitio web, como tu nombre, número de teléfono, correo electrónico, dirección de envío y demás información necesaria para procesar tu compra, serán utilizados exclusivamente para gestionar tus pedidos, realizar los envíos, brindar atención al cliente y mantenerte informado sobre el estado de tu compra. Si así lo autorizas, también podremos enviarte información sobre nuevos lanzamientos, promociones y novedades de la marca.</p>
<p>Mar Plata adopta medidas razonables para proteger la información suministrada por sus clientes y evitar el acceso, el uso o la divulgación no autorizada de sus datos personales. Asimismo, nos comprometemos a no vender ni compartir tu información con terceros con fines comerciales. Tus datos únicamente podrán ser compartidos con proveedores indispensables para la prestación del servicio, como la empresa transportadora Coordinadora y la pasarela de pagos, con el único propósito de procesar tu compra y realizar la entrega de tu pedido de manera segura.</p>
<p>Como titular de tus datos personales, podrás solicitar en cualquier momento la actualización, corrección o eliminación de tu información, así como realizar consultas relacionadas con el tratamiento de tus datos a través de nuestros canales oficiales de atención.</p>
<p>Mar Plata podrá actualizar esta Política de Privacidad cuando sea necesario para mejorar sus procesos o dar cumplimiento a la normativa aplicable. Cualquier modificación será publicada en este sitio web y entrará en vigor a partir de su fecha de publicación.</p>""",
    },
    {
        "slug": "terminos-condiciones",
        "title": "Términos y condiciones",
        "subtitle": "Conoce nuestras políticas de compra, envíos, cambios y garantías.",
        "footer_section": "legal",
        "order": 2,
        "content": """<p>Gracias por elegir Mar Plata.</p>
<p>Al realizar una compra con nosotros, aceptas los presentes términos y condiciones, así como nuestras políticas de compra.</p>
<p>Mar Plata diseña y confecciona vestidos de baño, ropa de playa y accesorios, con piezas atemporales que unen diseño, calidad y versatilidad para resaltar la esencia de cada mujer.</p>
<hr>
<h2>Pagos</h2>
<p>Todos los pedidos deben estar pagados en su totalidad antes de ser procesados. No manejamos pagos contra entrega.</p>""",
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
