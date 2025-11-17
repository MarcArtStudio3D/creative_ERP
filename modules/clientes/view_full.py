"""
Vista del módulo de Clientes - Solo lógica de negocio
La UI se genera automáticamente desde frmClientes.ui
"""

from logging import disable
from PySide6.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QVBoxLayout, QTableWidget, QTableView
from PySide6.QtCore import Qt, QDate, Signal, QAbstractTableModel
from typing import Any
from PySide6.QtGui import QStandardItemModel, QStandardItem
from datetime import date
from core.db import get_session
from modules.clientes.models import Cliente, DireccionAlternativa
from modules.clientes.repository import ClienteRepository
from modules.clientes.ui_clientes import Ui_frmClientes


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
        self._nombre_fiscal_manual = False  # si el usuario ha editado manualmente txtnombre_fiscal
        
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

        # Botones de guardar/deshacer en la ficha de edición
        for name, handler in (("btnGuardar", self.guardar_cliente), ("btnDeshacer", self.deshacer_cambios)):
            w = self._get_widget(name)
            if w is not None and hasattr(w, "clicked"):
                w.clicked.connect(handler)

        # Conectar cambio de página del stackedWidget para activar/desactivar campos
        if hasattr(self.ui, 'stackedWidget'):
            self.ui.stackedWidget.currentChanged.connect(self.on_pagina_cambiada)

        # Activar validaciones inline (conectar señales) - se ignoran fuera de modo edición
        if not hasattr(self, '_validations_connected') or not self._validations_connected:
            try:
                from PySide6.QtWidgets import QLineEdit, QTextEdit, QPlainTextEdit, QDateEdit, QSpinBox, QComboBox, QDoubleSpinBox
                # Useful fields for validation
                names = ['txtcodigo_cliente', 'txtnombre', 'txtPrimerApellido', 'txtSegundoApellido', 'txtnombre_fiscal', 'txtcif_nif', 'txtemail', 'txtdia_pago1', 'txtdia_pago2', 'txtcuenta_corriente', 'txtiban', 'txtCuentaIBAN']
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
                        # Track manual edits for nombre_fiscal so we don't override user's edits (QLineEdit only)
                        try:
                            if n == 'txtnombre_fiscal' and isinstance(w, QLineEdit) and hasattr(w, 'textEdited'):
                                w.textEdited.connect(lambda *a, _self=self: setattr(_self, '_nombre_fiscal_manual', True))
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
        # Complete CIF check: compute control digit/letter
        import re
        if not re.fullmatch(r"[A-HJNP-SUVW]\d{7}[0-9A-J]", s):
            return False
        # Compute sums
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
        control_letter_map = 'JABCDEFGHI'  # index by digit
        provided = s[-1]
        # Some entity types expect numeric or letter control or both; accept both
        if provided == str(control_digit) or provided == control_letter_map[control_digit]:
            return True
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
            errores.append('El código de cliente es obligatorio.')

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
            errores.append('Debe introducir el nombre o el nombre fiscal del cliente.')

        # NIF/CIF/SIRET validation if provided
        if getattr(self.ui, 'txtcif_nif', None) is not None:
            txt = None
            w = getattr(self.ui, 'txtcif_nif')
            if hasattr(w, 'text'):
                txt = w.text()
            if txt and txt.strip():
                if not self._is_valid_nif_cif(txt):
                    errores.append('El NIF/CIF introducido no parece válido.')

        # Validar email si está presente
        if getattr(self.ui, 'txtemail', None) is not None:
            w = getattr(self.ui, 'txtemail')
            txt_email = w.text() if hasattr(w, 'text') else ''
            if txt_email and txt_email.strip():
                import re
                # Very simple email validation
                if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", txt_email.strip()):
                    errores.append('El email introducido no es válido.')

        # CCC (cuenta bancaria) validation if present
        if getattr(self.ui, 'txtcuenta_corriente', None) is not None:
            w = getattr(self.ui, 'txtcuenta_corriente')
            txtccc = w.text() if hasattr(w, 'text') else ''
            if txtccc and txtccc.strip():
                if not self._is_valid_ccc(txtccc):
                    errores.append('La cuenta bancaria (CCC) no es válida.')

        # IBAN validation if present
        if getattr(self.ui, 'txtiban', None) is not None or getattr(self.ui, 'txtCuentaIBAN', None) is not None:
            w = getattr(self.ui, 'txtiban', None) or getattr(self.ui, 'txtCuentaIBAN', None)
            txtiban = w.text() if (w is not None and hasattr(w, 'text')) else ''
            if txtiban and txtiban.strip():
                if not self._is_valid_iban(txtiban):
                    errores.append('El IBAN introducido no es válido.')

        # Dias de pago (si existen) deben ser 0-31
        for dname in ('txtdia_pago1', 'txtdia_pago2'):
            w = getattr(self.ui, dname, None)
            if w is not None:
                try:
                    val = int(w.value()) if hasattr(w, 'value') else int(w.text()) if hasattr(w, 'text') and w.text() else None
                    if val is not None and not (0 <= int(val) <= 31):
                        errores.append(f'Día de pago {dname} fuera de rango 0-31.')
                except Exception:
                    errores.append(f'Día de pago {dname} no es un número válido.')

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
            model.setHorizontalHeaderLabels(["Código", "NIF/CIF", "Nombre Fiscal", "Teléfono", "Email"])
            
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
                
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al cargar clientes: {str(e)}")
    
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
            
            # Si es QTableView
            elif isinstance(tabla, QTableView):
                model = QStandardItemModel(len(clientes), 5, self)
                model.setHorizontalHeaderLabels(["Código", "NIF/CIF", "Nombre Fiscal", "Teléfono", "Email"])
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
                
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al filtrar clientes: {str(e)}")

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
            QMessageBox.warning(self, "Error", "No se pudo cargar el cliente")
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
            # If the DB has a non-empty nombre_fiscal, consider it a manual/official value
            try:
                self._nombre_fiscal_manual = bool(val_fiscal and val_fiscal.strip())
            except Exception:
                self._nombre_fiscal_manual = False
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
        tabla = getattr(self.ui, 'tabla_busquedas', None) or getattr(self.ui, 'tabla_clientes', None)
        if not tabla:
            return
        
        # Verificar que hay un cliente seleccionado
        selection = tabla.selectionModel()
        if not selection.hasSelection():
            QMessageBox.warning(self, "Aviso", "Seleccione un cliente para editar")
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
            QMessageBox.warning(self, "Aviso", "Seleccione un cliente para borrar")
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
            "Confirmar borrado",
            f"¿Está seguro de que desea borrar el cliente '{cliente.nombre_completo()}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if respuesta == QMessageBox.StandardButton.Yes:
            try:
                self.repository.eliminar(id_cliente)
                QMessageBox.information(self, "Éxito", "Cliente borrado correctamente")
                self.cargar_clientes()
            except ValueError as e:
                QMessageBox.warning(self, "No se puede borrar", str(e))
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al borrar: {str(e)}")
    
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
                QMessageBox.warning(self, "Validación", "\n".join(errores))
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
                QMessageBox.information(self, "Éxito", "Cliente creado")
            
            self.cargar_clientes()
            self.ui.stackedWidget.setCurrentIndex(1)
            # Restablecer el modo edición y botones
            self._modo_edicion = False
            self.activar_botones_navegacion()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar: {str(e)}")
    
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
        self._validate_and_apply(str(name))

    def _maybe_fill_nombre_fiscal(self):
        """Compute `nombre_fiscal` from apellidos/nombre and fill if the field is empty.

        Rule: apellido1 + ' ' + apellido2 + ' ' + nombre (all uppercase). If apellido2 empty,
        omit it. If both surnames empty, use `nombre`. Only fill if the target field is blank.
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
            # Only change if target is empty
            current = w_nombre_fiscal.text().strip()
            # If the user edited nombre_fiscal manually, don't overwrite it when fields change
            if current and getattr(self, '_nombre_fiscal_manual', False):
                return
            parts = []
            if a1:
                parts.append(a1)
            if a2:
                parts.append(a2)
            if (a1 or a2) and nombre:
                parts.append(nombre)
            if not parts and nombre:
                parts = [nombre]
            computed = ' '.join(parts).strip()
            if not computed:
                return
            # Uppercase result
            computed = computed.upper()
            try:
                w_nombre_fiscal.setText(computed)
                # We just auto-generated this value; mark it as not manually edited
                self._nombre_fiscal_manual = False
            except Exception:
                pass
            # Also update label `txtNombreFiscal` if present (UI read-only label)
            lbl = getattr(ui, 'txtNombreFiscal', None)
            if lbl is not None and hasattr(lbl, 'setText'):
                try:
                    lbl.setText(computed)
                except Exception:
                    pass
        except Exception:
            return
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
            if txt and not self._is_valid_nif_cif(txt):
                self._apply_widget_valid_state(w, 'NIF/CIF/SIRET inválido')
            else:
                self._apply_widget_valid_state(w, None)

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

    def _update_form_validity(self):
        """Enable/disable Save button depending on form validation."""
        ok, errores = self._validar_campos()
        btn = getattr(self.ui, 'btnGuardar', None)
        if btn is None:
            return
        btn.setEnabled(bool(ok))
    
    def volver_a_lista(self):
        """Vuelve a la página de búsquedas/lista"""
        if hasattr(self.ui, 'stackedWidget'):
            self.ui.stackedWidget.setCurrentIndex(1)
    
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
    '''Zona activar/desactivar botones navegacion'''
    '''----------------------------------------------------------'''
    def activar_botones_navegacion(self):
        """Activa los botones normales """
    
        if hasattr(self.ui, 'btnSiguiente'):
            self.ui.btnSiguiente.setEnabled(True)
        if hasattr(self.ui, 'btnAnterior'):
            self.ui.btnAnterior.setEnabled(True)
        if hasattr(self.ui, 'btnEditar'):
            self.ui.btnEditar.setEnabled(True)
        if hasattr(self.ui, 'btnBorrar'):
            self.ui.btnBorrar.setEnabled(True)
        if hasattr(self.ui, 'btnAnadir'):
            self.ui.btnAnadir.setEnabled(True) 
        if hasattr(self.ui, 'btnBuscar'):
            self.ui.btnBuscar.setEnabled(True)
        """desactiva los botones de guardar/undo..... """
        if hasattr(self.ui, 'btnGuardar'):
            self.ui.btnGuardar.setEnabled(False)
        if hasattr(self.ui, 'btnDeshacer'):
            self.ui.btnDeshacer.setEnabled(False)

    def desactivar_botones_navegacion(self):
        """Desactiva los botones normales..... """
        if hasattr(self.ui, 'btnSiguiente'):
            self.ui.btnSiguiente.setEnabled(False)
        if hasattr(self.ui, 'btnAnterior'):
            self.ui.btnAnterior.setEnabled(False)
        if hasattr(self.ui, 'btnEditar'):
            self.ui.btnEditar.setEnabled(False)
        if hasattr(self.ui, 'btnBorrar'):
            self.ui.btnBorrar.setEnabled(False)
        if hasattr(self.ui, 'btnAnadir'):
            self.ui.btnAnadir.setEnabled(False) 
        if hasattr(self.ui, 'btnBuscar'):
            self.ui.btnBuscar.setEnabled(False)
        """Activa los botones de guardar/undo..... """
        if hasattr(self.ui, 'btnGuardar'):
            self.ui.btnGuardar.setEnabled(True)
        if hasattr(self.ui, 'btnDeshacer'):
            self.ui.btnDeshacer.setEnabled(True)
        