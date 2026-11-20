# Mi portafolio · Introducción a la Programación Web

Portafolio académico de cinco páginas y un error 404 personalizado, desarrollado con Django, HTML, CSS y JavaScript puro. Incluye contenido académico de ejemplo marcado como pendiente. No atribuye experiencia profesional al estudiante.

Autor: **Yakin José Esquit Toledo**, Ingeniería en Informática, UVG. [Perfil GitHub](https://github.com/wechojera) · [Repositorio privado del curso](https://github.com/wechojera/mi-portafolio-uvg) · Correo: yakintoledo@gmail.com.

El acceso del docente al repositorio privado debe compartirse desde la cuenta del estudiante.

## Requisitos e instalación

Python 3.10 o superior y pip. Ejecutar desde esta carpeta, donde está `manage.py`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py check
python manage.py runserver
```

En macOS/Linux, activar con `source .venv/bin/activate`. En Windows también se puede ejecutar directamente `.\.venv\Scripts\python.exe manage.py runserver` si PowerShell restringe la activación. Abrir http://127.0.0.1:8000/.

No ejecutar migraciones. `DATABASES = {}`: no hay modelos, base de datos, autenticación, sesiones ni panel admin. El formulario no hace peticiones ni conserva datos.

## Rutas

| Ruta | Página | Respuesta |
|---|---|---|
| `/` | Inicio | 200 |
| `/sobre-mi/` | Biografía, formación e intereses | 200 |
| `/habilidades/` | Categorías y niveles | 200 |
| `/proyectos/` | Tres propuestas y filtros | 200 |
| `/contacto/` | Formulario y perfiles pendientes | 200 |
| `/404/` | Demostración visible del error | 404 |

Para probar el handler real, detener el servidor y ejecutar en PowerShell:

```powershell
$env:DJANGO_DEBUG='False'
python manage.py runserver --insecure
```

Visitar `/ruta-inexistente/`. Debe mostrar el diseño personalizado y devolver 404. `--insecure` permite estáticos únicamente para esta comprobación local. Restaurar `$env:DJANGO_DEBUG='True'` al terminar. Con DEBUG activo, Django muestra su página técnica para rutas inexistentes, mientras `/404/` siempre muestra la página diseñada.

## Estructura

- `mi_portafolio/`: configuración, URLs raíz y puntos de entrada WSGI/ASGI.
- `portafolio/views.py` y `urls.py`: una vista y ruta por página; cada vista proporciona un título visible.
- `portafolio/templates/portafolio/`: base compartida y seis plantillas; contenido escrito directamente, sin ciclos de plantilla.
- `portafolio/static/portafolio/`: CSS, JavaScript e imágenes (marca SVG original).
- `GUIA_FIGMA.html`: especificación visual copiable a Figma, con frames de referencia.
- `FASE_1.html`: objetivos, público, mapa del sitio, inventario y criterios de aceptación.
- `verificar.py`: comprobación sin base de datos de rutas, plantillas, estáticos, enlaces y restricciones.
- `entrega/index.html`: índice local con mapa e inventario, doce wireframes SVG, 24 capturas reales, doce comparativas y guion de exposición de cinco minutos.

Los wireframes de referencia se prepararon con el proyecto ya existente. Las capturas comparan una vista de 900 px de alto, a 1440 y 390 px de ancho. Figma y Django comparten la identidad visual, con diferencias documentadas de composición y texto. Se comprobó la navegación del prototipo desde Inicio hacia Proyectos en escritorio y hacia Contacto en móvil.

El calendario recibido abarca seis semanas y exige revisiones antes de avanzar de fase. El historial que se registre desde esta preparación usa fechas reales; no acredita varias semanas anteriores de trabajo ni revisiones docentes aún no confirmadas.

## Personalización

El sitio ya incluye a Yakin José Esquit Toledo, estudiante de Ingeniería en Informática en la UVG. Se añadieron música, tecnología y resolución de problemas, junto con una biografía redactada con autorización del estudiante. Los niveles técnicos son orientativos. GitHub: https://github.com/wechojera. Correo: yakintoledo@gmail.com. Faltan LinkedIn y los repositorios de proyectos reales.

Para abrir sin terminal, hacer doble clic en `ABRIR_PORTAFOLIO.cmd`; mantener abierta su ventana mientras se utiliza el sitio. Si falta el entorno virtual, el archivo intenta crearlo e instalar Django automáticamente (requiere Python disponible y conexión en esa primera apertura). En esta computadora ya está preparado. Si el servidor está encendido, solo abre el sitio existente.

### Dónde editar después

1. Nombre en el contexto de `inicio` en `views.py`.
2. Frase y biografía en `inicio.html` y `sobre_mi.html`.
3. Formación, institución, carrera, período e intereses en `sobre_mi.html`.
4. Categorías y niveles reales en `habilidades.html`.
5. Tres proyectos reales: títulos, descripciones, categoría, tecnologías, portadas y URL de repositorios en `proyectos.html`; sincronizar el destacado de `inicio.html`.
6. GitHub, LinkedIn y correo en `contacto.html`: sustituir los estados pendientes por enlaces reales (`https://…` y `mailto:…`).
7. Confirmar si se usará foto. La composición CSS y el avatar abstracto funcionan sin ella. Guardar una foto autorizada en la carpeta `img/` y cargarla con la etiqueta `static`, con texto alternativo.

## JavaScript

`main.js` habilita el botón móvil, controla `aria-expanded`, cierra con Escape y devuelve el foco al botón. Los filtros ocultan tarjetas por categoría, mantienen `aria-pressed` y anuncian el número de resultados. El formulario impide el envío con `preventDefault`, valida nombre no vacío, correo con formato válido y mensaje de al menos 10 caracteres sin espacios extremos. Muestra errores asociados a los campos y lleva el foco al primer error. Una confirmación explica que no se envió ni guardó información. No utiliza fetch, almacenamiento ni bibliotecas. Sin JavaScript la navegación y todos los proyectos siguen visibles; el formulario queda deshabilitado.

## Comprobaciones

```powershell
python manage.py check
python verificar.py
```

Para revisión manual: probar a 1440 y 390 px; abrir/cerrar menú, navegar con Tab y Escape, seleccionar todos los filtros, enviar campos vacíos, un correo inválido, un mensaje corto y después valores válidos. Confirmar que no aparece ninguna petición de envío en la pestaña de red. El único breakpoint CSS es `max-width:768px`.

## Trabajar con el repositorio de GitHub

El repositorio privado se creó en la cuenta del estudiante. Para obtener una copia con el historial, desde una carpeta distinta a este proyecto:

```powershell
git clone https://github.com/wechojera/mi-portafolio-uvg.git
cd mi-portafolio-uvg
```

GitHub guarda el código; GitHub Pages no ejecuta Django. Para un despliegue posterior usar un alojamiento compatible con Python, definir una clave secreta en el entorno, DEBUG=False, hosts permitidos y servicio de archivos estáticos (`collectstatic`). El proyecto está configurado para desarrollo local.

Registrar cada cambio real durante el curso con `git add`, `git commit` y `git push`, usando mensajes que expliquen lo que se cambió. No cambiar fechas de commits para representar trabajo anterior.

## Archivo de Figma

[Yakin Esquit · Portafolio UVG](https://www.figma.com/design/9Yy8Ejx487zgaSkG4pRVaW/Yakin-Esquit-Portafolio-UVG): versiones de escritorio y móvil de las seis páginas, fundamentos y componentes editables. Se usa Inter en el diseño y en el sitio; la fuente se incluye en archivos estáticos con licencia OFL. La distribución en Figma es una propuesta visual con algunas diferencias de contenido y composición respecto de la implementación.
