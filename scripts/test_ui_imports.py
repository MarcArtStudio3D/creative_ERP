#!/usr/bin/env python3
"""
Unit tests to verify that compiled UI files can be imported correctly.

This script tests all generated UI files to ensure they import without errors
and that their classes can be instantiated.
"""

import sys
import os
import importlib
import traceback
from pathlib import Path

def find_ui_files(root_dir):
    """Find all generated UI Python files."""
    ui_files = []
    for py_file in Path(root_dir).rglob('ui_*.py'):
        if py_file.is_file():
            ui_files.append(py_file)
    return sorted(ui_files)

def test_ui_import(ui_file_path):
    """Test importing a single UI file."""
    try:
        # Get module name from file path relative to project root
        rel_path = os.path.relpath(ui_file_path)
        module_name = rel_path.replace('/', '.').replace('\\', '.').replace('.py', '')

        # Import the module
        module = importlib.import_module(module_name)

        # Find UI classes (they start with 'Ui_')
        ui_classes = [obj for name, obj in vars(module).items()
                     if name.startswith('Ui_') and isinstance(obj, type)]

        if not ui_classes:
            return False, f"No UI classes found in {ui_file_path}"

        # Test instantiating each UI class (without calling setupUi to avoid Qt dependencies)
        for ui_class in ui_classes:
            try:
                instance = ui_class()
                # Just check that the instance was created and has expected attributes
                if not hasattr(instance, 'setupUi'):
                    return False, f"UI class {ui_class.__name__} missing setupUi method"
            except Exception as e:
                return False, f"Failed to instantiate {ui_class.__name__}: {e}"

        return True, f"Successfully imported and tested {len(ui_classes)} UI classes"

    except Exception as e:
        return False, f"Import failed: {e}"

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_ui_imports.py <root_directory>")
        sys.exit(1)

    root_dir = sys.argv[1]
    if not os.path.exists(root_dir):
        print(f"Error: Directory not found: {root_dir}")
        sys.exit(1)

    # Add project root to Python path
    if root_dir not in sys.path:
        sys.path.insert(0, root_dir)

    print(f"Testing UI imports in: {root_dir}")
    print("=" * 60)

    ui_files = find_ui_files(root_dir)
    if not ui_files:
        print("No UI files found.")
        return

    print(f"Found {len(ui_files)} UI files to test:")
    for ui_file in ui_files:
        print(f"  - {ui_file}")
    print()

    passed = 0
    failed = 0

    for ui_file in ui_files:
        print(f"Testing: {os.path.basename(ui_file)}")
        success, message = test_ui_import(ui_file)

        if success:
            print(f"  ✓ PASS: {message}")
            passed += 1
        else:
            print(f"  ✗ FAIL: {message}")
            failed += 1
        print()

    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")

    if failed > 0:
        print("\nFailed tests:")
        # Re-run failed tests with full traceback
        for ui_file in ui_files:
            success, message = test_ui_import(ui_file)
            if not success:
                print(f"\n{os.path.basename(ui_file)}:")
                print(f"  Error: {message}")
                # Print full traceback if available
                if "Import failed" in message:
                    try:
                        test_ui_import(ui_file)  # This will trigger the exception again
                    except Exception:
                        traceback.print_exc()

        sys.exit(1)
    else:
        print("All UI imports successful! 🎉")

if __name__ == '__main__':
    main()