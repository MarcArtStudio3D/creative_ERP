#!/usr/bin/env python3
"""
Script mejorado para extraer TODOS los strings literales del código
y crear archivos de traducción .ts

Este script extrae strings de:
- QLabel("texto")
- QPushButton("texto")
- setWindowTitle("texto")
- setText("texto")
- Y otros métodos comunes de Qt

Uso: python scripts/extract_all_strings.py
"""

import os
import xml.etree.ElementTree as ET
from pathlib import Path
import re
from typing import List, Set, Tuple, Dict
from collections import defaultdict


def extract_all_strings(file_path: Path) -> Dict[str, Set[str]]:
    """
    Extrae TODOS los strings literales de un archivo Python que parecen
    ser texto de interfaz de usuario.
    
    Returns:
        Dict con contexto (nombre de clase) como clave y set de strings como valor
    """
    strings_by_context = defaultdict(set)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Buscar definiciones de clase para contexto
        class_pattern = r'class\s+(\w+)\s*\('
        classes = re.findall(class_pattern, content)
        current_class = classes[0] if classes else file_path.stem
        
        # Patrones para encontrar strings en métodos de Qt
        patterns = [
            # QLabel, QPushButton, etc con texto
            r'Q(?:Label|PushButton|Action|Menu|MessageBox|CheckBox|RadioButton|GroupBox|TabWidget|ToolButton|LineEdit)\s*\(\s*["\']([^"\']+)["\']\s*[,\)]',
            # setWindowTitle, setText, setStatusTip, etc
            r'set(?:WindowTitle|Text|StatusTip|ToolTip|PlaceholderText|Title)\s*\(\s*["\']([^"\']+)["\']\s*\)',
            # addMenu, addAction
            r'add(?:Menu|Action|Tab|Item)\s*\(\s*["\']([^"\']+)["\']\s*[,\)]',
            # showMessage
            r'showMessage\s*\(\s*["\']([^"\']+)["\']\s*[,\)]',
            # Diccionarios con "name", "description", etc
            r'["\'](?:name|description|icon)["\']:\s*["\']([^"\']+)["\']',
            # f-strings y format strings (capturar la parte fija)
            r'f["\']([^{}"\']+)["\']',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                # Filtrar strings que no son texto de UI
                if match and len(match) > 1 and not match.startswith('_'):
                    # Ignorar rutas de archivo, URLs, etc
                    if not any(x in match for x in ['/', '\\', 'http', '.py', '.ui', '.qm', '.ts']):
                        # Ignorar strings técnicos
                        if not match.startswith(('rgb', '#', 'palette', 'Q')):
                            strings_by_context[current_class].add(match)
        
    except Exception as e:
        print(f"Error procesando {file_path}: {e}")
    
    return dict(strings_by_context)


def create_ts_file(output_path: Path, language: str, source_files: List[Path]):
    """
    Crea un archivo .ts de Qt con las traducciones extraídas.
    
    Args:
        output_path: Ruta del archivo .ts a crear
        language: Código de idioma (ej: 'es', 'en', 'ca')
        source_files: Lista de archivos Python a procesar
    """
    # Crear elemento raíz
    root = ET.Element('TS')
    root.set('version', '2.1')
    root.set('language', language)
    
    # Agrupar strings por contexto
    all_contexts = {}
    
    for source_file in source_files:
        file_contexts = extract_all_strings(source_file)
        for context, strings in file_contexts.items():
            if context not in all_contexts:
                all_contexts[context] = set()
            all_contexts[context].update(strings)
    
    if not all_contexts:
        print(f"  ⚠ No se encontraron strings para traducir")
        # Crear archivo vacío válido
        tree = ET.ElementTree(root)
        ET.indent(tree, space='    ')
        with open(output_path, 'wb') as f:
            f.write(b'<?xml version="1.0" encoding="utf-8"?>\n')
            f.write(b'<!DOCTYPE TS>\n')
            tree.write(f, encoding='utf-8', xml_declaration=False)
        return
    
    # Crear elementos de contexto
    for context_name, texts in sorted(all_contexts.items()):
        context_elem = ET.SubElement(root, 'context')
        
        name_elem = ET.SubElement(context_elem, 'name')
        name_elem.text = context_name
        
        for text in sorted(texts):
            message_elem = ET.SubElement(context_elem, 'message')
            
            source_elem = ET.SubElement(message_elem, 'source')
            source_elem.text = text
            
            translation_elem = ET.SubElement(message_elem, 'translation')
            
            # Para español, dejar como está (ya está en español)
            # Para otros idiomas, marcar como no traducido
            if language == 'es':
                translation_elem.text = text
            else:
                translation_elem.set('type', 'unfinished')
                translation_elem.text = ''
    
    # Crear árbol y guardar
    tree = ET.ElementTree(root)
    ET.indent(tree, space='    ')
    
    with open(output_path, 'wb') as f:
        f.write(b'<?xml version="1.0" encoding="utf-8"?>\n')
        f.write(b'<!DOCTYPE TS>\n')
        tree.write(f, encoding='utf-8', xml_declaration=False)
    
    total_strings = sum(len(texts) for texts in all_contexts.values())
    print(f"  ✓ {total_strings} strings encontrados en {len(all_contexts)} contextos")


def main():
    print("=" * 60)
    print("Extrayendo strings de interfaz de usuario")
    print("=" * 60)
    
    # Obtener directorio raíz del proyecto
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # Crear directorio de traducciones
    translations_dir = project_root / "translations"
    translations_dir.mkdir(exist_ok=True)
    
    # Leer archivos fuente del .pro
    pro_file = project_root / "creative_erp.pro"
    source_files = []
    
    if pro_file.exists():
        with open(pro_file, 'r') as f:
            content = f.read()
            # Extraer rutas de SOURCES
            sources_match = re.search(r'SOURCES\s*=\s*(.*?)(?=TRANSLATIONS|$)', content, re.DOTALL)
            if sources_match:
                sources_text = sources_match.group(1)
                # Extraer cada archivo
                file_pattern = r'([a-zA-Z0-9_/]+\.py)'
                files = re.findall(file_pattern, sources_text)
                for file_path in files:
                    full_path = project_root / file_path
                    if full_path.exists():
                        source_files.append(full_path)
    
    if not source_files:
        print("No se encontraron archivos fuente en creative_erp.pro")
        return
    
    print(f"\nProcesando {len(source_files)} archivos fuente...\n")
    
    # Crear archivos .ts para cada idioma
    languages = {
        'es': 'Español',
        'en': 'English',
        'ca': 'Català',
        'fr': 'Français'
    }
    
    for lang_code, lang_name in languages.items():
        output_file = translations_dir / f"creative_erp_{lang_code}.ts"
        print(f"Generando {lang_name} ({lang_code})...")
        create_ts_file(output_file, lang_code, source_files)
    
    print("\n" + "=" * 60)
    print("Archivos .ts creados en translations/")
    print("=" * 60)
    print("\nPróximos pasos:")
    print("1. Revisa los archivos .ts generados")
    print("2. Edita las traducciones con Qt Linguist:")
    print("   linguist translations/creative_erp_en.ts")
    print("\n3. O edítalos manualmente con cualquier editor de texto")
    print("\n4. Compila las traducciones con:")
    print("   python scripts/compile_translations.py")
    print()

if __name__ == "__main__":
    main()
