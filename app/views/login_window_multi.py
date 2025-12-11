"""
Ventana de login multi-empresa con diseño moderno.
"""

import logging
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from core.auth import AuthenticationManager, User, UserRole
from core.business import CompanyContext
from core.company_manager import company_manager
from core.repositories import BusinessGroupRepository, CompanyRepository, UserRepository


class LoginWindowMultiCompany(QDialog):
    """
    Ventana de login multi-empresa.

    Permite seleccionar:
    - Usuario
    - Grupo empresarial
    - Empresa
    """

    login_successful = Signal(object)  # Emite el CompanyContext

    def __init__(self, auth_manager: AuthenticationManager):
        super().__init__()
        self.auth_manager = auth_manager
        self.setup_ui()
        self.load_demo_data()

        # Ensure password field receives initial focus so the user can type the
        # password immediately without using the mouse.
        # Calling setFocus here is fine because the widget exists and Qt will
        # apply focus when the dialog is shown; it's also safe to call even
        # if the dialog is executed later.
        # calling setFocus in __init__ may not always apply if the dialog is not
        # yet shown — ensure focus is applied when the dialog actually appears
        # by setting focus in showEvent (see below).

    def setup_ui(self):
        """Configura la interfaz basada en la imagen de referencia."""
        self.setWindowTitle(self.tr("Creative ERP - Acceso"))
        # Hacemos la ventana más alta para que el logo grande encaje sin apretar
        self.setFixedSize(540, 820)
        self.setModal(True)

        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(60, 50, 60, 50)

        # Espaciado superior
        main_layout.addSpacing(20)

        # header textual eliminado (usaremos solo el logo grande centrado)
        # dejamos un pequeño margen superior para balance visual
        main_layout.addSpacing(10)

        # ========== LOGO ISOMÉTRICO ==========
        logo_label = QLabel()
        logo_label.setObjectName("loginLogo")
        self.login_logo = logo_label
        try:
            pix = QPixmap(":/PNG/resources/icons/png/LogoCreative.png")
            if not pix.isNull():
                # Escalado para que el ancho del logo coincida con el ancho de los campos
                # disponibles en el layout (anchura total - márgenes principales - padding interno)
                margins = main_layout.contentsMargins()
                available_width = self.width() - (margins.left() + margins.right())
                # input containers usan 15px de padding a izquierda y derecha
                target_width = max(120, available_width - 30)
                logo_label.setPixmap(
                    pix.scaledToWidth(
                        int(target_width), Qt.TransformationMode.SmoothTransformation
                    )
                )
            else:
                # Fallback si no hay logo
                logo_label.setText("🎨")
                logo_label.setStyleSheet("font-size: 80px; background: transparent;")
        except Exception:
            logo_label.setText("🎨")
            logo_label.setStyleSheet("font-size: 80px; background: transparent;")

        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(logo_label)
        main_layout.addSpacing(40)

        # ========== FORMULARIO ==========
        # Usuario con icono
        user_container = QFrame()
        user_container.setObjectName("inputField")
        user_layout = QHBoxLayout(user_container)
        user_layout.setContentsMargins(15, 0, 15, 0)
        user_layout.setSpacing(10)

        user_icon = QLabel("👤")
        user_icon.setStyleSheet(
            "font-size: 20px; color: #95a5a6; background: transparent;"
        )
        user_layout.addWidget(user_icon)

        self.user_combo = QComboBox()
        self.user_combo.setObjectName("loginCombo")
        self.user_combo.setMinimumHeight(50)
        self.user_combo.setPlaceholderText(self.tr("Username"))
        self._setup_combo_popup(self.user_combo)
        user_layout.addWidget(self.user_combo)

        main_layout.addWidget(user_container)
        main_layout.addSpacing(15)

        # Contraseña con icono
        password_container = QFrame()
        password_container.setObjectName("inputField")
        password_layout = QHBoxLayout(password_container)
        password_layout.setContentsMargins(15, 0, 15, 0)
        password_layout.setSpacing(10)

        password_icon = QLabel("🔒")
        password_icon.setStyleSheet(
            "font-size: 20px; color: #95a5a6; background: transparent;"
        )
        password_layout.addWidget(password_icon)

        self.password_input = QLineEdit()
        self.password_input.setObjectName("loginInput")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(50)
        self.password_input.setPlaceholderText(self.tr("Password"))
        self.password_input.returnPressed.connect(self.on_login_clicked)
        password_layout.addWidget(self.password_input)

        main_layout.addWidget(password_container)
        main_layout.addSpacing(15)

        # Grupo con icono
        group_container = QFrame()
        group_container.setObjectName("inputField")
        group_layout = QHBoxLayout(group_container)
        group_layout.setContentsMargins(15, 0, 15, 0)
        group_layout.setSpacing(10)

        group_icon = QLabel("🏢")
        group_icon.setStyleSheet(
            "font-size: 20px; color: #95a5a6; background: transparent;"
        )
        group_layout.addWidget(group_icon)

        self.group_combo = QComboBox()
        self.group_combo.setObjectName("loginCombo")
        self.group_combo.setMinimumHeight(50)
        self.group_combo.setPlaceholderText(self.tr("Business Group"))
        self.group_combo.currentIndexChanged.connect(self.on_group_changed)
        self._setup_combo_popup(self.group_combo)
        group_layout.addWidget(self.group_combo)

        main_layout.addWidget(group_container)
        main_layout.addSpacing(15)

        # Empresa con icono
        company_container = QFrame()
        company_container.setObjectName("inputField")
        company_layout = QHBoxLayout(company_container)
        company_layout.setContentsMargins(15, 0, 15, 0)
        company_layout.setSpacing(10)

        company_icon = QLabel("🏭")
        company_icon.setStyleSheet(
            "font-size: 20px; color: #95a5a6; background: transparent;"
        )
        company_layout.addWidget(company_icon)

        self.company_combo = QComboBox()
        self.company_combo.setObjectName("loginCombo")
        self.company_combo.setMinimumHeight(50)
        self.company_combo.setPlaceholderText(self.tr("Company"))
        self._setup_combo_popup(self.company_combo)
        company_layout.addWidget(self.company_combo)

        main_layout.addWidget(company_container)
        main_layout.addSpacing(30)

        # ========== BOTÓN LOGIN ==========
        self.access_button = QPushButton(self.tr("LOGIN"))
        self.access_button.setObjectName("loginButton")
        self.access_button.setMinimumHeight(55)
        access_font = QFont()
        access_font.setBold(True)
        access_font.setPointSize(13)
        access_font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 2)
        self.access_button.setFont(access_font)
        self.access_button.clicked.connect(self.on_login_clicked)
        main_layout.addWidget(self.access_button)

        main_layout.addSpacing(20)

        # ========== ENLACES INFERIORES ==========
        links_layout = QHBoxLayout()
        links_layout.setSpacing(30)

        # Forgot Password
        #forgot_link = QPushButton(self.tr("Forgot Password?"))
        #forgot_link.setObjectName("linkButton")
        #forgot_link.setMinimumHeight(30)
        #forgot_link.setCursor(Qt.CursorShape.PointingHandCursor)
        #forgot_link.clicked.connect(self.reject)  # Por ahora solo cierra
        #links_layout.addWidget(forgot_link)

        # Small configuration button (icon only) — kept for quick access from login
        self.config_btn = QPushButton()
        self.config_btn.setObjectName("configButton")
        self.config_btn.setText(self.tr("Configuración"))

        # keep it compact
        self.config_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.config_btn.clicked.connect(self.open_config)
        links_layout.addWidget(self.config_btn)


        main_layout.addLayout(links_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)

        # Aplicar estilos
        self.apply_styles()

    def _setup_combo_popup(self, combo: QComboBox):
        """Configura el popup del combobox con un diseño personalizado."""
        from PySide6.QtCore import QPoint
        from PySide6.QtWidgets import QFrame, QPushButton, QVBoxLayout

        # Guardar el showPopup original
        # (intencionado) no necesitamos mantener la referencia al showPopup original

        def custom_show_popup():
            # Crear un frame personalizado para el popup
            popup_frame = QFrame()
            popup_frame.setWindowFlags(
                Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint
            )
            popup_frame.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
            popup_frame.setObjectName("customPopup")

            # Layout para los items
            layout = QVBoxLayout(popup_frame)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)

            # Container con borde redondeado
            container = QFrame()
            container.setObjectName("popupContainer")
            container_layout = QVBoxLayout(container)
            container_layout.setContentsMargins(8, 8, 8, 8)
            container_layout.setSpacing(2)

            # Añadir items
            for i in range(combo.count()):
                item_btn = QPushButton(combo.itemText(i))
                item_btn.setObjectName("popupItem")
                item_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                item_btn.setMinimumHeight(40)

                # Marcar el item seleccionado
                if i == combo.currentIndex():
                    item_btn.setProperty("selected", True)

                # Conectar el click
                item_btn.clicked.connect(
                    lambda checked=False, idx=i: (
                        combo.setCurrentIndex(idx),
                        popup_frame.close(),
                    )
                )

                container_layout.addWidget(item_btn)

            layout.addWidget(container)

            # Aplicar estilos
            popup_frame.setStyleSheet(
                """
                QFrame#customPopup {
                    background: transparent;
                }
                QFrame#popupContainer {
                    background-color: white;
                    border: 2px solid #021323;
                    border-radius: 10px;
                }
                QPushButton#popupItem {
                    background: transparent;
                    border: none;
                    border-radius: 6px;
                    color: #2c3e50;
                    font-size: 14px;
                    font-weight: 500;
                    text-align: left;
                    padding-left: 15px;
                    margin: 2px 4px;
                }
                QPushButton#popupItem:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgba(255, 140, 66, 0.15),
                        stop:1 rgba(255, 140, 66, 0.1));
                }
                QPushButton#popupItem[selected="true"] {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #ff8c42,
                        stop:1 #ff7a28);
                    color: white;
                }
            """
            )

            # Posicionar el popup
            global_pos = combo.mapToGlobal(QPoint(0, combo.height()))
            popup_frame.move(global_pos)
            popup_frame.setMinimumWidth(combo.width())

            # Mostrar
            popup_frame.show()

        # Reemplazar el método showPopup
        combo.showPopup = custom_show_popup

    def apply_styles(self):
        """Aplica los estilos CSS basados en la imagen de referencia."""
        self.setStyleSheet(
            """
            QDialog {
                /* Fondo ahora igual al fondo del logo */
                background: #021323;
            }
            
            QLabel {
                background: transparent;
            }
            
            QFrame#inputField {
                background: white;
                border-radius: 8px;
                border: none;
                min-height: 50px;
                max-height: 50px;
            }
            
            QComboBox#loginCombo {
                background: transparent;
                border: none;
                color: #2c3e50;
                font-size: 14px;
                font-weight: 500;
                padding-left: 5px;
                padding-right: 35px;
            }
            
            QComboBox#loginCombo::drop-down {
                border: none;
                width: 35px;
                background: transparent;
                border-radius: 6px;
                margin: 4px;
            }
            
            QComboBox#loginCombo::drop-down:hover {
                background: rgba(2, 19, 35, 0.05);
            }
            
            QComboBox#loginCombo::down-arrow {
                image: url(resources/icons/chevron-down-dark.svg);
                width: 14px;
                height: 14px;
                margin-right: 8px;
            }
            
            QComboBox#loginCombo::down-arrow:hover {
                /* El hover ya está manejado por el contenedor */
            }
            
            QLineEdit#loginInput {
                background: transparent;
                border: none;
                color: #2c3e50;
                font-size: 14px;
                padding-left: 5px;
            }
            
            QLineEdit#loginInput::placeholder {
                color: #95a5a6;
            }
            
            QPushButton#loginButton {
                background: #ff8c42;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
                letter-spacing: 2px;
            }
            
            QPushButton#loginButton:hover {
                background: #ff7a28;
            }
            
            QPushButton#loginButton:pressed {
                background: #e67a3c;
            }
            
            QPushButton#linkButton {
                background: transparent;
                border: none;
                color: white;
                font-size: 13px;
                text-decoration: underline;
            }
            
            QPushButton#linkButton:hover {
                color: #ff8c42;
            }
        """
        )

    def load_demo_data(self):
        """Carga datos de usuarios, grupos y empresas desde la base de datos."""
        # Cargar usuarios
        users = UserRepository.get_all_users()
        for user in users:
            self.user_combo.addItem(user.username, user)  # type: ignore

        # Seleccionar el usuario por defecto (preferir sesión actual si existe)
        try:
            session = None
            if hasattr(self.auth_manager, "get_current_session"):
                session = self.auth_manager.get_current_session()
            if users:
                if session and getattr(session, "user", None):
                    # buscar el índice del usuario en la lista
                    for i in range(self.user_combo.count()):
                        data = self.user_combo.itemData(i)
                        if (
                            data
                            and getattr(data, "username", None) == session.user.username
                        ):
                            self.user_combo.setCurrentIndex(i)
                            break
                    else:
                        # no encontrado, seleccionar el primero
                        self.user_combo.setCurrentIndex(0)
                else:
                    self.user_combo.setCurrentIndex(0)
        except Exception:
            # no bloquear si algo falla al aplicar la selección por defecto
            pass

        # Cargar grupos empresariales
        groups = BusinessGroupRepository.get_all_groups()
        for group in groups:
            self.group_combo.addItem(group.name, group)  # type: ignore

        # Las empresas se cargarán al seleccionar grupo
        if groups:
            # seleccionar grupo por defecto: preferir el grupo de la sesión si existe
            try:
                # obtener session si está disponible
                session = None
                if hasattr(self.auth_manager, "get_current_session"):
                    session = self.auth_manager.get_current_session()

                if (
                    session
                    and getattr(session, "company_context", None)
                    and getattr(session.company_context, "group", None)
                ):
                    target_group_id = session.company_context.group.id
                    for i in range(self.group_combo.count()):
                        data = self.group_combo.itemData(i)
                        if data and getattr(data, "id", None) == target_group_id:
                            self.group_combo.setCurrentIndex(i)
                            break
                    else:
                        self.group_combo.setCurrentIndex(0)
                else:
                    # no session info -> select first
                    self.group_combo.setCurrentIndex(0)

            except Exception:
                self.group_combo.setCurrentIndex(0)

            # Forzar carga de empresas del grupo seleccionado
            self.on_group_changed(self.group_combo.currentIndex())

    def on_group_changed(self, index: int):
        """Cuando cambia el grupo, cargar las empresas de ese grupo."""
        self.company_combo.clear()

        group = self.group_combo.currentData()
        if not group:
            return

        # Cargar empresas desde la base de datos
        group_id = group.id
        companies = CompanyRepository.get_companies_by_group(group_id)
        for company in companies:
            # company es ahora un objeto Empresa
            name = company.nombre_comercial or company.nombre_fiscal or "Empresa"
            self.company_combo.addItem(name, company)  # type: ignore

        # Intentar seleccionar la empresa por defecto:
        # 1) Preferir company del session (si existe)
        # 2) Preferir company_manager.current_company_id si está configurado
        # 3) Sino seleccionar la primera empresa
        try:
            desired_company_id = None
            session = None
            if hasattr(self.auth_manager, "get_current_session"):
                session = self.auth_manager.get_current_session()

            if (
                session
                and getattr(session, "company_context", None)
                and getattr(session.company_context, "company", None)
            ):
                desired_company_id = session.company_context.company.id
            else:
                try:
                    # company_manager puede contener la última empresa seleccionada en la sesión actual
                    if (
                        hasattr(company_manager, "current_company_id")
                        and company_manager.current_company_id
                    ):
                        desired_company_id = company_manager.current_company_id
                except Exception:
                    desired_company_id = None

            if desired_company_id is not None:
                # buscar y seleccionar
                for idx in range(self.company_combo.count()):
                    data = self.company_combo.itemData(idx)
                    if data and getattr(data, "id", None) == desired_company_id:
                        self.company_combo.setCurrentIndex(idx)
                        break
                else:
                    if self.company_combo.count() > 0:
                        self.company_combo.setCurrentIndex(0)
            else:
                if self.company_combo.count() > 0:
                    self.company_combo.setCurrentIndex(0)
        except Exception:
            # no bloquear si falla la selección por defecto
            if self.company_combo.count() > 0:
                self.company_combo.setCurrentIndex(0)

    def on_login_clicked(self):
        """Maneja el click en Acceder."""
        username = self.user_combo.currentText()
        password = self.password_input.text()

        if not username or not password:
            from core.ui_helpers import show_warning

            show_warning(
                self, self.tr("Error"), self.tr("Ingresa usuario y contraseña")
            )
            return

        group = self.group_combo.currentData()
        company = self.company_combo.currentData()

        if not group or not company:
            from core.ui_helpers import show_warning

            show_warning(self, self.tr("Error"), self.tr("Selecciona grupo y empresa"))
            return

        # Intentar login (delegar en AuthenticationManager vía repositorio)
        session = self.try_login(username, password)
        if not session:
            from core.ui_helpers import show_warning

            show_warning(
                self, self.tr("Error"), self.tr("Usuario o contraseña incorrectos")
            )
            self.password_input.clear()
            return

        # Verificar que el usuario tiene acceso al grupo/empresa seleccionados
        user = session.user
        try:
            # Soportar tanto dicts (BD) como objetos User (demo)
            if isinstance(user, dict):
                allowed_groups = user.get("allowed_groups")
                allowed_companies = user.get("allowed_companies")
            else:
                allowed_groups = getattr(user, "allowed_groups", None)
                allowed_companies = getattr(user, "allowed_companies", None)

            # Soportar tanto dicts (BD) como objetos (legacy)
            group_id = group.id
            company_id = company.id

            if allowed_groups is not None and group_id not in allowed_groups:
                from core.ui_helpers import show_warning

                show_warning(
                    self,
                    self.tr("Error"),
                    self.tr("Usuario no autorizado para el grupo seleccionado"),
                )
                return
            if allowed_companies is not None and company_id not in allowed_companies:
                from core.ui_helpers import show_warning

                show_warning(
                    self,
                    self.tr("Error"),
                    self.tr("Usuario no autorizado para la empresa seleccionada"),
                )
                return
        except Exception as e:
            # Si no podemos verificar permisos, denegamos acceso por seguridad
            logging.getLogger(__name__).exception(f"Error verificando permisos: {e}")
            from core.ui_helpers import show_warning

            show_warning(
                self, self.tr("Error"), self.tr("No se pudo verificar permisos de usuario")
            )
            return

        # Crear contexto de empresa
        context = CompanyContext(group=group, company=company)

        # Guardar en la sesión
        try:
            session.company_context = context
            self.auth_manager._current_session = session
        except Exception:
            pass

        # IMPORTANTE: Configurar la base de datos de la empresa
        logger = logging.getLogger(__name__)
        try:
            # Soportar tanto dicts como objetos
            company_id = company.id
            company_name = company.nombre_fiscal

            success = company_manager.select_company(company_id)
            if not success:
                from core.ui_helpers import show_warning

                show_warning(
                    self,
                    self.tr("Error"),
                    self.tr(
                        "No se pudo configurar la base de datos de la empresa seleccionada. Comprueba la configuración y vuelve a intentarlo."
                    ),
                )
                return

            logger.info("✅ Base de datos configurada para empresa: %s", company_name)

        except Exception as e:
            logger.exception("❌ Error configurando empresa: %s", e)
            from core.ui_helpers import show_warning
            show_warning(
                self,
                self.tr("Error"),
                self.tr(f"Error al configurar empresa: {str(e)}")
            )
            return  # No continuar si falla

        # Emitir solo si todo ha ido bien
        self.login_successful.emit(context)



    def try_login(self, username: str, password: str):
        """Intenta autenticar delegando en AuthenticationManager.

        Devuelve un objeto Session si el login fue exitoso, o None si falló.
        Mantiene un fallback a usuarios demo cuando el repositorio no devuelve usuario.
        """
        logger = logging.getLogger(__name__)
        logger.debug(f"try_login called for user: {username}")

        # Primero, intentar autenticar usando el repositorio real (MVC)
        try:
            from core.repositories import UserRepository

            class _UserRepoAdapter:
                @staticmethod
                def get_by_username(uname: str):
                    # Repositorio central expone `get_user_by_username`.
                    try:
                        user = UserRepository.get_user_by_username(uname)
                        logger.debug(f"UserRepository returned: {type(user).__name__ if user else 'None'}")
                        return user
                    except Exception as e:
                        logger.debug(f"UserRepository exception: {e}")
                        return None

            session = self.auth_manager.login(username, password, _UserRepoAdapter)
            if session:
                logger.info(f"Login successful via repository for {username}")
                return session
            else:
                logger.debug(f"Repository login failed for {username}, trying demo users")
        except Exception as e:
            # Si algo falla con el repo, intentamos fallback demo
            logger.exception(f"Error usando UserRepository for login - fallback a demo users: {e}")

        # Fallback: usuarios demo (local, para entornos sin BD)
        logger.debug("Trying demo users fallback")
        demo_users = self.create_demo_users()
        logger.debug(f"Created {len(demo_users)} demo users")

        for user in demo_users:
            # user es un objeto User (no dict)
            logger.debug(f"Checking demo user: {user.username}")
            if user.username == username and user.verify_password(password):
                import secrets
                from datetime import datetime

                from core.auth import Session

                logger.info(f"Login successful via demo user for {username}")
                session = Session(
                    user=user,
                    login_time=datetime.now(),
                    token=secrets.token_urlsafe(32),
                )

                return session

        logger.warning(f"Login failed for {username} - no matching user found")
        return None

    def create_demo_users(self):
        """Crea usuarios de demostración."""
        from datetime import datetime

        return [
            User(
                id=1,
                username="admin",
                email="marc.miralles@artstudio3d.fr",
                full_name="Administrador",
                password_hash=User.hash_password("admin"),
                role=UserRole.ADMIN,
                is_active=True,
                created_at=datetime.now(),
                allowed_groups=[1, 2],
                allowed_companies=[1, 2, 3],
            ),
            User(
                id=2,
                username="manager",
                email="manager@artstudio3d.com",
                full_name="Gestor Principal",
                password_hash=User.hash_password("manager"),
                role=UserRole.MANAGER,
                is_active=True,
                created_at=datetime.now(),
                allowed_groups=[1],
                allowed_companies=[1, 2],
            ),
            User(
                id=3,
                username="user",
                email="user@artstudio3d.com",
                full_name="Usuario Normal",
                password_hash=User.hash_password("user"),
                role=UserRole.EMPLOYEE,
                is_active=True,
                created_at=datetime.now(),
                allowed_groups=[1],
                allowed_companies=[1],
            ),
        ]

    def open_config(self):
        """Abre la configuración."""
        from app.views.config_dialog import ConfigDialog

        dialog = ConfigDialog(self)

        # Conectar señal de cambio de idioma
        dialog.language_changed.connect(self.on_language_changed)

        dialog.exec()

    def on_language_changed(self, language_code: str):
        """Maneja el cambio de idioma: notifica que la preferencia se guardó y que es necesario reiniciar.

        La preferencia ya se guarda en `QSettings` desde `ConfigDialog`. La aplicación carga
        la traducción al arrancar (en `CreativeERPApp.initialize`), por lo que un reinicio
        aplicará el idioma seleccionado.
        """
        from PySide6.QtWidgets import QApplication

        from core.ui_helpers import show_info

        app = QApplication.instance()
        # Solo informar al usuario: el idioma se guardó en QSettings en el diálogo de configuración
        if app:
            show_info(
                self,
                self.tr("Cambio de idioma"),
                self.tr(
                    "La preferencia de idioma se ha guardado. Por favor reinicie la aplicación para aplicar los cambios."
                ),
            )

    def showEvent(self, event):
        """Ensure the password input receives focus when the dialog is shown."""
        try:
            # Defer focus set to the next iteration of the event loop so it
            # happens after Qt has finished processing the show sequence.
            from PySide6.QtCore import QTimer

            QTimer.singleShot(0, self.password_input.setFocus)
        except Exception:
            pass
        super().showEvent(event)
