@echo off
chcp 65001 > nul
title MP4 to Images Studio
cd /d "%~dp0"

:: 1. Verifier si l'environnement virtuel existe et fonctionne
if not exist "venv\Scripts\python.exe" goto :SETUP_VENV

"venv\Scripts\python.exe" -c "import PyQt6, cv2" >nul 2>&1
if errorlevel 1 goto :SETUP_VENV

goto :LAUNCH_APP

:SETUP_VENV
echo ================================================================
echo    MP4 to Images Studio - Initialisation de l'environnement
echo ================================================================
echo.

:: Verifier Python
python --version >nul 2>&1
if errorlevel 1 goto :PYTHON_NOT_FOUND

if exist "venv" (
    echo [1/3] Nettoyage de l'ancien environnement virtuel...
    rmdir /s /q "venv" >nul 2>&1
)

echo [2/3] Creation de l'environnement virtuel venv...
python -m venv venv
if not exist "venv\Scripts\activate.bat" (
    echo [ERREUR] Impossible de creer le venv.
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

echo [3/3] Telechargement et installation des dependances...
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERREUR] L'installation des dependances a echoue.
    pause
    exit /b 1
)

echo.
echo [SUCCES] Configuration terminee !
echo Lancement de l'application...

:LAUNCH_APP
if not exist "app.py" (
    echo [ERREUR CRITIQUE] Le fichier app.py est introuvable dans le dossier.
    pause
    exit /b 1
)
start "" "%~dp0venv\Scripts\pythonw.exe" "%~dp0app.py"
exit

:PYTHON_NOT_FOUND
echo [ERREUR] Python n'est pas detecte sur cet ordinateur.
echo.
echo Veuillez installer Python depuis https://www.python.org/downloads/
echo N'oubliez pas de cocher la case : "Add python.exe to PATH"
echo.
pause
exit /b 1
