import os
import shutil
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
DIST_DIR = PROJECT_ROOT / "dist"
BUILD_DIR = PROJECT_ROOT / "build"
SPEC_PATH = PROJECT_ROOT / "BusinessEmpire.spec"
APP_NAME = "BusinessEmpire"


def build_add_data_args():
    separator = os.pathsep
    data_mappings = [
        ("BusinessEmpireLogo.jpg", "."),
        ("ClickMeIcon.png", "."),
        ("images", "images"),
    ]

    args = []
    for source, target in data_mappings:
        args.extend(["--add-data", f"{source}{separator}{target}"])
    return args


def main():
    for path in (DIST_DIR, BUILD_DIR):
        if path.exists():
            shutil.rmtree(path)

    if SPEC_PATH.exists():
        SPEC_PATH.unlink()

    command = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--windowed",
        "--name",
        APP_NAME,
        *build_add_data_args(),
        "main.py",
    ]

    if sys.platform == "win32":
        command.insert(4, "--onefile")

    subprocess.run(command, cwd=PROJECT_ROOT, check=True)

    if sys.platform == "darwin":
        app_path = DIST_DIR / f"{APP_NAME}.app"
        print(f"Built macOS app: {app_path}")
    elif sys.platform == "win32":
        exe_path = DIST_DIR / f"{APP_NAME}.exe"
        print(f"Built Windows executable: {exe_path}")
    else:
        print(f"Built release in: {DIST_DIR}")


if __name__ == "__main__":
    main()
