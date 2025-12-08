# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frmClientes.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject, QSize, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QFormLayout,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListView,
    QPushButton,
    QRadioButton,
    QSizePolicy,
    QSpacerItem,
    QSpinBox,
    QStackedWidget,
    QTableView,
    QTabWidget,
    QTextEdit,
    QTreeWidget,
    QVBoxLayout,
    QWidget,
)


class Ui_frmClientes(object):
    def setupUi(self, frmClientes):
        if not frmClientes.objectName():
            frmClientes.setObjectName("frmClientes")
        frmClientes.setWindowModality(Qt.WindowModality.WindowModal)
        frmClientes.resize(1073, 732)
        frmClientes.setBaseSize(QSize(1024, 500))
        frmClientes.setModal(True)
        self.gridLayout_3 = QGridLayout(frmClientes)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.textoTitulo = QLabel(frmClientes)
        self.textoTitulo.setObjectName("textoTitulo")
        self.textoTitulo.setMinimumSize(QSize(464, 27))
        self.textoTitulo.setMaximumSize(QSize(16777215, 27))
        self.textoTitulo.setStyleSheet(
            "background: #304163;\n"
            "color: rgb(255,255,255);\n"
            'font: 14pt "Sans Serif";'
        )
        self.textoTitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.textoTitulo, 0, 0, 1, 5)

        self.stackedWidget = QStackedWidget(frmClientes)
        self.stackedWidget.setObjectName("stackedWidget")
        self.paginaedicion = QWidget()
        self.paginaedicion.setObjectName("paginaedicion")
        self.gridLayout_27 = QGridLayout(self.paginaedicion)
        self.gridLayout_27.setObjectName("gridLayout_27")
        self.gridLayout_27.setContentsMargins(-1, -1, 20, -1)
        self.label_40 = QLabel(self.paginaedicion)
        self.label_40.setObjectName("label_40")

        self.gridLayout_27.addWidget(self.label_40, 0, 0, 1, 1)

        self.txtNombreFiscal = QLabel(self.paginaedicion)
        self.txtNombreFiscal.setObjectName("txtNombreFiscal")

        self.gridLayout_27.addWidget(self.txtNombreFiscal, 0, 1, 1, 1)

        self.frame_8 = QFrame(self.paginaedicion)
        self.frame_8.setObjectName("frame_8")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_8.sizePolicy().hasHeightForWidth())
        self.frame_8.setSizePolicy(sizePolicy)
        self.frame_8.setMinimumSize(QSize(135, 374))
        self.frame_8.setMaximumSize(QSize(110, 16777215))
        self.frame_8.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_8)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.btnBorrar = QPushButton(self.frame_8)
        self.btnBorrar.setObjectName("btnBorrar")
        self.btnBorrar.setMinimumSize(QSize(0, 45))
        icon = QIcon()
        icon.addFile(
            ":/PNG/resources/icons/png/delete.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.btnBorrar.setIcon(icon)
        self.btnBorrar.setIconSize(QSize(18, 18))

        self.gridLayout_7.addWidget(self.btnBorrar, 8, 0, 1, 1)

        self.btnGuardar = QPushButton(self.frame_8)
        self.btnGuardar.setObjectName("btnGuardar")
        self.btnGuardar.setEnabled(False)
        self.btnGuardar.setMinimumSize(QSize(0, 45))
        icon1 = QIcon()
        icon1.addFile(
            ":/PNG/resources/icons/png/Save.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.btnGuardar.setIcon(icon1)
        self.btnGuardar.setIconSize(QSize(24, 24))

        self.gridLayout_7.addWidget(self.btnGuardar, 5, 0, 1, 1)

        self.btnAnadir = QPushButton(self.frame_8)
        self.btnAnadir.setObjectName("btnAnadir")
        self.btnAnadir.setMinimumSize(QSize(0, 45))
        icon2 = QIcon()
        icon2.addFile(
            ":/PNG/resources/icons/png/Add.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.btnAnadir.setIcon(icon2)
        self.btnAnadir.setIconSize(QSize(24, 24))

        self.gridLayout_7.addWidget(self.btnAnadir, 0, 0, 1, 1)

        self.btnDeshacer = QPushButton(self.frame_8)
        self.btnDeshacer.setObjectName("btnDeshacer")
        self.btnDeshacer.setEnabled(False)
        self.btnDeshacer.setMinimumSize(QSize(0, 45))
        icon3 = QIcon()
        icon3.addFile(
            ":/PNG/resources/icons/png/undo.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.btnDeshacer.setIcon(icon3)
        self.btnDeshacer.setIconSize(QSize(24, 24))

        self.gridLayout_7.addWidget(self.btnDeshacer, 6, 0, 1, 1)

        self.btnEditar = QPushButton(self.frame_8)
        self.btnEditar.setObjectName("btnEditar")
        self.btnEditar.setMinimumSize(QSize(0, 45))
        icon4 = QIcon()
        icon4.addFile(
            ":/PNG/resources/icons/png/Edit.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.btnEditar.setIcon(icon4)
        self.btnEditar.setIconSize(QSize(24, 24))

        self.gridLayout_7.addWidget(self.btnEditar, 4, 0, 1, 1)

        self.btnBuscar = QPushButton(self.frame_8)
        self.btnBuscar.setObjectName("btnBuscar")
        self.btnBuscar.setMinimumSize(QSize(0, 45))
        icon5 = QIcon()
        icon5.addFile(
            ":/PNG/resources/icons/png/search.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.btnBuscar.setIcon(icon5)
        self.btnBuscar.setIconSize(QSize(24, 24))

        self.gridLayout_7.addWidget(self.btnBuscar, 3, 0, 1, 1)

        self.btnAnterior = QPushButton(self.frame_8)
        self.btnAnterior.setObjectName("btnAnterior")
        self.btnAnterior.setMinimumSize(QSize(0, 45))
        icon6 = QIcon()
        icon6.addFile(
            ":/PNG/resources/icons/png/Previous.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.btnAnterior.setIcon(icon6)
        self.btnAnterior.setIconSize(QSize(24, 24))

        self.gridLayout_7.addWidget(self.btnAnterior, 2, 0, 1, 1)

        self.btnSiguiente = QPushButton(self.frame_8)
        self.btnSiguiente.setObjectName("btnSiguiente")
        self.btnSiguiente.setMinimumSize(QSize(0, 45))
        icon7 = QIcon()
        icon7.addFile(
            ":/PNG/resources/icons/png/Next.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.btnSiguiente.setIcon(icon7)
        self.btnSiguiente.setIconSize(QSize(24, 24))

        self.gridLayout_7.addWidget(self.btnSiguiente, 1, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.gridLayout_7.addItem(self.verticalSpacer_3, 7, 0, 1, 1)

        self.gridLayout_27.addWidget(self.frame_8, 1, 0, 1, 1)

        self.tabwidget = QTabWidget(self.paginaedicion)
        self.tabwidget.setObjectName("tabwidget")
        sizePolicy1 = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tabwidget.sizePolicy().hasHeightForWidth())
        self.tabwidget.setSizePolicy(sizePolicy1)
        self.tabwidget.setAutoFillBackground(False)
        self.tab_datos = QWidget()
        self.tab_datos.setObjectName("tab_datos")
        self.tab_datos.setStyleSheet("")
        self.gridLayout_25 = QGridLayout(self.tab_datos)
        self.gridLayout_25.setObjectName("gridLayout_25")
        self.blink_stack = QStackedWidget(self.tab_datos)
        self.blink_stack.setObjectName("blink_stack")
        sizePolicy2 = QSizePolicy(
            QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred
        )
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.blink_stack.sizePolicy().hasHeightForWidth())
        self.blink_stack.setSizePolicy(sizePolicy2)
        self.page = QWidget()
        self.page.setObjectName("page")
        self.gridLayout_2 = QGridLayout(self.page)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.btnVer_OtrosContactos = QPushButton(self.page)
        self.btnVer_OtrosContactos.setObjectName("btnVer_OtrosContactos")
        self.btnVer_OtrosContactos.setEnabled(False)
        self.btnVer_OtrosContactos.setMinimumSize(QSize(145, 0))
        self.btnVer_OtrosContactos.setStyleSheet("")
        icon8 = QIcon()
        icon8.addFile(
            ":/Icons/PNG/users.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.btnVer_OtrosContactos.setIcon(icon8)
        self.btnVer_OtrosContactos.setIconSize(QSize(15, 15))

        self.gridLayout_2.addWidget(self.btnVer_OtrosContactos, 0, 0, 1, 1)

        self.frame_2 = QFrame(self.page)
        self.frame_2.setObjectName("frame_2")
        self.frame_2.setMaximumSize(QSize(250, 16777215))
        self.frame_2.setStyleSheet("")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_2)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_46 = QLabel(self.frame_2)
        self.label_46.setObjectName("label_46")
        self.label_46.setMaximumSize(QSize(16777215, 20))
        self.label_46.setStyleSheet("")
        self.label_46.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.label_46, 0, 0, 1, 1)

        self.btnEdita_tipoCliente = QPushButton(self.frame_2)
        self.btnEdita_tipoCliente.setObjectName("btnEdita_tipoCliente")

        self.gridLayout_5.addWidget(self.btnEdita_tipoCliente, 3, 0, 1, 1)

        self.lista_tipos = QTreeWidget(self.frame_2)
        self.lista_tipos.setObjectName("lista_tipos")
        self.lista_tipos.setFrameShape(QFrame.Shape.StyledPanel)
        self.lista_tipos.setProperty("showDropIndicator", True)
        self.lista_tipos.setRootIsDecorated(True)
        self.lista_tipos.header().setVisible(False)

        self.gridLayout_5.addWidget(self.lista_tipos, 1, 0, 2, 1)

        self.gridLayout_2.addWidget(self.frame_2, 1, 0, 1, 1)

        self.blink_stack.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName("page_2")
        self.gridLayout_17 = QGridLayout(self.page_2)
        self.gridLayout_17.setObjectName("gridLayout_17")
        self.blink_stack.addWidget(self.page_2)

        self.gridLayout_25.addWidget(self.blink_stack, 0, 1, 2, 1)

        self.gridLayout_30 = QGridLayout()
        self.gridLayout_30.setObjectName("gridLayout_30")
        self.label_3 = QLabel(self.tab_datos)
        self.label_3.setObjectName("label_3")

        self.gridLayout_30.addWidget(self.label_3, 3, 0, 1, 1)

        self.txtCifIntracomunitario = QLineEdit(self.tab_datos)
        self.txtCifIntracomunitario.setObjectName("txtCifIntracomunitario")
        self.txtCifIntracomunitario.setStyleSheet("")

        self.gridLayout_30.addWidget(self.txtCifIntracomunitario, 0, 5, 1, 1)

        self.btnValidarVIES = QPushButton(self.tab_datos)
        self.btnValidarVIES.setObjectName("btnValidarVIES")

        self.gridLayout_30.addWidget(self.btnValidarVIES, 0, 6, 1, 1)

        self.lblProvincia = QLabel(self.tab_datos)
        self.lblProvincia.setObjectName("lblProvincia")
        sizePolicy2.setHeightForWidth(
            self.lblProvincia.sizePolicy().hasHeightForWidth()
        )
        self.lblProvincia.setSizePolicy(sizePolicy2)

        self.gridLayout_30.addWidget(self.lblProvincia, 13, 0, 1, 1)

        self.label_15 = QLabel(self.tab_datos)
        self.label_15.setObjectName("label_15")
        sizePolicy2.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy2)

        self.gridLayout_30.addWidget(self.label_15, 10, 0, 1, 1)

        self.txtnombre_comercial = QLineEdit(self.tab_datos)
        self.txtnombre_comercial.setObjectName("txtnombre_comercial")
        self.txtnombre_comercial.setMaximumSize(QSize(774, 16777215))
        self.txtnombre_comercial.setStyleSheet("")

        self.gridLayout_30.addWidget(self.txtnombre_comercial, 9, 1, 1, 6)

        self.label_24 = QLabel(self.tab_datos)
        self.label_24.setObjectName("label_24")
        sizePolicy2.setHeightForWidth(self.label_24.sizePolicy().hasHeightForWidth())
        self.label_24.setSizePolicy(sizePolicy2)
        self.label_24.setMaximumSize(QSize(70, 16777215))

        self.gridLayout_30.addWidget(self.label_24, 18, 0, 1, 1)

        self.label_16 = QLabel(self.tab_datos)
        self.label_16.setObjectName("label_16")

        self.gridLayout_30.addWidget(self.label_16, 10, 2, 1, 1)

        self.label_22 = QLabel(self.tab_datos)
        self.label_22.setObjectName("label_22")
        sizePolicy2.setHeightForWidth(self.label_22.sizePolicy().hasHeightForWidth())
        self.label_22.setSizePolicy(sizePolicy2)

        self.gridLayout_30.addWidget(self.label_22, 16, 0, 1, 1)

        self.txtdireccion1 = QLineEdit(self.tab_datos)
        self.txtdireccion1.setObjectName("txtdireccion1")
        self.txtdireccion1.setStyleSheet("")

        self.gridLayout_30.addWidget(self.txtdireccion1, 11, 1, 1, 6)

        self.label_19 = QLabel(self.tab_datos)
        self.label_19.setObjectName("label_19")
        sizePolicy2.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy2)
        self.label_19.setMaximumSize(QSize(70, 16777215))

        self.gridLayout_30.addWidget(self.label_19, 14, 0, 1, 1)

        self.txttelefono1 = QLineEdit(self.tab_datos)
        self.txttelefono1.setObjectName("txttelefono1")
        self.txttelefono1.setStyleSheet("")

        self.gridLayout_30.addWidget(self.txttelefono1, 14, 1, 1, 3)

        self.txtnombre_fiscal = QLineEdit(self.tab_datos)
        self.txtnombre_fiscal.setObjectName("txtnombre_fiscal")
        sizePolicy3 = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed
        )
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(
            self.txtnombre_fiscal.sizePolicy().hasHeightForWidth()
        )
        self.txtnombre_fiscal.setSizePolicy(sizePolicy3)
        self.txtnombre_fiscal.setStyleSheet("")

        self.gridLayout_30.addWidget(self.txtnombre_fiscal, 8, 1, 1, 6)

        self.txtpoblacion = QLineEdit(self.tab_datos)
        self.txtpoblacion.setObjectName("txtpoblacion")
        self.txtpoblacion.setStyleSheet("")

        self.gridLayout_30.addWidget(self.txtpoblacion, 10, 3, 1, 4)

        self.txtdireccion2 = QLineEdit(self.tab_datos)
        self.txtdireccion2.setObjectName("txtdireccion2")
        self.txtdireccion2.setStyleSheet("")

        self.gridLayout_30.addWidget(self.txtdireccion2, 12, 1, 1, 6)

        self.txtprovincia = QLineEdit(self.tab_datos)
        self.txtprovincia.setObjectName("txtprovincia")
        self.txtprovincia.setStyleSheet("")

        self.gridLayout_30.addWidget(self.txtprovincia, 13, 1, 1, 3)

        self.txttelefono2 = QLineEdit(self.tab_datos)
        self.txttelefono2.setObjectName("txttelefono2")
        self.txttelefono2.setStyleSheet("")

        self.gridLayout_30.addWidget(self.txttelefono2, 14, 5, 1, 2)

        self.txtcp = QLineEdit(self.tab_datos)
        self.txtcp.setObjectName("txtcp")
        self.txtcp.setMaximumSize(QSize(100, 16777215))
        self.txtcp.setStyleSheet("")

        self.gridLayout_30.addWidget(self.txtcp, 10, 1, 1, 1)

        self.label_20 = QLabel(self.tab_datos)
        self.label_20.setObjectName("label_20")
        sizePolicy2.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy2)

        self.gridLayout_30.addWidget(self.label_20, 14, 4, 1, 1)

        self.label_13 = QLabel(self.tab_datos)
        self.label_13.setObjectName("label_13")
        sizePolicy2.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy2)

        self.gridLayout_30.addWidget(self.label_13, 11, 0, 1, 1)

        self.label_12 = QLabel(self.tab_datos)
        self.label_12.setObjectName("label_12")
        sizePolicy2.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy2)

        self.gridLayout_30.addWidget(self.label_12, 9, 0, 1, 1)

        self.lblCIF_IVA_UE = QLabel(self.tab_datos)
        self.lblCIF_IVA_UE.setObjectName("lblCIF_IVA_UE")

        self.gridLayout_30.addWidget(self.lblCIF_IVA_UE, 0, 4, 1, 1)

        self.txtemail = QLineEdit(self.tab_datos)
        self.txtemail.setObjectName("txtemail")
        self.txtemail.setStyleSheet("")

        self.gridLayout_30.addWidget(self.txtemail, 18, 1, 1, 6)

        self.label_18 = QLabel(self.tab_datos)
        self.label_18.setObjectName("label_18")

        self.gridLayout_30.addWidget(self.label_18, 13, 4, 1, 1)

        self.label_14 = QLabel(self.tab_datos)
        self.label_14.setObjectName("label_14")
        sizePolicy2.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy2)

        self.gridLayout_30.addWidget(self.label_14, 12, 0, 1, 1)

        self.cboPais = QComboBox(self.tab_datos)
        self.cboPais.setObjectName("cboPais")

        self.gridLayout_30.addWidget(self.cboPais, 13, 5, 1, 2)

        self.txtmovil = QLineEdit(self.tab_datos)
        self.txtmovil.setObjectName("txtmovil")
        self.txtmovil.setStyleSheet("")

        self.gridLayout_30.addWidget(self.txtmovil, 16, 1, 1, 3)

        self.label_23 = QLabel(self.tab_datos)
        self.label_23.setObjectName("label_23")
        sizePolicy2.setHeightForWidth(self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy2)

        self.gridLayout_30.addWidget(self.label_23, 19, 0, 1, 1)

        self.label_11 = QLabel(self.tab_datos)
        self.label_11.setObjectName("label_11")
        sizePolicy2.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy2)

        self.gridLayout_30.addWidget(self.label_11, 8, 0, 1, 1)

        self.label = QLabel(self.tab_datos)
        self.label.setObjectName("label")
        self.label.setMaximumSize(QSize(49, 16777215))
        self.label.setStyleSheet("")

        self.gridLayout_30.addWidget(self.label, 0, 0, 1, 1)

        self.txtweb = QLineEdit(self.tab_datos)
        self.txtweb.setObjectName("txtweb")
        self.txtweb.setStyleSheet("")

        self.gridLayout_30.addWidget(self.txtweb, 19, 1, 1, 3)

        self.label_25 = QLabel(self.tab_datos)
        self.label_25.setObjectName("label_25")
        sizePolicy2.setHeightForWidth(self.label_25.sizePolicy().hasHeightForWidth())
        self.label_25.setSizePolicy(sizePolicy2)

        self.gridLayout_30.addWidget(self.label_25, 19, 4, 1, 1)

        self.txtObservaciones = QLineEdit(self.tab_datos)
        self.txtObservaciones.setObjectName("txtObservaciones")
        self.txtObservaciones.setStyleSheet("")

        self.gridLayout_30.addWidget(self.txtObservaciones, 19, 5, 1, 2)

        self.label_2 = QLabel(self.tab_datos)
        self.label_2.setObjectName("label_2")

        self.gridLayout_30.addWidget(self.label_2, 1, 0, 1, 1)

        self.lblSegundoApellido = QLabel(self.tab_datos)
        self.lblSegundoApellido.setObjectName("lblSegundoApellido")
        self.lblSegundoApellido.setMinimumSize(QSize(0, 0))
        self.lblSegundoApellido.setMaximumSize(QSize(16777214, 16777215))

        self.gridLayout_30.addWidget(self.lblSegundoApellido, 5, 0, 1, 1)

        self.label_4 = QLabel(self.tab_datos)
        self.label_4.setObjectName("label_4")

        self.gridLayout_30.addWidget(self.label_4, 4, 0, 1, 1)

        self.txtnombre = QLineEdit(self.tab_datos)
        self.txtnombre.setObjectName("txtnombre")
        self.txtnombre.setStyleSheet("")
        self.txtnombre.setEchoMode(QLineEdit.EchoMode.Normal)

        self.gridLayout_30.addWidget(self.txtnombre, 3, 1, 1, 6)

        self.txtPrimerApellido = QLineEdit(self.tab_datos)
        self.txtPrimerApellido.setObjectName("txtPrimerApellido")
        self.txtPrimerApellido.setStyleSheet("")

        self.gridLayout_30.addWidget(self.txtPrimerApellido, 4, 1, 1, 6)

        self.txtSegundoApellido = QLineEdit(self.tab_datos)
        self.txtSegundoApellido.setObjectName("txtSegundoApellido")
        self.txtSegundoApellido.setStyleSheet("")

        self.gridLayout_30.addWidget(self.txtSegundoApellido, 5, 1, 1, 6)

        self.txtcodigo_cliente = QLineEdit(self.tab_datos)
        self.txtcodigo_cliente.setObjectName("txtcodigo_cliente")
        self.txtcodigo_cliente.setStyleSheet("")
        self.txtcodigo_cliente.setReadOnly(False)

        self.gridLayout_30.addWidget(self.txtcodigo_cliente, 0, 1, 1, 3)

        self.txtcif_nif = QLineEdit(self.tab_datos)
        self.txtcif_nif.setObjectName("txtcif_nif")
        self.txtcif_nif.setStyleSheet("")

        self.gridLayout_30.addWidget(self.txtcif_nif, 1, 1, 1, 3)

        self.LblSIRET = QLabel(self.tab_datos)
        self.LblSIRET.setObjectName("LblSIRET")

        self.gridLayout_30.addWidget(self.LblSIRET, 1, 4, 1, 1)

        self.txtSiret = QLineEdit(self.tab_datos)
        self.txtSiret.setObjectName("txtSiret")

        self.gridLayout_30.addWidget(self.txtSiret, 1, 5, 1, 2)

        self.gridLayout_25.addLayout(self.gridLayout_30, 0, 0, 2, 1)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.gridLayout_25.addItem(self.verticalSpacer, 2, 0, 1, 1)

        self.tabwidget.addTab(self.tab_datos, "")
        self.tab_direcciones = QWidget()
        self.tab_direcciones.setObjectName("tab_direcciones")
        self.tab_direcciones.setStyleSheet("")
        self.gridLayout = QGridLayout(self.tab_direcciones)
        self.gridLayout.setObjectName("gridLayout")
        self.label_7 = QLabel(self.tab_direcciones)
        self.label_7.setObjectName("label_7")
        self.label_7.setMaximumSize(QSize(16777215, 27))
        self.label_7.setStyleSheet("background: #304163;\n" "color: rgb(255,255,255);")
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_7, 0, 0, 1, 1)

        self.label_6 = QLabel(self.tab_direcciones)
        self.label_6.setObjectName("label_6")

        self.gridLayout.addWidget(self.label_6, 0, 1, 1, 1)

        self.txtdescripcion_direccion = QLineEdit(self.tab_direcciones)
        self.txtdescripcion_direccion.setObjectName("txtdescripcion_direccion")

        self.gridLayout.addWidget(self.txtdescripcion_direccion, 0, 2, 1, 1)

        self.lista_direccionesAlternativas = QListView(self.tab_direcciones)
        self.lista_direccionesAlternativas.setObjectName(
            "lista_direccionesAlternativas"
        )
        self.lista_direccionesAlternativas.setMaximumSize(QSize(200, 16777215))
        self.lista_direccionesAlternativas.setAlternatingRowColors(True)
        self.lista_direccionesAlternativas.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.lista_direccionesAlternativas.setViewMode(QListView.ViewMode.ListMode)
        self.lista_direccionesAlternativas.setModelColumn(0)

        self.gridLayout.addWidget(self.lista_direccionesAlternativas, 1, 0, 8, 1)

        self.label_29 = QLabel(self.tab_direcciones)
        self.label_29.setObjectName("label_29")

        self.gridLayout.addWidget(self.label_29, 1, 1, 1, 1)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.txtcpPoblacionAlternativa = QLineEdit(self.tab_direcciones)
        self.txtcpPoblacionAlternativa.setObjectName("txtcpPoblacionAlternativa")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(
            self.txtcpPoblacionAlternativa.sizePolicy().hasHeightForWidth()
        )
        self.txtcpPoblacionAlternativa.setSizePolicy(sizePolicy4)

        self.horizontalLayout_13.addWidget(self.txtcpPoblacionAlternativa)

        self.label_66 = QLabel(self.tab_direcciones)
        self.label_66.setObjectName("label_66")

        self.horizontalLayout_13.addWidget(self.label_66)

        self.txtpoblacionAlternativa = QLineEdit(self.tab_direcciones)
        self.txtpoblacionAlternativa.setObjectName("txtpoblacionAlternativa")

        self.horizontalLayout_13.addWidget(self.txtpoblacionAlternativa)

        self.gridLayout.addLayout(self.horizontalLayout_13, 1, 2, 1, 1)

        self.label_27 = QLabel(self.tab_direcciones)
        self.label_27.setObjectName("label_27")

        self.gridLayout.addWidget(self.label_27, 2, 1, 1, 1)

        self.txtdireccion1Alternativa1 = QLineEdit(self.tab_direcciones)
        self.txtdireccion1Alternativa1.setObjectName("txtdireccion1Alternativa1")

        self.gridLayout.addWidget(self.txtdireccion1Alternativa1, 2, 2, 1, 1)

        self.label_28 = QLabel(self.tab_direcciones)
        self.label_28.setObjectName("label_28")

        self.gridLayout.addWidget(self.label_28, 3, 1, 1, 1)

        self.txtdireccion1Alternativa2 = QLineEdit(self.tab_direcciones)
        self.txtdireccion1Alternativa2.setObjectName("txtdireccion1Alternativa2")

        self.gridLayout.addWidget(self.txtdireccion1Alternativa2, 3, 2, 1, 1)

        self.lblProvinciaAlternativa = QLabel(self.tab_direcciones)
        self.lblProvinciaAlternativa.setObjectName("lblProvinciaAlternativa")

        self.gridLayout.addWidget(self.lblProvinciaAlternativa, 4, 1, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.txtprovinciaAlternativa = QLineEdit(self.tab_direcciones)
        self.txtprovinciaAlternativa.setObjectName("txtprovinciaAlternativa")

        self.horizontalLayout.addWidget(self.txtprovinciaAlternativa)

        self.label_31 = QLabel(self.tab_direcciones)
        self.label_31.setObjectName("label_31")

        self.horizontalLayout.addWidget(self.label_31)

        self.cbopaisAlternativa = QComboBox(self.tab_direcciones)
        self.cbopaisAlternativa.setObjectName("cbopaisAlternativa")
        self.cbopaisAlternativa.setMinimumSize(QSize(200, 0))

        self.horizontalLayout.addWidget(self.cbopaisAlternativa)

        self.gridLayout.addLayout(self.horizontalLayout, 4, 2, 1, 1)

        self.label_64 = QLabel(self.tab_direcciones)
        self.label_64.setObjectName("label_64")

        self.gridLayout.addWidget(self.label_64, 5, 1, 1, 1)

        self.txtemail_alternativa = QLineEdit(self.tab_direcciones)
        self.txtemail_alternativa.setObjectName("txtemail_alternativa")

        self.gridLayout.addWidget(self.txtemail_alternativa, 5, 2, 1, 1)

        self.label_86 = QLabel(self.tab_direcciones)
        self.label_86.setObjectName("label_86")

        self.gridLayout.addWidget(self.label_86, 6, 1, 1, 1)

        self.txtcomentarios_alternativa = QTextEdit(self.tab_direcciones)
        self.txtcomentarios_alternativa.setObjectName("txtcomentarios_alternativa")

        self.gridLayout.addWidget(self.txtcomentarios_alternativa, 6, 2, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btnAnadirdireccion = QPushButton(self.tab_direcciones)
        self.btnAnadirdireccion.setObjectName("btnAnadirdireccion")
        self.btnAnadirdireccion.setEnabled(False)
        icon9 = QIcon()
        icon9.addFile(":/PNG/Add.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnAnadirdireccion.setIcon(icon9)
        self.btnAnadirdireccion.setIconSize(QSize(16, 16))

        self.horizontalLayout_2.addWidget(self.btnAnadirdireccion)

        self.btnEditardireccionAlternativa = QPushButton(self.tab_direcciones)
        self.btnEditardireccionAlternativa.setObjectName(
            "btnEditardireccionAlternativa"
        )
        self.btnEditardireccionAlternativa.setEnabled(False)
        icon10 = QIcon()
        icon10.addFile(":/PNG/Edit.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnEditardireccionAlternativa.setIcon(icon10)

        self.horizontalLayout_2.addWidget(self.btnEditardireccionAlternativa)

        self.btnBorrardireccion = QPushButton(self.tab_direcciones)
        self.btnBorrardireccion.setObjectName("btnBorrardireccion")
        self.btnBorrardireccion.setEnabled(False)
        icon11 = QIcon()
        icon11.addFile(":/PNG/delete.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnBorrardireccion.setIcon(icon11)
        self.btnBorrardireccion.setIconSize(QSize(16, 16))

        self.horizontalLayout_2.addWidget(self.btnBorrardireccion)

        self.gridLayout.addLayout(self.horizontalLayout_2, 7, 2, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.btnGuardardireccionAlternativa = QPushButton(self.tab_direcciones)
        self.btnGuardardireccionAlternativa.setObjectName(
            "btnGuardardireccionAlternativa"
        )
        self.btnGuardardireccionAlternativa.setEnabled(False)
        icon12 = QIcon()
        icon12.addFile(":/PNG/Save.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnGuardardireccionAlternativa.setIcon(icon12)

        self.horizontalLayout_4.addWidget(self.btnGuardardireccionAlternativa)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.btnDeshacerdireccionAlternativa = QPushButton(self.tab_direcciones)
        self.btnDeshacerdireccionAlternativa.setObjectName(
            "btnDeshacerdireccionAlternativa"
        )
        self.btnDeshacerdireccionAlternativa.setEnabled(False)
        icon13 = QIcon()
        icon13.addFile(":/PNG/undo.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnDeshacerdireccionAlternativa.setIcon(icon13)

        self.horizontalLayout_4.addWidget(self.btnDeshacerdireccionAlternativa)

        self.gridLayout.addLayout(self.horizontalLayout_4, 8, 2, 1, 1)

        self.tabwidget.addTab(self.tab_direcciones, "")
        self.tab_Datos_bancarios_financieros = QWidget()
        self.tab_Datos_bancarios_financieros.setObjectName(
            "tab_Datos_bancarios_financieros"
        )
        self.tab_Datos_bancarios_financieros.setStyleSheet("")
        self.gridLayout_16 = QGridLayout(self.tab_Datos_bancarios_financieros)
        self.gridLayout_16.setObjectName("gridLayout_16")
        self.frame_9 = QFrame(self.tab_Datos_bancarios_financieros)
        self.frame_9.setObjectName("frame_9")
        self.frame_9.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Shadow.Raised)
        self.formLayout_5 = QFormLayout(self.frame_9)
        self.formLayout_5.setObjectName("formLayout_5")
        self.label_33 = QLabel(self.frame_9)
        self.label_33.setObjectName("label_33")

        self.formLayout_5.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_33)

        self.cbotarifa_cliente = QComboBox(self.frame_9)
        self.cbotarifa_cliente.setObjectName("cbotarifa_cliente")

        self.formLayout_5.setWidget(
            0, QFormLayout.ItemRole.FieldRole, self.cbotarifa_cliente
        )

        self.label_65 = QLabel(self.frame_9)
        self.label_65.setObjectName("label_65")

        self.formLayout_5.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_65)

        self.cboDivisa = QComboBox(self.frame_9)
        self.cboDivisa.setObjectName("cboDivisa")

        self.formLayout_5.setWidget(1, QFormLayout.ItemRole.FieldRole, self.cboDivisa)

        self.label_67 = QLabel(self.frame_9)
        self.label_67.setObjectName("label_67")

        self.formLayout_5.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_67)

        self.cboforma_pago = QComboBox(self.frame_9)
        self.cboforma_pago.setObjectName("cboforma_pago")

        self.formLayout_5.setWidget(
            2, QFormLayout.ItemRole.FieldRole, self.cboforma_pago
        )

        self.label_68 = QLabel(self.frame_9)
        self.label_68.setObjectName("label_68")

        self.formLayout_5.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_68)

        self.txtdia_pago1 = QSpinBox(self.frame_9)
        self.txtdia_pago1.setObjectName("txtdia_pago1")

        self.formLayout_5.setWidget(
            3, QFormLayout.ItemRole.FieldRole, self.txtdia_pago1
        )

        self.label_69 = QLabel(self.frame_9)
        self.label_69.setObjectName("label_69")

        self.formLayout_5.setWidget(4, QFormLayout.ItemRole.LabelRole, self.label_69)

        self.txtdia_pago2 = QSpinBox(self.frame_9)
        self.txtdia_pago2.setObjectName("txtdia_pago2")

        self.formLayout_5.setWidget(
            4, QFormLayout.ItemRole.FieldRole, self.txtdia_pago2
        )

        self.label_32 = QLabel(self.frame_9)
        self.label_32.setObjectName("label_32")
        self.label_32.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.formLayout_5.setWidget(5, QFormLayout.ItemRole.LabelRole, self.label_32)

        self.txtporc_dto_cliente = QLineEdit(self.frame_9)
        self.txtporc_dto_cliente.setObjectName("txtporc_dto_cliente")
        self.txtporc_dto_cliente.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.formLayout_5.setWidget(
            5, QFormLayout.ItemRole.FieldRole, self.txtporc_dto_cliente
        )

        self.gridLayout_16.addWidget(self.frame_9, 0, 0, 1, 1)

        self.frame_6 = QFrame(self.tab_Datos_bancarios_financieros)
        self.frame_6.setObjectName("frame_6")
        self.frame_6.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_15 = QGridLayout(self.frame_6)
        self.gridLayout_15.setObjectName("gridLayout_15")
        self.pushButton = QPushButton(self.frame_6)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setMinimumSize(QSize(0, 27))

        self.gridLayout_15.addWidget(self.pushButton, 1, 0, 1, 2)

        self.label_72 = QLabel(self.frame_6)
        self.label_72.setObjectName("label_72")

        self.gridLayout_15.addWidget(self.label_72, 3, 0, 1, 1)

        self.txtcuenta_iva_repercutido = QLineEdit(self.frame_6)
        self.txtcuenta_iva_repercutido.setObjectName("txtcuenta_iva_repercutido")

        self.gridLayout_15.addWidget(self.txtcuenta_iva_repercutido, 3, 1, 1, 1)

        self.label_74 = QLabel(self.frame_6)
        self.label_74.setObjectName("label_74")

        self.gridLayout_15.addWidget(self.label_74, 5, 0, 1, 1)

        self.label_70 = QLabel(self.frame_6)
        self.label_70.setObjectName("label_70")

        self.gridLayout_15.addWidget(self.label_70, 0, 0, 1, 1)

        self.txtcuenta_deudas = QLineEdit(self.frame_6)
        self.txtcuenta_deudas.setObjectName("txtcuenta_deudas")

        self.gridLayout_15.addWidget(self.txtcuenta_deudas, 4, 1, 1, 1)

        self.txtcuenta_contable = QLineEdit(self.frame_6)
        self.txtcuenta_contable.setObjectName("txtcuenta_contable")

        self.gridLayout_15.addWidget(self.txtcuenta_contable, 2, 1, 1, 1)

        self.label_73 = QLabel(self.frame_6)
        self.label_73.setObjectName("label_73")

        self.gridLayout_15.addWidget(self.label_73, 4, 0, 1, 1)

        self.label_71 = QLabel(self.frame_6)
        self.label_71.setObjectName("label_71")

        self.gridLayout_15.addWidget(self.label_71, 2, 0, 1, 1)

        self.txtcuenta_cobros = QLineEdit(self.frame_6)
        self.txtcuenta_cobros.setObjectName("txtcuenta_cobros")

        self.gridLayout_15.addWidget(self.txtcuenta_cobros, 5, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.gridLayout_15.addItem(self.verticalSpacer_2, 6, 1, 1, 1)

        self.gridLayout_16.addWidget(self.frame_6, 0, 1, 1, 1)

        self.frame_7 = QFrame(self.tab_Datos_bancarios_financieros)
        self.frame_7.setObjectName("frame_7")
        self.frame_7.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_14 = QGridLayout(self.frame_7)
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.label_75 = QLabel(self.frame_7)
        self.label_75.setObjectName("label_75")
        sizePolicy5 = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum
        )
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.label_75.sizePolicy().hasHeightForWidth())
        self.label_75.setSizePolicy(sizePolicy5)

        self.gridLayout_14.addWidget(self.label_75, 0, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.chkClienteEmpresa = QCheckBox(self.frame_7)
        self.chkClienteEmpresa.setObjectName("chkClienteEmpresa")

        self.horizontalLayout_3.addWidget(self.chkClienteEmpresa)

        self.chkrecargo_equivalencia = QCheckBox(self.frame_7)
        self.chkrecargo_equivalencia.setObjectName("chkrecargo_equivalencia")

        self.horizontalLayout_3.addWidget(self.chkrecargo_equivalencia)

        self.gridLayout_14.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)

        self.gridLayout_31 = QGridLayout()
        self.gridLayout_31.setObjectName("gridLayout_31")
        self.label_76 = QLabel(self.frame_7)
        self.label_76.setObjectName("label_76")

        self.gridLayout_31.addWidget(self.label_76, 0, 0, 1, 1)

        self.label_77 = QLabel(self.frame_7)
        self.label_77.setObjectName("label_77")

        self.gridLayout_31.addWidget(self.label_77, 1, 0, 1, 1)

        self.lblCuentavalida = QLabel(self.frame_7)
        self.lblCuentavalida.setObjectName("lblCuentavalida")

        self.gridLayout_31.addWidget(self.lblCuentavalida, 6, 3, 1, 1)

        self.label_78 = QLabel(self.frame_7)
        self.label_78.setObjectName("label_78")

        self.gridLayout_31.addWidget(self.label_78, 2, 0, 1, 1)

        self.txtentidad_bancaria = QLineEdit(self.frame_7)
        self.txtentidad_bancaria.setObjectName("txtentidad_bancaria")
        self.txtentidad_bancaria.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout_31.addWidget(self.txtentidad_bancaria, 2, 1, 1, 3)

        self.txtimporte_a_cuenta = QLineEdit(self.frame_7)
        self.txtimporte_a_cuenta.setObjectName("txtimporte_a_cuenta")
        self.txtimporte_a_cuenta.setEnabled(False)
        self.txtimporte_a_cuenta.setMaximumSize(QSize(150, 16777215))
        self.txtimporte_a_cuenta.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.txtimporte_a_cuenta.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_31.addWidget(self.txtimporte_a_cuenta, 0, 1, 1, 1)

        self.txtvales = QLineEdit(self.frame_7)
        self.txtvales.setObjectName("txtvales")
        self.txtvales.setEnabled(False)
        self.txtvales.setMaximumSize(QSize(150, 16777215))
        self.txtvales.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.txtvales.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_31.addWidget(self.txtvales, 1, 1, 1, 1)

        self.gridLayout_14.addLayout(self.gridLayout_31, 2, 0, 1, 1)

        self.groupBox = QGroupBox(self.frame_7)
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setMinimumSize(QSize(182, 0))
        self.gridLayout_29 = QGridLayout(self.groupBox)
        self.gridLayout_29.setObjectName("gridLayout_29")
        self.radUE = QRadioButton(self.groupBox)
        self.radUE.setObjectName("radUE")

        self.gridLayout_29.addWidget(self.radUE, 0, 1, 1, 1)

        self.radGeneral = QRadioButton(self.groupBox)
        self.radGeneral.setObjectName("radGeneral")
        self.radGeneral.setChecked(True)

        self.gridLayout_29.addWidget(self.radGeneral, 0, 0, 1, 1)

        self.radExcento = QRadioButton(self.groupBox)
        self.radExcento.setObjectName("radExcento")

        self.gridLayout_29.addWidget(self.radExcento, 1, 0, 1, 1)

        self.radExportacion = QRadioButton(self.groupBox)
        self.radExportacion.setObjectName("radExportacion")

        self.gridLayout_29.addWidget(self.radExportacion, 1, 1, 1, 1)

        self.gridLayout_14.addWidget(self.groupBox, 2, 1, 1, 1)

        self.gridLayout_10 = QGridLayout()
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.label_45 = QLabel(self.frame_7)
        self.label_45.setObjectName("label_45")

        self.gridLayout_10.addWidget(self.label_45, 0, 1, 1, 1)

        self.label_59 = QLabel(self.frame_7)
        self.label_59.setObjectName("label_59")

        self.gridLayout_10.addWidget(self.label_59, 0, 2, 1, 1)

        self.label_60 = QLabel(self.frame_7)
        self.label_60.setObjectName("label_60")

        self.gridLayout_10.addWidget(self.label_60, 0, 3, 1, 1)

        self.label_61 = QLabel(self.frame_7)
        self.label_61.setObjectName("label_61")

        self.gridLayout_10.addWidget(self.label_61, 0, 4, 1, 1)

        self.label_26 = QLabel(self.frame_7)
        self.label_26.setObjectName("label_26")

        self.gridLayout_10.addWidget(self.label_26, 1, 0, 1, 1)

        self.txtvisa_distancia1 = QLineEdit(self.frame_7)
        self.txtvisa_distancia1.setObjectName("txtvisa_distancia1")
        self.txtvisa_distancia1.setMinimumSize(QSize(133, 0))

        self.gridLayout_10.addWidget(self.txtvisa_distancia1, 1, 1, 1, 1)

        self.txtvisa1_caduca_mes = QLineEdit(self.frame_7)
        self.txtvisa1_caduca_mes.setObjectName("txtvisa1_caduca_mes")
        self.txtvisa1_caduca_mes.setMaximumSize(QSize(47, 16777215))

        self.gridLayout_10.addWidget(self.txtvisa1_caduca_mes, 1, 2, 1, 1)

        self.txtvisa1_caduca_ano = QLineEdit(self.frame_7)
        self.txtvisa1_caduca_ano.setObjectName("txtvisa1_caduca_ano")
        self.txtvisa1_caduca_ano.setMaximumSize(QSize(47, 16777215))

        self.gridLayout_10.addWidget(self.txtvisa1_caduca_ano, 1, 3, 1, 1)

        self.txtvisa1_cod_valid = QLineEdit(self.frame_7)
        self.txtvisa1_cod_valid.setObjectName("txtvisa1_cod_valid")
        self.txtvisa1_cod_valid.setMaximumSize(QSize(47, 16777215))

        self.gridLayout_10.addWidget(self.txtvisa1_cod_valid, 1, 4, 1, 1)

        self.label_41 = QLabel(self.frame_7)
        self.label_41.setObjectName("label_41")

        self.gridLayout_10.addWidget(self.label_41, 2, 0, 1, 1)

        self.txtvisa_distancia2 = QLineEdit(self.frame_7)
        self.txtvisa_distancia2.setObjectName("txtvisa_distancia2")
        self.txtvisa_distancia2.setMinimumSize(QSize(133, 0))

        self.gridLayout_10.addWidget(self.txtvisa_distancia2, 2, 1, 1, 1)

        self.txtvisa2_caduca_mes = QLineEdit(self.frame_7)
        self.txtvisa2_caduca_mes.setObjectName("txtvisa2_caduca_mes")
        self.txtvisa2_caduca_mes.setMaximumSize(QSize(47, 16777215))

        self.gridLayout_10.addWidget(self.txtvisa2_caduca_mes, 2, 2, 1, 1)

        self.txtvisa2_caduca_ano = QLineEdit(self.frame_7)
        self.txtvisa2_caduca_ano.setObjectName("txtvisa2_caduca_ano")
        self.txtvisa2_caduca_ano.setMaximumSize(QSize(47, 16777215))

        self.gridLayout_10.addWidget(self.txtvisa2_caduca_ano, 2, 3, 1, 1)

        self.txtvisa2_cod_valid = QLineEdit(self.frame_7)
        self.txtvisa2_cod_valid.setObjectName("txtvisa2_cod_valid")
        self.txtvisa2_cod_valid.setMaximumSize(QSize(47, 16777215))

        self.gridLayout_10.addWidget(self.txtvisa2_cod_valid, 2, 4, 1, 1)

        self.gridLayout_14.addLayout(self.gridLayout_10, 3, 0, 1, 1)

        self.gridLayout_16.addWidget(self.frame_7, 1, 0, 1, 2)

        self.tabwidget.addTab(self.tab_Datos_bancarios_financieros, "")
        self.tab_estadistica = QWidget()
        self.tab_estadistica.setObjectName("tab_estadistica")
        self.tab_estadistica.setStyleSheet("")
        self.gridLayout_24 = QGridLayout(self.tab_estadistica)
        self.gridLayout_24.setObjectName("gridLayout_24")
        self.gridLayout_66 = QGridLayout()
        self.gridLayout_66.setObjectName("gridLayout_66")
        self.verticalSpacer_4 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.gridLayout_66.addItem(self.verticalSpacer_4, 4, 0, 1, 1)

        self.txtdeuda_actual = QLineEdit(self.tab_estadistica)
        self.txtdeuda_actual.setObjectName("txtdeuda_actual")
        self.txtdeuda_actual.setEnabled(True)
        self.txtdeuda_actual.setMaximumSize(QSize(100, 16777215))
        self.txtdeuda_actual.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.txtdeuda_actual.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.txtdeuda_actual.setReadOnly(True)

        self.gridLayout_66.addWidget(self.txtdeuda_actual, 2, 1, 1, 1)

        self.txtventas_ejercicio = QLineEdit(self.tab_estadistica)
        self.txtventas_ejercicio.setObjectName("txtventas_ejercicio")
        self.txtventas_ejercicio.setEnabled(True)
        self.txtventas_ejercicio.setMaximumSize(QSize(100, 16777215))
        self.txtventas_ejercicio.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.txtventas_ejercicio.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.txtventas_ejercicio.setReadOnly(True)

        self.gridLayout_66.addWidget(self.txtventas_ejercicio, 3, 1, 1, 1)

        self.txtfecha_ultima_compra = QDateEdit(self.tab_estadistica)
        self.txtfecha_ultima_compra.setObjectName("txtfecha_ultima_compra")
        self.txtfecha_ultima_compra.setEnabled(True)
        self.txtfecha_ultima_compra.setMaximumSize(QSize(100, 16777215))
        self.txtfecha_ultima_compra.setStyleSheet("")
        self.txtfecha_ultima_compra.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.txtfecha_ultima_compra.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.txtfecha_ultima_compra.setCalendarPopup(True)

        self.gridLayout_66.addWidget(self.txtfecha_ultima_compra, 1, 1, 1, 1)

        self.txtimporteAcumulado = QLineEdit(self.tab_estadistica)
        self.txtimporteAcumulado.setObjectName("txtimporteAcumulado")
        self.txtimporteAcumulado.setEnabled(True)
        self.txtimporteAcumulado.setMaximumSize(QSize(100, 16777215))
        self.txtimporteAcumulado.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.txtimporteAcumulado.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.txtimporteAcumulado.setReadOnly(True)

        self.gridLayout_66.addWidget(self.txtimporteAcumulado, 0, 1, 1, 1)

        self.label_37 = QLabel(self.tab_estadistica)
        self.label_37.setObjectName("label_37")
        self.label_37.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_66.addWidget(self.label_37, 1, 0, 1, 1)

        self.label_38 = QLabel(self.tab_estadistica)
        self.label_38.setObjectName("label_38")
        self.label_38.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_66.addWidget(self.label_38, 2, 0, 1, 1)

        self.label_39 = QLabel(self.tab_estadistica)
        self.label_39.setObjectName("label_39")
        self.label_39.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_66.addWidget(self.label_39, 3, 0, 1, 1)

        self.label_36 = QLabel(self.tab_estadistica)
        self.label_36.setObjectName("label_36")
        self.label_36.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_66.addWidget(self.label_36, 0, 0, 1, 1)

        self.gridLayout_24.addLayout(self.gridLayout_66, 0, 1, 1, 1)

        self.gridLayout_23 = QGridLayout()
        self.gridLayout_23.setObjectName("gridLayout_23")
        self.txtSeptiembre = QLineEdit(self.tab_estadistica)
        self.txtSeptiembre.setObjectName("txtSeptiembre")
        self.txtSeptiembre.setEnabled(True)
        self.txtSeptiembre.setMaximumSize(QSize(120, 16777215))
        self.txtSeptiembre.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.txtSeptiembre.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.txtSeptiembre.setReadOnly(True)

        self.gridLayout_23.addWidget(self.txtSeptiembre, 2, 3, 1, 1)

        self.label_56 = QLabel(self.tab_estadistica)
        self.label_56.setObjectName("label_56")
        self.label_56.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_23.addWidget(self.label_56, 5, 2, 1, 1)

        self.label_57 = QLabel(self.tab_estadistica)
        self.label_57.setObjectName("label_57")
        self.label_57.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_23.addWidget(self.label_57, 3, 2, 1, 1)

        self.label_55 = QLabel(self.tab_estadistica)
        self.label_55.setObjectName("label_55")
        self.label_55.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_23.addWidget(self.label_55, 1, 2, 1, 1)

        self.label_54 = QLabel(self.tab_estadistica)
        self.label_54.setObjectName("label_54")
        self.label_54.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_23.addWidget(self.label_54, 0, 2, 1, 1)

        self.txtAgosto = QLineEdit(self.tab_estadistica)
        self.txtAgosto.setObjectName("txtAgosto")
        self.txtAgosto.setEnabled(True)
        self.txtAgosto.setMaximumSize(QSize(120, 16777215))
        self.txtAgosto.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.txtAgosto.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.txtAgosto.setReadOnly(True)

        self.gridLayout_23.addWidget(self.txtAgosto, 1, 3, 1, 1)

        self.label_53 = QLabel(self.tab_estadistica)
        self.label_53.setObjectName("label_53")
        self.label_53.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_23.addWidget(self.label_53, 4, 2, 1, 1)

        self.txtMarzo = QLineEdit(self.tab_estadistica)
        self.txtMarzo.setObjectName("txtMarzo")
        self.txtMarzo.setEnabled(True)
        self.txtMarzo.setMaximumSize(QSize(120, 16777215))
        self.txtMarzo.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.txtMarzo.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.txtMarzo.setReadOnly(True)

        self.gridLayout_23.addWidget(self.txtMarzo, 2, 1, 1, 1)

        self.txtEnero = QLineEdit(self.tab_estadistica)
        self.txtEnero.setObjectName("txtEnero")
        self.txtEnero.setEnabled(True)
        self.txtEnero.setMaximumSize(QSize(120, 16777215))
        self.txtEnero.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.txtEnero.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.txtEnero.setReadOnly(True)

        self.gridLayout_23.addWidget(self.txtEnero, 0, 1, 1, 1)

        self.label_51 = QLabel(self.tab_estadistica)
        self.label_51.setObjectName("label_51")
        self.label_51.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_23.addWidget(self.label_51, 4, 0, 1, 1)

        self.txtFebrero = QLineEdit(self.tab_estadistica)
        self.txtFebrero.setObjectName("txtFebrero")
        self.txtFebrero.setEnabled(True)
        self.txtFebrero.setMaximumSize(QSize(120, 16777215))
        self.txtFebrero.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.txtFebrero.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.txtFebrero.setReadOnly(True)

        self.gridLayout_23.addWidget(self.txtFebrero, 1, 1, 1, 1)

        self.label_48 = QLabel(self.tab_estadistica)
        self.label_48.setObjectName("label_48")
        self.label_48.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_23.addWidget(self.label_48, 1, 0, 1, 1)

        self.label_58 = QLabel(self.tab_estadistica)
        self.label_58.setObjectName("label_58")
        self.label_58.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_23.addWidget(self.label_58, 2, 2, 1, 1)

        self.txtJunio = QLineEdit(self.tab_estadistica)
        self.txtJunio.setObjectName("txtJunio")
        self.txtJunio.setEnabled(True)
        self.txtJunio.setMaximumSize(QSize(120, 16777215))
        self.txtJunio.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.txtJunio.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.txtJunio.setReadOnly(True)

        self.gridLayout_23.addWidget(self.txtJunio, 5, 1, 1, 1)

        self.label_50 = QLabel(self.tab_estadistica)
        self.label_50.setObjectName("label_50")
        self.label_50.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_23.addWidget(self.label_50, 3, 0, 1, 1)

        self.txtNoviembre = QLineEdit(self.tab_estadistica)
        self.txtNoviembre.setObjectName("txtNoviembre")
        self.txtNoviembre.setEnabled(True)
        self.txtNoviembre.setMaximumSize(QSize(120, 16777215))
        self.txtNoviembre.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.txtNoviembre.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.txtNoviembre.setReadOnly(True)

        self.gridLayout_23.addWidget(self.txtNoviembre, 4, 3, 1, 1)

        self.txtOctubre = QLineEdit(self.tab_estadistica)
        self.txtOctubre.setObjectName("txtOctubre")
        self.txtOctubre.setEnabled(True)
        self.txtOctubre.setMaximumSize(QSize(120, 16777215))
        self.txtOctubre.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.txtOctubre.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.txtOctubre.setReadOnly(True)

        self.gridLayout_23.addWidget(self.txtOctubre, 3, 3, 1, 1)

        self.txtjulio = QLineEdit(self.tab_estadistica)
        self.txtjulio.setObjectName("txtjulio")
        self.txtjulio.setEnabled(True)
        self.txtjulio.setMaximumSize(QSize(120, 16777215))
        self.txtjulio.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.txtjulio.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.txtjulio.setReadOnly(True)

        self.gridLayout_23.addWidget(self.txtjulio, 0, 3, 1, 1)

        self.label_52 = QLabel(self.tab_estadistica)
        self.label_52.setObjectName("label_52")
        self.label_52.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_23.addWidget(self.label_52, 5, 0, 1, 1)

        self.label_49 = QLabel(self.tab_estadistica)
        self.label_49.setObjectName("label_49")
        self.label_49.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_23.addWidget(self.label_49, 2, 0, 1, 1)

        self.txtAbril = QLineEdit(self.tab_estadistica)
        self.txtAbril.setObjectName("txtAbril")
        self.txtAbril.setEnabled(True)
        self.txtAbril.setMaximumSize(QSize(120, 16777215))
        self.txtAbril.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.txtAbril.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.txtAbril.setReadOnly(True)

        self.gridLayout_23.addWidget(self.txtAbril, 3, 1, 1, 1)

        self.label_47 = QLabel(self.tab_estadistica)
        self.label_47.setObjectName("label_47")
        self.label_47.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_23.addWidget(self.label_47, 0, 0, 1, 1)

        self.txtMayo = QLineEdit(self.tab_estadistica)
        self.txtMayo.setObjectName("txtMayo")
        self.txtMayo.setEnabled(True)
        self.txtMayo.setMaximumSize(QSize(120, 16777215))
        self.txtMayo.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.txtMayo.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.txtMayo.setReadOnly(True)

        self.gridLayout_23.addWidget(self.txtMayo, 4, 1, 1, 1)

        self.txtDiciembre = QLineEdit(self.tab_estadistica)
        self.txtDiciembre.setObjectName("txtDiciembre")
        self.txtDiciembre.setEnabled(True)
        self.txtDiciembre.setMaximumSize(QSize(120, 16777215))
        self.txtDiciembre.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.txtDiciembre.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.txtDiciembre.setReadOnly(True)

        self.gridLayout_23.addWidget(self.txtDiciembre, 5, 3, 1, 1)

        self.ChartWidget = QWidget(self.tab_estadistica)
        self.ChartWidget.setObjectName("ChartWidget")

        self.gridLayout_23.addWidget(self.ChartWidget, 6, 0, 1, 4)

        self.gridLayout_24.addLayout(self.gridLayout_23, 0, 0, 1, 1)

        self.tabwidget.addTab(self.tab_estadistica, "")
        self.tab_deudas = QWidget()
        self.tab_deudas.setObjectName("tab_deudas")
        self.tab_deudas.setStyleSheet("")
        self.gridLayout_20 = QGridLayout(self.tab_deudas)
        self.gridLayout_20.setObjectName("gridLayout_20")
        self.btnCobroTotal = QPushButton(self.tab_deudas)
        self.btnCobroTotal.setObjectName("btnCobroTotal")
        icon14 = QIcon()
        icon14.addFile(
            ":/Icons/PNG/Fp.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.btnCobroTotal.setIcon(icon14)
        self.btnCobroTotal.setIconSize(QSize(34, 34))

        self.gridLayout_20.addWidget(self.btnCobroTotal, 3, 1, 1, 1)

        self.label_83 = QLabel(self.tab_deudas)
        self.label_83.setObjectName("label_83")
        self.label_83.setStyleSheet("background: #304163;\n" "color: rgb(255,255,255);")
        self.label_83.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_20.addWidget(self.label_83, 0, 0, 1, 1)

        self.frame = QFrame(self.tab_deudas)
        self.frame.setObjectName("frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.radPendientes = QRadioButton(self.frame)
        self.radPendientes.setObjectName("radPendientes")
        self.radPendientes.setChecked(True)

        self.verticalLayout.addWidget(self.radPendientes)

        self.radPagadas = QRadioButton(self.frame)
        self.radPagadas.setObjectName("radPagadas")

        self.verticalLayout.addWidget(self.radPagadas)

        self.gridLayout_20.addWidget(self.frame, 1, 1, 1, 1)

        self.TablaDeudas = QTableView(self.tab_deudas)
        self.TablaDeudas.setObjectName("TablaDeudas")
        self.TablaDeudas.setAlternatingRowColors(True)
        self.TablaDeudas.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.TablaDeudas.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.TablaDeudas.horizontalHeader().setStretchLastSection(True)

        self.gridLayout_20.addWidget(self.TablaDeudas, 1, 0, 4, 1)

        self.verticalSpacer_5 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.gridLayout_20.addItem(self.verticalSpacer_5, 2, 1, 1, 1)

        self.label_84 = QLabel(self.tab_deudas)
        self.label_84.setObjectName("label_84")
        self.label_84.setStyleSheet("background: #304163;\n" "color: rgb(255,255,255);")
        self.label_84.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_20.addWidget(self.label_84, 5, 0, 1, 2)

        self.tablahistorial_deudas = QTableView(self.tab_deudas)
        self.tablahistorial_deudas.setObjectName("tablahistorial_deudas")

        self.gridLayout_20.addWidget(self.tablahistorial_deudas, 6, 0, 1, 2)

        self.tabwidget.addTab(self.tab_deudas, "")
        self.tab_coments = QWidget()
        self.tab_coments.setObjectName("tab_coments")
        self.tab_coments.setStyleSheet("")
        self.gridLayout_18 = QGridLayout(self.tab_coments)
        self.gridLayout_18.setObjectName("gridLayout_18")
        self.frame_5 = QFrame(self.tab_coments)
        self.frame_5.setObjectName("frame_5")
        self.frame_5.setMinimumSize(QSize(0, 100))
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_9 = QGridLayout(self.frame_5)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.gridLayout_8 = QGridLayout()
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.label_35 = QLabel(self.frame_5)
        self.label_35.setObjectName("label_35")

        self.gridLayout_8.addWidget(self.label_35, 1, 0, 1, 1)

        self.txtfecha_alta = QDateEdit(self.frame_5)
        self.txtfecha_alta.setObjectName("txtfecha_alta")
        self.txtfecha_alta.setMaximumSize(QSize(100, 16777215))
        self.txtfecha_alta.setStyleSheet("")
        self.txtfecha_alta.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.txtfecha_alta.setCalendarPopup(True)

        self.gridLayout_8.addWidget(self.txtfecha_alta, 0, 2, 1, 1)

        self.txtrRiesgoPermitido = QLineEdit(self.frame_5)
        self.txtrRiesgoPermitido.setObjectName("txtrRiesgoPermitido")
        self.txtrRiesgoPermitido.setEnabled(True)
        self.txtrRiesgoPermitido.setMaximumSize(QSize(100, 16777215))
        self.txtrRiesgoPermitido.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_8.addWidget(self.txtrRiesgoPermitido, 1, 2, 1, 1)

        self.label_34 = QLabel(self.frame_5)
        self.label_34.setObjectName("label_34")

        self.gridLayout_8.addWidget(self.label_34, 0, 0, 1, 1)

        self.cboagente = QComboBox(self.frame_5)
        self.cboagente.setObjectName("cboagente")
        self.cboagente.setMinimumSize(QSize(200, 0))

        self.gridLayout_8.addWidget(self.cboagente, 0, 4, 1, 2)

        self.label_62 = QLabel(self.frame_5)
        self.label_62.setObjectName("label_62")

        self.gridLayout_8.addWidget(self.label_62, 2, 0, 1, 1)

        self.label_63 = QLabel(self.frame_5)
        self.label_63.setObjectName("label_63")

        self.gridLayout_8.addWidget(self.label_63, 0, 3, 1, 1)

        self.cbotransportista = QComboBox(self.frame_5)
        self.cbotransportista.setObjectName("cbotransportista")

        self.gridLayout_8.addWidget(self.cbotransportista, 2, 2, 1, 4)

        self.gridLayout_9.addLayout(self.gridLayout_8, 0, 0, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.gridLayout_9.addItem(self.horizontalSpacer_6, 0, 1, 1, 1)

        self.gridLayout_18.addWidget(self.frame_5, 3, 0, 1, 4)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.chklBloqueoCliente = QCheckBox(self.tab_coments)
        self.chklBloqueoCliente.setObjectName("chklBloqueoCliente")

        self.verticalLayout_6.addWidget(self.chklBloqueoCliente)

        self.txtcomentario_bloqueo = QTextEdit(self.tab_coments)
        self.txtcomentario_bloqueo.setObjectName("txtcomentario_bloqueo")
        self.txtcomentario_bloqueo.setEnabled(True)
        self.txtcomentario_bloqueo.setUndoRedoEnabled(True)
        self.txtcomentario_bloqueo.setReadOnly(True)

        self.verticalLayout_6.addWidget(self.txtcomentario_bloqueo)

        self.label_43 = QLabel(self.tab_coments)
        self.label_43.setObjectName("label_43")

        self.verticalLayout_6.addWidget(self.label_43)

        self.txtacceso_web = QLineEdit(self.tab_coments)
        self.txtacceso_web.setObjectName("txtacceso_web")

        self.verticalLayout_6.addWidget(self.txtacceso_web)

        self.label_44 = QLabel(self.tab_coments)
        self.label_44.setObjectName("label_44")

        self.verticalLayout_6.addWidget(self.label_44)

        self.txtpassword_web = QLineEdit(self.tab_coments)
        self.txtpassword_web.setObjectName("txtpassword_web")

        self.verticalLayout_6.addWidget(self.txtpassword_web)

        self.gridLayout_18.addLayout(self.verticalLayout_6, 0, 0, 3, 1)

        self.label_82 = QLabel(self.tab_coments)
        self.label_82.setObjectName("label_82")
        self.label_82.setMaximumSize(QSize(16777215, 21))

        self.gridLayout_18.addWidget(self.label_82, 0, 1, 1, 2)

        self.cboidiomaDocumentos = QComboBox(self.tab_coments)
        self.cboidiomaDocumentos.setObjectName("cboidiomaDocumentos")

        self.gridLayout_18.addWidget(self.cboidiomaDocumentos, 2, 3, 1, 1)

        self.label_9 = QLabel(self.tab_coments)
        self.label_9.setObjectName("label_9")

        self.gridLayout_18.addWidget(self.label_9, 2, 2, 1, 1)

        self.txtcomentarios = QTextEdit(self.tab_coments)
        self.txtcomentarios.setObjectName("txtcomentarios")

        self.gridLayout_18.addWidget(self.txtcomentarios, 1, 1, 1, 3)

        self.tabwidget.addTab(self.tab_coments, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_22 = QGridLayout(self.tab_3)
        self.gridLayout_22.setObjectName("gridLayout_22")
        self.frame_3 = QFrame(self.tab_3)
        self.frame_3.setObjectName("frame_3")
        self.frame_3.setMinimumSize(QSize(250, 0))
        self.frame_3.setMaximumSize(QSize(16777215, 16777215))
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.tabWidget_2 = QTabWidget(self.frame_3)
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tabWidget_2.setAutoFillBackground(False)
        self.tabWidget_2.setTabPosition(QTabWidget.TabPosition.North)
        self.tabWidget_2.setTabShape(QTabWidget.TabShape.Rounded)
        self.tabWidget_2.setMovable(True)
        self.tab_13 = QWidget()
        self.tab_13.setObjectName("tab_13")
        self.gridLayout_19 = QGridLayout(self.tab_13)
        self.gridLayout_19.setObjectName("gridLayout_19")
        self.tablaPresupuestos = QTableView(self.tab_13)
        self.tablaPresupuestos.setObjectName("tablaPresupuestos")
        self.tablaPresupuestos.setAlternatingRowColors(True)
        self.tablaPresupuestos.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.tablaPresupuestos.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.tablaPresupuestos.horizontalHeader().setStretchLastSection(True)

        self.gridLayout_19.addWidget(self.tablaPresupuestos, 0, 0, 1, 1)

        self.tabWidget_2.addTab(self.tab_13, "")
        self.tab_9 = QWidget()
        self.tab_9.setObjectName("tab_9")
        self.gridLayout_26 = QGridLayout(self.tab_9)
        self.gridLayout_26.setObjectName("gridLayout_26")
        self.tablaPedidos = QTableView(self.tab_9)
        self.tablaPedidos.setObjectName("tablaPedidos")
        self.tablaPedidos.setAlternatingRowColors(True)
        self.tablaPedidos.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.tablaPedidos.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.tablaPedidos.horizontalHeader().setStretchLastSection(True)

        self.gridLayout_26.addWidget(self.tablaPedidos, 0, 0, 1, 1)

        self.tabWidget_2.addTab(self.tab_9, "")
        self.tab_7 = QWidget()
        self.tab_7.setObjectName("tab_7")
        self.gridLayout_6 = QGridLayout(self.tab_7)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.TablaAlbaranes = QTableView(self.tab_7)
        self.TablaAlbaranes.setObjectName("TablaAlbaranes")
        self.TablaAlbaranes.setAlternatingRowColors(True)
        self.TablaAlbaranes.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.TablaAlbaranes.horizontalHeader().setStretchLastSection(True)

        self.gridLayout_6.addWidget(self.TablaAlbaranes, 0, 0, 1, 1)

        self.tabWidget_2.addTab(self.tab_7, "")
        self.tab_Facturas = QWidget()
        self.tab_Facturas.setObjectName("tab_Facturas")
        self.gridLayout_11 = QGridLayout(self.tab_Facturas)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.tablaFacturas = QTableView(self.tab_Facturas)
        self.tablaFacturas.setObjectName("tablaFacturas")
        self.tablaFacturas.setAlternatingRowColors(True)
        self.tablaFacturas.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.tablaFacturas.horizontalHeader().setStretchLastSection(True)

        self.gridLayout_11.addWidget(self.tablaFacturas, 0, 0, 1, 1)

        self.tabWidget_2.addTab(self.tab_Facturas, "")
        self.tab_12 = QWidget()
        self.tab_12.setObjectName("tab_12")
        self.gridLayout_13 = QGridLayout(self.tab_12)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.tablaVales = QTableView(self.tab_12)
        self.tablaVales.setObjectName("tablaVales")
        self.tablaVales.setAlternatingRowColors(True)
        self.tablaVales.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.tablaVales.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.tablaVales.horizontalHeader().setStretchLastSection(True)

        self.gridLayout_13.addWidget(self.tablaVales, 0, 0, 1, 1)

        self.tabWidget_2.addTab(self.tab_12, "")

        self.horizontalLayout_5.addWidget(self.tabWidget_2)

        self.frameConta = QFrame(self.frame_3)
        self.frameConta.setObjectName("frameConta")
        self.frameConta.setMinimumSize(QSize(0, 0))
        self.frameConta.setMaximumSize(QSize(373, 16777215))
        self.frameConta.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameConta.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_21 = QGridLayout(self.frameConta)
        self.gridLayout_21.setObjectName("gridLayout_21")
        self.tablaAsientos = QTableView(self.frameConta)
        self.tablaAsientos.setObjectName("tablaAsientos")

        self.gridLayout_21.addWidget(self.tablaAsientos, 1, 0, 1, 1)

        self.label_10 = QLabel(self.frameConta)
        self.label_10.setObjectName("label_10")
        self.label_10.setStyleSheet("background: #304163;\n" "color: rgb(255,255,255);")
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_21.addWidget(self.label_10, 0, 0, 1, 1)

        self.horizontalLayout_5.addWidget(self.frameConta)

        self.gridLayout_22.addWidget(self.frame_3, 0, 0, 1, 1)

        self.tabwidget.addTab(self.tab_3, "")

        self.gridLayout_27.addWidget(self.tabwidget, 1, 1, 1, 1)

        self.stackedWidget.addWidget(self.paginaedicion)
        self.paginaBisquedas = QWidget()
        self.paginaBisquedas.setObjectName("paginaBisquedas")
        self.gridLayout_28 = QGridLayout(self.paginaBisquedas)
        self.gridLayout_28.setObjectName("gridLayout_28")
        self.gridLayout_28.setContentsMargins(-1, -1, 20, -1)
        self.tabla_busquedas = QTableView(self.paginaBisquedas)
        self.tabla_busquedas.setObjectName("tabla_busquedas")
        self.tabla_busquedas.setAutoFillBackground(True)
        self.tabla_busquedas.setAlternatingRowColors(True)
        self.tabla_busquedas.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.tabla_busquedas.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.tabla_busquedas.setGridStyle(Qt.PenStyle.DotLine)
        self.tabla_busquedas.setSortingEnabled(True)
        self.tabla_busquedas.setCornerButtonEnabled(False)
        self.tabla_busquedas.horizontalHeader().setStretchLastSection(True)
        self.tabla_busquedas.verticalHeader().setVisible(False)

        self.gridLayout_28.addWidget(self.tabla_busquedas, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.paginaBisquedas)

        self.gridLayout_3.addWidget(self.stackedWidget, 1, 0, 1, 5)

        QWidget.setTabOrder(self.btnAnadir, self.btnSiguiente)
        QWidget.setTabOrder(self.btnSiguiente, self.btnAnterior)
        QWidget.setTabOrder(self.btnAnterior, self.btnBuscar)
        QWidget.setTabOrder(self.btnBuscar, self.btnEditar)
        QWidget.setTabOrder(self.btnEditar, self.btnGuardar)
        QWidget.setTabOrder(self.btnGuardar, self.btnDeshacer)
        QWidget.setTabOrder(self.btnDeshacer, self.btnBorrar)
        QWidget.setTabOrder(self.btnBorrar, self.txtcodigo_cliente)
        QWidget.setTabOrder(self.txtcodigo_cliente, self.txtCifIntracomunitario)
        QWidget.setTabOrder(self.txtCifIntracomunitario, self.btnValidarVIES)
        QWidget.setTabOrder(self.btnValidarVIES, self.txtcif_nif)
        QWidget.setTabOrder(self.txtcif_nif, self.txtnombre)
        QWidget.setTabOrder(self.txtnombre, self.txtPrimerApellido)
        QWidget.setTabOrder(self.txtPrimerApellido, self.txtSegundoApellido)
        QWidget.setTabOrder(self.txtSegundoApellido, self.txtnombre_fiscal)
        QWidget.setTabOrder(self.txtnombre_fiscal, self.txtnombre_comercial)
        QWidget.setTabOrder(self.txtnombre_comercial, self.txtcp)
        QWidget.setTabOrder(self.txtcp, self.txtpoblacion)
        QWidget.setTabOrder(self.txtpoblacion, self.txtdireccion1)
        QWidget.setTabOrder(self.txtdireccion1, self.txtdireccion2)
        QWidget.setTabOrder(self.txtdireccion2, self.txtprovincia)
        QWidget.setTabOrder(self.txtprovincia, self.cboPais)
        QWidget.setTabOrder(self.cboPais, self.txttelefono1)
        QWidget.setTabOrder(self.txttelefono1, self.txttelefono2)
        QWidget.setTabOrder(self.txttelefono2, self.txtmovil)
        QWidget.setTabOrder(self.txtmovil, self.txtemail)
        QWidget.setTabOrder(self.txtemail, self.txtweb)
        QWidget.setTabOrder(self.txtweb, self.txtObservaciones)
        QWidget.setTabOrder(self.txtObservaciones, self.btnVer_OtrosContactos)
        QWidget.setTabOrder(self.btnVer_OtrosContactos, self.lista_tipos)
        QWidget.setTabOrder(self.lista_tipos, self.btnEdita_tipoCliente)
        QWidget.setTabOrder(self.btnEdita_tipoCliente, self.tabwidget)
        QWidget.setTabOrder(self.tabwidget, self.lista_direccionesAlternativas)
        QWidget.setTabOrder(
            self.lista_direccionesAlternativas, self.txtdescripcion_direccion
        )
        QWidget.setTabOrder(
            self.txtdescripcion_direccion, self.txtcpPoblacionAlternativa
        )
        QWidget.setTabOrder(
            self.txtcpPoblacionAlternativa, self.txtpoblacionAlternativa
        )
        QWidget.setTabOrder(
            self.txtpoblacionAlternativa, self.txtdireccion1Alternativa1
        )
        QWidget.setTabOrder(
            self.txtdireccion1Alternativa1, self.txtdireccion1Alternativa2
        )
        QWidget.setTabOrder(
            self.txtdireccion1Alternativa2, self.txtprovinciaAlternativa
        )
        QWidget.setTabOrder(self.txtprovinciaAlternativa, self.cbopaisAlternativa)
        QWidget.setTabOrder(self.cbopaisAlternativa, self.txtemail_alternativa)
        QWidget.setTabOrder(self.txtemail_alternativa, self.txtcomentarios_alternativa)
        QWidget.setTabOrder(self.txtcomentarios_alternativa, self.btnAnadirdireccion)
        QWidget.setTabOrder(self.btnAnadirdireccion, self.btnEditardireccionAlternativa)
        QWidget.setTabOrder(self.btnEditardireccionAlternativa, self.btnBorrardireccion)
        QWidget.setTabOrder(
            self.btnBorrardireccion, self.btnGuardardireccionAlternativa
        )
        QWidget.setTabOrder(
            self.btnGuardardireccionAlternativa, self.btnDeshacerdireccionAlternativa
        )
        QWidget.setTabOrder(
            self.btnDeshacerdireccionAlternativa, self.cbotarifa_cliente
        )
        QWidget.setTabOrder(self.cbotarifa_cliente, self.cboDivisa)
        QWidget.setTabOrder(self.cboDivisa, self.cboforma_pago)
        QWidget.setTabOrder(self.cboforma_pago, self.txtdia_pago1)
        QWidget.setTabOrder(self.txtdia_pago1, self.txtdia_pago2)
        QWidget.setTabOrder(self.txtdia_pago2, self.txtporc_dto_cliente)
        QWidget.setTabOrder(self.txtporc_dto_cliente, self.pushButton)
        QWidget.setTabOrder(self.pushButton, self.txtcuenta_contable)
        QWidget.setTabOrder(self.txtcuenta_contable, self.txtcuenta_iva_repercutido)
        QWidget.setTabOrder(self.txtcuenta_iva_repercutido, self.txtcuenta_deudas)
        QWidget.setTabOrder(self.txtcuenta_deudas, self.txtcuenta_cobros)
        QWidget.setTabOrder(self.txtcuenta_cobros, self.chkClienteEmpresa)
        QWidget.setTabOrder(self.chkClienteEmpresa, self.chkrecargo_equivalencia)
        QWidget.setTabOrder(self.chkrecargo_equivalencia, self.radGeneral)
        QWidget.setTabOrder(self.radGeneral, self.radUE)
        QWidget.setTabOrder(self.radUE, self.radExcento)
        QWidget.setTabOrder(self.radExcento, self.radExportacion)
        QWidget.setTabOrder(self.radExportacion, self.txtvisa_distancia1)
        QWidget.setTabOrder(self.txtvisa_distancia1, self.txtvisa1_caduca_mes)
        QWidget.setTabOrder(self.txtvisa1_caduca_mes, self.txtvisa1_caduca_ano)
        QWidget.setTabOrder(self.txtvisa1_caduca_ano, self.txtvisa1_cod_valid)
        QWidget.setTabOrder(self.txtvisa1_cod_valid, self.txtvisa_distancia2)
        QWidget.setTabOrder(self.txtvisa_distancia2, self.txtvisa2_caduca_mes)
        QWidget.setTabOrder(self.txtvisa2_caduca_mes, self.txtvisa2_caduca_ano)
        QWidget.setTabOrder(self.txtvisa2_caduca_ano, self.txtvisa2_cod_valid)
        QWidget.setTabOrder(self.txtvisa2_cod_valid, self.TablaDeudas)
        QWidget.setTabOrder(self.TablaDeudas, self.radPendientes)
        QWidget.setTabOrder(self.radPendientes, self.radPagadas)
        QWidget.setTabOrder(self.radPagadas, self.btnCobroTotal)
        QWidget.setTabOrder(self.btnCobroTotal, self.tablahistorial_deudas)
        QWidget.setTabOrder(self.tablahistorial_deudas, self.chklBloqueoCliente)
        QWidget.setTabOrder(self.chklBloqueoCliente, self.txtcomentario_bloqueo)
        QWidget.setTabOrder(self.txtcomentario_bloqueo, self.txtacceso_web)
        QWidget.setTabOrder(self.txtacceso_web, self.txtpassword_web)
        QWidget.setTabOrder(self.txtpassword_web, self.txtfecha_alta)
        QWidget.setTabOrder(self.txtfecha_alta, self.cboagente)
        QWidget.setTabOrder(self.cboagente, self.txtrRiesgoPermitido)
        QWidget.setTabOrder(self.txtrRiesgoPermitido, self.cbotransportista)
        QWidget.setTabOrder(self.cbotransportista, self.txtcomentarios)
        QWidget.setTabOrder(self.txtcomentarios, self.cboidiomaDocumentos)
        QWidget.setTabOrder(self.cboidiomaDocumentos, self.tabWidget_2)
        QWidget.setTabOrder(self.tabWidget_2, self.tablaPresupuestos)
        QWidget.setTabOrder(self.tablaPresupuestos, self.tablaAsientos)
        QWidget.setTabOrder(self.tablaAsientos, self.tablaPedidos)
        QWidget.setTabOrder(self.tablaPedidos, self.TablaAlbaranes)
        QWidget.setTabOrder(self.TablaAlbaranes, self.tablaFacturas)
        QWidget.setTabOrder(self.tablaFacturas, self.tablaVales)
        QWidget.setTabOrder(self.tablaVales, self.tabla_busquedas)

        self.retranslateUi(frmClientes)

        self.stackedWidget.setCurrentIndex(0)
        self.tabwidget.setCurrentIndex(0)
        self.blink_stack.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(frmClientes)

    # setupUi

    def retranslateUi(self, frmClientes):
        frmClientes.setWindowTitle(
            QCoreApplication.translate("frmClientes", "Gestion de clientes", None)
        )
        self.textoTitulo.setText(
            QCoreApplication.translate(
                "frmClientes", "Gesti\u00f3n de Clientes - Datos administrativos", None
            )
        )
        self.label_40.setText(
            QCoreApplication.translate("frmClientes", "Cliente:", None)
        )
        self.txtNombreFiscal.setText(
            QCoreApplication.translate("frmClientes", "TextLabel", None)
        )
        self.btnBorrar.setText(
            QCoreApplication.translate("frmClientes", "B&orrar", None)
        )
        self.btnGuardar.setText(
            QCoreApplication.translate("frmClientes", "&Guardar", None)
        )
        self.btnAnadir.setText(
            QCoreApplication.translate("frmClientes", "&Nuevo", None)
        )
        self.btnDeshacer.setText(
            QCoreApplication.translate("frmClientes", "&Deshacer", None)
        )
        self.btnEditar.setText(
            QCoreApplication.translate("frmClientes", "&Editar", None)
        )
        self.btnBuscar.setText(
            QCoreApplication.translate("frmClientes", "&Buscar", None)
        )
        self.btnAnterior.setText(
            QCoreApplication.translate("frmClientes", "&Anterior", None)
        )
        self.btnSiguiente.setText(
            QCoreApplication.translate("frmClientes", "&Siguiente", None)
        )
        # if QT_CONFIG(tooltip)
        self.btnVer_OtrosContactos.setToolTip(
            QCoreApplication.translate(
                "frmClientes", "Otras personas de contacto", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.btnVer_OtrosContactos.setText(
            QCoreApplication.translate("frmClientes", "Personas de contacto", None)
        )
        self.label_46.setText(
            QCoreApplication.translate("frmClientes", "TIPO CLIENTE", None)
        )
        self.btnEdita_tipoCliente.setText(
            QCoreApplication.translate("frmClientes", "Editar tipo de cliente", None)
        )
        ___qtreewidgetitem = self.lista_tipos.headerItem()
        ___qtreewidgetitem.setText(
            0, QCoreApplication.translate("frmClientes", "Tipo", None)
        )
        self.lista_tipos.setStyleSheet("")
        self.label_3.setStyleSheet("")
        self.label_3.setText(QCoreApplication.translate("frmClientes", "Nombre", None))
        self.btnValidarVIES.setStyleSheet("")
        self.btnValidarVIES.setText(
            QCoreApplication.translate("frmClientes", "Validar VIES", None)
        )
        self.lblProvincia.setStyleSheet("")
        self.lblProvincia.setText(
            QCoreApplication.translate("frmClientes", "Provincia:", None)
        )
        self.label_15.setStyleSheet("")
        self.label_15.setText(QCoreApplication.translate("frmClientes", "CP:", None))
        self.label_24.setStyleSheet("")
        self.label_24.setText(QCoreApplication.translate("frmClientes", "Mail:", None))
        self.label_16.setStyleSheet("")
        self.label_16.setText(
            QCoreApplication.translate("frmClientes", "Poblaci\u00f3n:", None)
        )
        self.label_22.setStyleSheet("")
        self.label_22.setText(
            QCoreApplication.translate("frmClientes", "M\u00f3vil:", None)
        )
        self.label_19.setStyleSheet("")
        self.label_19.setText(
            QCoreApplication.translate("frmClientes", "Tel\u00e9fono1:", None)
        )
        self.label_20.setStyleSheet("")
        self.label_20.setText(
            QCoreApplication.translate("frmClientes", "Tel\u00e9fono 2:", None)
        )
        self.label_13.setStyleSheet("")
        self.label_13.setText(
            QCoreApplication.translate("frmClientes", "Direcci\u00f3n:", None)
        )
        self.label_12.setStyleSheet("")
        self.label_12.setText(
            QCoreApplication.translate("frmClientes", "Nombre Comercial:", None)
        )
        self.lblCIF_IVA_UE.setStyleSheet("")
        self.lblCIF_IVA_UE.setText(
            QCoreApplication.translate("frmClientes", "CIF IVA UE:", None)
        )
        self.label_18.setStyleSheet("")
        self.label_18.setText(QCoreApplication.translate("frmClientes", "Pais:", None))
        self.label_14.setStyleSheet("")
        self.label_14.setText(
            QCoreApplication.translate("frmClientes", "Direccion 2:", None)
        )
        self.cboPais.setStyleSheet("")
        self.label_23.setStyleSheet("")
        self.label_23.setText(QCoreApplication.translate("frmClientes", "web:", None))
        self.label_11.setStyleSheet("")
        self.label_11.setText(
            QCoreApplication.translate("frmClientes", "Nombre Fiscal:", None)
        )
        self.label.setText(
            QCoreApplication.translate(
                "frmClientes", "C\u00f3digo:                        ", None
            )
        )
        self.label_25.setStyleSheet("")
        self.label_25.setText(
            QCoreApplication.translate("frmClientes", "Observaciones:", None)
        )
        self.label_2.setStyleSheet("")
        self.label_2.setText(
            QCoreApplication.translate("frmClientes", "Cif/Nif:", None)
        )
        self.lblSegundoApellido.setStyleSheet("")
        self.lblSegundoApellido.setText(
            QCoreApplication.translate("frmClientes", "Segundo Apellido:", None)
        )
        self.label_4.setStyleSheet("")
        self.label_4.setText(
            QCoreApplication.translate("frmClientes", "Primer Apellido:", None)
        )
        self.LblSIRET.setText(QCoreApplication.translate("frmClientes", "SIRET", None))
        self.tabwidget.setTabText(
            self.tabwidget.indexOf(self.tab_datos),
            QCoreApplication.translate("frmClientes", "Cliente", None),
        )
        self.label_7.setText(
            QCoreApplication.translate("frmClientes", "DIRECCIONES", None)
        )
        self.label_6.setText(
            QCoreApplication.translate("frmClientes", "Descripci\u00f3n:", None)
        )
        self.label_29.setText(QCoreApplication.translate("frmClientes", "C.P.:", None))
        self.label_66.setText(
            QCoreApplication.translate("frmClientes", "Poblaci\u00f3n", None)
        )
        self.label_27.setText(
            QCoreApplication.translate("frmClientes", "Direcci\u00f3n:", None)
        )
        self.label_28.setText(
            QCoreApplication.translate("frmClientes", "Direcci\u00f3n 2:", None)
        )
        self.lblProvinciaAlternativa.setText(
            QCoreApplication.translate("frmClientes", "Provincia:", None)
        )
        self.label_31.setText(QCoreApplication.translate("frmClientes", "Pais:", None))
        self.label_64.setText(QCoreApplication.translate("frmClientes", "email:", None))
        self.label_86.setText(
            QCoreApplication.translate("frmClientes", "Comentarios:", None)
        )
        # if QT_CONFIG(tooltip)
        self.btnAnadirdireccion.setToolTip(
            QCoreApplication.translate(
                "frmClientes", "A\u00f1adir nueva direcci\u00f3n alternativa", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.btnAnadirdireccion.setText(
            QCoreApplication.translate("frmClientes", "A\u00f1adir", None)
        )
        self.btnEditardireccionAlternativa.setText(
            QCoreApplication.translate("frmClientes", "Editar", None)
        )
        # if QT_CONFIG(tooltip)
        self.btnBorrardireccion.setToolTip(
            QCoreApplication.translate(
                "frmClientes", "Borrar una direcci\u00f3n alternativa", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.btnBorrardireccion.setText(
            QCoreApplication.translate("frmClientes", "Borrar", None)
        )
        self.btnGuardardireccionAlternativa.setText(
            QCoreApplication.translate("frmClientes", "Guardar", None)
        )
        self.btnDeshacerdireccionAlternativa.setText(
            QCoreApplication.translate("frmClientes", "Deshacer", None)
        )
        self.tabwidget.setTabText(
            self.tabwidget.indexOf(self.tab_direcciones),
            QCoreApplication.translate("frmClientes", "Direcciones alternativas", None),
        )
        self.label_33.setText(
            QCoreApplication.translate("frmClientes", "Tarifa Cliente:", None)
        )
        self.label_65.setText(
            QCoreApplication.translate("frmClientes", "Divisa:", None)
        )
        self.label_67.setText(
            QCoreApplication.translate("frmClientes", "Forma de Pago:", None)
        )
        self.label_68.setText(
            QCoreApplication.translate("frmClientes", "D\u00eda de pago 1:", None)
        )
        self.label_69.setText(
            QCoreApplication.translate("frmClientes", "D\u00eda de pago 2:", None)
        )
        self.label_32.setText(
            QCoreApplication.translate("frmClientes", "Porcentaje DTO Fijo:", None)
        )
        self.txtporc_dto_cliente.setText(
            QCoreApplication.translate("frmClientes", "0", None)
        )
        self.pushButton.setText(
            QCoreApplication.translate("frmClientes", "Ver Asientos Cliente", None)
        )
        self.label_72.setText(
            QCoreApplication.translate("frmClientes", "Cuenta IVA Repercutido:", None)
        )
        self.label_74.setText(
            QCoreApplication.translate("frmClientes", "Cuenta Cobros:", None)
        )
        self.label_70.setText(
            QCoreApplication.translate(
                "frmClientes",
                '<html><head/><body><p><span style=" font-size:11pt; text-decoration: underline; color:#ff0000;">Contabilidad (P.G.C):</span></p></body></html>',
                None,
            )
        )
        self.label_73.setText(
            QCoreApplication.translate("frmClientes", "Cuenta deudas:", None)
        )
        self.label_71.setText(
            QCoreApplication.translate("frmClientes", "Cuenta contable:", None)
        )
        self.label_75.setText(
            QCoreApplication.translate(
                "frmClientes",
                '<html><head/><body><p><span style=" font-size:11pt; text-decoration: underline; color:#ff0000;">Datos financieros:</span></p></body></html>',
                None,
            )
        )
        self.chkClienteEmpresa.setText(
            QCoreApplication.translate(
                "frmClientes", "Cliente Empresa (Aplicar IRPF)", None
            )
        )
        self.chkrecargo_equivalencia.setText(
            QCoreApplication.translate("frmClientes", "Recargo Equivalencia", None)
        )
        self.label_76.setText(
            QCoreApplication.translate("frmClientes", "Entregado a cuenta:", None)
        )
        self.label_77.setText(
            QCoreApplication.translate("frmClientes", "Importe Vales:", None)
        )
        self.lblCuentavalida.setText(
            QCoreApplication.translate("frmClientes", "Cuenta Valida", None)
        )
        self.label_78.setText(QCoreApplication.translate("frmClientes", "IBAN", None))
        self.txtimporte_a_cuenta.setText(
            QCoreApplication.translate("frmClientes", "0,00", None)
        )
        self.txtvales.setText(QCoreApplication.translate("frmClientes", "0,00", None))
        self.groupBox.setTitle(
            QCoreApplication.translate("frmClientes", "Iva Cliente", None)
        )
        self.radUE.setText(QCoreApplication.translate("frmClientes", "U.E.", None))
        self.radGeneral.setText(
            QCoreApplication.translate("frmClientes", "General", None)
        )
        self.radExcento.setText(
            QCoreApplication.translate("frmClientes", "Exento", None)
        )
        self.radExportacion.setText(
            QCoreApplication.translate("frmClientes", "Exportaci\u00f3n", None)
        )
        self.label_45.setText(
            QCoreApplication.translate("frmClientes", "tarjeta", None)
        )
        self.label_59.setText(
            QCoreApplication.translate("frmClientes", "mes/cad", None)
        )
        self.label_60.setText(
            QCoreApplication.translate("frmClientes", "a\u00f1o/cad", None)
        )
        self.label_61.setText(QCoreApplication.translate("frmClientes", "codigo", None))
        self.label_26.setText(
            QCoreApplication.translate("frmClientes", "Visa1 distancia:", None)
        )
        self.label_41.setText(
            QCoreApplication.translate("frmClientes", "Visa2_distancia:", None)
        )
        self.tabwidget.setTabText(
            self.tabwidget.indexOf(self.tab_Datos_bancarios_financieros),
            QCoreApplication.translate(
                "frmClientes", "Datos Bancarios y Financieros", None
            ),
        )
        self.txtdeuda_actual.setText(
            QCoreApplication.translate("frmClientes", "0,00", None)
        )
        self.txtventas_ejercicio.setText(
            QCoreApplication.translate("frmClientes", "0,00", None)
        )
        self.txtfecha_ultima_compra.setDisplayFormat(
            QCoreApplication.translate("frmClientes", "dd/MM/yyyy", None)
        )
        self.txtimporteAcumulado.setText(
            QCoreApplication.translate("frmClientes", "0,00", None)
        )
        self.label_37.setText(
            QCoreApplication.translate("frmClientes", "Fecha ultima compra:", None)
        )
        self.label_38.setText(
            QCoreApplication.translate("frmClientes", "Deuda Actual:", None)
        )
        self.label_39.setText(
            QCoreApplication.translate("frmClientes", "Ventas Ejercicio:", None)
        )
        self.label_36.setText(
            QCoreApplication.translate("frmClientes", "Importe Acumulado:", None)
        )
        self.txtSeptiembre.setText(
            QCoreApplication.translate("frmClientes", "0,00", None)
        )
        self.label_56.setText(
            QCoreApplication.translate("frmClientes", "Diciembre:", None)
        )
        self.label_57.setText(
            QCoreApplication.translate("frmClientes", "Octubre:", None)
        )
        self.label_55.setText(
            QCoreApplication.translate("frmClientes", "Agosto:", None)
        )
        self.label_54.setText(QCoreApplication.translate("frmClientes", "Julio:", None))
        self.txtAgosto.setText(QCoreApplication.translate("frmClientes", "0,00", None))
        self.label_53.setText(
            QCoreApplication.translate("frmClientes", "Noviembre:", None)
        )
        self.txtMarzo.setText(QCoreApplication.translate("frmClientes", "0,00", None))
        self.txtEnero.setText(QCoreApplication.translate("frmClientes", "0,00", None))
        self.label_51.setText(QCoreApplication.translate("frmClientes", "Mayo:", None))
        self.txtFebrero.setText(QCoreApplication.translate("frmClientes", "0,00", None))
        self.label_48.setText(
            QCoreApplication.translate("frmClientes", "Febrero:", None)
        )
        self.label_58.setText(
            QCoreApplication.translate("frmClientes", "Septiembre:", None)
        )
        self.txtJunio.setText(QCoreApplication.translate("frmClientes", "0,00", None))
        self.label_50.setText(QCoreApplication.translate("frmClientes", "Abril:", None))
        self.txtNoviembre.setText(
            QCoreApplication.translate("frmClientes", "0,00", None)
        )
        self.txtOctubre.setText(QCoreApplication.translate("frmClientes", "0,00", None))
        self.txtjulio.setText(QCoreApplication.translate("frmClientes", "0,00", None))
        self.label_52.setText(QCoreApplication.translate("frmClientes", "Junio:", None))
        self.label_49.setText(QCoreApplication.translate("frmClientes", "Marzo", None))
        self.txtAbril.setText(QCoreApplication.translate("frmClientes", "0,00", None))
        self.label_47.setText(QCoreApplication.translate("frmClientes", "Enero:", None))
        self.txtMayo.setText(QCoreApplication.translate("frmClientes", "0,00", None))
        self.txtDiciembre.setText(
            QCoreApplication.translate("frmClientes", "0,00", None)
        )
        self.tabwidget.setTabText(
            self.tabwidget.indexOf(self.tab_estadistica),
            QCoreApplication.translate("frmClientes", "Estadistica", None),
        )
        self.btnCobroTotal.setText(
            QCoreApplication.translate("frmClientes", "Cobro ", None)
        )
        self.label_83.setText(QCoreApplication.translate("frmClientes", "Deudas", None))
        self.radPendientes.setText(
            QCoreApplication.translate("frmClientes", "Pendientes", None)
        )
        self.radPagadas.setText(
            QCoreApplication.translate("frmClientes", "Pagadas", None)
        )
        self.label_84.setText(
            QCoreApplication.translate("frmClientes", "Historial de deuda", None)
        )
        self.tabwidget.setTabText(
            self.tabwidget.indexOf(self.tab_deudas),
            QCoreApplication.translate(
                "frmClientes", "Gesti\u00f3n deuda cliente", None
            ),
        )
        self.label_35.setText(
            QCoreApplication.translate("frmClientes", "Riesgo permitido:", None)
        )
        self.txtfecha_alta.setDisplayFormat(
            QCoreApplication.translate("frmClientes", "dd/MM/yyyy", None)
        )
        self.txtrRiesgoPermitido.setText(
            QCoreApplication.translate("frmClientes", "0,00", None)
        )
        self.label_34.setText(
            QCoreApplication.translate("frmClientes", "Fecha de Alta:", None)
        )
        self.label_62.setText(
            QCoreApplication.translate("frmClientes", "Transportista:", None)
        )
        self.label_63.setText(
            QCoreApplication.translate("frmClientes", "Agente: ", None)
        )
        self.chklBloqueoCliente.setText(
            QCoreApplication.translate("frmClientes", "Activar Bloqueo cliente", None)
        )
        self.label_43.setText(
            QCoreApplication.translate("frmClientes", "Usuario Acceso Web:", None)
        )
        self.label_44.setText(
            QCoreApplication.translate("frmClientes", "Password Acceso web:", None)
        )
        self.label_82.setText(
            QCoreApplication.translate(
                "frmClientes", "Comentarios generales sobre el cliente:", None
            )
        )
        self.label_9.setText(
            QCoreApplication.translate("frmClientes", "idioma Documentos:", None)
        )
        self.tabwidget.setTabText(
            self.tabwidget.indexOf(self.tab_coments),
            QCoreApplication.translate("frmClientes", "Comentarios y Otros", None),
        )
        self.tabWidget_2.setTabText(
            self.tabWidget_2.indexOf(self.tab_13),
            QCoreApplication.translate("frmClientes", "Presupuestos", None),
        )
        self.tabWidget_2.setTabText(
            self.tabWidget_2.indexOf(self.tab_9),
            QCoreApplication.translate("frmClientes", "Pedidos", None),
        )
        self.tabWidget_2.setTabText(
            self.tabWidget_2.indexOf(self.tab_7),
            QCoreApplication.translate("frmClientes", "Albaranes", None),
        )
        self.tabWidget_2.setTabText(
            self.tabWidget_2.indexOf(self.tab_Facturas),
            QCoreApplication.translate("frmClientes", "Facturas", None),
        )
        self.tabWidget_2.setTabText(
            self.tabWidget_2.indexOf(self.tab_12),
            QCoreApplication.translate("frmClientes", "Vales", None),
        )
        self.label_10.setText(
            QCoreApplication.translate("frmClientes", "Asientos Contables", None)
        )
        self.tabwidget.setTabText(
            self.tabwidget.indexOf(self.tab_3),
            QCoreApplication.translate("frmClientes", "Historial", None),
        )

    # retranslateUi
