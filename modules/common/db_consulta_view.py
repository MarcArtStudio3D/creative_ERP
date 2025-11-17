from typing import Optional, List

from PySide6.QtWidgets import QDialog
from PySide6.QtSql import QSqlQueryModel, QSqlDatabase
from PySide6.QtCore import Qt, QEvent

from app.views.ui_db_consulta_view import Ui_db_consulta_view


class DBConsultaView(QDialog):
    """Generic DB lookup dialog.

    It wraps the generated UI `Ui_db_consulta_view` and provides helpers to set
    SQL, headers, column sizes and delegates, and returns the selected row.
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
        self.cSQLFiltered = self.cSQL
        if 'where' in self.cSQL.lower():
            self.cSQLFiltered += ' and '
        else:
            self.cSQLFiltered += ' where '
        # Use the current selected field to filter
        campo = self.ui.cboCampoBusqueda.currentText().strip() or ''
        if campo:
            self.cSQLFiltered += f"{campo} like '%{filtro}%'"
        else:
            # fallback to generic clause: search across all columns would be needed, but
            # for now append a LIKE on the first column
            self.cSQLFiltered += f"like '%{filtro}%'"
        # extra filters (example from old code for articles)
        if self.ui.lbltabla.text() == 'articulos' and ('vista_art_prov' not in self.cSQL):
            if self.id_tarifa_cliente:
                self.cSQLFiltered += f" and tarifa = {int(self.id_tarifa_cliente)} "
        # append ordering
        self.cSQLFiltered += ' order by ' + (campo or '1') + f' {sentido}'
        try:
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
        self.setWindowTitle(str(titulo))

    def set_headers(self, cabecera: List[str]):
        if self.modelo is None:
            return
        for i, h in enumerate(cabecera):
            self.modelo.setHeaderData(i, Qt.Horizontal, h)
        # hide id column
        self.ui.resultado_list.setColumnHidden(0, True)
        self.headers = list(cabecera)

    def set_tamano_columnas(self, tamanos: List[int]):
        for i, t in enumerate(tamanos):
            self.ui.resultado_list.setColumnWidth(i, int(t))

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
        if event.type() == QEvent.KeyPress and target is self.ui.resultado_list:
            key = event.key()
            if key in (Qt.Key_Return, Qt.Key_Enter, Qt.Key_Tab):
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
