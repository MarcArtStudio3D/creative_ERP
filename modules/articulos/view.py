from PySide6.QtWidgets import QWidget, QMessageBox, QLineEdit, QComboBox, QTextEdit, QCheckBox, QDateEdit, QDoubleSpinBox, QHeaderView
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, QDate
from PySide6.QtCharts import QChart, QChartView, QBarSet, QBarSeries, QBarCategoryAxis, QValueAxis
from PySide6.QtGui import QPainter, QShortcut, QKeySequence
from modules.articulos.ui_frmarticulos import Ui_FrmArticulos
from modules.articulos.controller import ArticuloController
from modules.common.db_consulta_view import DBConsultaView
from core.db import get_current_database, set_current_database
from core.utils import format_decimal_value, get_company_decimal_settings, parse_decimal_input, qdate_to_date


class ArticulosView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_FrmArticulos()
        self.ui.setupUi(self)
        # Asegurar que el botón 'Nuevo' utilice el estilo centralizado 'success' desde modern.qss
        try:
            # Establecer una propiedad dinámica 'class' para que coincida con selectores tipo QPushButton[class="success"]
            self.ui.botAnadir.setProperty('class', 'success')
        except Exception:
            pass
        
        # Ensure we're using the correct database for articles
        self._ensure_articles_database()
        
        self.controller = ArticuloController()
        # Decimal formatting settings (populated from current company)
        self.decimales_totales = 2
        self.decimales_precios = 2

        self._init_complete = False
        
        # Initialize UI
        self._setup_connections()
        self._setup_initial_state()
        
        self._init_complete = True
    
    # ==================== Database Setup ====================
    
    def _ensure_articles_database(self):
        """Asegurar que se esté usando la base de datos correcta para el módulo de artículos"""
        current_db = get_current_database()
        
        # If we're on main database, we need to switch to articles database
        # Esto debería ser la base de datos configurada para la compañía (p.ej. artstudio3d)
        if current_db == 'main':
            # TODO: En una configuración multi-empresa completa, aquí se obtendría la BD de la compañía
            # For now, default to artstudio3d for articles
            try:
                set_current_database('artstudio3d')
                print(f"Switched to articles database: artstudio3d")
            except Exception as e:
                print(f"❌ Error switching to articles database: {e}")
                # Stay on current database if switch fails
    
    # ==================== Setup ====================
    
    def _setup_connections(self):
        """Conectar señales de la UI a sus handlers (slots)"""
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
        
        # Keyboard shortcut for search (Ctrl+F)
        self.search_shortcut = QShortcut(QKeySequence("Ctrl+F"), self)
        self.search_shortcut.activated.connect(self._on_search_clicked)
        
        # Tab changes
        self.ui.Pestanas.currentChanged.connect(self._on_tab_changed)
        
        # Chart controls
        self.ui.cboTipoGrafica.currentTextChanged.connect(self._on_chart_type_changed)
        self.ui.radGrafica_unidades.toggled.connect(self._on_chart_data_changed)
        self.ui.radGrafica_importes.toggled.connect(self._on_chart_data_changed)
        
        # Lookup buttons
        self.ui.botBuscarSeccion.clicked.connect(self._on_buscar_seccion_clicked)
        self.ui.botBuscarFamilia.clicked.connect(self._on_buscar_familia_clicked)
        self.ui.botBuscarSubfamilia.clicked.connect(self._on_buscar_subfamilia_clicked)
        
        # Promociones - control de campos de fecha según checkbox
        self.ui.chkArticulo_promocionado.toggled.connect(self._on_articulo_promocionado_changed)
        # Promociones action buttons
        try:
            if hasattr(self.ui, 'btnAnadirOferta'):
                self.ui.btnAnadirOferta.clicked.connect(self._on_add_oferta)
        except Exception:
            pass
        try:
            if hasattr(self.ui, 'btnEditarOferta'):
                self.ui.btnEditarOferta.clicked.connect(self._on_edit_oferta)
        except Exception:
            pass
        try:
            if hasattr(self.ui, 'btnguardar_oferta'):
                self.ui.btnguardar_oferta.clicked.connect(self._on_save_oferta)
        except Exception:
            pass
        try:
            if hasattr(self.ui, 'btnDeshacerOferta'):
                self.ui.btnDeshacerOferta.clicked.connect(self._on_undo_oferta)
        except Exception:
            pass

        # Formatear campos numéricos al terminar la edición para que el usuario vea una representación normalizada (separador coma)
        if hasattr(self.ui, 'txtPrecioVenta'):
            try:
                self.ui.txtPrecioVenta.editingFinished.connect(lambda: self._format_price_field(self.ui.txtPrecioVenta))
            except Exception:
                pass

        if hasattr(self.ui, 'txtcoste'):
            try:
                self.ui.txtcoste.editingFinished.connect(lambda: self._format_price_field(self.ui.txtcoste))
            except Exception:
                pass

        if hasattr(self.ui, 'txtCoste_real'):
            try:
                self.ui.txtCoste_real.editingFinished.connect(lambda: self._format_price_field(self.ui.txtCoste_real))
            except Exception:
                pass
    
    def search(self, text: str):
        """
        Método invocado por el panel lateral de búsqueda en main_window_v2.py
        """
        self._load_articles_data(text)
        
    def nuevo(self):
        """Método público para la acción 'Nuevo' desde el panel lateral"""
        self._on_add_clicked()
        
    def editar(self):
        """Método público para la acción 'Editar' desde el panel lateral"""
        self._on_edit_clicked()
        
    def borrar(self):
        """Método público para la acción 'Borrar' desde el panel lateral"""
        self._on_delete_clicked()
        
    def list(self):
        """Método público para cambiar a la vista de lista"""
        self.ui.stackedWidget.setCurrentIndex(1)


    def get_search_options(self) -> dict:
        """
        Devuelve la configuración para las opciones de búsqueda del panel lateral.
        Usado por main_window_v2.py para rellenar el combo de ordenación.
        """
        return {
            'sort_fields': [
                ("Descripción", "descripcion_reducida"),
                ("Código", "codigo"),
                ("Stock", "stock_real"),
                ("Precio", "pvp")
            ],
            'search_placeholder': "Buscar por código, descripción..."
        }





    
    def _setup_initial_state(self):
        """Establecer el estado inicial de la interfaz (vista, tablas, y configuraciones)"""
        # Show list view initially
        self.ui.stackedWidget.setCurrentIndex(1)
        
        # Setup articles table
        self._setup_articles_table()
        
        # Setup chart
        self._setup_chart()
        
        # Populate IVA types combo box
        self._populate_iva_combo()
        
        # Lock fields initially
        self._lock_fields(True)

        # Load company decimal formatting preferences (if any)
        try:
            vals = get_company_decimal_settings()
            self.decimales_totales = vals.get('decimales_totales', self.decimales_totales)
            self.decimales_precios = vals.get('decimales_precios', self.decimales_precios)
        except Exception:
            pass
        
        # Hide certain labels
        self.ui.lblkit.setVisible(False)
        self.ui.lbl_en_promocion.setVisible(False)

    def _load_company_decimal_settings(self):
        """Load company decimal settings (decimales_totales, decimales_precios)

        This reads the Empresa record from the main DB for the currently selected company
        and sets self.decimales_totales / self.decimales_precios. Keeps defaults on error.
        """
        try:
            from core.company_manager import get_current_company_context
            from core.db import get_current_database, set_current_database, get_session
            from core.models import Empresa

            ctx = get_current_company_context()
            if not ctx.get('has_company'):
                return

            company_id = ctx.get('company_id')
            if not company_id:
                return

            original_db = get_current_database()
                # Asegurarnos de que estamos en 'main' para leer metadatos de la empresa
            set_current_database('main')
            session = get_session()
            try:
                empresa = session.query(Empresa).filter_by(id=company_id).first()
                if empresa:
                    self.decimales_totales = int(getattr(empresa, 'decimales_totales', 2) or 2)
                    self.decimales_precios = int(getattr(empresa, 'decimales_precios', 2) or 2)
            finally:
                # restore previous DB and cleanup
                set_current_database(original_db)
                try:
                    session.close()
                except Exception:
                    pass

        except Exception:
            # Keep default values on any error
            pass

    def _format_price_field(self, widget):
        """Normalizar y formatear el QLineEdit de precio/importe para mostrar al usuario.

        Utiliza parse_decimal_input -> format_decimal_value con separador coma.
        """
        try:
            if not widget:
                return

            text = widget.text() if hasattr(widget, 'text') else ''
            if text is None:
                return

            # Allow empty -> set to 0 with formatted display
            if str(text).strip() == '':
                widget.setText(format_decimal_value(0.0, self.decimales_precios, use_comma=True))
                return

            # Parse robustly and reformat for display
            try:
                val = parse_decimal_input(text)
            except Exception:
                # Leave original text if cannot parse
                return

            widget.setText(format_decimal_value(val, self.decimales_precios, use_comma=True))
        except Exception:
            # Don't propagate UI errors
            return
    
    def _populate_iva_combo(self):
        """Rellenar el combo de tipos de IVA desde la tabla TVAIVA"""
        try:
                # Obtener tipos de IVA desde el controlador
            iva_types = self.controller.get_iva_types()
            
            # Clear existing items
            self.ui.cboTipoIVA.clear()
            
            # Add empty option
            self.ui.cboTipoIVA.addItem("", None)
            
            # Add IVA types
            for iva in iva_types:
                # Display format: "descripcion (porcentaje%)"
                display_text = f"{iva['descripcion']} ({iva['porcentaje']}%)"
                # Store the ID as user data
                self.ui.cboTipoIVA.addItem(display_text, iva['id'])
            
            print(f"✓ Loaded {len(iva_types)} IVA types")
            
        except Exception as e:
            print(f"Error populating IVA combo: {e}")
            # Add a default option if error
            self.ui.cboTipoIVA.clear()
            self.ui.cboTipoIVA.addItem("Error cargando tipos IVA", None)
    
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
        # Restore default: main Add/Edit buttons follow locked state (enabled when not editing)
        promo_tab_active = False
        try:
            if hasattr(self.ui, 'Pestanas') and self.ui.Pestanas.currentWidget() is not None:
                promo_tab_active = (self.ui.Pestanas.currentWidget().objectName() == 'tab_promociones')
        except Exception:
            promo_tab_active = False

        self.ui.botAnadir.setEnabled(locked)
        self.ui.botAnterior.setEnabled(locked)
        self.ui.botBorrar.setEnabled(locked)
        self.ui.botDeshacer.setEnabled(not locked)
        self.ui.botEditar.setEnabled(locked)

        # Promotions-specific buttons: enabled only when editing and on the promotions tab
        try:
            editing = (not locked)
            # Enable/disable entire promotions frame so children follow suit
            if hasattr(self.ui, 'framePromocion'):
                try:
                    self.ui.framePromocion.setEnabled(editing and promo_tab_active)
                except Exception:
                    pass
            # Explicitly set children states as some UI generators set widgets disabled
            if hasattr(self.ui, 'btnAnadirOferta'):
                try:
                    self.ui.btnAnadirOferta.setEnabled(editing and promo_tab_active)
                except Exception:
                    pass
            if hasattr(self.ui, 'btnEditarOferta'):
                try:
                    self.ui.btnEditarOferta.setEnabled(editing and promo_tab_active)
                except Exception:
                    pass
            # Some older UI variants may use btnEditartarifa — keep compatibility
            if hasattr(self.ui, 'btnEditartarifa'):
                self.ui.btnEditartarifa.setEnabled(editing and promo_tab_active)
        except Exception:
            pass
        self.ui.botGuardar.setEnabled(not locked)
        self.ui.botSiguiente.setEnabled(locked)
        self.ui.btnBuscar.setEnabled(locked)
        
        # Lookup buttons - enable when editing/adding
        self.ui.botBuscarSeccion.setEnabled(not locked)
        # También permitir buscar familia/subfamilia en modo edición
        if hasattr(self.ui, 'botBuscarFamilia'):
            # Only allow family lookup when editing AND there is a section selected
            has_section = False
            current = self.controller.get_current_article() if hasattr(self, 'controller') else None
            if current and isinstance(current, dict) and current.get('id_seccion'):
                has_section = True

            self.ui.botBuscarFamilia.setEnabled(not locked and has_section)
        if hasattr(self.ui, 'botBuscarSubfamilia'):
            # Sólo habilitar búsqueda de subfamilia si estamos en modo edición
            # y además hay una familia seleccionada (current_article tiene id_familia)
            has_family = False
            current = self.controller.get_current_article() if hasattr(self, 'controller') else None
            if current and isinstance(current, dict) and current.get('id_familia'):
                    has_family = True

            self.ui.botBuscarSubfamilia.setEnabled(not locked and has_family)
        
        # Keep certain fields always readonly
        self._set_readonly_fields()
        
        # Restaurar el estado correcto de los campos de fecha de oferta
        # Estos campos deben seguir el estado del checkbox de promoción, no la lógica general
        if hasattr(self.ui, 'chkArticulo_promocionado'):
            promocionado = self.ui.chkArticulo_promocionado.isChecked()
            # Solo habilitar los campos de fecha si estamos en modo edición Y el checkbox está marcado
            enable_dates = (not locked) and promocionado
            self.ui.txtOferta_Fecha_ini.setEnabled(enable_dates)
            self.ui.txtOferta_Fecha_fin.setEnabled(enable_dates)
    
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
        
        # Section/Family/Subfamily - always set text (clear if no ID)
        id_seccion = article.get("id_seccion")
        if id_seccion:
            seccion_name = self.controller.get_seccion_name(id_seccion)
            self.ui.txtseccion.setText(seccion_name or "")
        else:
            self.ui.txtseccion.clear()
        
        id_familia = article.get("id_familia")
        if id_familia:
            familia_name = self.controller.get_familia_name(id_familia)
            self.ui.txtfamilia.setText(familia_name or "")
        else:
            self.ui.txtfamilia.clear()
        
        id_subfamilia = article.get("id_subfamilia")
        if id_subfamilia:
            subfamilia_name = self.controller.get_subfamilia_name(id_subfamilia)
            self.ui.txtsubfamilia.setText(subfamilia_name or "")
        else:
            self.ui.txtsubfamilia.clear()

        # Ajustar estado del botón de búsqueda de subfamilias según si hay familia y modo edición
        if hasattr(self.ui, 'botBuscarSubfamilia'):
            # Detectar si estamos en modo edición observando el botón Guardar
            editing = self.ui.botGuardar.isEnabled()
            has_family = bool(article.get('id_familia'))
            self.ui.botBuscarSubfamilia.setEnabled(editing and has_family)

        # Ajustar estado del botón de búsqueda de familias según si hay sección y modo edición
        if hasattr(self.ui, 'botBuscarFamilia'):
            editing = self.ui.botGuardar.isEnabled()
            has_section = bool(article.get('id_seccion'))
            self.ui.botBuscarFamilia.setEnabled(editing and has_section)
        
        # Provider - always set text (clear if no ID)
        id_proveedor = article.get("id_proveedor")
        if id_proveedor:
            cod_prov, nombre_prov = self.controller.get_proveedor_info(id_proveedor)
            self.ui.txtcodigo_proveedor.setText(cod_prov or "")
            self.ui.txtproveedor.setText(nombre_prov or "")
        else:
            self.ui.txtcodigo_proveedor.clear()
            self.ui.txtproveedor.clear()
        
        # Precios: formatear según la configuración de decimales de la empresa
        try:
            coste_val = float(article.get("coste", 0) or 0)
        except Exception:
            coste_val = 0.0

        try:
            coste_real_val = float(article.get("coste_real", 0) or 0)
        except Exception:
            coste_real_val = 0.0

        # Use decimals_precios for price-like fields (UI uses comma separator)
        self.ui.txtcoste.setText(format_decimal_value(coste_val, self.decimales_precios, use_comma=True))
        self.ui.txtCoste_real.setText(format_decimal_value(coste_real_val, self.decimales_precios, use_comma=True))
        # Precio de venta (campo nuevo)
        if hasattr(self.ui, 'txtPrecioVenta'):
            # Mostrar como número formateado; preferir el valor existente del artículo o 0
            try:
                pv = article.get("precio_venta", 0)
                # Keep consistent display like other price fields
                try:
                    pv_val = float(pv or 0)
                except Exception:
                    pv_val = 0.0

                self.ui.txtPrecioVenta.setText(format_decimal_value(pv_val, self.decimales_precios, use_comma=True))
            except Exception:
                self.ui.txtPrecioVenta.setText("0")
        self.ui.txtdto.setText(str(article.get("porc_dto", 0)))
        self.ui.txtMargen.setValue(article.get("margen", 0))
        self.ui.txtMargen_min.setValue(article.get("margen_min", 0))
        
        # Flags
        self.ui.chkmostrar_web.setChecked(article.get("mostrar_web", 0) == 1)
        self.ui.chkcontrolar_stock.setChecked(article.get("controlar_stock", False))
        
        # Promociones - cargar estado del checkbox y configurar campos de fecha
        articulo_promocionado = article.get("articulo_promocionado", False)
        # If oferta_activa exists and article flag is not set, prefer the oferta flag for UX consistency
        oferta_activa = article.get('oferta_activa')
        if oferta_activa is not None:
            checked = bool(oferta_activa) or bool(articulo_promocionado)
        else:
            checked = bool(articulo_promocionado)

        self.ui.chkArticulo_promocionado.setChecked(checked)

        # Load date edits from oferta fields if present
        fecha_ini = article.get('oferta_fecha_inicio')
        fecha_fin = article.get('oferta_fecha_fin')

        # Ayudante: convertir fecha Python -> QDate
        def _to_qdate(d):
            if not d:
                return QDate()
            try:
                # If it's already a QDate, return
                if isinstance(d, QDate):
                    return d
                # Try to use attributes
                return QDate(d.year, d.month, d.day)
            except Exception:
                try:
                    return QDate(d.year, d.month, d.day)
                except Exception:
                    return QDate()

        if hasattr(self.ui, 'txtOferta_Fecha_ini'):
            self.ui.txtOferta_Fecha_ini.setDate(_to_qdate(fecha_ini))
        if hasattr(self.ui, 'txtOferta_Fecha_fin'):
            self.ui.txtOferta_Fecha_fin.setDate(_to_qdate(fecha_fin))
        # El signal toggled se encargará de habilitar/deshabilitar los campos de fecha
        
        # Update chart if on graphics tab
        if self.ui.Pestanas.currentIndex() == 6:  # Graphics tab (tab_grafica is index 6)
            self._update_chart()
        
        # TODO: Establecer combo IVA
        # TODO: Cargar otras pestañas cuando estén implementadas
    
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
            data["coste"] = parse_decimal_input(self.ui.txtcoste.text())
        except Exception:
            data["coste"] = 0
        
        try:
            data["coste_real"] = parse_decimal_input(self.ui.txtCoste_real.text())
        except Exception:
            data["coste_real"] = 0

        # Precio de venta (nuevo campo)
        if hasattr(self.ui, 'txtPrecioVenta'):
            try:
                data["precio_venta"] = parse_decimal_input(self.ui.txtPrecioVenta.text())
            except Exception:
                # Don't raise - default to 0.0 if parsing fails
                data["precio_venta"] = 0.0
        
        try:
            data["porc_dto"] = float(self.ui.txtdto.text())
        except:
            data["porc_dto"] = 0
        
        data["margen"] = self.ui.txtMargen.value()
        data["margen_min"] = self.ui.txtMargen_min.value()
        
        # Flags
        data["mostrar_web"] = 1 if self.ui.chkmostrar_web.isChecked() else 0
        data["controlar_stock"] = self.ui.chkcontrolar_stock.isChecked()
        data["articulo_promocionado"] = self.ui.chkArticulo_promocionado.isChecked()
        
        # Get lookup IDs from current article (set by lookup dialogs)
        current = self.controller.get_current_article()
        if current:
            # ID de sección (establecido por set_seccion_from_lookup)
            if 'id_seccion' in current:
                data["id_seccion"] = current['id_seccion']

            # ID de familia (establecido por set_familia_from_lookup)
            if 'id_familia' in current:
                data["id_familia"] = current['id_familia']

            # ID de subfamilia (si existe)
            if 'id_subfamilia' in current:
                data["id_subfamilia"] = current['id_subfamilia']

            # Family ID (set by set_familia_from_lookup)
            if 'id_familia' in current:
                data["id_familia"] = current['id_familia']
        
        # TODO: Obtener IDs de familia/subfamilia desde los diálogos de búsqueda
        # TODO: Obtener tipo de IVA desde el combo
        # TODO: Obtener ID del proveedor desde el lookup
        
        # Promotion dates - QDateEdit -> Python date or None
        try:
            if hasattr(self.ui, 'txtOferta_Fecha_ini'):
                qd = self.ui.txtOferta_Fecha_ini.date()
                py = qdate_to_date(qd)

                data['oferta_fecha_inicio'] = py

            if hasattr(self.ui, 'txtOferta_Fecha_fin'):
                qd = self.ui.txtOferta_Fecha_fin.date()
                py = qdate_to_date(qd)

                data['oferta_fecha_fin'] = py
        except Exception:
            # Don't break saving if date conversion fails; just omit dates
            pass

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
        if hasattr(self.ui, 'txtPrecioVenta'):
            self.ui.txtPrecioVenta.clear()
        self.ui.txtdto.clear()
        self.ui.txtMargen.setValue(0)
        self.ui.txtMargen_min.setValue(0)
        self.ui.chkmostrar_web.setChecked(False)
        self.ui.chkcontrolar_stock.setChecked(True)
        self.ui.chkArticulo_promocionado.setChecked(False)  # Esto deshabilitará los campos de fecha
        
        self.ui.lblCodigo.setText("")
        self.ui.lblDescripcion.setText("Nuevo artículo")
    
    # ==================== Table Setup ====================
    
    def _setup_articles_table(self):
        """Configurar la tabla de lista de artículos"""
        # Crear y asignar el modelo
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
        
        # Conectar doble clic para editar
        self.ui.tablaBusqueda.doubleClicked.connect(self._on_table_double_click)
        
        # Cargar datos
        self._load_articles_data()
    
    def _load_articles_data(self, filter_text: str = ""):
        """Load articles data into the table with optional filter"""
        try:
            articles = self.controller.filter_articles(filter_text)
            self.articles_model.set_articles(articles)
        except Exception as e:
            print(f"Error loading articles: {e}")
    
    def _on_filter_changed(self, text: str):
        """Manejar cambio de filtro - recargar artículos con filtro"""
        self._load_articles_data(text)

    
    def _on_table_double_click(self, index: QModelIndex):
        """Manejar doble clic en la tabla para editar el artículo"""
        if not index.isValid():
            return
        
        article = self.articles_model.get_article(index.row())
        if article:
            self.controller.load_by_id(article['id'])
            self._load_form_from_article()
            self.ui.stackedWidget.setCurrentIndex(0)  # Show form
    
    # ==================== Button Handlers ====================
    
    def _on_add_clicked(self):
        """Manejar click en el botón Añadir"""
        success = self.controller.add_new()
        if success:
            self._clear_form()
            self._lock_fields(False)
            self.ui.stackedWidget.setCurrentIndex(0)  # Show form
            self.ui.Pestanas.setCurrentIndex(0)  # Article tab
            
            # Poner foco en el campo código o código de barras si hay autocódigo
            # TODO: Revisar la configuración de auto_codigo
            self.ui.txtcodigo.setFocus()
        else:
            QMessageBox.warning(self, "Error", "No se pudo crear el artículo")
    
    def _on_edit_clicked(self):
        """Manejar click en el botón Editar"""
        # If we're already in form view with an article loaded, just unlock
        if self.controller.get_current_article() and self.ui.stackedWidget.currentIndex() == 0:
            self._lock_fields(False)
            return
        
        # Otherwise, get the selected article from the table
        selection = self.ui.tablaBusqueda.selectionModel()
        if not selection or not selection.hasSelection():
            QMessageBox.information(self, "Editar", "Por favor, selecciona un artículo de la lista")
            return
        
        index = selection.currentIndex()
        if not index.isValid():
            return
        
        article = self.articles_model.get_article(index.row())
        if article:
            self.controller.load_by_id(article['id'])
            self._load_form_from_article()
            self._lock_fields(False)
            # Switch to edit tab
            self.ui.stackedWidget.setCurrentIndex(0)


    
    def _on_save_clicked(self):
        """Manejar click en el botón Guardar"""
        form_data = self._save_form_to_article()
        success, message = self.controller.save(form_data)
        
        if success:
            QMessageBox.information(self, "Guardar", message)
            self._load_form_from_article()
            self._lock_fields(True)
        else:
            QMessageBox.warning(self, "Error", message)
    
    def _on_undo_clicked(self):
        """Manejar click en el botón Deshacer"""
        if self.controller.is_editing_new():
            # If new article, delete it and go back to list
            self.controller.delete()
            self.ui.stackedWidget.setCurrentIndex(1)
        else:
            # Reload from database
            self._load_form_from_article()
        
        self._lock_fields(True)
    
    def _on_delete_clicked(self):
        """Manejar click en el botón Borrar"""
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
        """Manejar click en el botón Siguiente"""
        if self.controller.next_article():
            self._load_form_from_article()
    
    def _on_prev_clicked(self):
        """Manejar click en el botón Anterior"""
        if self.controller.prev_article():
            self._load_form_from_article()
    
    def _on_search_clicked(self):
        """Manejar click en Buscar - cambiar a la vista de lista"""
        # Simply switch to the list view (page_2 with tablaBusqueda)
        self.ui.stackedWidget.setCurrentIndex(1)
        # Set focus on the table for immediate keyboard navigation
        self.ui.tablaBusqueda.setFocus()
    
    def _on_tab_changed(self, index: int):
        """Manejar cambio de pestaña"""
        # Reload data for the selected tab
        if not self._init_complete:
            return
        
        # If switching to graphics tab, update chart
        if index == 6:  # Graphics tab (tab_grafica is index 6)
            self._update_chart()
    
    # ==================== Chart Methods ====================
    
    def _setup_chart(self):
        """Inicializar el widget de gráficas"""
        # Create chart
        self.chart = QChart()
        self.chart.setTitle("Estadísticas Mensuales")
        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        
        # Set softer background color
        from PySide6.QtGui import QBrush, QColor
        self.chart.setBackgroundBrush(QBrush(QColor(248, 248, 248)))  # Gris muy suave
        
        # Set chart to the chart view
        self.ui.ChartViewWidget.setChart(self.chart)
        self.ui.ChartViewWidget.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Inicializar con datos vacíos
        self._create_empty_chart()
    
    def _create_empty_chart(self):
        """Create an empty chart with month labels"""
        self.chart.removeAllSeries()
        
        # Create bar series
        self.bar_series = QBarSeries()
        
        # Create bar set
        self.bar_set = QBarSet("Sin datos")
        self.bar_set.append([0] * 12)  # 12 months with 0 values
        
        self.bar_series.append(self.bar_set)
        
        # Add series to chart
        self.chart.addSeries(self.bar_series)
        
        # Create axes
        self.categories = ["Ene", "Feb", "Mar", "Abr", "May", "Jun",
                          "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        
        self.axis_x = QBarCategoryAxis()
        self.axis_x.append(self.categories)
        self.chart.addAxis(self.axis_x, Qt.AlignmentFlag.AlignBottom)
        self.bar_series.attachAxis(self.axis_x)
        
        self.axis_y = QValueAxis()
        self.axis_y.setRange(0, 100)
        self.chart.addAxis(self.axis_y, Qt.AlignmentFlag.AlignLeft)
        self.bar_series.attachAxis(self.axis_y)
    
    def _update_chart(self):
        """Update chart with current article data"""
        article = self.controller.get_current_article()
        if not article:
            self._create_empty_chart()
            return
        
        # Get monthly data based on selected option
        if self.ui.radGrafica_unidades.isChecked():
            data, title = self._get_monthly_units_data(article)
        else:
            data, title = self._get_monthly_amounts_data(article)
        
        # Clear existing series
        self.chart.removeAllSeries()
        
        # Create new bar series
        self.bar_series = QBarSeries()
        
        # Create bar set with data
        self.bar_set = QBarSet(title)
        self.bar_set.append(data)
        
        self.bar_series.append(self.bar_set)
        
        # Add series to chart
        self.chart.addSeries(self.bar_series)
        
        # Update chart title
        article_desc = article.get("descripcion_reducida", "Artículo")
        self.chart.setTitle(f"{article_desc} - {title}")
        
        # Remove existing axes if they exist
        for axis in self.chart.axes():
            self.chart.removeAxis(axis)
        
        # Create new axes
        self.axis_x = QBarCategoryAxis()
        self.axis_x.append(self.categories)
        self.chart.addAxis(self.axis_x, Qt.AlignmentFlag.AlignBottom)
        self.bar_series.attachAxis(self.axis_x)
        
        # Update Y axis range based on data
        max_value = max(data) if data and max(data) > 0 else 100
        y_max = max_value * 1.2  # Add 20% padding
            
        self.axis_y = QValueAxis()
        self.axis_y.setRange(0, y_max)
        self.chart.addAxis(self.axis_y, Qt.AlignmentFlag.AlignLeft)
        self.bar_series.attachAxis(self.axis_y)
    
    def _get_monthly_units_data(self, article):
        """Obtener datos mensuales de unidades desde el artículo"""
        # Intentar obtener datos desde los campos de la UI primero (lo que ve el usuario)
        ui_field_names = [
            "txtUnid_ventas_enero", "txtUnid_ventas_febrero", "txtUnid_ventas_marzo",
            "txtUnid_ventas_abril", "txtUnid_ventas_mayo", "txtUnid_ventas_junio",
            "txtUnid_ventas_julio", "txtUnid_ventas_agosto", "txtUnid_ventas_septiembre",
            "txtUnid_ventas_octubre", "txtUnid_ventas_noviembre", "txtUnid_ventas_diciembre"
        ]
        
        data = []
        for field_name in ui_field_names:
            if hasattr(self.ui, field_name):
                field = getattr(self.ui, field_name)
                try:
                    value = float(field.text().replace(",", "."))
                    data.append(value)
                except (ValueError, AttributeError):
                    data.append(0.0)
            else:
                data.append(0.0)
        
        # Si no hay datos en la UI, intentar obtenerlos desde la base de datos
        if all(x == 0 for x in data):
            months_units = [
                "unidades_vendidas_enero", "unidades_vendidas_febrero", "unidades_vendidas_marzo",
                "unidades_vendidas_abril", "unidades_vendidas_mayo", "unidades_vendidas_junio",
                "unidades_vendidas_julio", "unidades_vendidas_agosto", "unidades_vendidas_septiembre",
                "unidades_vendidas_octubre", "unidades_vendidas_noviembre", "unidades_vendidas_diciembre"
            ]
            
            for month_field in months_units:
                value = article.get(month_field, 0)
                try:
                    data.append(float(value))
                except (ValueError, TypeError):
                    data.append(0.0)
        
        # Si aún no hay datos, crear datos de ejemplo realistas basados en el stock
        if all(x == 0 for x in data):
            import random
            stock = float(article.get("stock_real", 25))
            base_sales = max(5, int(stock / 4))  # Base sales relative to stock
            
            data = []
            for i in range(12):
                # Simulate seasonal variations (summer and winter peaks)
                seasonal = 1.0
                if i in [5, 6, 7]:  # Jun, Jul, Aug - summer peak
                    seasonal = 1.4
                elif i in [10, 11]:  # Nov, Dec - winter peak  
                    seasonal = 1.3
                elif i in [0, 1]:  # Jan, Feb - post-holiday low
                    seasonal = 0.7
                
                monthly_sales = int(base_sales * seasonal * random.uniform(0.6, 1.4))
                data.append(float(monthly_sales))
        
        return data, "Unidades Vendidas"
    
    def _get_monthly_amounts_data(self, article):
        """Obtener datos mensuales de importes desde el artículo"""
        # Intentar obtener datos desde los campos de la UI primero
        ui_field_names = [
            "txtImporte_ventas_enero", "txtImporte_ventas_febrero", "txtImporte_ventas_marzo",
            "txtImporte_ventas_abril", "txtImporte_ventas_mayo", "txtImporte_ventas_junio",
            "txtImporte_ventas_julio", "txtImporte_ventas_agosto", "txtImporte_ventas_septiembre",
            "txtImporte_ventas_octubre", "txtImporte_ventas_noviembre", "txtImporte_ventas_diciembre"
        ]
        
        data = []
        for field_name in ui_field_names:
            if hasattr(self.ui, field_name):
                field = getattr(self.ui, field_name)
                try:
                    value = float(field.text().replace(",", ".").replace("€", ""))
                    data.append(value)
                except (ValueError, AttributeError):
                    data.append(0.0)
            else:
                data.append(0.0)
        
        # Si no hay datos en la UI, intentar obtenerlos desde la base de datos
        if all(x == 0 for x in data):
            months_amounts = [
                "importe_ventas_enero", "importe_ventas_febrero", "importe_ventas_marzo",
                "importe_ventas_abril", "importe_ventas_mayo", "importe_ventas_junio",
                "importe_ventas_julio", "importe_ventas_agosto", "importe_ventas_septiembre",
                "importe_ventas_octubre", "importe_ventas_noviembre", "importe_ventas_diciembre"
            ]
            
            for month_field in months_amounts:
                value = article.get(month_field, 0)
                try:
                    data.append(float(value))
                except (ValueError, TypeError):
                    data.append(0.0)
        
        # Si aún no hay datos, calcular a partir de las unidades y el precio
        if all(x == 0 for x in data):
            units_data, _ = self._get_monthly_units_data(article)
            coste = float(article.get("coste", 25))
            margen = float(article.get("margen", 30))
            pvp = coste * (1 + margen/100)
            data = [units * pvp for units in units_data]
        
        return data, "Importes de Ventas (€)"
    
    def _on_chart_type_changed(self):
        """Manejar cambio de tipo de gráfica"""
        # TODO: Implement when more chart types are added
        self._update_chart()
    
    def _on_chart_data_changed(self):
        """Manejar cambio de tipo de datos de la gráfica (unidades vs importes)"""
        if self._init_complete:
            self._update_chart()
    
    # ==================== Lookup Dialogs ====================
    
    def _on_buscar_seccion_clicked(self):
        """Abrir diálogo de búsqueda de secciones."""
        try:
            # Get secciones data directly from SQLAlchemy
            secciones_data = self.controller.get_secciones_data()
            
            if not secciones_data:
                QMessageBox.information(self, "Info", "No se encontraron secciones en la base de datos")
                return
            
            # Use DBConsultaView.select_from_data - no QSqlDatabase needed!
            selected_data, record = DBConsultaView.select_from_data(
                parent=self,
                data=secciones_data,
                headers=["ID", "Código", "Sección"],
                campos=["codigo", "seccion"],
                titulo="Seleccionar Sección"
            )
            
            if selected_data:
                # Get selected values directly from dictionary
                seccion_id = selected_data.get('id')
                seccion_codigo = selected_data.get('codigo')
                seccion_nombre = selected_data.get('seccion')
                
                # Update controller
                if self.controller.set_seccion_from_lookup(seccion_id, seccion_codigo, seccion_nombre):
                    # Update UI field
                    self.ui.txtseccion.setText(seccion_nombre)


                    # Note: controller.set_seccion_from_lookup already clears dependent ids

                    # Clear family/subfamily UI fields
                    if hasattr(self.ui, 'txtfamilia'):
                        self.ui.txtfamilia.clear()
                    if hasattr(self.ui, 'txtsubfamilia'):
                        self.ui.txtsubfamilia.clear()

                    # Update family/subfamily button states: family enabled only if editing, subfamily disabled
                    editing = self.ui.botGuardar.isEnabled()
                    if hasattr(self.ui, 'botBuscarFamilia'):
                        # family enabled only if editing (controller will ensure family None until selected)
                        self.ui.botBuscarFamilia.setEnabled(editing and True)
                    if hasattr(self.ui, 'botBuscarSubfamilia'):
                        self.ui.botBuscarSubfamilia.setEnabled(False)

                    print(f"✅ Sección seleccionada: {seccion_codigo} - {seccion_nombre}")
                else:
                    QMessageBox.warning(self, "Error", "No se pudo actualizar la sección")
        
        except Exception as e:
            print(f"Error opening section lookup: {e}")
            QMessageBox.critical(self, "Error", f"Error al abrir consulta de secciones: {str(e)}")

    def _on_buscar_familia_clicked(self):
        """Abrir diálogo de búsqueda de familias y actualizar controller/modelo/vista (MVC)."""
        try:
            # Families depend on section; obtain current article's section and filter families
            current = self.controller.get_current_article() or {}
            id_seccion = current.get('id_seccion')
            if not id_seccion:
                QMessageBox.information(self, "Info", "Seleccione primero una sección para listar las familias correspondientes")
                return

            familias_data = self.controller.get_familias_data(id_seccion)

            if not familias_data:
                QMessageBox.information(self, "Info", "No se encontraron familias en la base de datos")
                return

            selected_data, record = DBConsultaView.select_from_data(
                parent=self,
                data=familias_data,
                headers=["ID", "Código", "Familia"],
                campos=["codigo", "familia"],
                titulo="Seleccionar Familia"
            )

            if selected_data:
                familia_id = selected_data.get('id')
                familia_codigo = selected_data.get('codigo')
                familia_nombre = selected_data.get('familia')

                # Delegate state change to controller (MVC)
                if self.controller.set_familia_from_lookup(familia_id, familia_codigo, familia_nombre):
                    self.ui.txtfamilia.setText(familia_nombre)
                    print(f"✅ Familia seleccionada: {familia_codigo} - {familia_nombre}")

                    # Si estamos en modo edición, habilitar subfamilia (ahora que hay familia)
                    locked = self.ui.botGuardar.isEnabled() == False
                    # locked True means fields are read-only; we want enabled when not locked
                    if hasattr(self.ui, 'botBuscarSubfamilia') and not locked:
                        self.ui.botBuscarSubfamilia.setEnabled(True)
                    # Clear subfamily UI because a family change invalidates previous subfamily
                    if hasattr(self.ui, 'txtsubfamilia'):
                        self.ui.txtsubfamilia.clear()
                else:
                    QMessageBox.warning(self, "Error", "No se pudo actualizar la familia")

        except Exception as e:
            print(f"Error opening family lookup: {e}")
            QMessageBox.critical(self, "Error", f"Error al abrir consulta de familias: {str(e)}")

    def _on_buscar_subfamilia_clicked(self):
        """Abrir diálogo de búsqueda de subfamilias y actualizar controller/modelo/vista (MVC)."""
        try:
            # Si hay familia seleccionada, filtramos subfamilias por esa familia
            current = self.controller.get_current_article() or {}
            id_familia = current.get('id_familia')

            # Si no hay familia seleccionada, mostrar hint y no abrir diálogo
            if not id_familia:
                # Mostrar mensaje orientativo al usuario
                from PySide6.QtWidgets import QMessageBox
                QMessageBox.information(
                    self,
                    "Info",
                    "Antes de buscar subfamilias, seleccione primero una familia."
                )

                # Añadir tooltip informativo al botón para UX
                if hasattr(self.ui, 'botBuscarSubfamilia'):
                    self.ui.botBuscarSubfamilia.setToolTip("Seleccione una familia antes de buscar subfamilias")

                return

            subfamilias_data = self.controller.get_subfamilias_data(id_familia)

            if not subfamilias_data:
                QMessageBox.information(self, "Info", "No se encontraron subfamilias en la base de datos")
                return

            selected_data, record = DBConsultaView.select_from_data(
                parent=self,
                data=subfamilias_data,
                headers=["ID", "Código", "Subfamilia"],
                campos=["codigo", "subfamilia"],
                titulo="Seleccionar Subfamilia"
            )

            if selected_data:
                sub_id = selected_data.get('id')
                sub_codigo = selected_data.get('codigo')
                sub_nombre = selected_data.get('subfamilia')

                if self.controller.set_subfamilia_from_lookup(sub_id, sub_codigo, sub_nombre):
                    self.ui.txtsubfamilia.setText(sub_nombre)
                    print(f"✅ Subfamilia seleccionada: {sub_codigo} - {sub_nombre}")
                else:
                    QMessageBox.warning(self, "Error", "No se pudo actualizar la subfamilia")

        except Exception as e:
            print(f"Error opening subfamily lookup: {e}")
            QMessageBox.critical(self, "Error", f"Error al abrir consulta de subfamilias: {str(e)}")
    
    # ==================== Promociones Logic ====================
    
    def _on_articulo_promocionado_changed(self, checked: bool):
        """
        Habilitar/deshabilitar campos de fecha de oferta según el estado del checkbox.
        Si chkArticulo_promocionado está marcado, habilitar txtOferta_Fecha_ini y txtOferta_Fecha_fin.
        Si está desmarcado, deshabilitar estos campos.
        """
        # Only allow editing the date fields if the checkbox is checked AND
        # we are in edit mode. Edit mode is determined by the 'Guardar'
        # button being enabled (set by _lock_fields).
        editing = False
        if hasattr(self.ui, 'botGuardar'):
            try:
                editing = self.ui.botGuardar.isEnabled()
            except Exception:
                editing = False

        enable_dates = checked and editing
        self.ui.txtOferta_Fecha_ini.setEnabled(enable_dates)
        self.ui.txtOferta_Fecha_fin.setEnabled(enable_dates)
        
        # Actualizar visibilidad del label de promoción en el header
        self.ui.lbl_en_promocion.setVisible(checked)

    # ==================== Promotions button handlers ====================
    def _enable_oferta_editing(self, enable: bool):
        """Toggle UI state for editing a promotion within the promotions frame."""
        # Note: do not disable/enable the whole frame here; _lock_fields controls framePromocion

        try:
            if hasattr(self.ui, 'btnguardar_oferta'):
                self.ui.btnguardar_oferta.setEnabled(enable)
        except Exception:
            pass
        try:
            if hasattr(self.ui, 'btnDeshacerOferta'):
                self.ui.btnDeshacerOferta.setEnabled(enable)
        except Exception:
            pass

        # When editing we must disable the add/edit buttons to prevent nested operations
        try:
            if hasattr(self.ui, 'btnAnadirOferta'):
                # If disabling editing, re-enable add/edit according to overall edit state
                if not enable:
                    # add/edit should be active if article is in edit mode and promotions tab active
                    promo_tab_active = False
                    try:
                        if hasattr(self.ui, 'Pestanas') and self.ui.Pestanas.currentWidget() is not None:
                            promo_tab_active = (self.ui.Pestanas.currentWidget().objectName() == 'tab_promociones')
                    except Exception:
                        promo_tab_active = False
                    article_editing = self.ui.botGuardar.isEnabled()
                    self.ui.btnAnadirOferta.setEnabled(article_editing and promo_tab_active)
                else:
                    self.ui.btnAnadirOferta.setEnabled(False)
        except Exception:
            pass
        try:
            if hasattr(self.ui, 'btnEditarOferta'):
                if not enable:
                    promo_tab_active = False
                    try:
                        if hasattr(self.ui, 'Pestanas') and self.ui.Pestanas.currentWidget() is not None:
                            promo_tab_active = (self.ui.Pestanas.currentWidget().objectName() == 'tab_promociones')
                    except Exception:
                        promo_tab_active = False
                    article_editing = self.ui.botGuardar.isEnabled()
                    self.ui.btnEditarOferta.setEnabled(article_editing and promo_tab_active)
                else:
                    self.ui.btnEditarOferta.setEnabled(False)
        except Exception:
            pass

    def _on_add_oferta(self):
        """User clicked 'Añadir oferta' — enter oferta edit mode (new oferta).

        Enable save/undo and disable add/edit controls until saved or undone.
        """
        # Mark internal state (optional)
        self._editing_oferta = True

        # Clear oferta form fields if present and enable editing
        try:
            if hasattr(self.ui, 'txtOferta_Descripcion_promocion'):
                self.ui.txtOferta_Descripcion_promocion.clear()
        except Exception:
            pass

        self._enable_oferta_editing(True)

    def _on_edit_oferta(self):
        """User clicked 'Editar oferta' — enable editing existing oferta."""
        self._editing_oferta = True
        self._enable_oferta_editing(True)

    def _on_save_oferta(self):
        """User clicked 'Guardar oferta' — perform basic save workflow and exit edit mode.

        Note: detailed persistence is handled when the article is saved via self._on_save_clicked
        — this handler toggles UI state only.
        """
        try:
            # For UX: disable editing buttons immediately to prevent double clicks while saving
            self._enable_oferta_editing(False)
        finally:
            self._editing_oferta = False

    def _on_undo_oferta(self):
        """User clicked 'Deshacer oferta' — cancel changes and exit edit mode."""
        # Reload oferta values from controller (if available) — otherwise just disable editing
        try:
            current = None
            if hasattr(self, 'controller') and hasattr(self.controller, 'get_current_article'):
                current = self.controller.get_current_article()
            # If we have loaded data, restore description and dates
            if current and isinstance(current, dict):
                if hasattr(self.ui, 'txtOferta_Descripcion_promocion'):
                    try:
                        self.ui.txtOferta_Descripcion_promocion.setText(str(current.get('descripcion', '') or ''))
                    except Exception:
                        pass
        except Exception:
            pass

        # Exit editing
        self._editing_oferta = False
        self._enable_oferta_editing(False)


class ArticlesTableModel(QAbstractTableModel):
    """Modelo de tabla para la lista de artículos"""
    
    def __init__(self):
        super().__init__()
        self.articles = []
        self.headers = ["Código", "Descripción", "Stock", "PVP"]
        # Determine decimals for display
        try:
            vals = get_company_decimal_settings()
            self.decimales_precios = vals.get('decimales_precios', 2)
        except Exception:
            self.decimales_precios = 2
    
    def set_articles(self, articles):
        """Set articles data"""
        # Validar que la entrada contiene la columna precio_venta — fallar pronto si falta
        if articles:
            for art in articles:
                # We require the key to be present in the returned rows
                if 'precio_venta' not in art or art.get('precio_venta') is None:
                    raise RuntimeError(
                        "Missing required column 'precio_venta' in articulos results. "
                        "Please add column precio_venta to the articulos table and run migrations before proceeding."
                    )

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
            elif column == 3:  # PVP / Precio venta
                # Preferir la columna precio_venta explícita si está presente en el diccionario del artículo
                # precio_venta debe estar presente y no ser NULL — fallar pronto
                if 'precio_venta' not in article:
                    raise RuntimeError(
                        "Missing required column 'precio_venta' in articulos results. "
                        "Please add column precio_venta to the articulos table and run migrations before proceeding."
                    )

                pv_val = article.get('precio_venta')
                if pv_val is None:
                    raise RuntimeError(
                        "Column 'precio_venta' present but contains NULL for an article — this must be populated."
                    )

                try:
                    pv_val = float(pv_val or 0)
                except Exception:
                    pv_val = 0.0

                # Format using company decimal preferences with comma for display
                pv_text = format_decimal_value(pv_val, self.decimales_precios, use_comma=True)
                # Mostrar el símbolo de euro a la derecha según convención europea
                # Ejemplo: "122,00 €"
                return f"{pv_text} €"
        
        elif role == Qt.ItemDataRole.TextAlignmentRole:
            if column in [2, 3]:  # Stock y PVP alineados a la derecha
                return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        
        return None
