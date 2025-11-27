from typing import Optional
from PySide6.QtWidgets import QWidget, QMessageBox, QTableView, QHeaderView
from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtSql import QSqlDatabase
import os

from modules.empresas.ui_frmempresas import Ui_FrmEmpresas
from modules.empresas.controller import EmpresasController
from core.models import Empresa
from modules.common.db_consulta_view import DBConsultaView


class EmpresasView(QWidget):
    """Vista de empresas integrada en la ventana principal."""

    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Instanciar controlador
        self.controller = EmpresasController(self)
        
        # Configurar UI
        self.ui = Ui_FrmEmpresas()
        self.ui.setupUi(self)
        
        # Configurar tabla
        self.ui.tableView.setModel(self.controller.model)
        self.ui.tableView.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.ui.tableView.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.ui.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        # Conectar señales de UI
        self.ui.tableView.doubleClicked.connect(self.editar)
        self.ui.btn_guardar_nuevo.clicked.connect(self.guardar)
        self.ui.btn_salir.clicked.connect(self.cancelar)
        # Conectar botón Descartar/Deshacer
        if hasattr(self.ui, 'pushButton'):
            self.ui.pushButton.clicked.connect(self.deshacer)
        
        # Conectar señales del controlador
        self.controller.error_occurred.connect(self.mostrar_error)
        self.controller.operation_success.connect(self.mostrar_exito)
        
        # Cargar datos y mostrar lista
        # Cargar datos y mostrar lista
        self.controller.cargar_empresas()
        
        # Cargar grupos en el combo si existe
        # Cargar grupos en el combo si existe
        if hasattr(self.ui, 'cboGrupoEmpresa'):
            self.controller.llenar_combo_grupos(self.ui.cboGrupoEmpresa)
            
        # Cargar países
        self.cargar_paises()
        
    def cargar_paises(self):
        """Carga los países usando el controlador."""
        # Obtener idioma actual de la aplicación
        locale = QCoreApplication.instance().property("current_locale")
        usar_frances = locale == "fr" if locale else False
        
        try:
            paises = self.controller.obtener_paises()
            
            # Llenar combo cboPais_create
            if hasattr(self.ui, 'cboPais_create'):
                combo = self.ui.cboPais_create
                combo.clear()
                for pais_es, pais_fr in paises:
                    # Mostrar en el idioma apropiado
                    display_name = pais_fr if usar_frances else pais_es
                    # Guardar ambos valores como data (para poder recuperar al guardar/cargar)
                    combo.addItem(display_name, {'es': pais_es, 'fr': pais_fr})
                    
        except Exception as e:
            print(f"Error cargando países: {e}")
        
        # Conectar evento de Enter en campo de código postal
        if hasattr(self.ui, 'txtcp'):
            self.ui.txtcp.returnPressed.connect(self._handle_postal_code_change)
            
        self.ui.stackedWidget.setCurrentIndex(1)  # Mostrar lista por defecto

    def mostrar_error(self, mensaje: str):
        QMessageBox.warning(self, "Error", mensaje)

    def mostrar_exito(self, mensaje: str):
        QMessageBox.information(self, "Éxito", mensaje)

    def _get_selected_id(self) -> Optional[int]:
        sel = self.ui.tableView.selectionModel()
        if not sel.hasSelection():
            return None
        idx = sel.currentIndex()
        try:
            # Usar el modelo del controlador
            return int(self.controller.model.item(idx.row(), 0).text())
        except Exception:
            return None

    def nuevo(self):
        """Prepara el formulario para una nueva empresa."""
        self.controller.nueva_empresa()
        self._limpiar_formulario()
        self.ui.stackedWidget.setCurrentIndex(0)  # Ir al formulario

    def editar(self):
        """Carga la empresa seleccionada en el formulario."""
        id_ = self._get_selected_id()
        if id_ is None:
            QMessageBox.information(self, "Selecciona", "Selecciona una empresa primero.")
            return
            
        empresa = self.controller.obtener_empresa(id_)
        if empresa:
            self._map_to_form(empresa)
            self.ui.stackedWidget.setCurrentIndex(0)  # Ir al formulario

    def borrar(self):
        """Borra la empresa seleccionada."""
        id_ = self._get_selected_id()
        if id_ is None:
            QMessageBox.information(self, "Selecciona", "Selecciona una empresa primero.")
            return
            
        # Obtener nombre para confirmación (opcional, requiere acceso al objeto)
        # Por simplicidad, preguntamos genéricamente o accedemos al modelo
        idx = self.ui.tableView.selectionModel().currentIndex()
        nombre = self.controller.model.item(idx.row(), 2).text()
        
        
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setWindowTitle(self.tr("Confirmar"))
        msg.setText(self.tr("¿Borrar empresa {}?").format(nombre))
        
        btn_yes = msg.addButton(self.tr("Sí"), QMessageBox.ButtonRole.YesRole)
        btn_no = msg.addButton(self.tr("No"), QMessageBox.ButtonRole.NoRole)
        msg.setDefaultButton(btn_no)
        
        msg.exec()
        reply = msg.clickedButton()
        
        if reply == btn_yes:
            self.controller.borrar_empresa(id_)

    def guardar(self):
        """Guarda los cambios del formulario."""
        empresa = self._map_from_form()
        self.controller.guardar_empresa(empresa)
        # No volvemos al listado, nos quedamos en la ficha

    def deshacer(self):
        """Deshace los cambios recargando los datos de la empresa actual."""
        if self.controller.empresa_actual:
            self._map_to_form(self.controller.empresa_actual)
            QMessageBox.information(self, "Deshacer", "Cambios descartados. Datos recargados.")
        else:
            # Si es una nueva empresa, limpiamos el formulario
            self._limpiar_formulario()

    def cancelar(self):
        """Cancela la edición y vuelve a la lista."""
        self.ui.stackedWidget.setCurrentIndex(1)

    def accept(self):
        """Método requerido por Ui_FrmEmpresas (generado para QDialog)."""
        self.cancelar()

    def _limpiar_formulario(self):
        """Limpia los campos del formulario."""
        w = self.ui
        # Limpiar QLineEdits
        for widget_name in dir(w):
            widget = getattr(w, widget_name)
            if hasattr(widget, 'clear') and callable(widget.clear):
                if "txt" in widget_name or "lineEdit" in widget_name:
                    widget.clear()

    def _map_to_form(self, empresa: Empresa):
        """Rellena el formulario con los datos de la empresa."""
        w = self.ui
        try:
            # Datos Generales
            if hasattr(w, 'txtcodigo') and getattr(empresa, 'codigo_empresa', None) is not None:
                w.txtcodigo.setText(str(empresa.codigo_empresa))
            if hasattr(w, 'txtEmpresa'):
                w.txtEmpresa.setText(getattr(empresa, 'nombre_fiscal', '') or '')
            if hasattr(w, 'txtNombreComercial'):
                w.txtNombreComercial.setText(getattr(empresa, 'nombre_comercial', '') or '')
            if hasattr(w, 'txtcif'):
                w.txtcif.setText(getattr(empresa, 'cif_nif', '') or '')
            if hasattr(w, 'txtdireccion1'):
                w.txtdireccion1.setText(getattr(empresa, 'direccion', '') or '')
            if hasattr(w, 'txtcp'):
                w.txtcp.setText(getattr(empresa, 'cp', '') or '')
            if hasattr(w, 'txtpoblacion'):
                w.txtpoblacion.setText(getattr(empresa, 'poblacion', '') or '')
            if hasattr(w, 'txtprovincia'):
                w.txtprovincia.setText(getattr(empresa, 'provincia', '') or '')
            if hasattr(w, 'txttelefono1'):
                w.txttelefono1.setText(getattr(empresa, 'telefono', '') or '')
            if hasattr(w, 'txtcMail'):
                w.txtcMail.setText(getattr(empresa, 'email', '') or '')
            if hasattr(w, 'txtweb'):
                w.txtweb.setText(getattr(empresa, 'web', '') or '')
            
            # Contacto adicional
            if hasattr(w, 'txttelefono2'):
                w.txttelefono2.setText(getattr(empresa, 'telefono_contacto', '') or '')
            if hasattr(w, 'txtMovil'):
                w.txtMovil.setText(getattr(empresa, 'movil_contacto', '') or '')

            # Mapear grupo empresarial
            if hasattr(w, 'cboGrupoEmpresa') and hasattr(empresa, 'group_id'):
                idx = w.cboGrupoEmpresa.findData(empresa.group_id)
                if idx >= 0:
                    w.cboGrupoEmpresa.setCurrentIndex(idx)
                    
            # Mapear País (cboPais_create)
            if hasattr(w, 'cboPais_create') and hasattr(empresa, 'id_pais'):
                # Asumimos que el combo ya está cargado con data={'es':..., 'fr':...}
                # No tenemos el ID del país en el combo, sino nombres. 
                # El modelo tiene id_pais (int). Esto podría requerir ajuste si id_pais es FK.
                # Por ahora, intentamos seleccionar por texto si id_pais fuera nombre, 
                # o si tenemos lógica de conversión.
                # TODO: Revisar si id_pais es int o string en la práctica o si necesitamos mapear ID a nombre.
                pass

            # Datos Fiscales y Forma Jurídica
            if hasattr(w, 'cboFormajuridica'):
                w.cboFormajuridica.setCurrentText(getattr(empresa, 'tipo_sociedad', '') or '')
            
            if hasattr(w, 'chkTVA'):
                w.chkTVA.setChecked(bool(getattr(empresa, 'exento_iva', 0)))
            
            if hasattr(w, 'chkInternacional'):
                w.chkInternacional.setChecked(bool(getattr(empresa, 'intracomunitario', 0)))
                
            if hasattr(w, 'spinPorc_irpf'):
                w.spinPorc_irpf.setValue(float(getattr(empresa, 'porcentaje_retencion', 0.0)))

            # Configuración Base de Datos
            if hasattr(w, 'comboBox'): # Motor BD
                w.comboBox.setCurrentText(getattr(empresa, 'motor_base_datos', 'MariaDB'))
            
            # MariaDB Config
            if hasattr(w, 'txtHostMariaDB'):
                w.txtHostMariaDB.setText(getattr(empresa, 'host_mariadb', '') or '')
            if hasattr(w, 'lineEdit'): # Puerto MariaDB
                w.lineEdit.setText(str(getattr(empresa, 'puerto_mariadb', 3306)))
            if hasattr(w, 'lineEdit_15'): # Nombre BD MariaDB
                w.lineEdit_15.setText(getattr(empresa, 'nombre_base_datos_maria_db', '') or '')
            if hasattr(w, 'txtUsuarioMariaDB'):
                w.txtUsuarioMariaDB.setText(getattr(empresa, 'usuario_mariadb', '') or '')
            if hasattr(w, 'txtPasswordMariaDB'):
                w.txtPasswordMariaDB.setText(getattr(empresa, 'password_mariadb', '') or '')
                
            # PostgreSQL Config
            if hasattr(w, 'txtHostMariaDB_2'):
                w.txtHostMariaDB_2.setText(getattr(empresa, 'host_postgresql', '') or '')
            if hasattr(w, 'lineEdit_17'): # Puerto PG
                w.lineEdit_17.setText(str(getattr(empresa, 'puerto_postgresql', 5432)))
            if hasattr(w, 'lineEdit_16'): # Nombre BD PG
                w.lineEdit_16.setText(getattr(empresa, 'nombre_base_datos_postgresql', '') or '')
            if hasattr(w, 'txtUsuarioMariaDB_2'):
                w.txtUsuarioMariaDB_2.setText(getattr(empresa, 'usuario_postgresql', '') or '')
            if hasattr(w, 'txtPasswordMariaDB_2'):
                w.txtPasswordMariaDB_2.setText(getattr(empresa, 'password_postgresql', '') or '')

            # --- NUEVOS CAMPOS ---
            
            # Divisas y Configuración
            if hasattr(w, 'cboDivisas'):
                w.cboDivisas.setCurrentText(getattr(empresa, 'moneda_predeterminada', 'EUR'))
            if hasattr(w, 'chk_upate_divisas'):
                w.chk_upate_divisas.setChecked(bool(getattr(empresa, 'actualizar_divisas', 0)))
            if hasattr(w, 'chkIRPF'):
                w.chkIRPF.setChecked(bool(getattr(empresa, 'aplicar_irpf', 0)))
            if hasattr(w, 'spinPorc_irpf'):
                w.spinPorc_irpf.setValue(float(getattr(empresa, 'porcentaje_irpf', 0.0)))
            if hasattr(w, 'spinDecimales_create'):
                w.spinDecimales_create.setValue(int(getattr(empresa, 'decimales_totales', 2)))
            if hasattr(w, 'spinDecimales_precios_create'):
                w.spinDecimales_precios_create.setValue(int(getattr(empresa, 'decimales_precios', 2)))

            # Facturación
            if hasattr(w, 'spinDigitos'):
                w.spinDigitos.setValue(int(getattr(empresa, 'digitos_factura', 7)))
            if hasattr(w, 'cboSerie'):
                w.cboSerie.setCurrentText(getattr(empresa, 'serie_factura', '') or '')
            if hasattr(w, 'txtDiaCierre'):
                w.txtDiaCierre.setValue(int(getattr(empresa, 'dia_cierre_ejercicio', 31)))
            if hasattr(w, 'tstMesCierre'):
                w.tstMesCierre.setValue(int(getattr(empresa, 'mes_cierre_ejercicio', 12)))

            # Varios y Artículos
            if hasattr(w, 'chkEnlace_web'):
                w.chkEnlace_web.setChecked(bool(getattr(empresa, 'enlace_web_activo', 0)))
            if hasattr(w, 'chkInternacional'):
                w.chkInternacional.setChecked(bool(getattr(empresa, 'gestion_internacional', 0)))
            if hasattr(w, 'chkAutocodificiar'):
                w.chkAutocodificiar.setChecked(bool(getattr(empresa, 'autocodificar_articulos', 1)))
            if hasattr(w, 'txttamano_codigoart'):
                w.txttamano_codigoart.setValue(int(getattr(empresa, 'tamano_codigo_articulo', 15)))
            if hasattr(w, 'cboTarifa'):
                w.cboTarifa.setCurrentText(getattr(empresa, 'tarifa_predeterminada', '') or '')
            if hasattr(w, 'spinMargen'):
                w.spinMargen.setValue(float(getattr(empresa, 'margen_general', 0.0)))
            if hasattr(w, 'spinMargen_minimo'):
                w.spinMargen_minimo.setValue(float(getattr(empresa, 'margen_minimo', 0.0)))

            # Comentarios
            if hasattr(w, 'txtcCometarioAlbaran'):
                w.txtcCometarioAlbaran.setPlainText(getattr(empresa, 'comentario_albaran', '') or '')
            if hasattr(w, 'txtccomentario_factura'):
                w.txtccomentario_factura.setPlainText(getattr(empresa, 'comentario_factura', '') or '')

            # Horarios
            if hasattr(w, 'txt_horario_primer_dia'): w.txt_horario_primer_dia.setText(getattr(empresa, 'horario_lunes', '') or '')
            if hasattr(w, 'txt_horario_dia_normal'): w.txt_horario_dia_normal.setText(getattr(empresa, 'horario_martes', '') or '')
            if hasattr(w, 'txt_horario_ultimo_dia'): w.txt_horario_ultimo_dia.setText(getattr(empresa, 'horario_miercoles', '') or '')
            if hasattr(w, 'lineEdit_7'): w.lineEdit_7.setText(getattr(empresa, 'horario_jueves', '') or '')
            if hasattr(w, 'lineEdit_8'): w.lineEdit_8.setText(getattr(empresa, 'horario_viernes', '') or '')
            if hasattr(w, 'lineEdit_9'): w.lineEdit_9.setText(getattr(empresa, 'horario_sabado', '') or '')
            if hasattr(w, 'lineEdit_10'): w.lineEdit_10.setText(getattr(empresa, 'horario_domingo', '') or '')

            # Google Calendar
            if hasattr(w, 'lineEdit_11'): w.lineEdit_11.setText(getattr(empresa, 'google_calendar_id', '') or '')
            if hasattr(w, 'lineEdit_12'): w.lineEdit_12.setText(getattr(empresa, 'google_oauth_token', '') or '')
            if hasattr(w, 'lineEdit_13'): w.lineEdit_13.setText(getattr(empresa, 'google_refresh_token', '') or '')
            if hasattr(w, 'lineEdit_14'): w.lineEdit_14.setText(getattr(empresa, 'google_token_expiry', '') or '')

            # Contabilidad
            if hasattr(w, 'chkContabilidad'):
                w.chkContabilidad.setChecked(bool(getattr(empresa, 'activar_contabilidad', 1)))
            
            if hasattr(w, 'txtdigitos_cuentas'): w.txtdigitos_cuentas.setValue(int(getattr(empresa, 'digitos_cuentas_contables', 8)))
            if hasattr(w, 'txtcuentaCliente'): w.txtcuentaCliente.setText(getattr(empresa, 'cuenta_clientes', '') or '')
            if hasattr(w, 'txtcuenta_proveedores'): w.txtcuenta_proveedores.setText(getattr(empresa, 'cuenta_proveedores', '') or '')
            if hasattr(w, 'txtcuenta_acreedores'): w.txtcuenta_acreedores.setText(getattr(empresa, 'cuenta_acreedores', '') or '')
            if hasattr(w, 'txtCuenta_venta_mercaderias'): w.txtCuenta_venta_mercaderias.setText(getattr(empresa, 'cuenta_venta_mercaderias', '') or '')
            if hasattr(w, 'txtCuenta_venta_servicios'): w.txtCuenta_venta_servicios.setText(getattr(empresa, 'cuenta_venta_servicios', '') or '')
            if hasattr(w, 'txtcuenta_cobros'): w.txtcuenta_cobros.setText(getattr(empresa, 'cuenta_cobros', '') or '')
            if hasattr(w, 'txtcuenta_pagos'): w.txtcuenta_pagos.setText(getattr(empresa, 'cuenta_pagos', '') or '')

            # Cuentas IVA
            if hasattr(w, 'ivasoportado1'): w.ivasoportado1.setText(getattr(empresa, 'cuenta_iva_soportado_1', '') or '')
            if hasattr(w, 'ivasoportado2'): w.ivasoportado2.setText(getattr(empresa, 'cuenta_iva_soportado_2', '') or '')
            if hasattr(w, 'ivasoportado3'): w.ivasoportado3.setText(getattr(empresa, 'cuenta_iva_soportado_3', '') or '')
            if hasattr(w, 'ivasoportado4'): w.ivasoportado4.setText(getattr(empresa, 'cuenta_iva_soportado_4', '') or '')

            if hasattr(w, 'ivasoportadore1'): w.ivasoportadore1.setText(getattr(empresa, 'cuenta_iva_soportado_re_1', '') or '')
            if hasattr(w, 'ivasoportadore2'): w.ivasoportadore2.setText(getattr(empresa, 'cuenta_iva_soportado_re_2', '') or '')
            if hasattr(w, 'ivasoportadore3'): w.ivasoportadore3.setText(getattr(empresa, 'cuenta_iva_soportado_re_3', '') or '')
            if hasattr(w, 'ivasoportadore4'): w.ivasoportadore4.setText(getattr(empresa, 'cuenta_iva_soportado_re_4', '') or '')

            if hasattr(w, 'ivarepercutido1'): w.ivarepercutido1.setText(getattr(empresa, 'cuenta_iva_repercutido_1', '') or '')
            if hasattr(w, 'ivarepercutido2'): w.ivarepercutido2.setText(getattr(empresa, 'cuenta_iva_repercutido_2', '') or '')
            if hasattr(w, 'ivarepercutido3'): w.ivarepercutido3.setText(getattr(empresa, 'cuenta_iva_repercutido_3', '') or '')
            if hasattr(w, 'ivarepercutido4'): w.ivarepercutido4.setText(getattr(empresa, 'cuenta_iva_repercutido_4', '') or '')

            if hasattr(w, 'ivarepercutidore1'): w.ivarepercutidore1.setText(getattr(empresa, 'cuenta_iva_repercutido_re_1', '') or '')
            if hasattr(w, 'ivarepercutidore2'): w.ivarepercutidore2.setText(getattr(empresa, 'cuenta_iva_repercutido_re_2', '') or '')
            if hasattr(w, 'ivarepercutidore3'): w.ivarepercutidore3.setText(getattr(empresa, 'cuenta_iva_repercutido_re_3', '') or '')
            if hasattr(w, 'ivarepercutidore4'): w.ivarepercutidore4.setText(getattr(empresa, 'cuenta_iva_repercutido_re_4', '') or '')
            
            # Datos Registrales
            if hasattr(w, 'txtcInscripcion'): w.txtcInscripcion.setText(getattr(empresa, 'inscripcion_registro', '') or '')
            if hasattr(w, 'lineEdit_2'): w.lineEdit_2.setText(getattr(empresa, 'numero_rcs', '') or '')
            if hasattr(w, 'lineEdit_3'): w.lineEdit_3.setText(getattr(empresa, 'siret', '') or '')
            if hasattr(w, 'lineEdit_4'): w.lineEdit_4.setText(getattr(empresa, 'ciudad_rcs', '') or '')
            if hasattr(w, 'lineEdit_5'): w.lineEdit_5.setText(getattr(empresa, 'numero_rm', '') or '')
            if hasattr(w, 'lineEdit_6'): w.lineEdit_6.setText(getattr(empresa, 'ape_naf', '') or '')

        except Exception as e:
            print(f"Error mapping to form: {e}")
            pass

    def _map_from_form(self) -> Empresa:
        """Crea/Actualiza el objeto Empresa con los datos del formulario."""
        # Usar la empresa actual del controlador o crear una nueva
        if self.controller.empresa_actual is None:
            empresa = Empresa()
        else:
            empresa = self.controller.empresa_actual
            
        w = self.ui
        
        try:
            # Datos Generales
            if hasattr(w, 'txtcodigo'):
                empresa.codigo_empresa = w.txtcodigo.text()
            if hasattr(w, 'txtEmpresa'):
                empresa.nombre_fiscal = w.txtEmpresa.text()
            if hasattr(w, 'txtNombreComercial'):
                empresa.nombre_comercial = w.txtNombreComercial.text()
            if hasattr(w, 'txtcif'):
                empresa.cif_nif = w.txtcif.text()
            if hasattr(w, 'txtdireccion1'):
                empresa.direccion = w.txtdireccion1.text()
            if hasattr(w, 'txtcp'):
                empresa.cp = w.txtcp.text()
            if hasattr(w, 'txtpoblacion'):
                empresa.poblacion = w.txtpoblacion.text()
            if hasattr(w, 'txtprovincia'):
                empresa.provincia = w.txtprovincia.text()
            if hasattr(w, 'txttelefono1'):
                empresa.telefono = w.txttelefono1.text()
            if hasattr(w, 'txtcMail'):
                empresa.email = w.txtcMail.text()
            if hasattr(w, 'txtweb'):
                empresa.web = w.txtweb.text()
            
            # Contacto adicional
            if hasattr(w, 'txttelefono2'):
                empresa.telefono_contacto = w.txttelefono2.text()
            if hasattr(w, 'txtMovil'):
                empresa.movil_contacto = w.txtMovil.text()

            # Mapear grupo empresarial
            if hasattr(w, 'cboGrupoEmpresa'):
                group_id = w.cboGrupoEmpresa.currentData()
                if group_id:
                    empresa.group_id = int(group_id)
            
            # Mapear País (TODO: Resolver ID vs Texto)
            # Por ahora no guardamos id_pais desde el combo porque falta lógica de ID
            
            # Datos Fiscales y Forma Jurídica
            if hasattr(w, 'cboFormajuridica'):
                empresa.tipo_sociedad = w.cboFormajuridica.currentText()
            
            if hasattr(w, 'chkTVA'):
                empresa.exento_iva = 1 if w.chkTVA.isChecked() else 0
            
            if hasattr(w, 'chkInternacional'):
                empresa.intracomunitario = 1 if w.chkInternacional.isChecked() else 0
                
            if hasattr(w, 'spinPorc_irpf'):
                empresa.porcentaje_retencion = w.spinPorc_irpf.value()

            # Configuración Base de Datos
            if hasattr(w, 'comboBox'): # Motor BD
                empresa.motor_base_datos = w.comboBox.currentText()
            
            # MariaDB Config
            if hasattr(w, 'txtHostMariaDB'):
                empresa.host_mariadb = w.txtHostMariaDB.text()
            if hasattr(w, 'lineEdit'): # Puerto MariaDB
                try:
                    empresa.puerto_mariadb = int(w.lineEdit.text())
                except ValueError:
                    empresa.puerto_mariadb = 3306
            if hasattr(w, 'lineEdit_15'): # Nombre BD MariaDB
                empresa.nombre_base_datos_maria_db = w.lineEdit_15.text()
            if hasattr(w, 'txtUsuarioMariaDB'):
                empresa.usuario_mariadb = w.txtUsuarioMariaDB.text()
            if hasattr(w, 'txtPasswordMariaDB'):
                empresa.password_mariadb = w.txtPasswordMariaDB.text()
                
            # PostgreSQL Config
            if hasattr(w, 'txtHostMariaDB_2'):
                empresa.host_postgresql = w.txtHostMariaDB_2.text()
            if hasattr(w, 'lineEdit_17'): # Puerto PG
                try:
                    empresa.puerto_postgresql = int(w.lineEdit_17.text())
                except ValueError:
                    empresa.puerto_postgresql = 5432
            if hasattr(w, 'lineEdit_16'): # Nombre BD PG
                empresa.nombre_base_datos_postgresql = w.lineEdit_16.text()
            if hasattr(w, 'txtUsuarioMariaDB_2'):
                empresa.usuario_postgresql = w.txtUsuarioMariaDB_2.text()
            if hasattr(w, 'txtPasswordMariaDB_2'):
                empresa.password_postgresql = w.txtPasswordMariaDB_2.text()

            # --- NUEVOS CAMPOS ---
            
            # Divisas y Configuración
            if hasattr(w, 'cboDivisas'):
                empresa.moneda_predeterminada = w.cboDivisas.currentText()
            if hasattr(w, 'chk_upate_divisas'):
                empresa.actualizar_divisas = 1 if w.chk_upate_divisas.isChecked() else 0
            if hasattr(w, 'chkIRPF'):
                empresa.aplicar_irpf = 1 if w.chkIRPF.isChecked() else 0
            if hasattr(w, 'spinPorc_irpf'):
                empresa.porcentaje_irpf = w.spinPorc_irpf.value()
            if hasattr(w, 'spinDecimales_create'):
                empresa.decimales_totales = w.spinDecimales_create.value()
            if hasattr(w, 'spinDecimales_precios_create'):
                empresa.decimales_precios = w.spinDecimales_precios_create.value()

            # Facturación
            if hasattr(w, 'spinDigitos'):
                empresa.digitos_factura = w.spinDigitos.value()
            if hasattr(w, 'cboSerie'):
                empresa.serie_factura = w.cboSerie.currentText()
            if hasattr(w, 'txtDiaCierre'):
                empresa.dia_cierre_ejercicio = w.txtDiaCierre.value()
            if hasattr(w, 'tstMesCierre'):
                empresa.mes_cierre_ejercicio = w.tstMesCierre.value()

            # Varios y Artículos
            if hasattr(w, 'chkEnlace_web'):
                empresa.enlace_web_activo = 1 if w.chkEnlace_web.isChecked() else 0
            if hasattr(w, 'chkInternacional'):
                empresa.gestion_internacional = 1 if w.chkInternacional.isChecked() else 0
            if hasattr(w, 'chkAutocodificiar'):
                empresa.autocodificar_articulos = 1 if w.chkAutocodificiar.isChecked() else 0
            if hasattr(w, 'txttamano_codigoart'):
                empresa.tamano_codigo_articulo = w.txttamano_codigoart.value()
            if hasattr(w, 'cboTarifa'):
                empresa.tarifa_predeterminada = w.cboTarifa.currentText()
            if hasattr(w, 'spinMargen'):
                empresa.margen_general = w.spinMargen.value()
            if hasattr(w, 'spinMargen_minimo'):
                empresa.margen_minimo = w.spinMargen_minimo.value()

            # Comentarios
            if hasattr(w, 'txtcCometarioAlbaran'):
                empresa.comentario_albaran = w.txtcCometarioAlbaran.toPlainText()
            if hasattr(w, 'txtccomentario_factura'):
                empresa.comentario_factura = w.txtccomentario_factura.toPlainText()

            # Horarios
            if hasattr(w, 'txt_horario_primer_dia'): empresa.horario_lunes = w.txt_horario_primer_dia.text()
            if hasattr(w, 'txt_horario_dia_normal'): empresa.horario_martes = w.txt_horario_dia_normal.text()
            if hasattr(w, 'txt_horario_ultimo_dia'): empresa.horario_miercoles = w.txt_horario_ultimo_dia.text()
            if hasattr(w, 'lineEdit_7'): empresa.horario_jueves = w.lineEdit_7.text()
            if hasattr(w, 'lineEdit_8'): empresa.horario_viernes = w.lineEdit_8.text()
            if hasattr(w, 'lineEdit_9'): empresa.horario_sabado = w.lineEdit_9.text()
            if hasattr(w, 'lineEdit_10'): empresa.horario_domingo = w.lineEdit_10.text()

            # Google Calendar
            if hasattr(w, 'lineEdit_11'): empresa.google_calendar_id = w.lineEdit_11.text()
            if hasattr(w, 'lineEdit_12'): empresa.google_oauth_token = w.lineEdit_12.text()
            if hasattr(w, 'lineEdit_13'): empresa.google_refresh_token = w.lineEdit_13.text()
            if hasattr(w, 'lineEdit_14'): empresa.google_token_expiry = w.lineEdit_14.text()

            # Contabilidad
            if hasattr(w, 'chkContabilidad'):
                empresa.activar_contabilidad = 1 if w.chkContabilidad.isChecked() else 0
            
            if hasattr(w, 'txtdigitos_cuentas'): empresa.digitos_cuentas_contables = w.txtdigitos_cuentas.value()
            if hasattr(w, 'txtcuentaCliente'): empresa.cuenta_clientes = w.txtcuentaCliente.text()
            if hasattr(w, 'txtcuenta_proveedores'): empresa.cuenta_proveedores = w.txtcuenta_proveedores.text()
            if hasattr(w, 'txtcuenta_acreedores'): empresa.cuenta_acreedores = w.txtcuenta_acreedores.text()
            if hasattr(w, 'txtCuenta_venta_mercaderias'): empresa.cuenta_venta_mercaderias = w.txtCuenta_venta_mercaderias.text()
            if hasattr(w, 'txtCuenta_venta_servicios'): empresa.cuenta_venta_servicios = w.txtCuenta_venta_servicios.text()
            if hasattr(w, 'txtcuenta_cobros'): empresa.cuenta_cobros = w.txtcuenta_cobros.text()
            if hasattr(w, 'txtcuenta_pagos'): empresa.cuenta_pagos = w.txtcuenta_pagos.text()

            # Cuentas IVA
            if hasattr(w, 'ivasoportado1'): empresa.cuenta_iva_soportado_1 = w.ivasoportado1.text()
            if hasattr(w, 'ivasoportado2'): empresa.cuenta_iva_soportado_2 = w.ivasoportado2.text()
            if hasattr(w, 'ivasoportado3'): empresa.cuenta_iva_soportado_3 = w.ivasoportado3.text()
            if hasattr(w, 'ivasoportado4'): empresa.cuenta_iva_soportado_4 = w.ivasoportado4.text()

            if hasattr(w, 'ivasoportadore1'): empresa.cuenta_iva_soportado_re_1 = w.ivasoportadore1.text()
            if hasattr(w, 'ivasoportadore2'): empresa.cuenta_iva_soportado_re_2 = w.ivasoportadore2.text()
            if hasattr(w, 'ivasoportadore3'): empresa.cuenta_iva_soportado_re_3 = w.ivasoportadore3.text()
            if hasattr(w, 'ivasoportadore4'): empresa.cuenta_iva_soportado_re_4 = w.ivasoportadore4.text()

            if hasattr(w, 'ivarepercutido1'): empresa.cuenta_iva_repercutido_1 = w.ivarepercutido1.text()
            if hasattr(w, 'ivarepercutido2'): empresa.cuenta_iva_repercutido_2 = w.ivarepercutido2.text()
            if hasattr(w, 'ivarepercutido3'): empresa.cuenta_iva_repercutido_3 = w.ivarepercutido3.text()
            if hasattr(w, 'ivarepercutido4'): empresa.cuenta_iva_repercutido_4 = w.ivarepercutido4.text()

            if hasattr(w, 'ivarepercutidore1'): empresa.cuenta_iva_repercutido_re_1 = w.ivarepercutidore1.text()
            if hasattr(w, 'ivarepercutidore2'): empresa.cuenta_iva_repercutido_re_2 = w.ivarepercutidore2.text()
            if hasattr(w, 'ivarepercutidore3'): empresa.cuenta_iva_repercutido_re_3 = w.ivarepercutidore3.text()
            if hasattr(w, 'ivarepercutidore4'): empresa.cuenta_iva_repercutido_re_4 = w.ivarepercutidore4.text()
            
            # Datos Registrales
            if hasattr(w, 'txtcInscripcion'): empresa.inscripcion_registro = w.txtcInscripcion.text()
            if hasattr(w, 'lineEdit_2'): empresa.numero_rcs = w.lineEdit_2.text()
            if hasattr(w, 'lineEdit_3'): empresa.siret = w.lineEdit_3.text()
            if hasattr(w, 'lineEdit_4'): empresa.ciudad_rcs = w.lineEdit_4.text()
            if hasattr(w, 'lineEdit_5'): empresa.numero_rm = w.lineEdit_5.text()
            if hasattr(w, 'lineEdit_6'): empresa.ape_naf = w.lineEdit_6.text()

        except Exception as e:
            print(f"Error mapping from form: {e}")
            pass
            
        return empresa

    def _handle_postal_code_change(self):
        """Handle postal code changes - lookup city and province using controller"""
        if not hasattr(self.ui, 'txtcp'):
            return
            
        cp = self.ui.txtcp.text().strip()
        if not cp:
            return
            
        try:
            # Get active country from cboPais_create combo
            pais_activo = 'Francia'  # Default
            if hasattr(self.ui, 'cboPais_create'):
                # Get the current text from combo
                pais_texto = self.ui.cboPais_create.currentText()
                if pais_texto:
                    pais_activo = pais_texto
            
            # Use controller to search
            results, db_path, db_config = self.controller.buscar_poblacion(cp, pais_activo)
            
            if not results:
                return
                
            # Unpack config for potential dialog use
            _, table_name, cp_col, city_col, prov_col = db_config
            
            if len(results) == 1:
                # Single result - fill fields directly
                poblacion, provincia = results[0]
                if hasattr(self.ui, 'txtpoblacion'):
                    self.ui.txtpoblacion.setText(poblacion or '')
                if hasattr(self.ui, 'txtprovincia'):
                    self.ui.txtprovincia.setText(provincia or '')
                    
            elif len(results) > 1:
                # Multiple results - show selection dialog
                # Create QSqlDatabase connection to country database
                country_db = QSqlDatabase.addDatabase("QSQLITE", "country_connection_empresas")
                country_db.setDatabaseName(db_path)
                
                if country_db.open():
                    sql = f"""
                        SELECT ROWID, {city_col}, {prov_col} 
                        FROM {table_name} 
                        WHERE {cp_col} = '{cp}' 
                        ORDER BY {city_col}
                    """
                    
                    id_selected, record = DBConsultaView.select_from_sql(
                        parent=self,
                        sql=sql,
                        db=country_db,
                        headers=['ID', self.tr('Población'), self.tr('Provincia')],
                        campos=[city_col],
                        titulo=self.tr('Seleccionar población para CP {cp}').format(cp=cp),
                        tamanos=[0, 250, 200]  # ID (hidden), Población, Provincia
                    )
                    
                    if record and record.count() >= 3:  # Make sure we have all columns
                        poblacion = record.value(1)  # City column
                        provincia = record.value(2)  # Province column
                        
                        if hasattr(self.ui, 'txtpoblacion'):
                            self.ui.txtpoblacion.setText(poblacion or '')
                        if hasattr(self.ui, 'txtprovincia'):
                            self.ui.txtprovincia.setText(provincia or '')
                    
                    country_db.close()
                    QSqlDatabase.removeDatabase("country_connection_empresas")
                        
        except Exception as e:
            # Silently ignore errors to not disrupt user experience
            print(f"Error in postal code lookup: {e}")
            pass
