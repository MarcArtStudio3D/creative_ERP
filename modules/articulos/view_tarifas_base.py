from PySide6.QtWidgets import QDialog, QMessageBox, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSizePolicy

from modules.articulos.ui_frmTarifasBase import Ui_Dialog
from modules.articulos.tarifa_tipo_controller import TarifaTipoController
from core.db import get_current_database, set_current_database


class TarifasBaseView(QDialog):
    """Vista y wiring mínimo CRUD para `tarifas_tipo` usando la UI generada.

    - Página 1: formulario (fields: codigo, nombre, moneda, descripcion)
    - Página 2: lista (tableWidget) con resultados de búsqueda/consulta
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # When embedded inside MainWindow, ensure this view behaves as a widget
        # and not as a floating dialog (which would resist layout stretching).
        self.setWindowFlags(Qt.Widget)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Ensure DB points to artstudio3d for tarifa types
        self._ensure_tarifas_database()

        self.controller = TarifaTipoController()
        self.is_new = False
        # Track whether the user has edited search/form fields since last navigation/load
        self._search_dirty = False
        self._suppress_search_dirty = False

        self._setup_connections()
        self._setup_initial_state()

    def _ensure_tarifas_database(self):
        """
        Ensure the view is using the correct articles database for the currently
        selected company. In a multi-company setup the database name should come
        from the company context and must NOT be hard-coded.

        Behavior:
        - If current DB is 'main' and a company is selected, switch to that
          company's database (company context returns 'database_name').
        - Otherwise do nothing and keep current database.
        """
        current = get_current_database()
        if current == 'main':
            try:
                # Use company_manager to find the company DB name rather than hardcoding
                from core.company_manager import get_current_company_context

                ctx = get_current_company_context()
                if ctx.get('has_company') and ctx.get('database_name'):
                    set_current_database(ctx.get('database_name'))
            except Exception:
                # If anything goes wrong, don't crash the view — leave the current DB
                pass

    def _setup_connections(self):
        self.ui.btnAnadir.clicked.connect(self._on_add)
        self.ui.btnSiguente.clicked.connect(self._on_next)
        self.ui.btnAnterior.clicked.connect(self._on_prev)
        self.ui.btnBuscar.clicked.connect(self._on_search)
        self.ui.btnEditar.clicked.connect(self._on_edit)
        self.ui.btnGuardar.clicked.connect(self._on_save)
        self.ui.btnDeshacer.clicked.connect(self._on_undo)
        self.ui.btnBorrar.clicked.connect(self._on_delete)
        self.ui.pushButton.clicked.connect(self.close)

        # Table selection: double-click or selection to load
        # Connect all three available double-click signals to be robust
        # connect double-click signals (no debug prints)
        try:
            self.ui.tableWidget.cellDoubleClicked.connect(self._on_table_double_click)
            pass
        except Exception as e:
            print(f"✗ Warning: No se pudo conectar cellDoubleClicked: {e}")
        try:
            # map QModelIndex -> (row, col)
            self.ui.tableWidget.doubleClicked.connect(lambda idx: self._on_table_double_click(idx.row(), idx.column()))
            pass
        except Exception as e:
            print(f"✗ Warning: No se pudo conectar doubleClicked: {e}")
        try:
            # itemDoubleClicked provides the QTableWidgetItem directly
            self.ui.tableWidget.itemDoubleClicked.connect(lambda item: self._on_table_double_click(item.row(), item.column()))
            pass
        except Exception as e:
            print(f"✗ Warning: No se pudo conectar itemDoubleClicked: {e}")

        # Mark search fields as dirty when the user edits them explicitly
        if hasattr(self.ui, 'lineEdit'):
            try:
                # mark dirty when user edits
                self.ui.lineEdit.textEdited.connect(lambda *_: self._mark_search_dirty(True))
                # real-time filtering: when the user changes the text (typing) or finishes editing,
                # run the search so the list updates immediately.
                def _lineedit_search(_=None):
                    if getattr(self, '_suppress_search_dirty', False):
                        return
                    # mark as user-modified and search (but don't switch pages during typing)
                    self._mark_search_dirty(True)
                    self._on_search(switch_to_list=False)

                self.ui.lineEdit.textChanged.connect(_lineedit_search)
                try:
                    # When user finishes editing, keep filtering only (don't switch pages)
                    self.ui.lineEdit.editingFinished.connect(lambda: self._on_search(switch_to_list=False))
                except Exception:
                    pass
            except Exception:
                pass
        if hasattr(self.ui, 'lineEdit_2'):
            try:
                self.ui.lineEdit_2.textEdited.connect(lambda *_: self._mark_search_dirty(True))
                def _lineedit2_search(_=None):
                    if getattr(self, '_suppress_search_dirty', False):
                        return
                    self._mark_search_dirty(True)
                    self._on_search(switch_to_list=False)
                self.ui.lineEdit_2.textChanged.connect(_lineedit2_search)
                try:
                    self.ui.lineEdit_2.editingFinished.connect(lambda: self._on_search(switch_to_list=False))
                except Exception:
                    pass
            except Exception:
                pass
        if hasattr(self.ui, 'plainTextEdit'):
            try:
                self.ui.plainTextEdit.textChanged.connect(lambda *_: self._mark_search_dirty(True))
                # PlainTextEdit emits textChanged frequently; use it to trigger live search as well
                def _plaintext_search():
                    if getattr(self, '_suppress_search_dirty', False):
                        return
                    self._mark_search_dirty(True)
                    self._on_search(switch_to_list=False)
                self.ui.plainTextEdit.textChanged.connect(_plaintext_search)
            except Exception:
                pass
        if hasattr(self.ui, 'comboBox'):
            try:
                self.ui.comboBox.currentTextChanged.connect(lambda *_: self._mark_search_dirty(True))
                self.ui.comboBox.currentTextChanged.connect(lambda *_: self._on_search(switch_to_list=False))
            except Exception:
                pass

    def _setup_initial_state(self):
        # show list initially
        try:
            self.ui.stackedWidget.setCurrentIndex(1)
        except Exception:
            pass

        # configure table columns
        self._setup_table()
        # load data
        self._load_table()
        # lock fields
        self._lock_fields(True)

    def _setup_table(self):
        # Show two visible columns: Código and Nombre. Keep an ID column hidden so we can
        # identify records when users select rows (used by edit/delete handlers).
        headers = ["ID", "Código", "Nombre"]
        self.ui.tableWidget.setColumnCount(len(headers))
        self.ui.tableWidget.setHorizontalHeaderLabels(headers)
        # Hide the internal ID column (index 0) -- UI shows only Código and Nombre
        self.ui.tableWidget.setColumnHidden(0, True)

        # Make 'Código' column fit its contents and let 'Nombre' take remaining width
        header = self.ui.tableWidget.horizontalHeader()
        # column indexes: 0=ID(hidden), 1=Código, 2=Nombre
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        
        # Ensure the table allows selection and editing
        from PySide6.QtWidgets import QAbstractItemView
        self.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        
        # setup complete

    def _load_table(self, data: list | None = None):
        # Suppress dirty signals while we populate the table (programmatic update)
        self._suppress_search_dirty = True
        try:
            if data is None:
                data = self.controller.list_all()

            self.ui.tableWidget.setRowCount(0)
            for row in data:
                r = self.ui.tableWidget.rowCount()
                self.ui.tableWidget.insertRow(r)
                # Column 0 is internal ID (hidden), 1 -> Código, 2 -> Nombre
                self.ui.tableWidget.setItem(r, 0, QTableWidgetItem(str(row.get('id', ''))))
                self.ui.tableWidget.setItem(r, 1, QTableWidgetItem(row.get('codigo') or ''))
                self.ui.tableWidget.setItem(r, 2, QTableWidgetItem(row.get('nombre') or ''))
        finally:
            # After loading a full list, the search fields are considered clean (not dirty)
            self._suppress_search_dirty = False
            self._mark_search_dirty(False)

    def _lock_fields(self, locked: bool):
        # Map fields prepared in UI
        for wname in ('lineEdit', 'lineEdit_2', 'comboBox', 'plainTextEdit'):
            if hasattr(self.ui, wname):
                w = getattr(self.ui, wname)
                try:
                    w.setReadOnly(locked)
                except Exception:
                    # comboBox doesn't have setReadOnly -> use setEnabled
                    try:
                        w.setEnabled(not locked)
                    except Exception:
                        pass

        # Buttons
        self.ui.btnAnadir.setEnabled(locked)
        self.ui.btnEditar.setEnabled(locked)
        self.ui.btnGuardar.setEnabled(not locked)
        self.ui.btnDeshacer.setEnabled(not locked)
        self.ui.btnBorrar.setEnabled(locked)
        self.ui.btnBuscar.setEnabled(locked)

    def _collect_form(self) -> dict:
        payload = {
            'codigo': self.ui.lineEdit.text().strip() if hasattr(self.ui, 'lineEdit') else None,
            'nombre': self.ui.lineEdit_2.text().strip() if hasattr(self.ui, 'lineEdit_2') else None,
            'moneda': self.ui.comboBox.currentText() if hasattr(self.ui, 'comboBox') else None,
            'descripcion': self.ui.plainTextEdit.toPlainText().strip() if hasattr(self.ui, 'plainTextEdit') else None,
        }
        return payload

    def _fill_form(self, data: dict | None):
        if data is None:
            # clear
            if hasattr(self.ui, 'lineEdit'):
                self.ui.lineEdit.clear()
            if hasattr(self.ui, 'lineEdit_2'):
                self.ui.lineEdit_2.clear()
            if hasattr(self.ui, 'comboBox'):
                self.ui.comboBox.setCurrentIndex(-1)
            if hasattr(self.ui, 'plainTextEdit'):
                self.ui.plainTextEdit.clear()
            # If we clear the form, treat as user editing (dirty)
            self._mark_search_dirty(True)
            return

        # When loading a record from controller (navigation) we want to suppress
        # any signal that would mark the search as dirty (user edits). Set suppression
        # while we programmatically populate fields.
        self._suppress_search_dirty = True
        try:
            if hasattr(self.ui, 'lineEdit'):
                self.ui.lineEdit.setText(str(data.get('codigo', '') or ''))
            if hasattr(self.ui, 'lineEdit_2'):
                self.ui.lineEdit_2.setText(str(data.get('nombre', '') or ''))
            if hasattr(self.ui, 'comboBox'):
                # try to match text
                value = str(data.get('moneda', '') or '')
                idx = self.ui.comboBox.findText(value)
                if idx >= 0:
                    self.ui.comboBox.setCurrentIndex(idx)
                else:
                    # append if not present
                    if value:
                        self.ui.comboBox.addItem(value)
                        self.ui.comboBox.setCurrentText(value)

            if hasattr(self.ui, 'plainTextEdit'):
                self.ui.plainTextEdit.setPlainText(str(data.get('descripcion', '') or ''))

            # Loading a record should not mark the search as dirty so Buscar shows all rows.
            self._mark_search_dirty(False)
        finally:
            self._suppress_search_dirty = False

    # ==================== Handlers ====================

    def _on_search(self, switch_to_list=True):
        """Filter table based on search fields.
        
        Args:
            switch_to_list: If True, switch to list page after filtering.
                           If False, only update the table data without changing pages.
        """
        # Simple filter using provided fields
        try:
            all_items = self.controller.list_all()
            code_q = self.ui.lineEdit.text().strip() if hasattr(self.ui, 'lineEdit') else ''
            name_q = self.ui.lineEdit_2.text().strip() if hasattr(self.ui, 'lineEdit_2') else ''
            moneda_q = self.ui.comboBox.currentText().strip() if hasattr(self.ui, 'comboBox') else ''
            desc_q = self.ui.plainTextEdit.toPlainText().strip() if hasattr(self.ui, 'plainTextEdit') else ''

            # If the user hasn't explicitly edited the search fields (not dirty),
            # show all records by default instead of filtering by current form values.
            if not getattr(self, '_search_dirty', False):
                filtered = all_items
            else:
                def match(item):
                    if code_q and code_q.lower() not in str(item.get('codigo', '')).lower():
                        return False
                    if name_q and name_q.lower() not in str(item.get('nombre', '')).lower():
                        return False
                    if moneda_q and moneda_q.lower() not in str(item.get('moneda', '')).lower():
                        return False
                    if desc_q and desc_q.lower() not in str(item.get('descripcion', '')).lower():
                        return False
                    return True
                filtered = [i for i in all_items if match(i)]
            self._load_table(filtered)
            # Only switch to list page if explicitly requested (e.g., "Buscar" button clicked)
            # Don't switch during real-time filtering while editing
            if switch_to_list:
                self.ui.stackedWidget.setCurrentIndex(1)
        except Exception as e:
            QMessageBox.critical(self, self.tr("Error"), str(e))

    def _on_table_double_click(self, row, col):
        # called when a user double-clicks a row; attempt to load the corresponding record
        try:
            # Try to obtain the internal ID from hidden column 0
            id_item = self.ui.tableWidget.item(row, 0)
            tipo_id = None
            if id_item and id_item.text():
                try:
                    tipo_id = int(id_item.text())
                    pass
                except Exception as e:
                    # If the hidden column wasn't numeric, leave tipo_id None
                    pass
                    tipo_id = None
            else:
                print(f"DEBUG: id_item es None o vacío")

            # Primary path: try to load by ID
            loaded = False
            if tipo_id is not None:
                print(f"DEBUG: Intentando cargar por ID {tipo_id}...")
                loaded = self.controller.load_by_id(tipo_id)
                print(f"DEBUG: load_by_id result = {loaded}")
            else:
                pass

            # Fallback: try to match the row by codigo or nombre within cached list
            if not loaded:
                # fallback: try to find by visible values
                # Attempt to get codigo or nombre from visible columns
                codigo_item = self.ui.tableWidget.item(row, 1)
                nombre_item = self.ui.tableWidget.item(row, 2)
                codigo_val = codigo_item.text().strip() if codigo_item and codigo_item.text() else ''
                nombre_val = nombre_item.text().strip() if nombre_item and nombre_item.text() else ''

                # Ensure we have a fresh list to search in (controller may have cached list)
                try:
                    candidates = self.controller.index_list or self.controller.list_all() or []
                except Exception:
                    candidates = []

                found_id = None
                for itm in candidates:
                    # Match on codigo or nombre (case-insensitive, substring)
                    try:
                        if codigo_val and codigo_val.lower() in str(itm.get('codigo', '') or '').lower():
                            found_id = itm.get('id')
                            break
                        if nombre_val and nombre_val.lower() in str(itm.get('nombre', '') or '').lower():
                            found_id = itm.get('id')
                            break
                    except Exception:
                        continue

                if found_id is not None:
                    pass
                    loaded = self.controller.load_by_id(found_id)
                    pass
                else:
                    pass

            if loaded:
                # We have loaded the record successfully — populate the form and switch to edit
                self._fill_form(self.controller.current)
                self._lock_fields(True)
                self.is_new = False
                # switch to edit page
                self.ui.stackedWidget.setCurrentIndex(0)
                pass
            else:
                # Inform the user if we couldn't load the record — prevents silent failures
                # inform the user if loading failed
                QMessageBox.warning(self, self.tr("No encontrado"), self.tr("No se pudo cargar el registro para edición"))
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, self.tr("Error"), str(e))

    def _on_add(self):
        # prepare new
        self.is_new = True
        self._fill_form(None)
        self._lock_fields(False)
        self.ui.stackedWidget.setCurrentIndex(0)

    def _on_edit(self):
        # try to find selected row in table
        current_row = self.ui.tableWidget.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, self.tr("Seleccione"), self.tr("Seleccione un registro en la lista para editar"))
            return
        id_item = self.ui.tableWidget.item(current_row, 0)
        if not id_item:
            QMessageBox.warning(self, self.tr("Seleccione"), self.tr("ID no encontrado en la fila seleccionada"))
            return
        tipo_id = int(id_item.text())
        if not self.controller.load_by_id(tipo_id):
            QMessageBox.warning(self, self.tr("No encontrado"), self.tr("Registro no encontrado"))
            return

        self._fill_form(self.controller.current)
        self.is_new = False
        self._lock_fields(False)
        self.ui.stackedWidget.setCurrentIndex(0)

    def _on_save(self):
        payload = self._collect_form()
        if not payload.get('nombre'):
            QMessageBox.warning(self, self.tr("Validación"), self.tr("El campo nombre es obligatorio"))
            return

        try:
            if self.is_new:
                new_id = self.controller.create(payload)
                if new_id:
                    QMessageBox.information(self, self.tr("Éxito"), self.tr("Tipo de tarifa creado"))
            else:
                # must have current
                if not self.controller.current:
                    QMessageBox.warning(self, self.tr("Seleccione"), self.tr("No hay registro cargado para actualizar"))
                    return
                ok = self.controller.update(int(self.controller.current.get('id')), payload)
                if ok:
                    QMessageBox.information(self, self.tr("Éxito"), self.tr("Tipo de tarifa actualizado"))

            # Refresh table and switch to list
            self._load_table()
            self._lock_fields(True)
            self.is_new = False
            self.ui.stackedWidget.setCurrentIndex(1)

        except Exception as e:
            QMessageBox.critical(self, self.tr("Error"), str(e))

    def _on_undo(self):
        if self.is_new:
            self._fill_form(None)
        else:
            self._fill_form(self.controller.current)
        self._lock_fields(True)

    def _mark_search_dirty(self, value: bool):
        """Set internal dirty flag which signals the user has modified search fields.

        When False: Buscar will show all records by default.
        When True: Buscar will apply the current field values as filters.
        """
        # If suppression is active, ignore attempts to mark the search as dirty
        # coming from programmatic updates. Allow clearing (False) though.
        if getattr(self, '_suppress_search_dirty', False) and value:
            return
        try:
            self._search_dirty = bool(value)
        except Exception:
            self._search_dirty = False
        self.is_new = False

    def _on_delete(self):
        # delete selected
        current_row = self.ui.tableWidget.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, self.tr("Seleccione"), self.tr("Seleccione un registro en la lista para borrar"))
            return
        id_item = self.ui.tableWidget.item(current_row, 0)
        if not id_item:
            return
        tipo_id = int(id_item.text())

        reply = QMessageBox.question(self, self.tr("Confirmar"), self.tr("¿Desea borrar este tipo de tarifa?"),
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.No:
            return

        try:
            ok = self.controller.delete(tipo_id)
            if ok:
                QMessageBox.information(self, self.tr("Éxito"), self.tr("Registro borrado"))
            else:
                QMessageBox.warning(self, self.tr("Error"), self.tr("No se pudo borrar el registro"))
            self._load_table()
        except Exception as e:
            QMessageBox.critical(self, self.tr("Error"), str(e))

    def _on_next(self):
        if self.controller.next():
            self._fill_form(self.controller.current)
            self.ui.stackedWidget.setCurrentIndex(0)

    def _on_prev(self):
        if self.controller.prev():
            self._fill_form(self.controller.current)
            self.ui.stackedWidget.setCurrentIndex(0)

    # ------------------ Public API for MainWindow side-panel ------------------
    def list(self):
        """Public method to switch to list view (used by main_window side-panel)."""
        try:
            self.ui.stackedWidget.setCurrentIndex(1)
        except Exception:
            pass

    def nuevo(self):
        """Public alias for creating a new record (panel action 'Nuevo')."""
        self._on_add()
        # Ensure the public flag remains set after internal handlers which may
        # reset it (e.g. _mark_search_dirty). Keep the external contract: nuevo()
        # sets is_new True.
        try:
            self.is_new = True
        except Exception:
            pass

    def editar(self):
        """Public alias for edit action (panel action 'Editar')."""
        self._on_edit()

    def borrar(self):
        """Public alias for delete action (panel action 'Borrar')."""
        self._on_delete()

    def search(self, text: str):
        """Search API intended to be invoked by side-panel search field.

        The main window will pass a single free-text string — here we perform a
        simple substring match across codigo, nombre, descripcion and moneda.
        """
        try:
            q = (text or '').strip().lower()
            all_items = self.controller.list_all()
            if not q:
                self._load_table(all_items)
                return

            def match(item: dict) -> bool:
                for k in ('codigo', 'nombre', 'descripcion', 'moneda'):
                    if q in str(item.get(k, '') or '').lower():
                        return True
                return False

            filtered = [itm for itm in all_items if match(itm)]
            self._load_table(filtered)
            self.ui.stackedWidget.setCurrentIndex(1)
        except Exception:
            # Keep robust — panel should not break the module
            pass

    def filtrar(self, text: str):
        """Spanish alias for search()."""
        self.search(text)

    def filter_records(self, text: str, order_by: str | None = None, order_mode: str | None = None):
        """More advanced search signature used from main_window if available.

        This implementation currently ignores order_by / order_mode and delegates
        to the simple search() behaviour.
        """
        self.search(text)

    def get_search_options(self) -> dict:
        """Expose search options for the side-panel (labels and placeholders)."""
        return {
            'sort_fields': [
                ("Código", "codigo"),
                ("Nombre", "nombre"),
            ],
            'search_placeholder': self.tr("Buscar por código, nombre o descripción...")
        }
