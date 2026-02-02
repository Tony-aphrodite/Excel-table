@echo off
echo ============================================
echo   Building MunicipiosEspana.exe
echo ============================================
echo.

REM Install requirements
pip install -r requirements.txt

REM Build .exe
pyinstaller --onefile --windowed --name MunicipiosEspana --add-data "config.py;." --add-data "src;src" gui.py

echo.
echo ============================================
echo   Build Complete!
echo ============================================
echo.
echo The .exe file is at: dist\MunicipiosEspana.exe
echo.
pause
