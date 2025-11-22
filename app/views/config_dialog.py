"""
Vista del diálogo de configuración de Creative ERP.
Permite configurar el idioma de la aplicación.
"""

from PySide6.QtWidgets import QDialog, QMessageBox
from PySide6.QtCore import QSettings, Signal
from app.views.ui_frmConfig import Ui_frmConfig
from core.translations import AVAILABLE_LANGUAGES


class ConfigDialog(QDialog):
    """Diálogo de configuración de la aplicación."""
    
    # Señal emitida cuando se cambia el idioma
    language_changed = Signal(str)  # Emite el código del idioma (es, en, ca, fr)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_frmConfig()
        self.ui.setupUi(self)
        
        # Mapeo de índices del ComboBox a códigos de idioma
        # El orden en el .ui es: Español, Française, Català, English
        self.language_map = {
            0: 'es',  # Español
            1: 'fr',  # Français
            2: 'ca',  # Català
            3: 'en',  # English
        }
        
        # Mapeo inverso: código -> índice
        self.index_map = {v: k for k, v in self.language_map.items()}
        
        # Cargar idioma actual
        self._load_current_language()
        
        # Conectar señales
        self.ui.buttonBox.accepted.connect(self._on_accept)
        self.ui.buttonBox.rejected.connect(self.reject)
    
    def _load_current_language(self):
        """Carga el idioma actual desde QSettings."""
        settings = QSettings()
        current_lang = settings.value("language", "es")  # Default: español
        
        # Establecer el índice correcto en el ComboBox
        if current_lang in self.index_map:
            index = self.index_map[current_lang]
            self.ui.cboIdioma.setCurrentIndex(index)
    
    def _on_accept(self):
        """Maneja el evento de aceptar el diálogo."""
        # Obtener el idioma seleccionado
        selected_index = self.ui.cboIdioma.currentIndex()
        selected_lang = self.language_map.get(selected_index, 'es')
        
        # Guardar en QSettings
        settings = QSettings()
        old_lang = settings.value("language", "es")
        
        if old_lang != selected_lang:
            # El idioma ha cambiado
            settings.setValue("language", selected_lang)
            
            # Emitir señal de cambio de idioma
            # El diálogo se mostrará en el manejador de la señal (login_window_multi.py)
            self.language_changed.emit(selected_lang)
        
        self.accept()
    
    def get_selected_language(self):
        """Retorna el código del idioma seleccionado."""
        selected_index = self.ui.cboIdioma.currentIndex()
        return self.language_map.get(selected_index, 'es')
