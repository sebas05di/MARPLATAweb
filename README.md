# MARPLATA — E-commerce de vestidos de baño

> **Diseña tu estilo, resalta tu esencia.**  
> Plataforma de e-commerce para MARPLATA, marca de vestidos de baño premium.
> Cierre de venta asistido por WhatsApp, panel de administración y dashboard de ventas.

[![Django](https://img.shields.io/badge/Django-4.2-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-v4-06B6D4?logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)

---

## ✨ Características

- **Catálogo de productos** con colecciones, variantes (talla / color) y búsqueda.
- **Carrito de compras** basado en sesión + **checkout** con cierre de venta por WhatsApp.
- **Panel de administración** con [Jazzmin](https://github.com/farridav/django-jazzmin) (UI moderna sobre el admin nativo de Django).
- **Dashboard de ventas** con métricas de pedidos (`/admin/dashboard/`).
- **Cuentas de usuario**: registro, login, perfil, **wishlist** y **newsletter**.
- **Páginas estáticas** dinámicas (nosotros, contacto, cuidados, cambios, envíos) gestionables desde el admin.
- **SEO**: meta descriptions dinámicas, `sitemap.xml`, `robots.txt`, Open Graph y Twitter Cards.
- **PWA**: `site.webmanifest` + favicons multi-resolución.
- **Caché** de páginas estáticas frecuentes (5 min TTL) para reducir queries.
- **Imágenes** optimizadas con [WhiteNoise](https://whitenoise.evans.io/) + soporte opcional de [Cloudinary](https://cloudinary.com/).
- **Tracking de errores** opcional con [Sentry](https://sentry.io/).
- **Deploy a producción** documentado (Gunicorn + WhiteNoise + PostgreSQL).

---

## 🛠 Stack técnico

| Capa           | Tecnología                                                         |
|----------------|--------------------------------------------------------------------|
| Backend        | Django 4.2 · Python 3.11+                                          |
| Base de datos  | PostgreSQL 17                                                      |
| Frontend       | Tailwind CSS v4 · Garet + Jost · JavaScript vanilla                 |
| Admin          | Jazzmin (sobre Django Admin)                                       |
| Imágenes       | WhiteNoise · Cloudinary (opcional)                                  |
| Caché          | LocMemCache (dev) · Redis (prod opcional)                          |
| Emails         | SMTP (Gmail App Password)                                          |
| Monitoring     | Sentry (opcional)                                                  |
| Deploy         | Gunicorn · Render / Heroku · `render.yaml` + `Procfile`            |
| DevOps         | Git · GitHub · entornos separados `dev` / `prod`                   |

---

## 🚀 Setup rápido

```bash
# 1. Crear entorno virtual e instalar dependencias
python -m venv venv
.\venv\Scripts\Activate.ps1            # Windows
source venv/bin/activate               # Mac/Linux
pip install -r requirements.txt

# 2. Instalar dependencias Node y compilar CSS
npm install
npm run build:css

# 3. Configurar variables de entorno
copy .env.example .env                 # Windows
cp .env.example .env                   # Mac/Linux
# Luego editá .env con tus valores

# 4. Aplicar migraciones y crear datos base
python manage.py migrate
python manage.py seed_pages
python manage.py createsuperuser

# 5. Correr el servidor
python manage.py runserver
```

Abrí:
- `http://localhost:8000/` — sitio público
- `http://localhost:8000/admin/` — admin Jazzmin
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
│   └── core/                      # Site config, páginas estáticas, emails
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
│   │   └── marplata.css           # CSS compilado (Tailwind v4)
│   ├── js/                        # JavaScript
│   ├── img/
│   │   ├── hero/                  # Imágenes del hero
│   │   ├── products/              # Fotos fuente de productos
│   │   ├── branding/              # og:image y favicons
│   │   └── favicons/              # Favicon multi-resolución
│   └── site.webmanifest           # PWA manifest
├── assets/                        # Fuentes del frontend
│   └── css/tailwind.css           # CSS fuente (Tailwind v4)
├── media/                         # Archivos subidos por usuarios/admin
├── DEPLOYMENT.md                  # Guía de deploy a producción
├── requirements.txt               # Dependencias Python
├── package.json                   # Dependencias Node
├── .env.example                   # Plantilla de .env
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

## Comandos útiles

| Comando | Uso |
|---------|-----|
| `python manage.py migrate` | Aplicar migraciones |
| `python manage.py seed_pages` | Cargar/actualizar páginas estáticas |
| `python manage.py seed_products` | Cargar/actualizar productos desde `static/img/products/` |
| `python manage.py collectstatic --noinput` | Recopilar estáticos para prod |
| `python manage.py createsuperuser` | Crear admin |
| `python manage.py test_cloudinary` | Verificar configuración de Cloudinary |
| `npm run build:css` | Compilar Tailwind CSS v4 |
| `npm run watch:css` | Compilar en watch mode |

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

Para producción, copiá `.env.example` a `.env.prod` y completá los valores reales. Ver [`DEPLOYMENT.md`](DEPLOYMENT.md) para la guía completa.

---

## Deploy a producción

Ver [`DEPLOYMENT.md`](DEPLOYMENT.md).

Resumen:
1. Provisionar PostgreSQL.
2. Crear `.env.prod` con valores reales.
3. `pip install -r requirements.txt`
4. `npm install && npm run build:css`
5. `python manage.py migrate`
6. `python manage.py collectstatic --noinput`
7. Iniciar con Gunicorn + WhiteNoise.

---

## Licencia

Privado. Todos los derechos reservados por MARPLATA.
