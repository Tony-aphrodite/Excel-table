@echo off
echo ============================================
echo   Building MunicipiosGenerator.exe
echo ============================================
echo.

REM Install requirements
pip install -r requirements.txt

REM Build .exe with countries folder and SSL certificates included
pyinstaller --onefile --windowed --name MunicipiosGenerator --add-data "config.py;." --add-data "src;src" --add-data "countries;countries" --collect-data certifi --hidden-import certifi gui.py

echo.
echo ============================================
echo   Build Complete!
echo ============================================
echo.
echo The .exe file is at: dist\MunicipiosGenerator.exe
echo.
pause
