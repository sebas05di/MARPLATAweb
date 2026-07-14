@echo off
chcp 65001 >nul
echo ============================================
echo   MARPLATA — Reiniciar base de datos
echo ============================================
echo.
echo ATENCION: Esto borra TODOS los datos (pedidos, usuarios, productos)
echo Solo hacerlo en desarrollo local.
echo.
set /p confirm=Escribi SI para continuar: 
if not "%confirm%"=="SI" (
    echo Cancelado.
    pause
    exit /b
)
echo.
cd /d C:\Users\Sebastian16\Desktop\MARPLATA
call venv\Scripts\activate
echo Borrando base de datos...
python manage.py flush --noinput
echo Aplicando migraciones...
python manage.py migrate
echo Cargando productos de prueba...
python scripts\seed_products.py
echo Cargando paginas estaticas...
python scripts\seed_pages.py
echo.
echo ============================================
echo   Base de datos reiniciada
echo   Email admin: admin@marplata.com
echo   Password: admin123 (creala con createsuperuser)
echo ============================================
pause
