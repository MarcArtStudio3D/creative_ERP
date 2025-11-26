#!/usr/bin/env python3
"""
Script para generar archivos de traducción manualmente.
Crea archivos .ts básicos que pueden ser editados con Qt Linguist.

Uso: python scripts/create_translation_files.py
"""

import os
import xml.etree.ElementTree as ET
from pathlib import Path
import re
from typing import List, Set, Tuple

def extract_tr_strings(file_path: Path) -> Set[Tuple[str, str]]:
    """
    Extrae strings marcadas con tr() o self.tr() de un archivo Python.
    
    Returns:
        Set de tuplas (contexto, texto) donde contexto es el nombre de la clase
    """
    strings = set()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Buscar definiciones de clase para contexto
        class_pattern = r'class\s+(\w+)\s*\('
        classes = re.findall(class_pattern, content)
        current_class = classes[0] if classes else file_path.stem
        
        # Patrones para encontrar strings traducibles
        # Patrón 1: self.tr("texto")
        pattern1 = r'self\.tr\(["\']([^"\']+)["\']\)'
        # Patrón 2: tr("texto")
        pattern2 = r'(?<!self\.)tr\(["\']([^"\']+)["\']\)'
        # Patrón 3: QCoreApplication.translate("context", "texto")
        pattern3 = r'QCoreApplication\.translate\(["\']([^"\']+)["\']\s*,\s*["\']([^"\']+)["\']\)'
        
        # Extraer con patrón 1 y 2
        for pattern in [pattern1, pattern2]:
            matches = re.findall(pattern, content)
            for match in matches:
                strings.add((current_class, match))
        
        # Extraer con patrón 3 (tiene contexto explícito)
        matches = re.findall(pattern3, content)
        for context, text in matches:
            strings.add((context, text))
            
    except Exception as e:
        print(f"Error procesando {file_path}: {e}")
    
    return strings

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
    contexts = {}
    
    for source_file in source_files:
        strings = extract_tr_strings(source_file)
        for context, text in strings:
            if context not in contexts:
                contexts[context] = set()
            contexts[context].add(text)
    
    # Crear elementos de contexto
    for context_name, texts in sorted(contexts.items()):
        context_elem = ET.SubElement(root, 'context')
        
        name_elem = ET.SubElement(context_elem, 'name')
        name_elem.text = context_name
        
        for text in sorted(texts):
            message_elem = ET.SubElement(context_elem, 'message')
            
            source_elem = ET.SubElement(message_elem, 'source')
            source_elem.text = text
            
            translation_elem = ET.SubElement(message_elem, 'translation')
            translation_elem.set('type', 'unfinished')
            translation_elem.text = ''
    
    # Crear árbol y guardar
    tree = ET.ElementTree(root)
    ET.indent(tree, space='    ')
    
    with open(output_path, 'wb') as f:
        f.write(b'<?xml version="1.0" encoding="utf-8"?>\n')
        f.write(b'<!DOCTYPE TS>\n')
        tree.write(f, encoding='utf-8', xml_declaration=False)
    
    print(f"✓ Creado: {output_path}")

def main():
    print("=" * 60)
    print("Creando archivos de traducción manualmente")
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
        'ca': 'Català'
    }
    
    for lang_code, lang_name in languages.items():
        output_file = translations_dir / f"creative_erp_{lang_code}.ts"
        print(f"Generando {lang_name} ({lang_code})...")
        create_ts_file(output_file, lang_code, source_files)
    
    print("\n" + "=" * 60)
    print("Archivos .ts creados en translations/")
    print("=" * 60)
    print("\nPróximos pasos:")
    print("1. Edita los archivos .ts con Qt Linguist:")
    print("   linguist translations/creative_erp_es.ts")
    print("\n2. O edítalos manualmente con cualquier editor de texto")
    print("\n3. Compila las traducciones con:")
    print("   python scripts/compile_translations.py")
    print()

if __name__ == "__main__":
    main()
