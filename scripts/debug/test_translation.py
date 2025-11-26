#!/usr/bin/env python3
"""Script de prueba para verificar traducciones"""

from PySide6.QtWidgets import QApplication, QDialog
from PySide6.QtCore import QTranslator, QCoreApplication, QSettings
import sys

# Crear aplicación
app = QApplication(sys.argv)

# Configurar idioma en settings
settings = QSettings("ArtStudio3D", "Creative ERP")
settings.setValue("language", "fr")

# Cargar traductor
translator = QTranslator()
if translator.load('translations/creative_erp_fr.qm'):
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
print(f"\nTextos en el widget:")
print(f"  btnAnadir: '{ui.btnAnadir.text()}'")
print(f"  btnEditar: '{ui.btnEditar.text()}'")
print(f"  btnGuardar: '{ui.btnGuardar.text()}'")
print(f"  label_3 (Nombre): '{ui.label_3.text()}'")

# Mostrar el diálogo
dialog.show()
sys.exit(app.exec())
