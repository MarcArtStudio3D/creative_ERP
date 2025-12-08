#!/usr/bin/env python3
"""
Script para añadir los strings adicionales de main_window_v2.py
a los archivos .ts de traducción.
"""

import xml.etree.ElementTree as ET
from pathlib import Path

# Nuevos strings adicionales para MainWindowV2
ADDITIONAL_STRINGS = {
    "MainWindowV2": [
        # Categorías
        "Ventas",
        "Compras",
        "Almacén",
        "Financiero",
        "Proyectos",
        "Administración",
        # Descripciones
        "Gestión de clientes y facturación",
        "Proveedores y facturas de compra",
        "Inventario y control de stock",
        "Contabilidad y tesorería",
        "Gestión de proyectos creativos",
        "Configuración y usuarios",
        # UI
        "MÓDULOS",
        "Ver módulos",
        "Bienvenido, {}",
        "Selecciona un módulo del menú superior para comenzar",
        # Menús
        "Utilidades",
        "Preferencias",
        "Acerca de",
        "Sesión",
        "Cambiar Empresa",
        "Cerrar Sesión",
    ],
}

# Traducciones al francés
FRENCH_TRANSLATIONS = {
    # Categorías
    "Ventas": "Ventes",
    "Compras": "Achats",
    "Almacén": "Entrepôt",
    "Financiero": "Financier",
    "Proyectos": "Projets",
    "Administración": "Administration",
    # Descripciones
    "Gestión de clientes y facturación": "Gestion des clients et facturation",
    "Proveedores y facturas de compra": "Fournisseurs et factures d'achat",
    "Inventario y control de stock": "Inventaire et contrôle de stock",
    "Contabilidad y tesorería": "Comptabilité et trésorerie",
    "Gestión de proyectos creativos": "Gestion de projets créatifs",
    "Configuración y usuarios": "Configuration et utilisateurs",
    # UI
    "MÓDULOS": "MODULES",
    "Ver módulos": "Voir modules",
    "Bienvenido, {}": "Bienvenue, {}",
    "Selecciona un módulo del menú superior para comenzar": "Sélectionnez un module du menu supérieur pour commencer",
    # Menús
    "Utilidades": "Utilitaires",
    "Preferencias": "Préférences",
    "Acerca de": "À propos",
    "Sesión": "Session",
    "Cambiar Empresa": "Changer d'entreprise",
    "Cerrar Sesión": "Fermer la session",
}


def add_strings_to_ts(ts_file: Path, lang_code: str):
    """Añade los nuevos strings al archivo .ts"""

    # Parsear el archivo XML
    tree = ET.parse(ts_file)
    root = tree.getroot()

    added_count = 0

    # Para cada contexto (clase)
    for context_name, strings in ADDITIONAL_STRINGS.items():
        # Buscar si el contexto ya existe
        context = None
        for ctx in root.findall("context"):
            name_elem = ctx.find("name")
            if name_elem is not None and name_elem.text == context_name:
                context = ctx
                break

        # Si no existe, crear el contexto
        if context is None:
            context = ET.SubElement(root, "context")
            name_elem = ET.SubElement(context, "name")
            name_elem.text = context_name

        # Para cada string
        for source_text in strings:
            # Verificar si ya existe
            exists = False
            for msg in context.findall("message"):
                source_elem = msg.find("source")
                if source_elem is not None and source_elem.text == source_text:
                    exists = True
                    break

            # Si no existe, añadirlo
            if not exists:
                message = ET.SubElement(context, "message")
                source = ET.SubElement(message, "source")
                source.text = source_text

                translation = ET.SubElement(message, "translation")

                # Si es francés y tenemos traducción, añadirla
                if lang_code == "fr" and source_text in FRENCH_TRANSLATIONS:
                    translation.text = FRENCH_TRANSLATIONS[source_text]
                else:
                    translation.set("type", "unfinished")

                added_count += 1

    # Guardar el archivo
    tree.write(ts_file, encoding="utf-8", xml_declaration=True)

    return added_count


def main():
    ts_files = {
        "es": Path("translations/creative_erp_es.ts"),
        "en": Path("translations/creative_erp_en.ts"),
        "ca": Path("translations/creative_erp_ca.ts"),
        "fr": Path("translations/creative_erp_fr.ts"),
    }

    print("=" * 60)
    print("Añadiendo strings adicionales de main_window")
    print("=" * 60)

    for lang_code, ts_file in ts_files.items():
        if ts_file.exists():
            count = add_strings_to_ts(ts_file, lang_code)
            status = "OK" if lang_code == "fr" else "-"
            print(f"{status} {ts_file.name}: {count} strings añadidos")

    print("\nTranslation files updated")
    print("\nPróximo paso:")
    print("  python scripts/compile_translations.py")


if __name__ == "__main__":
    main()
