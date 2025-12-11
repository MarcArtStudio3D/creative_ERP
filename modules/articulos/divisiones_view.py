"""
Vista para Divisiones del Almacén (Secciones, Familias, Subfamilias)
Gestiona la interfaz de usuario y conecta con el controller
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QListWidgetItem, QMessageBox

from core.ui_helpers import show_info, show_question, show_warning
from modules.articulos.divisiones_controller import DivisionesController
from modules.articulos.ui_frmDivisiones import Ui_DlgDivisionesAlmacen


class DivisionesView(QDialog):
    """Vista para gestionar las divisiones del almacén"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_DlgDivisionesAlmacen()
        self.ui.setupUi(self)

        self.controller = DivisionesController()

        # Configurar UI inicial
        self._configurar_ui()
        self._conectar_senales()
        self._cargar_datos_iniciales()

    def _configurar_ui(self):
        """Configura el estado inicial de la UI"""
        # Campos siempre editables
        self.ui.txtcodigo.setReadOnly(False)
        self.ui.txtnombre.setReadOnly(False)

        # Botones de añadir siempre habilitados (se validará al pulsar)
        self.ui.btnAddSeccion.setEnabled(True)
        self.ui.btnAddFamily.setEnabled(False)  # Requiere sección seleccionada
        self.ui.btnAddSub.setEnabled(False)  # Requiere familia seleccionada

        # Botones de actualizar deshabilitados inicialmente
        self.ui.btnActualizarSeccion.setEnabled(False)
        self.ui.btnActualizarFamilia.setEnabled(False)
        self.ui.btnActualizarSubfamilia.setEnabled(False)

        # Botones de borrar deshabilitados inicialmente
        self.ui.btnBorrarSec.setEnabled(False)
        self.ui.btnBorrarFam.setEnabled(False)
        self.ui.btnBorrarSub.setEnabled(False)

        # Botón cerrar siempre habilitado
        self.ui.btnCerrar.setEnabled(True)

        self._actualizar_arbol()

    def _conectar_senales(self):
        """Conecta las señales de los widgets con los slots"""
        # Botones de añadir (Crear nuevo)
        self.ui.btnAddSeccion.clicked.connect(self._on_add_seccion)
        self.ui.btnAddFamily.clicked.connect(self._on_add_familia)
        self.ui.btnAddSub.clicked.connect(self._on_add_subfamilia)

        # Botones de actualizar (Guardar cambios)
        self.ui.btnActualizarSeccion.clicked.connect(self._on_guardar_seccion)
        self.ui.btnActualizarFamilia.clicked.connect(self._on_guardar_familia)
        self.ui.btnActualizarSubfamilia.clicked.connect(self._on_guardar_subfamilia)

        # Botones de borrar
        self.ui.btnBorrarSec.clicked.connect(self._on_borrar_seccion)
        self.ui.btnBorrarFam.clicked.connect(self._on_borrar_familia)
        self.ui.btnBorrarSub.clicked.connect(self._on_borrar_subfamilia)

        # Botón cerrar
        self.ui.btnCerrar.clicked.connect(self.close)

        # Conectar eventos de teclado para mejorar usabilidad
        from PySide6.QtCore import Qt
        from PySide6.QtGui import QKeySequence, QShortcut

        # Escape para limpiar selecciones
        self.escape_shortcut = QShortcut(QKeySequence(Qt.Key_Escape), self)
        self.escape_shortcut.activated.connect(self._limpiar_selecciones)

        # Selección en las listas (Navegación)
        self.ui.listSecciones.itemSelectionChanged.connect(self._on_seccion_selected)
        self.ui.listFamilias.itemSelectionChanged.connect(self._on_familia_selected)
        self.ui.listSubfamilias.itemSelectionChanged.connect(
            self._on_subfamilia_selected
        )

        # Clic en items (Edición / Re-selección)
        self.ui.listSecciones.itemClicked.connect(self._on_seccion_clicked)
        self.ui.listFamilias.itemClicked.connect(self._on_familia_clicked)
        self.ui.listSubfamilias.itemClicked.connect(self._on_subfamilia_clicked)

        # Permitir deselección haciendo clic en área vacía o elemento ya seleccionado
        self.ui.listSecciones.mousePressEvent = self._create_deselect_handler(
            self.ui.listSecciones, self._deseleccionar_seccion
        )
        self.ui.listFamilias.mousePressEvent = self._create_deselect_handler(
            self.ui.listFamilias, self._deseleccionar_familia
        )
        self.ui.listSubfamilias.mousePressEvent = self._create_deselect_handler(
            self.ui.listSubfamilias, self._deseleccionar_subfamilia
        )

    def _cargar_datos_iniciales(self):
        """Carga los datos iniciales en las listas"""
        self._cargar_secciones()

    # ==================== CARGA DE DATOS ====================

    def _cargar_secciones(self):
        """Carga todas las secciones en la lista"""
        self.ui.listSecciones.clear()
        secciones = self.controller.obtener_todas_secciones()

        for seccion in secciones:
            item = QListWidgetItem(
                self.tr("{code} - {name}").format(
                    code=seccion.codigo, name=seccion.seccion
                )
            )
            item.setData(Qt.UserRole, seccion)
            self.ui.listSecciones.addItem(item)

    def _cargar_familias(self):
        """Carga las familias de la sección seleccionada"""
        self.ui.listFamilias.clear()
        familias = self.controller.obtener_familias_seccion_actual()

        for familia in familias:
            item = QListWidgetItem(
                self.tr("{code} - {name}").format(
                    code=familia.codigo, name=familia.familia
                )
            )
            item.setData(Qt.UserRole, familia)
            self.ui.listFamilias.addItem(item)

    def _cargar_subfamilias(self):
        """Carga las subfamilias de la familia seleccionada"""
        self.ui.listSubfamilias.clear()
        subfamilias = self.controller.obtener_subfamilias_familia_actual()

        for subfamilia in subfamilias:
            item = QListWidgetItem(
                self.tr("{code} - {name}").format(
                    code=subfamilia.codigo, name=subfamilia.subfamilia
                )
            )
            item.setData(Qt.UserRole, subfamilia)
            self.ui.listSubfamilias.addItem(item)

    # ==================== EVENTOS DE SELECCIÓN (NAVEGACIÓN) ====================

    def _on_seccion_selected(self):
        """Se ejecuta cuando cambia la selección de sección"""
        items = self.ui.listSecciones.selectedItems()
        if items:
            seccion = items[0].data(Qt.UserRole)
            self.controller.seleccionar_seccion(seccion)
            self._cargar_familias()
            self.ui.listSubfamilias.clear()

            # Cargar datos y habilitar edición
            self._cargar_datos_edicion(seccion.codigo, seccion.seccion, "seccion")

            # Habilitar botones de estructura
            self.ui.btnAddFamily.setEnabled(True)
            self.ui.btnBorrarSec.setEnabled(True)
            self.ui.btnAddSub.setEnabled(False)
            self.ui.btnBorrarFam.setEnabled(False)
            self.ui.btnBorrarSub.setEnabled(False)
        else:
            self.controller.seleccionar_seccion(None)
            self.ui.listFamilias.clear()
            self.ui.listSubfamilias.clear()
            self._limpiar_formulario()
            self.ui.btnAddFamily.setEnabled(False)
            self.ui.btnBorrarSec.setEnabled(False)
            self.ui.btnActualizarSeccion.setEnabled(False)

        self._actualizar_arbol()

    def _on_familia_selected(self):
        """Se ejecuta cuando cambia la selección de familia"""
        items = self.ui.listFamilias.selectedItems()
        if items:
            familia = items[0].data(Qt.UserRole)
            self.controller.seleccionar_familia(familia)
            self._cargar_subfamilias()

            # Cargar datos y habilitar edición
            self._cargar_datos_edicion(familia.codigo, familia.familia, "familia")

            # Habilitar botones de estructura
            self.ui.btnAddSub.setEnabled(True)
            self.ui.btnBorrarFam.setEnabled(True)
            self.ui.btnBorrarSub.setEnabled(False)
        else:
            self.controller.seleccionar_familia(None)
            self.ui.listSubfamilias.clear()
            self.ui.btnAddSub.setEnabled(False)
            self.ui.btnBorrarFam.setEnabled(False)

            # Si hay sección, volver el foco a ella
            if self.ui.listSecciones.selectedItems():
                item = self.ui.listSecciones.selectedItems()[0]
                self._on_seccion_clicked(item)
            else:
                self._limpiar_formulario()

        self._actualizar_arbol()

    def _on_subfamilia_selected(self):
        """Se ejecuta cuando cambia la selección de subfamilia"""
        items = self.ui.listSubfamilias.selectedItems()
        if items:
            subfamilia = items[0].data(Qt.UserRole)
            self.controller.seleccionar_subfamilia(subfamilia)

            # Cargar datos y habilitar edición
            self._cargar_datos_edicion(
                subfamilia.codigo, subfamilia.subfamilia, "subfamilia"
            )

            self.ui.btnBorrarSub.setEnabled(True)
        else:
            self.controller.seleccionar_subfamilia(None)
            self.ui.btnBorrarSub.setEnabled(False)

            # Si hay familia, volver el foco a ella
            if self.ui.listFamilias.selectedItems():
                item = self.ui.listFamilias.selectedItems()[0]
                self._on_familia_clicked(item)
            else:
                self._limpiar_formulario()

        self._actualizar_arbol()

    # ==================== EVENTOS DE CLIC (EDICIÓN) ====================

    def _on_seccion_clicked(self, item):
        """Al hacer clic en una sección (incluso si ya está seleccionada)"""
        if item:  # Verificar que el item no sea None
            seccion = item.data(Qt.UserRole)
            self.controller.tipo_seleccion = "seccion"  # Forzar tipo en controlador
            self._cargar_datos_edicion(seccion.codigo, seccion.seccion, "seccion")

    def _on_familia_clicked(self, item):
        """Al hacer clic en una familia"""
        if item:  # Verificar que el item no sea None
            familia = item.data(Qt.UserRole)
            self.controller.tipo_seleccion = "familia"
            self._cargar_datos_edicion(familia.codigo, familia.familia, "familia")

    def _on_subfamilia_clicked(self, item):
        """Al hacer clic en una subfamilia"""
        if item:  # Verificar que el item no sea None
            subfamilia = item.data(Qt.UserRole)
            self.controller.tipo_seleccion = "subfamilia"
            self._cargar_datos_edicion(
                subfamilia.codigo, subfamilia.subfamilia, "subfamilia"
            )

    def _cargar_datos_edicion(self, codigo, nombre, tipo):
        """Helper para cargar datos en el formulario y gestionar botones de actualización"""
        self.ui.txtcodigo.setText(codigo)
        self.ui.txtnombre.setText(nombre)

        # Gestionar visibilidad de botones de actualización
        self.ui.btnActualizarSeccion.setEnabled(tipo == "seccion")
        self.ui.btnActualizarFamilia.setEnabled(tipo == "familia")
        self.ui.btnActualizarSubfamilia.setEnabled(tipo == "subfamilia")

    # ==================== EVENTOS DE BOTONES (AÑADIR) ====================

    def _on_add_seccion(self):
        """Crear nueva sección con los datos de los campos"""
        codigo = self.ui.txtcodigo.text().strip()
        nombre = self.ui.txtnombre.text().strip()

        exito, mensaje = self.controller.crear_seccion(codigo, nombre)
        if exito:
            self._cargar_secciones()
            self._limpiar_formulario()
            show_info(self, self.tr("Éxito"), self.tr("Sección creada correctamente"))
        else:
            show_warning(self, self.tr("Error"), mensaje)

    def _on_add_familia(self):
        """Crear nueva familia con los datos de los campos"""
        codigo = self.ui.txtcodigo.text().strip()
        nombre = self.ui.txtnombre.text().strip()

        exito, mensaje = self.controller.crear_familia(codigo, nombre)
        if exito:
            self._cargar_familias()
            self._limpiar_formulario()
            # Restaurar selección de sección
            if self.controller.seccion_actual:
                self.ui.txtcodigo.setText(self.controller.seccion_actual['codigo'])
                self.ui.txtnombre.setText(self.controller.seccion_actual['seccion'])
                self.ui.btnActualizarSeccion.setEnabled(True)
            show_info(self, self.tr("Éxito"), self.tr("Familia creada correctamente"))
        else:
            show_warning(self, self.tr("Error"), mensaje)

    def _on_add_subfamilia(self):
        """Crear nueva subfamilia con los datos de los campos"""
        codigo = self.ui.txtcodigo.text().strip()
        nombre = self.ui.txtnombre.text().strip()

        exito, mensaje = self.controller.crear_subfamilia(codigo, nombre)
        if exito:
            self._cargar_subfamilias()
            self._limpiar_formulario()
            # Restaurar selección de familia
            if self.controller.familia_actual:
                self.ui.txtcodigo.setText(self.controller.familia_actual['codigo'])
                self.ui.txtnombre.setText(self.controller.familia_actual['familia'])
                self.ui.btnActualizarFamilia.setEnabled(True)
            show_info(
                self, self.tr("Éxito"), self.tr("Subfamilia creada correctamente")
            )
        else:
            show_warning(self, self.tr("Error"), mensaje)

    # ==================== EVENTOS DE BOTONES (BORRAR) ====================

    def _on_borrar_seccion(self):
        """Borrar la sección seleccionada"""
        if (
            show_question(
                self,
                self.tr("Confirmar"),
                self.tr("¿Borrar sección y todo su contenido?"),
            )
            == QMessageBox.StandardButton.Yes
        ):
            exito, mensaje = self.controller.borrar_seccion_actual()
            if exito:
                self._cargar_secciones()
                self.ui.listFamilias.clear()
                self.ui.listSubfamilias.clear()
                self._limpiar_formulario()
                self._actualizar_arbol()
                self.ui.btnActualizarSeccion.setEnabled(False)
            else:
                show_warning(self, self.tr("Error"), mensaje)

    def _on_borrar_familia(self):
        """Borrar la familia seleccionada"""
        if (
            show_question(
                self,
                self.tr("Confirmar"),
                self.tr("¿Borrar familia y sus subfamilias?"),
            )
            == QMessageBox.StandardButton.Yes
        ):
            exito, mensaje = self.controller.borrar_familia_actual()
            if exito:
                self._cargar_familias()
                self.ui.listSubfamilias.clear()
                self._actualizar_arbol()
                self.ui.btnActualizarFamilia.setEnabled(False)
                # Restaurar datos de sección
                if self.controller.seccion_actual:
                    self.ui.txtcodigo.setText(self.controller.seccion_actual['codigo'])
                    self.ui.txtnombre.setText(self.controller.seccion_actual['seccion'])
                    self.ui.btnActualizarSeccion.setEnabled(True)
            else:
                show_warning(self, self.tr("Error"), mensaje)

    def _on_borrar_subfamilia(self):
        """Borrar la subfamilia seleccionada"""
        if (
            show_question(self, self.tr("Confirmar"), self.tr("¿Borrar subfamilia?"))
            == QMessageBox.StandardButton.Yes
        ):
            exito, mensaje = self.controller.borrar_subfamilia_actual()
            if exito:
                self._cargar_subfamilias()
                self._actualizar_arbol()
                self.ui.btnActualizarSubfamilia.setEnabled(False)
                # Restaurar datos de familia
                if self.controller.familia_actual:
                    self.ui.txtcodigo.setText(self.controller.familia_actual['codigo'])
                    self.ui.txtnombre.setText(self.controller.familia_actual['familia'])
                    self.ui.btnActualizarFamilia.setEnabled(True)
            else:
                show_warning(self, self.tr("Error"), mensaje)

    # ==================== EVENTOS DE BOTONES (ACTUALIZAR) ====================

    def _on_guardar_seccion(self):
        """Actualiza la sección seleccionada"""
        codigo = self.ui.txtcodigo.text().strip()
        nombre = self.ui.txtnombre.text().strip()

        exito, mensaje = self.controller.actualizar_seccion_actual(codigo, nombre)
        if exito:
            self._cargar_secciones()
            show_info(
                self, self.tr("Éxito"), self.tr("Sección actualizada correctamente")
            )
        else:
            show_warning(self, self.tr("Error"), mensaje)

    def _on_guardar_familia(self):
        """Actualiza la familia seleccionada"""
        codigo = self.ui.txtcodigo.text().strip()
        nombre = self.ui.txtnombre.text().strip()

        exito, mensaje = self.controller.actualizar_familia_actual(codigo, nombre)
        if exito:
            self._cargar_familias()
            show_info(
                self, self.tr("Éxito"), self.tr("Familia actualizada correctamente")
            )
        else:
            show_warning(self, self.tr("Error"), mensaje)

    def _on_guardar_subfamilia(self):
        """Actualiza la subfamilia seleccionada"""
        codigo = self.ui.txtcodigo.text().strip()
        nombre = self.ui.txtnombre.text().strip()

        exito, mensaje = self.controller.actualizar_subfamilia_actual(codigo, nombre)
        if exito:
            self._cargar_subfamilias()
            show_info(
                self, self.tr("Éxito"), self.tr("Subfamilia actualizada correctamente")
            )
        else:
            show_warning(self, self.tr("Error"), mensaje)

    # ==================== FUNCIONES AUXILIARES ====================

    def _limpiar_formulario(self):
        """Limpia los campos del formulario"""
        self.ui.txtcodigo.clear()
        self.ui.txtnombre.clear()
        self.ui.txtcodigo.setFocus()

    def _actualizar_arbol(self):
        """Actualiza la etiqueta que muestra la jerarquía seleccionada"""
        arbol_texto = ""
        if self.controller.seccion_actual:
            arbol_texto = self.tr("Sección: {name}").format(
                name=self.controller.seccion_actual['seccion']
            )
            if self.controller.familia_actual:
                arbol_texto += self.tr(" → Familia: {name}").format(
                    name=self.controller.familia_actual['familia']
                )
                if self.controller.subfamilia_actual:
                    arbol_texto += self.tr(" → Subfamilia: {name}").format(
                        name=self.controller.subfamilia_actual['subfamilia']
                    )

        self.ui.lbl_tree.setText(arbol_texto)

    # ==================== FUNCIONES DE DESELECCIÓN ====================

    def _create_deselect_handler(self, list_widget, deselect_function):
        """Crea un manejador de eventos de mouse para permitir deseleccionar"""
        original_mouse_press = list_widget.mousePressEvent

        def mouse_press_handler(event):
            # Verificar si se hizo clic en área vacía
            item = list_widget.itemAt(event.pos())
            if item is None:
                # Clic en área vacía - deseleccionar
                deselect_function()
            else:
                # Clic en item - verificar si ya está seleccionado
                if item.isSelected():
                    # Si el item ya está seleccionado, deseleccionarlo
                    item.setSelected(False)
                    deselect_function()
                else:
                    # Comportamiento normal de selección
                    original_mouse_press(event)

        return mouse_press_handler

    def _deseleccionar_seccion(self):
        """Deselecciona la sección actual"""
        self.ui.listSecciones.clearSelection()
        self.controller.seleccionar_seccion(None)
        self.ui.listFamilias.clear()
        self.ui.listSubfamilias.clear()
        self._limpiar_formulario()

        # Deshabilitar botones relevantes
        self.ui.btnAddFamily.setEnabled(False)
        self.ui.btnBorrarSec.setEnabled(False)
        self.ui.btnActualizarSeccion.setEnabled(False)
        self._actualizar_arbol()

    def _deseleccionar_familia(self):
        """Deselecciona la familia actual"""
        self.ui.listFamilias.clearSelection()
        self.controller.seleccionar_familia(None)
        self.ui.listSubfamilias.clear()

        # Restaurar datos de sección si existe
        if self.controller.seccion_actual:
            self._cargar_datos_edicion(
                self.controller.seccion_actual.codigo,
                self.controller.seccion_actual.seccion,
                "seccion",
            )
        else:
            self._limpiar_formulario()

        # Deshabilitar botones relevantes
        self.ui.btnAddSub.setEnabled(False)
        self.ui.btnBorrarFam.setEnabled(False)
        self.ui.btnActualizarFamilia.setEnabled(False)
        self._actualizar_arbol()

    def _deseleccionar_subfamilia(self):
        """Deselecciona la subfamilia actual"""
        self.ui.listSubfamilias.clearSelection()
        self.controller.seleccionar_subfamilia(None)

        # Restaurar datos de familia si existe
        if self.controller.familia_actual:
            self._cargar_datos_edicion(
                self.controller.familia_actual.codigo,
                self.controller.familia_actual.familia,
                "familia",
            )
        elif self.controller.seccion_actual:
            self._cargar_datos_edicion(
                self.controller.seccion_actual.codigo,
                self.controller.seccion_actual.seccion,
                "seccion",
            )
        else:
            self._limpiar_formulario()

        # Deshabilitar botones relevantes
        self.ui.btnBorrarSub.setEnabled(False)
        self.ui.btnActualizarSubfamilia.setEnabled(False)
        self._actualizar_arbol()

    def _limpiar_selecciones(self):
        """Limpia todas las selecciones (atajo Escape)"""
        self._deseleccionar_seccion()
