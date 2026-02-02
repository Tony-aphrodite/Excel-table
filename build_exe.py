#!/usr/bin/env python3
"""
Build script to create .exe file for Windows distribution
Run this script on Windows to create the executable
"""
import subprocess
import sys
import os

def main():
    print("=" * 60)
    print("  Building Spanish Municipalities Generator .exe")
    print("=" * 60)
    print()

    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("✓ PyInstaller found")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # Build command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                          # Single .exe file
        "--windowed",                         # No console window
        "--name", "MunicipiosEspana",         # Output name
        "--add-data", "config.py;.",          # Include config
        "--add-data", "src;src",              # Include src folder
        "--icon", "NONE",                     # No icon (or add your .ico file)
        "gui.py"                              # Main script
    ]

    print("\nRunning PyInstaller...")
    print(f"Command: {' '.join(cmd)}")
    print()

    try:
        subprocess.check_call(cmd)
        print()
        print("=" * 60)
        print("  BUILD SUCCESSFUL!")
        print("=" * 60)
        print()
        print("The .exe file is located at:")
        print("  dist/MunicipiosEspana.exe")
        print()
        print("You can distribute this file to the client.")
        print("=" * 60)
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
