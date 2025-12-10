#!/usr/bin/env python3
"""Script de prueba para verificar traducciones

Se convierte en un script seguro para importar por tests (no ejecuta app.exec()
cuando se importa)."""

import sys

from PySide6.QtCore import QSettings, QTranslator
from PySide6.QtWidgets import QApplication, QDialog


def main(argv=None):
    """Ejecutar la comprobación de traducciones (solo cuando se ejecuta como script)."""
    argv = argv or sys.argv

    # Crear aplicación
    app = QApplication(argv)

    # Configurar idioma en settings
    settings = QSettings("ArtStudio3D", "Creative ERP")
    settings.setValue("language", "fr")

    # Cargar traductor
    translator = QTranslator()
    if translator.load("translations/creative_erp_fr.qm"):
        app.installTranslator(translator)
        print("✓ Traductor instalado")
    else:
        print("✗ Error al cargar traductor")

    # Crear un widget desde el archivo UI compilado
    from modules.clientes.ui_frmClientes import Ui_frmClientes

    dialog = QDialog()
    ui = Ui_frmClientes()
    ui.setupUi(dialog)

    # Verificar algunos textos
    print("\nTextos en el widget:")
    print(f"  btnAnadir: '{ui.btnAnadir.text()}'")
    print(f"  btnEditar: '{ui.btnEditar.text()}'")
    print(f"  btnGuardar: '{ui.btnGuardar.text()}'")
    print(f"  label_3 (Nombre): '{ui.label_3.text()}'")

    # Mostrar el diálogo
    dialog.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
