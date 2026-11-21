"""Inicia el sitio local o abre el servidor existente, sin pasos de terminal."""
from pathlib import Path
import socket
import subprocess
import sys
import time
import webbrowser

root = Path(__file__).resolve().parent
def running():
    try:
        with socket.create_connection(('127.0.0.1', 8000), timeout=0.5):
            return True
    except OSError:
        return False

if running():
    webbrowser.open('http://127.0.0.1:8000/')
    print('El sitio ya esta encendido. Se abrio en el navegador.')
else:
    server = subprocess.Popen([sys.executable, 'manage.py', 'runserver', '127.0.0.1:8000', '--noreload'], cwd=root)
    try:
        for attempt in range(50):
            if server.poll() is not None:
                raise SystemExit('El servidor no pudo iniciar. Revisa el mensaje anterior.')
            if running():
                webbrowser.open('http://127.0.0.1:8000/')
                break
            time.sleep(0.2)
        else:
            server.terminate()
            raise SystemExit('El servidor tardo demasiado en iniciar.')
        print('Manten esta ventana abierta. Ctrl+C para detener el servidor.')
        server.wait()
    except KeyboardInterrupt:
        server.terminate()
        server.wait()
