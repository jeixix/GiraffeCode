"""
GiraffeCode / SavannaCode
A playful educational coding game for children aged 5-9.
"""
import sys
import os

# Add the project root to sys.path so 'from src.X' imports work correctly
# whether run as `python src/main.py` or via PyInstaller.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.game import main_wrapper

if __name__ == "__main__":
    main_wrapper()
