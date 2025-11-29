#!/usr/bin/env python3
"""
Script para eliminar colores hardcodeados de los archivos UI generados y dejar solo
colores alternativos neutros como en clientes y empresas modernos.
"""

import sys
import re
import os

def clean_hardcoded_colors(content):
    """Remove hardcoded background colors from UI Python file content."""
    # First, handle multiline setStyleSheet cases with regex
    # Remove background-color from multiline strings like:
    # setStyleSheet(u"color: rgb(0, 0, 0);\n"
    # "background-color: rgb(239, 239, 239);")
    content = re.sub(
        r'"background-color: rgb\(\d+,\s*\d+,\s*\d+\);"',
        '""',
        content
    )
    
    # Clean up extra newlines left after removing background colors
    content = re.sub(r'\\n"\s*\n""', '"', content)
    content = re.sub(r';\s*\\n"\s*\n""', ';"', content)
    
    # Handle complete setStyleSheet replacements for problematic cases
    # Replace entire setStyleSheet calls that only contain background-color
    content = re.sub(
        r'(\s+)(\w+)\.setStyleSheet\(u"background-color: rgb\(\d+,\s*\d+,\s*\d+\);\s*\\n"\s*\n"[^"]*"\)',
        r'\1# \2.setStyleSheet(...) # Removed hardcoded background color',
        content
    )
    
    # Now process line by line for remaining cases
    lines = content.split('\n')
    result_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check for setStyleSheet with background-color
        if 'setStyleSheet' in line and 'background-color: rgb(' in line:
            # Keep only alternate-background-color and font settings
            if 'alternate-background-color' in line:
                # Clean the style to keep only alternating and font
                new_line = re.sub(r'background-color: rgb\(\d+,\s*\d+,\s*\d+\);?\s*', '', line)
                result_lines.append(new_line)
            else:
                # Check if it's a multiline setStyleSheet that we need to comment out entirely
                if line.strip().endswith('\\n"') and i + 1 < len(lines):
                    next_line = lines[i + 1]
                    if 'background-color: rgb(' in next_line and next_line.strip().endswith('")'):
                        # Comment out both lines
                        result_lines.append('        # ' + line.strip() + ' # Removed hardcoded background color')
                        result_lines.append('        # ' + next_line.strip() + ' # Removed hardcoded background color')
                        i += 1  # Skip the next line since we processed it
                    else:
                        result_lines.append(line)
                else:
                    # Single line case - comment it out
                    result_lines.append('        # ' + line.strip() + ' # Removed hardcoded background color')
        else:
            result_lines.append(line)
        
        i += 1
    
    return '\n'.join(result_lines)

def process_file(filepath):
    """Process a single UI Python file to remove hardcoded colors."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        content = clean_hardcoded_colors(content)

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
        print("Usage: python clean_ui_colors.py <ui_python_file>", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    if process_file(filepath):
        print(f"Cleaned hardcoded colors from {filepath}")
    else:
        print(f"No hardcoded colors found in {filepath}")

if __name__ == "__main__":
    main()