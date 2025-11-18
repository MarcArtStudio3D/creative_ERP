#!/usr/bin/env python3
"""
Remove palette-related code from generated UI Python files to allow system themes to work properly.
"""

import sys
import re
import os

def remove_palette_code(content):
    """Remove palette setup code from UI Python file content."""
    lines = content.split('\n')
    result_lines = []
    skip_mode = False
    brace_count = 0
    
    for line in lines:
        # Check if this line starts palette setup
        if re.search(r'\bpalette\s*=\s*QtGui\.QPalette\(\)', line):
            skip_mode = True
            brace_count = 0
            continue
            
        # Also check for direct palette.setColor/setBrush calls
        if re.search(r'\bself\.\w+\.setPalette\(|\.setPalette\(.*QPalette', line):
            # This is a setPalette call - could be problematic for themes
            # Comment it out instead of removing it completely
            result_lines.append('# ' + line.strip())
            continue

        if skip_mode:
            # Count braces to find the end of the palette setup
            brace_count += line.count('{') - line.count('}')
            # Also check for palette.setColor calls
            if re.search(r'\bpalette\.setColor\(', line):
                continue
            # Check for palette.setBrush calls
            if re.search(r'\bpalette\.setBrush\(', line):
                continue
            # Check for widget.setPalette calls
            if re.search(r'\.setPalette\(palette\)', line):
                continue

            # If we find the end of the palette setup (brace count returns to 0)
            if brace_count <= 0 and line.strip():
                skip_mode = False
                continue
            elif brace_count > 0:
                continue

        result_lines.append(line)

    return '\n'.join(result_lines)

def process_file(filepath):
    """Process a single UI Python file to remove palette code."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        content = remove_palette_code(content)

        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False

    except Exception as e:
        print(f"Error processing {filepath}: {e}", file=sys.stderr)
        return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python remove_palette.py <ui_python_file>", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    if process_file(filepath):
        print(f"Removed palette code from {filepath}")
    else:
        print(f"No palette code found in {filepath}")

if __name__ == "__main__":
    main()