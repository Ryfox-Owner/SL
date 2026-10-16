@echo off
REM Crea el .exe (necesita Python instalado). Ejecuta este archivo con doble clic.
pip install pywebview pyinstaller
pyinstaller --noconfirm --onefile --windowed --name SimuladorGestion --add-data "index.html;." --add-data "datos;datos" app.py
echo.
echo Listo: el programa esta en la carpeta dist\SimuladorGestion.exe
pause
