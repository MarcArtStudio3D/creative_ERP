"""
Módulo de gestión de traducciones para Creative ERP.

Este módulo proporciona funciones para cargar y cambiar el idioma
de la aplicación en tiempo de ejecución.

Uso:
    from core.translations import load_translation, available_languages
    
    # Cargar traducción al iniciar la app
    translator = load_translation(app, 'es')
    
    # Cambiar idioma en tiempo de ejecución
    change_language(app, translator, 'en')
"""

from pathlib import Path
from typing import Optional
from PySide6.QtCore import QTranslator, QCoreApplication, QLocale
from PySide6.QtWidgets import QApplication


# Directorio de traducciones
TRANSLATIONS_DIR = Path(__file__).parent.parent / "translations"

# Idiomas disponibles
AVAILABLE_LANGUAGES = {
    'es': 'Español',
    'en': 'English',
    'ca': 'Català',
    'fr': 'Français',
}


def get_system_language() -> str:
    """
    Obtiene el idioma del sistema.
    
    Returns:
        Código de idioma (ej: 'es', 'en', 'ca')
    """
    system_locale = QLocale.system()
    language_code = system_locale.name().split('_')[0]
    
    # Si el idioma del sistema está disponible, usarlo
    if language_code in AVAILABLE_LANGUAGES:
        return language_code
    
    # Por defecto, español
    return 'es'


def load_translation(app: QCoreApplication, language: Optional[str] = None) -> Optional[QTranslator]:
    """
    Carga un archivo de traducción.
    
    Args:
        app: Instancia de QApplication o QCoreApplication
        language: Código de idioma (ej: 'es', 'en', 'ca'). 
                 Si es None, usa el idioma del sistema.
    
    Returns:
        QTranslator si se cargó correctamente, None en caso contrario
    """
    if language is None:
        language = get_system_language()
    
    if language not in AVAILABLE_LANGUAGES:
        print(f"Advertencia: Idioma '{language}' no disponible. Usando español.")
        language = 'es'
    
    # Ruta del archivo de traducción compilado (.qm)
    qm_file = TRANSLATIONS_DIR / f"creative_erp_{language}.qm"
    
    if not qm_file.exists():
        print(f"Advertencia: Archivo de traducción no encontrado: {qm_file}")
        print("Ejecuta: python scripts/compile_translations.py")
        return None
    
    # Crear y cargar traductor
    translator = QTranslator()
    
    if translator.load(str(qm_file)):
        app.installTranslator(translator)
        print(f"✓ Traducción cargada: {AVAILABLE_LANGUAGES[language]} ({language})")
        return translator
    else:
        print(f"Error: No se pudo cargar la traducción desde {qm_file}")
        return None


def change_language(app: QCoreApplication, old_translator: Optional[QTranslator], 
                   new_language: str) -> Optional[QTranslator]:
    """
    Cambia el idioma de la aplicación en tiempo de ejecución.
    
    Args:
        app: Instancia de QApplication o QCoreApplication
        old_translator: Traductor anterior (puede ser None)
        new_language: Nuevo código de idioma
    
    Returns:
        Nuevo QTranslator si se cargó correctamente, None en caso contrario
    """
    # Remover traductor anterior
    if old_translator is not None:
        app.removeTranslator(old_translator)
    
    # Cargar nuevo traductor
    return load_translation(app, new_language)


def available_languages() -> dict:
    """
    Retorna un diccionario con los idiomas disponibles.
    
    Returns:
        Dict con código de idioma como clave y nombre como valor
    """
    return AVAILABLE_LANGUAGES.copy()


def get_language_name(language_code: str) -> str:
    """
    Obtiene el nombre de un idioma dado su código.
    
    Args:
        language_code: Código de idioma (ej: 'es')
    
    Returns:
        Nombre del idioma (ej: 'Español')
    """
    return AVAILABLE_LANGUAGES.get(language_code, language_code)
