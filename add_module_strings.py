#!/usr/bin/env python3
"""
Script para añadir los strings de módulos (core/modules.py)
a los archivos .ts de traducción.
"""

import xml.etree.ElementTree as ET
from pathlib import Path

# Strings de módulos
MODULE_STRINGS = {
    "Modules": [
        # Nombres de módulos
        "Clientes",
        "Presupuestos",
        "Albaranes",
        "Facturas",
        "Proveedores",
        "Facturas de Compra",
        "Artículos",
        "Almacén",
        "Contabilidad",
        "Tesorería",
        "Proyectos",
        "Control de Tiempo",
        "Empresas",
        "Usuarios",
        "Configuración",
        "Informes",
        "Gestor Módulos",
        
        # Descripciones
        "Gestión de clientes y contactos",
        "Creación de presupuestos",
        "Albaranes de entrega",
        "Emisión y gestión de facturas",
        "Gestión de proveedores",
        "Registro de facturas de proveedores",
        "Catálogo de productos y servicios",
        "Control de inventario y stock",
        "Asientos contables y balance",
        "Gestión de cobros y pagos",
        "Gestión de proyectos creativos",
        "Registro de horas trabajadas",
        "Gestión de empresas y multi-empresa",
        "Gestión de usuarios y permisos",
        "Configuración general del sistema",
        "Informes y estadísticas",
        "Ver módulos y otorgar permisos por rol",
    ],
}

# Traducciones al francés
FRENCH_TRANSLATIONS = {
    # Nombres
    "Clientes": "Clients",
    "Presupuestos": "Devis",
    "Albaranes": "Bons de livraison",
    "Facturas": "Factures",
    "Proveedores": "Fournisseurs",
    "Facturas de Compra": "Factures d'achat",
    "Artículos": "Articles",
    "Almacén": "Entrepôt",
    "Contabilidad": "Comptabilité",
    "Tesorería": "Trésorerie",
    "Proyectos": "Projets",
    "Control de Tiempo": "Contrôle du temps",
    "Empresas": "Entreprises",
    "Usuarios": "Utilisateurs",
    "Configuración": "Configuration",
    "Informes": "Rapports",
    "Gestor Módulos": "Gestionnaire de modules",
    
    # Descripciones
    "Gestión de clientes y contactos": "Gestion des clients et contacts",
    "Creación de presupuestos": "Création de devis",
    "Albaranes de entrega": "Bons de livraison",
    "Emisión y gestión de facturas": "Émission et gestion de factures",
    "Gestión de proveedores": "Gestion des fournisseurs",
    "Registro de facturas de proveedores": "Enregistrement des factures fournisseurs",
    "Catálogo de productos y servicios": "Catalogue de produits et services",
    "Control de inventario y stock": "Contrôle d'inventaire et de stock",
    "Asientos contables y balance": "Écritures comptables et bilan",
    "Gestión de cobros y pagos": "Gestion des encaissements et paiements",
    "Gestión de proyectos creativos": "Gestion de projets créatifs",
    "Registro de horas trabajadas": "Enregistrement des heures travaillées",
    "Gestión de empresas y multi-empresa": "Gestion d'entreprises et multi-entreprise",
    "Gestión de usuarios y permisos": "Gestion des utilisateurs et permissions",
    "Configuración general del sistema": "Configuration générale du système",
    "Informes y estadísticas": "Rapports et statistiques",
    "Ver módulos y otorgar permisos por rol": "Voir modules et attribuer permissions par rôle",
}


def add_strings_to_ts(ts_file: Path, lang_code: str):
    """Añade los nuevos strings al archivo .ts"""
    
    # Parsear el archivo XML
    tree = ET.parse(ts_file)
    root = tree.getroot()
    
    added_count = 0
    
    # Para cada contexto (clase)
    for context_name, strings in MODULE_STRINGS.items():
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
    print("Añadiendo strings de módulos (core/modules.py)")
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
