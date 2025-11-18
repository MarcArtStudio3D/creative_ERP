#!/usr/bin/env python3
"""
Script to fix Qt constants in generated UI files for better Pylance compatibility.

This script replaces abbreviated Qt constants with their full enum forms that Pylance
recognizes correctly.

Usage: python fix_qt_constants.py <ui_file.py>
"""

import sys
import re
import os

# Mapping of Qt constants that need to be fixed
QT_CONSTANT_FIXES = {
    # Qt constants
    r'\bQt\.WindowModal\b': 'Qt.WindowModality.WindowModal',
    r'\bQt\.AlignCenter\b': 'Qt.AlignmentFlag.AlignCenter',
    r'\bQt\.Horizontal\b': 'Qt.Orientation.Horizontal',
    r'\bQt\.Vertical\b': 'Qt.Orientation.Vertical',

    # QFrame constants
    r'\bQFrame\.StyledPanel\b': 'QFrame.Shape.StyledPanel',
    r'\bQFrame\.Raised\b': 'QFrame.Shadow.Raised',
    r'\bQFrame\.Sunken\b': 'QFrame.Shadow.Sunken',

    # QAbstractItemView constants
    r'\bQAbstractItemView\.SingleSelection\b': 'QAbstractItemView.SelectionMode.SingleSelection',
    r'\bQAbstractItemView\.MultiSelection\b': 'QAbstractItemView.SelectionMode.MultiSelection',
    r'\bQAbstractItemView\.SelectRows\b': 'QAbstractItemView.SelectionBehavior.SelectRows',
    r'\bQAbstractItemView\.SelectColumns\b': 'QAbstractItemView.SelectionBehavior.SelectColumns',
    r'\bQAbstractItemView\.SelectItems\b': 'QAbstractItemView.SelectionBehavior.SelectItems',

    # QDialog constants
    r'\bQDialog\.Accepted\b': 'QDialog.DialogCode.Accepted',
    r'\bQDialog\.Rejected\b': 'QDialog.DialogCode.Rejected',

    # QEvent constants
    r'\bQEvent\.KeyPress\b': 'QEvent.Type.KeyPress',
    r'\bQEvent\.KeyRelease\b': 'QEvent.Type.KeyRelease',
    r'\bQEvent\.MouseButtonPress\b': 'QEvent.Type.MouseButtonPress',
    r'\bQEvent\.MouseButtonRelease\b': 'QEvent.Type.MouseButtonRelease',

    # Qt Key constants
    r'\bQt\.Key_Return\b': 'Qt.Key.Key_Return',
    r'\bQt\.Key_Enter\b': 'Qt.Key.Key_Enter',
    r'\bQt\.Key_Tab\b': 'Qt.Key.Key_Tab',
    r'\bQt\.Key_Backspace\b': 'Qt.Key.Key_Backspace',
    r'\bQt\.Key_Escape\b': 'Qt.Key.Key_Escape',
}

def fix_qt_constants_in_file(filepath):
    """Fix Qt constants in a single file."""
    print(f"Fixing Qt constants in: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Apply all fixes
    for pattern, replacement in QT_CONSTANT_FIXES.items():
        content = re.sub(pattern, replacement, content)

    # Write back only if content changed
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Fixed {len([m for m in re.finditer('|'.join(QT_CONSTANT_FIXES.keys()), original_content)])} Qt constants")
        return True
    else:
        print("  ✓ No Qt constants needed fixing")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python fix_qt_constants.py <ui_file.py> [ui_file2.py ...]")
        sys.exit(1)

    total_fixed = 0
    for filepath in sys.argv[1:]:
        if not os.path.exists(filepath):
            print(f"Error: File not found: {filepath}")
            continue

        if fix_qt_constants_in_file(filepath):
            total_fixed += 1

    print(f"\nFixed Qt constants in {total_fixed} files.")

if __name__ == '__main__':
    main()