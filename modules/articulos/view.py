from PySide6.QtWidgets import QWidget, QMessageBox, QLineEdit, QComboBox, QTextEdit, QCheckBox, QDateEdit, QDoubleSpinBox, QHeaderView, QListWidgetItem
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, QDate
from PySide6.QtCharts import QChart, QBarSet, QBarSeries, QBarCategoryAxis, QValueAxis
from PySide6.QtGui import QPainter, QBrush, QColor
from modules.articulos.ui_frmarticulos import Ui_FrmArticulos
from modules.articulos.controller import ArticuloController
from modules.common.db_consulta_view import DBConsultaView
from core.db import get_current_database, set_current_database
import logging
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
        # Guard used to avoid re-entrancy / duplicate lookups when F1 is
        # handled both by a local QShortcut and by application-level
        # eventFilter (ShortcutOverride). The guard prevents DBConsultaView
        # from being opened twice in quick succession.
        self._tipo_lookup_running = False
        # last invocation timestamp to avoid duplicate open after modal closes
        self._last_tipo_lookup_time = 0.0
        # small time-window to suppress duplicate KeyPress after we handled
        # ShortcutOverride and opened the lookup (prevents two dialogs when
        # ShortcutOverride triggers then KeyPress arrives later).
        self._suppress_next_keypress_until = 0.0
        # Flags for oferta workflow
        self._editing_oferta = False
        self._creating_oferta = False
        self._current_oferta_id = None
        self._created_db_row = False
        
        # Initialize UI
        self._setup_connections()
        self._setup_initial_state()
        
        self._init_complete = True

    def _coerce_flag(self, val, default=False):
        """Coerce various DB/JSON values to a boolean flag.

        Handles ints (0/1), strings ('0','1','true','false'), booleans and None.
        Returns `default` when `val` is None or cannot be interpreted.
        """
        try:
            if val is None:
                return default
            if isinstance(val, bool):
                return val
            # ints (SQLAlchemy may return ints)
            if isinstance(val, int):
                return bool(val)
            # strings
            s = str(val).strip().lower()
            if s in ('1', 'true', 't', 'yes', 'y'):
                return True
            if s in ('0', 'false', 'f', 'no', 'n', ''):
                return False
            # try numeric conversion
            try:
                return bool(int(s))
            except Exception:
                return default
        except Exception:
            return default
    
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
                logging.getLogger(__name__).debug("Switched to articles database: artstudio3d")
            except Exception as e:
                logging.getLogger(__name__).exception("Error switching to articles database: %s", e)
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
        # setup_connections finished
        # Offer-type radio toggles (only present for the promotions frame)
        try:
            if hasattr(self.ui, 'chkOferta_32'):
                self.ui.chkOferta_32.toggled.connect(self._sync_oferta_type_fields)
            if hasattr(self.ui, 'chkOferta_dto'):
                self.ui.chkOferta_dto.toggled.connect(self._sync_oferta_type_fields)
            if hasattr(self.ui, 'chkOferta_web'):
                self.ui.chkOferta_web.toggled.connect(self._sync_oferta_type_fields)
            # Normalized PVP radio name (from generated UI)
            if hasattr(self.ui, 'chkOfertaPvp'):
                self.ui.chkOfertaPvp.toggled.connect(self._sync_oferta_type_fields)
            # Promotions frame action buttons
            if hasattr(self.ui, 'btnAnadirOferta'):
                self.ui.btnAnadirOferta.clicked.connect(self._on_add_oferta)
            if hasattr(self.ui, 'btnEditarOferta'):
                self.ui.btnEditarOferta.clicked.connect(self._on_edit_oferta)
            if hasattr(self.ui, 'btnguardar_oferta'):
                self.ui.btnguardar_oferta.clicked.connect(self._on_save_oferta)
            if hasattr(self.ui, 'btnDeshacerOferta'):
                self.ui.btnDeshacerOferta.clicked.connect(self._on_undo_oferta)
            # Ensure PVP fixed-price widgets normalize/format on editing finished
            # Normalized PVP fixed-price widget name
            for candidate in ('txtofertaPvpFijo',):
                w = getattr(self.ui, candidate, None)
                if w is not None:
                    try:
                        # connect once only
                        if not getattr(w, '_currency_format_hooked', False):
                            w.editingFinished.connect(lambda _w=w: self._format_price_field(_w))
                            setattr(w, '_currency_format_hooked', True)
                    except Exception:
                        pass
            # Tipo lookup: when user finishes editing the Código Tipo field, attempt lookup
            if hasattr(self.ui, 'txtCodigoTipo'):
                try:
                    self.ui.txtCodigoTipo.editingFinished.connect(self._on_codigo_tipo_entered)
                except Exception:
                    pass
                # Bind F1 to open the tipo lookup when focused
                try:
                    from PySide6.QtGui import QKeySequence, QShortcut
                    # Keep a reference on the view so the QShortcut isn't garbage collected
                    # Create the QShortcut on the view (self) and set context so it
                    # activates when children widgets (like txtCodigoTipo) have focus.
                    if not hasattr(self, '_shortcut_txtCodigoTipo'):
                        # Use Ctrl+F for the field lookup so the main window keeps F1
                        # mapped to the global panel toggle.
                        self._shortcut_txtCodigoTipo = QShortcut(QKeySequence("Ctrl+F"), self)
                        # Make sure it's active while the widget or any children have focus
                        try:
                            self._shortcut_txtCodigoTipo.setContext(Qt.ShortcutContext.WidgetWithChildrenShortcut)
                        except Exception:
                            # Older Qt/PySide variants may have different enum locations; ignore if unavailable
                            pass
                        # Only open the tipo lookup when focus is on txtCodigoTipo and we are in edit mode
                        def _f1_handler():
                            try:
                                if not hasattr(self.ui, 'txtCodigoTipo'):
                                    return
                                # Only trigger when the txtCodigoTipo widget has focus
                                if self.ui.txtCodigoTipo.hasFocus():
                                    # Also require we are editing (botGuardar enabled)
                                    editing_flag = False
                                    try:
                                        editing_flag = bool(self.ui.botGuardar.isEnabled())
                                    except Exception:
                                        editing_flag = False

                                    if editing_flag:
                                        self._on_buscar_tipo_clicked()
                            except Exception:
                                # don't propagate UI errors
                                logging.getLogger(__name__).exception("Error handling Ctrl+F for txtCodigoTipo")

                        self._shortcut_txtCodigoTipo.activated.connect(_f1_handler)

                    # Provide a helpful tooltip so users discover the shortcut (best-effort)
                    try:
                        self.ui.txtCodigoTipo.setToolTip(self.tr("Ctrl+F - Buscar tipo"))
                    except Exception:
                        # Non-fatal if UI doesn't support tooltips
                        pass
                except Exception:
                    # outer import/shortcut setup failed; ignore in test environments
                    pass

        except Exception:
            # Signals may not be available in test environment; ignore
            pass
    
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

        # Agregar elementos de prueba al QListWidget
        try:
            list_colors = self.ui.listColors
            if list_colors:
                colores_prueba = [
                    ("Rojo", QColor(255, 0, 0)),
                    ("Verde", QColor(0, 255, 0)),
                    ("Azul", QColor(0, 0, 255)),
                    ("Amarillo", QColor(255, 255, 0)),
                ]
                for nombre, color in colores_prueba:
                    item = QListWidgetItem(nombre)
                    item.setBackground(QBrush(color))
                    # Qt.white no existe en algunas versiones de PySide; usar QColor blanca explícita
                    item.setForeground(QBrush(QColor(255, 255, 255)))
                    list_colors.addItem(item)
        except Exception as e:
            logging.getLogger(__name__).exception("Error agregando colores de prueba: %s", e)

        # Make colours list look like a graphical palette (small square swatches,
        # no visible labels, clear selection highlight). This is intentionally
        # defensive: done inside try/except because tests / headless runners
        # may not be able to create QPixmaps/QPainters.
        try:
            self._decorate_colors_list_as_palette()
        except Exception as e:
            logging.getLogger(__name__).exception("Error decorando la paleta de colores: %s", e)



    def _maybe_warn(self, title: str, message: str):
        """Delegate to central UI helper which avoids modals during test runs."""
        try:
            from core.ui_helpers import show_warning
            show_warning(self, title, message)
        except Exception:
            # Fallback to simple print in any unexpected error
            try:
                logging.getLogger(__name__).warning(f"{title}: {message}")
            except Exception:
                pass

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

    def _apply_tipo_flags_to_ui(self, requiere_ean: bool, proveedor_flag: bool):
        """Show or hide UI elements based on articulo_tipo flags.

        - requiere_ean -> shows/hides txtcodigo_barras and its label (label_3)
        - proveedor_flag -> shows/hides txtcodigo_fabricante and its label (label_4)
        """
        try:
            # EAN field + label. UI sometimes names the label differently
            # (older generators used 'label_3', newer UI uses 'lblCodigoEAN').
            if hasattr(self.ui, 'txtcodigo_barras'):
                try:
                    self.ui.txtcodigo_barras.setVisible(bool(requiere_ean))
                except Exception:
                    pass
            # Prefer explicit named label if present
            if hasattr(self.ui, 'lblCodigoEAN'):
                try:
                    self.ui.lblCodigoEAN.setVisible(bool(requiere_ean))
                except Exception:
                    pass
            else:
                if hasattr(self.ui, 'label_3'):
                    try:
                        self.ui.label_3.setVisible(bool(requiere_ean))
                    except Exception:
                        pass

            # Fabricante-related field
            if hasattr(self.ui, 'txtcodigo_fabricante'):
                try:
                    self.ui.txtcodigo_fabricante.setVisible(bool(proveedor_flag))
                except Exception:
                    pass

            # Provider-related fields - current widget names (with proper casing)
            # - provider label: 'lblProveedorHabitual'
            # - provider code field: 'txtCodigoProveedor'
            # - provider name field: 'txtProveedor'
            # Keep old names for backwards compatibility
            try:
                visible = bool(proveedor_flag)
            except Exception:
                visible = False

            # Label for "Proveedor Habitual:" - try all possible names
            for lbl_name in ('lblProveedorHabitual', 'lblProveedorhabitual', 'label_8', 'lblCodigoenProveedor', 'label_4'):
                if hasattr(self.ui, lbl_name):
                    try:
                        getattr(self.ui, lbl_name).setVisible(visible)
                    except Exception:
                        pass

            # Proveedor code field - try all possible names
            for field_name in ('txtCodigoProveedor', 'txtcodigo_proveedor'):
                if hasattr(self.ui, field_name):
                    try:
                        getattr(self.ui, field_name).setVisible(visible)
                    except Exception:
                        pass
            
            # Proveedor name field - try all possible names
            for field_name in ('txtProveedor', 'txtproveedor'):
                if hasattr(self.ui, field_name):
                    try:
                        getattr(self.ui, field_name).setVisible(visible)
                    except Exception:
                        pass
        except Exception:
            logging.getLogger(__name__).exception("Error applying tipo flags to UI")

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
                display_text = self.tr("{desc} ({pct}%)").format(desc=iva['descripcion'], pct=iva['porcentaje'])
                # Store the ID as user data
                self.ui.cboTipoIVA.addItem(display_text, iva['id'])
            
            logging.getLogger(__name__).info(f"✓ Loaded {len(iva_types)} IVA types")
            
        except Exception:
            logging.getLogger(__name__).exception("Error populating IVA combo")
            # Add a default option if error
            self.ui.cboTipoIVA.clear()
            self.ui.cboTipoIVA.addItem(self.tr("Error cargando tipos IVA"), None)

    def _decorate_colors_list_as_palette(self):
        """Convert the simple QListWidget into a colour-palette-style widget.

        This draws small rounded square swatches for each item using the
        item's background/foreground brush, hides textual labels (keeps them
        as tooltips) and reduces the icon/grid size so it looks like a
        graphics-program palette.

        The function is intentionally defensive: UI unit tests and CI runners
        may run headless or without a GUI; any exceptions are swallowed so
        we don't break the rest of the view initialization.
        """
        # Lightweight, very safe implementation: avoid any heavy GUI ops here
        # (the full rendering logic was moved into a separate safe block and
        # will be re-introduced when CI/headless concerns are resolved).
        try:
            lw = getattr(self.ui, 'listColors', None)
            if not lw:
                return
            # Ensure the list is in icon mode with a small icon size so it
            # will look like a palette even if we cannot paint swatches.
            from PySide6.QtCore import QSize
            try:
                lw.setGridSize(QSize(56, 56))
            except Exception:
                pass
            try:
                lw.setIconSize(QSize(44, 44))
            except Exception:
                pass
            try:
                lw.setSpacing(8)
            except Exception:
                pass
            try:
                lw.setViewMode(lw.ViewMode.IconMode)
            except Exception:
                pass

            # Compute whether we are allowed to paint QPixmaps (best-effort):
            # avoid painting in headless/offscreen environments which can abort
            try:
                import os
                from PySide6.QtGui import QGuiApplication
                _platform = os.environ.get('QT_QPA_PLATFORM', '').lower()
                # Asumimos que podemos pintar a menos que estemos en modo offscreen/minimal
                _can_paint = _platform not in ('offscreen', 'minimal')
                # Si no hay variable de entorno, asumimos entorno gráfico normal
                if not _platform:
                    _can_paint = True
            except Exception:
                # En caso de error, asumimos que podemos intentar pintar
                _can_paint = True

            # Hide textual labels (keep them as tooltips) so the list looks like
            # a palette of swatches rather than a list of named colours.
            for i in range(lw.count()):
                try:
                    it = lw.item(i)
                    if it is None:
                        continue
                    # keep label as tooltip
                    try:
                        lbl = it.text()
                        it.setToolTip(lbl or '')
                    except Exception:
                        pass
                    try:
                        it.setText('')
                    except Exception:
                        pass

                    # Determine if we should create QPixmap icons for this run.
                    _has_screen = _can_paint

                    # Build a small rounded swatch icon matching the intended
                    # colour. Prefer background brush, fall back to toolTip/name
                    # mapping, then foreground. Use defensive try/except because
                    # QPixmap/QPainter might fail in headless CI.
                    try:
                        colour = None
                        bg = it.background()
                        try:
                            if bg and hasattr(bg, 'color'):
                                colour = bg.color()
                        except Exception:
                            colour = None

                        if colour is None:
                            # try using tooltip or text (localized names) as fallback
                            # Use ItemDataRole enum for compatibility
                            name = (it.toolTip() or it.data(Qt.ItemDataRole.DisplayRole) or '').strip().lower()
                            # quick mapping for names we know are used in ui_frmarticulos
                            name_map = {
                                'blanco': QColor(255, 255, 255),
                                'negro': QColor(0, 0, 0),
                                'rojo': QColor(170, 0, 0),
                                'azul': QColor(0, 0, 127),
                            }
                            if name in name_map:
                                colour = name_map[name]

                        if colour is None:
                            try:
                                fg = it.foreground()
                                if fg and hasattr(fg, 'color'):
                                    colour = fg.color()
                            except Exception:
                                colour = None

                        if colour is None:
                            # last resort: neutral gray
                            colour = QColor(200, 200, 200)

                        # create pixmap icon (rounded rect) sized to iconSize or grid
                        if not _has_screen:
                            # skip painting icons in headless/offscreen environments
                            pass
                        else:
                            try:
                                from PySide6.QtGui import QPixmap, QPainter, QIcon
                                from PySide6.QtCore import QRect
                                # icon size should match list icon size when possible
                                isz = lw.iconSize() if hasattr(lw, 'iconSize') else None
                                if isz and isz.width() > 0 and isz.height() > 0:
                                    pix = QPixmap(isz.width(), isz.height())
                                else:
                                    pix = QPixmap(44, 44)

                                pix.fill(QColor(0, 0, 0, 0))
                                p = QPainter(pix)
                                try:
                                    p.setRenderHint(QPainter.RenderHint.Antialiasing)
                                    r = pix.rect().adjusted(2, 2, -2, -2)
                                    p.setBrush(colour)
                                    # Choose a contrasting outline depending on luminance so
                                    # swatches remain visible on similar backgrounds.
                                    try:
                                        rcol = colour
                                        rr = rcol.red(); rg = rcol.green(); rb = rcol.blue()
                                        lum = (0.299*rr + 0.587*rg + 0.114*rb)
                                    except Exception:
                                        lum = 200

                                    if lum > 180:
                                        outline = QColor(0, 0, 0, 200)
                                    else:
                                        outline = QColor(255, 255, 255, 200)

                                    # draw slight outer shadow for depth (semi-transparent)
                                    try:
                                        shadow = QColor(0, 0, 0, 30)
                                        p.setPen(shadow)
                                        sh_r = pix.rect().adjusted(3, 3, -1, -1)
                                        p.drawRoundedRect(sh_r, 6, 6)
                                    except Exception:
                                        pass

                                    # main swatch
                                    p.setPen(outline)
                                    p.drawRoundedRect(r, 6, 6)
                                finally:
                                    p.end()

                                try:
                                    it.setIcon(QIcon(pix))
                                except Exception:
                                    # setting icon may fail in some PySide builds; ignore
                                    pass
                            except Exception:
                                # If QPixmap isn't available (headless), skip icon creation
                                pass
                    except Exception:
                        # non-fatal - continue building remaining items
                        pass
                except Exception:
                    pass

            try:
                # subtle selection border to match a palette feel
                lw.setStyleSheet('QListWidget::item{border:1px solid transparent; margin:3px; padding:0px;} QListWidget::item:selected{border:3px solid #1976d2; border-radius:6px; margin:-2px;} QListWidget::item:hover{border:1px solid rgba(0,0,0,40);}')
            except Exception:
                pass
        except Exception:
            logging.getLogger(__name__).exception("Error decorating colors palette")
    
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
        # Try both old and new widget names for backwards compatibility
        id_proveedor = article.get("id_proveedor")
        if id_proveedor:
            cod_prov, nombre_prov = self.controller.get_proveedor_info(id_proveedor)
            # Set provider code - try new name first, then old name
            if hasattr(self.ui, 'txtCodigoProveedor'):
                self.ui.txtCodigoProveedor.setText(cod_prov or "")
            elif hasattr(self.ui, 'txtcodigo_proveedor'):
                self.ui.txtcodigo_proveedor.setText(cod_prov or "")
            # Set provider name - try new name first, then old name
            if hasattr(self.ui, 'txtProveedor'):
                self.ui.txtProveedor.setText(nombre_prov or "")
            elif hasattr(self.ui, 'txtproveedor'):
                self.ui.txtproveedor.setText(nombre_prov or "")
        else:
            # Clear provider fields
            if hasattr(self.ui, 'txtCodigoProveedor'):
                self.ui.txtCodigoProveedor.clear()
            elif hasattr(self.ui, 'txtcodigo_proveedor'):
                self.ui.txtcodigo_proveedor.clear()
            if hasattr(self.ui, 'txtProveedor'):
                self.ui.txtProveedor.clear()
            elif hasattr(self.ui, 'txtproveedor'):
                self.ui.txtproveedor.clear()

        # Tipo: show codigo and descripcion if present
        # Initialize flags to default (hidden)
        requiere_ean = False
        proveedor_flag = False
        
        id_tipo = article.get('id_tipo')
        if id_tipo:
            try:
                t = self.controller.repository.get_articulo_tipo(id_tipo)
                if t:
                    if hasattr(self.ui, 'txtCodigoTipo'):
                        self.ui.txtCodigoTipo.setText(str(t.get('codigo') or ''))
                    if hasattr(self.ui, 'txtDescripcionTipo'):
                        self.ui.txtDescripcionTipo.setText(str(t.get('descripcion') or ''))
                    
                    # Extract tipo flags
                    requiere_ean = self._coerce_flag(t.get('requiereEAN'), default=False)
                    proveedor_flag = self._coerce_flag(t.get('proveedor'), default=False)
                    
                    # Store transient flags in current article
                    try:
                        if self.controller.current_article is not None:
                            self.controller.current_article['tipo_requiereEAN'] = requiere_ean
                            self.controller.current_article['tipo_proveedor'] = proveedor_flag
                    except Exception:
                        pass
                else:
                    # No tipo found - use fallback fields from article
                    if hasattr(self.ui, 'txtCodigoTipo'):
                        self.ui.txtCodigoTipo.setText(str(article.get('codigo_tipo') or ''))
                    if hasattr(self.ui, 'txtDescripcionTipo'):
                        self.ui.txtDescripcionTipo.setText(str(article.get('descripcion_tipo') or ''))
                    
                    # Clear transient flags
                    try:
                        if self.controller.current_article is not None:
                            self.controller.current_article.pop('tipo_requiereEAN', None)
                            self.controller.current_article.pop('tipo_proveedor', None)
                    except Exception:
                        pass
            except Exception:
                # Error fetching tipo - use fallback fields from article
                if hasattr(self.ui, 'txtCodigoTipo'):
                    self.ui.txtCodigoTipo.setText(str(article.get('codigo_tipo') or ''))
                if hasattr(self.ui, 'txtDescripcionTipo'):
                    self.ui.txtDescripcionTipo.setText(str(article.get('descripcion_tipo') or ''))
                
                # Clear transient flags
                try:
                    if self.controller.current_article is not None:
                        self.controller.current_article.pop('tipo_requiereEAN', None)
                        self.controller.current_article.pop('tipo_proveedor', None)
                except Exception:
                    pass
        else:
            # No tipo ID - use fallback fields from article
            if hasattr(self.ui, 'txtCodigoTipo'):
                self.ui.txtCodigoTipo.setText(str(article.get('codigo_tipo') or ''))
            if hasattr(self.ui, 'txtDescripcionTipo'):
                self.ui.txtDescripcionTipo.setText(str(article.get('descripcion_tipo') or ''))
            
            # Clear transient flags
            try:
                if self.controller.current_article is not None:
                    self.controller.current_article.pop('tipo_requiereEAN', None)
                    self.controller.current_article.pop('tipo_proveedor', None)
            except Exception:
                pass
        
        # ALWAYS apply tipo flags to UI (show/hide fields based on tipo configuration)
        # This ensures provider fields are shown/hidden correctly every time an article is loaded
        # Special behaviour: if the tipo code field is empty after loading the article
        # we must show provider fields by default (requirement from product owner).
        try:
            if hasattr(self.ui, 'txtCodigoTipo'):
                try:
                    if (self.ui.txtCodigoTipo.text() or '').strip() == '':
                        proveedor_flag = True
                except Exception:
                    pass
        except Exception:
            pass

        self._apply_tipo_flags_to_ui(requiere_ean, proveedor_flag)

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
            """Convertir varios tipos (date, datetime, objeto con year/month/day) a QDate.

            Maneja year/month/day como atributo o como callable (p.ej. d.year()).
            Devuelve QDate() en caso de fallo.
            """
            # Usar helper centralizado para convertir objetos Python date/datetime -> QDate
            # (evita duplicar lógica y cubre casos donde year/month/day son métodos o atributos)
            from core.utils import pydate_to_qdate as _pydate_helper
            return _pydate_helper(d)

        if hasattr(self.ui, 'txtOferta_Fecha_ini'):
            self.ui.txtOferta_Fecha_ini.setDate(_to_qdate(fecha_ini))
        if hasattr(self.ui, 'txtOferta_Fecha_fin'):
            self.ui.txtOferta_Fecha_fin.setDate(_to_qdate(fecha_fin))
        # Populate other oferta controls if we have oferta data merged into current article
        try:
            curr = self.controller.get_current_article() or {}
            # Store current oferta id for later save/delete
            if 'oferta_id' in curr:
                self._current_oferta_id = curr.get('oferta_id')

            if hasattr(self.ui, 'txtOferta_Descripcion_promocion'):
                val = curr.get('oferta_descripcion') or ''
                try:
                    self.ui.txtOferta_Descripcion_promocion.setText(str(val))
                except Exception:
                    pass

            if hasattr(self.ui, 'txtOfertaPorCada'):
                try:
                    v = curr.get('oferta_unidades')
                    if v is None:
                        v = ''
                    else:
                        v = str(int(v)) if float(v).is_integer() else str(v)
                    self.ui.txtOfertaPorCada.setText(v)
                except Exception:
                    pass

            if hasattr(self.ui, 'txtOfertaregaloUnidades'):
                try:
                    v = curr.get('oferta_regalo')
                    self.ui.txtOfertaregaloUnidades.setText(str(int(v)) if v and float(v).is_integer() else (str(v) if v is not None else ''))
                except Exception:
                    pass

            # price/pvp fixed field canonical name
            pvp_widget = getattr(self.ui, 'txtofertaPvpFijo', None)
            if pvp_widget is not None:
                try:
                    v = curr.get('oferta_precio_final')
                    if v is None:
                        pvp_widget.setText('')
                    else:
                        pvp_widget.setText(format_decimal_value(float(v), self.decimales_precios, use_comma=True))
                except Exception:
                    pass

            if hasattr(self.ui, 'txtOfertaDtoOferta'):
                try:
                    v = curr.get('oferta_dto_local')
                    self.ui.txtOfertaDtoOferta.setText(str(v) if v is not None else '')
                except Exception:
                    pass

            if hasattr(self.ui, 'txtOferta_dto_web'):
                try:
                    v = curr.get('oferta_dto_web')
                    self.ui.txtOferta_dto_web.setText(str(v) if v is not None else '')
                except Exception:
                    pass

            # Flags
            try:
                if hasattr(self.ui, 'chkOferta_32'):
                    self.ui.chkOferta_32.setChecked(bool(curr.get('oferta_oferta32')))
            except Exception:
                pass
            try:
                if hasattr(self.ui, 'chkOferta_dto'):
                    self.ui.chkOferta_dto.setChecked(bool(curr.get('oferta_oferta_dto')))
            except Exception:
                pass
            try:
                if hasattr(self.ui, 'chkOferta_web'):
                    self.ui.chkOferta_web.setChecked(bool(curr.get('oferta_oferta_web')))
            except Exception:
                pass
        except Exception:
            pass
        # Refresh ofertas table for this article
        try:
            art = self.controller.get_current_article()
            if art and isinstance(art, dict):
                art_id = art.get('id')
                if art_id and hasattr(self.controller, 'repository'):
                    try:
                        offers = self.controller.repository.get_ofertas_for_article(art_id)
                        if hasattr(self, 'ofertas_model'):
                            self.ofertas_model.set_offers(offers)
                    except Exception:
                        # Non-fatal
                        pass
        except Exception:
            pass
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

            # Tipo de artículo (lookup) - include only if present on the loaded article
            if 'id_tipo' in current:
                data['id_tipo'] = current['id_tipo']
            elif 'codigo_tipo' in current:
                data['codigo_tipo'] = current['codigo_tipo']
        
        # TODO: Obtener IDs de familia/subfamilia desde los diálogos de búsqueda
        # TODO: Obtener tipo de IVA desde el combo
        # TODO: Obtener ID del proveedor desde el lookup
        
        # Promotion dates - QDateEdit -> Python date or None
        try:
            # Only include oferta date fields when the article is explicitly marked as
            # promoted or the promotions editor is active — avoid inserting empty oferta rows
            # just because QDateEdit controls contain default dates.
            include_oferta_dates = False
            try:
                if hasattr(self.ui, 'chkArticulo_promocionado') and self.ui.chkArticulo_promocionado.isChecked():
                    include_oferta_dates = True
            except Exception:
                include_oferta_dates = include_oferta_dates

            # Also include dates when we are editing/creating an oferta (explicit user action)
            if getattr(self, '_editing_oferta', False) or getattr(self, '_creating_oferta', False) or getattr(self, '_current_oferta_id', None):
                include_oferta_dates = True

            if include_oferta_dates:
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

        # Ensure we don't persist fields that are not relevant for the current tipo
        try:
            # Prefer transient flags stored on current_article (set at load or selection time)
            tipo_requiereEAN = None
            tipo_proveedor = None
            if current and isinstance(current, dict):
                if 'tipo_requiereEAN' in current:
                    tipo_requiereEAN = bool(current.get('tipo_requiereEAN'))
                if 'tipo_proveedor' in current:
                    tipo_proveedor = bool(current.get('tipo_proveedor'))

                # If flags were not set, try to inspect the tipo record directly
                if (tipo_requiereEAN is None or tipo_proveedor is None) and current.get('id_tipo'):
                    try:
                        t = self.controller.repository.get_articulo_tipo(current.get('id_tipo'))
                        if t:
                            if tipo_requiereEAN is None:
                                tipo_requiereEAN = self._coerce_flag(t.get('requiereEAN'), default=False)
                            if tipo_proveedor is None:
                                tipo_proveedor = self._coerce_flag(t.get('proveedor'), default=False)
                    except Exception:
                        pass

            # If flags are explicitly False, remove related fields from the payload
            if tipo_requiereEAN is False:
                try:
                    if 'codigo_barras' in data:
                        del data['codigo_barras']
                except Exception:
                    pass

            if tipo_proveedor is False:
                try:
                    if 'codigo_fabricante' in data:
                        del data['codigo_fabricante']
                except Exception:
                    pass
        except Exception:
            logging.getLogger(__name__).exception("Error filtering out non-applicable fields before save")

        return data

    def _refresh_ofertas_table(self):
        """Reload offers for the current article into the ofertas model.

        This centralises the refresh logic so multiple handlers can update the table
        immediately after changes (save / undo / add / delete).
        """
        try:
            art = None
            if hasattr(self.controller, 'get_current_article'):
                art = self.controller.get_current_article()

            if art and isinstance(art, dict):
                art_id = art.get('id')
                if art_id and hasattr(self.controller, 'repository'):
                    offers = self.controller.repository.get_ofertas_for_article(art_id)
                    if hasattr(self, 'ofertas_model'):
                        self.ofertas_model.set_offers(offers)
        except Exception:
            # Best-effort - non-fatal
            pass
    
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
        # Clear provider fields - try new names first, then old names
        if hasattr(self.ui, 'txtProveedor'):
            self.ui.txtProveedor.clear()
        elif hasattr(self.ui, 'txtproveedor'):
            self.ui.txtproveedor.clear()
        if hasattr(self.ui, 'txtCodigoProveedor'):
            self.ui.txtCodigoProveedor.clear()
        elif hasattr(self.ui, 'txtcodigo_proveedor'):
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

        # Setup ofertas table model
        try:
            self.ofertas_model = OffersTableModel()
            if hasattr(self.ui, 'tabla_ofertas'):
                self.ui.tabla_ofertas.setModel(self.ofertas_model)
                # Prefer wider first column (~20px wider than before) and center its contents
                try:
                    self.ui.tabla_ofertas.setColumnWidth(0, 56)
                    # Center alignment for first column cells
                    try:
                        header = self.ui.tabla_ofertas.horizontalHeader()
                        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
                    except Exception:
                        pass
                except Exception:
                    pass
                try:
                    # Clicking a row populates the promotion fields (does not enable editing)
                    self.ui.tabla_ofertas.clicked.connect(self._on_tabla_ofertas_clicked)
                except Exception:
                    pass
        except Exception:
            pass
    
    def _load_articles_data(self, filter_text: str = ""):
        """Load articles data into the table with optional filter"""
        try:
            articles = self.controller.filter_articles(filter_text)
            self.articles_model.set_articles(articles)
        except Exception:
            logging.getLogger(__name__).exception("Error loading articles")
    
    def _on_filter_changed(self, text: str):
        """Manejar cambio de filtro - recargar artículos con filtro"""
        self._load_articles_data(text)

    
    def _on_table_double_click(self, index: QModelIndex):
        """Manejar doble clic en la tabla para editar el artículo"""
        if not index.isValid():
            return
        
        article = self.articles_model.get_article(index.row())
        if article:
            # Obtener id de forma segura para evitar avisos estáticos
            try:
                article_id = article.get('id') if isinstance(article, dict) else None
            except Exception:
                article_id = None
            if article_id:
                try:
                    self.controller.load_by_id(article_id)
                except Exception:
                    # Dejar que la carga falle silenciosamente en entornos de prueba
                    pass
            self._load_form_from_article()
            self.ui.stackedWidget.setCurrentIndex(0)  # Show form

    def _on_tabla_ofertas_clicked(self, index: QModelIndex):
        """Populate the promotions form when the user selects a row in tabla_ofertas.

        This does NOT enable editing — the user must press Edit to change values.
        """
        try:
            if not index or not index.isValid():
                return

            if not hasattr(self, 'ofertas_model'):
                return

            # Safely get the offer dict from the model
            offer = None
            try:
                if hasattr(self.ofertas_model, 'get_offer'):
                    offer = self.ofertas_model.get_offer(index.row())
                else:
                    offer = self.ofertas_model.offers[index.row()]
            except Exception:
                offer = None

            if not offer:
                return

            # Keep track of selected oferta id for saves/deletes
            try:
                self._current_oferta_id = offer.get('id')
            except Exception:
                pass

            # Populate UI controls with oferta values
            try:
                if hasattr(self.ui, 'txtOferta_Descripcion_promocion'):
                    self.ui.txtOferta_Descripcion_promocion.setText(str(offer.get('descripcion') or ''))
            except Exception:
                pass

            # Convert python date -> QDate for date fields
            def _pydate_to_qdate(d):
                from core.utils import pydate_to_qdate as _pydate_helper
                return _pydate_helper(d)

            try:
                if hasattr(self.ui, 'txtOferta_Fecha_ini'):
                    self.ui.txtOferta_Fecha_ini.setDate(_pydate_to_qdate(offer.get('fecha_inicio')))
            except Exception:
                pass

            try:
                if hasattr(self.ui, 'txtOferta_Fecha_fin'):
                    self.ui.txtOferta_Fecha_fin.setDate(_pydate_to_qdate(offer.get('fecha_fin')))
            except Exception:
                pass

            # Flags and numeric fields
            try:
                if hasattr(self.ui, 'chkArticulo_promocionado'):
                    self.ui.chkArticulo_promocionado.setChecked(bool(offer.get('activa')))
            except Exception:
                pass

            try:
                if hasattr(self.ui, 'txtOfertaPorCada'):
                    v = offer.get('unidades')
                    if v is None:
                        self.ui.txtOfertaPorCada.setText('')
                    else:
                        self.ui.txtOfertaPorCada.setText(str(int(v)) if float(v).is_integer() else str(v))
            except Exception:
                pass

            try:
                if hasattr(self.ui, 'txtOfertaregaloUnidades'):
                    v = offer.get('regalo')
                    if v is None:
                        self.ui.txtOfertaregaloUnidades.setText('')
                    else:
                        self.ui.txtOfertaregaloUnidades.setText(str(int(v)) if float(v).is_integer() else str(v))
            except Exception:
                pass

            try:
                # canonical pvp fixed-price input
                pvp_widget = getattr(self.ui, 'txtofertaPvpFijo', None)

                if pvp_widget is not None:
                    v = offer.get('precio_final')
                    if v is None:
                        pvp_widget.setText('')
                    else:
                        # precio_final in model is likely oferta_precio_final key; fallback accordingly
                        value = None
                        if 'precio_final' in offer:
                            value = offer.get('precio_final')
                        elif 'oferta_precio_final' in offer:
                            value = offer.get('oferta_precio_final')
                        if value is None:
                            pvp_widget.setText('')
                        else:
                            try:
                                pvp_widget.setText(format_decimal_value(float(value), self.decimales_precios, use_comma=True))
                            except Exception:
                                pvp_widget.setText(str(value))
            except Exception:
                pass

            try:
                if hasattr(self.ui, 'txtOfertaDtoOferta'):
                    v = offer.get('dto_local') or offer.get('oferta_dto')
                    self.ui.txtOfertaDtoOferta.setText(str(v) if v is not None else '')
            except Exception:
                pass

            try:
                if hasattr(self.ui, 'txtOferta_dto_web'):
                    v = offer.get('dto_web') or offer.get('oferta_web')
                    self.ui.txtOferta_dto_web.setText(str(v) if v is not None else '')
            except Exception:
                pass

            try:
                if hasattr(self.ui, 'chkOferta_32'):
                    self.ui.chkOferta_32.setChecked(bool(offer.get('oferta32')))
            except Exception:
                pass

            try:
                if hasattr(self.ui, 'chkOferta_dto'):
                    self.ui.chkOferta_dto.setChecked(bool(offer.get('oferta_dto') or offer.get('oferta_dto')))
            except Exception:
                pass
            try:
                if hasattr(self.ui, 'chkOferta_web'):
                    self.ui.chkOferta_web.setChecked(bool(offer.get('oferta_web')))
            except Exception:
                pass

            # Ensure related fields are enabled/disabled according to the selected oferta type
            try:
                self._sync_oferta_type_fields()
            except Exception:
                pass

        except Exception:
            # Selection handling should never break the main UI
            return
    
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
            self._maybe_warn("Error", "No se pudo crear el artículo")
    
    def _on_edit_clicked(self):
        """Manejar click en el botón Editar"""
        # If we're already in form view with an article loaded, just unlock
        if self.controller.get_current_article() and self.ui.stackedWidget.currentIndex() == 0:
            self._lock_fields(False)
            return
        
        # Otherwise, get the selected article from the table
        selection = self.ui.tablaBusqueda.selectionModel()
        if not selection or not selection.hasSelection():
            from core.ui_helpers import show_info
            show_info(self, self.tr("Editar"), self.tr("Por favor, selecciona un artículo de la lista"))
            return
        
        index = selection.currentIndex()
        if not index.isValid():
            return
        
        article = self.articles_model.get_article(index.row())
        if article:
            # Obtener id de forma segura para evitar avisos estáticos
            try:
                article_id = article.get('id') if isinstance(article, dict) else None
            except Exception:
                article_id = None
            if article_id:
                try:
                    self.controller.load_by_id(article_id)
                except Exception:
                    # Dejar que la carga falle silenciosamente en entornos de prueba
                    pass
            self._load_form_from_article()
            self._lock_fields(False)
            # Switch to edit tab
            self.ui.stackedWidget.setCurrentIndex(0)


    
    def _on_save_clicked(self):
        """Manejar click en el botón Guardar"""
        form_data = self._save_form_to_article()
        success, message = self.controller.save(form_data)
        
        if success:
            from core.ui_helpers import show_info
            show_info(self, self.tr("Guardar"), message)
            self._load_form_from_article()
            self._lock_fields(True)
        else:
            self._maybe_warn("Error", message)
    
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
        from core.ui_helpers import show_question
        reply = show_question(
            self,
            self.tr("Borrar Artículo"),
            self.tr("¿Desea realmente borrar este artículo?\nEsta opción no se puede deshacer"),
            QMessageBox.StandardButton.No | QMessageBox.StandardButton.Yes,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            success, message = self.controller.delete()
            if success:
                from core.ui_helpers import show_info
                show_info(self, self.tr("Borrar"), message)
                self._load_form_from_article()
            else:
                self._maybe_warn("Error", message)
    
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

    def _on_codigo_tipo_entered(self):
        """Handler: cuando el usuario termina de editar txtCodigoTipo intentar buscar el tipo por código."""
        try:
            if not hasattr(self.ui, 'txtCodigoTipo'):
                return
            code = (self.ui.txtCodigoTipo.text() or '').strip()
            if not code:
                # Clear description when code is empty
                if hasattr(self.ui, 'txtDescripcionTipo'):
                    self.ui.txtDescripcionTipo.clear()
                # Remove stored type in controller current article
                cur = self.controller.get_current_article()
                if cur and 'id_tipo' in cur:
                    cur.pop('id_tipo', None)
                    cur.pop('codigo_tipo', None)
                    cur.pop('descripcion_tipo', None)
                return

            tipo = None
            try:
                tipo = self.controller.get_tipo_by_codigo(code)
            except Exception:
                tipo = None

            if tipo:
                # Populate UI and set in current article transiently
                if hasattr(self.ui, 'txtCodigoTipo'):
                    self.ui.txtCodigoTipo.setText(str(tipo.get('codigo') or ''))
                if hasattr(self.ui, 'txtDescripcionTipo'):
                    self.ui.txtDescripcionTipo.setText(str(tipo.get('descripcion') or ''))

                # update controller state for save to pick up if necessary
                try:
                    self.controller.set_tipo_from_lookup(tipo.get('id'), tipo.get('codigo'), tipo.get('descripcion'))
                except Exception:
                    pass
                # Apply UI visibility rules according to the tipo flags (if available)
                try:
                    # Use the 'tipo' variable returned by the repository/ controller
                    requiere_ean = self._coerce_flag(tipo.get('requiereEAN'), default=False)
                    proveedor_flag = self._coerce_flag(tipo.get('proveedor'), default=False)
                    try:
                        logging.getLogger(__name__).info(
                            "[ARTICULO-TIPO] id_tipo=%s raw_requiere=%s coerced_requiere=%s raw_proveedor=%s coerced_proveedor=%s",
                            tipo.get('id'), tipo.get('requiereEAN'), requiere_ean, tipo.get('proveedor'), proveedor_flag
                        )
                    except Exception:
                        pass
                    self._apply_tipo_flags_to_ui(requiere_ean, proveedor_flag)
                except Exception:
                    pass
            else:
                # No match found — clear description and warn user
                if hasattr(self.ui, 'txtDescripcionTipo'):
                    self.ui.txtDescripcionTipo.clear()
                # clear tipo-based UI visibility
                try:
                    if self.controller.current_article is not None:
                        self.controller.current_article.pop('tipo_requiereEAN', None)
                        self.controller.current_article.pop('tipo_proveedor', None)
                except Exception:
                    pass
                self._apply_tipo_flags_to_ui(False, False)
                self._maybe_warn(self.tr("Tipo no encontrado"), self.tr("No se encontró ningún tipo con ese código"))
        except Exception:
            # Don't crash UI on lookup errors
            logging.getLogger(__name__).exception("Error buscando tipo por código")
    
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
        # Avoid creating chart objects in headless/test environments which can
        # trigger native aborts on some Qt builds. If there is no primary screen
        # accessible, skip full chart initialization.
        try:
            import os
            from PySide6.QtGui import QGuiApplication
            platform = os.environ.get('QT_QPA_PLATFORM', '').lower()
            if platform in ('offscreen', 'minimal') or QGuiApplication.primaryScreen() is None:
                return
        except Exception:
            # If we cannot determine screen availability, skip chart setup
            return

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
        
        return data, self.tr("Importes de Ventas (€)")
    
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
                from core.ui_helpers import show_info
                show_info(self, self.tr("Info"), self.tr("No se encontraron secciones en la base de datos"))
                return
            
            # Use DBConsultaView.select_from_data - no QSqlDatabase needed!
            selected_data, record = DBConsultaView.select_from_data(
                parent=self,
                data=secciones_data,
                headers=[self.tr("ID"), self.tr("Código"), self.tr("Sección")],
                campos=["codigo", "seccion"],
                titulo=self.tr("Seleccionar Sección")
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

                    logging.getLogger(__name__).info(f"✅ Sección seleccionada: {seccion_codigo} - {seccion_nombre}")
                else:
                    self._maybe_warn(self.tr("Error"), self.tr("No se pudo actualizar la sección"))
        
        except Exception as e:
            logging.getLogger(__name__).exception("Error opening section lookup")
            from core.ui_helpers import show_critical
            show_critical(self, self.tr("Error"), self.tr("Error al abrir consulta de secciones: {}").format(str(e)))

    def _on_buscar_familia_clicked(self):
        """Abrir diálogo de búsqueda de familias y actualizar controller/modelo/vista (MVC)."""
        try:
            # Families depend on section; obtain current article's section and filter families
            current = self.controller.get_current_article() or {}
            id_seccion = current.get('id_seccion')
            if not id_seccion:
                from core.ui_helpers import show_info
                show_info(self, self.tr("Info"), self.tr("Seleccione primero una sección para listar las familias correspondientes"))
                return

            familias_data = self.controller.get_familias_data(id_seccion)

            if not familias_data:
                from core.ui_helpers import show_info
                show_info(self, self.tr("Info"), self.tr("No se encontraron familias en la base de datos"))
                return

            selected_data, record = DBConsultaView.select_from_data(
                parent=self,
                data=familias_data,
                headers=[self.tr("ID"), self.tr("Código"), self.tr("Familia")],
                campos=["codigo", "familia"],
                titulo=self.tr("Seleccionar Familia")
            )

            if selected_data:
                familia_id = selected_data.get('id')
                familia_codigo = selected_data.get('codigo')
                familia_nombre = selected_data.get('familia')

                # Delegate state change to controller (MVC)
                if self.controller.set_familia_from_lookup(familia_id, familia_codigo, familia_nombre):
                    self.ui.txtfamilia.setText(familia_nombre)
                    logging.getLogger(__name__).info(f"✅ Familia seleccionada: {familia_codigo} - {familia_nombre}")

                    # Si estamos en modo edición, habilitar subfamilia (ahora que hay familia)
                    locked = self.ui.botGuardar.isEnabled() == False
                    # locked True means fields are read-only; we want enabled when not locked
                    if hasattr(self.ui, 'botBuscarSubfamilia') and not locked:
                        self.ui.botBuscarSubfamilia.setEnabled(True)
                    # Clear subfamily UI because a family change invalidates previous subfamily
                    if hasattr(self.ui, 'txtsubfamilia'):
                        self.ui.txtsubfamilia.clear()
                else:
                    self._maybe_warn(self.tr("Error"), self.tr("No se pudo actualizar la familia"))

        except Exception as e:
            logging.getLogger(__name__).exception("Error opening family lookup")
            from core.ui_helpers import show_critical
            show_critical(self, self.tr("Error"), self.tr("Error al abrir consulta de familias: {}").format(str(e)))

    def _on_buscar_subfamilia_clicked(self):
        """Abrir diálogo de búsqueda de subfamilias y actualizar controller/modelo/vista (MVC)."""
        try:
            # Si hay familia seleccionada, filtramos subfamilias por esa familia
            current = self.controller.get_current_article() or {}
            id_familia = current.get('id_familia')

            # Si no hay familia seleccionada, mostrar hint y no abrir diálogo
            if not id_familia:
                # Mostrar mensaje orientativo al usuario
                from core.ui_helpers import show_info
                show_info(
                    self,
                    self.tr("Info"),
                    self.tr("Antes de buscar subfamilias, seleccione primero una familia.")
                )

                # Añadir tooltip informativo al botón para UX
                if hasattr(self.ui, 'botBuscarSubfamilia'):
                    self.ui.botBuscarSubfamilia.setToolTip(self.tr("Seleccione una familia antes de buscar subfamilias"))

                return

            subfamilias_data = self.controller.get_subfamilias_data(id_familia)

            if not subfamilias_data:
                from core.ui_helpers import show_info
                show_info(self, self.tr("Info"), self.tr("No se encontraron subfamilias en la base de datos"))
                return

            selected_data, record = DBConsultaView.select_from_data(
                parent=self,
                data=subfamilias_data,
                headers=[self.tr("ID"), self.tr("Código"), self.tr("Subfamilia")],
                campos=["codigo", "subfamilia"],
                titulo=self.tr("Seleccionar Subfamilia")
            )

            if selected_data:
                sub_id = selected_data.get('id')
                sub_codigo = selected_data.get('codigo')
                sub_nombre = selected_data.get('subfamilia')

                if self.controller.set_subfamilia_from_lookup(sub_id, sub_codigo, sub_nombre):
                    self.ui.txtsubfamilia.setText(sub_nombre)
                    logging.getLogger(__name__).info(f"✅ Subfamilia seleccionada: {sub_codigo} - {sub_nombre}")
                else:
                    self._maybe_warn("Error", "No se pudo actualizar la subfamilia")

        except Exception as e:
            logging.getLogger(__name__).exception("Error opening subfamily lookup")
            from core.ui_helpers import show_critical
            show_critical(self, self.tr("Error"), self.tr("Error al abrir consulta de subfamilias: {}").format(str(e)))

    def _on_buscar_tipo_clicked(self):
        """Abrir diálogo de búsqueda de Tipos de Artículo (articulo_tipo).

        Solo cuando estamos en modo edición (botGuardar habilitado).
        """
        import time
        import traceback
        
        # Log every invocation with stack trace
        stack = ''.join(traceback.format_stack()[-4:-1])
        logging.getLogger(__name__).warning(f"_on_buscar_tipo_clicked CALLED at {time.time():.3f}\nStack:\n{stack}")
        
        # Deduplicate within a short window (protects across multiple event sources)
        try:
            now = time.time()
            if getattr(self, '_last_tipo_lookup_time', 0) and (now - self._last_tipo_lookup_time) < 0.7:
                logging.getLogger(__name__).warning(f"BLOCKED by timestamp guard: last={self._last_tipo_lookup_time:.3f}, now={now:.3f}, diff={now - self._last_tipo_lookup_time:.3f}")
                return
            self._last_tipo_lookup_time = now
        except Exception as e:
            # if time is unavailable, continue but rely on other guards
            logging.getLogger(__name__).exception(f"Timestamp guard failed: {e}")
            pass
        
        # Prevent duplicate/opening re-entrancy
        if getattr(self, '_tipo_lookup_running', False):
            logging.getLogger(__name__).warning("BLOCKED by _tipo_lookup_running guard")
            return

        try:
            self._tipo_lookup_running = True
            editing = False
            if hasattr(self.ui, 'botGuardar'):
                try:
                    editing = self.ui.botGuardar.isEnabled()
                except Exception:
                    editing = False

            if not editing:
                return

            tipos = self.controller.get_tipos_data() or []
            if not tipos:
                from core.ui_helpers import show_info
                show_info(self, self.tr("Info"), self.tr("No se encontraron tipos de artículo"))
                return

            selected, record = DBConsultaView.select_from_data(
                parent=self,
                data=tipos,
                headers=[self.tr("ID"), self.tr("Código"), self.tr("Descripción")],
                campos=["codigo", "descripcion"],
                titulo=self.tr("Seleccionar Tipo de Artículo")
            )

            if selected:
                tipo_id = selected.get('id')
                codigo = selected.get('codigo')
                descripcion = selected.get('descripcion')

                ok = self.controller.set_tipo_from_lookup(tipo_id, codigo, descripcion)
                if ok:
                    if hasattr(self.ui, 'txtCodigoTipo'):
                        self.ui.txtCodigoTipo.setText(str(codigo or ''))
                    if hasattr(self.ui, 'txtDescripcionTipo'):
                        self.ui.txtDescripcionTipo.setText(str(descripcion or ''))
                    logging.getLogger(__name__).info(f"✅ Tipo seleccionado: {codigo} - {descripcion}")
                    # read flags from selected data (if present) and apply visibility
                    try:
                        requiere_ean = self._coerce_flag(selected.get('requiereEAN'), default=False)
                        proveedor_flag = self._coerce_flag(selected.get('proveedor'), default=False)
                        # store transient flags on current_article for later
                        if self.controller.current_article is not None:
                            self.controller.current_article['tipo_requiereEAN'] = requiere_ean
                            self.controller.current_article['tipo_proveedor'] = proveedor_flag
                        try:
                            logging.getLogger(__name__).info(
                                "[SELECT-TIPO] selected_id=%s raw_requiere=%s coerced_requiere=%s raw_proveedor=%s coerced_proveedor=%s",
                                tipo_id, selected.get('requiereEAN'), requiere_ean, selected.get('proveedor'), proveedor_flag
                            )
                        except Exception:
                            pass
                        self._apply_tipo_flags_to_ui(requiere_ean, proveedor_flag)
                    except Exception:
                        pass
                else:
                    self._maybe_warn(self.tr("Error"), self.tr("No se pudo asignar el tipo seleccionado"))

        except Exception:
            logging.getLogger(__name__).exception("Error opening tipo lookup")
            from core.ui_helpers import show_critical
            show_critical(self, self.tr("Error"), self.tr("Error al abrir consulta de tipos: {}"))
        finally:
            # Ensure the guard is always cleared
            try:
                self._tipo_lookup_running = False
            except Exception:
                pass
    
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
            # Primary action buttons inside the promotions frame
            if hasattr(self.ui, 'btnguardar_oferta'):
                self.ui.btnguardar_oferta.setEnabled(enable)

            if hasattr(self.ui, 'btnDeshacerOferta'):
                self.ui.btnDeshacerOferta.setEnabled(enable)

            # Decide whether the article itself is in edit mode and whether promotions tab is active
            promo_tab_active = False
            try:
                if hasattr(self.ui, 'Pestanas') and self.ui.Pestanas.currentWidget() is not None:
                    promo_tab_active = (self.ui.Pestanas.currentWidget().objectName() == 'tab_promociones')
            except Exception:
                promo_tab_active = False

            article_editing = False
            try:
                article_editing = bool(self.ui.botGuardar.isEnabled())
            except Exception:
                article_editing = False

            # Toggle the add/edit offer buttons: enabled only when NOT editing an oferta and
            # the article is in edit mode and the promotions tab is active
            add_edit_enabled = (not enable) and article_editing and promo_tab_active
            if hasattr(self.ui, 'btnAnadirOferta'):
                self.ui.btnAnadirOferta.setEnabled(add_edit_enabled)
            if hasattr(self.ui, 'btnEditarOferta'):
                self.ui.btnEditarOferta.setEnabled(add_edit_enabled)
            if hasattr(self.ui, 'btnEditartarifa'):
                self.ui.btnEditartarifa.setEnabled(add_edit_enabled)

            # Enable/disable common promotion input widgets in one pass
            from PySide6.QtWidgets import QLineEdit, QDateEdit, QCheckBox, QRadioButton, QComboBox, QDoubleSpinBox, QTextEdit

            frame = getattr(self.ui, 'framePromocion', None)
            tab = getattr(self.ui, 'tab_promociones', None)

            target_widgets = []
            classes = (QLineEdit, QDateEdit, QCheckBox, QRadioButton, QComboBox, QDoubleSpinBox, QTextEdit)
            if frame is not None:
                for cls in classes:
                    try:
                        target_widgets.extend(frame.findChildren(cls))
                    except Exception:
                        pass
            if tab is not None:
                for cls in classes:
                    try:
                        target_widgets.extend(tab.findChildren(cls))
                    except Exception:
                        pass

            # Toggle known sub-frames too (some elements live inside these frame containers)
            for fname in ('frame_pvp_fijo', 'frame_tipo_32', 'frame_dto', 'frame_ofertaweb', 'frame_comentarios'):
                frm = getattr(self.ui, fname, None)
                if frm is not None:
                    try:
                        frm.setEnabled(enable)
                    except Exception:
                        pass

            for w in target_widgets:
                try:
                    w.setEnabled(enable)
                except Exception:
                    try:
                        # Some widgets don't support setEnabled in a uniform way; try readOnly
                        w.setReadOnly(not enable)
                    except Exception:
                        pass

            # Ensure activation / delete buttons on the promotions table are toggled
            try:
                if hasattr(self.ui, 'btnActivarOferta'):
                    self.ui.btnActivarOferta.setEnabled(enable)
                    try:
                        # Connect activation toggle handler once (test-friendly via core.ui_helpers)
                        if not getattr(self.ui.btnActivarOferta, '_toggle_connected', False):
                            self.ui.btnActivarOferta.clicked.connect(self._on_toggle_oferta_activa)
                            setattr(self.ui.btnActivarOferta, '_toggle_connected', True)
                    except Exception:
                        pass
            except Exception:
                pass
            try:
                # UI generator uses 'btnBorrar_oferta' for the delete button
                if hasattr(self.ui, 'btnBorrar_oferta'):
                    self.ui.btnBorrar_oferta.setEnabled(enable)
                    try:
                        if not getattr(self.ui.btnBorrar_oferta, '_delete_connected', False):
                            self.ui.btnBorrar_oferta.clicked.connect(self._on_borrar_oferta)
                            setattr(self.ui.btnBorrar_oferta, '_delete_connected', True)
                    except Exception:
                        pass
            except Exception:
                pass

            # Master promotion checkbox: should be enabled when the article is in edit mode
            try:
                if hasattr(self.ui, 'chkArticulo_promocionado'):
                    self.ui.chkArticulo_promocionado.setEnabled(article_editing)
            except Exception:
                pass

            # Give focus to description field if enabling
            if enable:
                try:
                    if hasattr(self.ui, 'txtOferta_Descripcion_promocion'):
                        self.ui.txtOferta_Descripcion_promocion.setFocus()
                except Exception:
                    pass

        except Exception:
            # Any unexpected error toggling edit state should not crash the UI
            pass

        # Keep oferta-type dependent fields in sync when toggling types
        try:
            self._sync_oferta_type_fields()
        except Exception:
            pass

    def _sync_oferta_type_fields(self):
        """Enable/disable oferta fields based on the currently selected oferta type.

        Behavior:
        - If chkOferta_32 is selected: enable txtOferta_por_cada and txtOfertaregalo_de; disable txtOfertaDtoOferta, txtOferta_dto_web and txtoferta_pvp_fijo.
        - If chkOferta_dto selected: enable txtOfertaDtoOferta only.
        - If chkOferta_web selected: enable txtOferta_dto_web only.
        - If chkOferta_pvp selected: enable txtoferta_pvp_fijo only.
        - If none selected, disable all specialty oferta fields.
        """
        try:
            # Determine which (if any) radio is selected
            is_32 = getattr(self.ui, 'chkOferta_32', None) and bool(self.ui.chkOferta_32.isChecked())
            is_dto = getattr(self.ui, 'chkOferta_dto', None) and bool(self.ui.chkOferta_dto.isChecked())
            is_web = getattr(self.ui, 'chkOferta_web', None) and bool(self.ui.chkOferta_web.isChecked())
            # Use the normalized PVP radio name from the generated UI
            is_pvp = getattr(self.ui, 'chkOfertaPvp', None) and bool(self.ui.chkOfertaPvp.isChecked())

            # Helper to toggle a widget if it exists. Support multiple naming variants
            def set_enabled(names, value):
                if isinstance(names, str):
                    names = [names]
                for name in names:
                    if hasattr(self.ui, name):
                        try:
                            getattr(self.ui, name).setEnabled(value)
                        except Exception:
                            try:
                                getattr(self.ui, name).setReadOnly(not value)
                            except Exception:
                                pass

            # 3x2 -> enable por cada & ofertaregalo; use canonical names from UI
            set_enabled(['txtOfertaPorCada'], bool(is_32))
            set_enabled(['txtOfertaregaloUnidades'], bool(is_32))

            # DTO local -> enable DTO local field; disable web, pvp, 3x2 fields
            set_enabled(['txtOfertaDtoOferta'], bool(is_dto))

            # DTO web -> enable web DTO only (canonical name as generated)
            set_enabled('txtOferta_dto_web', bool(is_web))

            # precio fijo -> enable the canonical fixed-price input only
            set_enabled('txtofertaPvpFijo', bool(is_pvp))

            # Make sure all the mutually exclusive fields are disabled when not selected
            # Disable counterparts for each type (explicitly set False for clarity)
            if is_32:
                set_enabled(['txtOfertaDtoOferta', 'txtOferta_dto_web', 'txtofertaPvpFijo'], False)
            elif is_dto:
                set_enabled(['txtOferta_dto_web', 'txtofertaPvpFijo', 'txtOfertaPorCada', 'txtOfertaregaloUnidades'], False)
            elif is_web:
                # web mode disables DTO local, pvp and 3x2 fields
                set_enabled(['txtOfertaDtoOferta', 'txtofertaPvpFijo', 'txtOfertaPorCada', 'txtOfertaregaloUnidades'], False)
            elif is_pvp:
                # pvp mode: ensure pvp fields are left enabled and other special fields are disabled
                set_enabled(['txtOfertaPorCada', 'txtOfertaregaloUnidades', 'txtOfertaDtoOferta', 'txtOferta_dto_web'], False)
            else:
                # None selected -> disable all special offer fields
                set_enabled(['txtOfertaPorCada', 'txtOfertaregaloUnidades', 'txtOfertaDtoOferta', 'txtOferta_dto_web', 'txtofertaPvpFijo'], False)

        except Exception:
            # Keep silent on any error – this code is best-effort UI sync
            pass

    def _on_add_oferta(self):
        """User clicked 'Añadir oferta' — enter oferta edit mode (new oferta).

        Enable save/undo and disable add/edit controls until saved or undone.
        """
        self._editing_oferta = True
        self._creating_oferta = False

        # Clear oferta form fields and enable editing
        try:
            if hasattr(self.ui, 'txtOferta_Descripcion_promocion'):
                self.ui.txtOferta_Descripcion_promocion.clear()
        except Exception:
            pass

        # Do NOT create a DB row immediately. Enter editing state and allow
        # the user to fill the form and press Guardar to persist the oferta.
        # This prevents transient/accidental DB rows when users only open the
        # add form and then cancel.
        self._creating_oferta = True
        # clear any previously selected oferta id (we haven't created it yet)
        self._current_oferta_id = None

        self._enable_oferta_editing(True)

    def _on_edit_oferta(self):
        """User clicked 'Editar oferta' — enable editing existing oferta."""
        self._editing_oferta = True
        self._enable_oferta_editing(True)

    # NOTE: _on_save_oferta logic has been consolidated further down; earlier
    # definitions were removed to avoid duplicated handlers.

    # NOTE: The undo/save handlers were consolidated later in the file. Removed
    # duplicate implementation earlier in the source.


    def _on_save_oferta(self):
        """User clicked 'Guardar oferta' — perform basic save workflow and exit edit mode.

        Note: detailed persistence is handled when the article is saved via self._on_save_clicked
        — this handler toggles UI state only.
        """
        # Gather oferta payload from UI and persist using controller
        # enter save handler
        payload = {}
        # Ensure we always have these variables defined for the remainder of the handler
        success = False
        message = None
        try:
            # Description
            if hasattr(self.ui, 'txtOferta_Descripcion_promocion'):
                try:
                    payload['descripcion'] = self.ui.txtOferta_Descripcion_promocion.text() or None
                except Exception:
                    pass

            # Dates
            try:
                if hasattr(self.ui, 'txtOferta_Fecha_ini'):
                    d1 = self.ui.txtOferta_Fecha_ini.date()
                    dt = qdate_to_date(d1) if d1 is not None else None
                    payload['fecha_inicio'] = dt
            except Exception:
                pass

            try:
                if hasattr(self.ui, 'txtOferta_Fecha_fin'):
                    d2 = self.ui.txtOferta_Fecha_fin.date()
                    dt2 = qdate_to_date(d2) if d2 is not None else None
                    payload['fecha_fin'] = dt2
            except Exception:
                pass

            # Activa flag - use article-level checkbox if present
            try:
                if hasattr(self.ui, 'chkArticulo_promocionado'):
                    payload['activa'] = bool(self.ui.chkArticulo_promocionado.isChecked())
            except Exception:
                pass

            # Offer type flags
            try:
                if hasattr(self.ui, 'chkOferta_32'):
                    payload['oferta32'] = bool(getattr(self.ui, 'chkOferta_32').isChecked())
            except Exception:
                pass
            try:
                if hasattr(self.ui, 'chkOferta_dto'):
                    payload['oferta_dto'] = bool(getattr(self.ui, 'chkOferta_dto').isChecked())
            except Exception:
                pass
            try:
                if hasattr(self.ui, 'chkOferta_web'):
                    payload['oferta_web'] = bool(getattr(self.ui, 'chkOferta_web').isChecked())
            except Exception:
                pass

            # Numeric mappings (UI -> DB)
            try:
                # unidades
                if hasattr(self.ui, 'txtOfertaPorCada'):
                    v = self.ui.txtOfertaPorCada.text().strip()
                else:
                    v = ''
                if v != '':
                    payload['unidades'] = float(parse_decimal_input(v))
            except Exception:
                pass

            try:
                # regalo unidades
                if hasattr(self.ui, 'txtOfertaregaloUnidades'):
                    v = self.ui.txtOfertaregaloUnidades.text().strip()
                else:
                    v = ''
                if v != '':
                    payload['regalo'] = float(parse_decimal_input(v))
            except Exception:
                pass

            try:
                # canonical fixed-price input name
                pvp_widget = getattr(self.ui, 'txtofertaPvpFijo', None)
                if pvp_widget is not None:
                    v = pvp_widget.text().strip()
                    if v != '':
                        payload['precio_final'] = float(parse_decimal_input(v))
                        payload['oferta_precio_final'] = True
            except Exception:
                pass

            try:
                if hasattr(self.ui, 'txtOfertaDtoOferta'):
                    v = self.ui.txtOfertaDtoOferta.text().strip()
                    if v != '':
                        payload['dto_local'] = float(parse_decimal_input(v))
                        if 'oferta_dto' not in payload:
                            payload['oferta_dto'] = True
            except Exception:
                pass

            try:
                if hasattr(self.ui, 'txtOferta_dto_web'):
                    v = self.ui.txtOferta_dto_web.text().strip()
                    if v != '':
                        payload['dto_web'] = float(parse_decimal_input(v))
                        if 'oferta_web' not in payload:
                            payload['oferta_web'] = True
            except Exception:
                pass

            # Attempt to persist via controller
            if hasattr(self, 'controller') and hasattr(self.controller, 'save_oferta'):
                try:
                    # Initialize defaults
                    success = False
                    message = None

                    # If we are in the Add flow (creating an oferta) and the oferta has not
                    # yet been persisted to the DB, call controller.insert_oferta to create
                    # the row. Otherwise call save_oferta which will update existing oferta.
                    if getattr(self, '_current_oferta_id', None) is None:
                        # We are adding a new oferta
                        res = self.controller.insert_oferta(payload)
                        # res may be tuple(success, message, row) or other shape depending on controller
                        if isinstance(res, (list, tuple)):
                            try:
                                it = iter(res)
                                success = None
                                message = None
                                row = None
                                try:
                                    success = next(it)
                                except StopIteration:
                                    success = False
                                try:
                                    message = next(it)
                                except StopIteration:
                                    message = None
                                try:
                                    row = next(it)
                                except StopIteration:
                                    row = None

                                if success and row and isinstance(row, dict) and 'id' in row:
                                    self._current_oferta_id = row['id']
                            except Exception:
                                # mantener defaults si res no cumple el shape esperado
                                pass
                        else:
                            # Best-effort: if controller returned a simple (ok, msg)
                            try:
                                if isinstance(res, tuple) and len(res) == 2:
                                    success, message = res
                            except Exception:
                                pass
                    else:
                        # We are editing an existing oferta
                        payload['id'] = self._current_oferta_id
                        try:
                            success, message = self.controller.save_oferta(payload)
                        except Exception:
                            # Some controllers may return non-tuple or raise; keep defaults
                            success = False
                            message = None
                except Exception as e:
                    # Capture exception and report it in message
                    success = False
                    try:
                        message = str(e)
                    except Exception:
                        message = None

            if success:
                # Inform the user only if there was a message to show
                if message:
                    from core.ui_helpers import show_info
                    show_info(self, self.tr("Guardar oferta"), message)
            else:
                self._maybe_warn("Error", message)
        except Exception:
            # Ensure we reset editing state even on unexpected exceptions
            self._editing_oferta = False
            self._enable_oferta_editing(False)

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
                        desc = current.get('oferta_descripcion', None)
                        if desc is None:
                            desc = current.get('descripcion', '')
                        self.ui.txtOferta_Descripcion_promocion.setText(str(desc or ''))
                    except Exception:
                        pass
        except Exception:
            pass

        # If we created a new oferta in DB during Add/save and then undo, remove it
        try:
            # Only delete when we actually created a DB row (created_db_row True)
            if getattr(self, '_created_db_row', False) and getattr(self, '_current_oferta_id', None):
                if hasattr(self, 'controller') and hasattr(self.controller, 'delete_oferta'):
                    # controller.delete_oferta prefers deleting by oferta_id when present
                    try:
                        self.controller.delete_oferta()
                    except Exception:
                        # Best-effort: attempt repository deletion by id if provided
                        try:
                            if hasattr(self, 'controller') and hasattr(self.controller, 'repository'):
                                self.controller.repository.delete_oferta_by_id(self._current_oferta_id)
                        except Exception:
                            pass
                # Clear flags
                self._created_db_row = False
                self._current_oferta_id = None
            # If we were in add flow but never persisted, just clear the creating flag
            elif getattr(self, '_creating_oferta', False):
                self._creating_oferta = False
        except Exception:
            pass

        # Exit editing
        self._editing_oferta = False
        self._enable_oferta_editing(False)

        # Refresh offers table so that any created-then-undo'd record disappears from the UI
        try:
            self._refresh_ofertas_table()
        except Exception:
            pass

    def _on_toggle_oferta_activa(self):
        """Handle btnActivarOferta — confirm with the user then toggle oferta.activa."""
        try:
            from PySide6.QtWidgets import QMessageBox
            from core.ui_helpers import show_question, show_info, show_critical

            # Determine which oferta is selected
            oferta_id = getattr(self, '_current_oferta_id', None)
            if not oferta_id:
                # No selection — ask user to pick an oferta from the table
                try:
                    show_info(self, self.tr("Activar"), self.tr("Por favor, selecciona una oferta de la lista"))
                except Exception:
                    pass
                return

            # Try to obtain the current oferta dict from the model first (best-effort), then fall back to repository
            current = None
            try:
                if hasattr(self, 'ofertas_model') and getattr(self, 'ofertas_model') is not None:
                    for of in getattr(self.ofertas_model, 'offers', []):
                        if of and isinstance(of, dict) and of.get('id') == oferta_id:
                            current = of
                            break
            except Exception:
                current = None

            try:
                if current is None and hasattr(self, 'controller') and getattr(self.controller, 'repository', None):
                    try:
                        current = self.controller.repository.get_oferta_by_id(oferta_id)
                    except Exception:
                        current = None
            except Exception:
                current = None

            if current is None:
                try:
                    show_critical(self, self.tr("Activar"), self.tr("No se pudo localizar la oferta seleccionada"))
                except Exception:
                    pass
                return

            current_state = bool(current.get('activa'))

            # Show confirmation dialog
            reply = show_question(
                self,
                self.tr("Cambiar estado de oferta"),
                self.tr("¿Desea cambiar estado de oferta?"),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                # default to No so destructive actions require explicit confirmation in UI
                QMessageBox.StandardButton.No,
            )

            if reply != QMessageBox.StandardButton.Yes:
                # canceled
                return

            # Toggle value
            payload = {'id': oferta_id, 'activa': (not current_state)}
            try:
                ok, msg = self.controller.save_oferta(payload)
            except Exception as e:
                ok = False
                msg = str(e)

            if not ok:
                try:
                    self._maybe_warn(self.tr("Error"), self.tr("Ocurrió un error al modificar la oferta activa:%1").format(str(msg)))
                except Exception:
                    pass
                return

            # Refresh UI, keep selection and reflect checkbox state
            try:
                self._refresh_ofertas_table()
            except Exception:
                pass

            try:
                # Update currently loaded article / oferta flags
                # controller.save_oferta refreshes controller.current_article, but ensure checkbox is synced
                if hasattr(self.ui, 'chkArticulo_promocionado'):
                    try:
                        self.ui.chkArticulo_promocionado.setChecked(not current_state)
                    except Exception:
                        pass
            except Exception:
                pass

        except Exception:
            # Don't allow activation flow to crash the UI
            return

    def _on_borrar_oferta(self):
        """Handler for delete oferta button: ask confirmation and delete the selected oferta."""
        try:
            from core.ui_helpers import show_question, show_info, show_critical
            from PySide6.QtWidgets import QMessageBox

            oferta_id = getattr(self, '_current_oferta_id', None)
            if not oferta_id:
                try:
                    show_info(self, self.tr("Borrar Oferta"), self.tr("Por favor, selecciona una oferta de la lista para borrar"))
                except Exception:
                    pass
                return

            reply = show_question(
                self,
                self.tr("Borrar Oferta"),
                self.tr("¿Desea borrar la oferta seleccionada?"),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )

            if reply != QMessageBox.StandardButton.Yes:
                return

            # Attempt deletion
            deleted = False
            try:
                # Prefer controller.delete_oferta when the controller's current article points to same oferta
                current = None
                try:
                    current = self.controller.get_current_article()
                except Exception:
                    current = None

                if current and current.get('oferta_id') == oferta_id:
                    ok, msg = self.controller.delete_oferta()
                    deleted = ok
                else:
                    # Fall back to repository-level deletion by primary key
                    if hasattr(self.controller, 'repository') and getattr(self.controller, 'repository'):
                        deleted = self.controller.repository.delete_oferta_by_id(oferta_id)
            except Exception:
                deleted = False

            if not deleted:
                try:
                    show_critical(self, self.tr("Error"), self.tr("Ocurrió un error al borrar la oferta"))
                except Exception:
                    pass
                return

            # Refresh UI and clear selection
            try:
                try:
                    art = self.controller.get_current_article()
                    if art and isinstance(art, dict) and art.get('id'):
                        self.controller.load_by_id(art.get('id'))
                except Exception:
                    pass

                try:
                    self._refresh_ofertas_table()
                except Exception:
                    pass

                try:
                    self._current_oferta_id = None
                    if hasattr(self.ui, 'txtOferta_Descripcion_promocion'):
                        self.ui.txtOferta_Descripcion_promocion.clear()
                except Exception:
                    pass

                try:
                    show_info(self, self.tr("Borrar Oferta"), self.tr("Oferta borrada correctamente"))
                except Exception:
                    pass
            except Exception:
                pass

        except Exception:
            return


class OffersTableModel(QAbstractTableModel):
    """Model for `tabla_ofertas` — two columns: active indicator and description."""

    def __init__(self):
        super().__init__()
        self.offers = []
        self.headers = ["Activo", "Descripción"]
        # Rows which should be displayed in a highlighted state for a short time
        # mapping oferta_id -> current opacity (float 0.0..1.0) used to paint background
        self._highlighted_ids = {}
        # active animations (keep references so they don't get GC'd)
        self._active_animations = {}

    def set_offers(self, offers: list):
        self.beginResetModel()
        self.offers = offers or []
        self.endResetModel()

    def highlight_row_by_id(self, oferta_id, duration_ms=2000):
        """Highlight a row (by oferta id) for a given duration (ms).

        The highlight is implemented by storing the id in _highlighted_ids and
        emitting dataChanged for the row so views will update the BackgroundRole.
        """
        if not oferta_id:
            return

        # find the row index
        row_idx = None
        for i, of in enumerate(self.offers):
            try:
                if of and isinstance(of, dict) and of.get('id') == oferta_id:
                    row_idx = i
                    break
            except Exception:
                continue

        if row_idx is None:
            return
        # initialize as fully opaque highlight (1.0 float opacity)
        self._highlighted_ids[oferta_id] = 1.0
        # notify view to repaint the row (background role)
        top_left = self.index(row_idx, 0)
        bottom_right = self.index(row_idx, self.columnCount() - 1)
        self.dataChanged.emit(top_left, bottom_right, [Qt.ItemDataRole.BackgroundRole])

        # Prefer a smooth fade using QVariantAnimation where available. Fallback to QTimer.
        try:
            from PySide6.QtCore import QVariantAnimation, QEasingCurve
            from PySide6.QtWidgets import QApplication

            if QApplication.instance() is not None:
                # Cancel any running animation for this oferta
                prev = self._active_animations.get(oferta_id)
                try:
                    if prev is not None:
                        prev.stop()
                except Exception:
                    pass

                anim = QVariantAnimation(self)
                anim.setStartValue(1.0)
                anim.setEndValue(0.0)
                # make the fade long enough to be visible by default (2s)
                anim.setDuration(duration_ms)
                try:
                    anim.setEasingCurve(QEasingCurve.Type.OutQuad)
                except Exception:
                    pass

                def on_value(val):
                    try:
                        self._highlighted_ids[oferta_id] = float(val)
                        self.dataChanged.emit(top_left, bottom_right, [Qt.ItemDataRole.BackgroundRole])
                    except Exception:
                        pass

                def on_finished():
                    try:
                        self._highlighted_ids.pop(oferta_id, None)
                        # clean animation reference
                        self._active_animations.pop(oferta_id, None)
                        self.dataChanged.emit(top_left, bottom_right, [Qt.ItemDataRole.BackgroundRole])
                    except Exception:
                        pass

                anim.valueChanged.connect(on_value)
                anim.finished.connect(on_finished)
                self._active_animations[oferta_id] = anim
                anim.start()
                return
        except Exception:
            # fall through to timer fallback
            pass

        # Fallback: decrement alpha periodically using QTimer (scale from 1.0)
        try:
            from PySide6.QtCore import QTimer

            interval = 50
            steps = max(1, duration_ms // interval)
            delta = 1.0 / max(1, steps)

            def _step():
                try:
                    cur = self._highlighted_ids.get(oferta_id)
                    if cur is None:
                        return
                    cur -= delta
                    if cur <= 0.0:
                        try:
                            del self._highlighted_ids[oferta_id]
                        except Exception:
                            self._highlighted_ids.pop(oferta_id, None)
                        self.dataChanged.emit(top_left, bottom_right, [Qt.ItemDataRole.BackgroundRole])
                        timer.stop()
                    else:
                        self._highlighted_ids[oferta_id] = cur
                        self.dataChanged.emit(top_left, bottom_right, [Qt.ItemDataRole.BackgroundRole])
                except Exception:
                    self._highlighted_ids.pop(oferta_id, None)
                    try:
                        timer.stop()
                    except Exception:
                        pass

            timer = QTimer(self)
            timer.timeout.connect(_step)
            timer.start(interval)
        except Exception:
            # If timers not available, clear instantly
            try:
                self._highlighted_ids.pop(oferta_id, None)
            except Exception:
                pass

    def rowCount(self, parent=QModelIndex()):
        return len(self.offers)

    def columnCount(self, parent=QModelIndex()):
        return 2

    def headerData(self, section: int, orientation: int, role: int = Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.headers[section]
        return None

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.offers)):
            return None

        offer = self.offers[index.row()]
        col = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            # first column must be empty — decoration (pixmap) will show active indicator
            if col == 0:
                return ''
            elif col == 1:
                return offer.get('descripcion') or ''

        # DecorationRole draws the green circle only when 'activa' is True. No decoration otherwise.
        if role == Qt.ItemDataRole.DecorationRole and col == 0:
            try:
                from PySide6.QtGui import QPixmap, QPainter, QColor
                pix = QPixmap(12, 12)
                pix.fill(QColor(0, 0, 0, 0))
                p = QPainter(pix)
                if bool(offer.get('activa')):
                    color = QColor(0, 180, 0)
                    p.setBrush(color)
                    p.setPen(color)
                    p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
                    p.drawEllipse(1, 1, 10, 10)
                    try:
                        p.end()
                    except Exception:
                        pass
                    return pix
                else:
                    try:
                        p.end()
                    except Exception:
                        pass
                    return None
            except Exception:
                # If any error occurs while drawing decoration, ignore and continue
                return None

        # Background highlight for recently-saved rows
        if role == Qt.ItemDataRole.BackgroundRole:
            try:
                oferta_id = offer.get('id')
                alpha = self._highlighted_ids.get(oferta_id)
                if alpha is not None:
                    from PySide6.QtGui import QBrush, QColor
                    # alpha may be float (0.0..1.0) or int (0..255) depending on implementation
                    try:
                        if isinstance(alpha, float):
                            val = int(alpha * 255)
                        else:
                            val = int(alpha)
                        a = max(0, min(255, val))
                    except Exception:
                        a = 200
                    return QBrush(QColor(255, 255, 150, a))
            except Exception:
                # Non-fatal; fall through to default
                return None

        # Center the decoration in the cell
        if role == Qt.ItemDataRole.TextAlignmentRole and col == 0:
            return Qt.AlignmentFlag.AlignCenter

    def get_offer(self, row: int):
        """Return the offer dict at row or None if out of range."""
        if 0 <= row < len(self.offers):
            return self.offers[row]
        return None


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
    
    def headerData(self, section: int, orientation: int, role: int = Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.headers[section]
        return None
    
    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
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
