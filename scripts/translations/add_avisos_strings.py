#!/usr/bin/env python3
"""
Script para añadir los strings del panel de avisos y barra de estado
a los archivos .ts de traducción.
"""

import xml.etree.ElementTree as ET
from pathlib import Path

# Strings del panel de avisos y barra de estado
AVISOS_STRINGS = {
    "MainWindowV2": [
        "⚠️ AVISOS",
        "✓ Sin Avisos",
        "No hay avisos pendientes",
        "AVISOS",
        "Usuario",
        "Rol",
    ],
}

# Traducciones al francés
FRENCH_TRANSLATIONS = {
    "⚠️ AVISOS": "⚠️ AVIS",
    "✓ Sin Avisos": "✓ Sans Avis",
    "No hay avisos pendientes": "Aucun avis en attente",
    "AVISOS": "AVIS",
    "Usuario": "Utilisateur",
    "Rol": "Rôle",
}


def add_strings_to_ts(ts_file: Path, lang_code: str):
    """Añade los nuevos strings al archivo .ts"""
    
    # Parsear el archivo XML
    tree = ET.parse(ts_file)
    root = tree.getroot()
    
    added_count = 0
    
    # Para cada contexto (clase)
    for context_name, strings in AVISOS_STRINGS.items():
        # Buscar si el contexto ya existe
        context = None
        for ctx in root.findall('context'):
            name_elem = ctx.find('name')
            if name_elem is not None and name_elem.text == context_name:
                context = ctx
                break
        
        # Si no existe, crear el contexto
        if context is None:
            context = ET.SubElement(root, 'context')
            name_elem = ET.SubElement(context, 'name')
            name_elem.text = context_name
        
        # Para cada string
        for source_text in strings:
            # Verificar si ya existe
            exists = False
            for msg in context.findall('message'):
                source_elem = msg.find('source')
                if source_elem is not None and source_elem.text == source_text:
                    exists = True
                    break
            
            # Si no existe, añadirlo
            if not exists:
                message = ET.SubElement(context, 'message')
                source = ET.SubElement(message, 'source')
                source.text = source_text
                
                translation = ET.SubElement(message, 'translation')
                
                # Si es francés y tenemos traducción, añadirla
                if lang_code == 'fr' and source_text in FRENCH_TRANSLATIONS:
                    translation.text = FRENCH_TRANSLATIONS[source_text]
                else:
                    translation.set('type', 'unfinished')
                
                added_count += 1
    
    # Guardar el archivo
    tree.write(ts_file, encoding='utf-8', xml_declaration=True)
    
    return added_count


def main():
    ts_files = {
        'es': Path('translations/creative_erp_es.ts'),
        'en': Path('translations/creative_erp_en.ts'),
        'ca': Path('translations/creative_erp_ca.ts'),
        'fr': Path('translations/creative_erp_fr.ts'),
    }
    
    print("=" * 60)
    print("Añadiendo strings de panel de avisos y barra de estado")
    print("=" * 60)
    
    for lang_code, ts_file in ts_files.items():
        if ts_file.exists():
            count = add_strings_to_ts(ts_file, lang_code)
            status = "✓" if lang_code == 'fr' else "○"
            print(f"{status} {ts_file.name}: {count} strings añadidos")
    
    print("\n✓ Archivos .ts actualizados")
    print("\nPróximo paso:")
    print("  python scripts/compile_translations.py")


if __name__ == "__main__":
    main()
