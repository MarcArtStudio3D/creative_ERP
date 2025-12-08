"""
Vista del módulo Divisiones del Almacén
Abre el diálogo de gestión de Secciones, Familias y Subfamilias
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

from core.ui_helpers import show_critical
from modules.articulos.divisiones_view import DivisionesView


class DivisionesAlmacenView(QWidget):
    """Vista principal para el módulo de Divisiones del Almacén"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz de usuario"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # Título (sin emojis)
        title = QLabel(self.tr("Divisiones del Almacén"))
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Descripción
        description = QLabel(
            "Gestiona la estructura jerárquica de tu almacén:\n\n"
            "• Secciones: Primera división del almacén\n"
            "• Familias: Agrupación dentro de cada sección\n"
            "• Subfamilias: Clasificación detallada de productos"
        )
        description.setStyleSheet("font-size: 14px; padding: 20px;")
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(description)

        # Botón para abrir el diálogo
        btn_abrir = QPushButton(self.tr("Abrir Gestor de Divisiones"))
        try:
            btn_abrir.setIcon(QIcon(":/PNG/resources/icons/png/List.png"))
        except Exception:
            pass
        btn_abrir.setMinimumHeight(50)
        btn_abrir.setStyleSheet(
            """
            QPushButton {
                background-color: #6c5ce7;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #5f4dd1;
            }
            QPushButton:pressed {
                background-color: #5041b3;
            }
        """
        )
        btn_abrir.clicked.connect(self.abrir_divisiones)
        layout.addWidget(btn_abrir)

        layout.addStretch()

        # Información adicional
        info = QLabel(
            "Consejo: Organiza tus productos en secciones y familias\n"
            "para facilitar su búsqueda y gestión."
        )
        info.setStyleSheet("font-size: 12px; color: #666; padding: 10px;")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info)

    def abrir_divisiones(self):
        """Abre el diálogo de divisiones"""
        try:
            dialog = DivisionesView(self)
            dialog.exec()
        except Exception as e:
            show_critical(
                self,
                self.tr("Error"),
                self.tr("No se pudo abrir el gestor de divisiones:\n{}").format(str(e)),
            )
            import traceback

            traceback.print_exc()

    def nuevo(self):
        """Método llamado desde el botón 'Añadir' del panel lateral"""
        self.abrir_divisiones()

    def nuevo_registro(self):
        """Alias para compatibilidad"""
        self.abrir_divisiones()

    def editar(self):
        """Método llamado desde el botón 'Editar' del panel lateral"""
        self.abrir_divisiones()

    def editar_registro(self):
        """Alias para compatibilidad"""
        self.abrir_divisiones()
