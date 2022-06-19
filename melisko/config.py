from pathlib import Path
import os

def root_dir():
    return Path(os.path.dirname(os.path.abspath(__file__)))