@echo off
REM AI-Augmented Smart Safety Helmet - Phase 1
REM Quick Setup Script for Windows

echo ======================================================================
echo 🎯 Smart Safety Helmet - Phase 1 Setup Script (Windows)
echo ======================================================================
echo.

REM Check Python installation
echo 📋 Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python not found. Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

python --version
echo ✅ Python detected
echo.

REM Create virtual environment
echo 📦 Creating virtual environment...
if exist venv (
    echo ⚠️  Virtual environment already exists
    set /p recreate="Recreate? (y/n): "
    if /i "%recreate%"=="y" (
        rmdir /s /q venv
        python -m venv venv
        echo ✅ Virtual environment recreated
    )
) else (
    python -m venv venv
    echo ✅ Virtual environment created
)
echo.

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo 📥 Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install dependencies
echo 📥 Installing dependencies (this may take 5-10 minutes)...
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Error installing dependencies
    pause
    exit /b 1
)

echo ✅ All dependencies installed successfully
echo.

REM Pre-download YOLOv5 model
echo 📦 Pre-downloading YOLOv5 model...
python -c "import torch; torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)"
if errorlevel 1 (
    echo ⚠️  Model download will happen on first run
) else (
    echo ✅ YOLOv5 model cached successfully
)
echo.

REM Test camera
echo 📷 Testing camera availability...
python -c "import cv2; cap = cv2.VideoCapture(0); print('✅ Camera detected' if cap.isOpened() else '⚠️ No camera at index 0'); cap.release()"
echo.

REM Test audio
echo 🔊 Testing audio system...
python -c "import pygame; pygame.mixer.init(); print('✅ Audio system OK'); pygame.mixer.quit()"
echo.

echo ======================================================================
echo 🎉 Setup Complete!
echo ======================================================================
echo.
echo To run the system:
echo   1. Activate virtual environment: venv\Scripts\activate
echo   2. Run main script: python fall_detection_phase1.py
echo.
echo 📚 Documentation:
echo   - README.md          : Full usage guide
echo   - TESTING_GUIDE.md   : Testing procedures
echo   - VIVA_DEMO_SCRIPT.md: Presentation script
echo.
echo Good luck with your demo! 🚀
echo.
pause
