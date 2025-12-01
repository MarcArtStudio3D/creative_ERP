from typing import Optional, List, Dict

from PySide6.QtWidgets import QDialog
from PySide6.QtSql import QSqlQueryModel, QSqlDatabase
from PySide6.QtCore import Qt, QEvent, QAbstractTableModel

from modules.common.ui_db_consulta_view import Ui_db_consulta_view


class DBConsultaView(QDialog):
    """Generic DB lookup dialog.

    It wraps the generated UI `Ui_db_consulta_view` and provides helpers to set
    SQL, headers, column sizes and delegates, and returns the selected row.
    
    Example usage:
        from modules.common.db_consulta_view import DBConsultaView
        sql = "SELECT id, poblacion, provincia FROM poblaciones WHERE cp = 28001"
        id, record = DBConsultaView.select_from_sql(parent, sql, db='group', 
                                                    headers=['id','poblacion','provincia'],
                                                    campos=['poblacion'])
        if id:
            # record is a QSqlRecord, can call record.value('poblacion') or by index
            poblacion = record.value('poblacion')
            provincia = record.value('provincia')
            # put this back to your form
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_db_consulta_view()
        self.ui.setupUi(self)
        self.ui.resultado_list.installEventFilter(self)
        self.id = 0
        self._r = None
        self.cSQL = ''
        self.cSQLFiltered = ''
        self.modelo: Optional[QSqlQueryModel] = None
        self.db: Optional[str | QSqlDatabase] = None
        self.headers: List[str] = []
        self.id_tarifa_cliente = None
        self.tipo_dto_tarifa = None

        # initialize sentido list
        self.ui.cboSentido.addItems(["A-Z", "Z-A"])

        # wire signals
        self.ui.lineaTextoBuscar.textChanged.connect(self.on_lineaTextoBuscar_textChanged)
        self.ui.resultado_list.clicked.connect(self.on_resultado_list_clicked)
        self.ui.resultado_list.doubleClicked.connect(self.on_resultado_list_doubleClicked)
        self.ui.btn_aceptar.clicked.connect(self.accept)
        self.ui.btn_cancelar.clicked.connect(self.reject)
        
        # Connect comboboxes to update filter immediately
        self.ui.cboSentido.currentIndexChanged.connect(lambda: self.set_filtro(self.ui.lineaTextoBuscar.text()))
        self.ui.cboCampoBusqueda.currentIndexChanged.connect(lambda: self.set_filtro(self.ui.lineaTextoBuscar.text()))

    # helper getters
    def get_selected_id(self) -> int:
        return int(self.id) if self.id else 0

    def get_selected_record(self):
        return self._r

    # API to configure dialog
    def set_texto_tabla(self, tabla: str):
        self.ui.lbltabla.setText(str(tabla))

    def set_SQL(self, cSQL: str, qdb: Optional[QSqlDatabase] = None):
        """Set the SQL that will be used for the model. If qdb is provided
        it is used as the database connection; otherwise self.db string is used
        to lookup a connection by name with QSqlDatabase.database(name).
        """
        self.cSQL = cSQL
        self.modelo = QSqlQueryModel(self)
        db_conn = None
        if isinstance(qdb, QSqlDatabase):
            db_conn = qdb
        elif isinstance(self.db, QSqlDatabase):
            db_conn = self.db
        elif isinstance(self.db, str):
            # attempt to get a named connection
            try:
                db_conn = QSqlDatabase.database(self.db)
            except Exception:
                db_conn = None
        try:
            if db_conn is not None:
                self.modelo.setQuery(cSQL, db_conn)
            else:
                self.modelo.setQuery(cSQL)
            self.ui.resultado_list.setModel(self.modelo)
        except Exception:
            # swallow error — model will be empty; caller can inspect errors
            pass

    def set_filtro(self, filtro: str):
        sentido = ''
        if self.ui.cboSentido.currentText() == 'Z-A':
            sentido = 'DESC'
        self.cSQLFiltered = ''
        if not self.cSQL:
            return
        self.cSQLFiltered = ''
        if not self.cSQL:
            return
            
        # Strip existing ORDER BY to avoid syntax errors (e.g. ... ORDER BY ... WHERE ...)
        base_sql = self.cSQL
        lower_sql = base_sql.lower()
        
        # Strip LIMIT first (it's usually at the end)
        limit_index = lower_sql.rfind(' limit ')
        if limit_index != -1:
            base_sql = base_sql[:limit_index]
            lower_sql = base_sql.lower() # update lower_sql for order by check
            
        order_by_index = lower_sql.rfind(' order by ')
        if order_by_index != -1:
            base_sql = base_sql[:order_by_index]
            
        self.cSQLFiltered = base_sql
        
        if 'where' in base_sql.lower():
            self.cSQLFiltered += ' and '
        else:
            self.cSQLFiltered += ' where '
            
        # Use the current selected field to filter
        campo = self.ui.cboCampoBusqueda.currentText().strip() or ''
        if campo:
            # Escape single quotes in filtro to prevent SQL injection
            filtro_escaped = filtro.replace("'", "''")
            # Use UPPER for case-insensitive matching on accented characters in SQLite
            self.cSQLFiltered += f"{campo} like '%{filtro_escaped.upper()}%'"
        else:
            # fallback to generic clause: search across all columns would be needed, but
            # for now append a LIKE on the first column (assuming it's not the ID column)
            # If no columns available, skip filtering
            if self.headers and len(self.headers) > 1:
                first_column = self.headers[1]  # Skip ID column (index 0)
                filtro_escaped = filtro.replace("'", "''")
                self.cSQLFiltered += f"{first_column} like '%{filtro_escaped}%'"
            else:
                # No valid columns to filter, remove the WHERE/AND clause we just added
                # We go back to base_sql which has no ORDER BY, but we will add it later
                self.cSQLFiltered = base_sql
        # extra filters (example from old code for articles)
        if self.ui.lbltabla.text() == 'articulos' and ('vista_art_prov' not in self.cSQL):
            if self.id_tarifa_cliente:
                self.cSQLFiltered += f" and tarifa = {int(self.id_tarifa_cliente)} "
        # append ordering
        self.cSQLFiltered += ' order by ' + (campo or '1') + f' {sentido}'
        try:
            if self.modelo is None:
                return  # No model set, cannot filter
            if isinstance(self.db, QSqlDatabase):
                self.modelo.setQuery(self.cSQLFiltered, self.db)
            elif isinstance(self.db, str):
                try:
                    dbc = QSqlDatabase.database(self.db)
                    self.modelo.setQuery(self.cSQLFiltered, dbc)
                except Exception:
                    self.modelo.setQuery(self.cSQLFiltered)
            else:
                self.modelo.setQuery(self.cSQLFiltered)
        except Exception:
            pass

    def set_titulo(self, titulo: str):
        self.ui.lbltabla.setText(str(titulo))
        self.setWindowTitle(str(titulo))

    def set_headers(self, cabecera: List[str]):
        if self.modelo is None:
            return
        for i, h in enumerate(cabecera):
            self.modelo.setHeaderData(i, Qt.Orientation.Horizontal, h)
        # hide id column
        self.ui.resultado_list.setColumnHidden(0, True)
        self.headers = list(cabecera)

    def set_tamano_columnas(self, tamanos: List[int]):
        """Set column widths. Last column will stretch to fill remaining space.
        
        Args:
            tamanos: List of column widths in pixels. If fewer widths than columns,
                    remaining columns use default width. Last column always stretches.
        """
        from PySide6.QtWidgets import QHeaderView
        
        # Set specific widths for provided columns
        for i, t in enumerate(tamanos):
            if i < self.ui.resultado_list.model().columnCount():
                self.ui.resultado_list.setColumnWidth(i, int(t))
        
        # Make the last visible column stretch to fill remaining space
        last_col = self.ui.resultado_list.model().columnCount() - 1
        if last_col >= 0:
            self.ui.resultado_list.horizontalHeader().setStretchLastSection(True)

    def set_delegate_monetary(self, cols):
        # Delegates are project-specific; no-op if not available
        from importlib import import_module
        try:
            Monetary = import_module('modules.auxiliares.monetarydelegate')
            for pos in cols:
                try:
                    self.ui.resultado_list.setItemDelegateForColumn(int(pos), Monetary.MonetaryDelegate(self))
                except Exception:
                    pass
        except Exception:
            pass

    def set_delegate_fecha(self, cols):
        from importlib import import_module
        try:
            DateD = import_module('modules.auxiliares.datedelegate')
            for pos in cols:
                try:
                    self.ui.resultado_list.setItemDelegateForColumn(int(pos), DateD.DateDelegate(self))
                except Exception:
                    pass
        except Exception:
            pass

    def set_campoBusqueda(self, campos: List[str]):
        self.ui.cboCampoBusqueda.clear()
        self.ui.cboCampoBusqueda.addItems(campos)

    def set_db(self, nombre_db: str | QSqlDatabase):
        self.db = nombre_db

    def setId_tarifa_cliente(self, value: int):
        self.id_tarifa_cliente = value

    def setTipo_dto_tarifa(self, value: int):
        self.tipo_dto_tarifa = value

    # event filter to detect Enter/Tab
    def eventFilter(self, target, event):
        if event.type() == QEvent.Type.KeyPress and target is self.ui.resultado_list:
            key = event.key()
            if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_Tab):
                row = self.ui.resultado_list.currentIndex().row()
                if self.modelo is not None:
                    self.id = int(self.modelo.data(self.modelo.index(row, 0)))
                self.ui.btn_aceptar.setFocus()
                return True
        return super().eventFilter(target, event)

    # slots
    def on_lineaTextoBuscar_textChanged(self, text: str):
        self.set_filtro(text)

    def on_resultado_list_clicked(self, index):
        self.ui.resultado_list.blockSignals(True)
        row = index.row()
        if self.modelo is not None:
            try:
                self.id = int(self.modelo.data(self.modelo.index(row, 0)))
            except Exception:
                self.id = 0
            try:
                self._r = self.modelo.record(row)
            except Exception:
                self._r = None
        self.ui.resultado_list.blockSignals(False)

    def on_resultado_list_doubleClicked(self, index):
        self.on_resultado_list_clicked(index)
        try:
            self.ui.btn_aceptar.click()
        except Exception:
            self.accept()

    def exec_select(self):
        """Execute dialog and return (id, record) tuple if accepted else (0, None)."""
        rv = self.exec()
        if rv == QDialog.DialogCode.Accepted:
            return self.get_selected_id(), self.get_selected_record()
        return 0, None

    @staticmethod
    def select_from_sql(parent, sql: str, db: Optional[str | QSqlDatabase] = None, 
                       headers: Optional[List[str]] = None, campos: Optional[List[str]] = None, 
                       titulo: Optional[str] = None, tamanos: Optional[List[int]] = None):
        """Convenience method to show dialog and return (id, record) after user selects.

        Parameters:
            parent: parent widget
            sql: SQL string for the model
            db: either a connection name or a QSqlDatabase
            headers: optional column headers (strings)
            campos: optional list of fields for search combobox
            titulo: optional window title
            tamanos: optional list of column widths in pixels (last column stretches)
        """
        dlg = DBConsultaView(parent)
        if db:
            dlg.set_db(db)
        if titulo:
            dlg.set_titulo(titulo)
        if campos:
            dlg.set_campoBusqueda(campos)
        # Set SQL first to create the model
        dlg.set_SQL(sql)
        # Then set headers and column widths (they need the model to exist)
        if headers:
            dlg.set_headers(headers)
        if tamanos:
            dlg.set_tamano_columnas(tamanos)
        return dlg.exec_select()
    
    @staticmethod
    def select_from_data(parent, data: List[Dict], headers: List[str], 
                        campos: Optional[List[str]] = None, titulo: Optional[str] = None):
        """Convenience method to show dialog with dictionary data and return selected item.
        
        This is a direct alternative to select_from_sql that works with Python data
        without requiring QSqlDatabase connections.
        
        Parameters:
            parent: parent widget
            data: list of dictionaries with the data to display
            headers: column headers (strings) 
            campos: optional list of fields for search combobox
            titulo: optional window title
        
        Returns:
            (selected_dict, None) if user selects, (None, None) if cancelled
        """
        from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
        from PySide6.QtSql import QSqlRecord
        
        class DataTableModel(QAbstractTableModel):
            def __init__(self, data, headers):
                super().__init__()
                self._data = data
                self._headers = headers
                self._filtered_data = data.copy()
                
            def rowCount(self, parent=QModelIndex()):
                return len(self._filtered_data)
                
            def columnCount(self, parent=QModelIndex()):
                return len(self._headers)
                
            def data(self, index, role):
                if not index.isValid() or index.row() >= len(self._filtered_data) or index.column() >= len(self._headers):
                    return None
                    
                if role == Qt.ItemDataRole.DisplayRole:
                    row_data = self._filtered_data[index.row()]
                    col = index.column()
                    
                    # Simple mapping: column 0=id, column 1=codigo, column 2=seccion
                    if col == 0:
                        return str(row_data.get('id', ''))
                    elif col == 1:
                        return str(row_data.get('codigo', ''))
                    elif col == 2:
                        return str(row_data.get('seccion', ''))
                    
                return None
                
            def headerData(self, section, orientation, role):
                if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
                    if 0 <= section < len(self._headers):
                        return self._headers[section]
                return None
                
            def filter_data(self, search_text, search_field=None):
                self.beginResetModel()
                
                if not search_text:
                    self._filtered_data = self._data.copy()
                else:
                    self._filtered_data = []
                    search_lower = search_text.lower()
                    
                    for row in self._data:
                        if search_field:
                            # Search in specific field
                            field_value = str(row.get(search_field, '')).lower()
                            if search_lower in field_value:
                                self._filtered_data.append(row)
                        else:
                            # Search in all fields
                            found = False
                            for key, value in row.items():
                                if search_lower in str(value).lower():
                                    found = True
                                    break
                            if found:
                                self._filtered_data.append(row)
                
                self.endResetModel()
        
        # Create dialog
        dlg = DBConsultaView(parent)
        
        # Set title
        if titulo:
            dlg.set_titulo(titulo)
            
        # Set search fields
        if campos:
            dlg.set_campoBusqueda(campos)
            
        # Create and set custom model
        model = DataTableModel(data, headers)
        dlg.modelo = model
        dlg.ui.resultado_list.setModel(model)
        
        # Set headers
        if headers:
            dlg.set_headers(headers)
            # Also set table headers directly for custom model
            dlg.ui.resultado_list.model().headers = headers
        
        # Override filter method to work with our custom model
        original_filter = dlg.set_filtro
        def custom_filter(filtro_text):
            search_field = dlg.ui.cboCampoBusqueda.currentText().strip()
            if not search_field and campos:
                search_field = campos[0] if campos else None
            model.filter_data(filtro_text, search_field)
        dlg.set_filtro = custom_filter
        
        # Override click handler to work with filtered data
        def custom_click_handler():
            current_index = dlg.ui.resultado_list.currentIndex()
            if current_index.isValid():
                row = current_index.row()
                if 0 <= row < len(model._filtered_data):
                    selected_data = model._filtered_data[row]
                    # Create a mock QSqlRecord for compatibility
                    from PySide6.QtSql import QSqlField
                    record = QSqlRecord()
                    for i, header in enumerate(headers):
                        key = header.lower()
                        if key == 'código':
                            key = 'codigo'
                        elif key == 'sección':
                            key = 'seccion'
                        
                        field = QSqlField(key)
                        field.setValue(str(selected_data.get(key, '')))
                        record.append(field)
                    
                    dlg.id = selected_data.get('id', 0)
                    dlg._r = record
        
        dlg.ui.resultado_list.clicked.connect(custom_click_handler)
        dlg.ui.resultado_list.doubleClicked.connect(lambda: (custom_click_handler(), dlg.accept()))
        
        # Show dialog
        if dlg.exec() == dlg.DialogCode.Accepted:
            current_index = dlg.ui.resultado_list.currentIndex()
            if current_index.isValid():
                row = current_index.row()
                if 0 <= row < len(model._filtered_data):
                    return model._filtered_data[row], dlg._r
        
        return None, None
