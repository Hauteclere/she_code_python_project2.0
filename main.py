#!/usr/bin/env python3
"""
Entry point for She Codes Weather application.
"""
import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from she_codes_weather.main import run

if __name__ == "__main__":
    run()