"""
SavannaCode / GiraffeCode
Root entry point for Android (Buildozer) and Desktop execution.
"""
import sys
import os

# Ensure the root directory is at the front of sys.path
root_dir = os.path.dirname(os.path.abspath(__file__))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from src.game import main_wrapper

if __name__ == "__main__":
    main_wrapper()
