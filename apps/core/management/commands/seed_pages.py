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
<p>Soy Ana María, fundadora de Mar Plata. Siempre soñé con crear una marca donde las mujeres encontraran mucho más que vestidos de baño: un universo de prendas y complementos que las acompañaran en cada momento.</p>
<p>Diseñamos piezas atemporales y versátiles, pensadas para adaptarse a diferentes siluetas y resaltar la esencia de cada mujer.</p>""",
    },
    {
        "slug": "contacto",
        "title": "Contacto",
        "subtitle": "Estamos para ayudarte.",
        "footer_section": "ayuda",
        "order": 1,
        "content": """<p>¿Tienes alguna duda sobre nuestros productos, tu pedido o quieres asesoramiento personalizado? No dudes en escribirnos.</p>
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
        "title": "Envíos",
        "subtitle": "Información sobre entregas, costos y tiempos de envío.",
        "footer_section": "envios",
        "order": 2,
        "content": """<h2>Envíos</h2>
<p>En Mar Plata realizamos envíos a todo Colombia a través de Coordinadora.</p>
<p>El costo del envío será asumido por el cliente y se calculará automáticamente al finalizar la compra, antes de realizar el pago.</p>
<p>Todos los pedidos son procesados en días hábiles (lunes a viernes) y despachados al siguiente día hábil una vez se confirme el pago. El tiempo estimado de entrega es de 2 a 5 días hábiles, dependiendo del destino. En temporadas de alta demanda, eventos promocionales o fechas especiales, los tiempos de entrega pueden extenderse.</p>
<p>Una vez el pedido sea entregado a la empresa transportadora, el cliente recibirá la información necesaria para realizar el seguimiento de su envío.</p>
<p>Mar Plata no se hace responsable por retrasos, pérdidas o daños ocasionados durante el transporte, ya que estos procesos dependen directamente de la empresa transportadora. En caso de presentarse alguna novedad, el cliente podrá contactarnos y lo acompañaremos en la gestión correspondiente con la transportadora.</p>
<p>No manejamos la modalidad de pago contra entrega. Todos los pedidos deben ser pagados en su totalidad antes de ser procesados y despachados.</p>
<p>Una vez el pedido haya sido confirmado y el pago validado, no será posible cancelarlo.</p>""",
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
<li>No lavar en lavadora ni secar en secadora.</li>
<li>No retorcer ni arrugar la prenda para escurrirla. Retirar el exceso de agua presionando suavemente con una toalla.</li>
<li>Secar a la sombra y evitar la exposición prolongada al sol.</li>
<li>Evitar el contacto con superficies ásperas que puedan ocasionar enganches o desgaste en la tela.</li>
<li>No planchar ni lavar en seco.</li>
<li>Guardar la prenda únicamente cuando esté completamente seca.</li>
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
        "subtitle": "Las reglas que rigen el uso de nuestro sitio y la compra de nuestros productos.",
        "footer_section": "legal",
        "order": 2,
        "content": """<h2>Términos y Condiciones</h2>
<p>Gracias por elegir Mar Plata. Al realizar una compra con nosotros, declaras haber leído, entendido y aceptado nuestros términos, condiciones y políticas de compra.</p>
<p>Mar Plata diseña y confecciona vestidos de baño, salidas de baño y accesorios de playa, creando piezas que combinan calidad, comodidad, diseño y estilo para resaltar la esencia de cada mujer.</p>
<h2>Pagos</h2>
<p>Todos los pedidos deben estar pagados en su totalidad antes de ser procesados. Actualmente no manejamos pagos contra entrega ni realizamos devoluciones de dinero.</p>
<h2>Procesamiento y Envíos</h2>
<p>Los pedidos realizados dentro de nuestro horario de atención podrán ser despachados el mismo día, sujeto a disponibilidad y confirmación del pago. Los pedidos realizados fuera de este horario serán procesados el siguiente día hábil.</p>
<p>El tiempo estimado de entrega es de 1 a 3 días hábiles en ciudades principales, dependiendo de la transportadora aliada y la ubicación de destino.</p>
<p>Una vez el pedido es entregado a la empresa transportadora, Mar Plata realizará seguimiento al estado del envío para acompañarte durante el proceso hasta la entrega. Sin embargo, factores externos propios de la operación logística, como retrasos, pérdidas o daños ocasionados durante el transporte, son responsabilidad de la empresa transportadora.</p>
<h2>Producto y Color</h2>
<p>En Mar Plata hacemos todo lo posible por mostrar con precisión los colores, estampados y detalles de cada prenda. Sin embargo, pueden presentarse ligeras variaciones debido a la iluminación de las fotografías o a la configuración de la pantalla desde la cual se visualice el producto.</p>
<h2>Cambios y Devoluciones</h2>
<p>Por razones de higiene, nuestros vestidos de baño no tienen cambios ni devoluciones por talla, gusto personal o preferencias estéticas.</p>
<p>Por esta razón, recomendamos revisar cuidadosamente la guía de tallas antes de realizar tu compra.</p>
<p>Únicamente se aceptarán cambios en los siguientes casos:</p>
<ul>
<li>Defectos de fabricación</li>
<li>Imperfecciones de confección</li>
<li>Error en el producto enviado</li>
</ul>
<p>Si tu producto presenta alguna novedad, deberás reportarla dentro de las primeras 24 horas después de recibirlo, enviando evidencia fotográfica o en video.</p>
<p>Una vez validado el caso por nuestro equipo, Mar Plata podrá realizar el cambio o reemplazo de la prenda sin costo adicional.</p>
<h2>Modificaciones</h2>
<p>Mar Plata se reserva el derecho de modificar precios, referencias, disponibilidad, términos y condiciones en cualquier momento, sin previo aviso.</p>""",
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
