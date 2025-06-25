
# FitKitchen App - macOS Installation Guide

This document explains how to install and run the FitKitchen app on a Mac, including how to build a `.app` for double-click launch.

---

##  Requirements

- macOS (Ventura or later preferred)
- Python 3.x installed from [https://www.python.org](https://www.python.org)
- Internet connection (for installing dependencies)

---

##  Setup Steps

### 1. Clone or Copy the Project
Copy the full project folder (this folder) to your Mac’s Desktop or Downloads.

### 2. Open Terminal and Navigate to the Project

```bash
cd ~/Desktop/fitkitchen_database
```

> Adjust the path if needed.

---

### 3. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install customtkinter openpyxl tkcalendar
```

---

### 5. Test the Application

```bash
python3 ui/main.py
```

Make sure the app opens and works as expected.

---

### 6. Install PyInstaller

```bash
pip install pyinstaller
```

---

### 7. Build the macOS App

```bash
pyinstaller --noconfirm --windowed --name "FitKitchen" main.py
```

This creates a `.app` file in the `dist/` folder.

---

### 8. Launch the App

```bash
open dist
```

Double-click **FitKitchen.app** to run it.

---

##  Optional Cleanup

You may remove these folders if you like:

- `build/`
- `__pycache__/`
- `FitKitchen.spec`

---

##  Security Note

If macOS blocks the app:

- Go to **System Settings → Privacy & Security**
- Click **Open Anyway**

---

##  Updating the App

If you make code changes:
1. Replace the project folder
2. Rebuild the app:

```bash
source venv/bin/activate
pyinstaller --noconfirm --windowed --name "FitKitchen" ui/main.py
```

---

For help, contact the developer.
