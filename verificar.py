"""Auditoría de integración sin crear ni consultar una base de datos."""
import os
import re
from pathlib import Path
from html.parser import HTMLParser

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_portafolio.settings')
import django
django.setup()
from django.conf import settings
from django.test import Client, override_settings
from django.contrib.staticfiles import finders

ROOT = Path(__file__).resolve().parent

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.targets = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for key in ('href', 'src'):
            if key in attrs:
                self.targets.append(attrs[key])

client = Client()
paths = ['/', '/sobre-mi/', '/habilidades/', '/proyectos/', '/contacto/', '/404/']
with override_settings(DEBUG=False):
    for url in paths + ['/ruta-inexistente/']:
        response = client.get(url)
        expected = 200 if url in paths[:5] else 404
        assert response.status_code == expected, (url, response.status_code)
        html = response.content.decode()
        assert '<html lang="es">' in html
        assert '<title>' in html and '{%' not in html
        assert 'site-footer' in html
        parser = Links()
        parser.feed(html)
        for target in parser.targets:
            if target.startswith(settings.STATIC_URL):
                assert finders.find(target.removeprefix(settings.STATIC_URL)), target
            elif target.startswith('/'):
                assert target in paths, target
                assert client.get(target).status_code in (200, 404), target
        print('OK ruta, plantilla y enlaces:', url)

# Django normaliza {} a un backend dummy al resolver las conexiones.
import ast
config = ast.parse((ROOT / 'mi_portafolio/settings.py').read_text(encoding='utf-8'))
database_config = next(node.value for node in config.body if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'DATABASES' for t in node.targets))
assert ast.literal_eval(database_config) == {}
assert all(db['ENGINE'] == 'django.db.backends.dummy' for db in settings.DATABASES.values())
assert not (ROOT / 'db.sqlite3').exists()
assert not any('sessions' in entry or 'auth.' in entry or 'admin' in entry for entry in settings.INSTALLED_APPS)
for template in (ROOT / 'portafolio/templates').rglob('*.html'):
    assert not re.search(r'{%\s*for\b', template.read_text(encoding='utf-8')), template
css = (ROOT / 'portafolio/static/portafolio/css/estilos.css').read_text(encoding='utf-8')
assert len(re.findall('@media', css)) == 1
assert '@media (max-width:768px)' in css
print('OK restricciones: sin base de datos, sin ciclos y un breakpoint de 768px')
