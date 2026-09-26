@echo off
chcp 65001 > nul
cd /d "%~dp0"
title Compilation en Executable Autonome (.exe)

echo ======================================================
echo    Creation de l'executable autonome Windows (.exe)
echo ======================================================
echo.

if not exist "venv\Scripts\activate.bat" (
    echo [ERREUR] L'environnement virtuel n'existe pas encore.
    echo Veuillez d'abord executer run.bat une fois.
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

echo [1/3] Installation / Verification de PyInstaller...
pip install pyinstaller

echo.
echo [2/3] Compilation en cours... (cette operation peut prendre 1 a 2 minutes)
pyinstaller --noconsole --onefile --icon=icon.ico --add-data="icon.png;." --add-data="timeline_slider.py;." --add-data="extractor.py;." --name="MP4_to_Images_Studio" app.py

echo.
if exist "dist\MP4_to_Images_Studio.exe" (
    echo ======================================================
    echo [SUCCES] Compilation reussie !
    echo.
    echo Votre application autonome se trouve ici :
    echo    dist\MP4_to_Images_Studio.exe
    echo.
    echo Vous pouvez copier ce fichier .exe sur N'IMPORTE QUEL PC
    echo Windows sans avoir besoin d'installer Python !
    echo ======================================================
) else (
    echo [ERREUR] La compilation a echoue.
)

pause
