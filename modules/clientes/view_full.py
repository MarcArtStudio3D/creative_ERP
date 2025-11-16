"""
Vista del módulo de Clientes - Solo lógica de negocio
La UI se genera automáticamente desde frmClientes.ui
"""

from logging import disable
from PySide6.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QVBoxLayout, QTableWidget, QTableView
from PySide6.QtCore import Qt, QDate, Signal, QAbstractTableModel
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
        self.ui = Ui_frmClientes()
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
        
        # Inicializar datos
        self.session = get_session()
        self.repository = ClienteRepository(self.session)
        self.cliente_actual = None
        
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

    def _find_table(self):
        """Encuentra la tabla principal probando varios nombres y tipos."""
        for candidate in ("tabla_busquedas", "tabla_clientes", "tableWidget", "tabla_busqueda"):
            w = self._get_widget(candidate)
            if w is not None:
                return w
        # fallback: buscar primer hijo que sea QTableWidget o QTableView
        try:
            tables = self.findChildren((QTableWidget, QTableView))
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
                item = QStandardItem(cliente.codigo_cliente or "")
                item.setData(cliente.id, Qt.ItemDataRole.UserRole)
                item.setEditable(False)
                model.setItem(row, 0, item)
                
                # CIF/NIF
                item = QStandardItem(cliente.cif_nif or "")
                item.setEditable(False)
                model.setItem(row, 1, item)
                
                # Nombre Fiscal
                item = QStandardItem(cliente.nombre_fiscal or cliente.nombre_completo())
                item.setEditable(False)
                model.setItem(row, 2, item)
                
                # Teléfono
                item = QStandardItem(cliente.telefono1 or "")
                item.setEditable(False)
                model.setItem(row, 3, item)
                
                # Email
                item = QStandardItem(cliente.email or "")
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
                clientes = [c for c in clientes if (
                    (c.codigo_cliente and search_lower in c.codigo_cliente.lower()) or
                    (c.cif_nif and search_lower in c.cif_nif.lower()) or
                    (c.nombre_fiscal and search_lower in c.nombre_fiscal.lower()) or
                    (c.nombre and search_lower in c.nombre.lower()) or
                    (c.apellido1 and search_lower in c.apellido1.lower()) or
                    (c.apellido2 and search_lower in c.apellido2.lower()) or
                    (c.telefono1 and search_lower in c.telefono1.lower()) or
                    (c.email and search_lower in c.email.lower())
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
                    item = QTableWidgetItem(cliente.codigo_cliente or "")
                    item.setData(Qt.ItemDataRole.UserRole, cliente.id)
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    tabla.setItem(row, 0, item)
                    # CIF/NIF
                    item = QTableWidgetItem(cliente.cif_nif or "")
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    tabla.setItem(row, 1, item)
                    # Nombre Fiscal
                    item = QTableWidgetItem(cliente.nombre_fiscal or cliente.nombre_completo())
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    tabla.setItem(row, 2, item)
                    # Teléfono
                    item = QTableWidgetItem(cliente.telefono1 or "")
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    tabla.setItem(row, 3, item)
                    # Email
                    item = QTableWidgetItem(cliente.email or "")
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    tabla.setItem(row, 4, item)
            
            # Si es QTableView
            elif isinstance(tabla, QTableView):
                model = QStandardItemModel(len(clientes), 5, self)
                model.setHorizontalHeaderLabels(["Código", "NIF/CIF", "Nombre Fiscal", "Teléfono", "Email"])
                for row, cliente in enumerate(clientes):
                    def std_item(text, cid):
                        it = QStandardItem(text or "")
                        it.setEditable(False)
                        it.setData(cid, Qt.ItemDataRole.UserRole)
                        return it

                    model.setItem(row, 0, std_item(cliente.codigo_cliente, cliente.id))
                    model.setItem(row, 1, std_item(cliente.cif_nif, cliente.id))
                    model.setItem(row, 2, std_item(cliente.nombre_fiscal or cliente.nombre_completo(), cliente.id))
                    model.setItem(row, 3, std_item(cliente.telefono1, cliente.id))
                    model.setItem(row, 4, std_item(cliente.email, cliente.id))
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
            self.ui.txtcodigo_cliente.setText(cliente.codigo_cliente or "")
        if hasattr(self.ui, 'txtcif_nif'):
            self.ui.txtcif_nif.setText(cliente.cif_nif or "")
        if hasattr(self.ui, 'txtnombre'):
            self.ui.txtnombre.setText(cliente.nombre or "")
        if hasattr(self.ui, 'txtPrimerApellido'):
            self.ui.txtPrimerApellido.setText(cliente.apellido1 or "")
        if hasattr(self.ui, 'txtSegundoApellido'):
            self.ui.txtSegundoApellido.setText(cliente.apellido2 or "")
        if hasattr(self.ui, 'txtnombre_fiscal'):
            self.ui.txtnombre_fiscal.setText(cliente.nombre_fiscal or "")
        if hasattr(self.ui, 'txtnombre_comercial'):
            self.ui.txtnombre_comercial.setText(cliente.nombre_comercial or "")
        
        # Dirección
        if hasattr(self.ui, 'txtdireccion1'):
            self.ui.txtdireccion1.setText(cliente.direccion1 or "")
        if hasattr(self.ui, 'txtdireccion2'):
            self.ui.txtdireccion2.setText(cliente.direccion2 or "")
        if hasattr(self.ui, 'txtcp'):
            self.ui.txtcp.setText(cliente.cp or "")
        if hasattr(self.ui, 'txtpoblacion'):
            self.ui.txtpoblacion.setText(cliente.poblacion or "")
        if hasattr(self.ui, 'txtprovincia'):
            self.ui.txtprovincia.setText(cliente.provincia or "")
        
        # Contacto
        if hasattr(self.ui, 'txttelefono1'):
            self.ui.txttelefono1.setText(cliente.telefono1 or "")
        if hasattr(self.ui, 'txttelefono2'):
            self.ui.txttelefono2.setText(cliente.telefono2 or "")
        if hasattr(self.ui, 'txtmovil'):
            self.ui.txtmovil.setText(cliente.movil or "")
        if hasattr(self.ui, 'txtfax'):
            self.ui.txtfax.setText(cliente.fax or "")
        if hasattr(self.ui, 'txtemail'):
            self.ui.txtemail.setText(cliente.email or "")
        if hasattr(self.ui, 'txtweb'):
            self.ui.txtweb.setText(cliente.web or "")
        
        # Actualizar label con nombre del cliente
        if hasattr(self.ui, 'txtNombreFiscal'):
            self.ui.txtNombreFiscal.setText(cliente.nombre_completo())
        
        # Cargar datos adicionales
        self.cargar_direcciones_alternativas(cliente.id)
        self.cargar_deudas(cliente.id)
        self.cargar_estadisticas(cliente.id)
    
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
        self.ui.stackedWidget.setCurrentIndex(0)
        
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
        self.abrir_ficha_cliente()
    
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
            if self.cliente_actual:
                # Actualizar campos
                if hasattr(self.ui, 'txtcif_nif'):
                    self.cliente_actual.cif_nif = self.ui.txtcif_nif.text()
                if hasattr(self.ui, 'txtnombre'):
                    self.cliente_actual.nombre = self.ui.txtnombre.text()
                # ... más campos
                
                self.repository.actualizar(self.cliente_actual)
                QMessageBox.information(self, "Éxito", "Cliente actualizado")
            else:
                # Crear nuevo
                cliente = Cliente(
                    codigo_cliente=self.ui.txtcodigo_cliente.text() if hasattr(self.ui, 'txtcodigo_cliente') else "",
                    cif_nif=self.ui.txtcif_nif.text() if hasattr(self.ui, 'txtcif_nif') else "",
                    # ... más campos
                )
                self.repository.crear(cliente)
                QMessageBox.information(self, "Éxito", "Cliente creado")
            
            self.cargar_clientes()
            self.ui.stackedWidget.setCurrentIndex(1)
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
                widget.setValue(widget.minimum())

            # QDateEdit - resetear a fecha actual
            elif isinstance(widget, QDateEdit):
                widget.setDate(QDate.currentDate())

            # QCheckBox - desmarcar
            elif isinstance(widget, QCheckBox):
                widget.setChecked(False)
    
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
        if hasattr(self.ui, 'btnUndo'):
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
        if hasattr(self.ui, 'btnUndo'):
            self.ui.btnDeshacer.setEnabled(True)
        