import os
import sys


def get_base_path():
    if getattr(sys, "frozen", False):
        return getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    return os.path.dirname(__file__)


def resource_path(*parts):
    return os.path.join(get_base_path(), *parts)


def writable_path(filename):
    if getattr(sys, "frozen", False):
        return os.path.join(os.path.dirname(sys.executable), filename)
    return os.path.join(os.path.dirname(__file__), filename)
