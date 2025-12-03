from PySide6.QtWidgets import QDialog, QMessageBox, QTableWidgetItem
from PySide6.QtCore import Qt

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

        # Ensure DB points to artstudio3d for tarifa types
        self._ensure_tarifas_database()

        self.controller = TarifaTipoController()
        self.is_new = False

        self._setup_connections()
        self._setup_initial_state()

    def _ensure_tarifas_database(self):
        current = get_current_database()
        if current == 'main':
            try:
                set_current_database('artstudio3d')
            except Exception:
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
        self.ui.tableWidget.cellDoubleClicked.connect(self._on_table_double_click)

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
        headers = ["ID", "Código", "Nombre", "Moneda", "Descripción"]
        self.ui.tableWidget.setColumnCount(len(headers))
        self.ui.tableWidget.setHorizontalHeaderLabels(headers)
        self.ui.tableWidget.setColumnHidden(0, True)  # hide id

    def _load_table(self, data: list | None = None):
        if data is None:
            data = self.controller.list_all()

        self.ui.tableWidget.setRowCount(0)
        for row in data:
            r = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(r)
            self.ui.tableWidget.setItem(r, 0, QTableWidgetItem(str(row.get('id', ''))))
            self.ui.tableWidget.setItem(r, 1, QTableWidgetItem(row.get('codigo') or ''))
            self.ui.tableWidget.setItem(r, 2, QTableWidgetItem(row.get('nombre') or ''))
            self.ui.tableWidget.setItem(r, 3, QTableWidgetItem(str(row.get('moneda') or '')))
            self.ui.tableWidget.setItem(r, 4, QTableWidgetItem(row.get('descripcion') or ''))

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
            'activo': True
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
            return

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

    # ==================== Handlers ====================

    def _on_search(self):
        # Simple filter using provided fields
        try:
            all_items = self.controller.list_all()
            code_q = self.ui.lineEdit.text().strip() if hasattr(self.ui, 'lineEdit') else ''
            name_q = self.ui.lineEdit_2.text().strip() if hasattr(self.ui, 'lineEdit_2') else ''
            moneda_q = self.ui.comboBox.currentText().strip() if hasattr(self.ui, 'comboBox') else ''
            desc_q = self.ui.plainTextEdit.toPlainText().strip() if hasattr(self.ui, 'plainTextEdit') else ''

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
            self.ui.stackedWidget.setCurrentIndex(1)
        except Exception as e:
            QMessageBox.critical(self, self.tr("Error"), str(e))

    def _on_table_double_click(self, row, col):
        try:
            id_item = self.ui.tableWidget.item(row, 0)
            if not id_item:
                return
            tipo_id = int(id_item.text())
            ok = self.controller.load_by_id(tipo_id)
            if ok:
                self._fill_form(self.controller.current)
                self._lock_fields(True)
                self.is_new = False
                self.ui.stackedWidget.setCurrentIndex(0)
        except Exception as e:
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
