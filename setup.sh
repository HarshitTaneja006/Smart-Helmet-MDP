#!/bin/bash

# AI-Augmented Smart Safety Helmet - Phase 1
# Quick Setup Script for Linux/Mac
# For Windows, run commands manually in PowerShell

echo "======================================================================"
echo "🎯 Smart Safety Helmet - Phase 1 Setup Script"
echo "======================================================================"
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
if (( $(echo "$python_version < 3.8" | bc -l) )); then
    echo "❌ Error: Python 3.8+ required. Current: $python_version"
    exit 1
else
    echo "✅ Python $python_version detected"
fi

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists"
    read -p "Recreate? (y/n): " recreate
    if [ "$recreate" = "y" ]; then
        rm -rf venv
        python3 -m venv venv
        echo "✅ Virtual environment recreated"
    fi
else
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "📥 Installing dependencies (this may take 5-10 minutes)..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ All dependencies installed successfully"
else
    echo "❌ Error installing dependencies"
    exit 1
fi

# Download YOLOv5 model (pre-cache)
echo ""
echo "📦 Pre-downloading YOLOv5 model..."
python3 -c "import torch; torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ YOLOv5 model cached successfully"
else
    echo "⚠️  Model download will happen on first run"
fi

# Test camera availability
echo ""
echo "📷 Testing camera availability..."
python3 << END
import cv2
cap = cv2.VideoCapture(0)
if cap.isOpened():
    print("✅ Camera detected (Index 0)")
    cap.release()
else:
    print("⚠️  No camera found at index 0")
    print("   Try changing CAMERA_INDEX to 1 or 2 in the code")
END

# Test audio system
echo ""
echo "🔊 Testing audio system..."
python3 << END
try:
    import pygame
    pygame.mixer.init()
    print("✅ Audio system initialized")
    pygame.mixer.quit()
except Exception as e:
    print(f"⚠️  Audio test failed: {e}")
    print("   Install audio dependencies:")
    print("   Ubuntu/Debian: sudo apt-get install python3-pygame libsdl2-mixer-2.0-0")
    print("   Mac: brew install sdl2 sdl2_mixer")
END

echo ""
echo "======================================================================"
echo "🎉 Setup Complete!"
echo "======================================================================"
echo ""
echo "To run the system:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run main script: python fall_detection_phase1.py"
echo ""
echo "📚 Documentation:"
echo "  - README.md          : Full usage guide"
echo "  - TESTING_GUIDE.md   : Testing procedures"
echo "  - VIVA_DEMO_SCRIPT.md: Presentation script"
echo ""
echo "Good luck with your demo! 🚀"
echo ""
