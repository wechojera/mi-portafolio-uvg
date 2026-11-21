@echo off
chcp 65001 >nul
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Preparando el proyecto por primera vez...
  if exist "%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" (
    "%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m venv .venv
  ) else (
    python -m venv .venv
  )
  if not exist ".venv\Scripts\python.exe" (
    echo Hace falta instalar Python 3.10 o superior desde python.org.
    pause
    exit /b 1
  )
  ".venv\Scripts\python.exe" -m pip install -r requirements.txt
  if errorlevel 1 (
    echo No se pudieron instalar las dependencias. Revisa la conexion a internet.
    pause
    exit /b 1
  )
)
echo Abriendo el portafolio de Yakin. Manten esta ventana abierta.
".venv\Scripts\python.exe" abrir_portafolio.py
pause
