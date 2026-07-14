@echo off
chcp 65001 >nul
echo ============================================
echo   MARPLATA — Iniciando servidor
echo ============================================
echo.
cd /d C:\Users\Sebastian16\Desktop\MARPLATA
call venv\Scripts\activate
echo Venv activado
echo.
echo Compilando CSS (por si hubo cambios)...
call npm run build:css >nul 2>&1
echo CSS listo
echo.
echo ============================================
echo   Servidor corriendo en http://localhost:8000/
echo   Presiona Ctrl+C para detener
echo ============================================
echo.
python manage.py runserver
pause
