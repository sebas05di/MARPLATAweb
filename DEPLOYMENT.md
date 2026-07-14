# 🚀 MARPLATA — Deployment Checklist

## Pre-deployment

### 1. Variables de entorno

El proyecto usa **3 archivos de environment** (NUNCA commitear `.env` ni `.env.prod`):

| Archivo | Propósito | Commiteado |
|---------|-----------|------------|
| `.env.example` | Plantilla de referencia (sin valores reales) | ✅ Sí |
| `.env` | **Desarrollo local** (DEBUG=True, localhost) | ❌ No (en .gitignore) |
| `.env.prod` | **Producción** (DEBUG=False, dominio real) | ❌ No (en .gitignore) |

#### En el servidor de producción:
1. Subir `.env.prod` (NO renombrar a `.env`, dejarlo como `.env.prod`).
2. Configurar el servidor para usar `DJANGO_SETTINGS_MODULE=config.settings.prod`.
3. En producción, `load_dotenv()` busca automáticamente `.env` primero, luego `.env.prod` como fallback en `prod.py`.

Generar `SECRET_KEY` seguro:
```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

#### Checklist de variables:
- [ ] `SECRET_KEY` — clave aleatoria larga.
- [ ] `DEBUG=False`
- [ ] `ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com`
- [ ] `SITE_URL=https://tu-dominio.com`
- [ ] `DATABASE_URL=postgres://...`
- [ ] `MARPLATA_WHATSAPP_NUMBER=+57...`
- [ ] `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL`
- [ ] (Opcional) `CLOUDINARY_*` para imágenes
- [ ] (Opcional) `SENTRY_DSN` para tracking de errores

### 2. Instalar dependencias de producción
```bash
pip install -r requirements.txt
```

### 3. Recolectar archivos estáticos
```bash
python manage.py collectstatic --noinput
```

### 4. Aplicar migraciones
```bash
python manage.py migrate --noinput
```

### 5. Compilar Tailwind CSS
```bash
npm install
npm run build:css
```

### 6. Crear superusuario
```bash
python manage.py createsuperuser
```

## 2. Configurar Email transaccional (Gmail)

El sitio envía emails automáticos para:
- Confirmación de pedido al cliente
- Aviso al admin cuando hay pedido nuevo
- Cambios de estado del pedido (enviado, entregado)
- Recuperación de contraseña
- Newsletter (bienvenida)
- Bienvenida al registrarse

**Importante:** el email es solo notificación. El cierre de venta se hace en WhatsApp.

### Paso a paso para Gmail

1. **Crear/elegir cuenta Gmail del negocio**
   - Recomendado: una cuenta solo para notificaciones, no la personal.
   - Ejemplo: `marplata.notificaciones@gmail.com`

2. **Activar verificación en 2 pasos**
   - Ir a https://myaccount.google.com/security
   - Sección "Verificación en 2 pasos" → Activar.

3. **Generar App Password**
   - Ir a https://myaccount.google.com/apppasswords
   - Nombre de la app: "MARPLATA Web"
   - Click "Crear"
   - Copiar la contraseña de 16 caracteres.
   - Esta es la que va en `EMAIL_HOST_PASSWORD`.

4. **Completar variables en `.env.prod`**
   ```env
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=marplata.notificaciones@gmail.com
   EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
   DEFAULT_FROM_EMAIL=MARPLATA <no-reply@marplata.com>
   ```

5. **Probar envío de emails**
   ```bash
   python manage.py shell -c "from django.core.mail import send_mail; send_mail('Test MARPLATA', 'Funciona', None, ['tu-email@gmail.com'])"
   ```

6. **Verificar que llegan a inbox (no spam)**
   - Revisar la bandeja de entrada del email de destino.
   - Si caen en spam, configurar SPF/DKIM en el dominio.

### Límites de Gmail
- **500 emails por día** (cuenta gratuita).
- Si se supera: cambiar a **SendGrid** (100 emails/día gratis).

### Alternativa: SendGrid
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DEFAULT_FROM_EMAIL=MARPLATA <no-reply@marplata.com>
```

## 3. Assets visuales y branding

Los assets de branding ya están generados en `static/img/branding/` y `static/img/favicons/`.

### Archivos incluidos

| Archivo | Uso |
|---------|-----|
| `static/img/branding/og-image.png` | Open Graph (1200x630) para compartir en redes |
| `static/img/favicons/favicon.ico` | Favicon multi-resolución |
| `static/img/favicons/apple-touch-icon.png` | iOS home screen (180x180) |
| `static/site.webmanifest` | PWA manifest |

### Verificación manual
- [ ] Abrir el sitio → favicon aparece en la pestaña.
- [ ] Compartir URL en WhatsApp/Facebook → og:image se ve correctamente.
- [ ] En mobile: logo responsive (no se deforma).

## 4. Imágenes de productos

Las imágenes de productos se suben por el admin de Django y se almacenan en `media/products/`.

### Estándares recomendados
- **Mínimo:** 1200x1600 px
- **Recomendado:** 1920x2560 px
- **Peso máximo:** 500 KB

### Workflow para actualizar fotos

1. Recibir las fotos HD y optimizarlas (JPG/WebP, máximo 1920 px de ancho).
2. Subirlas por el admin de Django asociándolas a cada producto/variante.
3. Verificar en el navegador que se vean correctamente en catálogo y detalle.

## Verificación post-deploy

### Funcional
- [ ] `https://tu-dominio.com/` carga correctamente
- [ ] `https://tu-dominio.com/admin/login/` carga
- [ ] `https://tu-dominio.com/health/` devuelve `{"status":"ok","database":"ok"}`
- [ ] `https://tu-dominio.com/sitemap.xml` es accesible
- [ ] `https://tu-dominio.com/robots.txt` es accesible
- [ ] Login con superuser funciona
- [ ] Registrar un usuario de prueba funciona
- [ ] Agregar al carrito y hacer checkout → redirige a WhatsApp
- [ ] Newsletter AJAX funciona
- [ ] Búsqueda funciona
- [ ] Wishlist funciona (con login)
- [ ] Emails transaccionales llegan (verificar con un pedido de prueba)

### Seguridad
- [ ] HTTPS forzado (redirige http → https)
- [ ] `Strict-Transport-Security` header presente
- [ ] `X-Frame-Options: DENY` header presente
- [ ] `X-Content-Type-Options: nosniff` header presente
- [ ] `Referrer-Policy: same-origin` header presente
- [ ] Cookies marcadas como `Secure` y `HttpOnly`
- [ ] `SECRET_KEY` único y NO está en el repositorio
- [ ] `.env` está en `.gitignore`

### Performance
- [ ] Compresión gzip/brotli activada (WhiteNoise)
- [ ] Imágenes de producto en formato WebP
- [ ] Tailwind CSS minificado
- [ ] Static files servidos por CDN (Cloudflare, Cloudinary, etc.)

## Plataformas recomendadas

### Render.com
1. Conectar repo de GitHub.
2. Crear Web Service:
   - Build command: `./build.sh`
   - Start command: `gunicorn config.wsgi`
3. Crear PostgreSQL database.
4. Configurar variables de entorno en dashboard.
5. Custom domain + SSL automático.

### Railway.app
1. Conectar repo.
2. Agregar PostgreSQL plugin.
3. Variables de entorno en Variables tab.
4. Deploy automático.

### DigitalOcean App Platform
1. Crear app desde GitHub.
2. Build command: `pip install -r requirements.txt && npm install && npm run build:css && python manage.py collectstatic --noinput && python manage.py migrate`
3. Run command: `gunicorn config.wsgi`

## Rollback

En caso de error crítico:
```bash
git revert HEAD
git push origin main
# La plataforma hace redeploy automático
```

## Monitoreo (opcional)

### Sentry
Configurar `SENTRY_DSN` en `.env.prod`. El proyecto ya incluye la integración en `config/settings/prod.py`.

### Uptime monitoring
- UptimeRobot (gratis): monitorea `/health/`
- Better Uptime
- Cronitor

## Comandos útiles post-deploy

```bash
python manage.py shell
python manage.py createsuperuser
python manage.py changepassword admin
python manage.py dumpdata > backup.json
```
