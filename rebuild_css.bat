@echo off
chcp 65001 >nul
echo ============================================
echo   MARPLATA — Recompilar CSS
echo ============================================
echo.
cd /d C:\Users\Sebastian16\Desktop\MARPLATA
call venv\Scripts\activate
call npm run build:css
echo.
echo CSS recompilado. Volve a abrir el navegador.
pause
