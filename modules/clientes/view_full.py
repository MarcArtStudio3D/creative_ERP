"""
Vista del módulo de Clientes - Solo lógica de negocio
La UI se genera automáticamente desde frmClientes.ui
"""

from logging import disable
from PySide6.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QVBoxLayout, QTableWidget, QTableView
from PySide6.QtCore import Qt, QDate, Signal, QAbstractTableModel
from PySide6.QtSql import QSqlDatabase
from typing import Any
from PySide6.QtGui import QStandardItemModel, QStandardItem
from datetime import date
import sqlite3
import os
from core.db import get_session
from modules.clientes.models import Cliente, DireccionAlternativa
from modules.clientes.repository import ClienteRepository
from modules.clientes.ui_frmClientes import Ui_frmClientes
from modules.common.db_consulta_view import DBConsultaView


def format_nombre_fiscal(ap1: str, ap2: str, nombre: str) -> str:
    """
    Formats fiscal name from components.
    ap1: First surname/apellido
    ap2: Second surname/apellido  
    nombre: Given name(s)
    Returns: Formatted string in uppercase, space-separated, or empty string if no parts
    """
    parts = []
    if ap1:
        parts.append(ap1)
    if ap2:
        parts.append(ap2)
    if (ap1 or ap2) and nombre:
        parts.append(nombre)
    if not parts and nombre:
        parts = [nombre]
    computed = ' '.join(parts).strip()
    return computed.upper() if computed else ''


class ClientesViewFull(QWidget):
    """Vista completa de clientes - Solo lógica, UI desde archivo .ui"""
    
    cliente_seleccionado = Signal(int)
    
    def __init__(self, parent=None, preserve_styles=None, custom_styles=None):
        """
        preserve_styles: iterable of objectName strings to NOT clear styles for.
        custom_styles: dict mapping objectName -> stylesheet string to apply.
        """
        super().__init__(parent)
        # exclusiones y estilos personalizados (por objectName)
        self._preserve_styles = set(preserve_styles or [])
        self._custom_styles = dict(custom_styles or {})
        
        # Crear layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Crear un widget temporal para cargar el UI
        from PySide6.QtWidgets import QDialog
        temp_dialog = QDialog()
        self.ui: Any = Ui_frmClientes()
        self.ui.setupUi(temp_dialog)
        
        # Mantener el stackedWidget intacto pero reparentarlo
        if hasattr(self.ui, 'stackedWidget'):
            self.ui.stackedWidget.setParent(self)
            self.ui.stackedWidget.setVisible(True)
            layout.addWidget(self.ui.stackedWidget)
            
            # Forzar actualización del tabwidget después del reparenting
            if hasattr(self.ui, 'tabwidget'):
                self.ui.tabwidget.update()
                self.ui.tabwidget.repaint()
        
        # Cerrar el diálogo temporal
        temp_dialog.deleteLater()
        
        # Desactivar campos de edición inmediatamente después de crear la UI
        self.desactivar_campos_edicion()
        
        # Verificar que los campos estén realmente desactivados
        # self.verificar_estado_campos()  # Deshabilitado en producción
        
        # Forzar desactivación después de que la vista se muestre completamente
        from PySide6.QtCore import QTimer
        QTimer.singleShot(100, self.forzar_desactivacion_campos)
        
        # Inicializar datos
        self.session = get_session()
        self.repository = ClienteRepository(self.session)
        self.cliente_actual = None
        self._modo_edicion = False  # Bandera para controlar el modo de edición
        
        # Conectar señales de botones principales
        self.conectar_senales()
        
        # Aplicar ajustes de tema para que los widgets usen colores del palette
        try:
            self.apply_palette_styles()
        except Exception:
            # No crítico; si falla seguimos adelante
            pass

        # Mostrar página de búsquedas/lista al inicio (índice 1)
        if hasattr(self.ui, 'stackedWidget'):
            self.ui.stackedWidget.setCurrentIndex(1)
        
        # Cargar clientes
        self.cargar_clientes()
        # Re-aplicar ajustes de estilo para asegurar que cualquier limpieza posterior
        # no borre las exclusiones o estilos personalizados.
        try:
            self.apply_palette_styles()
        except Exception:
            pass
        
        # CRÍTICO: Re-aplicar desactivación de campos después de apply_palette_styles
        # ya que setStyleSheet puede resetear propiedades de los widgets
        self.desactivar_campos_edicion()
    
    def conectar_senales(self):
        """Conecta las señales de los widgets a los métodos"""
        # Botones principales (página lista - estos están en el frame lateral)
        for name, handler in (
            ("btnAnadir", self.nuevo_cliente),
            ("btnEditar", self.editar_cliente),
            ("btnBorrar", self.borrar_cliente),
        ):
            w = self._get_widget(name)
            if w is not None and hasattr(w, "clicked"):
                w.clicked.connect(handler)

        # Tabla de búsquedas (doble clic para abrir ficha)
        tabla = self._find_table()
        if tabla is not None:
            # QTableWidget tiene señal itemDoubleClicked/cellDoubleClicked
            # QTableView tiene señal doubleClicked (index)
            if hasattr(tabla, "itemDoubleClicked"):
                try:
                    tabla.itemDoubleClicked.connect(lambda *args: self.abrir_ficha_cliente())
                except Exception:
                    pass
            elif hasattr(tabla, "cellDoubleClicked"):
                try:
                    tabla.cellDoubleClicked.connect(lambda r, c: self.abrir_ficha_cliente())
                except Exception:
                    pass
            elif hasattr(tabla, "doubleClicked"):
                try:
                    tabla.doubleClicked.connect(self.abrir_ficha_cliente)
                except Exception:
                    pass

        # Botones de navegación en la ficha
        for name, handler in (("btnSiguiente", self.siguiente_cliente), ("btnAnterior", self.anterior_cliente), ("btnBuscar", self.volver_a_lista)):
            w = self._get_widget(name)
            if w is not None and hasattr(w, "clicked"):
                w.clicked.connect(handler)

        # Botón 'Listados' (mostrar la lista completa de clientes)
        bl = self._get_widget('botListados')
        if bl is not None and hasattr(bl, 'clicked'):
            try:
                bl.clicked.connect(self.volver_a_lista)
            except Exception:
                pass

        # Botones de guardar/deshacer en la ficha de edición
        for name, handler in (("btnGuardar", self.guardar_cliente), ("btnDeshacer", self.deshacer_cambios)):
            w = self._get_widget(name)
            if w is not None and hasattr(w, "clicked"):
                w.clicked.connect(handler)

        # Conectar cambio de página del stackedWidget para activar/desactivar campos
        if hasattr(self.ui, 'stackedWidget'):
            self.ui.stackedWidget.currentChanged.connect(self.on_pagina_cambiada)
        
        # Obtener el país fiscal desde la configuración global
        from PySide6.QtCore import QSettings
        settings = QSettings()
        fiscal_country = settings.value("fiscal_country", "fr")  # Default: Francia
        
        # ESPAÑA (desactivar campos no necesarios)
        if fiscal_country == 'es':
            if hasattr(self.ui, 'txtSiret'):
                self.ui.txtSiret.setVisible(False)
                self.ui.lblSiret.setVisible(False)
        
        # FRANCIA (desactivar campos no necesarios)
        if fiscal_country == 'fr':
            if hasattr(self.ui, 'txtSegundoApellido'):
                self.ui.txtSegundoApellido.setVisible(False)
                self.ui.lblSegundoApellido.setVisible(False)

        
        # Activar validaciones inline (conectar señales) - se ignoran fuera de modo edición
        if not hasattr(self, '_validations_connected') or not self._validations_connected:
            try:
                from PySide6.QtWidgets import QLineEdit, QTextEdit, QPlainTextEdit, QDateEdit, QSpinBox, QComboBox, QDoubleSpinBox
                # Useful fields for validation
                names = ['txtcodigo_cliente', 'txtnombre', 'txtPrimerApellido', 'txtSegundoApellido', 'txtnombre_fiscal', 'txtcif_nif', 'txtemail', 'txtdia_pago1', 'txtdia_pago2', 'txtcuenta_corriente', 'txtiban', 'txtCuentaIBAN', 'txtcp']
                for n in names:
                    w = getattr(self.ui, n, None)
                    if w is None:
                        continue
                    # Connect according to widget type
                    if isinstance(w, (QLineEdit, QTextEdit, QPlainTextEdit)):
                        try:
                            # connect to textChanged and use sender()
                            w.textChanged.connect(self._on_widget_change)
                        except Exception:
                            pass
                        # Special handling for txtnombre_fiscal to detect manual edits
                        if n == 'txtnombre_fiscal' and isinstance(w, QLineEdit):
                            try:
                                # textEdited is only emitted when user types, not when setText is called
                                w.textEdited.connect(self._on_nombre_fiscal_manual_edit)
                            except Exception:
                                pass

                    elif isinstance(w, QComboBox):
                        try:
                            w.currentIndexChanged.connect(self._on_widget_change)
                        except Exception:
                            pass
                    elif isinstance(w, (QSpinBox, QDoubleSpinBox)):
                        try:
                            w.valueChanged.connect(self._on_widget_change)
                        except Exception:
                            pass
                    elif isinstance(w, QDateEdit):
                        try:
                            w.dateChanged.connect(self._on_widget_change)
                        except Exception:
                            pass
                    
                self._validations_connected = True
            except Exception:
                self._validations_connected = False

        # Instalar event filter para validación visual en foco
        self._install_focus_validation()

    def _install_focus_validation(self):
        """Instala event filter para mostrar bordes verdes/rojos en campos al recibir foco"""
        from PySide6.QtWidgets import QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit
        from PySide6.QtCore import QEvent

        # Campos que queremos validar visualmente
        validation_fields = [
            'txtcodigo_cliente', 'txtnombre', 'txtPrimerApellido', 'txtSegundoApellido',
            'txtnombre_fiscal', 'txtcif_nif', 'txtemail', 'txtdia_pago1', 'txtdia_pago2',
            'txtcuenta_corriente', 'txtiban', 'txtCuentaIBAN', 'txtcp'
        ]

        for field_name in validation_fields:
            widget = getattr(self.ui, field_name, None)
            if widget is not None:
                widget.installEventFilter(self)

    def eventFilter(self, obj, event):
        """Event filter para manejar eventos de foco y aplicar validación visual"""
        from PySide6.QtCore import QEvent
        from PySide6.QtWidgets import QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit

        if event.type() == QEvent.Type.FocusIn:
            if isinstance(obj, (QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit)):
                self._validate_field_on_focus(obj)
        elif event.type() == QEvent.Type.FocusOut:
            # Limpiar estilos cuando pierde el foco (opcional)
            if isinstance(obj, (QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit)):
                # Solo limpiamos si no hay errores de validación pendientes
                if not self._has_validation_error(obj):
                    obj.setStyleSheet("")

        return super().eventFilter(obj, event)

    def _validate_field_on_focus(self, widget):
        """Valida el contenido del campo cuando recibe el foco y aplica borde verde/rojo"""
        from PySide6.QtWidgets import QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit

        # Obtener el nombre del campo
        field_name = None
        for attr_name in dir(self.ui):
            if getattr(self.ui, attr_name) is widget:
                field_name = attr_name
                break

        if not field_name:
            return

        # Obtener el valor del campo
        value = ""
        if isinstance(widget, QLineEdit):
            value = widget.text().strip()
        elif isinstance(widget, (QTextEdit, QPlainTextEdit)):
            value = widget.toPlainText().strip()
        elif isinstance(widget, QComboBox):
            value = widget.currentText().strip()
        elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
            value = str(widget.value())
        elif isinstance(widget, QDateEdit):
            value = widget.date().toString("yyyy-MM-dd")

        # Validar según el tipo de campo
        is_valid = self._validate_field_value(field_name, value)

        # Aplicar borde verde si válido, rojo si inválido
        if is_valid and value:  # Solo mostrar verde si hay contenido y es válido
            widget.setStyleSheet("border: 2px solid #52c41a; border-radius: 2px;")
        elif value and not is_valid:  # Mostrar rojo solo si hay contenido inválido
            widget.setStyleSheet("border: 2px solid #ff4d4f; border-radius: 2px;")
        else:
            # Sin contenido o campo vacío - borde normal
            widget.setStyleSheet("")

    def _validate_field_value(self, field_name: str, value: str) -> bool:
        """Valida el valor de un campo específico"""
        if not value:
            return True  # Campos vacíos son considerados válidos

        # Validaciones específicas por campo
        if field_name in ['txtcif_nif']:
            return self._is_valid_nif_cif(value)
        elif field_name in ['txtemail']:
            return self._is_valid_email(value)
        elif field_name in ['txtcodigo_cliente']:
            return len(value.strip()) > 0  # Código debe tener contenido
        elif field_name in ['txtdia_pago1', 'txtdia_pago2']:
            try:
                dia = int(value)
                return 1 <= dia <= 31
            except ValueError:
                return False
        elif field_name in ['txtcp']:
            return self._is_valid_postal_code(value)
        elif field_name in ['txtcuenta_corriente', 'txtiban', 'txtCuentaIBAN']:
            return self._is_valid_iban_focus(value)
        else:
            # Para otros campos, cualquier contenido no vacío es válido
            return True

    def _is_valid_email(self, email: str) -> bool:
        """Valida formato básico de email"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def _is_valid_postal_code(self, cp: str) -> bool:
        """Valida código postal español (5 dígitos)"""
        return len(cp) == 5 and cp.isdigit()

    def _is_valid_iban_focus(self, iban: str) -> bool:
        """Valida formato básico de IBAN (versión para validación en foco)"""
        if not iban:
            return True
        # Remover espacios y convertir a mayúsculas
        iban = iban.replace(' ', '').upper()
        # IBAN español debe empezar con ES y tener 24 caracteres
        if len(iban) == 24 and iban.startswith('ES'):
            return iban[2:].isdigit()
        return False

    def _has_validation_error(self, widget) -> bool:
        """Verifica si un widget tiene errores de validación pendientes"""
        # Esta función puede ser expandida para verificar errores específicos
        # Por ahora, asumimos que si hay un tooltip de error, hay un error
        tooltip = widget.toolTip()
        return bool(tooltip and ("error" in tooltip.lower() or "inválido" in tooltip.lower()))

    def _get_widget(self, name, qtype=None):
        """Intento seguro de obtener un widget por nombre (getattr -> findChild)."""
        w = getattr(self.ui, name, None)
        if w is not None:
            return w
        try:
            qtype = qtype or QWidget
            return self.ui.findChild(qtype, name)
        except Exception:
            return None

    def on_pagina_cambiada(self, index):
        """Maneja el cambio de página en el stackedWidget"""
        if index == 0:  # Página de edición
            # Solo activar si realmente estamos en modo edición (nuevo o editar)
            if hasattr(self, '_modo_edicion') and self._modo_edicion:
                self.activar_campos_edicion()
        else:  # Página de lista/búsqueda - SIEMPRE desactivar campos
            self._modo_edicion = False
            self.desactivar_campos_edicion()

    def desactivar_campos_edicion(self):
        """Desactiva todos los campos editables relacionados con la base de datos"""
        from PySide6.QtWidgets import QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit, QCheckBox

        # Lista de campos que deben estar desactivados cuando no se está editando
        campos_edicion = [
            'txtcodigo_cliente', 'txtcif_nif', 'txtnombre', 'txtPrimerApellido', 'txtSegundoApellido',
            'txtnombre_fiscal', 'txtnombre_comercial', 'txtdireccion1', 'txtdireccion2', 'txtcp',
            'txtpoblacion', 'txtprovincia', 'txttelefono1', 'txttelefono2', 'txtmovil', 'txtfax',
            'txtemail', 'txtweb', 'txtNombreFiscal'
        ]

        for campo in campos_edicion:
            widget = self._get_widget(campo)
            if widget:
                self._desactivar_widget(widget)

        # Desactivar también otros tipos de widgets editables que puedan existir
        for widget_name in dir(self.ui):
            if widget_name.startswith('_'):
                continue

            widget = getattr(self.ui, widget_name)
            if isinstance(widget, (QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit, QCheckBox, QLineEdit, QTextEdit, QPlainTextEdit)):
                self._desactivar_widget(widget)
        # Desactivar validaciones visuales
        self._set_all_valid_state()

    def _desactivar_widget(self, widget):
        """Desactiva un widget usando la propiedad correcta según su tipo"""
        from PySide6.QtWidgets import QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit, QCheckBox
        
        if isinstance(widget, (QLineEdit, QTextEdit, QPlainTextEdit)):
            # Para campos de texto, usar setReadOnly para impedir edición pero mantener apariencia normal
            widget.setReadOnly(True)
        elif isinstance(widget, (QSpinBox, QDoubleSpinBox, QDateEdit)):
            # Para spinboxes y date edits, usar setReadOnly
            widget.setReadOnly(True)
        else:
            # Para comboboxes y checkboxes, usar setEnabled
            widget.setEnabled(False)

    def _activar_widget(self, widget):
        """Activa un widget usando la propiedad correcta según su tipo"""
        from PySide6.QtWidgets import QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit, QCheckBox
        
        if isinstance(widget, (QLineEdit, QTextEdit, QPlainTextEdit)):
            # Para campos de texto, quitar readOnly
            widget.setReadOnly(False)
        elif isinstance(widget, (QSpinBox, QDoubleSpinBox, QDateEdit)):
            # Para spinboxes y date edits, quitar readOnly
            widget.setReadOnly(False)
        else:
            # Para comboboxes y checkboxes, usar setEnabled
            widget.setEnabled(True)
        # If becoming editable, update validation visuals and enable validation hooks
        self._update_form_validity()

    def forzar_desactivacion_campos(self):
        """Fuerza la desactivación de campos después de que la vista se muestre completamente"""
        # Asegurar que estamos en la página correcta (1 = lista)
        if hasattr(self.ui, 'stackedWidget'):
            current_page = self.ui.stackedWidget.currentIndex()
            if current_page != 1:
                self.ui.stackedWidget.setCurrentIndex(1)
            else:
                # Si ya estamos en página 1, forzar desactivación sin disparar señal
                self.desactivar_campos_edicion()

    def activar_campos_edicion(self):
        """Activa todos los campos editables relacionados con la base de datos"""
        from PySide6.QtWidgets import QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit, QCheckBox

        # Lista de campos que deben estar activados cuando se está editando
        campos_edicion = [
            'txtcodigo_cliente', 'txtcif_nif', 'txtnombre', 'txtPrimerApellido', 'txtSegundoApellido',
            'txtnombre_fiscal', 'txtnombre_comercial', 'txtdireccion1', 'txtdireccion2', 'txtcp',
            'txtpoblacion', 'txtprovincia', 'txttelefono1', 'txttelefono2', 'txtmovil', 'txtfax',
            'txtemail', 'txtweb', 'txtNombreFiscal'
        ]

        for campo in campos_edicion:
            widget = self._get_widget(campo)
            if widget:
                self._activar_widget(widget)

        # Activar también otros tipos de widgets editables que puedan existir
        for widget_name in dir(self.ui):
            if widget_name.startswith('_'):
                continue

            widget = getattr(self.ui, widget_name)
            if isinstance(widget, (QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit, QCheckBox, QLineEdit, QTextEdit, QPlainTextEdit)):
                self._activar_widget(widget)

    def _find_table(self):
        """Encuentra la tabla principal probando varios nombres y tipos."""
        for candidate in ("tabla_busquedas", "tabla_clientes", "tableWidget", "tabla_busqueda"):
            w = self._get_widget(candidate)
            if w is not None:
                return w
        # fallback: buscar primer hijo que sea QTableWidget o QTableView
        try:
            tables = []
            try:
                tables.extend(self.findChildren(QTableWidget))
            except Exception:
                pass
            try:
                tables.extend(self.findChildren(QTableView))
            except Exception:
                pass
            if tables:
                return tables[0]
        except Exception:
            pass

        # Asegurar que cualquier estilo personalizado solicitado se aplique
        try:
            for name, style in self._custom_styles.items():
                try:
                    w = self._get_widget(name)
                    if w is None:
                        # fallback: buscar por findChildren globalmente
                        w = self.findChild(QWidget, name)
                    if w is not None:
                        w.setStyleSheet(style)
                except Exception:
                    continue
        except Exception:
            pass
        return None

    def _ajustar_encabezado_tabla(self, tabla, stretch_index: int = 2):
        """Ajusta el comportamiento de redimensionado del encabezado de `tabla`.

        - `stretch_index`: índice de la columna que debe quedarse en modo Stretch.
        Intenta aplicar `ResizeToContents` al resto de columnas y `Stretch` a la columna
        indicada. Funciona para `QTableWidget` y `QTableView`.
        """
        try:
            from PySide6.QtWidgets import QHeaderView
            # Determinar número de columnas
            cols = 0
            try:
                m = tabla.model()
                cols = m.columnCount() if m is not None else (tabla.columnCount() if hasattr(tabla, 'columnCount') else 0)
            except Exception:
                try:
                    cols = tabla.columnCount()
                except Exception:
                    cols = 0

            header = tabla.horizontalHeader()
            try:
                header.setStretchLastSection(True)
            except Exception:
                pass

            if cols <= 0:
                # Si no conocemos el número de columnas, intentar hasta 10 como fallback
                cols = 10

            for i in range(cols):
                try:
                    if i == stretch_index:
                        try:
                            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
                        except Exception:
                            # Fallback: intentar de nuevo con la misma API por compatibilidad
                            try:
                                header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
                            except Exception:
                                pass
                    else:
                        try:
                            header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
                        except Exception:
                            try:
                                header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
                            except Exception:
                                pass
                except Exception:
                    # Ignorar columnas fuera de rango o errores concretos
                    continue
        except Exception:
            # No hacer nada si no se puede ajustar
            pass

    def _get_str(self, obj, attr: str) -> str:
        """Devuelve de forma segura el valor de un atributo como string ('' si no existe).

        Usa getattr para evitar que el type checker trate a los atributos de SQLAlchemy
        como Column[] en tiempo estático.
        """
        try:
            val = getattr(obj, attr, None)
            return str(val) if val is not None else ""
        except Exception:
            return ""

    def _is_valid_dni(self, dni: str) -> bool:
        """Valida DNI (formato 8 dígitos + letra de control)."""
        if not dni:
            return False
        s = dni.strip().upper().replace('-', '').replace(' ', '')
        import re
        if not re.fullmatch(r"\d{8}[A-Z]", s):
            return False
        letters = "TRWAGMYFPDXBNJZSQVHLCKE"
        number = int(s[:8])
        expected = letters[number % 23]
        return s[-1] == expected

    def _is_valid_nie(self, nie: str) -> bool:
        """Valida NIE (X/Y/Z + 7 dígitos + letra)."""
        if not nie:
            return False
        s = nie.strip().upper().replace('-', '').replace(' ', '')
        import re
        if not re.fullmatch(r"[XYZ]\d{7}[A-Z]", s):
            return False
        mapping = {'X': '0', 'Y': '1', 'Z': '2'}
        num = mapping[s[0]] + s[1:8]
        letters = "TRWAGMYFPDXBNJZSQVHLCKE"
        expected = letters[int(num) % 23]
        return s[-1] == expected

    def _is_valid_cif(self, cif: str) -> bool:
        """Validación básica de formato de CIF (no calcula control completo)."""
        if not cif:
            return False
        s = cif.strip().upper().replace('-', '').replace(' ', '')
        import re
        # Letra inicial de sociedad + 7 dígitos + dígito/control (letra o número)
        # Expanded regex to include K, L, M just in case (legacy)
        if not re.fullmatch(r"[A-Z]\d{7}[0-9A-Z]", s):
            return False
            
        # Valid letters check
        valid_starts = "ABCDEFGHJNPQRSUVWKLM"
        if s[0] not in valid_starts:
            return False

        # Compute sums
        try:
            digits = [int(ch) for ch in s[1:8]]  # 7 digits d1..d7
            
            # sum of even positions: d2, d4, d6 (index: 1,3,5)
            s_even = sum(digits[i] for i in [1, 3, 5])
            
            # sum of odd positions: d1,d3,d5,d7 doubled
            def sum_odd(d):
                acc = 0
                for val in d[0::2]:
                    prod = val * 2
                    acc += prod // 10 + prod % 10
                return acc
                
            s_odd = sum_odd(digits)
            total = s_even + s_odd
            control_digit = (10 - (total % 10)) % 10
            
            control_letter_map = 'JABCDEFGHI'  # index by digit (0=J, 1=A, etc.)
            provided = s[-1]
            
            # Tipos de organización y su tipo de control esperado
            # Numérico: A, B, E, H
            # Letra: P, Q, S, K, W
            # Ambos (usualmente número, pero puede ser letra): C, D, F, G, J, N, R, U, V
            
            # Check numeric control
            if provided == str(control_digit):
                return True
                
            # Check letter control
            if provided == control_letter_map[control_digit]:
                return True
                
            return False
        except Exception:
            return False

    def _is_valid_nif_cif(self, value: str) -> bool:
        """Check combined NIF/NIE/CIF validity."""
        if not value:
            return False
        v = value.strip().upper()
        # Try DNI
        if self._is_valid_dni(v):
            return True
        # NIE
        if self._is_valid_nie(v):
            return True
        # CIF basic format check
        if self._is_valid_cif(v):
            return True
        # SIRET checks (Francia)
        if self._is_valid_siret(v):
            return True
        # SIREN checks (Francia - 9 dígitos)
        if self._is_valid_siren(v):
            return True
        return False

    def _luhn_check(self, digits: str) -> bool:
        """Return True if digits pass Luhn algorithm."""
        try:
            total = 0
            reverse_digits = digits[::-1]
            for i, ch in enumerate(reverse_digits):
                d = int(ch)
                if i % 2 == 1:
                    d = d * 2
                    if d > 9:
                        d -= 9
                total += d
            return total % 10 == 0
        except Exception:
            return False

    def _is_valid_siren(self, siren: str) -> bool:
        """Validate SIREN: 9 digits and Luhn check."""
        if not siren:
            return False
        s = siren.strip().replace(' ', '').replace('-', '')
        if not s.isdigit() or len(s) != 9:
            return False
        return self._luhn_check(s)

    def _is_valid_siret(self, siret: str) -> bool:
        """Validate SIRET: 14 digits and Luhn check."""
        if not siret:
            return False
        s = siret.strip().replace(' ', '').replace('-', '')
        if not s.isdigit() or len(s) != 14:
            return False
        return self._luhn_check(s)

    def _is_valid_iban(self, iban: str) -> bool:
        """Generic IBAN validation (mod 97)"""
        if not iban:
            return False
        s = iban.strip().replace(' ', '').upper()
        import re
        if not re.fullmatch(r"[A-Z]{2}\d{2}[A-Z0-9]+", s):
            return False
        # Move first 4 chars to end
        rearr = s[4:] + s[:4]
        # Replace letters with digits: A=10..Z=35
        conv = ''
        for ch in rearr:
            if ch.isalpha():
                conv += str(ord(ch) - 55)
            else:
                conv += ch
        # Compute int mod 97 (in chunks)
        try:
            total = 0
            for i in range(0, len(conv), 6):
                chunk = str(total) + conv[i:i+6]
                total = int(chunk) % 97
            return total == 1
        except Exception:
            return False

    def _is_valid_ccc(self, ccc: str) -> bool:
        """Validate Spanish CCC (Cuenta Corriente) control digits.
        ccc: 20 digits long string (bank 4, office 4, dc 2, account 10)
        """
        if not ccc:
            return False
        s = ccc.strip().replace(' ', '').replace('-', '')
        if not s.isdigit() or len(s) != 20:
            return False
        bank = s[0:4]
        office = s[4:8]
        dc = s[8:10]
        account = s[10:20]
        weights1 = [4, 8, 5, 10, 9, 7, 3, 6]
        weights2 = [1, 2, 4, 8, 5, 10, 9, 7, 3, 6]
        def compute_check(digits, weights):
            total = sum(int(d)*w for d, w in zip(digits, weights))
            r = 11 - (total % 11)
            if r == 11:
                r = 0
            elif r == 10:
                r = 1
            return r
        # First control digit computed from bank and office
        cd1 = compute_check(bank + office, weights1)
        cd2 = compute_check(account, weights2)
        return dc == f"{cd1}{cd2}"

    def _validar_campos(self) -> tuple[bool, list]:
        """Valida campos obligatorios y NIF/CIF. Devuelve (es_valido, lista_errores)."""
        errores = []

        # Código cliente obligatorio
        codigo = ''
        if hasattr(self.ui, 'txtcodigo_cliente'):
            codigo = (self.ui.txtcodigo_cliente.text() if hasattr(self.ui.txtcodigo_cliente, 'text') else '')
        elif getattr(self.ui, 'txtcodigo_cliente', None) is not None:
            # getattr fallback handled above
            codigo = getattr(self.ui, 'txtcodigo_cliente').text() if hasattr(getattr(self.ui, 'txtcodigo_cliente'), 'text') else ''
        if not codigo or str(codigo).strip() == '':
            errores.append(self.tr('El código de cliente es obligatorio.'))

        # Nombre o nombre fiscal obligatorio
        nombre = getattr(self.ui, 'txtnombre', None)
        nombre_fiscal = getattr(self.ui, 'txtnombre_fiscal', None)
        v_nombre = ''
        if nombre is not None and hasattr(nombre, 'text'):
            v_nombre = nombre.text()
        v_nombre_fiscal = ''
        if nombre_fiscal is not None and hasattr(nombre_fiscal, 'text'):
            v_nombre_fiscal = nombre_fiscal.text()
        if not (v_nombre and v_nombre.strip()) and not (v_nombre_fiscal and v_nombre_fiscal.strip()):
            errores.append(self.tr('Debe introducir el nombre o el nombre fiscal del cliente.'))

        # NIF/CIF/SIRET validation if provided
        if getattr(self.ui, 'txtcif_nif', None) is not None:
            txt = None
            w = getattr(self.ui, 'txtcif_nif')
            if hasattr(w, 'text'):
                txt = w.text()
            if txt and txt.strip():
                if not self._is_valid_nif_cif(txt):
                    errores.append(self.tr('El NIF/CIF introducido no parece válido.'))

        # Validar email si está presente
        if getattr(self.ui, 'txtemail', None) is not None:
            w = getattr(self.ui, 'txtemail')
            txt_email = w.text() if hasattr(w, 'text') else ''
            if txt_email and txt_email.strip():
                import re
                # Very simple email validation
                if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", txt_email.strip()):
                    errores.append(self.tr('El email introducido no es válido.'))

        # CCC (cuenta bancaria) validation if present
        if getattr(self.ui, 'txtcuenta_corriente', None) is not None:
            w = getattr(self.ui, 'txtcuenta_corriente')
            txtccc = w.text() if hasattr(w, 'text') else ''
            if txtccc and txtccc.strip():
                if not self._is_valid_ccc(txtccc):
                    errores.append(self.tr('La cuenta bancaria (CCC) no es válida.'))

        # IBAN validation if present
        if getattr(self.ui, 'txtiban', None) is not None or getattr(self.ui, 'txtCuentaIBAN', None) is not None:
            w = getattr(self.ui, 'txtiban', None) or getattr(self.ui, 'txtCuentaIBAN', None)
            txtiban = w.text() if (w is not None and hasattr(w, 'text')) else ''
            if txtiban and txtiban.strip():
                if not self._is_valid_iban(txtiban):
                    errores.append(self.tr('El IBAN introducido no es válido.'))

        # Dias de pago (si existen) deben ser 0-31
        for dname in ('txtdia_pago1', 'txtdia_pago2'):
            w = getattr(self.ui, dname, None)
            if w is not None:
                try:
                    val = int(w.value()) if hasattr(w, 'value') else int(w.text()) if hasattr(w, 'text') and w.text() else None
                    if val is not None and not (0 <= int(val) <= 31):
                        errores.append(self.tr('Día de pago {} fuera de rango 0-31.').format(dname))
                except Exception:
                    errores.append(self.tr('Día de pago {} no es un número válido.').format(dname))

        return (len(errores) == 0, errores)
    
    def cargar_clientes(self):
        """Carga los clientes desde la base de datos en la tabla"""
        try:
            clientes = self.repository.obtener_todos()
            
            # Buscar la tabla en la UI generada
            tabla = None
            if hasattr(self.ui, 'tabla_busquedas'):
                tabla = self.ui.tabla_busquedas
            elif hasattr(self.ui, 'tabla_clientes'):
                tabla = self.ui.tabla_clientes
            elif hasattr(self.ui, 'tableWidget'):
                tabla = self.ui.tableWidget
            
            if not tabla:
                print("No se encontró widget de tabla de clientes")
                return
            
            # Crear modelo para QTableView
            model = QStandardItemModel(len(clientes), 5)
            model.setHorizontalHeaderLabels([self.tr("Código"), self.tr("NIF/CIF"), self.tr("Nombre Fiscal"), self.tr("Teléfono"), self.tr("Email")])
            
            for row, cliente in enumerate(clientes):
                # Código
                item = QStandardItem(self._get_str(cliente, 'codigo_cliente'))
                item.setData(cliente.id, Qt.ItemDataRole.UserRole)
                item.setEditable(False)
                model.setItem(row, 0, item)
                
                # CIF/NIF
                item = QStandardItem(self._get_str(cliente, 'cif_nif_siren'))
                item.setEditable(False)
                model.setItem(row, 1, item)
                
                # Nombre Fiscal
                nombre_fiscal = self._get_str(cliente, 'nombre_fiscal') or (cliente.nombre_completo() if hasattr(cliente, 'nombre_completo') else '')
                item = QStandardItem(str(nombre_fiscal))
                item.setEditable(False)
                model.setItem(row, 2, item)
                
                # Teléfono
                item = QStandardItem(self._get_str(cliente, 'telefono1'))
                item.setEditable(False)
                model.setItem(row, 3, item)
                
                # Email
                item = QStandardItem(self._get_str(cliente, 'email'))
                item.setEditable(False)
                model.setItem(row, 4, item)
            
            tabla.setModel(model)
            tabla.resizeColumnsToContents()
            # Ajustar comportamiento de redimensionado de columnas mediante helper
            try:
                self._ajustar_encabezado_tabla(tabla, stretch_index=2)
            except Exception:
                pass
                
        except Exception as e:
            QMessageBox.warning(self, self.tr("Error"), self.tr("Error al cargar clientes: {}").format(str(e)))
    
    def filter_records(self, search_text: str, order_by: str, order_mode: str):
        """Filtra y ordena los registros de clientes según los criterios especificados.
        
        Args:
            search_text: Texto a buscar en código, NIF/CIF, nombre, teléfono o email
            order_by: Campo por el que ordenar ("Nombre Fiscal", "Código", "Fecha")
            order_mode: Modo de ordenación ("A-Z" o "Z-A")
        """
        try:
            # Obtener todos los clientes
            clientes = self.repository.obtener_todos()
            
            # Filtrar por texto de búsqueda (case-insensitive)
            if search_text:
                search_lower = search_text.lower()
                def str_lower(attr_val):
                    return attr_val.lower() if isinstance(attr_val, str) else str(attr_val).lower()
                clientes = [c for c in clientes if (
                    (search_lower in ((c.codigo_cliente or '')).lower()) or
                    (search_lower in ((c.cif_nif_siren or '')).lower()) or
                    (search_lower in ((c.nombre_fiscal or '')).lower()) or
                    (search_lower in ((c.nombre or '')).lower()) or
                    (search_lower in ((c.apellido1 or '')).lower()) or
                    (search_lower in ((c.apellido2 or '')).lower()) or
                    (search_lower in ((c.telefono1 or '')).lower()) or
                    (search_lower in ((c.email or '')).lower())
                )]
            
            # Ordenar según el campo especificado
            if order_by == "Código":
                clientes.sort(key=lambda c: c.codigo_cliente or "", reverse=(order_mode == "Z-A"))
            elif order_by == "Fecha":
                clientes.sort(key=lambda c: c.fecha_alta or date(1900, 1, 1), reverse=(order_mode == "Z-A"))
            else:  # "Nombre Fiscal" por defecto
                clientes.sort(key=lambda c: (c.nombre_fiscal or c.nombre_completo() or "").lower(), reverse=(order_mode == "Z-A"))
            
            # Actualizar la tabla con los resultados filtrados
            tabla = self._find_table()
            if not tabla:
                return
            
            # Si es QTableWidget
            if isinstance(tabla, QTableWidget):
                tabla.setRowCount(len(clientes))
                for row, cliente in enumerate(clientes):
                    # Código
                    item = QTableWidgetItem(self._get_str(cliente, 'codigo_cliente'))
                    item.setData(Qt.ItemDataRole.UserRole, cliente.id)
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    tabla.setItem(row, 0, item)
                    # CIF/NIF
                    item = QTableWidgetItem(self._get_str(cliente, 'cif_nif_siren'))
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    tabla.setItem(row, 1, item)
                    # Nombre Fiscal
                    nombre_fiscal = self._get_str(cliente, 'nombre_fiscal') or (cliente.nombre_completo() if hasattr(cliente, 'nombre_completo') else '')
                    item = QTableWidgetItem(str(nombre_fiscal))
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    tabla.setItem(row, 2, item)
                    # Teléfono
                    item = QTableWidgetItem(self._get_str(cliente, 'telefono1'))
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    tabla.setItem(row, 3, item)
                    # Email
                    item = QTableWidgetItem(self._get_str(cliente, 'email'))
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    tabla.setItem(row, 4, item)
                try:
                    self._ajustar_encabezado_tabla(tabla, stretch_index=2)
                except Exception:
                    pass
            
            # Si es QTableView
            elif isinstance(tabla, QTableView):
                model = QStandardItemModel(len(clientes), 5, self)
                model.setHorizontalHeaderLabels([self.tr("Código"), self.tr("NIF/CIF"), self.tr("Nombre Fiscal"), self.tr("Teléfono"), self.tr("Email")])
                for row, cliente in enumerate(clientes):
                    def std_item(text, cid):
                        it = QStandardItem(str(text or ""))
                        it.setEditable(False)
                        it.setData(cid, Qt.ItemDataRole.UserRole)
                        return it

                    model.setItem(row, 0, std_item(self._get_str(cliente, 'codigo_cliente'), cliente.id))
                    model.setItem(row, 1, std_item(self._get_str(cliente, 'cif_nif_siren'), cliente.id))
                    model.setItem(row, 2, std_item(self._get_str(cliente, 'nombre_fiscal') or (cliente.nombre_completo() if hasattr(cliente, 'nombre_completo') else ''), cliente.id))
                    model.setItem(row, 3, std_item(self._get_str(cliente, 'telefono1'), cliente.id))
                    model.setItem(row, 4, std_item(self._get_str(cliente, 'email'), cliente.id))
                tabla.setModel(model)
                tabla.resizeColumnsToContents()
                # Forzar comportamiento de resize similar al de la lista inicial
                try:
                    self._ajustar_encabezado_tabla(tabla, stretch_index=2)
                except Exception:
                    pass
                
        except Exception as e:
            QMessageBox.warning(self, self.tr("Error"), self.tr("Error al filtrar clientes: {}").format(str(e)))

    def apply_palette_styles(self):
        """Quita estilos forzados de colores para que el sistema use sus valores por defecto.

        En lugar de aplicar colores explícitos, limpiamos las `styleSheet` de widgets
        típicamente coloreados (QLabel, QLineEdit, QTextEdit, QTableView, QHeaderView)
        para que use el estilo/paleta del sistema o del tema del escritorio.
        """
        from PySide6.QtWidgets import QLabel, QLineEdit, QTextEdit, QTableView, QHeaderView

        targets = (QLabel, QLineEdit, QTextEdit, QTableView, QHeaderView)

        # Limpiar estilos en widgets referenciados directamente en self.ui
        for attr in dir(self.ui):
            try:
                w = getattr(self.ui, attr)
            except Exception:
                continue
            # Evitar tocar objetos que no sean widgets
            if not hasattr(w, 'metaObject'):
                continue

            try:
                name = getattr(w, 'objectName', lambda: None)()
                # Si el widget está en la lista de preservación, no tocar
                if name in self._preserve_styles:
                    continue

                # Si hay un estilo personalizado para este widget, aplicarlo
                if name and name in self._custom_styles:
                    try:
                        w.setStyleSheet(self._custom_styles[name])
                        continue
                    except Exception:
                        pass

                # Si el widget es uno de los tipos objetivo, limpiamos su stylesheet
                if isinstance(w, targets):
                    w.setStyleSheet("")
                else:
                    # Limpiar hijos de esos tipos dentro del widget (respetando preservaciones)
                    for t in targets:
                        try:
                            children = w.findChildren(t)
                            for ch in children:
                                ch_name = getattr(ch, 'objectName', lambda: None)()
                                if ch_name in self._preserve_styles:
                                    continue
                                if ch_name and ch_name in self._custom_styles:
                                    try:
                                        ch.setStyleSheet(self._custom_styles[ch_name])
                                        continue
                                    except Exception:
                                        pass
                                ch.setStyleSheet("")
                        except Exception:
                            continue
            except Exception:
                continue

        # También limpiar dentro de las páginas de QTabWidget si existiesen
        try:
            from PySide6.QtWidgets import QTabWidget
            tab_widgets = []
            for attr in dir(self.ui):
                try:
                    candidate = getattr(self.ui, attr)
                except Exception:
                    continue
                if isinstance(candidate, QTabWidget):
                    tab_widgets.append(candidate)

            try:
                tab_widgets.extend(self.findChildren(QTabWidget))
            except Exception:
                pass

            for tw in set(tab_widgets):
                for i in range(tw.count()):
                    page = tw.widget(i)
                    if not page:
                        continue
                    try:
                        for t in (QLabel, QLineEdit, QTextEdit):
                            for lbl in page.findChildren(t):
                                lbl_name = getattr(lbl, 'objectName', lambda: None)()
                                if lbl_name in self._preserve_styles:
                                    continue
                                if lbl_name and lbl_name in self._custom_styles:
                                    try:
                                        lbl.setStyleSheet(self._custom_styles[lbl_name])
                                        continue
                                    except Exception:
                                        pass
                                lbl.setStyleSheet("")
                    except Exception:
                        continue
        except Exception:
            pass
    
    def abrir_ficha_cliente(self):
        """Abre la ficha del cliente seleccionado"""
        # Obtener tabla
        tabla = getattr(self.ui, 'tabla_busquedas', None) or getattr(self.ui, 'tabla_clientes', None)
        if not tabla:
            return
        
        # Obtener fila seleccionada
        selection = tabla.selectionModel()
        if not selection.hasSelection():
            return
        
        index = selection.currentIndex()
        if not index.isValid():
            return
        
        # Obtener ID del cliente desde el modelo
        model = tabla.model()
        id_cliente = model.item(index.row(), 0).data(Qt.ItemDataRole.UserRole)
        
        # Cargar cliente
        self.cliente_actual = self.repository.obtener_por_id(id_cliente)
        if not self.cliente_actual:
            QMessageBox.warning(self, self.tr("Error"), self.tr("No se pudo cargar el cliente"))
            return
        
        # Cargar datos en formulario
        self.cargar_datos_en_formulario(self.cliente_actual)
        
        # Cambiar a página de edición (índice 0)
        self.ui.stackedWidget.setCurrentIndex(0)
    
    def cargar_datos_en_formulario(self, cliente: Cliente):
        """Carga los datos del cliente en los campos del formulario"""
        # Campos principales
        if hasattr(self.ui, 'txtcodigo_cliente'):
            self.ui.txtcodigo_cliente.setText(self._get_str(cliente, 'codigo_cliente'))
        if hasattr(self.ui, 'txtcif_nif'):
            self.ui.txtcif_nif.setText(self._get_str(cliente, 'cif_nif_siren'))
        if hasattr(self.ui, 'txtnombre'):
            self.ui.txtnombre.setText(self._get_str(cliente, 'nombre'))
        if hasattr(self.ui, 'txtPrimerApellido'):
            self.ui.txtPrimerApellido.setText(self._get_str(cliente, 'apellido1'))
        if hasattr(self.ui, 'txtSegundoApellido'):
            self.ui.txtSegundoApellido.setText(self._get_str(cliente, 'apellido2'))
        if hasattr(self.ui, 'txtnombre_fiscal'):
            val_fiscal = self._get_str(cliente, 'nombre_fiscal')
            self.ui.txtnombre_fiscal.setText(val_fiscal)
        if hasattr(self.ui, 'txtnombre_comercial'):
            self.ui.txtnombre_comercial.setText(self._get_str(cliente, 'nombre_comercial'))
        
        # Dirección
        if hasattr(self.ui, 'txtdireccion1'):
            self.ui.txtdireccion1.setText(self._get_str(cliente, 'direccion1'))
        if hasattr(self.ui, 'txtdireccion2'):
            self.ui.txtdireccion2.setText(self._get_str(cliente, 'direccion2'))
        if hasattr(self.ui, 'txtcp'):
            self.ui.txtcp.setText(self._get_str(cliente, 'cp'))
        if hasattr(self.ui, 'txtpoblacion'):
            self.ui.txtpoblacion.setText(self._get_str(cliente, 'poblacion'))
        if hasattr(self.ui, 'txtprovincia'):
            self.ui.txtprovincia.setText(self._get_str(cliente, 'provincia'))
        # Otros campos que pueden no estar definidos en la UI
        if hasattr(self.ui, 'txtCifIntracomunitario'):
            self.ui.txtCifIntracomunitario.setText(self._get_str(cliente, 'cif_vies'))
        w = getattr(self.ui, 'txtSiret', None)
        if w is not None:
            w.setText(self._get_str(cliente, 'siret'))
        w = getattr(self.ui, 'txtpersona_contacto', None)
        if w is not None:
            w.setText(self._get_str(cliente, 'persona_contacto'))
        
        # Contacto
        if hasattr(self.ui, 'txttelefono1'):
            self.ui.txttelefono1.setText(self._get_str(cliente, 'telefono1'))
        if hasattr(self.ui, 'txttelefono2'):
            self.ui.txttelefono2.setText(self._get_str(cliente, 'telefono2'))
        if hasattr(self.ui, 'txtmovil'):
            self.ui.txtmovil.setText(self._get_str(cliente, 'movil'))
        w = getattr(self.ui, 'txtfax', None)
        if w is not None:
            w.setText(self._get_str(cliente, 'fax'))
        if hasattr(self.ui, 'txtemail'):
            self.ui.txtemail.setText(self._get_str(cliente, 'email'))
        if hasattr(self.ui, 'txtweb'):
            self.ui.txtweb.setText(self._get_str(cliente, 'web'))
        
        # Actualizar label con nombre del cliente
        if hasattr(self.ui, 'txtNombreFiscal'):
            try:
                self.ui.txtNombreFiscal.setText(str(cliente.nombre_completo()))
            except Exception:
                self.ui.txtNombreFiscal.setText(self._get_str(cliente, 'nombre_fiscal'))
        # Establecer comboboxes por itemData si existe, else por index
        try:
            if hasattr(self.ui, 'cboDivisa'):
                for i in range(self.ui.cboDivisa.count()):
                    itemdata = self.ui.cboDivisa.itemData(i)
                    if itemdata is not None and cliente.id_divisa is not None and int(itemdata) == cliente.id_divisa:
                        self.ui.cboDivisa.setCurrentIndex(i)
                        break
        except Exception:
            pass
        try:
            if hasattr(self.ui, 'cboforma_pago'):
                for i in range(self.ui.cboforma_pago.count()):
                    itemdata = self.ui.cboforma_pago.itemData(i)
                    if itemdata is not None and cliente.id_forma_pago is not None and int(itemdata) == cliente.id_forma_pago:
                        self.ui.cboforma_pago.setCurrentIndex(i)
                        break
        except Exception:
            pass
        try:
            if hasattr(self.ui, 'cbotarifa_cliente'):
                for i in range(self.ui.cbotarifa_cliente.count()):
                    itemdata = self.ui.cbotarifa_cliente.itemData(i)
                    if itemdata is not None and cliente.id_tarifa is not None and int(itemdata) == cliente.id_tarifa:
                        self.ui.cbotarifa_cliente.setCurrentIndex(i)
                        break
        except Exception:
            pass
        try:
            if hasattr(self.ui, 'cboagente'):
                for i in range(self.ui.cboagente.count()):
                    itemdata = self.ui.cboagente.itemData(i)
                    if itemdata is not None and cliente.id_agente is not None and int(itemdata) == cliente.id_agente:
                        self.ui.cboagente.setCurrentIndex(i)
                        break
        except Exception:
            pass
        try:
            if hasattr(self.ui, 'cbotransportista'):
                for i in range(self.ui.cbotransportista.count()):
                    itemdata = self.ui.cbotransportista.itemData(i)
                    if itemdata is not None and cliente.id_transportista is not None and int(itemdata) == cliente.id_transportista:
                        self.ui.cbotransportista.setCurrentIndex(i)
                        break
        except Exception:
            pass
        try:
            if hasattr(self.ui, 'cboidiomaDocumentos'):
                for i in range(self.ui.cboidiomaDocumentos.count()):
                    itemdata = self.ui.cboidiomaDocumentos.itemData(i)
                    if itemdata is not None and cliente.id_idioma_documentos is not None and int(itemdata) == cliente.id_idioma_documentos:
                        self.ui.cboidiomaDocumentos.setCurrentIndex(i)
                        break
        except Exception:
            pass
        try:
            if hasattr(self.ui, 'cboPais'):
                for i in range(self.ui.cboPais.count()):
                    itemdata = self.ui.cboPais.itemData(i)
                    if itemdata is not None and cliente.id_pais is not None and int(itemdata) == cliente.id_pais:
                        self.ui.cboPais.setCurrentIndex(i)
                        break
        except Exception:
            pass
        
        # Cargar datos adicionales
        cid = cliente.id if cliente is not None else None
        if cid is not None:
            try:
                self.cargar_direcciones_alternativas(int(cid))
            except Exception:
                self.cargar_direcciones_alternativas(cid)
            try:
                self.cargar_deudas(int(cid))
            except Exception:
                self.cargar_deudas(cid)
            try:
                self.cargar_estadisticas(int(cid))
            except Exception:
                self.cargar_estadisticas(cid)
        # Validar campos para mostrar iconos al cargar cliente
        for vn in ('txtcodigo_cliente', 'txtnombre', 'txtnombre_fiscal', 'txtcif_nif', 'txtemail', 'txtcuenta_corriente', 'txtiban', 'txtdia_pago1', 'txtdia_pago2'):
            try:
                self._validate_and_apply(vn)
            except Exception:
                continue
        self._update_form_validity()
    
    def cargar_direcciones_alternativas(self, id_cliente: int):
        """Carga direcciones alternativas en la tabla correspondiente"""
        if not hasattr(self.ui, 'lista_direccionesAlternativas'):
            return
        
        direcciones = self.repository.obtener_direcciones(id_cliente)
        # Implementar carga en lista/tabla
    
    def cargar_deudas(self, id_cliente: int):
        """Carga las deudas del cliente"""
        if not hasattr(self.ui, 'TablaDeudas'):
            return
        
        deudas = self.repository.obtener_deudas(id_cliente, solo_pendientes=True)
        # Implementar carga en tabla
    
    def cargar_estadisticas(self, id_cliente: int):
        """Carga estadísticas del cliente"""
        anio_actual = date.today().year
        stats = self.repository.obtener_estadisticas_mes(id_cliente, anio_actual)
        
        # Mapear a los campos del formulario
        meses_map = {
            1: 'txtEnero', 2: 'txtFebrero', 3: 'txtMarzo', 4: 'txtAbril',
            5: 'txtMayo', 6: 'txtJunio', 7: 'txtjulio', 8: 'txtAgosto',
            9: 'txtSeptiembre', 10: 'txtOctubre', 11: 'txtNoviembre', 12: 'txtDiciembre'
        }
        
        for mes, nombre_campo in meses_map.items():
            if hasattr(self.ui, nombre_campo):
                importe = stats.get(mes, 0.0)
                getattr(self.ui, nombre_campo).setText(f"{importe:.2f}")
    
    def nuevo_cliente(self):
        """Crea un nuevo cliente"""
        self.cliente_actual = None
        self.limpiar_formulario()
        self.desactivar_botones_navegacion()
        self._modo_edicion = True  # Activar modo edición
        self.ui.stackedWidget.setCurrentIndex(0)
        
        # Generar código único automáticamente
        try:
            codigo_generado = self.repository._generar_codigo()
            if hasattr(self.ui, 'txtcodigo_cliente'):
                self.ui.txtcodigo_cliente.setText(codigo_generado)
        except Exception as e:
            print(f"Error al generar código: {e}")
        
        # Asegurar que txtnombre_fiscal esté vacío para que se auto-rellene
        if hasattr(self.ui, 'txtnombre_fiscal'):
            self.ui.txtnombre_fiscal.clear()
        
        self.activar_campos_edicion()  # Activar campos para edición
        # Force initial validation state
        self._set_all_valid_state()
        self._update_form_validity()
        
        # Reconstruir pestañas del tabwidget si es necesario
        if hasattr(self.ui, 'tabwidget') and self.ui.tabwidget.count() == 0:
            # Las pestañas se perdieron, intentar reconstruirlas
            tab_names = ['tab_datos', 'tab_direcciones', 'tab_Datos_bancarios_financieros', 
                        'tab_estadistica', 'tab_deudas', 'tab_coments', 'tab_3']
            tab_texts = ['', '', '', '', '', '', '']  # Los textos se definen en retranslateUi
            
            for i, tab_name in enumerate(tab_names):
                tab_widget = getattr(self.ui, tab_name, None)
                if tab_widget:
                    self.ui.tabwidget.addTab(tab_widget, tab_texts[i])
        
        # Forzar actualización del tabwidget
        if hasattr(self.ui, 'tabwidget'):
            self.ui.tabwidget.update()
            self.ui.tabwidget.repaint()
    
    def editar_cliente(self):
        """Edita el cliente seleccionado"""
        # Si ya tenemos un cliente cargado y estamos en la ficha (página 0), editar directamente
        if self.cliente_actual is not None and hasattr(self.ui, 'stackedWidget') and self.ui.stackedWidget.currentIndex() == 0:
            self.desactivar_botones_navegacion()
            self._modo_edicion = True  # Activar modo edición
            self.activar_campos_edicion()  # Activar campos para edición
            # Ensure validation applied to loaded data
            if hasattr(self, '_on_widget_change'):
                self._validate_and_apply('txtcodigo_cliente')
                self._validate_and_apply('txtcif_nif')
                self._validate_and_apply('txtnombre')
                self._validate_and_apply('txtnombre_fiscal')
            self._update_form_validity()
            return

        # Si no, buscar en la tabla
        tabla = getattr(self.ui, 'tabla_busquedas', None) or getattr(self.ui, 'tabla_clientes', None)
        if not tabla:
            return
        
        # Verificar que hay un cliente seleccionado
        selection = tabla.selectionModel()
        if not selection.hasSelection():
            QMessageBox.warning(self, self.tr("Aviso"), self.tr("Seleccione un cliente para editar"))
            return
        self.desactivar_botones_navegacion()
        self._modo_edicion = True  # Activar modo edición
        self.abrir_ficha_cliente()
        self.activar_campos_edicion()  # Activar campos para edición
        # Ensure validation applied to loaded data
        if hasattr(self, '_on_widget_change'):
            self._validate_and_apply('txtcodigo_cliente')
            self._validate_and_apply('txtcif_nif')
            self._validate_and_apply('txtnombre')
            self._validate_and_apply('txtnombre_fiscal')
        self._update_form_validity()
    
    def borrar_cliente(self):
        """Borra el cliente seleccionado"""
        tabla = getattr(self.ui, 'tabla_busquedas', None) or getattr(self.ui, 'tabla_clientes', None)
        if not tabla:
            return
        
        # Obtener fila seleccionada
        selection = tabla.selectionModel()
        if not selection.hasSelection():
            QMessageBox.warning(self, self.tr("Aviso"), self.tr("Seleccione un cliente para borrar"))
            return
        
        index = selection.currentIndex()
        if not index.isValid():
            return
        
        # Obtener ID del cliente
        model = tabla.model()
        id_cliente = model.item(index.row(), 0).data(Qt.ItemDataRole.UserRole)
        cliente = self.repository.obtener_por_id(id_cliente)
        
        if not cliente:
            return
        
        respuesta = QMessageBox.question(
            self,
            self.tr("Confirmar borrado"),
            self.tr("¿Está seguro de que desea borrar el cliente '{}'?").format(cliente.nombre_completo()),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if respuesta == QMessageBox.StandardButton.Yes:
            try:
                self.repository.eliminar(id_cliente)
                QMessageBox.information(self, self.tr("Éxito"), self.tr("Cliente borrado correctamente"))
                self.cargar_clientes()
            except ValueError as e:
                QMessageBox.warning(self, self.tr("No se puede borrar"), str(e))
            except Exception as e:
                QMessageBox.critical(self, self.tr("Error"), self.tr("Error al borrar: {}").format(str(e)))
    
    def guardar_cliente(self):
        """Guarda el cliente actual"""
        try:
            # helper lambdas for conversion (moved here so both branches can use them)
            def txt(name):
                w = getattr(self.ui, name, None)
                if not w:
                    return ''
                # QTextEdit has toPlainText, QLineEdit has text
                if hasattr(w, 'toPlainText'):
                    return w.toPlainText() or ''
                if hasattr(w, 'text'):
                    return w.text() or ''
                return ''
            def val_int(name):
                try:
                    w = getattr(self.ui, name, None)
                    if w is None:
                        return None
                    v = w.value() if hasattr(w, 'value') else int(w.text()) if w.text() else None
                    return int(v) if v is not None else None
                except Exception:
                    return None
            def val_float(name):
                try:
                    w = getattr(self.ui, name, None)
                    if w is None:
                        return None
                    t = w.text() if hasattr(w, 'text') else None
                    if t is None or t == '':
                        return None
                    return float(t)
                except Exception:
                    return None
            def val_bool(name):
                try:
                    w = getattr(self.ui, name, None)
                    if w is None:
                        return False
                    return bool(w.isChecked())
                except Exception:
                    return False
            def val_qdate_to_date(name):
                try:
                    w = getattr(self.ui, name, None)
                    if w is None:
                        return None
                    from datetime import date as _date
                    d = w.date()
                    return _date(d.year(), d.month(), d.day())
                except Exception:
                    return None
            def get_combo_value(name):
                w = getattr(self.ui, name, None)
                if w is None:
                    return None
                try:
                    idx = w.currentIndex()
                    val = w.itemData(idx)
                    return val if val is not None else idx
                except Exception:
                    return None
            # Validar campos antes de construir el mapeo (y antes de guardar)
            ok, errores = self._validar_campos()
            if not ok:
                QMessageBox.warning(self, self.tr("Validación"), "\n".join(errores))
                return
            # Declarative mappings for fields (attribute name in model -> widget name)
            txt_map = [
                ('codigo_cliente','txtcodigo_cliente'), ('cif_nif_siren','txtcif_nif'), ('nombre','txtnombre'),
                ('apellido1','txtPrimerApellido'), ('apellido2','txtSegundoApellido'), ('nombre_fiscal','txtnombre_fiscal'),
                ('nombre_comercial','txtnombre_comercial'), ('direccion1','txtdireccion1'), ('direccion2','txtdireccion2'),
                ('cp','txtcp'), ('poblacion','txtpoblacion'), ('provincia','txtprovincia'), ('telefono1','txttelefono1'),
                ('telefono2','txttelefono2'), ('movil','txtmovil'), ('fax','txtfax'), ('email','txtemail'),
                ('web','txtweb'), ('siret','txtSiret'), ('cif_vies','txtCifIntracomunitario'), ('persona_contacto','txtpersona_contacto'),
                ('entidad_bancaria','txtentidad_bancaria'), ('oficina_bancaria','txtoficina_bancaria'), ('dc','txtdc'),
                ('cuenta_corriente','txtcuenta_corriente'), ('acceso_web','txtacceso_web'), ('password_web','txtpassword_web'),
                ('cuenta_contable','txtcuenta_contable'), ('cuenta_iva_repercutido','txtcuenta_iva_repercutido'),
                ('cuenta_deudas','txtcuenta_deudas'), ('cuenta_cobros','txtcuenta_cobros'), ('visa_distancia1','txtvisa_distancia1'),
                ('visa_distancia2','txtvisa_distancia2'), ('comentarios','txtcomentarios'), ('comentario_bloqueo','txtcomentario_bloqueo'),
                ('observaciones','txtObservaciones')
            ]
            date_map = [('fecha_alta','txtfecha_alta'), ('fecha_nacimiento','txtfecha_nacimiento'), ('fecha_ultima_compra','txtfecha_ultima_compra')]
            int_map = [('dia_pago1','txtdia_pago1'), ('dia_pago2','txtdia_pago2'), ('visa1_caduca_mes','txtvisa1_caduca_mes'),
                       ('visa2_caduca_mes','txtvisa2_caduca_mes'), ('visa1_caduca_ano','txtvisa1_caduca_ano'), ('visa2_caduca_ano','txtvisa2_caduca_ano'),
                       ('visa1_cod_valid','txtvisa1_cod_valid'), ('visa2_cod_valid','txtvisa2_cod_valid')]
            float_map = [('acumulado_ventas','txtimporteAcumulado'), ('ventas_ejercicio','txtventas_ejercicio'), ('riesgo_maximo','txtrRiesgoPermitido'),
                         ('deuda_actual','txtdeuda_actual'), ('porc_dto_cliente','txtporc_dto_cliente'), ('importe_a_cuenta','txtimporte_a_cuenta'),
                         ('vales','txtvales')]
            bool_map = [('recargo_equivalencia','chkrecargo_equivalencia'), ('irpf','chkClienteEmpresa'), ('bloqueado','chklBloqueoCliente')]
            cbo_map = [('id_idioma_documentos','cboidiomaDocumentos'), ('id_pais','cboPais'), ('id_divisa','cboDivisa'),
                       ('id_forma_pago','cboforma_pago'), ('id_tarifa','cbotarifa_cliente'), ('id_agente','cboagente'), ('id_transportista','cbotransportista')]

            if self.cliente_actual:
                # Actualizar campos (UI -> Modelo) usando los mapeos
                for attr, widget_name in txt_map:
                    w = getattr(self.ui, widget_name, None)
                    if w is not None:
                        setattr(self.cliente_actual, attr, txt(widget_name))

                for attr, widget_name in date_map:
                    v = val_qdate_to_date(widget_name)
                    if v is not None:
                        setattr(self.cliente_actual, attr, v)

                for attr, widget_name in int_map:
                    v = val_int(widget_name)
                    if v is not None:
                        setattr(self.cliente_actual, attr, v)

                for attr, widget_name in float_map:
                    v = val_float(widget_name)
                    if v is not None:
                        setattr(self.cliente_actual, attr, v)

                for attr, widget_name in bool_map:
                    w = getattr(self.ui, widget_name, None)
                    if w is not None:
                        setattr(self.cliente_actual, attr, val_bool(widget_name))

                # Comboboxes (IDs)
                for attr, widget_name in cbo_map:
                    try:
                        w = getattr(self.ui, widget_name, None)
                        if w is not None:
                            setattr(self.cliente_actual, attr, get_combo_value(widget_name))
                    except Exception:
                        continue
                # Persistir cambios en la base de datos usando el repositorio
                try:
                    # Debug log: indicate update attempt
                    try:
                        cid = getattr(self.cliente_actual, 'id', None)
                    except Exception:
                        cid = None
                    print(f"[DEBUG] guardar_cliente: calling repository.actualizar id={cid}")
                    # Use repository.actualizar para asegurar commit y registro de historial
                    self.repository.actualizar(self.cliente_actual)
                    print(f"[DEBUG] guardar_cliente: repository.actualizar succeeded for id={cid}")
                except Exception as e:
                    # Log exception and traceback for debugging
                    print(f"[ERROR] guardar_cliente: repository.actualizar raised: {e}")
                    import traceback
                    traceback.print_exc()
                    # Fallback: si el repositorio falla, intentar commit directo
                    try:
                        print("[DEBUG] guardar_cliente: attempting session.commit() fallback")
                        self.session.commit()
                        print("[DEBUG] guardar_cliente: session.commit() fallback succeeded")
                    except Exception:
                        print("[ERROR] guardar_cliente: session.commit() fallback failed")
                
            else:
                # Crear nuevo de forma declarativa con mapping
                cliente_kwargs = {}
                for attr, widget_name in txt_map:
                    w = getattr(self.ui, widget_name, None)
                    if w is not None:
                        val = txt(widget_name)
                        if val != '':
                            cliente_kwargs[attr] = val

                for attr, widget_name in date_map:
                    v = val_qdate_to_date(widget_name)
                    if v is not None:
                        cliente_kwargs[attr] = v

                for attr, widget_name in int_map:
                    v = val_int(widget_name)
                    if v is not None:
                        cliente_kwargs[attr] = v

                for attr, widget_name in float_map:
                    v = val_float(widget_name)
                    if v is not None:
                        cliente_kwargs[attr] = v

                for attr, widget_name in bool_map:
                    w = getattr(self.ui, widget_name, None)
                    if w is not None:
                        cliente_kwargs[attr] = val_bool(widget_name)

                for attr, widget_name in cbo_map:
                    v = get_combo_value(widget_name)
                    if v is not None:
                        cliente_kwargs[attr] = v

                # Los días de pago a 0 por defecto si no existe
                if 'dia_pago1' not in cliente_kwargs:
                    v = val_int('txtdia_pago1')
                    cliente_kwargs['dia_pago1'] = v if v is not None else 0
                if 'dia_pago2' not in cliente_kwargs:
                    v = val_int('txtdia_pago2')
                    cliente_kwargs['dia_pago2'] = v if v is not None else 0

                cliente = Cliente(**cliente_kwargs)
                self.repository.crear(cliente)
                QMessageBox.information(self, self.tr("Éxito"), self.tr("Cliente creado"))
            
            self.cargar_clientes()
            # Mantenerse en la página de edición pero desactivar campos
            # (no volver a la lista de clientes). El usuario pidió que
            # tras guardar se queden los campos visibles pero no editables.
            try:
                self.desactivar_campos_edicion()
            except Exception:
                pass
            # Restablecer el modo edición y botones de navegación
            self._modo_edicion = False
            self.activar_botones_navegacion()
            
        except Exception as e:
            QMessageBox.critical(self, self.tr("Error"), self.tr("Error al guardar: {}").format(str(e)))
    
    def deshacer_cambios(self):
        """Deshace los cambios y recarga los datos del cliente actual"""
        if self.cliente_actual:
            # Recargar datos del cliente actual
            self.abrir_ficha_cliente()
        else:
            # Si es un cliente nuevo, limpiar el formulario
            self.limpiar_formulario()
    
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario de datos del cliente"""
        from PySide6.QtWidgets import QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit, QCheckBox, QLabel
        from PySide6.QtCore import QDate

        # Recorrer todos los widgets y limpiarlos según su tipo
        for widget_name in dir(self.ui):
            if widget_name.startswith('_'):
                continue

            widget = getattr(self.ui, widget_name)

            # QLineEdit, QTextEdit - limpiar texto
            if isinstance(widget, (QLineEdit, QTextEdit)):
                widget.clear()

            # QLabel que empiecen con 'txt' (campos de visualización de datos del cliente)
            elif isinstance(widget, QLabel) and widget_name.startswith('txt'):
                widget.setText("")

            # QComboBox - seleccionar primer elemento si existe
            elif isinstance(widget, QComboBox):
                if widget.count() > 0:
                    widget.setCurrentIndex(0)

            # QSpinBox, QDoubleSpinBox - resetear a valor mínimo
            elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
                # set minimum using appropriate type
                if isinstance(widget, QSpinBox):
                    widget.setValue(int(widget.minimum()))
                else:
                    widget.setValue(float(widget.minimum()))

            # QDateEdit - resetear a fecha actual
            elif isinstance(widget, QDateEdit):
                widget.setDate(QDate.currentDate())

            # QCheckBox - desmarcar
            elif isinstance(widget, QCheckBox):
                widget.setChecked(False)
        # Reset validation visuals
        self._set_all_valid_state()

    def _set_all_valid_state(self):
        """Clear validation visuals for all known widgets"""
        from PySide6.QtWidgets import QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit, QCheckBox
        for widget_name in dir(self.ui):
            if widget_name.startswith('_'):
                continue
            w = getattr(self.ui, widget_name)
            if isinstance(w, (QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit, QCheckBox)):
                try:
                    w.setStyleSheet("")
                    w.setToolTip("")
                    # Clear any validation visuals (we removed status labels)
                except Exception:
                    continue

    def _ensure_status_label(self, widget):
        """Placeholder: no-op for historical status label creation.

        This function used to create dynamic QLabel widgets next to inputs to show
        validation icons; they have been removed (icons caused black artifacts).
        The function remains as a compatibility no-op for calls elsewhere.
        """
        # This project no longer shows status icons via QLabels; return None to keep API-compatible.
        return None
        # previously created a QLabel for status icons; icons removed as requested
        return None

    def _apply_widget_valid_state(self, widget, error_message: str | None):
        """Apply styling (red border and tooltip) if invalid, clear if None/empty"""
        if widget is None:
            return
        try:
            if not error_message:
                # Clear style
                widget.setStyleSheet("")
                widget.setToolTip("")
            else:
                # Apply invalid style and tooltip (no more icons)
                widget.setToolTip(error_message)
                try:
                    # Use a subtle red border to mark invalid fields
                    widget.setStyleSheet("border: 1px solid #ff4d4f; border-radius: 2px;")
                except Exception:
                    # Be defensive: ignore style errors
                    pass
            # If valid, we simply clear visual validation states (no icons)
            if not error_message:
                try:
                    widget.setStyleSheet("")
                    widget.setToolTip("")
                except Exception:
                    pass
        except Exception:
            pass

    def _on_widget_change(self, *args, **kwargs):
        """Slot called when a widget changes; validates the related field and updates the form validity"""
        if not getattr(self, '_modo_edicion', False):
            return
        sender = self.sender()
        if sender is None:
            return
        name = getattr(sender, 'objectName', lambda: None)()
        if not name:
            return
        # After any name/ surname change, attempt to fill nombre_fiscal if it's empty
        if name in ('txtnombre', 'txtPrimerApellido', 'txtSegundoApellido'):
            try:
                self._maybe_fill_nombre_fiscal()
            except Exception:
                pass
        # Handle postal code lookup
        if name == 'txtcp':
            try:
                self._handle_postal_code_change()
            except Exception:
                pass
        self._validate_and_apply(str(name))

    def _on_nombre_fiscal_manual_edit(self, text):
        """Called when user manually edits the txtnombre_fiscal field.
        
        Marks the field as manually edited so auto-fill stops overwriting it.
        """
        if hasattr(self.ui, 'txtnombre_fiscal'):
            w = self.ui.txtnombre_fiscal
            # Mark as manually edited - auto-fill will stop updating
            w._auto_filled = False

    def _maybe_fill_nombre_fiscal(self):

        """Compute `nombre_fiscal` from apellidos/nombre and fill automatically.

        Rule: apellido1 + ' ' + apellido2 + ' ' + nombre (all uppercase). If apellido2 empty,
        omit it. If both surnames empty, use `nombre`. 
        
        Updates automatically unless the user has manually edited the nombre_fiscal field.
        """
        ui = getattr(self, 'ui', None)
        if ui is None:
            return
        try:
            w_ap1 = getattr(ui, 'txtPrimerApellido', None)
            w_ap2 = getattr(ui, 'txtSegundoApellido', None)
            w_nombre = getattr(ui, 'txtnombre', None)
            w_nombre_fiscal = getattr(ui, 'txtnombre_fiscal', None)
            a1 = w_ap1.text().strip() if (w_ap1 is not None and hasattr(w_ap1, 'text')) else ''
            a2 = w_ap2.text().strip() if (w_ap2 is not None and hasattr(w_ap2, 'text')) else ''
            nombre = w_nombre.text().strip() if (w_nombre is not None and hasattr(w_nombre, 'text')) else ''
            
            # If target field not present, nothing to do
            if w_nombre_fiscal is None or not hasattr(w_nombre_fiscal, 'text') or not hasattr(w_nombre_fiscal, 'setText'):
                return
            
            # Compute what the nombre_fiscal should be
            parts = []
            if a1:
                parts.append(a1)
            if a2:
                parts.append(a2)
            if (a1 or a2) and nombre:
                parts.append(nombre)
            if not parts and nombre:
                parts = [nombre]
            computed = ' '.join(parts).strip().upper()
            
            # Get current value
            current = w_nombre_fiscal.text().strip().upper()
            
            # Check if user has manually edited the field
            # If the current value doesn't match what we would auto-generate from the last known state,
            # it means the user edited it manually. In that case, don't auto-update.
            # We track this with a flag on the widget itself.
            if not hasattr(w_nombre_fiscal, '_auto_filled'):
                w_nombre_fiscal._auto_filled = True
            
            # If current value matches the computed value, or if it's empty, update it
            # This allows continuous updates while typing
            if current == computed or not current:
                w_nombre_fiscal._auto_filled = True
                if computed:
                    try:
                        w_nombre_fiscal.setText(computed)
                    except Exception:
                        pass
            else:
                # Current value doesn't match computed - user may have edited manually
                # Only update if the flag says it was auto-filled before
                if getattr(w_nombre_fiscal, '_auto_filled', True):
                    if computed:
                        try:
                            w_nombre_fiscal.setText(computed)
                        except Exception:
                            pass
            
            # Also update label `txtNombreFiscal` if present (UI read-only label)
            lbl = getattr(ui, 'txtNombreFiscal', None)
            if lbl is not None and hasattr(lbl, 'setText'):
                try:
                    if computed:
                        lbl.setText(computed)
                except Exception:
                    pass
        except Exception:
            pass
        self._update_form_validity()

    def _validate_and_apply(self, widget_name: str):
        """Check a single named widget and apply validation state"""
        if not widget_name:
            return
        # Map widget name to validation
        # Txtcif_nif validation
        if widget_name == 'txtcif_nif':
            w = getattr(self.ui, 'txtcif_nif', None)
            txt = w.text() if (w is not None and hasattr(w, 'text')) else ''
            
            # Validar formato
            if txt and not self._is_valid_nif_cif(txt):
                self._apply_widget_valid_state(w, 'NIF/CIF/SIRET inválido')
            else:
                self._apply_widget_valid_state(w, None)
                
                # Verificar duplicados solo si el formato es válido y estamos en modo edición
                if txt and txt.strip() and getattr(self, '_modo_edicion', False):
                    cliente_existente = self._check_duplicate_cif(txt)
                    if cliente_existente:
                        # Mostrar diálogo en el siguiente ciclo de eventos para no bloquear la validación
                        from PySide6.QtCore import QTimer
                        QTimer.singleShot(100, lambda: self._handle_duplicate_cif(cliente_existente))


        # Email
        elif widget_name == 'txtemail':
            w = getattr(self.ui, 'txtemail', None)
            txt = w.text() if (w is not None and hasattr(w, 'text')) else ''
            if txt and txt.strip():
                import re
                if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", txt.strip()):
                    self._apply_widget_valid_state(w, 'Formato de email inválido')
                else:
                    self._apply_widget_valid_state(w, None)
            else:
                self._apply_widget_valid_state(w, None)

        # Codigo cliente (required)
        elif widget_name == 'txtcodigo_cliente':
            w = getattr(self.ui, 'txtcodigo_cliente', None)
            txt = w.text() if (w is not None and hasattr(w, 'text')) else ''
            if not txt or not txt.strip():
                self._apply_widget_valid_state(w, 'Código obligatorio')
            else:
                self._apply_widget_valid_state(w, None)

        # Nombre / Nombre fiscal - both interplay
        elif widget_name in ('txtnombre', 'txtnombre_fiscal'):
            w1 = getattr(self.ui, 'txtnombre', None)
            w2 = getattr(self.ui, 'txtnombre_fiscal', None)
            v1 = w1.text() if (w1 is not None and hasattr(w1, 'text')) else ''
            v2 = w2.text() if (w2 is not None and hasattr(w2, 'text')) else ''
            if (not v1 or not v1.strip()) and (not v2 or not v2.strip()):
                # mark both invalid
                self._apply_widget_valid_state(w1, 'Se requiere un nombre o nombre fiscal')
                self._apply_widget_valid_state(w2, 'Se requiere un nombre o nombre fiscal')
            else:
                self._apply_widget_valid_state(w1, None)
                self._apply_widget_valid_state(w2, None)

        # If any of the name fields changed recompute nombre_fiscal if empty
        if widget_name in ('txtPrimerApellido', 'txtSegundoApellido', 'txtnombre'):
            try:
                self._maybe_fill_nombre_fiscal()
            except Exception:
                pass

        # Días de pago
        elif widget_name in ('txtdia_pago1', 'txtdia_pago2'):
            w = getattr(self.ui, widget_name, None)
            try:
                if w is None:
                    val = None
                else:
                    val = int(w.value()) if hasattr(w, 'value') else int(w.text()) if (hasattr(w, 'text') and w.text()) else None
                if val is not None and not (0 <= val <= 31):
                    self._apply_widget_valid_state(w, 'Día fuera de rango 0-31')
                else:
                    self._apply_widget_valid_state(w, None)
            except Exception:
                self._apply_widget_valid_state(w, 'Día no válido')

        # CCC (cuenta bancaria)
        elif widget_name == 'txtcuenta_corriente':
            w = getattr(self.ui, 'txtcuenta_corriente', None)
            txt = w.text() if (w is not None and hasattr(w, 'text')) else ''
            if txt and txt.strip():
                if not self._is_valid_ccc(txt):
                    self._apply_widget_valid_state(w, 'Cuenta bancaria (CCC) inválida')
                else:
                    self._apply_widget_valid_state(w, None)
            else:
                self._apply_widget_valid_state(w, None)

        # IBAN if present
        elif widget_name in ('txtiban', 'txtCuentaIBAN'):
            w = getattr(self.ui, widget_name, None)
            txt = w.text() if (w is not None and hasattr(w, 'text')) else ''
            if txt and txt.strip():
                if not self._is_valid_iban(txt):
                    self._apply_widget_valid_state(w, 'IBAN inválido')
                else:
                    self._apply_widget_valid_state(w, None)
            else:
                self._apply_widget_valid_state(w, None)

        else:
            # Reset style for unhandled widgets
            w = getattr(self.ui, widget_name, None)
            if w is not None:
                self._apply_widget_valid_state(w, None)

    def _check_duplicate_cif(self, cif: str):
        """Verifica si existe un cliente con el CIF dado (excluyendo el actual)
        
        Returns:
            Cliente existente si hay duplicado, None si no hay duplicado
        """
        if not cif or not cif.strip():
            return None
        
        try:
            cliente_existente = self.repository.obtener_por_cif(cif.strip())
            
            # Si existe y NO es el cliente actual
            if cliente_existente and (
                self.cliente_actual is None or 
                cliente_existente.id != self.cliente_actual.id
            ):
                return cliente_existente
        except Exception as e:
            print(f"Error al verificar CIF duplicado: {e}")
        
        return None

    def _handle_duplicate_cif(self, cliente_existente):
        """Maneja el caso de CIF duplicado con diálogo al usuario"""
        from PySide6.QtWidgets import QMessageBox
        
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle(self.tr("CIF/NIF Duplicado"))
        msg.setText(
            self.tr("Ya existe un cliente con el CIF/NIF") + f": {cliente_existente.cif_nif_siren}\n\n" +
            self.tr("Cliente") + f": {cliente_existente.nombre_fiscal}\n" +
            self.tr("Código") + f": {cliente_existente.codigo_cliente}"
        )
        msg.setInformativeText(self.tr("¿Qué desea hacer?"))
        
        btn_cargar = msg.addButton(self.tr("Cargar cliente existente"), QMessageBox.ButtonRole.AcceptRole)
        btn_deshacer = msg.addButton(self.tr("Deshacer cambios"), QMessageBox.ButtonRole.RejectRole)
        
        msg.exec()
        
        if msg.clickedButton() == btn_cargar:
            self._cargar_cliente_existente(cliente_existente)
        else:
            # Limpiar campo CIF
            if hasattr(self.ui, 'txtcif_nif'):
                self.ui.txtcif_nif.clear()
                self._apply_widget_valid_state(self.ui.txtcif_nif, None)

    def _cargar_cliente_existente(self, cliente):
        """Carga un cliente existente en el formulario"""
        self.cliente_actual = cliente
        self.cargar_datos_en_formulario(cliente)
        self._modo_edicion = False
        self.desactivar_campos_edicion()
        self.activar_botones_navegacion()
        # Cambiar a la vista de ficha
        if hasattr(self.ui, 'stackedWidget'):
            self.ui.stackedWidget.setCurrentIndex(0)

    def _update_form_validity(self):

        """Enable/disable Save button depending on form validation."""
        btn = getattr(self.ui, 'btnGuardar', None)
        if btn is None:
            return

        # Only allow saving when in edit mode (new or editing an existing client)
        if not getattr(self, '_modo_edicion', False):
            try:
                btn.setEnabled(False)
            except Exception:
                pass
            return

        # En modo edición, siempre habilitar el botón Guardar
        # La validación se hará al intentar guardar, mostrando errores al usuario
        try:
            btn.setEnabled(True)
        except Exception:
            pass
    
    def volver_a_lista(self):
        """Vuelve a la página de búsquedas/lista"""
        if hasattr(self.ui, 'stackedWidget'):
            self.ui.stackedWidget.setCurrentIndex(1)

        # Asegurar que la lista está actualizada
        try:
            self.cargar_clientes()
        except Exception:
            pass

        # Si tenemos un cliente seleccionado en la ficha, intentar seleccionarlo en la tabla
        try:
            cid = getattr(self, 'cliente_actual', None)
            cid = getattr(cid, 'id', None) if cid is not None else None
            if cid is None:
                return

            tabla = None
            if hasattr(self.ui, 'tabla_busquedas'):
                tabla = self.ui.tabla_busquedas
            elif hasattr(self.ui, 'tabla_clientes'):
                tabla = self.ui.tabla_clientes
            elif hasattr(self.ui, 'tableWidget'):
                tabla = self.ui.tableWidget

            if tabla is None:
                return

            # Si es QTableWidget
            if isinstance(tabla, QTableWidget):
                rows = tabla.rowCount()
                for r in range(rows):
                    item = tabla.item(r, 0)
                    if item is None:
                        continue
                    try:
                        data_get = getattr(item, 'data', None)
                        val = data_get(Qt.ItemDataRole.UserRole) if callable(data_get) else None
                    except Exception:
                        val = None
                    if val == cid:
                        selection = tabla.selectionModel()
                        index = tabla.model().index(r, 0)
                        selection.setCurrentIndex(index, selection.SelectionFlag.ClearAndSelect | selection.SelectionFlag.Rows)
                        break

            # Si es QTableView con QStandardItemModel
            elif isinstance(tabla, QTableView):
                model = tabla.model()
                if model is None:
                    return
                row_count = model.rowCount()
                for r in range(row_count):
                    val = None
                    try:
                        # Prefer QStandardItemModel.item when available
                        item_get = getattr(model, 'item', None)
                        if callable(item_get):
                            it = item_get(r, 0)
                            if it is not None:
                                try:
                                    data_get = getattr(it, 'data', None)
                                    val = data_get(Qt.ItemDataRole.UserRole) if callable(data_get) else None
                                except Exception:
                                    val = None
                        else:
                            idx = model.index(r, 0)
                            val = model.data(idx, Qt.ItemDataRole.UserRole)
                    except Exception:
                        val = None
                    if val == cid:
                        index = model.index(r, 0)
                        selection = tabla.selectionModel()
                        selection.setCurrentIndex(index, selection.SelectionFlag.ClearAndSelect | selection.SelectionFlag.Rows)
                        break
        except Exception:
            # No crítico; si algo falla no queremos romper la navegación
            pass
    
    def siguiente_cliente(self):
        """Navega al siguiente cliente en la lista"""
        tabla = getattr(self.ui, 'tabla_busquedas', None)
        if not tabla or not tabla.model():
            return
        
        selection = tabla.selectionModel()
        if not selection.hasSelection():
            return
        
        current_index = selection.currentIndex()
        next_row = current_index.row() + 1
        
        if next_row < tabla.model().rowCount():
            next_index = tabla.model().index(next_row, 0)
            selection.setCurrentIndex(next_index, selection.SelectionFlag.ClearAndSelect | selection.SelectionFlag.Rows)
            self.abrir_ficha_cliente()
    
    def anterior_cliente(self):
        """Navega al cliente anterior en la lista"""
        tabla = getattr(self.ui, 'tabla_busquedas', None)
        if not tabla or not tabla.model():
            return
        
        selection = tabla.selectionModel()
        if not selection.hasSelection():
            return
        
        current_index = selection.currentIndex()
        prev_row = current_index.row() - 1
        
        if prev_row >= 0:
            prev_index = tabla.model().index(prev_row, 0)
            selection.setCurrentIndex(prev_index, selection.SelectionFlag.ClearAndSelect | selection.SelectionFlag.Rows)
            self.abrir_ficha_cliente()
    
    
    '''----------------------------------------------------------'''
    '''Zona activar/desactivar botones navegacion                '''
    '''----------------------------------------------------------'''
    def activar_botones_navegacion(self):
        """Activa los botones normales """
        get = self._get_widget

        # Activar botones de navegación principales
        for name in ('btnSiguiente', 'btnAnterior', 'btnEditar', 'btnBorrar', 'btnAnadir', 'btnBuscar'):
            w = get(name)
            if w is not None:
                try:
                    w.setEnabled(True)
                except Exception:
                    pass

        # Asegurarse de que los controles de edición estén deshabilitados
        for name in ('btnGuardar', 'btnDeshacer'):
            w = get(name)
            if w is not None:
                try:
                    w.setEnabled(False)
                except Exception:
                    pass

        # Restaurar el botón de listados a su estado normal (visible/enabled)
        bl = get('botListados')
        if bl is not None:
            try:
                bl.setEnabled(True)
            except Exception:
                pass

    def desactivar_botones_navegacion(self):
        """Desactiva los botones normales..... """
        get = self._get_widget

        # Desactivar botones de navegación principales
        for name in ('btnSiguiente', 'btnAnterior', 'btnEditar', 'btnBorrar', 'btnAnadir', 'btnBuscar'):
            w = get(name)
            if w is not None:
                try:
                    w.setEnabled(False)
                except Exception:
                    pass

        # Activar los botones de guardar/undo (modo edición)
        for name in ('btnGuardar', 'btnDeshacer'):
            w = get(name)
            if w is not None:
                try:
                    w.setEnabled(True)
                except Exception:
                    pass

        # Durante edición no queremos que 'Listados' aparezca como activo
        bl = get('botListados')
        if bl is not None:
            try:
                bl.setEnabled(False)
            except Exception:
                pass
        
    def _handle_postal_code_change(self):
        """Handle postal code changes - lookup city and province from france.db"""
        if not hasattr(self.ui, 'txtcp'):
            return
            
        cp = self.ui.txtcp.text().strip()
        if not cp or len(cp) < 5:  # French postal codes are 5 digits
            return
            
        try:
            # Connect to france.db
            db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'datos', 'france.db')
            if not os.path.exists(db_path):
                return
                
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Query for postal code
            cursor.execute("""
                SELECT nom_standard_majuscule, dep_nom 
                FROM villes 
                WHERE code_postal = ? 
                ORDER BY nom_standard_majuscule
            """, (cp,))
            
            results = cursor.fetchall()
            conn.close()
            
            if len(results) == 1:
                # Single result - fill fields directly
                poblacion, provincia = results[0]
                if hasattr(self.ui, 'txtpoblacion'):
                    self.ui.txtpoblacion.setText(poblacion or '')
                if hasattr(self.ui, 'txtprovincia'):
                    self.ui.txtprovincia.setText(provincia or '')
                    
            elif len(results) > 1:
                # Create QSqlDatabase connection to france.db
                db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'datos', 'france.db')
                france_db = QSqlDatabase.addDatabase("QSQLITE", "france_connection")
                france_db.setDatabaseName(db_path)
                
                if france_db.open():
                    sql = f"""
                        SELECT ROWID, nom_standard_majuscule, dep_nom 
                        FROM villes 
                        WHERE code_postal = '{cp}' 
                        ORDER BY nom_standard_majuscule
                    """
                    
                    id_selected, record = DBConsultaView.select_from_sql(
                        parent=self,
                        sql=sql,
                        db=france_db,
                        headers=['ID', 'Población', 'Provincia'],
                        campos=['nom_standard_majuscule'],
                        titulo=f'Seleccionar población para CP {cp}'
                    )
                    
                    if record and record.count() >= 3:  # Make sure we have all columns
                        poblacion = record.value(1)  # nom_standard_majuscule (columna 1, ya que 0 es ROWID)
                        provincia = record.value(2)  # dep_nom (columna 2)
                        
                        if hasattr(self.ui, 'txtpoblacion'):
                            self.ui.txtpoblacion.setText(poblacion or '')
                        if hasattr(self.ui, 'txtprovincia'):
                            self.ui.txtprovincia.setText(provincia or '')
                    
                    france_db.close()
                    QSqlDatabase.removeDatabase("france_connection")
                    
                    france_db.close()
                    QSqlDatabase.removeDatabase("france_connection")
                        
        except Exception as e:
            # Silently ignore errors to not disrupt user experience
            print(f"Error in postal code lookup: {e}")
            pass

    def has_unsaved_changes(self) -> bool:
        """Retorna True si hay cambios sin guardar (modo edición activo)."""
        return getattr(self, '_modo_edicion', False)

    def _save_changes(self) -> bool:
        """Intenta guardar los cambios. Retorna True si tuvo éxito."""
        self.guardar_cliente()
        # Si el guardado fue exitoso, _modo_edicion se habrá puesto a False
        return not getattr(self, '_modo_edicion', False)