@echo off
chcp 65001 >nul
echo ============================================
echo   MARPLATA — Verificacion rapida
echo ============================================
echo.
cd /d C:\Users\Sebastian16\Desktop\MARPLATA
call venv\Scripts\activate
python scripts\smoke_test.py
echo.
pause
