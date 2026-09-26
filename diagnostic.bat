@echo off
chcp 65001 > nul
title Diagnostic MP4 to Images Studio
cd /d "%~dp0"

echo ================================================================
echo    DIAGNOSTIC DE VOTRE ENVIRONNEMENT WINDOWS
echo ================================================================
echo.

echo [1] Verification de Python :
where python
if %errorlevel% neq 0 (
    echo [X] Python n'est PAS detecte dans votre PATH Windows.
) else (
    python --version
    echo [OK] Python est bien detecte.
)
echo.

echo [2] Verification de l'environnement virtuel venv :
if exist "venv\Scripts\python.exe" (
    echo [OK] Le dossier venv existe.
    echo Test d'execution du venv :
    venv\Scripts\python.exe -c "import sys; print('  Python venv version:', sys.version)"
    if %errorlevel% neq 0 (
        echo [X] Le venv est casse ou provient d'une autre machine !
    ) else (
        echo [OK] Le venv repond correctement.
        echo.
        echo Test des dependances PyQt6 et OpenCV :
        venv\Scripts\python.exe -c "import PyQt6; print('  [OK] PyQt6 :', PyQt6.__file__)"
        venv\Scripts\python.exe -c "import cv2; print('  [OK] OpenCV :', cv2.__version__)"
    )
) else (
    echo [-] Aucun dossier venv present.
)

echo.
echo ================================================================
echo Fin du diagnostic.
echo ================================================================
pause
