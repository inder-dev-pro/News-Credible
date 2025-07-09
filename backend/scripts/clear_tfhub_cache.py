#!/usr/bin/env python3
"""
Script to clear TensorFlow Hub cache to resolve model loading issues.
Run this script if you encounter TensorFlow Hub model loading errors.
"""

import os
import shutil
import sys
from pathlib import Path

def clear_tfhub_cache():
    """Clear TensorFlow Hub cache directories"""
    
    # Common TensorFlow Hub cache locations
    cache_locations = [
        os.path.expanduser("~/.cache/tfhub_modules"),
        os.path.expanduser("~/.cache/tensorflow/hub"),
        os.path.expanduser("~/.local/share/tensorflow/hub"),
        "/tmp/tfhub_modules",
        "C:/Users/dell/AppData/Local/Temp/tfhub_modules"
    ]
    
    cleared_count = 0
    
    for cache_dir in cache_locations:
        if os.path.exists(cache_dir):
            try:
                print(f"Clearing cache directory: {cache_dir}")
                shutil.rmtree(cache_dir)
                print(f"✓ Successfully cleared: {cache_dir}")
                cleared_count += 1
            except Exception as e:
                print(f"✗ Failed to clear {cache_dir}: {str(e)}")
    
    if cleared_count == 0:
        print("No TensorFlow Hub cache directories found to clear.")
    else:
        print(f"\nCleared {cleared_count} cache directory(ies).")
        print("You can now restart your application and the models should load properly.")

def main():
    print("TensorFlow Hub Cache Cleaner")
    print("=" * 30)
    
    # Check if running on Windows
    if sys.platform.startswith('win'):
        print("Detected Windows system")
    
    clear_tfhub_cache()
    
    print("\nCache clearing completed!")
    print("If you still experience issues, try:")
    print("1. Restarting your application")
    print("2. Checking your internet connection")
    print("3. Verifying your TensorFlow installation")

if __name__ == "__main__":
    main() 