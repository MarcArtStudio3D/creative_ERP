#!/usr/bin/env python3
"""
Ejemplo de integración Qt con selección de empresa y cambio automático de base de datos
Este archivo muestra cómo integrar el sistema multi-base de datos en la UI de Qt
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

# Importar módulos necesarios
try:
    from PySide6.QtWidgets import (
            QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
            QLabel, QComboBox, QPushButton, QTextEdit, QGroupBox, QFormLayout,
            QStatusBar
    )
    from PySide6.QtCore import Qt, Signal
    from PySide6.QtGui import QFont, QPalette, QColor
except ImportError:
    print("❌ PySide6 no está instalado. Instalar con: pip install PySide6")
    sys.exit(1)

from core.company_manager import company_manager, setup_company_selection_combo, on_company_selected, get_current_company_context
from core.ui_helpers import show_warning, show_info, show_critical, show_question


class CompanySelectionWidget(QWidget):
    """Widget para selección de empresa con cambio automático de base de datos."""

    company_changed = Signal(dict)  # Señal emitida cuando cambia la empresa

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Inicializa la interfaz de usuario."""
        layout = QVBoxLayout()

        # Grupo de selección de empresa
        selection_group = QGroupBox(self.tr("Selección de Empresa"))
        selection_layout = QFormLayout()

        # Combo de empresas
        self.company_combo = QComboBox()
        self.company_combo.addItem(self.tr("Cargando empresas..."), None)
        self.company_combo.currentIndexChanged.connect(self.on_company_combo_changed)
        selection_layout.addRow(self.tr("Empresa:"), self.company_combo)

        # Botón de validar
        self.validate_btn = QPushButton(self.tr("Validar Configuración"))
        self.validate_btn.clicked.connect(self.validate_current_company)
        selection_layout.addRow(self.validate_btn)

        selection_group.setLayout(selection_layout)
        layout.addWidget(selection_group)

        # Grupo de información de empresa actual
        info_group = QGroupBox(self.tr("Empresa Actual"))
        info_layout = QFormLayout()

        self.company_name_label = QLabel(self.tr("Ninguna empresa seleccionada"))
        info_layout.addRow(self.tr("Nombre:"), self.company_name_label)

        self.database_label = QLabel(self.tr("N/A"))
        info_layout.addRow(self.tr("Base de Datos:"), self.database_label)

        self.motor_label = QLabel(self.tr("N/A"))
        info_layout.addRow(self.tr("Motor BD:"), self.motor_label)

        info_group.setLayout(info_layout)
        layout.addWidget(info_group)

        # Área de log
        log_group = QGroupBox(self.tr("Log de Operaciones"))
        log_layout = QVBoxLayout()

        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(150)
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)

        # Botón de limpiar log
        clear_log_btn = QPushButton(self.tr("Limpiar Log"))
        clear_log_btn.clicked.connect(self.clear_log)
        log_layout.addWidget(clear_log_btn)

        log_group.setLayout(log_layout)
        layout.addWidget(log_group)

        self.setLayout(layout)

        # Cargar empresas al inicializar
        self.load_companies()

    def load_companies(self):
        """Carga la lista de empresas disponibles."""
        try:
            self.log_message(self.tr("Cargando empresas disponibles..."))
            setup_company_selection_combo(self.company_combo)
            self.log_message(self.tr("✅ Empresas cargadas exitosamente"))
        except Exception as e:
            self.log_message(f"❌ Error cargando empresas: {e}")
            show_critical(self, self.tr("Error"), self.tr("Error cargando empresas:\n{}").format(str(e)))

    def on_company_combo_changed(self, index):
        """Maneja el cambio de selección en el combo de empresas."""
        company_id = self.company_combo.itemData(index)

        if company_id is None:
            # Opción por defecto seleccionada
            self.update_company_info(None)
            return

        self.log_message(f"Selecting company ID: {company_id}")

        # Intentar seleccionar la empresa
        success = on_company_selected(company_id)

        if success:
            # Actualizar información en UI
            context = get_current_company_context()
            self.update_company_info(context)

            # Emitir señal de cambio de empresa
            self.company_changed.emit(context)

            self.log_message("✅ Empresa seleccionada exitosamente")
        else:
            self.log_message(self.tr("❌ Error seleccionando empresa"))
            # Resetear combo a opción por defecto
            self.company_combo.setCurrentIndex(0)
            show_warning(self, self.tr("Error"), self.tr("No se pudo seleccionar la empresa.\nVerifique la configuración de base de datos."))

    def validate_current_company(self):
        """Valida la configuración de la empresa actualmente seleccionada."""
        current_index = self.company_combo.currentIndex()
        company_id = self.company_combo.itemData(current_index)

        if company_id is None:
            show_info(self, self.tr("Validación"), self.tr("Seleccione una empresa primero."))
            return

        self.log_message(f"Validando configuración de empresa ID: {company_id}")

        try:
            validation = company_manager.validate_company_database(company_id)

            if validation['valid']:
                self.log_message("✅ Configuración de base de datos válida")
                show_info(self, self.tr("Validación Exitosa"),
                    self.tr("La configuración de base de datos es correcta.\nEmpresa: {company}\nMotor: {motor}\nBase de datos: {db}").format(
                        company=validation['company_info']['company_name'],
                        motor=validation['company_info']['motor_base_datos'],
                        db=validation['company_info']['database_name']
                    ))
            else:
                self.log_message(f"❌ Configuración inválida: {validation['message']}")
                show_warning(self, self.tr("Validación Fallida"),
                    self.tr("La configuración de base de datos no es válida:\n{}").format(validation['message']))

        except Exception as e:
            self.log_message(f"❌ Error en validación: {e}")
            show_critical(self, self.tr("Error"), self.tr("Error validando configuración:\n{}").format(str(e)))

    def update_company_info(self, context):
        """Actualiza la información mostrada de la empresa actual."""
        if not context or not context.get('has_company'):
            self.company_name_label.setText("Ninguna empresa seleccionada")
            self.database_label.setText("N/A")
            self.motor_label.setText("N/A")
        else:
            self.company_name_label.setText(context['company_name'])
            self.database_label.setText(context['database_name'])
            self.motor_label.setText(context['motor_bd'])

    def log_message(self, message):
        """Agrega un mensaje al log."""
        self.log_text.append(message)
        # Auto-scroll al final
        cursor = self.log_text.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.log_text.setTextCursor(cursor)

    def clear_log(self):
        """Limpia el área de log."""
        self.log_text.clear()


class MainWindow(QMainWindow):
    """Ventana principal de ejemplo."""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Inicializa la interfaz principal."""
        self.setWindowTitle(self.tr("Creative ERP - Gestión Multi-Base de Datos"))
        self.setGeometry(100, 100, 800, 600)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # Título
        title_label = QLabel(self.tr("Creative ERP - Multi-Database System"))
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Widget de selección de empresa
        self.company_widget = CompanySelectionWidget()
        self.company_widget.company_changed.connect(self.on_company_changed)
        layout.addWidget(self.company_widget)

        # Área de contenido de ejemplo
        content_group = QGroupBox(self.tr("Contenido de la Aplicación"))
        content_layout = QVBoxLayout()

        self.content_label = QLabel(self.tr("Aquí iría el contenido principal de tu aplicación.\n"
                       "Cuando cambies de empresa, esta área se actualizaría automáticamente."))
        self.content_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content_label.setStyleSheet("QLabel { padding: 20px; border: 1px solid #ccc; border-radius: 5px; }")
        content_layout.addWidget(self.content_label)

        content_group.setLayout(content_layout)
        layout.addWidget(content_group)

        central_widget.setLayout(layout)

        # Barra de estado
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(self.tr("Listo - Seleccione una empresa para comenzar"))

    def on_company_changed(self, context):
        """Maneja el cambio de empresa."""
        if context['has_company']:
            self.status_bar.showMessage(f"Empresa activa: {context['company_name']} - BD: {context['database_name']}")

            # Actualizar contenido de ejemplo
            self.content_label.setText(f"Company: {context['company_name']}\n"
                                     f"Database: {context['database_name']}\n"
                                     f"⚙️  Motor: {context['motor_bd']}\n\n"
                                     "¡Aquí puedes cargar los módulos específicos de esta empresa!")
        else:
            self.status_bar.showMessage("Ninguna empresa seleccionada")
            self.content_label.setText(self.tr("Seleccione una empresa para ver su contenido."))


def main():
    """Función principal."""
    app = QApplication(sys.argv)

    # Configurar estilo de la aplicación
    app.setStyle('Fusion')

    # Paleta oscura opcional
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
    palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)

    # Aplicar paleta si se desea tema oscuro
    # app.setPalette(palette)

    # Crear y mostrar ventana principal
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()