"""
Vista de ficha detallada de cliente.
Muestra los datos completos de un cliente específico.
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, 
                               QLabel, QLineEdit, QPushButton, QGroupBox, 
                               QScrollArea, QFrame, QTextEdit, QDateEdit, 
                               QComboBox, QMessageBox)
from PySide6.QtCore import Qt, Signal, QDate
from PySide6.QtGui import QFont, QPalette

from core.auth import Session
import sys
from pathlib import Path


class ClienteFichaView(QWidget):
    """
    Vista de ficha completa de un cliente.
    
    Muestra todos los datos de un cliente específico de forma detallada
    y permite la edición de los mismos.
    """
    
    # Señal para volver a la lista de clientes
    volver_lista = Signal()
    
    def __init__(self, session: Session, cliente_id: int = None, parent=None):
        super().__init__(parent)
        self.session = session
        self.cliente_id = cliente_id
        self.cliente_data = None
        
        self.setup_ui()
        if cliente_id:
            self.load_cliente(cliente_id)
    
    def setup_ui(self):
        """Configura la interfaz de usuario."""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header con botón de volver
        header_layout = QHBoxLayout()
        
        # Botón volver
        btn_volver = QPushButton("← Volver a Lista")
        btn_volver.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        btn_volver.clicked.connect(self.volver_lista.emit)
        header_layout.addWidget(btn_volver)
        
        header_layout.addStretch()
        
        # Título
        self.title_label = QLabel("Ficha de Cliente")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(self.title_label)
        
        header_layout.addStretch()
        
        # Botón Guardar
        self.btn_guardar = QPushButton("💾 Guardar")
        self.btn_guardar.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        self.btn_guardar.clicked.connect(self.guardar_cliente)
        self.btn_guardar.setEnabled(False)
        header_layout.addWidget(self.btn_guardar)
        
        layout.addLayout(header_layout)
        
        # Scroll area para el contenido
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Widget del contenido del scroll
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        
        # Crear las secciones de datos
        self.create_datos_basicos(scroll_layout)
        self.create_datos_contacto(scroll_layout)
        self.create_datos_fiscales(scroll_layout)
        self.create_observaciones(scroll_layout)
        
        scroll_widget.setLayout(scroll_layout)
        scroll.setWidget(scroll_widget)
        
        layout.addWidget(scroll)
        
        self.setLayout(layout)
        
        # Conectar cambios para habilitar guardar
        self.connect_change_signals()
    
    def create_datos_basicos(self, parent_layout):
        """Crea la sección de datos básicos."""
        group = QGroupBox("📋 Datos Básicos")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                padding-top: 10px;
                margin-top: 6px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
            }
        """)
        
        layout = QFormLayout()
        
        self.txt_codigo = QLineEdit()
        self.txt_codigo.setPlaceholderText("Código del cliente")
        layout.addRow("Código:", self.txt_codigo)
        
        self.txt_nombre_fiscal = QLineEdit()
        self.txt_nombre_fiscal.setPlaceholderText("Nombre fiscal completo")
        layout.addRow("Nombre Fiscal:", self.txt_nombre_fiscal)
        
        self.txt_nombre_comercial = QLineEdit()
        self.txt_nombre_comercial.setPlaceholderText("Nombre comercial")
        layout.addRow("Nombre Comercial:", self.txt_nombre_comercial)
        
        self.cmb_tipo_cliente = QComboBox()
        self.cmb_tipo_cliente.addItems(["Particular", "Empresa", "Autónomo"])
        layout.addRow("Tipo Cliente:", self.cmb_tipo_cliente)
        
        group.setLayout(layout)
        parent_layout.addWidget(group)
    
    def create_datos_contacto(self, parent_layout):
        """Crea la sección de datos de contacto."""
        group = QGroupBox("📞 Datos de Contacto")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                padding-top: 10px;
                margin-top: 6px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
            }
        """)
        
        layout = QFormLayout()
        
        self.txt_telefono1 = QLineEdit()
        self.txt_telefono1.setPlaceholderText("Teléfono principal")
        layout.addRow("Teléfono 1:", self.txt_telefono1)
        
        self.txt_telefono2 = QLineEdit()
        self.txt_telefono2.setPlaceholderText("Teléfono secundario")
        layout.addRow("Teléfono 2:", self.txt_telefono2)
        
        self.txt_email = QLineEdit()
        self.txt_email.setPlaceholderText("correo@ejemplo.com")
        layout.addRow("Email:", self.txt_email)
        
        self.txt_web = QLineEdit()
        self.txt_web.setPlaceholderText("www.ejemplo.com")
        layout.addRow("Web:", self.txt_web)
        
        # Dirección
        self.txt_direccion = QLineEdit()
        self.txt_direccion.setPlaceholderText("Dirección completa")
        layout.addRow("Dirección:", self.txt_direccion)
        
        self.txt_codigo_postal = QLineEdit()
        self.txt_codigo_postal.setPlaceholderText("Código postal")
        layout.addRow("Código Postal:", self.txt_codigo_postal)
        
        self.txt_poblacion = QLineEdit()
        self.txt_poblacion.setPlaceholderText("Ciudad/Población")
        layout.addRow("Población:", self.txt_poblacion)
        
        self.txt_provincia = QLineEdit()
        self.txt_provincia.setPlaceholderText("Provincia")
        layout.addRow("Provincia:", self.txt_provincia)
        
        self.txt_pais = QLineEdit()
        self.txt_pais.setPlaceholderText("País")
        layout.addRow("País:", self.txt_pais)
        
        group.setLayout(layout)
        parent_layout.addWidget(group)
    
    def create_datos_fiscales(self, parent_layout):
        """Crea la sección de datos fiscales."""
        group = QGroupBox("💰 Datos Fiscales")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                padding-top: 10px;
                margin-top: 6px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
            }
        """)
        
        layout = QFormLayout()
        
        self.txt_cif = QLineEdit()
        self.txt_cif.setPlaceholderText("CIF/NIF/SIREN")
        layout.addRow("CIF/NIF/SIREN:", self.txt_cif)
        
        self.date_fecha_alta = QDateEdit()
        self.date_fecha_alta.setDate(QDate.currentDate())
        self.date_fecha_alta.setCalendarPopup(True)
        layout.addRow("Fecha Alta:", self.date_fecha_alta)
        
        group.setLayout(layout)
        parent_layout.addWidget(group)
    
    def create_observaciones(self, parent_layout):
        """Crea la sección de observaciones."""
        group = QGroupBox("📝 Observaciones")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                padding-top: 10px;
                margin-top: 6px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
            }
        """)
        
        layout = QVBoxLayout()
        
        self.txt_observaciones = QTextEdit()
        self.txt_observaciones.setPlaceholderText("Observaciones y notas del cliente...")
        self.txt_observaciones.setMaximumHeight(100)
        layout.addWidget(self.txt_observaciones)
        
        group.setLayout(layout)
        parent_layout.addWidget(group)
    
    def connect_change_signals(self):
        """Conecta las señales de cambio para habilitar el botón guardar."""
        widgets = [
            self.txt_codigo, self.txt_nombre_fiscal, self.txt_nombre_comercial,
            self.txt_telefono1, self.txt_telefono2, self.txt_email, self.txt_web,
            self.txt_direccion, self.txt_codigo_postal, self.txt_poblacion,
            self.txt_provincia, self.txt_pais, self.txt_cif, self.txt_observaciones
        ]
        
        for widget in widgets:
            if hasattr(widget, 'textChanged'):
                widget.textChanged.connect(self.on_data_changed)
        
        self.cmb_tipo_cliente.currentTextChanged.connect(self.on_data_changed)
        self.date_fecha_alta.dateChanged.connect(self.on_data_changed)
    
    def on_data_changed(self):
        """Se ejecuta cuando cambia algún dato."""
        self.btn_guardar.setEnabled(True)
    
    def load_cliente(self, cliente_id: int):
        """Carga los datos de un cliente específico."""
        try:
            # Importar con sys.path configurado
            root_dir = Path(__file__).parent.parent.parent
            sys.path.insert(0, str(root_dir))
            
            from core.db import get_session
            import modules.clientes.models as clientes_models
            Cliente = clientes_models.Cliente
            
            # Obtener cliente desde la BD
            session = get_session()
            cliente = session.query(Cliente).filter(Cliente.id == cliente_id).first()
            
            if cliente:
                self.cliente_data = cliente
                self.populate_form(cliente)
                self.title_label.setText(f"Ficha de Cliente - {cliente.nombre_fiscal or 'Sin nombre'}")
                print(f"✅ Cliente {cliente_id} cargado correctamente")
            else:
                QMessageBox.warning(self, "Error", f"No se encontró el cliente con ID {cliente_id}")
                return
            
            session.close()
            
        except Exception as e:
            print(f"❌ Error al cargar cliente: {e}")
            QMessageBox.critical(self, "Error", f"Error al cargar los datos del cliente:\n{e}")
    
    def populate_form(self, cliente):
        """Rellena el formulario con los datos del cliente."""
        self.txt_codigo.setText(cliente.codigo_cliente or "")
        self.txt_nombre_fiscal.setText(cliente.nombre_fiscal or "")
        self.txt_nombre_comercial.setText(cliente.nombre_comercial or "")
        self.txt_telefono1.setText(cliente.telefono1 or "")
        self.txt_telefono2.setText(cliente.telefono2 or "")
        self.txt_email.setText(cliente.email or "")
        self.txt_web.setText(cliente.web or "")
        self.txt_direccion.setText(cliente.direccion1 or "")  # Usar direccion1
        self.txt_codigo_postal.setText(cliente.cp or "")  # Usar cp
        self.txt_poblacion.setText(cliente.poblacion or "")
        self.txt_provincia.setText(cliente.provincia or "")
        self.txt_pais.setText(cliente.id_pais or "")  # Usar id_pais
        self.txt_cif.setText(cliente.cif_nif_siren or "")
        self.txt_observaciones.setPlainText(cliente.observaciones or "")
        
        if cliente.fecha_alta:
            self.date_fecha_alta.setDate(QDate.fromString(str(cliente.fecha_alta), "yyyy-MM-dd"))
        
        # Resetear el estado de guardado
        self.btn_guardar.setEnabled(False)
    
    def guardar_cliente(self):
        """Guarda los cambios del cliente."""
        try:
            # Importar con sys.path configurado
            root_dir = Path(__file__).parent.parent.parent
            sys.path.insert(0, str(root_dir))
            
            from core.db import get_session
            import modules.clientes.models as clientes_models
            Cliente = clientes_models.Cliente
            
            session = get_session()
            
            if self.cliente_id:
                # Actualizar cliente existente
                cliente = session.query(Cliente).filter(Cliente.id == self.cliente_id).first()
                if not cliente:
                    QMessageBox.warning(self, "Error", "Cliente no encontrado")
                    return
            else:
                # Crear nuevo cliente
                cliente = Cliente()
                session.add(cliente)
            
            # Actualizar datos
            cliente.codigo_cliente = self.txt_codigo.text().strip()
            cliente.nombre_fiscal = self.txt_nombre_fiscal.text().strip()
            cliente.nombre_comercial = self.txt_nombre_comercial.text().strip()
            cliente.telefono1 = self.txt_telefono1.text().strip()
            cliente.telefono2 = self.txt_telefono2.text().strip()
            cliente.email = self.txt_email.text().strip()
            cliente.web = self.txt_web.text().strip()
            cliente.direccion1 = self.txt_direccion.text().strip()  # Usar direccion1
            cliente.cp = self.txt_codigo_postal.text().strip()  # Usar cp
            cliente.poblacion = self.txt_poblacion.text().strip()
            cliente.provincia = self.txt_provincia.text().strip()
            cliente.id_pais = self.txt_pais.text().strip()  # Usar id_pais
            cliente.cif_nif_siren = self.txt_cif.text().strip()
            cliente.observaciones = self.txt_observaciones.toPlainText().strip()
            cliente.fecha_alta = self.date_fecha_alta.date().toPython()
            
            session.commit()
            session.close()
            
            self.btn_guardar.setEnabled(False)
            QMessageBox.information(self, "Éxito", "Cliente guardado correctamente")
            print(f"✅ Cliente {self.cliente_id or 'nuevo'} guardado")
            
        except Exception as e:
            print(f"❌ Error al guardar cliente: {e}")
            QMessageBox.critical(self, "Error", f"Error al guardar el cliente:\n{e}")