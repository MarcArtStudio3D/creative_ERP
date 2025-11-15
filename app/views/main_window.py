"""
Ventana principal de la aplicación.
Muestra el dashboard y gestiona la navegación entre módulos.
"""

from typing import List, Dict
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QLabel, QPushButton, QScrollArea, QFrame, 
                               QGridLayout, QStatusBar, QToolBar, QMessageBox)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction, QIcon, QFont

from core.auth import Session
from core.modules import Module, ModuleManager, ModuleCategory


class MainWindow(QMainWindow):
    """
    Ventana principal del Creative ERP.
    
    Muestra un dashboard con los módulos disponibles para el usuario
    organizados por categorías.
    """
    
    def __init__(self, session: Session, available_modules: List[Module], 
                 module_manager: ModuleManager):
        super().__init__()
        
        self.session = session
        self.available_modules = available_modules
        self.module_manager = module_manager
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz principal."""
        self.setWindowTitle(f"Creative ERP - {self.session.user.full_name}")
        self.resize(1200, 800)
        
        # Crear toolbar
        self.create_toolbar()
        
        # Crear barra de estado
        self.create_status_bar()
        
        # Widget central
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header con bienvenida
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Área de módulos con scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        modules_widget = QWidget()
        modules_layout = QVBoxLayout()
        modules_layout.setSpacing(30)
        
        # Agrupar módulos por categoría
        categorized = self.module_manager.get_modules_by_category(self.available_modules)
        
        # Crear sección para cada categoría
        for category, modules in categorized.items():
            if modules:
                section = self.create_category_section(category, modules)
                modules_layout.addWidget(section)
        
        modules_layout.addStretch()
        modules_widget.setLayout(modules_layout)
        scroll.setWidget(modules_widget)
        
        main_layout.addWidget(scroll)
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
    
    def create_toolbar(self):
        """Crea la barra de herramientas."""
        toolbar = QToolBar("Principal")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        # Acción de configuración
        config_action = QAction("⚙️ Configuración", self)
        config_action.triggered.connect(self.open_settings)
        toolbar.addAction(config_action)
        
        toolbar.addSeparator()
        
        # Acción de ayuda
        help_action = QAction("❓ Ayuda", self)
        help_action.triggered.connect(self.show_help)
        toolbar.addAction(help_action)
        
        toolbar.addSeparator()
        
        # Acción de cerrar sesión
        logout_action = QAction("🚪 Cerrar Sesión", self)
        logout_action.triggered.connect(self.logout)
        toolbar.addAction(logout_action)
    
    def create_status_bar(self):
        """Crea la barra de estado."""
        status = QStatusBar()
        self.setStatusBar(status)
        
        # Info del usuario
        user_info = f"Usuario: {self.session.user.username} | Rol: {self.session.user.role.value}"
        status.showMessage(user_info)
    
    def create_header(self) -> QWidget:
        """Crea el header con bienvenida."""
        header = QFrame()
        header.setFrameShape(QFrame.Shape.StyledPanel)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Título de bienvenida
        welcome = QLabel(f"Bienvenido/a, {self.session.user.full_name}")
        welcome_font = QFont()
        welcome_font.setPointSize(18)
        welcome_font.setBold(True)
        welcome.setFont(welcome_font)
        layout.addWidget(welcome)
        
        # Información del rol
        role_label = QLabel(f"Rol: {self.session.user.role.value.title()}")
        role_font = QFont()
        role_font.setPointSize(11)
        role_label.setFont(role_font)
        layout.addWidget(role_label)
        
        # Info de módulos
        modules_info = QLabel(f"Tienes acceso a {len(self.available_modules)} módulos")
        modules_font = QFont()
        modules_font.setPointSize(10)
        modules_info.setFont(modules_font)
        layout.addWidget(modules_info)
        
        header.setLayout(layout)
        return header
    
    def create_category_section(self, category: ModuleCategory, 
                                modules: List[Module]) -> QWidget:
        """
        Crea una sección para una categoría de módulos.
        
        Args:
            category: Categoría de los módulos
            modules: Lista de módulos en esta categoría
        """
        section = QFrame()
        section.setFrameShape(QFrame.Shape.StyledPanel)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Título de la categoría
        category_title = QLabel(category.value.upper())
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        category_title.setFont(title_font)
        layout.addWidget(category_title)
        
        # Grid de módulos
        grid = QGridLayout()
        grid.setSpacing(15)
        
        # 3 módulos por fila
        for i, module in enumerate(modules):
            row = i // 3
            col = i % 3
            module_card = self.create_module_card(module)
            grid.addWidget(module_card, row, col)
        
        layout.addLayout(grid)
        section.setLayout(layout)
        
        return section
    
    def create_module_card(self, module: Module) -> QWidget:
        """
        Crea una tarjeta para un módulo.
        
        Args:
            module: Módulo a representar
        """
        card = QFrame()
        card.setFrameShape(QFrame.Shape.StyledPanel)
        card.setMinimumHeight(120)
        card.setMaximumWidth(350)
        
        layout = QVBoxLayout()
        
        # Icono y nombre
        header_layout = QHBoxLayout()
        
        icon_label = QLabel(f"📦")  # TODO: usar iconos reales según module.icon
        icon_font = QFont()
        icon_font.setPointSize(24)
        icon_label.setFont(icon_font)
        header_layout.addWidget(icon_label)
        
        name_label = QLabel(module.name)
        name_font = QFont()
        name_font.setPointSize(14)
        name_font.setBold(True)
        name_label.setFont(name_font)
        header_layout.addWidget(name_label)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Descripción
        desc_label = QLabel(module.description)
        desc_label.setWordWrap(True)
        desc_font = QFont()
        desc_font.setPointSize(10)
        desc_label.setFont(desc_font)
        layout.addWidget(desc_label)
        
        layout.addStretch()
        
        # Botón de abrir
        open_btn = QPushButton("Abrir")
        btn_font = QFont()
        btn_font.setBold(True)
        open_btn.setFont(btn_font)
        open_btn.setMinimumHeight(32)
        open_btn.clicked.connect(lambda: self.open_module(module))
        layout.addWidget(open_btn)
        
        card.setLayout(layout)
        
        # Hacer la tarjeta clickeable
        card.mousePressEvent = lambda event: self.open_module(module)
        
        return card
    
    def open_module(self, module: Module):
        """
        Abre un módulo.
        
        Args:
            module: Módulo a abrir
        """
        QMessageBox.information(
            self,
            module.name,
            f"Abriendo módulo: {module.name}\n\n"
            f"ID: {module.id}\n"
            f"Categoría: {module.category.value}\n\n"
            f"(Próximamente se abrirá la vista específica del módulo)"
        )
        
        # TODO: Aquí cargar la vista específica del módulo
        # Por ejemplo:
        # if module.id == "facturas":
        #     from modules.facturas.views import FacturaView
        #     view = FacturaView()
        #     view.show()
    
    def open_settings(self):
        """Abre la ventana de configuración."""
        QMessageBox.information(self, "Configuración", "Ventana de configuración (próximamente)")
    
    def show_help(self):
        """Muestra la ayuda."""
        QMessageBox.information(
            self, 
            "Ayuda",
            "Creative ERP v1.0\n\n"
            "Sistema de gestión para creativos\n\n"
            "Para más información, consulta la documentación:\n"
            "- ARCHITECTURE.md - Arquitectura del sistema\n"
            "- FIXES.md - Guía de correcciones\n"
        )
    
    def logout(self):
        """Cierra la sesión del usuario."""
        reply = QMessageBox.question(
            self,
            "Cerrar Sesión",
            "¿Estás seguro de que quieres cerrar la sesión?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.close()
            # TODO: Volver a mostrar la ventana de login