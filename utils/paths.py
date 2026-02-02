import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def asset(name):
    return os.path.join(BASE_DIR, "assets", name)

def rapport(name):
    return os.path.join(BASE_DIR, "rapport", name)
