"""Genera únicamente las páginas públicas del portafolio a partir de Django."""
import argparse
from html.parser import HTMLParser
import os
from pathlib import Path
import re
import shutil
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_portafolio.settings')

import django
django.setup()
from django.test import Client, override_settings
from django.urls import get_script_prefix, set_script_prefix

ROUTES = ['/', '/sobre-mi/', '/habilidades/', '/proyectos/', '/contacto/', '/404/']

class Resources(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ('href', 'src') and value:
                self.links.append(value)

def build(base_path=''):
    base = '/' + base_path.strip('/') if base_path.strip('/') else ''
    if base and not re.fullmatch(r'/[A-Za-z0-9._/-]+', base):
        raise ValueError('La ruta base contiene caracteres no permitidos.')
    if any(part in ('.', '..') for part in base.split('/')):
        raise ValueError('La ruta base no puede contener puntos relativos.')
    output = ROOT / '_site'
    output.mkdir(exist_ok=True)
    previous_prefix = get_script_prefix()
    documents = []
    try:
        with override_settings(DEBUG=False, FORCE_SCRIPT_NAME=base or None,
                               STATIC_URL=base + '/static/'):
            set_script_prefix(base + '/')
            client = Client()
            for route in ROUTES:
                response = client.get(route)
                expected = 404 if route == '/404/' else 200
                if response.status_code != expected:
                    raise RuntimeError(f'{route}: respuesta {response.status_code}')
                html = response.content.decode('utf-8')
                destination = output / route.strip('/') / 'index.html'
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_text(html, encoding='utf-8')
                documents.append((destination, html))
                if route == '/404/':
                    (output / '404.html').write_text(html, encoding='utf-8')
    finally:
        set_script_prefix(previous_prefix)
    shutil.copytree(ROOT / 'portafolio/static/portafolio',
                    output / 'static/portafolio', dirs_exist_ok=True)
    (output / '.nojekyll').write_text('', encoding='utf-8')
    # Comprobar enlaces después de aplicar la ruta /nombre-del-repositorio/.
    for destination, html in documents:
        parser = Resources()
        parser.feed(html)
        for link in parser.links:
            parts = urlsplit(link)
            if parts.scheme or parts.netloc or not parts.path:
                continue
            if not parts.path.startswith(base + '/'):
                raise RuntimeError(f'Enlace fuera de la ruta pública: {link}')
            relative = parts.path[len(base):].lstrip('/')
            resource = output / relative
            if parts.path.endswith('/'):
                resource /= 'index.html'
            if not resource.is_file():
                raise RuntimeError(f'Recurso inexistente en {destination.name}: {link}')
    for css in (output / 'static').rglob('*.css'):
        for resource in re.findall(r'url\([\"\']?([^\"\')]+)', css.read_text(encoding='utf-8')):
            if urlsplit(resource).scheme:
                continue
            if not (css.parent / resource).resolve().is_file():
                raise RuntimeError(f'Recurso CSS inexistente: {resource}')
    print(f'OK: seis páginas, 404 y recursos verificados para {base or "/"}.')
    print(f'Salida: {output}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-path', default='', help='Ruta base de GitHub Pages.')
    build(parser.parse_args().base_path)
