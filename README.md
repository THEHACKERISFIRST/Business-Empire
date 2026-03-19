# Business-Empire
This is a clicker game where you can buy businesses and crypto.

## Run from source

1. Create and activate a Python 3.12 virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Start the game with `python main.py`.

## Build a release

Use the included build script so the asset paths work on both Windows and macOS:

`python build_release.py`

### Windows output

Running the build on Windows creates:

`dist/BusinessEmpire.exe`

### macOS output

Running the build on a Mac creates:

`dist/BusinessEmpire.app`

PyInstaller cannot reliably build the Mac app from Windows. You need to run `python build_release.py` on a Mac to generate the `.app`.

## Save data

Save files are stored in the platform's user data folder:

- Windows: `%APPDATA%\\BusinessEmpire\\save_data.json`
- macOS: `~/Library/Application Support/BusinessEmpire/save_data.json`

Older save files next to the source folder or executable are still detected and loaded.

If you want to play this game.
You have to have an IDE like VS code or Pycharm Community.
Download as zip in code (top right. its a green button.)
unzip the file.
import the file into the IDE.
if needed download pygame (its a package from inside the IDE)
run main.py
