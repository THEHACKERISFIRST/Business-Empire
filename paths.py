import os
import sys

APP_NAME = "BusinessEmpire"


def get_base_path():
    if getattr(sys, "frozen", False):
        return getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    return os.path.dirname(__file__)


def resource_path(*parts):
    return os.path.join(get_base_path(), *parts)


def get_app_data_dir():
    if sys.platform == "darwin":
        base_dir = os.path.join(os.path.expanduser("~"), "Library", "Application Support")
    elif os.name == "nt":
        base_dir = os.environ.get("APPDATA", os.path.expanduser("~"))
    else:
        base_dir = os.environ.get("XDG_DATA_HOME", os.path.join(os.path.expanduser("~"), ".local", "share"))

    app_dir = os.path.join(base_dir, APP_NAME)
    os.makedirs(app_dir, exist_ok=True)
    return app_dir


def writable_path(filename):
    return os.path.join(get_app_data_dir(), filename)


def legacy_writable_paths(filename):
    legacy_paths = []
    if getattr(sys, "frozen", False):
        legacy_paths.append(os.path.join(os.path.dirname(sys.executable), filename))
    legacy_paths.append(os.path.join(os.path.dirname(__file__), filename))
    return legacy_paths
