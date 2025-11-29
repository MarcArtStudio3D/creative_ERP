from PySide6.QtWidgets import QDialog, QMessageBox, QLineEdit, QComboBox, QTextEdit, QCheckBox, QDateEdit, QDoubleSpinBox, QHeaderView
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from modules.articulos.ui_frmarticulos import Ui_FrmArticulos
from modules.articulos.controller import ArticuloController


class ArticulosView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_FrmArticulos()
        self.ui.setupUi(self)
        
        self.controller = ArticuloController()
        self._init_complete = False
        
        # Initialize UI
        self._setup_connections()
        self._setup_initial_state()
        
        self._init_complete = True
    
    # ==================== Setup ====================
    
    def _setup_connections(self):
        """Connect UI signals to slots"""
        # Navigation buttons
        self.ui.botAnadir.clicked.connect(self._on_add_clicked)
        self.ui.botSiguiente.clicked.connect(self._on_next_clicked)
        self.ui.botAnterior.clicked.connect(self._on_prev_clicked)
        self.ui.botEditar.clicked.connect(self._on_edit_clicked)
        self.ui.botGuardar.clicked.connect(self._on_save_clicked)
        self.ui.botDeshacer.clicked.connect(self._on_undo_clicked)
        self.ui.botBorrar.clicked.connect(self._on_delete_clicked)
        self.ui.btn_cerrar.clicked.connect(self.close)
        
        # Search button
        self.ui.btnBuscar.clicked.connect(self._on_search_clicked)
        
        # Tab changes
        self.ui.Pestanas.currentChanged.connect(self._on_tab_changed)
    
    def _setup_initial_state(self):
        """Set initial UI state"""
        # Show list view initially
        self.ui.stackedWidget.setCurrentIndex(1)
        
        # Setup articles table
        self._setup_articles_table()
        
        # Lock fields initially
        self._lock_fields(True)
        
        # Hide certain labels
        self.ui.lblkit.setVisible(False)
        self.ui.lbl_en_promocion.setVisible(False)
    
    # ==================== Field Locking ====================
    
    def _lock_fields(self, locked: bool):
        """Lock/unlock form fields"""
        # Lock all line edits
        for line_edit in self.findChildren(QLineEdit):
            line_edit.setReadOnly(locked)
        
        # Enable/disable combo boxes
        for combo_box in self.findChildren(QComboBox):
            combo_box.setEnabled(not locked)
        
        # Enable/disable text edits
        for text_edit in self.findChildren(QTextEdit):
            text_edit.setReadOnly(locked)
        
        # Enable/disable checkboxes
        for checkbox in self.findChildren(QCheckBox):
            checkbox.setEnabled(not locked)
        
        # Enable/disable date edits
        for date_edit in self.findChildren(QDateEdit):
            date_edit.setEnabled(not locked)
        
        # Enable/disable double spin boxes
        for spin_box in self.findChildren(QDoubleSpinBox):
            spin_box.setReadOnly(locked)
        
        # Button states
        self.ui.botAnadir.setEnabled(locked)
        self.ui.botAnterior.setEnabled(locked)
        self.ui.botBorrar.setEnabled(locked)
        self.ui.botDeshacer.setEnabled(not locked)
        self.ui.botEditar.setEnabled(locked)
        self.ui.botGuardar.setEnabled(not locked)
        self.ui.botSiguiente.setEnabled(locked)
        self.ui.btnBuscar.setEnabled(locked)
        
        # Keep certain fields always readonly
        self._set_readonly_fields()
    
    def _set_readonly_fields(self):
        """Set fields that should always be readonly"""
        readonly_fields = [
            'txtfecha_fecha_ultima_compra',
            'txtfechaUltimaVenta',
            'txtunidades_compradas',
            'txtunidades_vendidas',
            'txtimporte_acumulado_compras',
            'txtimporte_acumulado_ventas',
            'txtstock_fisico_almacen',
            'txtcantidad_pendiente_recibir',
            'txtunidades_reservadas',
            'txtstock_real_2',
            'txtfecha_prevista_recepcion',
        ]
        
        for field_name in readonly_fields:
            if hasattr(self.ui, field_name):
                field = getattr(self.ui, field_name)
                field.setReadOnly(True)
    
    # ==================== Form Data Mapping ====================
    
    def _load_form_from_article(self):
        """Load form fields from current article"""
        article = self.controller.get_current_article()
        if not article:
            return
        
        # Update header labels
        self.ui.lblCodigo.setText(article.get("codigo", ""))
        self.ui.lblDescripcion.setText(article.get("descripcion_reducida", ""))
        self.ui.lblkit.setVisible(article.get("kit", False))
        self.ui.lbl_en_promocion.setVisible(article.get("articulo_promocionado", False))
        
        # Article tab fields
        self.ui.txtcodigo.setText(article.get("codigo", ""))
        self.ui.txtcodigo_barras.setText(article.get("codigo_barras", ""))
        self.ui.txtcodigo_fabricante.setText(article.get("codigo_fabricante", ""))
        self.ui.txtdescripcion.setPlainText(article.get("descripcion", ""))
        self.ui.txtdescripcionResumida.setText(article.get("descripcion_reducida", ""))
        
        # Section/Family/Subfamily
        id_seccion = article.get("id_seccion")
        if id_seccion:
            self.ui.txtseccion.setText(self.controller.get_seccion_name(id_seccion))
        
        id_familia = article.get("id_familia")
        if id_familia:
            self.ui.txtfamilia.setText(self.controller.get_familia_name(id_familia))
        
        id_subfamilia = article.get("id_subfamilia")
        if id_subfamilia:
            self.ui.txtsubfamilia.setText(self.controller.get_subfamilia_name(id_subfamilia))
        
        # Provider
        id_proveedor = article.get("id_proveedor")
        if id_proveedor:
            cod_prov, nombre_prov = self.controller.get_proveedor_info(id_proveedor)
            self.ui.txtcodigo_proveedor.setText(cod_prov or "")
            self.ui.txtproveedor.setText(nombre_prov or "")
        
        # Pricing
        self.ui.txtcoste.setText(str(article.get("coste", 0)))
        self.ui.txtCoste_real.setText(str(article.get("coste_real", 0)))
        self.ui.txtdto.setText(str(article.get("porc_dto", 0)))
        self.ui.txtMargen.setValue(article.get("margen", 0))
        self.ui.txtMargen_min.setValue(article.get("margen_min", 0))
        
        # Flags
        self.ui.chkmostrar_web.setChecked(article.get("mostrar_web", 0) == 1)
        self.ui.chkcontrolar_stock.setChecked(article.get("controlar_stock", False))
        
        # TODO: Set IVA combo box
        # TODO: Load other tabs when implemented
    
    def _save_form_to_article(self) -> dict:
        """Get form data as dictionary"""
        data = {}
        
        # Basic fields
        data["codigo"] = self.ui.txtcodigo.text()
        data["codigo_barras"] = self.ui.txtcodigo_barras.text()
        data["codigo_fabricante"] = self.ui.txtcodigo_fabricante.text()
        data["descripcion"] = self.ui.txtdescripcion.toPlainText()
        data["descripcion_reducida"] = self.ui.txtdescripcionResumida.text()
        
        # Pricing
        try:
            data["coste"] = float(self.ui.txtcoste.text().replace(".", "").replace(",", "."))
        except:
            data["coste"] = 0
        
        try:
            data["coste_real"] = float(self.ui.txtCoste_real.text().replace(".", "").replace(",", "."))
        except:
            data["coste_real"] = 0
        
        try:
            data["porc_dto"] = float(self.ui.txtdto.text())
        except:
            data["porc_dto"] = 0
        
        data["margen"] = self.ui.txtMargen.value()
        data["margen_min"] = self.ui.txtMargen_min.value()
        
        # Flags
        data["mostrar_web"] = 1 if self.ui.chkmostrar_web.isChecked() else 0
        data["controlar_stock"] = self.ui.chkcontrolar_stock.isChecked()
        
        # TODO: Get section/family/subfamily IDs from lookups
        # TODO: Get IVA type from combo
        # TODO: Get provider ID from lookup
        
        return data
    
    def _clear_form(self):
        """Clear all form fields"""
        self.ui.txtcodigo.clear()
        self.ui.txtcodigo_barras.clear()
        self.ui.txtcodigo_fabricante.clear()
        self.ui.txtdescripcion.clear()
        self.ui.txtdescripcionResumida.clear()
        self.ui.txtseccion.clear()
        self.ui.txtfamilia.clear()
        self.ui.txtsubfamilia.clear()
        self.ui.txtproveedor.clear()
        self.ui.txtcodigo_proveedor.clear()
        self.ui.txtcoste.clear()
        self.ui.txtCoste_real.clear()
        self.ui.txtdto.clear()
        self.ui.txtMargen.setValue(0)
        self.ui.txtMargen_min.setValue(0)
        self.ui.chkmostrar_web.setChecked(False)
        self.ui.chkcontrolar_stock.setChecked(True)
        
        self.ui.lblCodigo.setText("")
        self.ui.lblDescripcion.setText("Nuevo artículo")
    
    # ==================== Table Setup ====================
    
    def _setup_articles_table(self):
        """Setup the articles list table"""
        # Create and set model
        self.articles_model = ArticlesTableModel()
        self.ui.tablaBusqueda.setModel(self.articles_model)
        
        # Configure table appearance
        self.ui.tablaBusqueda.setAlternatingRowColors(True)
        self.ui.tablaBusqueda.setSelectionBehavior(self.ui.tablaBusqueda.SelectionBehavior.SelectRows)
        self.ui.tablaBusqueda.setSelectionMode(self.ui.tablaBusqueda.SelectionMode.SingleSelection)
        
        # Configure column widths
        header = self.ui.tablaBusqueda.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)  # Código
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Descripción
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)  # Stock
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)  # PVP
        
        self.ui.tablaBusqueda.setColumnWidth(0, 100)  # Código
        self.ui.tablaBusqueda.setColumnWidth(2, 80)   # Stock
        self.ui.tablaBusqueda.setColumnWidth(3, 100)  # PVP
        
        # Connect double-click to edit
        self.ui.tablaBusqueda.doubleClicked.connect(self._on_table_double_click)
        
        # Load data
        self._load_articles_data()
    
    def _load_articles_data(self):
        """Load articles data into the table"""
        try:
            articles = self.controller.repository.get_all(limit=100)  # Load first 100 articles
            self.articles_model.set_articles(articles)
        except Exception as e:
            print(f"Error loading articles: {e}")
    
    def _on_table_double_click(self, index: QModelIndex):
        """Handle table double-click to edit article"""
        if not index.isValid():
            return
        
        article = self.articles_model.get_article(index.row())
        if article:
            self.controller.load_by_id(article['id'])
            self._load_form_from_article()
            self.ui.stackedWidget.setCurrentIndex(0)  # Show form
    
    # ==================== Button Handlers ====================
    
    def _on_add_clicked(self):
        """Handle Add button click"""
        success = self.controller.add_new()
        if success:
            self._clear_form()
            self._lock_fields(False)
            self.ui.stackedWidget.setCurrentIndex(0)  # Show form
            self.ui.Pestanas.setCurrentIndex(0)  # Article tab
            
            # Focus on code field or barcode if auto-code
            # TODO: Check auto_codigo configuration
            self.ui.txtcodigo.setFocus()
        else:
            QMessageBox.warning(self, "Error", "No se pudo crear el artículo")
    
    def _on_edit_clicked(self):
        """Handle Edit button click"""
        if self.controller.get_current_article():
            self._lock_fields(False)
    
    def _on_save_clicked(self):
        """Handle Save button click"""
        form_data = self._save_form_to_article()
        success, message = self.controller.save(form_data)
        
        if success:
            QMessageBox.information(self, "Guardar", message)
            self._load_form_from_article()
            self._lock_fields(True)
        else:
            QMessageBox.warning(self, "Error", message)
    
    def _on_undo_clicked(self):
        """Handle Undo button click"""
        if self.controller.is_editing_new():
            # If new article, delete it and go back to list
            self.controller.delete()
            self.ui.stackedWidget.setCurrentIndex(1)
        else:
            # Reload from database
            self._load_form_from_article()
        
        self._lock_fields(True)
    
    def _on_delete_clicked(self):
        """Handle Delete button click"""
        reply = QMessageBox.question(
            self,
            "Borrar Artículo",
            "¿Desea realmente borrar este artículo?\nEsta opción no se puede deshacer",
            QMessageBox.StandardButton.No | QMessageBox.StandardButton.Yes
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            success, message = self.controller.delete()
            if success:
                QMessageBox.information(self, "Borrar", message)
                self._load_form_from_article()
            else:
                QMessageBox.warning(self, "Error", message)
    
    def _on_next_clicked(self):
        """Handle Next button click"""
        if self.controller.next_article():
            self._load_form_from_article()
    
    def _on_prev_clicked(self):
        """Handle Previous button click"""
        if self.controller.prev_article():
            self._load_form_from_article()
    
    def _on_search_clicked(self):
        """Handle Search button click"""
        # TODO: Implement search dialog
        pass
    
    def _on_tab_changed(self, index: int):
        """Handle tab change"""
        # Reload data for the selected tab
        if not self._init_complete:
            return
        
        # TODO: Load data for specific tabs when implemented
        pass


class ArticlesTableModel(QAbstractTableModel):
    """Table model for articles list"""
    
    def __init__(self):
        super().__init__()
        self.articles = []
        self.headers = ["Código", "Descripción", "Stock", "PVP"]
    
    def set_articles(self, articles):
        """Set articles data"""
        self.beginResetModel()
        self.articles = articles
        self.endResetModel()
    
    def get_article(self, row):
        """Get article at row"""
        if 0 <= row < len(self.articles):
            return self.articles[row]
        return None
    
    def rowCount(self, parent=QModelIndex()):
        return len(self.articles)
    
    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)
    
    def headerData(self, section, orientation, role):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.headers[section]
        return None
    
    def data(self, index, role):
        if not index.isValid() or not (0 <= index.row() < len(self.articles)):
            return None
        
        article = self.articles[index.row()]
        column = index.column()
        
        if role == Qt.ItemDataRole.DisplayRole:
            if column == 0:  # Código
                return article.get("codigo", "")
            elif column == 1:  # Descripción
                return article.get("descripcion_reducida", "")
            elif column == 2:  # Stock
                stock = article.get("stock_real", 0)
                return f"{stock:.0f}"
            elif column == 3:  # PVP
                coste = float(article.get("coste", 0))
                margen = float(article.get("margen", 0))
                pvp = coste * (1 + margen/100)
                return f"€{pvp:.2f}"
        
        elif role == Qt.ItemDataRole.TextAlignmentRole:
            if column in [2, 3]:  # Stock y PVP alineados a la derecha
                return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        
        return None
