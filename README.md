# MARPLATA — E-commerce de vestidos de baño

Sitio web de e-commerce para **MARPLATA**, marca de vestidos de baño premium.
Construido con Django + PostgreSQL + Tailwind CSS v4. Cierre de venta por WhatsApp.

**Stack:** Django 4.2 · PostgreSQL 17 · Tailwind v4 · Garet + Jost · WhiteNoise · Jazzmin Admin

---

## Setup rápido

```bash
# 1. Setup automático (crea venv, instala deps, configura DB, compila CSS)
python scripts/setup.py

# 2. Activar venv
.\venv\Scripts\Activate.ps1   # Windows
source venv/bin/activate      # Mac/Linux

# 3. Crear superuser
python manage.py createsuperuser

# 4. Correr server
python manage.py runserver
```

Abrí:
- `http://localhost:8000/` — sitio público
- `http://localhost:8000/admin/` — admin
- `http://localhost:8000/admin/dashboard/` — dashboard de ventas

---

## Estructura del proyecto

```
MARPLATA/
├── apps/                          # Django apps
│   ├── accounts/                  # Usuarios, login, registro, wishlist, newsletter
│   ├── catalog/                   # Productos, categorías, variantes, búsqueda
│   ├── cart/                      # Carrito de compras (sesión)
│   ├── orders/                    # Pedidos WhatsApp + dashboard de ventas
│   ├── core/                      # Site config, páginas estáticas, emails
│   └── emails/                    # (legacy, ahora en core)
├── config/                        # Configuración Django
│   ├── settings/
│   │   ├── base.py                # Settings compartidos
│   │   ├── dev.py                 # Settings de desarrollo
│   │   └── prod.py                # Settings de producción
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── templates/                     # Templates Django
│   ├── base.html                  # Layout principal
│   ├── accounts/                  # Login, registro, perfil, wishlist
│   ├── catalog/                   # Producto, catálogo, búsqueda
│   ├── cart/                      # Carrito
│   ├── orders/                    # Checkout, tracking
│   ├── emails/                    # Templates HTML de emails
│   └── pages/                     # Home + páginas estáticas
├── static/                        # Archivos estáticos
│   ├── css/
│   │   ├── tailwind.css           # CSS fuente (Tailwind v4)
│   │   └── marplata.css           # CSS compilado
│   ├── js/                        # JavaScript
│   ├── img/
│   │   ├── hero/                  # Imágenes del hero
│   │   ├── products/              # Fotos de productos
│   │   ├── logos/                 # Logos extraídos del PDF
│   │   ├── branding/              # Logos optimizados + og:image
│   │   └── favicons/              # favicon.ico + apple-touch-icon
├── media/                         # Archivos subidos por usuarios/admin
│   └── products/                  # Covers y variants de productos
├── scripts/                       # Scripts de utilidad
│   ├── setup.py                   # Setup inicial
│   ├── seed_products.py           # Carga productos de prueba
│   ├── seed_pages.py              # Carga páginas estáticas
│   ├── generate_assets.py         # Genera logos + favicons desde PDF
│   ├── validate_product_images.py # Valida dimensiones de fotos
│   ├── optimize_product_images.py # Optimiza fotos (resize + WebP)
│   ├── test_email.py              # Prueba envío de emails
│   ├── test_e2e.py                # Testing E2E del flujo
│   └── smoke_test.py              # Verificación rápida pre-deploy
├── staticfiles/                   # Archivos estáticos para producción (collectstatic)
├── DEPLOYMENT.md                  # Guía de deploy a producción
├── requirements.txt               # Dependencias Python
├── package.json                   # Dependencias Node
├── .env                           # Variables de entorno (NO commitear)
├── .env.prod                      # Variables para producción (NO commitear)
├── .env.example                   # Plantilla de .env (sí commitear)
├── manage.py
└── README.md                      # Este archivo
```

---

## URLs principales

| URL | Descripción |
|-----|-------------|
| `/` | Home |
| `/coleccion/` | Catálogo completo |
| `/coleccion/<slug>/` | Filtrar por colección (ej: `/coleccion/esencia/`) |
| `/coleccion/buscar/?q=aura` | Búsqueda de productos |
| `/producto/<slug>/` | Detalle de producto |
| `/carrito/` | Carrito de compras |
| `/pedido/checkout/` | Formulario de checkout |
| `/pedido/orden/<n>/` | Tracking de pedido |
| `/pedido/rastrear/` | Búsqueda de pedido por número |
| `/pagina/<slug>/` | Páginas estáticas (nosotros, contacto, etc.) |
| `/cuenta/login/` | Login |
| `/cuenta/registro/` | Registro |
| `/cuenta/perfil/` | Perfil + mis pedidos |
| `/cuenta/favoritos/` | Wishlist |
| `/admin/` | Admin Jazzmin |
| `/admin/dashboard/` | Dashboard de ventas |
| `/health/` | Health check |
| `/sitemap.xml` | Sitemap |
| `/robots.txt` | Robots |

---

## Scripts útiles

| Script | Uso |
|--------|-----|
| `python scripts/setup.py` | Setup inicial completo |
| `python scripts/seed_products.py` | Cargar/actualizar productos de prueba |
| `python scripts/seed_pages.py` | Cargar/actualizar páginas estáticas |
| `python scripts/generate_assets.py` | Regenerar logos y favicons desde el PDF de marca |
| `python scripts/validate_product_images.py` | Verificar dimensiones de fotos |
| `python scripts/optimize_product_images.py` | Optimizar fotos de productos |
| `python scripts/test_email.py tu@email.com` | Probar envío de emails |
| `python scripts/test_e2e.py` | Testing E2E del flujo completo |
| `python scripts/smoke_test.py` | Verificación rápida pre-deploy |
| `python manage.py makemigrations` | Crear migraciones |
| `python manage.py migrate` | Aplicar migraciones |
| `python manage.py collectstatic --noinput` | Recopilar estáticos para prod |
| `python manage.py createsuperuser` | Crear admin |
| `npm run build:css` | Compilar Tailwind CSS v4 |
| `npm run watch:css` | Compilar en watch mode |

---

## Stack y decisiones técnicas

### Backend
- **Django 4.2** — Framework web
- **PostgreSQL 17** — Base de datos
- **Jazzmin** — Admin UI customizado
- **django-environ** — Manejo de variables de entorno

### Frontend
- **Tailwind CSS v4** — Utility-first CSS
- **Garet** (Fontshare) — Tipografía de headings, oficial de la marca
- **Jost** (Google Fonts) — Tipografía de body
- **Alpine.js** (no, no se usa) — Interactividad

### Despliegue
- **WhiteNoise** — Servir estáticos en producción
- **Gunicorn** — WSGI server
- **PostgreSQL gestionado** — Railway / Render / DigitalOcean

### Decisiones de diseño
- Productos vendidos como piezas separadas (Top + Tanga), no como set
- Carrito basado en sesión
- Checkout crea pedido + email de confirmación + redirige a WhatsApp con mensaje pre-llenado
- El cierre de venta SIEMPRE es en WhatsApp (no hay pasarela de pago)
- Stock manejado a nivel de variante (combinación color + talle)
- Imágenes almacenadas en `media/` (filesystem en dev, Cloudinary en prod opcional)

---

## Variables de entorno (`.env`)

| Variable | Descripción | Default dev |
|----------|-------------|-------------|
| `SECRET_KEY` | Clave secreta Django | `dev-key-...` |
| `DEBUG` | Modo debug | `True` |
| `ALLOWED_HOSTS` | Hosts permitidos (CSV) | `localhost,127.0.0.1` |
| `SITE_URL` | URL del sitio | `http://localhost:8000` |
| `DATABASE_URL` | URL de PostgreSQL | `postgres://postgres:2005@localhost:5433/marplata_db` |
| `MARPLATA_WHATSAPP_NUMBER` | Número de WhatsApp Business | `+573001234567` |
| `EMAIL_HOST` | SMTP host | `smtp.gmail.com` |
| `EMAIL_PORT` | SMTP port | `587` |
| `EMAIL_HOST_USER` | SMTP usuario | (vacío) |
| `EMAIL_HOST_PASSWORD` | SMTP password (App Password de Gmail) | (vacío) |
| `DEFAULT_FROM_EMAIL` | From de emails | `MARPLATA <no-reply@marplata.com>` |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary (opcional) | (vacío) |
| `CLOUDINARY_API_KEY` | Cloudinary API key | (vacío) |
| `CLOUDINARY_API_SECRET` | Cloudinary API secret | (vacío) |
| `SENTRY_DSN` | Sentry para tracking de errores (opcional) | (vacío) |

Para producción, copiá `.env.example` a `.env.prod` y completá los valores reales.

---

## Tipografía y branding

- **Headings:** Garet (Fontshare) con `tracking-[0.25em]`
- **Body:** Jost (Google Fonts) con peso 300 (light)
- **Colores:**
  - Primary: `#6B8BC8` (azul MARPLATA)
  - Neutral: `#F5EFEB` (fondo crema)
  - Text: `#2C3E50`

Ver `static/css/tailwind.css` para el theme completo.

---

## Deploy a producción

Ver [`DEPLOYMENT.md`](DEPLOYMENT.md) para la guía completa.

Resumen:
1. Provisionar PostgreSQL (Railway / Render / Supabase)
2. Crear `.env.prod` con valores reales
3. `pip install -r requirements.txt`
4. `python manage.py migrate`
5. `python manage.py collectstatic --noinput`
6. `python scripts/seed_products.py`
7. Iniciar con Gunicorn + WhiteNoise

---

## Licencia

Privado. Todos los derechos reservados por MARPLATA.
