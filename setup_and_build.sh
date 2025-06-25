#!/bin/bash

echo "Setting up FitKitchen..."
echo "--------------------------------"

# 1. Ensure pip is up to date
echo "Upgrading pip..."
python3 -m pip install --upgrade pip

# 2. Install required packages system-wide
echo "Installing dependencies..."
python3 -m pip install customtkinter openpyxl tkcalendar pyinstaller

# 3. Build the .app using PyInstaller
echo "Building the app..."
pyinstaller --noconfirm --windowed --name "FitKitchen" main.py

# 4. Launch the app
echo "Launching FitKitchen..."
open dist/FitKitchen.app

echo "✅ Done! You can now launch the app from dist/FitKitchen.app"
