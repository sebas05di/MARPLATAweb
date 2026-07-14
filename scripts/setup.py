"""Script de setup para nuevos desarrolladores.

Crea un entorno virtual, instala dependencias, configura .env,
aplica migraciones y carga datos de prueba.

Uso:
    python scripts/setup.py
"""
import os
import sys
import subprocess
import platform


VENV_NAME = 'venv'
REQUIREMENTS = 'requirements.txt'


def run(cmd, check=True, shell=True):
    print(f'$ {cmd}')
    result = subprocess.run(cmd, shell=shell, check=check)
    return result.returncode == 0


def header(text):
    print()
    print('=' * 60)
    print(text)
    print('=' * 60)


def main():
    is_windows = platform.system() == 'Windows'
    py = 'python' if is_windows else 'python3'
    venv_python = os.path.join(VENV_NAME, 'Scripts' if is_windows else 'bin', 'python')
    venv_pip = os.path.join(VENV_NAME, 'Scripts' if is_windows else 'bin', 'pip')
    venv_activate = os.path.join(VENV_NAME, 'Scripts' if is_windows else 'bin', 'activate')

    header('1. Creando entorno virtual')
    if not os.path.exists(VENV_NAME):
        run(f'{py} -m venv {VENV_NAME}')
    else:
        print(f'{VENV_NAME}/ ya existe, saltando...')

    header('2. Actualizando pip')
    run(f'"{venv_python}" -m pip install --upgrade pip')

    header('3. Instalando dependencias')
    if os.path.exists(REQUIREMENTS):
        run(f'"{venv_pip}" install -r {REQUIREMENTS}')
    else:
        print(f'No se encontró {REQUIREMENTS}')

    header('4. Instalando dependencias de Node')
    if os.path.exists('package.json'):
        run('npm install')
    else:
        print('No se encontró package.json')

    header('5. Configurando .env')
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            import shutil
            shutil.copy('.env.example', '.env')
            print('.env creado desde .env.example')
            print('IMPORTANTE: editá .env y completá SECRET_KEY y credenciales')
        else:
            print('No se encontró .env.example')
    else:
        print('.env ya existe, saltando...')

    header('6. Aplicando migraciones')
    run(f'"{venv_python}" manage.py migrate')

    header('7. Compilando CSS')
    run('npm run build:css')

    header('8. Cargando datos de prueba (opcional)')
    if os.path.exists('scripts/seed_products.py'):
        respuesta = input('¿Cargar productos de prueba? (s/n): ').strip().lower()
        if respuesta in ('s', 'si', 'sí', 'y', 'yes'):
            run(f'"{venv_python}" scripts/seed_products.py')
        else:
            print('Saltando seed de productos')

    if os.path.exists('scripts/seed_pages.py'):
        respuesta = input('¿Cargar páginas estáticas? (s/n): ').strip().lower()
        if respuesta in ('s', 'si', 'sí', 'y', 'yes'):
            run(f'"{venv_python}" scripts/seed_pages.py')

    header('Setup completo!')
    print()
    print('Próximos pasos:')
    print(f'  1. Activar venv:  {venv_activate}')
    print('  2. Crear superuser:  python manage.py createsuperuser')
    print('  3. Correr server:  python manage.py runserver')
    print()
    print('URLs:')
    print('  http://localhost:8000/')
    print('  http://localhost:8000/admin/')
    print('  http://localhost:8000/admin/dashboard/')


if __name__ == '__main__':
    main()
