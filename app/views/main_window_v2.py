"""
MainWindow v2 - Basada en RedFox SGC
Usa QStackedWidget para módulos dinámicos con barra superior personalizada.
"""

from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QLabel, QPushButton, QFrame, QStackedWidget, 
                               QDateEdit, QMenu, QMenuBar, QToolButton, QMessageBox,
                               QScrollArea, QComboBox, QLineEdit, QSizePolicy)
from PySide6.QtCore import Qt, QDate, Signal, QPropertyAnimation, QEasingCurve, Property, QPoint
from PySide6.QtGui import QFont, QPixmap, QAction, QPainter, QPen, QColor, QBrush, QShortcut, QKeySequence, QIcon


from typing import Optional, Callable
from core.ui_helpers import show_warning, show_info, show_critical, show_question

from core.auth import Session, UserRole
from core.module_manager import ModuleManager, ModuleCategory, Permission


class MainWindowV2(QMainWindow):
    """
    Ventana principal estilo RedFox SGC.
    
    Características:
    - Barra superior negra con logo, shortcuts, usuario, ejercicio
    - QStackedWidget para módulos dinámicos
    - MenuBar con categorías de módulos
    - Sistema de shortcuts rápidos
    """
    
    logout_requested = Signal()
    
    def __init__(self, session: Session):
        super().__init__()
        self.session = session
        self.module_manager = ModuleManager()
        self.module_widgets = {}  # Caché de widgets de módulos
        self.module_access_order = []  # Lista para rastrear orden de acceso (LRU)
        
        # Cargar configuración de caché desde QSettings
        from PySide6.QtCore import QSettings
        settings = QSettings()
        self.max_cached_modules = settings.value("max_cached_modules", 5, type=int)
        
        self.setup_ui()
        self.create_menus()
        self.update_user_info()
    
    def setup_ui(self) -> None:
        """Configura la interfaz principal."""
        self.setWindowTitle(self.tr("Creative ERP - Sistema de Gestión Empresarial"))
        self.setMinimumSize(1400, 800)
        self.resize(1600, 900)  # Tamaño inicial más grande
        
        # Widget central
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(18, 0, 18, 0)
        
        # ========== CONTENEDOR HORIZONTAL: Sidebar + Área de Contenido ==========
        content_layout = QHBoxLayout()
        content_layout.setSpacing(0)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Sidebar izquierda con módulos (llega hasta arriba)
        self.sidebar = self.create_sidebar()
        content_layout.addWidget(self.sidebar)
        
        # ========== ÁREA DE CONTENIDO (derecha): Top Bar + Botones + StackedWidget ==========
        content_area = QWidget()
        content_area_layout = QVBoxLayout()
        content_area_layout.setSpacing(0)
        content_area_layout.setContentsMargins(0, 0, 0, 0)
        
        # Top bar (barra negra) - solo en el área de contenido
        top_bar = self.create_top_bar()
        content_area_layout.addWidget(top_bar)
        
        # StackedWidget para contenido
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("")
        
        # Página inicial (splash/bienvenida)
        welcome_page = self.create_welcome_page()
        self.stacked_widget.addWidget(welcome_page)
        
        content_area_layout.addWidget(self.stacked_widget, 1)  # stretch=1 para que ocupe el espacio restante
        
        content_area.setLayout(content_area_layout)
        content_layout.addWidget(content_area, 1)  # stretch=1 para que ocupe el espacio restante
        
        content_container = QWidget()
        content_container.setLayout(content_layout)
        main_layout.addWidget(content_container)
        
        # ========== PANEL DE AVISOS GLOBAL (superpuesto) ==========
        self.avisos_panel_widget = self.create_global_avisos_panel()
        self.avisos_panel_widget.setParent(content_container)
        self.avisos_panel_widget.raise_()
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        # Barra de estado
        self.statusBar().showMessage(self.get_status_text())

        # Aplicar fondo global igual al del login (#021323) para probar la coherencia visual
        # Usamos QMainWindow selector para que el cambio afecte a toda la ventana
        try:
            self.setStyleSheet("QMainWindow { background: #021323; }")
        except Exception:
            # No fatal si falla el stylesheet
            pass
    
    def create_sidebar(self) -> QFrame:
        """Crea la barra lateral izquierda con módulos disponibles."""
        sidebar = QFrame()
        sidebar.setMinimumWidth(200)
        sidebar.setMaximumWidth(280)
        sidebar.setFrameShape(QFrame.Shape.StyledPanel)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: palette(window);
                border-right: 1px solid palette(mid);
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 10)
        
        # Título de la sidebar
        title = QLabel(self.tr("MÓDULOS"))
        title_font = QFont()
        title_font.setPointSize(11)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("padding: 10px; background-color: palette(dark);")
        layout.addWidget(title)
        
        # Scroll area para los módulos
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # Estilo con scrollbar superpuesta y más estrecha
        scroll.setStyleSheet("""
            QScrollArea { 
                border: none; 
                background-color: transparent; 
            }
            QScrollBar:vertical {
                border: none;
                background: transparent;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: palette(mid);
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: palette(dark);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        
        # Widget contenedor de módulos
        modules_widget = QWidget()
        self.sidebar_modules_container = QVBoxLayout()
        self.sidebar_modules_container.setSpacing(2)
        self.sidebar_modules_container.setContentsMargins(8, 10, 12, 5)  # Más margen derecho para scrollbar
        self.sidebar_modules_container.addStretch()  # Push todo hacia arriba
        modules_widget.setLayout(self.sidebar_modules_container)
        
        scroll.setWidget(modules_widget)
        layout.addWidget(scroll)
        
        # Cargar módulos iniciales
        self.update_sidebar_modules()
        
        sidebar.setLayout(layout)
        return sidebar
    
    def update_sidebar_modules(self, category: Optional[ModuleCategory] = None) -> None:
        """
        Actualiza los módulos mostrados en la sidebar.
        Muestra categorías como tarjetas estilo Odoo.
        """
        # Limpiar widgets existentes (excepto el stretch final)
        while self.sidebar_modules_container.count() > 1:
            item = self.sidebar_modules_container.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        # Obtener módulos disponibles
        user_permissions = self.session.user.get_effective_permissions()
        available_modules = self.module_manager.get_available_modules(user_permissions)
        
        # Agrupar por categoría
        categories = {}
        for module in available_modules:
            cat = module.category
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(module)
        
        # Información de categorías con colores
        category_info = {
            ModuleCategory.VENTAS: {
                "name": self.tr("Ventas"),
                "description": self.tr("Gestión de clientes y facturación"),
                    "icon": ":/PNG/resources/icons/png/Pay.png",
                "color": "#8B5CF6"  # Púrpura
            },
            ModuleCategory.COMPRAS: {
                "name": self.tr("Compras"), 
                "description": self.tr("Proveedores y facturas de compra"),
                "icon": ":/PNG/resources/icons/png/Pay.png",
                "color": "#3B82F6"  # Azul
            },
            ModuleCategory.ALMACEN: {
                "name": self.tr("Almacén"),
                "description": self.tr("Inventario y control de stock"),
                "icon": ":/PNG/resources/icons/png/List.png",
                "color": "#F59E0B"  # Ámbar
            },
            ModuleCategory.FINANCIERO: {
                "name": self.tr("Financiero"),
                "description": self.tr("Contabilidad y tesorería"),
                    "icon": ":/PNG/resources/icons/png/Pay.png",
                "color": "#10B981"  # Verde
            },
            ModuleCategory.PROYECTOS: {
                "name": self.tr("Proyectos"),
                "description": self.tr("Gestión de proyectos creativos"),
                    "icon": ":/PNG/resources/icons/png/List.png",
                "color": "#EC4899"  # Rosa
            },
            ModuleCategory.ADMINISTRACION: {
                "name": self.tr("Administración"),
                "description": self.tr("Configuración y usuarios"),
                    "icon": ":/PNG/resources/icons/png/Edit.png",
                "color": "#6B7280"  # Gris
            }
        }
        
        # Crear tarjetas por categoría
        for cat in [ModuleCategory.VENTAS, ModuleCategory.COMPRAS, 
                   ModuleCategory.ALMACEN, ModuleCategory.FINANCIERO,
                   ModuleCategory.PROYECTOS, ModuleCategory.ADMINISTRACION]:
            
            if cat not in categories:
                continue
            
            info = category_info[cat]
            modules_in_cat = categories[cat]
            
            # Crear tarjeta estilo Odoo
            card = self._create_category_card(
                cat, 
                info['name'],
                info['description'],
                info['icon'],
                info['color'],
                len(modules_in_cat),
                modules_in_cat
            )
            
            self.sidebar_modules_container.insertWidget(
                self.sidebar_modules_container.count() - 1, 
                card
            )
            
            # Espaciado entre tarjetas
            self.sidebar_modules_container.insertSpacing(
                self.sidebar_modules_container.count() - 1, 
                12
            )
    
    def _create_category_card(self, category: ModuleCategory, name: str, 
                             description: str, icon: str, color: str, 
                             module_count: int, modules: list) -> QWidget:
        """
        Crea una tarjeta estilo Odoo para una categoría.
        
        Args:
            category: Categoría del módulo
            name: Nombre de la categoría
            description: Descripción breve
            icon: Emoji del icono
            color: Color de acento (hex)
            module_count: Número de módulos en la categoría
            modules: Lista de módulos
        """
        card = QFrame()
        card.setObjectName("categoryCard")
        card.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Estilo de la tarjeta compatible con dark mode
        card.setStyleSheet(f"""
            QFrame#categoryCard {{
                background-color: palette(base);
                border: 1px solid palette(mid);
                border-radius: 8px;
                padding: 0px;
            }}
            QFrame#categoryCard:hover {{
                background-color: palette(alternate-base);
                border: 1px solid {color};
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 12, 10, 12)
        layout.setSpacing(6)
        
        # Header: Icono + Título
        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)
        
        # Icono con fondo de color
        icon_container = QFrame()
        icon_container.setFixedSize(40, 40)
        icon_container.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 8px;
            }}
        """)
        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        # Support resource path icons (:/...) — otherwise fall back to text
        if icon and isinstance(icon, str) and icon.startswith(':/'):
            icon_label = QLabel()
            try:
                pix = QPixmap(icon)
                if not pix.isNull():
                    icon_label.setPixmap(pix.scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            except Exception:
                # fallback to text representation if something fails
                icon_label = QLabel('')
        else:
            icon_label = QLabel(icon)
            icon_label.setStyleSheet("""
                font-size: 20px;
                background: transparent;
                border: none;
            """)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_layout.addWidget(icon_label)
        
        header_layout.addWidget(icon_container)
        
        # Título y contador
        title_layout = QVBoxLayout()
        title_layout.setSpacing(2)
        
        title_label = QLabel(name)
        title_label.setStyleSheet("""
            font-size: 14pt;
            font-weight: bold;
            color: palette(text);
            background: transparent;
            border: none;
        """)
        title_layout.addWidget(title_label)
        
        count_label = QLabel(f"{module_count} módulo{'s' if module_count != 1 else ''}")
        count_label.setStyleSheet("""
            font-size: 9pt;
            color: palette(mid);
            background: transparent;
            border: none;
        """)
        title_layout.addWidget(count_label)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Descripción
        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("""
            font-size: 10pt;
            color: palette(dark);
            background: transparent;
            border: none;
            padding: 4px 0px;
        """)
        layout.addWidget(desc_label)
        
        # Botón de acción
        action_btn = QPushButton(self.tr("Ver módulos"))
        action_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 10pt;
            }}
            QPushButton:hover {{
                background-color: {self._darken_color(color, 0.1)};
            }}
            QPushButton:pressed {{
                background-color: {self._darken_color(color, 0.2)};
            }}
        """)
        action_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        action_btn.clicked.connect(
            lambda: self.show_category_modules(category, modules)
        )
        
        layout.addWidget(action_btn)
        
        # Hacer toda la tarjeta clickeable
        card.mousePressEvent = lambda event: self.show_category_modules(category, modules)
        
        return card
    
    def _darken_color(self, hex_color: str, factor: float) -> str:
        """
        Oscurece un color hexadecimal.
        
        Args:
            hex_color: Color en formato #RRGGBB
            factor: Factor de oscurecimiento (0.0 - 1.0)
        """
        # Remover #
        hex_color = hex_color.lstrip('#')
        
        # Convertir a RGB
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        # Oscurecer
        r = int(r * (1 - factor))
        g = int(g * (1 - factor))
        b = int(b * (1 - factor))
        
        # Convertir de vuelta a hex
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def create_top_bar(self) -> QFrame:
        """Crea la barra superior negra estilo RedFox."""
        frame = QFrame()
        frame.setMinimumHeight(50)
        frame.setMaximumHeight(50)
        frame.setStyleSheet("background-color: rgb(0, 0, 0);")
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(9, 4, 9, 4)
        layout.setSpacing(5)
        
        # Logo pequeño
        logo_label = QLabel()
        logo_label.setMaximumSize(32, 32)
        logo_label.setStyleSheet("background-color: transparent;")
        # TODO: Cargar logo real
        # logo_label.setPixmap(QPixmap(":/icons/logo.png").scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio))
        layout.addWidget(logo_label)
        
        # Ícono de avisos/mensajes
        avisos_label = QLabel()
        avisos_label.setMaximumSize(40, 32)
        avisos_label.setStyleSheet("background-color: transparent;")
        # TODO: Cargar ícono de mail/avisos
        layout.addWidget(avisos_label)
        
        # Contenedor de botones de módulos
        self.module_buttons_container = QHBoxLayout()
        self.module_buttons_container.setSpacing(3)
        layout.addLayout(self.module_buttons_container)
        
        # Espaciador expansible
        layout.addStretch()
        
        # ========== ZONA DERECHA: Usuario, Empresa, Ejercicio, Bloquear ==========
        
        # Label Usuario/Grupo
        self.user_label = QLabel(self.tr("Usuario"))
        user_font = QFont()
        user_font.setPointSize(10)
        user_font.setBold(True)
        self.user_label.setFont(user_font)
        self.user_label.setStyleSheet("color: rgb(255, 255, 127); background-color: transparent;")
        layout.addWidget(self.user_label)
        
        # Empresa (botón clicable para cambiar)
        self.company_button = QPushButton(self.tr("Empresa"))
        self.company_button.setStyleSheet("""
            color: rgb(255, 255, 127);
            background-color: transparent;
            border: none;
            font-weight: bold;
            padding: 2px 8px;
        """)
        self.company_button.setFlat(True)
        self.company_button.clicked.connect(self.change_company)
        layout.addWidget(self.company_button)
        
        # Selector de ejercicio (año)
        self.year_selector = QDateEdit()
        self.year_selector.setDate(QDate.currentDate())
        self.year_selector.setDisplayFormat("yyyy")
        self.year_selector.setStyleSheet("color: rgb(255, 255, 127); background-color: rgb(30, 30, 30);")
        self.year_selector.setCalendarPopup(False)
        self.year_selector.setMaximumWidth(80)
        self.year_selector.dateChanged.connect(self.on_year_changed)
        layout.addWidget(self.year_selector)
        
        # Botón Bloquear/Salir
        lock_button = QPushButton(self.tr("Bloq."))
        lock_button.setMinimumHeight(27)
        lock_button.setStyleSheet("""
            color: rgb(0, 0, 0);
            background-color: rgb(133, 170, 142);
            border-radius: 3px;
            font-weight: bold;
            padding: 2px 8px;
        """)
        lock_button.clicked.connect(self.lock_or_logout)
        layout.addWidget(lock_button)
        
        frame.setLayout(layout)
        return frame
    
    def create_welcome_page(self) -> QWidget:
        """Crea la página de bienvenida (mostrada al iniciar sin módulos abiertos)."""
        page = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Logo grande
        logo_label = QLabel(self.tr("CREATIVE ERP"))
        logo_font = QFont()
        logo_font.setPointSize(48)
        logo_font.setBold(True)
        logo_label.setFont(logo_font)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_label)
        
        # Subtítulo
        subtitle = QLabel(self.tr("Sistema de Gestión Empresarial"))
        subtitle_font = QFont()
        subtitle_font.setPointSize(14)
        subtitle.setFont(subtitle_font)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(30)
        
        # Información del usuario
        user_info = QLabel(self.tr("Bienvenido, {}").format(self.session.user.username))
        info_font = QFont()
        info_font.setPointSize(12)
        user_info.setFont(info_font)
        user_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(user_info)
        
        if self.session.company_context:
            company_info = QLabel(
                f"{self.session.company_context.group.name} - "
                f"{self.session.company_context.company.nombre_comercial or self.session.company_context.company.nombre_fiscal}"
            )
            company_info.setFont(info_font)
            company_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(company_info)
        
        layout.addSpacing(20)
        
        instructions = QLabel(self.tr("Selecciona un módulo del menú superior para comenzar"))
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(instructions)
        
        page.setLayout(layout)
        return page
    
    def create_menus(self) -> None:
        """Crea el menú principal con categorías de módulos."""
        menubar = self.menuBar()
        
        # Obtener módulos disponibles para el usuario
        user_permissions = self.session.user.get_effective_permissions()
        available_modules = self.module_manager.get_available_modules(user_permissions)
        
        # Agrupar por categoría
        categories = {}
        for module in available_modules:
            cat = module.category
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(module)
        
        # Crear menús por categoría
        category_names = {
            ModuleCategory.VENTAS: self.tr("Ventas"),
            ModuleCategory.COMPRAS: self.tr("Compras"),
            ModuleCategory.ALMACEN: self.tr("Almacén"),
            ModuleCategory.FINANCIERO: self.tr("Financiero"),
            ModuleCategory.PROYECTOS: self.tr("Proyectos"),
            ModuleCategory.ADMINISTRACION: self.tr("Administración")
        }
        
        for category in [ModuleCategory.VENTAS, ModuleCategory.COMPRAS, 
                        ModuleCategory.ALMACEN, ModuleCategory.FINANCIERO,
                        ModuleCategory.PROYECTOS, ModuleCategory.ADMINISTRACION]:
            
            if category not in categories:
                continue
            
            menu = menubar.addMenu(category_names[category])
            
            for module in categories[category]:
                action_text = f"{module.icon} {module.name}".strip()
                action = QAction(action_text, self)
                action.setStatusTip(module.description)
                action.triggered.connect(lambda checked, m=module: self.open_module(m.id))  # type: ignore
                menu.addAction(action)
        
        # Menú Utilidades
        utils_menu = menubar.addMenu(self.tr("Utilidades"))
        
        preferences_action = QAction(self.tr("Preferencias"), self)
        try:
            preferences_action.setIcon(QIcon(":/PNG/resources/icons/png/Edit.png"))
        except Exception:
            pass
        preferences_action.triggered.connect(self.open_preferences)
        utils_menu.addAction(preferences_action)

        # Añadir acceso rápido al Gestor de Módulos (si está disponible para el usuario)
        gestor = None
        for m in available_modules:
            if m.id == 'gestor_modulos':
                gestor = m
                break
        if gestor:
            gestor_action_text = f"{gestor.icon} {gestor.name}".strip()
            gestor_action = QAction(gestor_action_text, self)
            gestor_action.setStatusTip(gestor.description)
            gestor_action.triggered.connect(lambda checked=False: self.open_module('gestor_modulos'))  # type: ignore
            utils_menu.addAction(gestor_action)
        
        utils_menu.addSeparator()

        # Acción administrativa: inicializar BD de una empresa (solo administradores)
        try:
            if self.session.has_permission('empresas', Permission.ADMIN) or self.session.user.role == UserRole.ADMIN:
                init_company_action = QAction(self.tr("Inicializar BD de Empresa..."), self)
                init_company_action.setStatusTip(self.tr("Inicializa el esquema de base de datos para una empresa (acción admin)"))
                init_company_action.triggered.connect(lambda *_: self.open_admin_init_dialog())
                utils_menu.addAction(init_company_action)
        except Exception:
            # En casos de error de permisos, no añadir la acción
            pass
        
        about_action = QAction(self.tr("Acerca de"), self)
        about_action.triggered.connect(self.show_about)
        utils_menu.addAction(about_action)
        
        # Menú Sesión
        session_menu = menubar.addMenu(self.tr("Sesión"))
        
        change_company_action = QAction(self.tr("Cambiar Empresa"), self)
        change_company_action.triggered.connect(self.change_company)
        session_menu.addAction(change_company_action)
        
        session_menu.addSeparator()
        
        logout_action = QAction(self.tr("Cerrar Sesión"), self)
        logout_action.triggered.connect(self.logout_requested.emit)
        session_menu.addAction(logout_action)
    
    def create_global_avisos_panel(self) -> QWidget:
        """Crea el panel de avisos global que está siempre disponible."""
        # Contenedor principal
        container = QWidget()
        container.setFixedWidth(250)
        container.setMinimumHeight(600)  # Altura mínima inicial
        container.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Panel de avisos
        panel = QFrame()
        panel.setObjectName("avisosPanel")
        panel.setFixedWidth(230)
        panel.setMinimumHeight(600)  # Altura mínima inicial
        
        # TODO: Consultar si hay avisos reales en la BD
        has_avisos = False  # Cambiar a True cuando haya avisos
        
        bg_color_rgb = (200, 50, 50) if has_avisos else (70, 130, 180)  # Rojo si hay avisos, azul si no
        border_color_rgb = (150, 30, 30) if has_avisos else (50, 100, 150)
        hover_color_rgb = (220, 80, 80) if has_avisos else (100, 160, 210)
        
        # Para los stylesheets necesitamos el formato rgb()
        bg_color = f"rgb{bg_color_rgb}"
        border_color = f"rgb{border_color_rgb}"
        
        panel.setStyleSheet(f"""
            QFrame#avisosPanel {{
                background-color: {bg_color};
                border-right: 2px solid {border_color};
                border-radius: 0px 10px 10px 0px;
            }}
        """)
        
        panel_layout = QVBoxLayout()
        panel_layout.setContentsMargins(15, 20, 15, 20)
        panel_layout.setSpacing(10)
        
        # Título
        title_label = QLabel(self.tr("AVISOS") if has_avisos else self.tr("Sin Avisos"))
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: white; background: transparent;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        panel_layout.addWidget(title_label)
        
        panel_layout.addSpacing(10)
        
        # Lista de avisos
        no_avisos = QLabel(self.tr("No hay avisos pendientes"))
        no_avisos.setStyleSheet("color: white; background: transparent;")
        no_avisos.setAlignment(Qt.AlignmentFlag.AlignCenter)
        panel_layout.addWidget(no_avisos)
        
        panel_layout.addStretch()
        panel.setLayout(panel_layout)
        
        # Pestaña vertical con texto rotado
        from PySide6.QtGui import QPainterPath
        
        class VerticalTabButton(QWidget):
            def __init__(self, text, bg_color, border_color, hover_color, parent=None):
                super().__init__(parent)
                self.vertical_text = text
                self.bg_color = bg_color
                self.border_color = border_color
                self.hover_color = hover_color
                self.is_hovered = False
                self._click_callback: Optional[Callable[[], None]] = None
                # Configurar para que no tenga fondo por defecto
                self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, False)
                self.setAutoFillBackground(False)
                
            def mousePressEvent(self, event):
                # Emitir señal de click
                if self._click_callback:
                    self._click_callback()
                super().mousePressEvent(event)
                
            def enterEvent(self, event):
                self.is_hovered = True
                self.update()
                super().enterEvent(event)
                
            def leaveEvent(self, event):
                self.is_hovered = False
                self.update()
                super().leaveEvent(event)
                
            def paintEvent(self, event):
                painter = QPainter(self)
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                
                # Color de fondo - crear QColor desde tupla RGB
                if self.is_hovered:
                    bg_color = QColor(*self.hover_color)
                else:
                    bg_color = QColor(*self.bg_color)
                
                # Crear path con bordes redondeados a la derecha
                rect = self.rect()
                radius = 10
                
                from PySide6.QtGui import QPainterPath
                path = QPainterPath()
                path.moveTo(0, 0)
                path.lineTo(rect.width() - radius, 0)
                path.arcTo(rect.width() - radius * 2, 0, radius * 2, radius * 2, 90, -90)
                path.lineTo(rect.width(), rect.height() - radius)
                path.arcTo(rect.width() - radius * 2, rect.height() - radius * 2, radius * 2, radius * 2, 0, -90)
                path.lineTo(0, rect.height())
                path.lineTo(0, 0)
                
                # Rellenar path con color de fondo
                painter.fillPath(path, bg_color)
                
                # Dibujar el borde
                painter.setPen(QPen(QColor(*self.border_color), 1))
                painter.drawPath(path)
                
                # Configurar y dibujar texto
                painter.setPen(QColor("white"))
                font = QFont()
                font.setPointSize(8)
                font.setBold(True)
                painter.setFont(font)
                
                # Guardar estado, rotar y dibujar texto
                painter.save()
                painter.translate(self.width() / 2, self.height() / 2)
                painter.rotate(-90)  # -90 para leer de abajo hacia arriba
                
                # Calcular ancho del texto aproximado
                text_width = len(self.vertical_text) * 6
                painter.drawText(-text_width // 2, 4, self.vertical_text)
                painter.restore()
        
        tab = VerticalTabButton(
            self.tr("AVISOS"),
            bg_color_rgb,
            border_color_rgb,
            hover_color_rgb
        )
        tab.setObjectName("avisosTab")
        tab.setFixedSize(20, 80)
        tab.setCursor(Qt.CursorShape.PointingHandCursor)
        # Asegurar que el fondo se dibuje correctamente
        tab.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, False)
        tab.setAutoFillBackground(False)
        
        # Añadir a layout
        layout.addWidget(panel)
        layout.addWidget(tab)
        container.setLayout(layout)
        
        # Estado del panel
        setattr(panel, '_is_open', False)
        
        # Animación
        panel_animation = QPropertyAnimation(container, b"pos")
        panel_animation.setDuration(600)
        panel_animation.setEasingCurve(QEasingCurve.Type.OutElastic)
        setattr(container, '_animation', panel_animation)
        
        def toggle_panel() -> None:
            if getattr(panel, '_is_open', False):
                # Cerrar
                getattr(container, '_animation').setStartValue(container.pos())
                getattr(container, '_animation').setEndValue(QPoint(-230, container.pos().y()))
                getattr(container, '_animation').start()
                setattr(panel, '_is_open', False)
            else:
                # Abrir
                getattr(container, '_animation').setStartValue(container.pos())
                getattr(container, '_animation').setEndValue(QPoint(0, container.pos().y()))
                getattr(container, '_animation').start()
                setattr(panel, '_is_open', True)
        
        setattr(tab, '_click_callback', toggle_panel)
        
        # Posicionar inicialmente cerrado
        container.move(-230, 0)
        
        # Actualizar posición al redimensionar ventana
        def update_position() -> None:
            parent = container.parent()
            if parent and isinstance(parent, QWidget):
                y_pos = 0
                container.setFixedHeight(parent.height())
                panel.setFixedHeight(parent.height())
                if not getattr(panel, '_is_open', False):
                    container.move(-230, y_pos)
                else:
                    container.move(0, y_pos)
        
        setattr(container, 'update_position', update_position)
        
        # Llamar update_position con un timer para asegurar que el parent exista
        from PySide6.QtCore import QTimer
        QTimer.singleShot(0, update_position)
        
        return container
    
    def resizeEvent(self, event) -> None:
        """Actualizar posiciones de paneles al redimensionar."""
        super().resizeEvent(event)
        if hasattr(self, 'avisos_panel_widget'):
            self.avisos_panel_widget.update_position()  # type: ignore
    
    def open_module(self, module_id: str) -> None:
        """
        Abre un módulo en el stacked widget con gestión de caché LRU.
        
        Si el módulo ya está en caché, lo muestra y actualiza su posición en LRU.
        Si no está en caché, lo crea y gestiona el límite de caché.
        """
        # Si el módulo ya está en caché, simplemente lo muestra
        if module_id in self.module_widgets:
            widget = self.module_widgets[module_id]
            self.stacked_widget.setCurrentWidget(widget)
            
            # Actualizar orden de acceso (mover al final = más reciente)
            if module_id in self.module_access_order:
                self.module_access_order.remove(module_id)
            self.module_access_order.append(module_id)
            
            msg = self.tr("Módulo {} activo").format(module_id)
            self.statusBar().showMessage(f"{self.get_status_text()} | {msg}")
            return
        
        # Verificar si necesitamos liberar memoria (límite de caché alcanzado)
        if len(self.module_widgets) >= self.max_cached_modules:
            self._cleanup_old_modules()
        
        # Crear el widget del módulo (carga bajo demanda)
        module_widget = self.create_module_widget(module_id)
        
        if module_widget:
            self.module_widgets[module_id] = module_widget
            self.module_access_order.append(module_id)
            self.stacked_widget.addWidget(module_widget)
            self.stacked_widget.setCurrentWidget(module_widget)
            
            msg = self.tr("Módulo {} cargado").format(module_id)
            self.statusBar().showMessage(f"{self.get_status_text()} | {msg}")
            
            print(f"Módulos en caché: {len(self.module_widgets)}/{self.max_cached_modules}")
        else:
            show_info(
                self,
                "Módulo en desarrollo",
                f"El módulo '{module_id}' aún no está implementado."
            )

    def open_admin_init_dialog(self) -> None:
        """Abrir diálogo administrativo para inicializar la BD de una empresa."""
        try:
            from app.views.admin_init_company_db import AdminInitCompanyDBDialog
            dialog = AdminInitCompanyDBDialog(self, current_session=self.session)
            dialog.exec()
        except Exception as e:
            show_critical(self, self.tr("Error"), str(e))
    
    def _cleanup_old_modules(self) -> None:
        """
        Libera memoria eliminando el módulo menos recientemente usado (LRU).
        """
        if not self.module_access_order:
            return
        
        # Obtener el módulo menos recientemente usado (primero en la lista)
        oldest_module_id = self.module_access_order[0]
        
        # Remover del stacked widget
        if oldest_module_id in self.module_widgets:
            widget = self.module_widgets[oldest_module_id]
            self.stacked_widget.removeWidget(widget)
            
            # Eliminar el widget para liberar memoria
            widget.deleteLater()
            
            # Remover de la caché
            del self.module_widgets[oldest_module_id]
            self.module_access_order.remove(oldest_module_id)
            
            print(f"Módulo '{oldest_module_id}' eliminado de caché para liberar memoria")
            print(f"Módulos restantes en caché: {len(self.module_widgets)}/{self.max_cached_modules}")
    
    def set_max_cached_modules(self, max_modules: int) -> None:
        """
        Configura el número máximo de módulos a mantener en caché.
        
        Args:
            max_modules: Número máximo de módulos (mínimo 1)
        """
        self.max_cached_modules = max(1, max_modules)
        
        # Si actualmente hay más módulos que el nuevo límite, limpiar
        while len(self.module_widgets) > self.max_cached_modules:
            self._cleanup_old_modules()
        
        print(f"Límite de caché configurado a {self.max_cached_modules} módulos")
    
    def clear_module_cache(self) -> None:
        """
        Limpia completamente la caché de módulos, liberando toda la memoria.
        Útil para liberar recursos cuando el usuario lo solicite.
        """
        # Guardar el módulo actual para no cerrarlo
        current_widget = self.stacked_widget.currentWidget()
        current_module_id = None
        
        # Encontrar el ID del módulo actual
        for module_id, widget in self.module_widgets.items():
            if widget == current_widget:
                current_module_id = module_id
                break
        
        # Limpiar todos los módulos excepto el actual
        modules_to_remove = [mid for mid in self.module_widgets.keys() if mid != current_module_id]
        
        for module_id in modules_to_remove:
            widget = self.module_widgets[module_id]
            self.stacked_widget.removeWidget(widget)
            widget.deleteLater()
            del self.module_widgets[module_id]
            if module_id in self.module_access_order:
                self.module_access_order.remove(module_id)
        
        print(f"Caché de módulos limpiada. Módulos eliminados: {len(modules_to_remove)}")
        print(f"Módulos en caché: {len(self.module_widgets)}/{self.max_cached_modules}")

    
    def create_module_widget(self, module_id: str) -> Optional[QWidget]:
        """
        Crea el widget para un módulo específico con panel lateral derecho superpuesto.
        - Panel derecho: acciones del módulo (verde) - overlay sobre el contenido
        """
        module_info = self.module_manager.get_module(module_id)
        if not module_info:
            return None
        
        # Contenedor principal con layout para que el contenido se expanda
        container = QWidget()
        container.setMinimumSize(800, 600)
        container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Layout principal que permite al contenido expandirse
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # ========== CONTENIDO PRINCIPAL (fondo) ==========
        module_content = self.load_module_view(module_id)
        if not module_content:
            module_content = self.create_placeholder_content(module_info)
        
        # Asegurar que el contenido del módulo se expanda
        module_content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Añadir al layout para que ocupe todo el espacio disponible
        main_layout.addWidget(module_content)
        
        # ========== PANEL DERECHO SUPERPUESTO ==========
        actions_panel = self.create_module_side_panel(module_id, module_info, module_view=module_content)
        actions_panel.setParent(container)
        
        # Función para posicionar el panel superpuesto
        def update_positions() -> None:
            # Panel derecho: actualizar posición
            if hasattr(actions_panel, 'update_position'):
                actions_panel.update_position()  # type: ignore
            
            # Elevar panel sobre el contenido
            actions_panel.raise_()
        
        # Aplicar posiciones iniciales
        # Dar tiempo para que el contenedor tenga las dimensiones correctas
        from PySide6.QtCore import QTimer
        def delayed_update():
            update_positions()
            actions_panel.raise_()
        QTimer.singleShot(100, delayed_update)
        
        # Actualizar al redimensionar
        original_resize = container.resizeEvent
        def on_resize(event) -> None:
            update_positions()
            if original_resize:
                original_resize(event)
        
        container.resizeEvent = on_resize
        
        return container
    
    def _module_id_to_class_name(self, module_id: str, suffix: str = "View") -> str:
        """
        Convierte un module_id a nombre de clase en CamelCase.
        
        Ejemplos:
            clientes -> ClientesView
            gestor_modulos -> GestorModulosView
            facturas_compra -> FacturasCompraView
        """
        # Dividir por guiones bajos y capitalizar cada parte
        parts = module_id.split('_')
        camel_case = ''.join(part.capitalize() for part in parts)
        return f"{camel_case}{suffix}"
    
    def load_module_view(self, module_id: str) -> Optional[QWidget]:
        """
        Intenta cargar dinámicamente la vista de un módulo.
        
        Busca en modules/{module_id}/view.py
        Por ejemplo: modules/clientes/view.py → ClientesView
        """
        try:
            # Todos los módulos usan view.py ahora
            module_name = f"modules.{module_id}.view"
            
            if module_id == 'clientes':
                view_class_name = "ClientesView"
            elif module_id == 'empresas':
                view_class_name = "EmpresasView"
            elif module_id == 'articulos':
                view_class_name = "ArticulosView"
            else:
                # Para otros módulos, usar convención estándar
                view_class_name = self._module_id_to_class_name(module_id, "View")
            
            print(f"Intentando cargar módulo {module_id} desde {module_name}.{view_class_name}")
            module = __import__(module_name, fromlist=[view_class_name])
            view_class = getattr(module, view_class_name)
            
            # Crear instancia de la vista con parámetros necesarios
            if module_id == 'clientes':
                # Importar get_session para obtener la sesión de la base de datos actual
                from core.db import get_session
                current_session = get_session()
                
                # Para ClientesView, pasar la sesión correcta
                view_instance = view_class(session=current_session)
            elif module_id == 'articulos':
                # ArticulosView no requiere sesión en el constructor por ahora, pero es bueno ser explícito
                view_instance = view_class()
            else:
                view_instance = view_class()
            
            return view_instance
            
        except (ImportError, AttributeError) as e:
            print(f"No se pudo cargar módulo {module_id}: {e}")
            import traceback
            traceback.print_exc()
            
            # Mostrar error al usuario si estamos en modo debug o desarrollo
            # Esto ayuda a diagnosticar por qué falla la carga
            show_warning(
                self,
                "Error de carga de módulo",
                f"No se pudo cargar el módulo '{module_id}'.\n\nError: {str(e)}"
            )
            return None

    
    def create_placeholder_content(self, module_info) -> QWidget:
        """Crea un contenido placeholder para módulos sin implementar."""
        content_container = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setSpacing(0)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Título del módulo
        header = QFrame()
        header.setMinimumHeight(60)
        header.setStyleSheet("background-color: palette(light); border-bottom: 1px solid palette(mid);")
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(20, 10, 20, 10)
        
        title = QLabel(f"{module_info.icon} {module_info.name}")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)
        header_layout.addStretch()
        header.setLayout(header_layout)
        
        content_layout.addWidget(header)
        
        # Contenido placeholder
        module_content = QWidget()
        module_content_layout = QVBoxLayout()
        module_content_layout.setContentsMargins(20, 20, 20, 20)
        
        description = QLabel(module_info.description)
        module_content_layout.addWidget(description)
        
        module_content_layout.addSpacing(20)
        
        placeholder = QLabel(self.tr("Este módulo está en desarrollo.\nAquí se cargará la tabla/lista de datos."))
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        module_content_layout.addWidget(placeholder)
        
        module_content_layout.addStretch()
        
        module_content.setLayout(module_content_layout)
        content_layout.addWidget(module_content)
        
        content_container.setLayout(content_layout)
        return content_container
    
    def create_module_side_panel(self, module_id: str, module_info, module_view=None) -> QWidget:
        """
        Crea el panel lateral derecho deslizante con las acciones del módulo.
        
        El panel está oculto por defecto y se despliega al hacer clic en la pestaña.
        """
        # Contenedor principal con layout
        container = QWidget()
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Panel con contenido
        panel = QFrame()
        panel.setObjectName("sidePanel")
        panel.setFixedWidth(230)
        panel.setStyleSheet("""
            QFrame#sidePanel {
                background-color: rgb(133, 170, 142);
                border-left: 2px solid rgb(100, 140, 110);
                border-radius: 10px 0px 0px 10px;
            }
        """)
        
        panel_layout = QVBoxLayout()
        panel_layout.setContentsMargins(15, 20, 15, 20)
        panel_layout.setSpacing(10)
        
        # Imagen/logo superior
        logo_container = QFrame()
        logo_container.setMinimumHeight(80)
        logo_container.setStyleSheet("""
            background-color: white;
            border-radius: 8px;
            border: 2px solid rgb(100, 140, 110);
        """)
        logo_layout = QVBoxLayout()
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Use resource icon for module panel header instead of emoji
        logo_label = QLabel()
        try:
            pix = QPixmap(":/PNG/resources/icons/png/search.png")
            if not pix.isNull():
                logo_label.setPixmap(pix.scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        except Exception:
            logo_label.setText("")
            logo_label.setStyleSheet("font-size: 32px; background: transparent; border: none;")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(logo_label)
        id_label = QLabel(f"ID: {module_info.id.upper()[:3]}")
        id_label.setStyleSheet("background: transparent; border: none; font-size: 9px;")
        id_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(id_label)
        logo_container.setLayout(logo_layout)
        panel_layout.addWidget(logo_container)
        
        # Botón "Limpiar y Refrescar"
        refresh_btn = QPushButton(self.tr("Limpiar y Refrescar"))
        try:
            refresh_btn.setIcon(QIcon(":/PNG/resources/icons/png/down_arrow.png"))
        except Exception:
            pass
        refresh_btn.setMinimumHeight(35)
        refresh_btn.setStyleSheet(self._get_panel_button_style())
        refresh_btn.clicked.connect(lambda: self.on_module_action(module_id, 'refresh'))  # type: ignore
        panel_layout.addWidget(refresh_btn)
        
        # Controles de ordenación y búsqueda
        order_label = QLabel(self.tr("Ordenar por:"))
        order_label.setStyleSheet("color: white; font-weight: bold; background: transparent;")
        panel_layout.addWidget(order_label)
        
        order_combo = QComboBox()
        
        # Configuración dinámica de opciones de búsqueda
        sort_fields = []
        search_placeholder = self.tr("Buscar...")
        
        if module_view and hasattr(module_view, 'get_search_options'):
            try:
                options = module_view.get_search_options()
                if 'sort_fields' in options:
                    # Expecting list of tuples (Label, Value) or just strings
                    raw_fields = options['sort_fields']
                    for field in raw_fields:
                        if isinstance(field, (list, tuple)) and len(field) >= 1:
                            sort_fields.append(field[0]) # Use label
                            # TODO: Store value mapping if needed
                        else:
                            sort_fields.append(str(field))
                
                if 'search_placeholder' in options:
                    search_placeholder = options['search_placeholder']
            except Exception as e:
                print(f"Error getting search options for {module_id}: {e}")
        
        # Fallback defaults if no options provided
        if not sort_fields:
            if module_id == 'articulos': # Fallback legacy
                sort_fields = [self.tr("Descripción"), self.tr("Código"), self.tr("Stock")]
            else:
                sort_fields = [self.tr("Nombre Fiscal"), self.tr("Código"), self.tr("Fecha")]
        
        order_combo.addItems(sort_fields)
        order_combo.setMinimumHeight(30)
        panel_layout.addWidget(order_combo)
        
        mode_label = QLabel(self.tr("Modo:"))
        mode_label.setStyleSheet("color: white; font-weight: bold; background: transparent;")
        panel_layout.addWidget(mode_label)
        
        mode_combo = QComboBox()
        mode_combo.addItems([self.tr("A-Z"), self.tr("Z-A")])
        mode_combo.setMinimumHeight(30)
        panel_layout.addWidget(mode_combo)
        
        search_label = QLabel(self.tr("Búsqueda:"))
        search_label.setStyleSheet("color: white; font-weight: bold; background: transparent;")
        panel_layout.addWidget(search_label)
        
        search_input = QLineEdit()
        search_input.setPlaceholderText(search_placeholder)

        search_input.setMinimumHeight(30)
        search_input.textChanged.connect(lambda text: self.on_search_changed(module_id, text, order_combo.currentText(), mode_combo.currentText()))  # type: ignore
        panel_layout.addWidget(search_input)
        
        # Guardar referencias para posterior uso
        setattr(panel, 'search_input', search_input)
        setattr(panel, 'order_combo', order_combo)
        setattr(panel, 'mode_combo', mode_combo)
        
        # Conectar combos ahora que todos están definidos
        order_combo.currentTextChanged.connect(lambda: self.on_search_changed(module_id, search_input.text(), order_combo.currentText(), mode_combo.currentText()))  # type: ignore
        mode_combo.currentTextChanged.connect(lambda: self.on_search_changed(module_id, search_input.text(), order_combo.currentText(), mode_combo.currentText()))  # type: ignore
        
        panel_layout.addSpacing(20)
        
        # Botones de acción principales
        add_btn = QPushButton(self.tr("Añadir"))
        try:
            add_btn.setIcon(QIcon(":/PNG/resources/icons/png/Add.png"))
        except Exception:
            pass
        add_btn.setMinimumHeight(40)
        add_btn.setStyleSheet(self._get_panel_button_style())
        add_btn.clicked.connect(lambda: self.on_module_action(module_id, 'new'))  # type: ignore
        panel_layout.addWidget(add_btn)
        
        edit_btn = QPushButton(self.tr("Editar"))
        try:
            edit_btn.setIcon(QIcon(":/PNG/resources/icons/png/Edit.png"))
        except Exception:
            pass
        edit_btn.setMinimumHeight(40)
        edit_btn.setStyleSheet(self._get_panel_button_style())
        edit_btn.clicked.connect(lambda: self.on_module_action(module_id, 'edit'))  # type: ignore
        panel_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton(self.tr("Borrar"))
        try:
            delete_btn.setIcon(QIcon(":/PNG/resources/icons/png/delete.png"))
        except Exception:
            pass
        delete_btn.setMinimumHeight(40)
        delete_btn.setStyleSheet(self._get_panel_button_style("#d63031"))
        delete_btn.clicked.connect(lambda: self.on_module_action(module_id, 'delete'))  # type: ignore
        panel_layout.addWidget(delete_btn)

        # Si estamos en un módulo de Administración, añadir acceso directo al Gestor de Módulos
        try:
            if getattr(module_info, 'category', None) == ModuleCategory.ADMINISTRACION:
                gestor_btn = QPushButton(self.tr("Gestor Módulos"))
                try:
                    gestor_btn.setIcon(QIcon(":/PNG/resources/icons/png/List.png"))
                except Exception:
                    pass
                gestor_btn.setMinimumHeight(40)
                gestor_btn.setStyleSheet(self._get_panel_button_style())
                gestor_btn.clicked.connect(lambda checked=False: self.open_module('gestor_modulos'))  # type: ignore
                panel_layout.addWidget(gestor_btn)
        except Exception:
            pass
        
        panel_layout.addStretch()
        
        # Botón Excepciones (abajo)
        exceptions_btn = QPushButton(self.tr("Excepciones"))
        try:
            exceptions_btn.setIcon(QIcon(":/PNG/resources/icons/png/List.png"))
        except Exception:
            pass
        exceptions_btn.setMinimumHeight(40)
        exceptions_btn.setStyleSheet(self._get_panel_button_style())
        exceptions_btn.clicked.connect(lambda: self.on_module_action(module_id, 'exceptions'))  # type: ignore
        panel_layout.addWidget(exceptions_btn)
        
        panel.setLayout(panel_layout)
        
        # Pestaña en un contenedor para alinearla arriba
        tab_container = QWidget()
        tab_container.setFixedWidth(20)
        tab_layout = QVBoxLayout()
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.setSpacing(0)
        
        tab = QPushButton("◀")
        tab.setObjectName("panelTab")
        tab.setFixedSize(20, 80)
        tab.setCursor(Qt.CursorShape.PointingHandCursor)
        tab.setStyleSheet("""
            QPushButton#panelTab {
                background-color: rgb(133, 170, 142);
                border: 2px solid rgb(100, 140, 110);
                border-right: none;
                border-radius: 15px;
                border-top-right-radius: 0px;
                border-bottom-right-radius: 0px;
                color: white;
                font-weight: bold;
                font-size: 16px;
                font-family: "Arial", "DejaVu Sans", sans-serif;
                text-align: center;
                padding: 0px;
            }
            QPushButton#panelTab:hover {
                background-color: rgb(150, 190, 160);
                color: rgb(240, 240, 240);
            }
        """)
        
        tab_layout.addWidget(tab)
        tab_layout.addStretch()  # Empuja el tab hacia arriba
        tab_container.setLayout(tab_layout)
        
        # Añadir al layout (tab primero a la derecha, luego panel a la izquierda)
        layout.addWidget(tab_container)
        layout.addWidget(panel)
        container.setLayout(layout)
        
        # Estado del panel
        setattr(panel, '_is_open', False)
        container.setFixedWidth(250)
        
        # Animación
        panel_animation = QPropertyAnimation(container, b"pos")
        panel_animation.setDuration(600)
        panel_animation.setEasingCurve(QEasingCurve.Type.OutElastic)
        setattr(container, '_animation', panel_animation)
        
        #---------------------------------------------------------------------
        # -          Panel derecho con funciones de búsqueda y acciones
        #---------------------------------------------------------------------
        def toggle_panel() -> None:
            parent = container.parent()
            if not parent or not isinstance(parent, QWidget):
                return
            
            if getattr(panel, '_is_open', False):
                # Cerrar - mover hacia la derecha
                tab.setText("◀")
                getattr(container, '_animation').setStartValue(container.pos())
                # Solo dejar visible la pestaña (20px desde el borde derecho)
                getattr(container, '_animation').setEndValue(QPoint(parent.width() - 20, container.pos().y()))
                getattr(container, '_animation').start()
                setattr(panel, '_is_open', False)
            else:
                # Abrir - mover hacia la izquierda
                tab.setText("▶")
                getattr(container, '_animation').setStartValue(container.pos())
                # Mostrar todo: 250px desde el borde derecho
                getattr(container, '_animation').setEndValue(QPoint(parent.width() - 250, container.pos().y()))
                getattr(container, '_animation').start()
                setattr(panel, '_is_open', True)
                
                # Poner foco en el campo de búsqueda para escribir inmediatamente
                search_input.setFocus()
                search_input.selectAll()
                
                # Cambiar a vista de lista si el módulo lo soporta
                if module_view and hasattr(module_view, 'list'):
                    module_view.list()
                elif module_view and hasattr(module_view, 'show_list'): # Alternative name
                    module_view.show_list()




        
        # Exponer toggle_panel como método del contenedor para uso externo
        setattr(container, 'toggle_panel', toggle_panel)
        
        tab.clicked.connect(toggle_panel)

        
        # Atajos de teclado
        # F1: Alternar panel (Abrir/Cerrar)
        shortcut_f1 = QShortcut(QKeySequence("F1"), container)
        shortcut_f1.activated.connect(toggle_panel)
        # Asegurar que el shortcut funcione en el contexto de la ventana
        shortcut_f1.setContext(Qt.ShortcutContext.WindowShortcut)
        
        # ESC: Cerrar panel (solo si está abierto)
        shortcut_esc = QShortcut(QKeySequence("Esc"), container)
        def close_panel_esc():
            if getattr(panel, '_is_open', False):
                toggle_panel()
        shortcut_esc.activated.connect(close_panel_esc)
        # Asegurar que el shortcut funcione en el contexto de la ventana
        shortcut_esc.setContext(Qt.ShortcutContext.WindowShortcut)
        
        # Actualizar posición al redimensionar y al mostrar

        def update_position() -> None:
            parent = container.parent()
            if parent and isinstance(parent, QWidget) and parent.width() > 0:
                container.setFixedHeight(parent.height())
                panel.setFixedHeight(parent.height())
                # Reposicionar según estado
                if not getattr(panel, '_is_open', False):
                    container.move(parent.width() - 20, 0)
                else:
                    container.move(parent.width() - 250, 0)
        
        setattr(container, 'update_position', update_position)
        
        # Sobrescribir showEvent para posicionar al mostrarse
        original_show = container.showEvent
        def on_show(event) -> None:
            update_position()
            if original_show:
                original_show(event)
        container.showEvent = on_show
        
        container.setStyleSheet("background-color: transparent;")
        return container
    
    def _get_panel_button_style(self, hover_color: str = "#2d3436") -> str:
        """Retorna el estilo CSS para los botones del panel lateral."""
        return f"""
            QPushButton {{
                background-color: {hover_color};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
                text-align: center;
            }}
            QPushButton:hover {{
                background-color: #636e72;
            }}
            QPushButton:pressed {{
                background-color: #2d3436;
            }}
        """
    
    def get_module_actions(self, module_id: str) -> list:
        """
        Retorna las acciones disponibles para un módulo específico.
        
        TODO: Esto debería estar en la definición de cada módulo.
        """
        # Acciones comunes para módulos de gestión
        common_actions = {
            'facturas': [
                {'icon': ':/PNG/resources/icons/png/Add.png', 'label': self.tr('Nueva'), 'action': 'new', 'tooltip': self.tr('Crear nueva factura')},
                {'icon': ':/PNG/resources/icons/png/search.png', 'label': self.tr('Buscar'), 'action': 'search', 'tooltip': self.tr('Buscar facturas')},
                {'icon': ':/PNG/resources/icons/png/List.png', 'label': self.tr('Listado'), 'action': 'list', 'tooltip': self.tr('Ver listado completo')},
                {'icon': ':/PNG/resources/icons/png/Print.png', 'label': self.tr('Imprimir'), 'action': 'print', 'tooltip': self.tr('Imprimir factura')},
                {'icon': ':/PNG/resources/icons/png/Save.png', 'label': self.tr('Exportar'), 'action': 'export', 'tooltip': self.tr('Exportar XML/PDF')},
            ],
            'clientes': [
                {'icon': ':/PNG/resources/icons/png/Add.png', 'label': self.tr('Nuevo'), 'action': 'new', 'tooltip': self.tr('Crear nuevo cliente')},
                {'icon': ':/PNG/resources/icons/png/search.png', 'label': self.tr('Buscar'), 'action': 'search', 'tooltip': self.tr('Buscar clientes')},
                {'icon': ':/PNG/resources/icons/png/List.png', 'label': self.tr('Listado'), 'action': 'list', 'tooltip': self.tr('Ver todos los clientes')},
                {'icon': ':/PNG/resources/icons/png/List.png', 'label': self.tr('Estadísticas'), 'action': 'stats', 'tooltip': self.tr('Estadísticas de clientes')},
            ],
            'productos': [
                {'icon': ':/PNG/resources/icons/png/Add.png', 'label': self.tr('Nuevo'), 'action': 'new', 'tooltip': self.tr('Crear nuevo producto')},
                {'icon': ':/PNG/resources/icons/png/search.png', 'label': self.tr('Buscar'), 'action': 'search', 'tooltip': self.tr('Buscar productos')},
                {'icon': ':/PNG/resources/icons/png/List.png', 'label': self.tr('Inventario'), 'action': 'inventory', 'tooltip': self.tr('Ver inventario')},
                {'icon': ':/PNG/resources/icons/png/List.png', 'label': self.tr('Categorías'), 'action': 'categories', 'tooltip': self.tr('Gestionar categorías')},
            ],
            'proyectos': [
                {'icon': ':/PNG/resources/icons/png/Add.png', 'label': self.tr('Nuevo'), 'action': 'new', 'tooltip': self.tr('Crear nuevo proyecto')},
                {'icon': ':/PNG/resources/icons/png/List.png', 'label': self.tr('Dashboard'), 'action': 'dashboard', 'tooltip': self.tr('Panel de proyectos')},
                {'icon': ':/PNG/resources/icons/png/Calendar.png', 'label': self.tr('Planificación'), 'action': 'planning', 'tooltip': self.tr('Planificar tareas')},
                {'icon': ':/PNG/resources/icons/png/Pay.png', 'label': self.tr('Presupuestos'), 'action': 'budgets', 'tooltip': self.tr('Gestionar presupuestos')},
            ],
        }
        
        # Retornar acciones específicas o genéricas
        return common_actions.get(module_id, [
            {'icon': ':/PNG/resources/icons/png/Add.png', 'label': self.tr('Nuevo'), 'action': 'new'},
            {'icon': ':/PNG/resources/icons/png/search.png', 'label': self.tr('Buscar'), 'action': 'search'},
            {'icon': ':/PNG/resources/icons/png/List.png', 'label': self.tr('Listado'), 'action': 'list'},
        ])
    
    def _find_module_view(self, container: QWidget) -> Optional[QWidget]:
        """
        Encuentra la vista real del módulo dentro del contenedor.
        
        El contenedor tiene:
        - module_content: La vista del módulo (lo que buscamos)
        - actions_panel: El panel lateral verde
        """
        # Buscar entre los hijos del contenedor
        for child in container.findChildren(QWidget):
            # Buscar widgets que tengan métodos típicos de módulos
            if hasattr(child, 'nuevo_cliente') or hasattr(child, 'nuevo') or \
               hasattr(child, 'editar_cliente') or hasattr(child, 'editar') or \
                hasattr(child, 'borrar_cliente') or hasattr(child, 'borrar'):
                return child
        
        return None
    
    def _close_side_panel(self, module_id: str) -> None:
        """
        Cierra el panel lateral de un módulo si está abierto.
        
        Args:
            module_id: ID del módulo cuyo panel se debe cerrar
        """
        if module_id not in self.module_widgets:
            return
        
        module_widget_container = self.module_widgets[module_id]
        
        # Buscar el contenedor del panel lateral (tiene el método toggle_panel)
        for child in module_widget_container.findChildren(QWidget):
            if hasattr(child, 'toggle_panel'):
                # Verificar si el panel está abierto
                panel = child.findChild(QFrame, "sidePanel")
                if panel and getattr(panel, '_is_open', False):
                    # Cerrar el panel
                    child.toggle_panel()
                break
    
    def _call_module_method(self, module_view: QWidget, method_names: list) -> bool:
        """
        Intenta llamar a uno de los métodos de la lista en el módulo.
        
        Args:
            module_view: La vista del módulo
            method_names: Lista de nombres de métodos a intentar (en orden de prioridad)
        
        Returns:
            True si se llamó algún método, False si no
        """
        for method_name in method_names:
            if hasattr(module_view, method_name):
                method = getattr(module_view, method_name)
                if callable(method):
                    try:
                        method()
                        return True
                    except Exception as e:
                        show_critical(
                            self,
                            self.tr("Error"),
                            f"{self.tr('Error al ejecutar')} {method_name}: {str(e)}"
                        )
                        return False
        
        # Si no se encontró ningún método
        show_info(
            self,
            self.tr("No implementado"),
            self.tr("Esta acción aún no está implementada para este módulo")
        )
        return False
    
    def on_search_changed(self, module_id: str, search_text: str, order_by: str, order_mode: str) -> None:
        """Maneja cambios en los controles de búsqueda y filtrado."""
        # Obtener el widget activo del módulo
        if module_id not in self.module_widgets:
            return
        
        module_widget_container = self.module_widgets[module_id]
        # El módulo real está dentro del contenedor, buscarlo
        # Buscar la vista del módulo
        module_view = self._find_module_view(module_widget_container)
        
        if module_view:
            # Si search_text está vacío, obtenerlo del panel
            if not search_text:
                panel = module_widget_container.findChild(QFrame, "sidePanel")
                if panel and hasattr(panel, 'search_input'):
                    search_text = getattr(panel, 'search_input').text()
            
            # Intentar llamar a métodos de búsqueda en orden de preferencia
            # 1. filter_records(text, order_by, order_mode) - El más completo
            if hasattr(module_view, 'filter_records'):
                try:
                    module_view.filter_records(search_text, order_by, order_mode)
                    return
                except TypeError:
                    # Si falla por argumentos, intentar solo con texto
                    module_view.filter_records(search_text)
                    return
            
            # 2. search(text) - Estándar simple
            if hasattr(module_view, 'search'):
                try:
                    # Intentar pasar todos los argumentos si los acepta
                    module_view.search(search_text, order_by, order_mode)
                except TypeError:
                    # Si no acepta ordenación, pasar solo texto
                    module_view.search(search_text)
                return
                
            # 3. filtrar(text) - Español
            if hasattr(module_view, 'filtrar'):
                module_view.filtrar(search_text)
                return
                
            # 4. buscar_clientes(text) - Legacy específico
            if hasattr(module_view, 'buscar_clientes'):
                module_view.buscar_clientes(search_text)
                return

    
    def on_module_action(self, module_id: str, action: str) -> None:
        """Ejecuta una acción específica de un módulo."""
        if action == 'refresh':
            # Limpiar búsqueda y recargar
            if module_id in self.module_widgets:
                module_widget_container = self.module_widgets[module_id]
                panel = module_widget_container.findChild(QFrame, "sidePanel")
                if panel and hasattr(panel, 'search_input'):
                    getattr(panel, 'search_input').clear()
                self.on_search_changed(module_id, "", "Nombre Fiscal", "A-Z")
            show_info(self, self.tr("Refrescar"), f"{self.tr('Actualizando datos de')} {module_id}...")
        
        elif action in ['new', 'edit', 'delete', 'exceptions']:
            # Obtener el widget del módulo
            if module_id not in self.module_widgets:
                return
            
            module_widget_container = self.module_widgets[module_id]
            
            # Buscar la vista del módulo (el widget real, no el contenedor)
            module_view = self._find_module_view(module_widget_container)
            
            if not module_view:
                show_warning(self, self.tr("Error"), self.tr("No se pudo encontrar la vista del módulo"))
                return
            
            # Llamar al método correspondiente según la acción
            if action == 'new':
                self._call_module_method(module_view, ['nuevo_cliente', 'nuevo', 'nuevo_registro', 'on_nuevo_cliente'])
                # Cerrar panel lateral para dar espacio a la edición
                self._close_side_panel(module_id)
            elif action == 'edit':
                self._call_module_method(module_view, ['editar_cliente', 'editar', 'editar_registro', 'on_edit_cliente'])
                # Cerrar panel lateral para dar espacio a la edición
                self._close_side_panel(module_id)
            elif action == 'delete':
                self._call_module_method(module_view, ['borrar_cliente', 'borrar', 'eliminar', 'borrar_registro', 'on_eliminar_cliente'])
            elif action == 'exceptions':
                # Funcionalidad futura
                show_info(self, self.tr("Excepciones"), self.tr("Funcionalidad en desarrollo"))

        
        else:
            show_info(
                self,
                self.tr("Acción del módulo"),
                f"{self.tr('Módulo')}: {module_id}\n{self.tr('Acción')}: {action}\n\n{self.tr('Esta funcionalidad está en desarrollo.')}"
            )
    
    def close_module(self, module_id: str) -> None:
        """
        Cierra un módulo abierto y libera su memoria.
        
        Esto permite mantener la aplicación ligera incluso con muchos módulos disponibles.
        """
        if module_id not in self.module_widgets:
            return
        
        widget = self.module_widgets[module_id]
        
        # Remover del stacked widget
        self.stacked_widget.removeWidget(widget)
        
        # Eliminar del diccionario de widgets
        del self.module_widgets[module_id]
        
        # Liberar memoria explícitamente
        widget.deleteLater()
        
        # Volver a la página de bienvenida si no hay módulos abiertos
        if not self.module_widgets:
            self.stacked_widget.setCurrentIndex(0)
        else:
            # Mostrar el último módulo abierto
            last_module = list(self.module_widgets.values())[-1]
            self.stacked_widget.setCurrentWidget(last_module)
        
        self.statusBar().showMessage(f"Módulo {module_id} cerrado", 2000)
        
        # Forzar recolección de basura (opcional, Python lo hará automáticamente)
        import gc
        gc.collect()
    
    def show_category_modules(self, category: ModuleCategory, modules: list) -> None:
        """
        Muestra los módulos de una categoría como botones en la barra de módulos.
        
        Args:
            category: La categoría seleccionada
            modules: Lista de módulos de esa categoría
        """
        # Limpiar botones existentes
        while self.module_buttons_container.count():
            item = self.module_buttons_container.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        # Agregar botón por cada módulo de la categoría
        for module in modules:
            btn = QPushButton(f"{module.icon} {module.name}")
            btn.setMinimumHeight(40)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: palette(button);
                    color: palette(button-text);
                    border: 1px solid palette(mid);
                    border-radius: 6px;
                    padding: 8px 16px;
                    font-weight: bold;
                    font-size: 11pt;
                }
                QPushButton:hover {
                    background-color: palette(light);
                    border: 1px solid palette(highlight);
                }
                QPushButton:pressed {
                    background-color: palette(dark);
                }
            """)
            btn.clicked.connect(lambda checked=False, m_id=module.id: self.open_module(m_id))  # type: ignore
            
            self.module_buttons_container.addWidget(btn)
    
    def update_shortcuts(self) -> None:
        """
        Actualiza los botones de shortcuts en la barra superior.
        Ya no se usa para módulos abiertos, solo para categorías seleccionadas.
        """
        pass
    
    def update_user_info(self) -> None:
        """Actualiza la información del usuario en la barra superior."""
        self.user_label.setText(f"{self.session.user.username}")
        
        if self.session.company_context:
            company_text = self.session.company_context.company.nombre_comercial or self.session.company_context.company.nombre_fiscal
            self.company_button.setText(f"{company_text}")
        else:
            self.company_button.setText(self.tr("Sin empresa"))
    
    def get_status_text(self) -> str:
        """Genera el texto de la barra de estado."""
        role_names = {
            UserRole.ADMIN: self.tr("Administrador"),
            UserRole.MANAGER: self.tr("Gerente"),
            UserRole.ACCOUNTANT: self.tr("Contable"),
            UserRole.SALES: self.tr("Ventas"),
            UserRole.PROJECT_MANAGER: self.tr("Jefe de Proyecto"),
            UserRole.EMPLOYEE: self.tr("Empleado"),
            UserRole.VIEWER: self.tr("Visor")
        }
        
        role = role_names.get(self.session.user.role, self.tr("Usuario"))
        
        # Obtener normativa fiscal
        from PySide6.QtCore import QSettings
        settings = QSettings()
        fiscal = settings.value("fiscal_country", "fr")
        fiscal_text = self.tr("Francia") if fiscal == "fr" else self.tr("España")
        
        if self.session.company_context:
            return (
                f"{self.tr('Usuario')}: {self.session.user.username} | "
                f"{self.tr('Rol')}: {role} | "
                f"{self.session.company_context.group.name} - "
                f"{self.session.company_context.company.nombre_comercial or self.session.company_context.company.nombre_fiscal} | "
                f"{self.tr('Normativa')}: {fiscal_text}"
            )
        else:
            return f"{self.tr('Usuario')}: {self.session.user.username} | {self.tr('Rol')}: {role} | {self.tr('Normativa')}: {fiscal_text}"
    
    def change_company(self) -> None:
        """Permite cambiar de empresa (volver al login)."""
        # Use test-friendly helper when running under pytest; otherwise show custom dialog
        import os
        if os.environ.get('PYTEST_CURRENT_TEST'):
            reply = show_question(
                self,
                self.tr("Cambiar Empresa"),
                self.tr("¿Desea cambiar de empresa?\n\nSe cerrará la sesión actual."),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
        else:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Question)
            msg.setWindowTitle(self.tr("Cambiar Empresa"))
            msg.setText(self.tr("¿Desea cambiar de empresa?\n\nSe cerrará la sesión actual."))

            btn_yes = msg.addButton(self.tr("Sí"), QMessageBox.ButtonRole.YesRole)
            btn_no = msg.addButton(self.tr("No"), QMessageBox.ButtonRole.NoRole)
            msg.setDefaultButton(btn_no)

            msg.exec()
            reply = msg.clickedButton()

        if reply == QMessageBox.StandardButton.Yes or (hasattr(reply, 'role') and getattr(reply, 'role', None) == QMessageBox.ButtonRole.YesRole):
            self.logout_requested.emit()
    
    def on_year_changed(self, date) -> None:
        """Cuando cambia el año/ejercicio."""
        year = date.year()
        self.statusBar().showMessage(f"Ejercicio cambiado a: {year}", 3000)
        # TODO: Actualizar contexto de ejercicio en sesión
    
    def lock_or_logout(self) -> None:
        """Bloquear o cerrar sesión."""
        # Por ahora, simplemente cerrar sesión
        self.logout_requested.emit()
    
    def open_preferences(self) -> None:
        """Abre ventana de preferencias."""
        show_info(self, self.tr("Preferencias"), self.tr("Ventana de preferencias en desarrollo"))
    
    def show_about(self) -> None:
        """Muestra ventana Acerca de."""
        # Use non-blocking info helper to avoid modal in tests
        show_info(
            self,
            self.tr("Acerca de Creative ERP"),
            self.tr("<h2>Creative ERP</h2><p>Sistema de Gestión Empresarial</p>"
                    "<p>Versión 2.0 - Python/Qt6</p><p>© 2025 ArtStudio3D</p>")
        )
    
    def closeEvent(self, event) -> None:
        """
        Maneja el evento de cierre de la ventana.
        Verifica si hay cambios sin guardar y solicita confirmación al usuario.
        """
        # Verificar si hay módulos con cambios sin guardar
        modules_with_changes = []
        
        for module_id, widget in self.module_widgets.items():
            # Verificar si el widget tiene el método has_unsaved_changes
            if hasattr(widget, 'has_unsaved_changes') and callable(getattr(widget, 'has_unsaved_changes')):
                if widget.has_unsaved_changes():
                    modules_with_changes.append(module_id)
            # Para módulos que están en un contenedor, buscar el widget interno
            elif hasattr(widget, 'findChildren'):
                # Buscar widgets hijos que tengan el método has_unsaved_changes
                for child in widget.findChildren(QWidget):
                    if hasattr(child, 'has_unsaved_changes') and callable(getattr(child, 'has_unsaved_changes')):
                        if child.has_unsaved_changes():
                            modules_with_changes.append(module_id)
                            break
        
        # Si hay cambios sin guardar, mostrar diálogo de confirmación
        if modules_with_changes:
            # Decide on action: for tests use a simplified non-blocking question, otherwise show a full dialog
            action = None  # 'save' | 'discard' | 'cancel'
            import os
            if os.environ.get('PYTEST_CURRENT_TEST'):
                reply = show_question(
                    self,
                    self.tr("Cambios sin guardar"),
                    self.tr("Hay cambios sin guardar en {} módulos").format(len(modules_with_changes)) if len(modules_with_changes) > 1 else self.tr("Hay cambios sin guardar en el módulo: {}").format(modules_with_changes[0]),
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No
                )

                if reply == QMessageBox.StandardButton.Yes:
                    action = 'save'
                else:
                    action = 'discard'
            else:
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setWindowTitle(self.tr("Cambios sin guardar"))

                if len(modules_with_changes) == 1:
                    msg.setText(self.tr("Hay cambios sin guardar en el módulo: {}").format(modules_with_changes[0]))
                else:
                    msg.setText(self.tr("Hay cambios sin guardar en {} módulos").format(len(modules_with_changes)))

                msg.setInformativeText(self.tr("¿Qué desea hacer con los cambios?"))

                # Botones personalizados
                save_btn = msg.addButton(self.tr("Guardar"), QMessageBox.ButtonRole.AcceptRole)
                discard_btn = msg.addButton(self.tr("Descartar"), QMessageBox.ButtonRole.DestructiveRole)
                cancel_btn = msg.addButton(self.tr("Cancelar"), QMessageBox.ButtonRole.RejectRole)

                msg.setDefaultButton(save_btn)
                msg.exec()

                clicked_button = msg.clickedButton()

                if clicked_button == save_btn:
                # Guardar cambios en todos los módulos afectados
                all_saved = True
                for module_id in modules_with_changes:
                    widget = self.module_widgets[module_id]
                    success = False
                    
                    try:
                        # Intentar guardar directamente si el widget tiene el método
                        if hasattr(widget, '_save_changes') and callable(getattr(widget, '_save_changes')):
                            result = widget._save_changes()
                            # Si retorna None, asumimos True por compatibilidad, si retorna bool usamos el valor
                            success = result if result is not None else True
                        # Buscar en widgets hijos
                        elif hasattr(widget, 'findChildren'):
                            for child in widget.findChildren(QWidget):
                                if hasattr(child, '_save_changes') and callable(getattr(child, '_save_changes')):
                                    result = child._save_changes()
                                    success = result if result is not None else True
                                    break
                    except Exception as e:
                        print(f"Error al guardar módulo {module_id}: {e}")
                        success = False
                    
                    if not success:
                        all_saved = False
                        break
                
                if all_saved:
                    # Aceptar el cierre
                    event.accept()
                else:
                    # Cancelar el cierre si hubo error al guardar
                    event.ignore()
                
                elif clicked_button == discard_btn:
                # Descartar cambios y cerrar
                event.accept()
                
                else:  # cancel_btn
                # Cancelar el cierre
                event.ignore()
                # end runtime dialog handling

            # test-mode simplified action handling
            if action == 'save':
                # Guardar cambios en todos los módulos afectados
                all_saved = True
                for module_id in modules_with_changes:
                    widget = self.module_widgets[module_id]
                    success = False
                    try:
                        if hasattr(widget, '_save_changes') and callable(getattr(widget, '_save_changes')):
                            result = widget._save_changes()
                            success = result if result is not None else True
                        elif hasattr(widget, 'findChildren'):
                            for child in widget.findChildren(QWidget):
                                if hasattr(child, '_save_changes') and callable(getattr(child, '_save_changes')):
                                    result = child._save_changes()
                                    success = result if result is not None else True
                                    break
                    except Exception as e:
                        print(f"Error al guardar módulo {module_id}: {e}")
                        success = False
                    if not success:
                        all_saved = False
                        break

                if all_saved:
                    event.accept()
                else:
                    event.ignore()
            elif action == 'discard':
                event.accept()
        else:
            # No hay cambios sin guardar, cerrar normalmente
            event.accept()

