"""
Vista del diálogo de configuración de Creative ERP.
Permite configurar el idioma de la aplicación.
"""

from PySide6.QtCore import QSettings, Signal
from PySide6.QtWidgets import QDialog, QMessageBox

from core.ui_helpers import show_info, show_question, show_warning
from modules.common.ui_frmConfig import Ui_frmConfig


class ConfigDialog(QDialog):
    """Diálogo de configuración de la aplicación."""

    # Señal emitida cuando se cambia el idioma
    language_changed = Signal(str)  # Emite el código del idioma (es, en, ca, fr)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_frmConfig()
        self.ui.setupUi(self)

        # Referencia a la ventana principal para acceder a los métodos de caché
        self.main_window = None
        # Buscar la ventana principal en los ancestros
        parent_widget = parent
        while parent_widget is not None:
            if hasattr(parent_widget, "set_max_cached_modules"):
                self.main_window = parent_widget
                break
            parent_widget = (
                parent_widget.parent() if hasattr(parent_widget, "parent") else None
            )

        # Mapeo de índices del ComboBox a códigos de idioma
        # El orden en el .ui es: Español, Française, Català, English
        self.language_map = {
            0: "es",  # Español
            1: "fr",  # Français
            2: "ca",  # Català
            3: "en",  # English
        }

        # Mapeo inverso: código -> índice
        self.index_map = {v: k for k, v in self.language_map.items()}

        # Cargar idioma actual y normativa fiscal
        self._load_current_language()
        self._load_fiscal_country()
        self._load_cache_settings()

        # Conectar señales
        self.ui.buttonBox.accepted.connect(self._on_accept)
        self.ui.buttonBox.rejected.connect(self.reject)
        self.ui.btnLimpiarCache.clicked.connect(self._on_clear_cache)

    def _load_current_language(self):
        """Carga el idioma actual desde QSettings."""
        settings = QSettings()
        current_lang = settings.value("language", "es")  # Default: español

        # Establecer el índice correcto en el ComboBox
        if current_lang in self.index_map:
            index = self.index_map[current_lang]
            self.ui.cboIdioma.setCurrentIndex(index)

    def _load_fiscal_country(self):
        """Carga la normativa fiscal actual desde QSettings y actualiza el combo correspondiente."""
        settings = QSettings()
        current_fiscal = settings.value("fiscal_country", "fr")  # Default: Francia
        # Mapeo de índices a códigos de país (as defined previously)
        fiscal_map = {0: "fr", 1: "es"}
        fiscal_index_map = {v: k for k, v in fiscal_map.items()}
        if (
            hasattr(self.ui, "cboValoresFiscales")
            and current_fiscal in fiscal_index_map
        ):
            idx = fiscal_index_map[current_fiscal]
            self.ui.cboValoresFiscales.setCurrentIndex(idx)

    def _load_cache_settings(self):
        """Carga la configuración de caché de módulos desde QSettings."""
        settings = QSettings()
        max_cached = settings.value("max_cached_modules", 5, type=int)
        self.ui.spinMaxModulos.setValue(max_cached)

    def _on_accept(self):
        """Maneja el evento de aceptar el diálogo, guardando idioma y normativa fiscal."""
        # Obtener el idioma seleccionado
        selected_index = self.ui.cboIdioma.currentIndex()
        selected_lang = self.language_map.get(selected_index, "es")

        # Obtener la normativa fiscal seleccionada (nuevo combo)
        fiscal_selected_index = getattr(self.ui, "cboValoresFiscales", None)
        if fiscal_selected_index is not None:
            fiscal_idx = self.ui.cboValoresFiscales.currentIndex()
            fiscal_map = {0: "fr", 1: "es"}
            selected_fiscal = fiscal_map.get(fiscal_idx, "fr")
        else:
            selected_fiscal = None

        # Guardar en QSettings
        settings = QSettings()
        old_lang = settings.value("language", "es")
        if old_lang != selected_lang:
            settings.setValue("language", selected_lang)
            self.language_changed.emit(selected_lang)

        if selected_fiscal is not None:
            settings.setValue("fiscal_country", selected_fiscal)

        # Guardar configuración de caché
        max_cached = self.ui.spinMaxModulos.value()
        settings.setValue("max_cached_modules", max_cached)

        # Aplicar el nuevo límite de caché si la ventana principal está disponible
        if self.main_window:
            self.main_window.set_max_cached_modules(max_cached)

        self.accept()

    def _on_clear_cache(self):
        """Maneja el evento del botón Limpiar Caché."""
        if self.main_window:
            reply = show_question(
                self,
                self.tr("Limpiar Caché"),
                self.tr(
                    "¿Desea limpiar la caché de módulos?\n\n"
                    "Esto liberará memoria de todos los módulos no activos.\n"
                    "Los módulos se volverán a cargar automáticamente cuando los necesite."
                ),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )

            if reply == QMessageBox.StandardButton.Yes:
                self.main_window.clear_module_cache()
                show_info(
                    self,
                    self.tr("Caché Limpiada"),
                    self.tr(
                        "La caché de módulos ha sido limpiada exitosamente.\nLa memoria ha sido liberada."
                    ),
                )
        else:
            show_warning(
                self,
                self.tr("No disponible"),
                self.tr(
                    "Esta función solo está disponible cuando la aplicación está en ejecución."
                ),
            )

    def get_selected_language(self):
        """Retorna el código del idioma seleccionado."""
        selected_index = self.ui.cboIdioma.currentIndex()
        return self.language_map.get(selected_index, "es")
