# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frmarticulos.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject, QSize, Qt
from PySide6.QtGui import QBrush, QColor, QFont, QIcon, QPixmap
from PySide6.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDoubleSpinBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListView,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QRadioButton,
    QSizePolicy,
    QSpacerItem,
    QStackedWidget,
    QTableView,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from modules.common.chartviewwidget import ChartViewWidget


class Ui_FrmArticulos(object):
    def setupUi(self, FrmArticulos):
        if not FrmArticulos.objectName():
            FrmArticulos.setObjectName("FrmArticulos")
        FrmArticulos.resize(1173, 630)
        FrmArticulos.setMaximumSize(QSize(16777215, 16777215))
        icon = QIcon()
        icon.addFile(
            ":/Icons/PNG/Maya.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        FrmArticulos.setWindowIcon(icon)
        self.gridLayout_10 = QGridLayout(FrmArticulos)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.stackedWidget = QStackedWidget(FrmArticulos)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QWidget()
        self.page.setObjectName("page")
        self.gridLayout_2 = QGridLayout(self.page)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout_2.setContentsMargins(-1, -1, 20, -1)
        self.lblkit = QLabel(self.page)
        self.lblkit.setObjectName("lblkit")
        self.lblkit.setMinimumSize(QSize(120, 0))
        self.lblkit.setMaximumSize(QSize(150, 16777215))
        self.lblkit.setStyleSheet(
            "background-color: rgb(0, 0, 127);\n" "color: rgb(255, 255, 255);"
        )
        self.lblkit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lblkit, 0, 5, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.gridLayout_2.addItem(self.horizontalSpacer_9, 0, 3, 1, 1)

        self.lbl_en_promocion = QLabel(self.page)
        self.lbl_en_promocion.setObjectName("lbl_en_promocion")
        self.lbl_en_promocion.setMinimumSize(QSize(120, 0))
        self.lbl_en_promocion.setMaximumSize(QSize(150, 19))
        self.lbl_en_promocion.setStyleSheet(
            "background-color: rgb(255, 85, 0);\n" "color: rgb(255, 255, 255);"
        )
        self.lbl_en_promocion.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lbl_en_promocion, 0, 4, 1, 1)

        self.lblCodigo = QLabel(self.page)
        self.lblCodigo.setObjectName("lblCodigo")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblCodigo.sizePolicy().hasHeightForWidth())
        self.lblCodigo.setSizePolicy(sizePolicy)
        self.lblCodigo.setMaximumSize(QSize(130, 16777215))

        self.gridLayout_2.addWidget(self.lblCodigo, 0, 1, 1, 1)

        self.lblDescripcion = QLabel(self.page)
        self.lblDescripcion.setObjectName("lblDescripcion")
        sizePolicy.setHeightForWidth(
            self.lblDescripcion.sizePolicy().hasHeightForWidth()
        )
        self.lblDescripcion.setSizePolicy(sizePolicy)
        self.lblDescripcion.setMinimumSize(QSize(0, 0))
        self.lblDescripcion.setMaximumSize(QSize(425, 16777215))

        self.gridLayout_2.addWidget(self.lblDescripcion, 0, 2, 1, 1)

        self.frame_16 = QFrame(self.page)
        self.frame_16.setObjectName("frame_16")
        self.frame_16.setMinimumSize(QSize(132, 0))
        self.frame_16.setMaximumSize(QSize(140, 16777215))
        self.frame_16.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_16.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_16)
        self.verticalLayout.setObjectName("verticalLayout")
        self.botAnadir = QPushButton(self.frame_16)
        self.botAnadir.setObjectName("botAnadir")
        self.botAnadir.setMinimumSize(QSize(115, 40))
        self.botAnadir.setMaximumSize(QSize(118, 16777215))
        icon1 = QIcon()
        icon1.addFile(
            ":/PNG/resources/icons/png/Add.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.botAnadir.setIcon(icon1)
        self.botAnadir.setIconSize(QSize(24, 24))

        self.verticalLayout.addWidget(self.botAnadir)

        self.botSiguiente = QPushButton(self.frame_16)
        self.botSiguiente.setObjectName("botSiguiente")
        self.botSiguiente.setMinimumSize(QSize(115, 40))
        self.botSiguiente.setMaximumSize(QSize(118, 16777215))
        icon2 = QIcon()
        icon2.addFile(
            ":/PNG/resources/icons/png/Next.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.botSiguiente.setIcon(icon2)
        self.botSiguiente.setIconSize(QSize(24, 24))

        self.verticalLayout.addWidget(self.botSiguiente)

        self.botAnterior = QPushButton(self.frame_16)
        self.botAnterior.setObjectName("botAnterior")
        self.botAnterior.setMinimumSize(QSize(115, 40))
        self.botAnterior.setMaximumSize(QSize(118, 16777215))
        icon3 = QIcon()
        icon3.addFile(
            ":/PNG/resources/icons/png/Previous.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.botAnterior.setIcon(icon3)
        self.botAnterior.setIconSize(QSize(24, 24))

        self.verticalLayout.addWidget(self.botAnterior)

        self.btnBuscar = QPushButton(self.frame_16)
        self.btnBuscar.setObjectName("btnBuscar")
        self.btnBuscar.setMinimumSize(QSize(0, 40))
        icon4 = QIcon()
        icon4.addFile(
            ":/PNG/resources/icons/png/search.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.btnBuscar.setIcon(icon4)
        self.btnBuscar.setIconSize(QSize(24, 24))

        self.verticalLayout.addWidget(self.btnBuscar)

        self.botEditar = QPushButton(self.frame_16)
        self.botEditar.setObjectName("botEditar")
        self.botEditar.setMinimumSize(QSize(115, 40))
        self.botEditar.setMaximumSize(QSize(118, 16777215))
        icon5 = QIcon()
        icon5.addFile(
            ":/PNG/resources/icons/png/Edit.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.botEditar.setIcon(icon5)
        self.botEditar.setIconSize(QSize(24, 24))

        self.verticalLayout.addWidget(self.botEditar)

        self.botGuardar = QPushButton(self.frame_16)
        self.botGuardar.setObjectName("botGuardar")
        self.botGuardar.setEnabled(False)
        self.botGuardar.setMinimumSize(QSize(115, 40))
        self.botGuardar.setMaximumSize(QSize(118, 16777215))
        icon6 = QIcon()
        icon6.addFile(
            ":/PNG/resources/icons/png/Save.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.botGuardar.setIcon(icon6)
        self.botGuardar.setIconSize(QSize(24, 24))

        self.verticalLayout.addWidget(self.botGuardar)

        self.botDeshacer = QPushButton(self.frame_16)
        self.botDeshacer.setObjectName("botDeshacer")
        self.botDeshacer.setEnabled(False)
        self.botDeshacer.setMinimumSize(QSize(115, 40))
        self.botDeshacer.setMaximumSize(QSize(118, 16777215))
        icon7 = QIcon()
        icon7.addFile(
            ":/PNG/resources/icons/png/undo.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.botDeshacer.setIcon(icon7)
        self.botDeshacer.setIconSize(QSize(24, 24))

        self.verticalLayout.addWidget(self.botDeshacer)

        self.btnKit = QPushButton(self.frame_16)
        self.btnKit.setObjectName("btnKit")
        self.btnKit.setMinimumSize(QSize(0, 40))
        icon8 = QIcon()
        icon8.addFile(
            ":/Icons/PNG/kits.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.btnKit.setIcon(icon8)
        self.btnKit.setIconSize(QSize(24, 24))

        self.verticalLayout.addWidget(self.btnKit)

        self.verticalSpacer_5 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.verticalLayout.addItem(self.verticalSpacer_5)

        self.botBorrar = QPushButton(self.frame_16)
        self.botBorrar.setObjectName("botBorrar")
        self.botBorrar.setMinimumSize(QSize(115, 40))
        self.botBorrar.setMaximumSize(QSize(118, 16777215))
        icon9 = QIcon()
        icon9.addFile(
            ":/PNG/resources/icons/png/delete.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.botBorrar.setIcon(icon9)
        self.botBorrar.setIconSize(QSize(24, 24))

        self.verticalLayout.addWidget(self.botBorrar)

        self.btn_cerrar = QPushButton(self.frame_16)
        self.btn_cerrar.setObjectName("btn_cerrar")
        self.btn_cerrar.setMinimumSize(QSize(115, 40))
        icon10 = QIcon()
        icon10.addFile(
            ":/PNG/resources/icons/png/Exit.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.btn_cerrar.setIcon(icon10)
        self.btn_cerrar.setIconSize(QSize(24, 24))

        self.verticalLayout.addWidget(self.btn_cerrar)

        self.gridLayout_2.addWidget(self.frame_16, 0, 0, 2, 1)

        self.Pestanas = QTabWidget(self.page)
        self.Pestanas.setObjectName("Pestanas")
        sizePolicy1 = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.Pestanas.sizePolicy().hasHeightForWidth())
        self.Pestanas.setSizePolicy(sizePolicy1)
        self.Pestanas.setMinimumSize(QSize(0, 46))
        font = QFont()
        font.setKerning(False)
        self.Pestanas.setFont(font)
        self.tab_articulo = QWidget()
        self.tab_articulo.setObjectName("tab_articulo")
        self.tab_articulo.setStyleSheet("")
        self.gridLayout_8 = QGridLayout(self.tab_articulo)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.cboTipoIVA = QComboBox(self.tab_articulo)
        self.cboTipoIVA.setObjectName("cboTipoIVA")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.cboTipoIVA.sizePolicy().hasHeightForWidth())
        self.cboTipoIVA.setSizePolicy(sizePolicy2)
        self.cboTipoIVA.setMinimumSize(QSize(0, 27))

        self.gridLayout_8.addWidget(self.cboTipoIVA, 8, 1, 1, 1)

        self.txtCodigoProveedor = QLineEdit(self.tab_articulo)
        self.txtCodigoProveedor.setObjectName("txtCodigoProveedor")
        sizePolicy2.setHeightForWidth(
            self.txtCodigoProveedor.sizePolicy().hasHeightForWidth()
        )
        self.txtCodigoProveedor.setSizePolicy(sizePolicy2)
        self.txtCodigoProveedor.setMinimumSize(QSize(100, 0))
        self.txtCodigoProveedor.setMaximumSize(QSize(150, 16777215))
        self.txtCodigoProveedor.setProperty("locateField", True)

        self.gridLayout_8.addWidget(self.txtCodigoProveedor, 7, 1, 1, 1)

        self.label_16 = QLabel(self.tab_articulo)
        self.label_16.setObjectName("label_16")

        self.gridLayout_8.addWidget(self.label_16, 4, 0, 1, 1)

        self.txtcodigo = QLineEdit(self.tab_articulo)
        self.txtcodigo.setObjectName("txtcodigo")
        sizePolicy.setHeightForWidth(self.txtcodigo.sizePolicy().hasHeightForWidth())
        self.txtcodigo.setSizePolicy(sizePolicy)
        self.txtcodigo.setProperty("codeField", True)

        self.gridLayout_8.addWidget(self.txtcodigo, 5, 1, 1, 1)

        self.lblProveedorHabitual = QLabel(self.tab_articulo)
        self.lblProveedorHabitual.setObjectName("lblProveedorHabitual")

        self.gridLayout_8.addWidget(self.lblProveedorHabitual, 7, 0, 1, 1)

        self.frame_8 = QFrame(self.tab_articulo)
        self.frame_8.setObjectName("frame_8")
        sizePolicy3 = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.frame_8.sizePolicy().hasHeightForWidth())
        self.frame_8.setSizePolicy(sizePolicy3)
        self.frame_8.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_8)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.TablaTarifas = QTableView(self.frame_8)
        self.TablaTarifas.setObjectName("TablaTarifas")
        sizePolicy1.setHeightForWidth(
            self.TablaTarifas.sizePolicy().hasHeightForWidth()
        )
        self.TablaTarifas.setSizePolicy(sizePolicy1)
        self.TablaTarifas.setAlternatingRowColors(True)
        self.TablaTarifas.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.TablaTarifas.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.gridLayout_4.addWidget(self.TablaTarifas, 0, 0, 1, 3)

        self.btnEditartarifa = QPushButton(self.frame_8)
        self.btnEditartarifa.setObjectName("btnEditartarifa")
        self.btnEditartarifa.setEnabled(False)
        sizePolicy.setHeightForWidth(
            self.btnEditartarifa.sizePolicy().hasHeightForWidth()
        )
        self.btnEditartarifa.setSizePolicy(sizePolicy)
        self.btnEditartarifa.setIcon(icon5)

        self.gridLayout_4.addWidget(self.btnEditartarifa, 1, 2, 1, 1)

        self.gridLayout_8.addWidget(self.frame_8, 13, 0, 3, 8)

        self.txtProveedor = QLineEdit(self.tab_articulo)
        self.txtProveedor.setObjectName("txtProveedor")
        self.txtProveedor.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout_8.addWidget(self.txtProveedor, 7, 2, 1, 5)

        self.label_15 = QLabel(self.tab_articulo)
        self.label_15.setObjectName("label_15")

        self.gridLayout_8.addWidget(self.label_15, 9, 6, 1, 1)

        self.frame_7 = QFrame(self.tab_articulo)
        self.frame_7.setObjectName("frame_7")
        sizePolicy4 = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.frame_7.sizePolicy().hasHeightForWidth())
        self.frame_7.setSizePolicy(sizePolicy4)
        self.frame_7.setMinimumSize(QSize(180, 0))
        self.frame_7.setMaximumSize(QSize(16777215, 40))
        self.frame_7.setAutoFillBackground(False)
        self.frame_7.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_7)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_14 = QLabel(self.frame_7)
        self.label_14.setObjectName("label_14")
        self.label_14.setAutoFillBackground(False)

        self.horizontalLayout_5.addWidget(self.label_14)

        self.txtcoste = QLineEdit(self.frame_7)
        self.txtcoste.setObjectName("txtcoste")
        sizePolicy2.setHeightForWidth(self.txtcoste.sizePolicy().hasHeightForWidth())
        self.txtcoste.setSizePolicy(sizePolicy2)
        self.txtcoste.setMinimumSize(QSize(0, 27))
        self.txtcoste.setMaximumSize(QSize(120, 16777215))
        self.txtcoste.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.horizontalLayout_5.addWidget(self.txtcoste)

        self.gridLayout_8.addWidget(self.frame_7, 8, 2, 1, 2)

        self.lblCodigoEAN = QLabel(self.tab_articulo)
        self.lblCodigoEAN.setObjectName("lblCodigoEAN")

        self.gridLayout_8.addWidget(self.lblCodigoEAN, 5, 2, 1, 1)

        self.txtcodigo_fabricante = QLineEdit(self.tab_articulo)
        self.txtcodigo_fabricante.setObjectName("txtcodigo_fabricante")
        self.txtcodigo_fabricante.setMaximumSize(QSize(120, 16777215))
        self.txtcodigo_fabricante.setAlignment(
            Qt.AlignmentFlag.AlignLeading
            | Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_8.addWidget(self.txtcodigo_fabricante, 5, 7, 1, 1)

        self.txtDescripcionTipo = QLineEdit(self.tab_articulo)
        self.txtDescripcionTipo.setObjectName("txtDescripcionTipo")
        self.txtDescripcionTipo.setReadOnly(True)

        self.gridLayout_8.addWidget(self.txtDescripcionTipo, 4, 2, 1, 6)

        self.FrameRF = QFrame(self.tab_articulo)
        self.FrameRF.setObjectName("FrameRF")
        self.FrameRF.setFrameShape(QFrame.Shape.StyledPanel)
        self.FrameRF.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_7 = QGridLayout(self.FrameRF)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.txtcomentario = QTextEdit(self.FrameRF)
        self.txtcomentario.setObjectName("txtcomentario")
        sizePolicy1.setHeightForWidth(
            self.txtcomentario.sizePolicy().hasHeightForWidth()
        )
        self.txtcomentario.setSizePolicy(sizePolicy1)

        self.gridLayout_7.addWidget(self.txtcomentario, 2, 1, 1, 1)

        self.label_18 = QLabel(self.FrameRF)
        self.label_18.setObjectName("label_18")

        self.gridLayout_7.addWidget(self.label_18, 1, 1, 1, 1)

        self.gridLayout_8.addWidget(self.FrameRF, 14, 8, 2, 1)

        self.txtcodigo_barras = QLineEdit(self.tab_articulo)
        self.txtcodigo_barras.setObjectName("txtcodigo_barras")
        sizePolicy.setHeightForWidth(
            self.txtcodigo_barras.sizePolicy().hasHeightForWidth()
        )
        self.txtcodigo_barras.setSizePolicy(sizePolicy)
        self.txtcodigo_barras.setMinimumSize(QSize(148, 0))
        self.txtcodigo_barras.setMaximumSize(QSize(120, 16777215))
        self.txtcodigo_barras.setProperty("testField", True)

        self.gridLayout_8.addWidget(self.txtcodigo_barras, 5, 3, 1, 1)

        self.txtCodigoTipo = QLineEdit(self.tab_articulo)
        self.txtCodigoTipo.setObjectName("txtCodigoTipo")
        self.txtCodigoTipo.setEnabled(True)

        self.gridLayout_8.addWidget(self.txtCodigoTipo, 4, 1, 1, 1)

        self.label_2 = QLabel(self.tab_articulo)
        self.label_2.setObjectName("label_2")
        sizePolicy5 = QSizePolicy(
            QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred
        )
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy5)

        self.gridLayout_8.addWidget(self.label_2, 5, 0, 1, 1)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")

        self.gridLayout_8.addLayout(self.horizontalLayout_12, 9, 0, 1, 1)

        self.frame_10 = QFrame(self.tab_articulo)
        self.frame_10.setObjectName("frame_10")
        self.frame_10.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_13 = QGridLayout(self.frame_10)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.chkmostrar_web = QCheckBox(self.frame_10)
        self.chkmostrar_web.setObjectName("chkmostrar_web")

        self.gridLayout_13.addWidget(self.chkmostrar_web, 0, 0, 1, 1)

        self.gridLayout_8.addWidget(self.frame_10, 8, 4, 1, 1)

        self.txtdescripcionResumida = QLineEdit(self.tab_articulo)
        self.txtdescripcionResumida.setObjectName("txtdescripcionResumida")
        self.txtdescripcionResumida.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout_8.addWidget(self.txtdescripcionResumida, 6, 1, 1, 7)

        self.frame_4 = QFrame(self.tab_articulo)
        self.frame_4.setObjectName("frame_4")
        sizePolicy.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy)
        self.frame_4.setMaximumSize(QSize(16777215, 40))
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_19 = QLabel(self.frame_4)
        self.label_19.setObjectName("label_19")

        self.horizontalLayout_4.addWidget(self.label_19)

        self.gridLayout_8.addWidget(self.frame_4, 8, 0, 1, 1)

        self.frame_5 = QFrame(self.tab_articulo)
        self.frame_5.setObjectName("frame_5")
        sizePolicy4.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy4)
        self.frame_5.setMinimumSize(QSize(0, 0))
        self.frame_5.setMaximumSize(QSize(16777215, 80))
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame_5)
        self.gridLayout.setObjectName("gridLayout")
        self.txtdto = QLineEdit(self.frame_5)
        self.txtdto.setObjectName("txtdto")
        self.txtdto.setMinimumSize(QSize(62, 0))
        self.txtdto.setMaximumSize(QSize(80, 16777215))
        self.txtdto.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout.addWidget(self.txtdto, 1, 7, 1, 1)

        self.label_5 = QLabel(self.frame_5)
        self.label_5.setObjectName("label_5")

        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)

        self.txtCoste_real = QLineEdit(self.frame_5)
        self.txtCoste_real.setObjectName("txtCoste_real")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(
            self.txtCoste_real.sizePolicy().hasHeightForWidth()
        )
        self.txtCoste_real.setSizePolicy(sizePolicy6)
        self.txtCoste_real.setMinimumSize(QSize(87, 0))
        self.txtCoste_real.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.txtCoste_real.setReadOnly(True)

        self.gridLayout.addWidget(self.txtCoste_real, 1, 1, 1, 1)

        self.txtMargen = QDoubleSpinBox(self.frame_5)
        self.txtMargen.setObjectName("txtMargen")
        sizePolicy6.setHeightForWidth(self.txtMargen.sizePolicy().hasHeightForWidth())
        self.txtMargen.setSizePolicy(sizePolicy6)
        self.txtMargen.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.txtMargen.setDecimals(2)
        self.txtMargen.setMinimum(-1000.000000000000000)
        self.txtMargen.setMaximum(9999.989999999999782)
        self.txtMargen.setValue(0.000000000000000)

        self.gridLayout.addWidget(self.txtMargen, 1, 3, 1, 1)

        self.txtMargen_min = QDoubleSpinBox(self.frame_5)
        self.txtMargen_min.setObjectName("txtMargen_min")
        sizePolicy6.setHeightForWidth(
            self.txtMargen_min.sizePolicy().hasHeightForWidth()
        )
        self.txtMargen_min.setSizePolicy(sizePolicy6)
        self.txtMargen_min.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.txtMargen_min.setMinimum(-1000.000000000000000)
        self.txtMargen_min.setMaximum(9999.000000000000000)
        self.txtMargen_min.setValue(0.000000000000000)

        self.gridLayout.addWidget(self.txtMargen_min, 1, 5, 1, 1)

        self.label_13 = QLabel(self.frame_5)
        self.label_13.setObjectName("label_13")

        self.gridLayout.addWidget(self.label_13, 1, 4, 1, 1)

        self.label_12 = QLabel(self.frame_5)
        self.label_12.setObjectName("label_12")

        self.gridLayout.addWidget(self.label_12, 1, 2, 1, 1)

        self.label_20 = QLabel(self.frame_5)
        self.label_20.setObjectName("label_20")

        self.gridLayout.addWidget(self.label_20, 1, 6, 1, 1)

        self.gridLayout_8.addWidget(self.frame_5, 12, 0, 1, 8)

        self.txtPrecioVenta = QLineEdit(self.tab_articulo)
        self.txtPrecioVenta.setObjectName("txtPrecioVenta")
        sizePolicy6.setHeightForWidth(
            self.txtPrecioVenta.sizePolicy().hasHeightForWidth()
        )
        self.txtPrecioVenta.setSizePolicy(sizePolicy6)
        self.txtPrecioVenta.setMaximumSize(QSize(120, 16777215))
        font1 = QFont()
        font1.setPointSize(14)
        font1.setKerning(False)
        self.txtPrecioVenta.setFont(font1)
        self.txtPrecioVenta.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_8.addWidget(self.txtPrecioVenta, 9, 7, 1, 1)

        self.frame_20 = QFrame(self.tab_articulo)
        self.frame_20.setObjectName("frame_20")
        self.frame_20.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_20.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_42 = QGridLayout(self.frame_20)
        self.gridLayout_42.setObjectName("gridLayout_42")
        self.txtdescripcion = QTextEdit(self.frame_20)
        self.txtdescripcion.setObjectName("txtdescripcion")

        self.gridLayout_42.addWidget(self.txtdescripcion, 1, 0, 1, 1)

        self.label_7 = QLabel(self.frame_20)
        self.label_7.setObjectName("label_7")

        self.gridLayout_42.addWidget(self.label_7, 0, 0, 1, 1)

        self.gridLayout_8.addWidget(self.frame_20, 1, 8, 13, 1)

        self.label_6 = QLabel(self.tab_articulo)
        self.label_6.setObjectName("label_6")

        self.gridLayout_8.addWidget(self.label_6, 6, 0, 1, 1)

        self.frame_2 = QFrame(self.tab_articulo)
        self.frame_2.setObjectName("frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_2)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.chkcontrolar_stock = QCheckBox(self.frame_2)
        self.chkcontrolar_stock.setObjectName("chkcontrolar_stock")

        self.gridLayout_5.addWidget(self.chkcontrolar_stock, 0, 0, 1, 1)

        self.gridLayout_8.addWidget(self.frame_2, 8, 5, 1, 3)

        self.lblCodigoenProveedor = QLabel(self.tab_articulo)
        self.lblCodigoenProveedor.setObjectName("lblCodigoenProveedor")

        self.gridLayout_8.addWidget(self.lblCodigoenProveedor, 5, 6, 1, 1)

        self.Pestanas.addTab(self.tab_articulo, "")
        self.TallasColores = QWidget()
        self.TallasColores.setObjectName("TallasColores")
        self.verticalLayout_6 = QVBoxLayout(self.TallasColores)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.gridLayout_11 = QGridLayout()
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.frame_3 = QFrame(self.TallasColores)
        self.frame_3.setObjectName("frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_11.addWidget(self.frame_3, 0, 2, 1, 1)

        self.gridLayout_14 = QGridLayout()
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.listColors = QListWidget(self.TallasColores)
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        brush1 = QBrush(QColor(255, 255, 255, 255))
        brush1.setStyle(Qt.BrushStyle.SolidPattern)
        __qlistwidgetitem = QListWidgetItem(self.listColors)
        __qlistwidgetitem.setBackground(brush1)
        __qlistwidgetitem.setForeground(brush)
        __qlistwidgetitem1 = QListWidgetItem(self.listColors)
        __qlistwidgetitem1.setBackground(brush)
        __qlistwidgetitem1.setForeground(brush1)
        brush2 = QBrush(QColor(255, 255, 255, 255))
        brush2.setStyle(Qt.BrushStyle.NoBrush)
        brush3 = QBrush(QColor(170, 0, 0, 255))
        brush3.setStyle(Qt.BrushStyle.SolidPattern)
        __qlistwidgetitem2 = QListWidgetItem(self.listColors)
        __qlistwidgetitem2.setBackground(brush3)
        __qlistwidgetitem2.setForeground(brush2)
        brush4 = QBrush(QColor(255, 255, 255, 255))
        brush4.setStyle(Qt.BrushStyle.NoBrush)
        brush5 = QBrush(QColor(0, 0, 127, 255))
        brush5.setStyle(Qt.BrushStyle.SolidPattern)
        __qlistwidgetitem3 = QListWidgetItem(self.listColors)
        __qlistwidgetitem3.setBackground(brush5)
        __qlistwidgetitem3.setForeground(brush4)
        self.listColors.setObjectName("listColors")
        self.listColors.setStyleSheet(
            "QListWidget::item{border:1px solid transparent; margin:3px; padding:0px;}\\nQListWidget::item:selected{border:3px solid #1976d2; border-radius:6px; margin:-2px;}\\nQListWidget::item:hover{border:1px solid rgba(0,0,0,40);}"
        )
        self.listColors.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.listColors.setIconSize(QSize(44, 44))
        self.listColors.setResizeMode(QListView.ResizeMode.Adjust)
        self.listColors.setLayoutMode(QListView.LayoutMode.SinglePass)
        self.listColors.setSpacing(8)
        self.listColors.setGridSize(QSize(56, 56))
        self.listColors.setViewMode(QListView.ViewMode.IconMode)

        self.gridLayout_14.addWidget(self.listColors, 0, 2, 1, 1)

        self.gridLayout_11.addLayout(self.gridLayout_14, 0, 0, 1, 1)

        self.tableView = QTableView(self.TallasColores)
        self.tableView.setObjectName("tableView")

        self.gridLayout_11.addWidget(self.tableView, 0, 1, 1, 1)

        self.verticalLayout_6.addLayout(self.gridLayout_11)

        self.Pestanas.addTab(self.TallasColores, "")
        self.tab = QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_32 = QGridLayout(self.tab)
        self.gridLayout_32.setObjectName("gridLayout_32")
        self.FrameRF_2 = QFrame(self.tab)
        self.FrameRF_2.setObjectName("FrameRF_2")
        self.FrameRF_2.setMinimumSize(QSize(0, 0))
        self.FrameRF_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.FrameRF_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.FrameRF_2)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_9 = QLabel(self.FrameRF_2)
        self.label_9.setObjectName("label_9")

        self.verticalLayout_5.addWidget(self.label_9)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.txtseccion = QLineEdit(self.FrameRF_2)
        self.txtseccion.setObjectName("txtseccion")
        self.txtseccion.setEnabled(True)
        self.txtseccion.setAutoFillBackground(False)
        self.txtseccion.setReadOnly(True)
        self.txtseccion.setProperty("locateField", True)

        self.horizontalLayout_2.addWidget(self.txtseccion)

        self.botBuscarSeccion = QPushButton(self.FrameRF_2)
        self.botBuscarSeccion.setObjectName("botBuscarSeccion")
        self.botBuscarSeccion.setEnabled(False)
        sizePolicy.setHeightForWidth(
            self.botBuscarSeccion.sizePolicy().hasHeightForWidth()
        )
        self.botBuscarSeccion.setSizePolicy(sizePolicy)
        self.botBuscarSeccion.setMaximumSize(QSize(25, 16777215))
        self.botBuscarSeccion.setIcon(icon4)
        self.botBuscarSeccion.setIconSize(QSize(16, 16))

        self.horizontalLayout_2.addWidget(self.botBuscarSeccion)

        self.verticalLayout_5.addLayout(self.horizontalLayout_2)

        self.label_10 = QLabel(self.FrameRF_2)
        self.label_10.setObjectName("label_10")

        self.verticalLayout_5.addWidget(self.label_10)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.txtfamilia = QLineEdit(self.FrameRF_2)
        self.txtfamilia.setObjectName("txtfamilia")
        self.txtfamilia.setEnabled(True)
        self.txtfamilia.setAutoFillBackground(False)
        self.txtfamilia.setReadOnly(True)
        self.txtfamilia.setProperty("locateField", True)

        self.horizontalLayout_6.addWidget(self.txtfamilia)

        self.botBuscarFamilia = QPushButton(self.FrameRF_2)
        self.botBuscarFamilia.setObjectName("botBuscarFamilia")
        self.botBuscarFamilia.setEnabled(False)
        sizePolicy.setHeightForWidth(
            self.botBuscarFamilia.sizePolicy().hasHeightForWidth()
        )
        self.botBuscarFamilia.setSizePolicy(sizePolicy)
        self.botBuscarFamilia.setMaximumSize(QSize(25, 16777215))
        self.botBuscarFamilia.setIcon(icon4)
        self.botBuscarFamilia.setIconSize(QSize(16, 16))

        self.horizontalLayout_6.addWidget(self.botBuscarFamilia)

        self.verticalLayout_5.addLayout(self.horizontalLayout_6)

        self.label_11 = QLabel(self.FrameRF_2)
        self.label_11.setObjectName("label_11")

        self.verticalLayout_5.addWidget(self.label_11)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.txtsubfamilia = QLineEdit(self.FrameRF_2)
        self.txtsubfamilia.setObjectName("txtsubfamilia")
        self.txtsubfamilia.setEnabled(True)
        self.txtsubfamilia.setAutoFillBackground(False)
        self.txtsubfamilia.setReadOnly(True)
        self.txtsubfamilia.setProperty("locateField", True)

        self.horizontalLayout_7.addWidget(self.txtsubfamilia)

        self.botBuscarSubfamilia = QPushButton(self.FrameRF_2)
        self.botBuscarSubfamilia.setObjectName("botBuscarSubfamilia")
        self.botBuscarSubfamilia.setEnabled(False)
        sizePolicy.setHeightForWidth(
            self.botBuscarSubfamilia.sizePolicy().hasHeightForWidth()
        )
        self.botBuscarSubfamilia.setSizePolicy(sizePolicy)
        self.botBuscarSubfamilia.setMaximumSize(QSize(25, 16777215))
        self.botBuscarSubfamilia.setIcon(icon4)
        self.botBuscarSubfamilia.setIconSize(QSize(16, 16))

        self.horizontalLayout_7.addWidget(self.botBuscarSubfamilia)

        self.verticalLayout_5.addLayout(self.horizontalLayout_7)

        self.verticalSpacer_7 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.verticalLayout_5.addItem(self.verticalSpacer_7)

        self.gridLayout_32.addWidget(self.FrameRF_2, 0, 0, 1, 1)

        self.Pestanas.addTab(self.tab, "")
        self.tab_distribuidores = QWidget()
        self.tab_distribuidores.setObjectName("tab_distribuidores")
        self.verticalLayout_4 = QVBoxLayout(self.tab_distribuidores)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tablaProveedores = QTableView(self.tab_distribuidores)
        self.tablaProveedores.setObjectName("tablaProveedores")
        self.tablaProveedores.setMaximumSize(QSize(16777215, 1677215))
        self.tablaProveedores.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.tablaProveedores.setAlternatingRowColors(True)
        self.tablaProveedores.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.tablaProveedores.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.tablaProveedores.setGridStyle(Qt.PenStyle.DotLine)
        self.tablaProveedores.setSortingEnabled(False)
        self.tablaProveedores.horizontalHeader().setCascadingSectionResizes(False)
        self.tablaProveedores.horizontalHeader().setProperty("showSortIndicator", False)
        self.tablaProveedores.horizontalHeader().setStretchLastSection(True)
        self.tablaProveedores.verticalHeader().setVisible(False)

        self.verticalLayout_2.addWidget(self.tablaProveedores)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_23 = QLabel(self.tab_distribuidores)
        self.label_23.setObjectName("label_23")

        self.horizontalLayout_3.addWidget(self.label_23)

        self.btnAnadirDistribuidores = QPushButton(self.tab_distribuidores)
        self.btnAnadirDistribuidores.setObjectName("btnAnadirDistribuidores")
        self.btnAnadirDistribuidores.setEnabled(False)
        self.btnAnadirDistribuidores.setIcon(icon1)
        self.btnAnadirDistribuidores.setIconSize(QSize(15, 15))

        self.horizontalLayout_3.addWidget(self.btnAnadirDistribuidores)

        self.btnEditarDistribuidorFrecuente = QPushButton(self.tab_distribuidores)
        self.btnEditarDistribuidorFrecuente.setObjectName(
            "btnEditarDistribuidorFrecuente"
        )
        self.btnEditarDistribuidorFrecuente.setEnabled(False)
        self.btnEditarDistribuidorFrecuente.setIcon(icon5)
        self.btnEditarDistribuidorFrecuente.setIconSize(QSize(15, 15))

        self.horizontalLayout_3.addWidget(self.btnEditarDistribuidorFrecuente)

        self.btnBorrarDistribuidores = QPushButton(self.tab_distribuidores)
        self.btnBorrarDistribuidores.setObjectName("btnBorrarDistribuidores")
        self.btnBorrarDistribuidores.setEnabled(False)
        self.btnBorrarDistribuidores.setMaximumSize(QSize(25, 16777215))
        self.btnBorrarDistribuidores.setIcon(icon9)
        self.btnBorrarDistribuidores.setIconSize(QSize(15, 15))

        self.horizontalLayout_3.addWidget(self.btnBorrarDistribuidores)

        self.btnAsignarDistribuidor = QPushButton(self.tab_distribuidores)
        self.btnAsignarDistribuidor.setObjectName("btnAsignarDistribuidor")
        self.btnAsignarDistribuidor.setEnabled(False)
        self.btnAsignarDistribuidor.setIcon(icon6)
        self.btnAsignarDistribuidor.setIconSize(QSize(15, 15))

        self.horizontalLayout_3.addWidget(self.btnAsignarDistribuidor)

        self.horizontalSpacer_2 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.verticalLayout_4.addLayout(self.verticalLayout_2)

        self.Pestanas.addTab(self.tab_distribuidores, "")
        self.tab_promociones = QWidget()
        self.tab_promociones.setObjectName("tab_promociones")
        self.gridLayout_39 = QGridLayout(self.tab_promociones)
        self.gridLayout_39.setObjectName("gridLayout_39")
        self.chkArticulo_promocionado = QCheckBox(self.tab_promociones)
        self.chkArticulo_promocionado.setObjectName("chkArticulo_promocionado")

        self.gridLayout_39.addWidget(self.chkArticulo_promocionado, 0, 0, 1, 1)

        self.frame_pvp_fijo = QFrame(self.tab_promociones)
        self.frame_pvp_fijo.setObjectName("frame_pvp_fijo")
        self.frame_pvp_fijo.setEnabled(False)
        self.frame_pvp_fijo.setMaximumSize(QSize(16777215, 70))
        self.frame_pvp_fijo.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_pvp_fijo.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_26 = QGridLayout(self.frame_pvp_fijo)
        self.gridLayout_26.setObjectName("gridLayout_26")
        self.label_63 = QLabel(self.frame_pvp_fijo)
        self.label_63.setObjectName("label_63")
        self.label_63.setMinimumSize(QSize(0, 25))
        self.label_63.setMaximumSize(QSize(16777215, 27))
        self.label_63.setStyleSheet(
            "background-color: #304163;\n" "color: rgb(255, 255, 255);"
        )
        self.label_63.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_26.addWidget(self.label_63, 0, 0, 1, 3)

        self.horizontalSpacer_7 = QSpacerItem(
            224, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.gridLayout_26.addItem(self.horizontalSpacer_7, 1, 0, 1, 1)

        self.lbl_oferta_importe = QLabel(self.frame_pvp_fijo)
        self.lbl_oferta_importe.setObjectName("lbl_oferta_importe")

        self.gridLayout_26.addWidget(self.lbl_oferta_importe, 1, 1, 1, 1)

        self.txtofertaPvpFijo = QLineEdit(self.frame_pvp_fijo)
        self.txtofertaPvpFijo.setObjectName("txtofertaPvpFijo")
        self.txtofertaPvpFijo.setMinimumSize(QSize(0, 27))
        self.txtofertaPvpFijo.setMaximumSize(QSize(110, 27))
        self.txtofertaPvpFijo.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_26.addWidget(self.txtofertaPvpFijo, 1, 2, 1, 1)

        self.gridLayout_39.addWidget(self.frame_pvp_fijo, 6, 0, 1, 2)

        self.frame_tipo_32 = QFrame(self.tab_promociones)
        self.frame_tipo_32.setObjectName("frame_tipo_32")
        self.frame_tipo_32.setEnabled(False)
        self.frame_tipo_32.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_tipo_32.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_24 = QGridLayout(self.frame_tipo_32)
        self.gridLayout_24.setObjectName("gridLayout_24")
        self.lbl_por_cada = QLabel(self.frame_tipo_32)
        self.lbl_por_cada.setObjectName("lbl_por_cada")
        self.lbl_por_cada.setEnabled(False)
        self.lbl_por_cada.setMaximumSize(QSize(16777215, 27))

        self.gridLayout_24.addWidget(self.lbl_por_cada, 1, 0, 1, 1)

        self.txtOfertaPorCada = QLineEdit(self.frame_tipo_32)
        self.txtOfertaPorCada.setObjectName("txtOfertaPorCada")
        self.txtOfertaPorCada.setEnabled(False)
        self.txtOfertaPorCada.setMinimumSize(QSize(0, 27))
        self.txtOfertaPorCada.setMaximumSize(QSize(50, 27))
        self.txtOfertaPorCada.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_24.addWidget(self.txtOfertaPorCada, 1, 1, 1, 1)

        self.lbl_unidades = QLabel(self.frame_tipo_32)
        self.lbl_unidades.setObjectName("lbl_unidades")
        self.lbl_unidades.setEnabled(False)
        self.lbl_unidades.setMaximumSize(QSize(16777215, 27))

        self.gridLayout_24.addWidget(self.lbl_unidades, 1, 2, 1, 1)

        self.lbl_regalo_de = QLabel(self.frame_tipo_32)
        self.lbl_regalo_de.setObjectName("lbl_regalo_de")
        self.lbl_regalo_de.setEnabled(False)
        self.lbl_regalo_de.setMaximumSize(QSize(16777215, 27))

        self.gridLayout_24.addWidget(self.lbl_regalo_de, 1, 3, 1, 1)

        self.txtOfertaregaloUnidades = QLineEdit(self.frame_tipo_32)
        self.txtOfertaregaloUnidades.setObjectName("txtOfertaregaloUnidades")
        self.txtOfertaregaloUnidades.setEnabled(False)
        self.txtOfertaregaloUnidades.setMinimumSize(QSize(0, 27))
        self.txtOfertaregaloUnidades.setMaximumSize(QSize(50, 27))
        self.txtOfertaregaloUnidades.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_24.addWidget(self.txtOfertaregaloUnidades, 1, 4, 1, 1)

        self.lbl_unidades_2 = QLabel(self.frame_tipo_32)
        self.lbl_unidades_2.setObjectName("lbl_unidades_2")
        self.lbl_unidades_2.setEnabled(False)
        self.lbl_unidades_2.setMaximumSize(QSize(16777215, 27))

        self.gridLayout_24.addWidget(self.lbl_unidades_2, 1, 5, 1, 1)

        self.label_57 = QLabel(self.frame_tipo_32)
        self.label_57.setObjectName("label_57")
        self.label_57.setEnabled(False)
        self.label_57.setMinimumSize(QSize(0, 27))
        self.label_57.setMaximumSize(QSize(16777215, 27))
        self.label_57.setStyleSheet(
            "background-color: #304163;\n" "color: rgb(255, 255, 255);"
        )
        self.label_57.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_24.addWidget(self.label_57, 0, 0, 1, 6)

        self.gridLayout_39.addWidget(self.frame_tipo_32, 3, 0, 1, 2)

        self.txtOferta_Fecha_fin = QDateEdit(self.tab_promociones)
        self.txtOferta_Fecha_fin.setObjectName("txtOferta_Fecha_fin")
        self.txtOferta_Fecha_fin.setStyleSheet(
            "QDateEdit::up-button, QDateEdit::down-button {\n"
            "    width: 0px;\n"
            "    border: none;\n"
            "}"
        )
        self.txtOferta_Fecha_fin.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_39.addWidget(self.txtOferta_Fecha_fin, 0, 5, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.gridLayout_39.addItem(self.verticalSpacer_3, 7, 0, 1, 1)

        self.txtOferta_Fecha_ini = QDateEdit(self.tab_promociones)
        self.txtOferta_Fecha_ini.setObjectName("txtOferta_Fecha_ini")
        self.txtOferta_Fecha_ini.setStyleSheet(
            "QDateEdit::up-button, QDateEdit::down-button {\n"
            "    width: 0px;\n"
            "    border: none;\n"
            "}"
        )
        self.txtOferta_Fecha_ini.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_39.addWidget(self.txtOferta_Fecha_ini, 0, 3, 1, 1)

        self.frame_dto = QFrame(self.tab_promociones)
        self.frame_dto.setObjectName("frame_dto")
        self.frame_dto.setEnabled(False)
        self.frame_dto.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_dto.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_25 = QGridLayout(self.frame_dto)
        self.gridLayout_25.setObjectName("gridLayout_25")
        self.label_61 = QLabel(self.frame_dto)
        self.label_61.setObjectName("label_61")
        self.label_61.setMinimumSize(QSize(0, 27))
        self.label_61.setMaximumSize(QSize(16777215, 27))
        self.label_61.setStyleSheet(
            "background-color: #304163;\n" "color: rgb(255, 255, 255);"
        )
        self.label_61.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_25.addWidget(self.label_61, 0, 0, 1, 3)

        self.horizontalSpacer_5 = QSpacerItem(
            249, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.gridLayout_25.addItem(self.horizontalSpacer_5, 1, 0, 1, 1)

        self.lbl_oferta_dto = QLabel(self.frame_dto)
        self.lbl_oferta_dto.setObjectName("lbl_oferta_dto")

        self.gridLayout_25.addWidget(self.lbl_oferta_dto, 1, 1, 1, 1)

        self.txtOfertaDtoOferta = QLineEdit(self.frame_dto)
        self.txtOfertaDtoOferta.setObjectName("txtOfertaDtoOferta")
        self.txtOfertaDtoOferta.setMinimumSize(QSize(0, 27))
        self.txtOfertaDtoOferta.setMaximumSize(QSize(50, 27))
        self.txtOfertaDtoOferta.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_25.addWidget(self.txtOfertaDtoOferta, 1, 2, 1, 1)

        self.gridLayout_39.addWidget(self.frame_dto, 4, 0, 1, 2)

        self.frame_ofertaweb = QFrame(self.tab_promociones)
        self.frame_ofertaweb.setObjectName("frame_ofertaweb")
        self.frame_ofertaweb.setEnabled(False)
        self.frame_ofertaweb.setMinimumSize(QSize(0, 49))
        self.frame_ofertaweb.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_ofertaweb.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_ofertaweb)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalSpacer_8 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.horizontalLayout.addItem(self.horizontalSpacer_8)

        self.lbl_dto_web = QLabel(self.frame_ofertaweb)
        self.lbl_dto_web.setObjectName("lbl_dto_web")

        self.horizontalLayout.addWidget(self.lbl_dto_web)

        self.lbl_dto_web2 = QLabel(self.frame_ofertaweb)
        self.lbl_dto_web2.setObjectName("lbl_dto_web2")

        self.horizontalLayout.addWidget(self.lbl_dto_web2)

        self.txtOfertaDtoWeb = QLineEdit(self.frame_ofertaweb)
        self.txtOfertaDtoWeb.setObjectName("txtOfertaDtoWeb")
        self.txtOfertaDtoWeb.setMinimumSize(QSize(0, 27))
        self.txtOfertaDtoWeb.setMaximumSize(QSize(50, 27))
        self.txtOfertaDtoWeb.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.horizontalLayout.addWidget(self.txtOfertaDtoWeb)

        self.gridLayout_39.addWidget(self.frame_ofertaweb, 5, 0, 1, 2)

        self.label_68 = QLabel(self.tab_promociones)
        self.label_68.setObjectName("label_68")
        self.label_68.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_39.addWidget(self.label_68, 0, 4, 1, 1)

        self.label_21 = QLabel(self.tab_promociones)
        self.label_21.setObjectName("label_21")
        self.label_21.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_39.addWidget(self.label_21, 0, 2, 1, 1)

        self.chkMostrar_en_cuadro = QCheckBox(self.tab_promociones)
        self.chkMostrar_en_cuadro.setObjectName("chkMostrar_en_cuadro")

        self.gridLayout_39.addWidget(self.chkMostrar_en_cuadro, 0, 1, 1, 1)

        self.framePromocion = QFrame(self.tab_promociones)
        self.framePromocion.setObjectName("framePromocion")
        self.framePromocion.setEnabled(False)
        self.framePromocion.setFrameShape(QFrame.Shape.StyledPanel)
        self.framePromocion.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_34 = QGridLayout(self.framePromocion)
        self.gridLayout_34.setObjectName("gridLayout_34")
        self.lblDescripcion_oferta = QLabel(self.framePromocion)
        self.lblDescripcion_oferta.setObjectName("lblDescripcion_oferta")
        self.lblDescripcion_oferta.setEnabled(False)

        self.gridLayout_34.addWidget(self.lblDescripcion_oferta, 3, 0, 1, 1)

        self.txtOferta_Descripcion_promocion = QLineEdit(self.framePromocion)
        self.txtOferta_Descripcion_promocion.setObjectName(
            "txtOferta_Descripcion_promocion"
        )
        self.txtOferta_Descripcion_promocion.setEnabled(False)
        self.txtOferta_Descripcion_promocion.setProperty("mandatoryField", False)

        self.gridLayout_34.addWidget(self.txtOferta_Descripcion_promocion, 3, 1, 1, 1)

        self.btnAnadirOferta = QPushButton(self.framePromocion)
        self.btnAnadirOferta.setObjectName("btnAnadirOferta")
        self.btnAnadirOferta.setEnabled(False)
        sizePolicy4.setHeightForWidth(
            self.btnAnadirOferta.sizePolicy().hasHeightForWidth()
        )
        self.btnAnadirOferta.setSizePolicy(sizePolicy4)
        self.btnAnadirOferta.setIcon(icon1)

        self.gridLayout_34.addWidget(self.btnAnadirOferta, 0, 0, 1, 1)

        self.btnEditarOferta = QPushButton(self.framePromocion)
        self.btnEditarOferta.setObjectName("btnEditarOferta")
        self.btnEditarOferta.setEnabled(False)
        sizePolicy4.setHeightForWidth(
            self.btnEditarOferta.sizePolicy().hasHeightForWidth()
        )
        self.btnEditarOferta.setSizePolicy(sizePolicy4)
        self.btnEditarOferta.setIcon(icon5)

        self.gridLayout_34.addWidget(self.btnEditarOferta, 1, 0, 1, 1)

        self.btnguardar_oferta = QPushButton(self.framePromocion)
        self.btnguardar_oferta.setObjectName("btnguardar_oferta")
        self.btnguardar_oferta.setEnabled(False)
        self.btnguardar_oferta.setIcon(icon6)

        self.gridLayout_34.addWidget(self.btnguardar_oferta, 0, 1, 1, 1)

        self.btnDeshacerOferta = QPushButton(self.framePromocion)
        self.btnDeshacerOferta.setObjectName("btnDeshacerOferta")
        self.btnDeshacerOferta.setEnabled(False)
        self.btnDeshacerOferta.setIcon(icon7)

        self.gridLayout_34.addWidget(self.btnDeshacerOferta, 1, 1, 1, 1)

        self.chkOferta_32 = QRadioButton(self.framePromocion)
        self.chkOferta_32.setObjectName("chkOferta_32")
        self.chkOferta_32.setStyleSheet("")
        self.chkOferta_32.setCheckable(True)
        self.chkOferta_32.setChecked(True)

        self.gridLayout_34.addWidget(self.chkOferta_32, 4, 0, 1, 1)

        self.chkOferta_web = QRadioButton(self.framePromocion)
        self.chkOferta_web.setObjectName("chkOferta_web")
        self.chkOferta_web.setStyleSheet("")

        self.gridLayout_34.addWidget(self.chkOferta_web, 4, 1, 1, 1)

        self.chkOferta_dto = QRadioButton(self.framePromocion)
        self.chkOferta_dto.setObjectName("chkOferta_dto")
        self.chkOferta_dto.setEnabled(False)
        self.chkOferta_dto.setStyleSheet("")
        self.chkOferta_dto.setChecked(False)

        self.gridLayout_34.addWidget(self.chkOferta_dto, 5, 0, 1, 1)

        self.chkOfertaPvp = QRadioButton(self.framePromocion)
        self.chkOfertaPvp.setObjectName("chkOfertaPvp")
        self.chkOfertaPvp.setStyleSheet("")

        self.gridLayout_34.addWidget(self.chkOfertaPvp, 5, 1, 1, 1)

        self.gridLayout_39.addWidget(self.framePromocion, 1, 0, 2, 2)

        self.frame_comentarios = QFrame(self.tab_promociones)
        self.frame_comentarios.setObjectName("frame_comentarios")
        self.frame_comentarios.setEnabled(False)
        self.frame_comentarios.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_comentarios.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_27 = QGridLayout(self.frame_comentarios)
        self.gridLayout_27.setObjectName("gridLayout_27")
        self.txtOferta_comentarios_promocion = QTextEdit(self.frame_comentarios)
        self.txtOferta_comentarios_promocion.setObjectName(
            "txtOferta_comentarios_promocion"
        )

        self.gridLayout_27.addWidget(self.txtOferta_comentarios_promocion, 2, 0, 1, 1)

        self.label_65 = QLabel(self.frame_comentarios)
        self.label_65.setObjectName("label_65")
        self.label_65.setMinimumSize(QSize(0, 27))
        self.label_65.setStyleSheet(
            "background-color: #304163;\n" "color: rgb(255, 255, 255);"
        )
        self.label_65.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_27.addWidget(self.label_65, 1, 0, 1, 1)

        self.gridLayout_39.addWidget(self.frame_comentarios, 4, 2, 3, 5)

        self.frame_tabla_ofertas = QFrame(self.tab_promociones)
        self.frame_tabla_ofertas.setObjectName("frame_tabla_ofertas")
        self.frame_tabla_ofertas.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_tabla_ofertas.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_9 = QGridLayout(self.frame_tabla_ofertas)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label_72 = QLabel(self.frame_tabla_ofertas)
        self.label_72.setObjectName("label_72")
        self.label_72.setMinimumSize(QSize(0, 27))
        self.label_72.setStyleSheet(
            "background-color: #304163;\n" "color: rgb(255, 255, 255);"
        )
        self.label_72.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.label_72, 0, 0, 1, 5)

        self.btnActivarOferta = QPushButton(self.frame_tabla_ofertas)
        self.btnActivarOferta.setObjectName("btnActivarOferta")
        self.btnActivarOferta.setEnabled(False)
        icon11 = QIcon()
        icon11.addFile(
            ":/Icons/PNG/OK.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.btnActivarOferta.setIcon(icon11)

        self.gridLayout_6.addWidget(self.btnActivarOferta, 3, 0, 1, 2)

        self.tabla_ofertas = QTableView(self.frame_tabla_ofertas)
        self.tabla_ofertas.setObjectName("tabla_ofertas")
        self.tabla_ofertas.setAlternatingRowColors(True)
        self.tabla_ofertas.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.tabla_ofertas.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.tabla_ofertas.horizontalHeader().setStretchLastSection(True)
        self.tabla_ofertas.verticalHeader().setVisible(False)

        self.gridLayout_6.addWidget(self.tabla_ofertas, 2, 0, 1, 5)

        self.btnBorrarOferta = QPushButton(self.frame_tabla_ofertas)
        self.btnBorrarOferta.setObjectName("btnBorrarOferta")
        self.btnBorrarOferta.setEnabled(False)
        sizePolicy4.setHeightForWidth(
            self.btnBorrarOferta.sizePolicy().hasHeightForWidth()
        )
        self.btnBorrarOferta.setSizePolicy(sizePolicy4)
        icon12 = QIcon()
        icon12.addFile(
            ":/Icons/PNG/borrar.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.btnBorrarOferta.setIcon(icon12)

        self.gridLayout_6.addWidget(self.btnBorrarOferta, 3, 3, 1, 2)

        self.label = QLabel(self.frame_tabla_ofertas)
        self.label.setObjectName("label")

        self.gridLayout_6.addWidget(self.label, 1, 0, 1, 1)

        self.cboTarifaOferta = QComboBox(self.frame_tabla_ofertas)
        self.cboTarifaOferta.setObjectName("cboTarifaOferta")

        self.gridLayout_6.addWidget(self.cboTarifaOferta, 1, 1, 1, 2)

        self.gridLayout_9.addLayout(self.gridLayout_6, 0, 0, 1, 1)

        self.gridLayout_39.addWidget(self.frame_tabla_ofertas, 1, 2, 3, 5)

        self.Pestanas.addTab(self.tab_promociones, "")
        self.tab_imagenes = QWidget()
        self.tab_imagenes.setObjectName("tab_imagenes")
        self.gridLayout_23 = QGridLayout(self.tab_imagenes)
        self.gridLayout_23.setObjectName("gridLayout_23")
        self.lblImagenArticulo_2 = QLabel(self.tab_imagenes)
        self.lblImagenArticulo_2.setObjectName("lblImagenArticulo_2")
        sizePolicy7 = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        sizePolicy7.setHorizontalStretch(255)
        sizePolicy7.setVerticalStretch(255)
        sizePolicy7.setHeightForWidth(
            self.lblImagenArticulo_2.sizePolicy().hasHeightForWidth()
        )
        self.lblImagenArticulo_2.setSizePolicy(sizePolicy7)
        self.lblImagenArticulo_2.setMaximumSize(QSize(256, 256))
        self.lblImagenArticulo_2.setPixmap(QPixmap(":/Icons/PNG/paquete.png"))
        self.lblImagenArticulo_2.setScaledContents(True)

        self.gridLayout_23.addWidget(self.lblImagenArticulo_2, 0, 1, 1, 1)

        self.lblImagenArticulo_3 = QLabel(self.tab_imagenes)
        self.lblImagenArticulo_3.setObjectName("lblImagenArticulo_3")
        sizePolicy7.setHeightForWidth(
            self.lblImagenArticulo_3.sizePolicy().hasHeightForWidth()
        )
        self.lblImagenArticulo_3.setSizePolicy(sizePolicy7)
        self.lblImagenArticulo_3.setMaximumSize(QSize(256, 256))
        self.lblImagenArticulo_3.setPixmap(QPixmap(":/Icons/PNG/paquete.png"))
        self.lblImagenArticulo_3.setScaledContents(True)

        self.gridLayout_23.addWidget(self.lblImagenArticulo_3, 1, 0, 1, 1)

        self.lblImagenArticulo_1 = QLabel(self.tab_imagenes)
        self.lblImagenArticulo_1.setObjectName("lblImagenArticulo_1")
        sizePolicy7.setHeightForWidth(
            self.lblImagenArticulo_1.sizePolicy().hasHeightForWidth()
        )
        self.lblImagenArticulo_1.setSizePolicy(sizePolicy7)
        self.lblImagenArticulo_1.setMaximumSize(QSize(256, 256))
        self.lblImagenArticulo_1.setPixmap(QPixmap(":/Icons/PNG/paquete.png"))
        self.lblImagenArticulo_1.setScaledContents(True)

        self.gridLayout_23.addWidget(self.lblImagenArticulo_1, 0, 0, 1, 1)

        self.lblImagenArticulo_4 = QLabel(self.tab_imagenes)
        self.lblImagenArticulo_4.setObjectName("lblImagenArticulo_4")
        sizePolicy7.setHeightForWidth(
            self.lblImagenArticulo_4.sizePolicy().hasHeightForWidth()
        )
        self.lblImagenArticulo_4.setSizePolicy(sizePolicy7)
        self.lblImagenArticulo_4.setMaximumSize(QSize(256, 256))
        self.lblImagenArticulo_4.setPixmap(QPixmap(":/Icons/PNG/paquete.png"))
        self.lblImagenArticulo_4.setScaledContents(True)

        self.gridLayout_23.addWidget(self.lblImagenArticulo_4, 1, 1, 1, 1)

        self.Pestanas.addTab(self.tab_imagenes, "")
        self.tab_estadistica = QWidget()
        self.tab_estadistica.setObjectName("tab_estadistica")
        self.gridLayout_37 = QGridLayout(self.tab_estadistica)
        self.gridLayout_37.setObjectName("gridLayout_37")
        self.verticalSpacer_4 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.gridLayout_37.addItem(self.verticalSpacer_4, 3, 0, 1, 1)

        self.frame = QFrame(self.tab_estadistica)
        self.frame.setObjectName("frame")
        self.gridLayout_12 = QGridLayout(self.frame)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.label_28 = QLabel(self.frame)
        self.label_28.setObjectName("label_28")

        self.gridLayout_12.addWidget(self.label_28, 0, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.gridLayout_12.addItem(self.horizontalSpacer_3, 2, 3, 1, 1)

        self.label_29 = QLabel(self.frame)
        self.label_29.setObjectName("label_29")

        self.gridLayout_12.addWidget(self.label_29, 0, 4, 1, 1)

        self.lblFechaVenta = QLabel(self.frame)
        self.lblFechaVenta.setObjectName("lblFechaVenta")

        self.gridLayout_12.addWidget(self.lblFechaVenta, 2, 4, 1, 1)

        self.txtFechaUltimaVenta = QDateEdit(self.frame)
        self.txtFechaUltimaVenta.setObjectName("txtFechaUltimaVenta")
        self.txtFechaUltimaVenta.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_12.addWidget(self.txtFechaUltimaVenta, 2, 5, 1, 1)

        self.txtunidades_vendidas = QLineEdit(self.frame)
        self.txtunidades_vendidas.setObjectName("txtunidades_vendidas")
        self.txtunidades_vendidas.setEnabled(True)
        sizePolicy3.setHeightForWidth(
            self.txtunidades_vendidas.sizePolicy().hasHeightForWidth()
        )
        self.txtunidades_vendidas.setSizePolicy(sizePolicy3)
        self.txtunidades_vendidas.setMaximumSize(QSize(120, 27))
        self.txtunidades_vendidas.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_12.addWidget(self.txtunidades_vendidas, 0, 5, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.gridLayout_12.addItem(self.horizontalSpacer_4, 2, 0, 1, 1)

        self.txtimporte_acumulado_compras = QLineEdit(self.frame)
        self.txtimporte_acumulado_compras.setObjectName("txtimporte_acumulado_compras")
        self.txtimporte_acumulado_compras.setEnabled(True)
        sizePolicy3.setHeightForWidth(
            self.txtimporte_acumulado_compras.sizePolicy().hasHeightForWidth()
        )
        self.txtimporte_acumulado_compras.setSizePolicy(sizePolicy3)
        self.txtimporte_acumulado_compras.setMaximumSize(QSize(120, 27))
        self.txtimporte_acumulado_compras.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_12.addWidget(self.txtimporte_acumulado_compras, 1, 2, 1, 1)

        self.txtunidades_compradas = QLineEdit(self.frame)
        self.txtunidades_compradas.setObjectName("txtunidades_compradas")
        self.txtunidades_compradas.setEnabled(True)
        sizePolicy.setHeightForWidth(
            self.txtunidades_compradas.sizePolicy().hasHeightForWidth()
        )
        self.txtunidades_compradas.setSizePolicy(sizePolicy)
        self.txtunidades_compradas.setMaximumSize(QSize(120, 27))
        self.txtunidades_compradas.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_12.addWidget(self.txtunidades_compradas, 0, 2, 1, 1)

        self.txtfechaUltimaCompra = QDateEdit(self.frame)
        self.txtfechaUltimaCompra.setObjectName("txtfechaUltimaCompra")
        self.txtfechaUltimaCompra.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_12.addWidget(self.txtfechaUltimaCompra, 2, 2, 1, 1)

        self.label_43 = QLabel(self.frame)
        self.label_43.setObjectName("label_43")

        self.gridLayout_12.addWidget(self.label_43, 1, 4, 1, 1)

        self.txtimporte_acumulado_ventas = QLineEdit(self.frame)
        self.txtimporte_acumulado_ventas.setObjectName("txtimporte_acumulado_ventas")
        self.txtimporte_acumulado_ventas.setEnabled(True)
        sizePolicy3.setHeightForWidth(
            self.txtimporte_acumulado_ventas.sizePolicy().hasHeightForWidth()
        )
        self.txtimporte_acumulado_ventas.setSizePolicy(sizePolicy3)
        self.txtimporte_acumulado_ventas.setMaximumSize(QSize(120, 27))
        self.txtimporte_acumulado_ventas.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_12.addWidget(self.txtimporte_acumulado_ventas, 1, 5, 1, 1)

        self.label_42 = QLabel(self.frame)
        self.label_42.setObjectName("label_42")

        self.gridLayout_12.addWidget(self.label_42, 1, 1, 1, 1)

        self.lblFechaCompra = QLabel(self.frame)
        self.lblFechaCompra.setObjectName("lblFechaCompra")

        self.gridLayout_12.addWidget(self.lblFechaCompra, 2, 1, 1, 1)

        self.horizontalSpacer_10 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.gridLayout_12.addItem(self.horizontalSpacer_10, 1, 6, 1, 1)

        self.gridLayout_37.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_6 = QFrame(self.tab_estadistica)
        self.frame_6.setObjectName("frame_6")
        self.frame_6.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_33 = QGridLayout(self.frame_6)
        self.gridLayout_33.setObjectName("gridLayout_33")
        self.label_30 = QLabel(self.frame_6)
        self.label_30.setObjectName("label_30")
        self.label_30.setAutoFillBackground(False)

        self.gridLayout_33.addWidget(self.label_30, 0, 1, 1, 1)

        self.label_45 = QLabel(self.frame_6)
        self.label_45.setObjectName("label_45")

        self.gridLayout_33.addWidget(self.label_45, 3, 1, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.gridLayout_33.addItem(self.horizontalSpacer_6, 0, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.gridLayout_33.addItem(self.horizontalSpacer, 0, 3, 1, 1)

        self.label_31 = QLabel(self.frame_6)
        self.label_31.setObjectName("label_31")

        self.gridLayout_33.addWidget(self.label_31, 0, 4, 1, 1)

        self.label_32 = QLabel(self.frame_6)
        self.label_32.setObjectName("label_32")

        self.gridLayout_33.addWidget(self.label_32, 4, 1, 1, 1)

        self.label_44 = QLabel(self.frame_6)
        self.label_44.setObjectName("label_44")

        self.gridLayout_33.addWidget(self.label_44, 2, 1, 1, 1)

        self.txtstock_real_2 = QLineEdit(self.frame_6)
        self.txtstock_real_2.setObjectName("txtstock_real_2")
        self.txtstock_real_2.setEnabled(True)
        sizePolicy3.setHeightForWidth(
            self.txtstock_real_2.sizePolicy().hasHeightForWidth()
        )
        self.txtstock_real_2.setSizePolicy(sizePolicy3)
        self.txtstock_real_2.setMinimumSize(QSize(0, 27))
        self.txtstock_real_2.setMaximumSize(QSize(120, 27))
        self.txtstock_real_2.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_33.addWidget(self.txtstock_real_2, 4, 2, 1, 1)

        self.txtstock_minimo = QLineEdit(self.frame_6)
        self.txtstock_minimo.setObjectName("txtstock_minimo")
        sizePolicy3.setHeightForWidth(
            self.txtstock_minimo.sizePolicy().hasHeightForWidth()
        )
        self.txtstock_minimo.setSizePolicy(sizePolicy3)
        self.txtstock_minimo.setMaximumSize(QSize(120, 27))
        self.txtstock_minimo.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_33.addWidget(self.txtstock_minimo, 0, 2, 1, 1)

        self.txtunidades_reservadas = QLineEdit(self.frame_6)
        self.txtunidades_reservadas.setObjectName("txtunidades_reservadas")
        self.txtunidades_reservadas.setEnabled(True)
        sizePolicy3.setHeightForWidth(
            self.txtunidades_reservadas.sizePolicy().hasHeightForWidth()
        )
        self.txtunidades_reservadas.setSizePolicy(sizePolicy3)
        self.txtunidades_reservadas.setMaximumSize(QSize(120, 27))
        self.txtunidades_reservadas.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_33.addWidget(self.txtunidades_reservadas, 3, 2, 1, 1)

        self.txtFechaPrevistaEntrega = QDateEdit(self.frame_6)
        self.txtFechaPrevistaEntrega.setObjectName("txtFechaPrevistaEntrega")
        self.txtFechaPrevistaEntrega.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_33.addWidget(self.txtFechaPrevistaEntrega, 2, 7, 1, 1)

        self.txtstock_maximo = QLineEdit(self.frame_6)
        self.txtstock_maximo.setObjectName("txtstock_maximo")
        sizePolicy3.setHeightForWidth(
            self.txtstock_maximo.sizePolicy().hasHeightForWidth()
        )
        self.txtstock_maximo.setSizePolicy(sizePolicy3)
        self.txtstock_maximo.setMaximumSize(QSize(120, 27))
        self.txtstock_maximo.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_33.addWidget(self.txtstock_maximo, 0, 7, 1, 1)

        self.lblFechaPrevistaEntrega = QLabel(self.frame_6)
        self.lblFechaPrevistaEntrega.setObjectName("lblFechaPrevistaEntrega")

        self.gridLayout_33.addWidget(self.lblFechaPrevistaEntrega, 2, 4, 1, 1)

        self.txtcantidad_pendiente_recibir = QLineEdit(self.frame_6)
        self.txtcantidad_pendiente_recibir.setObjectName(
            "txtcantidad_pendiente_recibir"
        )
        self.txtcantidad_pendiente_recibir.setEnabled(True)
        sizePolicy3.setHeightForWidth(
            self.txtcantidad_pendiente_recibir.sizePolicy().hasHeightForWidth()
        )
        self.txtcantidad_pendiente_recibir.setSizePolicy(sizePolicy3)
        self.txtcantidad_pendiente_recibir.setMaximumSize(QSize(120, 27))
        self.txtcantidad_pendiente_recibir.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_33.addWidget(self.txtcantidad_pendiente_recibir, 2, 2, 1, 1)

        self.txtstock_fisico_almacen = QLineEdit(self.frame_6)
        self.txtstock_fisico_almacen.setObjectName("txtstock_fisico_almacen")
        self.txtstock_fisico_almacen.setMaximumSize(QSize(120, 27))
        self.txtstock_fisico_almacen.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_33.addWidget(self.txtstock_fisico_almacen, 1, 2, 1, 1)

        self.label_22 = QLabel(self.frame_6)
        self.label_22.setObjectName("label_22")

        self.gridLayout_33.addWidget(self.label_22, 1, 1, 1, 1)

        self.horizontalSpacer_11 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.gridLayout_33.addItem(self.horizontalSpacer_11, 2, 8, 1, 1)

        self.gridLayout_37.addWidget(self.frame_6, 1, 0, 1, 1)

        self.Pestanas.addTab(self.tab_estadistica, "")
        self.tab_grafica = QWidget()
        self.tab_grafica.setObjectName("tab_grafica")
        self.gridLayout_3 = QGridLayout(self.tab_grafica)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.frame_9 = QFrame(self.tab_grafica)
        self.frame_9.setObjectName("frame_9")
        self.frame_9.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_9)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.ChartViewWidget = ChartViewWidget(self.frame_9)
        self.ChartViewWidget.setObjectName("ChartViewWidget")

        self.verticalLayout_3.addWidget(self.ChartViewWidget)

        self.cboTipoGrafica = QComboBox(self.frame_9)
        self.cboTipoGrafica.addItem("")
        self.cboTipoGrafica.addItem("")
        self.cboTipoGrafica.setObjectName("cboTipoGrafica")

        self.verticalLayout_3.addWidget(self.cboTipoGrafica)

        self.radGrafica_unidades = QRadioButton(self.frame_9)
        self.radGrafica_unidades.setObjectName("radGrafica_unidades")
        self.radGrafica_unidades.setChecked(True)

        self.verticalLayout_3.addWidget(self.radGrafica_unidades)

        self.radGrafica_importes = QRadioButton(self.frame_9)
        self.radGrafica_importes.setObjectName("radGrafica_importes")

        self.verticalLayout_3.addWidget(self.radGrafica_importes)

        self.chkValorGrafica = QCheckBox(self.frame_9)
        self.chkValorGrafica.setObjectName("chkValorGrafica")
        self.chkValorGrafica.setAutoFillBackground(False)
        self.chkValorGrafica.setChecked(True)

        self.verticalLayout_3.addWidget(self.chkValorGrafica)

        self.gridLayout_3.addWidget(self.frame_9, 0, 0, 1, 1)

        self.cajaValores = QFrame(self.tab_grafica)
        self.cajaValores.setObjectName("cajaValores")
        self.cajaValores.setMinimumSize(QSize(512, 0))
        self.cajaValores.setFrameShape(QFrame.Shape.StyledPanel)
        self.cajaValores.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_22 = QGridLayout(self.cajaValores)
        self.gridLayout_22.setObjectName("gridLayout_22")
        self.frame_14 = QFrame(self.cajaValores)
        self.frame_14.setObjectName("frame_14")
        self.frame_14.setStyleSheet("")
        self.frame_14.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_14.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_18 = QGridLayout(self.frame_14)
        self.gridLayout_18.setObjectName("gridLayout_18")
        self.label_25 = QLabel(self.frame_14)
        self.label_25.setObjectName("label_25")
        self.label_25.setStyleSheet("")

        self.gridLayout_18.addWidget(self.label_25, 0, 0, 1, 1)

        self.gridLayout_20 = QGridLayout()
        self.gridLayout_20.setObjectName("gridLayout_20")
        self.txtImporte_compras_enero = QLineEdit(self.frame_14)
        self.txtImporte_compras_enero.setObjectName("txtImporte_compras_enero")
        self.txtImporte_compras_enero.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_compras_enero.setStyleSheet("")
        self.txtImporte_compras_enero.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_20.addWidget(self.txtImporte_compras_enero, 1, 2, 1, 1)

        self.txtImporte_compras_julio = QLineEdit(self.frame_14)
        self.txtImporte_compras_julio.setObjectName("txtImporte_compras_julio")
        self.txtImporte_compras_julio.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_compras_julio.setStyleSheet("")
        self.txtImporte_compras_julio.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_20.addWidget(self.txtImporte_compras_julio, 7, 2, 1, 1)

        self.txtImporte_compras_marzo = QLineEdit(self.frame_14)
        self.txtImporte_compras_marzo.setObjectName("txtImporte_compras_marzo")
        self.txtImporte_compras_marzo.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_compras_marzo.setStyleSheet("")
        self.txtImporte_compras_marzo.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_20.addWidget(self.txtImporte_compras_marzo, 3, 2, 1, 1)

        self.txtUnid_compras_febrero = QLineEdit(self.frame_14)
        self.txtUnid_compras_febrero.setObjectName("txtUnid_compras_febrero")
        self.txtUnid_compras_febrero.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_compras_febrero.setStyleSheet("")
        self.txtUnid_compras_febrero.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_20.addWidget(self.txtUnid_compras_febrero, 2, 1, 1, 1)

        self.txtUnid_compras_marzo = QLineEdit(self.frame_14)
        self.txtUnid_compras_marzo.setObjectName("txtUnid_compras_marzo")
        self.txtUnid_compras_marzo.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_compras_marzo.setStyleSheet("")
        self.txtUnid_compras_marzo.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_20.addWidget(self.txtUnid_compras_marzo, 3, 1, 1, 1)

        self.txtImporte_compras_septiembre = QLineEdit(self.frame_14)
        self.txtImporte_compras_septiembre.setObjectName(
            "txtImporte_compras_septiembre"
        )
        self.txtImporte_compras_septiembre.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_compras_septiembre.setStyleSheet("")
        self.txtImporte_compras_septiembre.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_20.addWidget(self.txtImporte_compras_septiembre, 9, 2, 1, 1)

        self.label_52 = QLabel(self.frame_14)
        self.label_52.setObjectName("label_52")
        self.label_52.setStyleSheet("")

        self.gridLayout_20.addWidget(self.label_52, 0, 1, 1, 1)

        self.txtImporte_compras_diciembre = QLineEdit(self.frame_14)
        self.txtImporte_compras_diciembre.setObjectName("txtImporte_compras_diciembre")
        self.txtImporte_compras_diciembre.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_compras_diciembre.setStyleSheet("")
        self.txtImporte_compras_diciembre.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_20.addWidget(self.txtImporte_compras_diciembre, 12, 2, 1, 1)

        self.txtUnid_compras_agosto = QLineEdit(self.frame_14)
        self.txtUnid_compras_agosto.setObjectName("txtUnid_compras_agosto")
        self.txtUnid_compras_agosto.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_compras_agosto.setStyleSheet("")
        self.txtUnid_compras_agosto.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_20.addWidget(self.txtUnid_compras_agosto, 8, 1, 1, 1)

        self.txtUnid_compras_diciembre = QLineEdit(self.frame_14)
        self.txtUnid_compras_diciembre.setObjectName("txtUnid_compras_diciembre")
        self.txtUnid_compras_diciembre.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_compras_diciembre.setStyleSheet("")
        self.txtUnid_compras_diciembre.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_20.addWidget(self.txtUnid_compras_diciembre, 12, 1, 1, 1)

        self.txtUnid_compras_junio = QLineEdit(self.frame_14)
        self.txtUnid_compras_junio.setObjectName("txtUnid_compras_junio")
        self.txtUnid_compras_junio.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_compras_junio.setStyleSheet("")
        self.txtUnid_compras_junio.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_20.addWidget(self.txtUnid_compras_junio, 6, 1, 1, 1)

        self.txtUnid_compras_mayo = QLineEdit(self.frame_14)
        self.txtUnid_compras_mayo.setObjectName("txtUnid_compras_mayo")
        self.txtUnid_compras_mayo.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_compras_mayo.setStyleSheet("")
        self.txtUnid_compras_mayo.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_20.addWidget(self.txtUnid_compras_mayo, 5, 1, 1, 1)

        self.txtUnid_compras_enero = QLineEdit(self.frame_14)
        self.txtUnid_compras_enero.setObjectName("txtUnid_compras_enero")
        self.txtUnid_compras_enero.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_compras_enero.setStyleSheet("")
        self.txtUnid_compras_enero.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_20.addWidget(self.txtUnid_compras_enero, 1, 1, 1, 1)

        self.txtImporte_compras_octubre = QLineEdit(self.frame_14)
        self.txtImporte_compras_octubre.setObjectName("txtImporte_compras_octubre")
        self.txtImporte_compras_octubre.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_compras_octubre.setStyleSheet("")
        self.txtImporte_compras_octubre.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_20.addWidget(self.txtImporte_compras_octubre, 10, 2, 1, 1)

        self.txtImporte_compras_noviembre = QLineEdit(self.frame_14)
        self.txtImporte_compras_noviembre.setObjectName("txtImporte_compras_noviembre")
        self.txtImporte_compras_noviembre.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_compras_noviembre.setStyleSheet("")
        self.txtImporte_compras_noviembre.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_20.addWidget(self.txtImporte_compras_noviembre, 11, 2, 1, 1)

        self.txtUnid_compras_noviembre = QLineEdit(self.frame_14)
        self.txtUnid_compras_noviembre.setObjectName("txtUnid_compras_noviembre")
        self.txtUnid_compras_noviembre.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_compras_noviembre.setStyleSheet("")
        self.txtUnid_compras_noviembre.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_20.addWidget(self.txtUnid_compras_noviembre, 11, 1, 1, 1)

        self.txtImporte_compras_agosto = QLineEdit(self.frame_14)
        self.txtImporte_compras_agosto.setObjectName("txtImporte_compras_agosto")
        self.txtImporte_compras_agosto.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_compras_agosto.setStyleSheet("")
        self.txtImporte_compras_agosto.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_20.addWidget(self.txtImporte_compras_agosto, 8, 2, 1, 1)

        self.txtImporte_compras_mayo = QLineEdit(self.frame_14)
        self.txtImporte_compras_mayo.setObjectName("txtImporte_compras_mayo")
        self.txtImporte_compras_mayo.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_compras_mayo.setStyleSheet("")
        self.txtImporte_compras_mayo.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_20.addWidget(self.txtImporte_compras_mayo, 5, 2, 1, 1)

        self.txtUnid_compras_septiembre = QLineEdit(self.frame_14)
        self.txtUnid_compras_septiembre.setObjectName("txtUnid_compras_septiembre")
        self.txtUnid_compras_septiembre.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_compras_septiembre.setStyleSheet("")
        self.txtUnid_compras_septiembre.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_20.addWidget(self.txtUnid_compras_septiembre, 9, 1, 1, 1)

        self.txtImporte_compras_febrero = QLineEdit(self.frame_14)
        self.txtImporte_compras_febrero.setObjectName("txtImporte_compras_febrero")
        self.txtImporte_compras_febrero.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_compras_febrero.setStyleSheet("")
        self.txtImporte_compras_febrero.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_20.addWidget(self.txtImporte_compras_febrero, 2, 2, 1, 1)

        self.txtUnid_compras_abril = QLineEdit(self.frame_14)
        self.txtUnid_compras_abril.setObjectName("txtUnid_compras_abril")
        self.txtUnid_compras_abril.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_compras_abril.setStyleSheet("")
        self.txtUnid_compras_abril.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_20.addWidget(self.txtUnid_compras_abril, 4, 1, 1, 1)

        self.txtImporte_compras_abril = QLineEdit(self.frame_14)
        self.txtImporte_compras_abril.setObjectName("txtImporte_compras_abril")
        self.txtImporte_compras_abril.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_compras_abril.setStyleSheet("")
        self.txtImporte_compras_abril.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_20.addWidget(self.txtImporte_compras_abril, 4, 2, 1, 1)

        self.label_53 = QLabel(self.frame_14)
        self.label_53.setObjectName("label_53")
        self.label_53.setStyleSheet("")

        self.gridLayout_20.addWidget(self.label_53, 0, 2, 1, 1)

        self.txtUnid_compras_julio = QLineEdit(self.frame_14)
        self.txtUnid_compras_julio.setObjectName("txtUnid_compras_julio")
        self.txtUnid_compras_julio.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_compras_julio.setStyleSheet("")
        self.txtUnid_compras_julio.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_20.addWidget(self.txtUnid_compras_julio, 7, 1, 1, 1)

        self.txtImporte_compras_junio = QLineEdit(self.frame_14)
        self.txtImporte_compras_junio.setObjectName("txtImporte_compras_junio")
        self.txtImporte_compras_junio.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_compras_junio.setStyleSheet("")
        self.txtImporte_compras_junio.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_20.addWidget(self.txtImporte_compras_junio, 6, 2, 1, 1)

        self.txtUnid_compras_octubre = QLineEdit(self.frame_14)
        self.txtUnid_compras_octubre.setObjectName("txtUnid_compras_octubre")
        self.txtUnid_compras_octubre.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_compras_octubre.setStyleSheet("")
        self.txtUnid_compras_octubre.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_20.addWidget(self.txtUnid_compras_octubre, 10, 1, 1, 1)

        self.label_27 = QLabel(self.frame_14)
        self.label_27.setObjectName("label_27")
        self.label_27.setStyleSheet("")

        self.gridLayout_20.addWidget(self.label_27, 1, 0, 1, 1)

        self.label_35 = QLabel(self.frame_14)
        self.label_35.setObjectName("label_35")
        self.label_35.setStyleSheet("")

        self.gridLayout_20.addWidget(self.label_35, 2, 0, 1, 1)

        self.label_36 = QLabel(self.frame_14)
        self.label_36.setObjectName("label_36")
        self.label_36.setStyleSheet("")

        self.gridLayout_20.addWidget(self.label_36, 3, 0, 1, 1)

        self.label_37 = QLabel(self.frame_14)
        self.label_37.setObjectName("label_37")
        self.label_37.setStyleSheet("")

        self.gridLayout_20.addWidget(self.label_37, 4, 0, 1, 1)

        self.label_39 = QLabel(self.frame_14)
        self.label_39.setObjectName("label_39")
        self.label_39.setStyleSheet("")

        self.gridLayout_20.addWidget(self.label_39, 5, 0, 1, 1)

        self.label_40 = QLabel(self.frame_14)
        self.label_40.setObjectName("label_40")
        self.label_40.setStyleSheet("")

        self.gridLayout_20.addWidget(self.label_40, 6, 0, 1, 1)

        self.label_41 = QLabel(self.frame_14)
        self.label_41.setObjectName("label_41")
        self.label_41.setStyleSheet("")

        self.gridLayout_20.addWidget(self.label_41, 7, 0, 1, 1)

        self.label_46 = QLabel(self.frame_14)
        self.label_46.setObjectName("label_46")
        self.label_46.setStyleSheet("")

        self.gridLayout_20.addWidget(self.label_46, 8, 0, 1, 1)

        self.label_47 = QLabel(self.frame_14)
        self.label_47.setObjectName("label_47")
        self.label_47.setStyleSheet("")

        self.gridLayout_20.addWidget(self.label_47, 9, 0, 1, 1)

        self.label_48 = QLabel(self.frame_14)
        self.label_48.setObjectName("label_48")
        self.label_48.setStyleSheet("")

        self.gridLayout_20.addWidget(self.label_48, 10, 0, 1, 1)

        self.label_49 = QLabel(self.frame_14)
        self.label_49.setObjectName("label_49")
        self.label_49.setStyleSheet("")

        self.gridLayout_20.addWidget(self.label_49, 11, 0, 1, 1)

        self.label_50 = QLabel(self.frame_14)
        self.label_50.setObjectName("label_50")
        self.label_50.setStyleSheet("")

        self.gridLayout_20.addWidget(self.label_50, 12, 0, 1, 1)

        self.gridLayout_18.addLayout(self.gridLayout_20, 1, 0, 2, 3)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.gridLayout_18.addItem(self.verticalSpacer, 3, 0, 1, 1)

        self.gridLayout_22.addWidget(self.frame_14, 0, 0, 1, 1)

        self.frame_15 = QFrame(self.cajaValores)
        self.frame_15.setObjectName("frame_15")
        self.frame_15.setStyleSheet("")
        self.frame_15.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_15.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_19 = QGridLayout(self.frame_15)
        self.gridLayout_19.setObjectName("gridLayout_19")
        self.label_26 = QLabel(self.frame_15)
        self.label_26.setObjectName("label_26")
        self.label_26.setStyleSheet("")

        self.gridLayout_19.addWidget(self.label_26, 0, 0, 1, 1)

        self.gridLayout_21 = QGridLayout()
        self.gridLayout_21.setObjectName("gridLayout_21")
        self.label_54 = QLabel(self.frame_15)
        self.label_54.setObjectName("label_54")
        self.label_54.setStyleSheet("")

        self.gridLayout_21.addWidget(self.label_54, 0, 0, 1, 1)

        self.label_55 = QLabel(self.frame_15)
        self.label_55.setObjectName("label_55")
        self.label_55.setStyleSheet("")

        self.gridLayout_21.addWidget(self.label_55, 0, 1, 1, 1)

        self.txtUnid_ventas_enero = QLineEdit(self.frame_15)
        self.txtUnid_ventas_enero.setObjectName("txtUnid_ventas_enero")
        self.txtUnid_ventas_enero.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_ventas_enero.setStyleSheet("")
        self.txtUnid_ventas_enero.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_21.addWidget(self.txtUnid_ventas_enero, 1, 0, 1, 1)

        self.txtImporte_ventas_enero = QLineEdit(self.frame_15)
        self.txtImporte_ventas_enero.setObjectName("txtImporte_ventas_enero")
        self.txtImporte_ventas_enero.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_ventas_enero.setStyleSheet("")
        self.txtImporte_ventas_enero.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_21.addWidget(self.txtImporte_ventas_enero, 1, 1, 1, 1)

        self.txtUnid_ventas_febrero = QLineEdit(self.frame_15)
        self.txtUnid_ventas_febrero.setObjectName("txtUnid_ventas_febrero")
        self.txtUnid_ventas_febrero.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_ventas_febrero.setStyleSheet("")
        self.txtUnid_ventas_febrero.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_21.addWidget(self.txtUnid_ventas_febrero, 2, 0, 1, 1)

        self.txtImporte_ventas_febrero = QLineEdit(self.frame_15)
        self.txtImporte_ventas_febrero.setObjectName("txtImporte_ventas_febrero")
        self.txtImporte_ventas_febrero.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_ventas_febrero.setStyleSheet("")
        self.txtImporte_ventas_febrero.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_21.addWidget(self.txtImporte_ventas_febrero, 2, 1, 1, 1)

        self.txtUnid_ventas_marzo = QLineEdit(self.frame_15)
        self.txtUnid_ventas_marzo.setObjectName("txtUnid_ventas_marzo")
        self.txtUnid_ventas_marzo.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_ventas_marzo.setStyleSheet("")
        self.txtUnid_ventas_marzo.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_21.addWidget(self.txtUnid_ventas_marzo, 3, 0, 1, 1)

        self.txtImporte_ventas_marzo = QLineEdit(self.frame_15)
        self.txtImporte_ventas_marzo.setObjectName("txtImporte_ventas_marzo")
        self.txtImporte_ventas_marzo.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_ventas_marzo.setStyleSheet("")
        self.txtImporte_ventas_marzo.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_21.addWidget(self.txtImporte_ventas_marzo, 3, 1, 1, 1)

        self.txtUnid_ventas_abril = QLineEdit(self.frame_15)
        self.txtUnid_ventas_abril.setObjectName("txtUnid_ventas_abril")
        self.txtUnid_ventas_abril.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_ventas_abril.setStyleSheet("")
        self.txtUnid_ventas_abril.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_21.addWidget(self.txtUnid_ventas_abril, 4, 0, 1, 1)

        self.txtImporte_ventas_abril = QLineEdit(self.frame_15)
        self.txtImporte_ventas_abril.setObjectName("txtImporte_ventas_abril")
        self.txtImporte_ventas_abril.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_ventas_abril.setStyleSheet("")
        self.txtImporte_ventas_abril.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_21.addWidget(self.txtImporte_ventas_abril, 4, 1, 1, 1)

        self.txtUnid_ventas_mayo = QLineEdit(self.frame_15)
        self.txtUnid_ventas_mayo.setObjectName("txtUnid_ventas_mayo")
        self.txtUnid_ventas_mayo.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_ventas_mayo.setStyleSheet("")
        self.txtUnid_ventas_mayo.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_21.addWidget(self.txtUnid_ventas_mayo, 5, 0, 1, 1)

        self.txtImporte_ventas_mayo = QLineEdit(self.frame_15)
        self.txtImporte_ventas_mayo.setObjectName("txtImporte_ventas_mayo")
        self.txtImporte_ventas_mayo.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_ventas_mayo.setStyleSheet("")
        self.txtImporte_ventas_mayo.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_21.addWidget(self.txtImporte_ventas_mayo, 5, 1, 1, 1)

        self.txtUnid_ventas_junio = QLineEdit(self.frame_15)
        self.txtUnid_ventas_junio.setObjectName("txtUnid_ventas_junio")
        self.txtUnid_ventas_junio.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_ventas_junio.setStyleSheet("")
        self.txtUnid_ventas_junio.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_21.addWidget(self.txtUnid_ventas_junio, 6, 0, 1, 1)

        self.txtImporte_ventas_junio = QLineEdit(self.frame_15)
        self.txtImporte_ventas_junio.setObjectName("txtImporte_ventas_junio")
        self.txtImporte_ventas_junio.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_ventas_junio.setStyleSheet("")
        self.txtImporte_ventas_junio.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_21.addWidget(self.txtImporte_ventas_junio, 6, 1, 1, 1)

        self.txtUnid_ventas_julio = QLineEdit(self.frame_15)
        self.txtUnid_ventas_julio.setObjectName("txtUnid_ventas_julio")
        self.txtUnid_ventas_julio.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_ventas_julio.setStyleSheet("")
        self.txtUnid_ventas_julio.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_21.addWidget(self.txtUnid_ventas_julio, 7, 0, 1, 1)

        self.txtImporte_ventas_julio = QLineEdit(self.frame_15)
        self.txtImporte_ventas_julio.setObjectName("txtImporte_ventas_julio")
        self.txtImporte_ventas_julio.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_ventas_julio.setStyleSheet("")
        self.txtImporte_ventas_julio.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_21.addWidget(self.txtImporte_ventas_julio, 7, 1, 1, 1)

        self.txtUnid_ventas_agosto = QLineEdit(self.frame_15)
        self.txtUnid_ventas_agosto.setObjectName("txtUnid_ventas_agosto")
        self.txtUnid_ventas_agosto.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_ventas_agosto.setStyleSheet("")
        self.txtUnid_ventas_agosto.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_21.addWidget(self.txtUnid_ventas_agosto, 8, 0, 1, 1)

        self.txtImporte_ventas_agosto = QLineEdit(self.frame_15)
        self.txtImporte_ventas_agosto.setObjectName("txtImporte_ventas_agosto")
        self.txtImporte_ventas_agosto.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_ventas_agosto.setStyleSheet("")
        self.txtImporte_ventas_agosto.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_21.addWidget(self.txtImporte_ventas_agosto, 8, 1, 1, 1)

        self.txtUnid_ventas_septiembre = QLineEdit(self.frame_15)
        self.txtUnid_ventas_septiembre.setObjectName("txtUnid_ventas_septiembre")
        self.txtUnid_ventas_septiembre.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_ventas_septiembre.setStyleSheet("")
        self.txtUnid_ventas_septiembre.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_21.addWidget(self.txtUnid_ventas_septiembre, 9, 0, 1, 1)

        self.txtImporte_ventas_septiembre = QLineEdit(self.frame_15)
        self.txtImporte_ventas_septiembre.setObjectName("txtImporte_ventas_septiembre")
        self.txtImporte_ventas_septiembre.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_ventas_septiembre.setStyleSheet("")
        self.txtImporte_ventas_septiembre.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_21.addWidget(self.txtImporte_ventas_septiembre, 9, 1, 1, 1)

        self.txtUnid_ventas_octubre = QLineEdit(self.frame_15)
        self.txtUnid_ventas_octubre.setObjectName("txtUnid_ventas_octubre")
        self.txtUnid_ventas_octubre.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_ventas_octubre.setStyleSheet("")
        self.txtUnid_ventas_octubre.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_21.addWidget(self.txtUnid_ventas_octubre, 10, 0, 1, 1)

        self.txtImporte_ventas_octubre = QLineEdit(self.frame_15)
        self.txtImporte_ventas_octubre.setObjectName("txtImporte_ventas_octubre")
        self.txtImporte_ventas_octubre.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_ventas_octubre.setStyleSheet("")
        self.txtImporte_ventas_octubre.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_21.addWidget(self.txtImporte_ventas_octubre, 10, 1, 1, 1)

        self.txtUnid_ventas_noviembre = QLineEdit(self.frame_15)
        self.txtUnid_ventas_noviembre.setObjectName("txtUnid_ventas_noviembre")
        self.txtUnid_ventas_noviembre.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_ventas_noviembre.setStyleSheet("")
        self.txtUnid_ventas_noviembre.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_21.addWidget(self.txtUnid_ventas_noviembre, 11, 0, 1, 1)

        self.txtImporte_ventas_noviembre = QLineEdit(self.frame_15)
        self.txtImporte_ventas_noviembre.setObjectName("txtImporte_ventas_noviembre")
        self.txtImporte_ventas_noviembre.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_ventas_noviembre.setStyleSheet("")
        self.txtImporte_ventas_noviembre.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_21.addWidget(self.txtImporte_ventas_noviembre, 11, 1, 1, 1)

        self.txtUnid_ventas_diciembre = QLineEdit(self.frame_15)
        self.txtUnid_ventas_diciembre.setObjectName("txtUnid_ventas_diciembre")
        self.txtUnid_ventas_diciembre.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_ventas_diciembre.setStyleSheet("")
        self.txtUnid_ventas_diciembre.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_21.addWidget(self.txtUnid_ventas_diciembre, 12, 0, 1, 1)

        self.txtImporte_ventas_diciembre = QLineEdit(self.frame_15)
        self.txtImporte_ventas_diciembre.setObjectName("txtImporte_ventas_diciembre")
        self.txtImporte_ventas_diciembre.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_ventas_diciembre.setStyleSheet("")
        self.txtImporte_ventas_diciembre.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_21.addWidget(self.txtImporte_ventas_diciembre, 12, 1, 1, 1)

        self.gridLayout_19.addLayout(self.gridLayout_21, 1, 0, 2, 3)

        self.verticalSpacer_2 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.gridLayout_19.addItem(self.verticalSpacer_2, 3, 0, 1, 1)

        self.gridLayout_22.addWidget(self.frame_15, 0, 1, 1, 1)

        self.gridLayout_3.addWidget(self.cajaValores, 0, 1, 1, 1)

        self.Pestanas.addTab(self.tab_grafica, "")

        self.gridLayout_2.addWidget(self.Pestanas, 1, 1, 1, 5)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName("page_2")
        self.gridLayout_38 = QGridLayout(self.page_2)
        self.gridLayout_38.setObjectName("gridLayout_38")
        self.gridLayout_38.setContentsMargins(-1, -1, 20, -1)
        self.tablaBusqueda = QTableView(self.page_2)
        self.tablaBusqueda.setObjectName("tablaBusqueda")
        self.tablaBusqueda.setAlternatingRowColors(True)
        self.tablaBusqueda.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.tablaBusqueda.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.tablaBusqueda.horizontalHeader().setStretchLastSection(True)
        self.tablaBusqueda.verticalHeader().setVisible(False)

        self.gridLayout_38.addWidget(self.tablaBusqueda, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_2)

        self.gridLayout_10.addWidget(self.stackedWidget, 1, 0, 1, 5)

        self.label_70 = QLabel(FrmArticulos)
        self.label_70.setObjectName("label_70")
        self.label_70.setMaximumSize(QSize(16777215, 22))
        self.label_70.setStyleSheet(
            "background: #304163;\n"
            "color: rgb(255,255,255);\n"
            'font: 14pt "Sans Serif";'
        )
        self.label_70.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.label_70, 0, 0, 1, 5)

        QWidget.setTabOrder(self.txtDescripcionTipo, self.txtcodigo_fabricante)
        QWidget.setTabOrder(self.txtcodigo_fabricante, self.txtcoste)
        QWidget.setTabOrder(self.txtcoste, self.chkmostrar_web)
        QWidget.setTabOrder(self.chkmostrar_web, self.chkcontrolar_stock)
        QWidget.setTabOrder(self.chkcontrolar_stock, self.txtPrecioVenta)
        QWidget.setTabOrder(self.txtPrecioVenta, self.txtCoste_real)
        QWidget.setTabOrder(self.txtCoste_real, self.txtMargen)
        QWidget.setTabOrder(self.txtMargen, self.txtMargen_min)
        QWidget.setTabOrder(self.txtMargen_min, self.txtdto)
        QWidget.setTabOrder(self.txtdto, self.TablaTarifas)
        QWidget.setTabOrder(self.TablaTarifas, self.btnEditartarifa)
        QWidget.setTabOrder(self.btnEditartarifa, self.txtdescripcion)
        QWidget.setTabOrder(self.txtdescripcion, self.txtcomentario)
        QWidget.setTabOrder(self.txtcomentario, self.txtseccion)
        QWidget.setTabOrder(self.txtseccion, self.botBuscarSeccion)
        QWidget.setTabOrder(self.botBuscarSeccion, self.txtfamilia)
        QWidget.setTabOrder(self.txtfamilia, self.botBuscarFamilia)
        QWidget.setTabOrder(self.botBuscarFamilia, self.txtsubfamilia)
        QWidget.setTabOrder(self.txtsubfamilia, self.botBuscarSubfamilia)
        QWidget.setTabOrder(self.botBuscarSubfamilia, self.tablaProveedores)
        QWidget.setTabOrder(self.tablaProveedores, self.btnAnadirDistribuidores)
        QWidget.setTabOrder(
            self.btnAnadirDistribuidores, self.btnEditarDistribuidorFrecuente
        )
        QWidget.setTabOrder(
            self.btnEditarDistribuidorFrecuente, self.btnBorrarDistribuidores
        )
        QWidget.setTabOrder(self.btnBorrarDistribuidores, self.btnAsignarDistribuidor)
        QWidget.setTabOrder(self.btnAsignarDistribuidor, self.chkArticulo_promocionado)
        QWidget.setTabOrder(self.chkArticulo_promocionado, self.chkMostrar_en_cuadro)
        QWidget.setTabOrder(self.chkMostrar_en_cuadro, self.txtOferta_Fecha_ini)
        QWidget.setTabOrder(self.txtOferta_Fecha_ini, self.txtOferta_Fecha_fin)
        QWidget.setTabOrder(self.txtOferta_Fecha_fin, self.btnAnadirOferta)
        QWidget.setTabOrder(self.btnAnadirOferta, self.btnEditarOferta)
        QWidget.setTabOrder(self.btnEditarOferta, self.btnguardar_oferta)
        QWidget.setTabOrder(self.btnguardar_oferta, self.btnDeshacerOferta)
        QWidget.setTabOrder(self.btnDeshacerOferta, self.chkOferta_32)
        QWidget.setTabOrder(self.chkOferta_32, self.chkOferta_web)
        QWidget.setTabOrder(self.chkOferta_web, self.chkOferta_dto)
        QWidget.setTabOrder(self.chkOferta_dto, self.chkOfertaPvp)
        QWidget.setTabOrder(self.chkOfertaPvp, self.txtOfertaPorCada)
        QWidget.setTabOrder(self.txtOfertaPorCada, self.txtOfertaregaloUnidades)
        QWidget.setTabOrder(self.txtOfertaregaloUnidades, self.txtOfertaDtoOferta)
        QWidget.setTabOrder(self.txtOfertaDtoOferta, self.txtOfertaDtoWeb)
        QWidget.setTabOrder(self.txtOfertaDtoWeb, self.txtofertaPvpFijo)
        QWidget.setTabOrder(self.txtofertaPvpFijo, self.cboTarifaOferta)
        QWidget.setTabOrder(self.cboTarifaOferta, self.tabla_ofertas)
        QWidget.setTabOrder(self.tabla_ofertas, self.btnActivarOferta)
        QWidget.setTabOrder(self.btnActivarOferta, self.btnBorrarOferta)
        QWidget.setTabOrder(self.btnBorrarOferta, self.txtOferta_comentarios_promocion)
        QWidget.setTabOrder(
            self.txtOferta_comentarios_promocion, self.txtunidades_compradas
        )
        QWidget.setTabOrder(
            self.txtunidades_compradas, self.txtimporte_acumulado_compras
        )
        QWidget.setTabOrder(
            self.txtimporte_acumulado_compras, self.txtfechaUltimaCompra
        )
        QWidget.setTabOrder(self.txtfechaUltimaCompra, self.txtstock_minimo)
        QWidget.setTabOrder(self.txtstock_minimo, self.txtstock_fisico_almacen)
        QWidget.setTabOrder(
            self.txtstock_fisico_almacen, self.txtcantidad_pendiente_recibir
        )
        QWidget.setTabOrder(
            self.txtcantidad_pendiente_recibir, self.txtunidades_reservadas
        )
        QWidget.setTabOrder(self.txtunidades_reservadas, self.txtstock_real_2)
        QWidget.setTabOrder(self.txtstock_real_2, self.txtunidades_vendidas)
        QWidget.setTabOrder(self.txtunidades_vendidas, self.txtimporte_acumulado_ventas)
        QWidget.setTabOrder(self.txtimporte_acumulado_ventas, self.txtFechaUltimaVenta)
        QWidget.setTabOrder(self.txtFechaUltimaVenta, self.txtstock_maximo)
        QWidget.setTabOrder(self.txtstock_maximo, self.txtFechaPrevistaEntrega)
        QWidget.setTabOrder(self.txtFechaPrevistaEntrega, self.txtUnid_compras_enero)
        QWidget.setTabOrder(self.txtUnid_compras_enero, self.txtImporte_compras_enero)
        QWidget.setTabOrder(self.txtImporte_compras_enero, self.txtUnid_compras_febrero)
        QWidget.setTabOrder(
            self.txtUnid_compras_febrero, self.txtImporte_compras_febrero
        )
        QWidget.setTabOrder(self.txtImporte_compras_febrero, self.txtUnid_compras_marzo)
        QWidget.setTabOrder(self.txtUnid_compras_marzo, self.txtImporte_compras_marzo)
        QWidget.setTabOrder(self.txtImporte_compras_marzo, self.txtUnid_compras_abril)
        QWidget.setTabOrder(self.txtUnid_compras_abril, self.txtImporte_compras_abril)
        QWidget.setTabOrder(self.txtImporte_compras_abril, self.txtUnid_compras_mayo)
        QWidget.setTabOrder(self.txtUnid_compras_mayo, self.txtImporte_compras_mayo)
        QWidget.setTabOrder(self.txtImporte_compras_mayo, self.txtUnid_compras_junio)
        QWidget.setTabOrder(self.txtUnid_compras_junio, self.txtImporte_compras_junio)
        QWidget.setTabOrder(self.txtImporte_compras_junio, self.txtUnid_compras_julio)
        QWidget.setTabOrder(self.txtUnid_compras_julio, self.txtImporte_compras_julio)
        QWidget.setTabOrder(self.txtImporte_compras_julio, self.txtUnid_compras_agosto)
        QWidget.setTabOrder(self.txtUnid_compras_agosto, self.txtImporte_compras_agosto)
        QWidget.setTabOrder(
            self.txtImporte_compras_agosto, self.txtUnid_compras_septiembre
        )
        QWidget.setTabOrder(
            self.txtUnid_compras_septiembre, self.txtImporte_compras_septiembre
        )
        QWidget.setTabOrder(
            self.txtImporte_compras_septiembre, self.txtUnid_compras_octubre
        )
        QWidget.setTabOrder(
            self.txtUnid_compras_octubre, self.txtImporte_compras_octubre
        )
        QWidget.setTabOrder(
            self.txtImporte_compras_octubre, self.txtUnid_compras_noviembre
        )
        QWidget.setTabOrder(
            self.txtUnid_compras_noviembre, self.txtImporte_compras_noviembre
        )
        QWidget.setTabOrder(
            self.txtImporte_compras_noviembre, self.txtUnid_compras_diciembre
        )
        QWidget.setTabOrder(
            self.txtUnid_compras_diciembre, self.txtImporte_compras_diciembre
        )
        QWidget.setTabOrder(
            self.txtImporte_compras_diciembre, self.txtUnid_ventas_enero
        )
        QWidget.setTabOrder(self.txtUnid_ventas_enero, self.txtImporte_ventas_enero)
        QWidget.setTabOrder(self.txtImporte_ventas_enero, self.txtUnid_ventas_febrero)
        QWidget.setTabOrder(self.txtUnid_ventas_febrero, self.txtImporte_ventas_febrero)
        QWidget.setTabOrder(self.txtImporte_ventas_febrero, self.txtUnid_ventas_marzo)
        QWidget.setTabOrder(self.txtUnid_ventas_marzo, self.txtImporte_ventas_marzo)
        QWidget.setTabOrder(self.txtImporte_ventas_marzo, self.txtUnid_ventas_abril)
        QWidget.setTabOrder(self.txtUnid_ventas_abril, self.txtImporte_ventas_abril)
        QWidget.setTabOrder(self.txtImporte_ventas_abril, self.txtUnid_ventas_mayo)
        QWidget.setTabOrder(self.txtUnid_ventas_mayo, self.txtImporte_ventas_mayo)
        QWidget.setTabOrder(self.txtImporte_ventas_mayo, self.txtUnid_ventas_junio)
        QWidget.setTabOrder(self.txtUnid_ventas_junio, self.txtImporte_ventas_junio)
        QWidget.setTabOrder(self.txtImporte_ventas_junio, self.txtUnid_ventas_julio)
        QWidget.setTabOrder(self.txtUnid_ventas_julio, self.txtImporte_ventas_julio)
        QWidget.setTabOrder(self.txtImporte_ventas_julio, self.txtUnid_ventas_agosto)
        QWidget.setTabOrder(self.txtUnid_ventas_agosto, self.txtImporte_ventas_agosto)
        QWidget.setTabOrder(
            self.txtImporte_ventas_agosto, self.txtUnid_ventas_septiembre
        )
        QWidget.setTabOrder(
            self.txtUnid_ventas_septiembre, self.txtImporte_ventas_septiembre
        )
        QWidget.setTabOrder(
            self.txtImporte_ventas_septiembre, self.txtUnid_ventas_octubre
        )
        QWidget.setTabOrder(self.txtUnid_ventas_octubre, self.txtImporte_ventas_octubre)
        QWidget.setTabOrder(
            self.txtImporte_ventas_octubre, self.txtUnid_ventas_noviembre
        )
        QWidget.setTabOrder(
            self.txtUnid_ventas_noviembre, self.txtImporte_ventas_noviembre
        )
        QWidget.setTabOrder(
            self.txtImporte_ventas_noviembre, self.txtUnid_ventas_diciembre
        )
        QWidget.setTabOrder(
            self.txtUnid_ventas_diciembre, self.txtImporte_ventas_diciembre
        )
        QWidget.setTabOrder(self.txtImporte_ventas_diciembre, self.cboTipoGrafica)
        QWidget.setTabOrder(self.cboTipoGrafica, self.radGrafica_unidades)
        QWidget.setTabOrder(self.radGrafica_unidades, self.radGrafica_importes)
        QWidget.setTabOrder(self.radGrafica_importes, self.chkValorGrafica)
        QWidget.setTabOrder(self.chkValorGrafica, self.botAnadir)
        QWidget.setTabOrder(self.botAnadir, self.botSiguiente)
        QWidget.setTabOrder(self.botSiguiente, self.botAnterior)
        QWidget.setTabOrder(self.botAnterior, self.btnBuscar)
        QWidget.setTabOrder(self.btnBuscar, self.botEditar)
        QWidget.setTabOrder(self.botEditar, self.botGuardar)
        QWidget.setTabOrder(self.botGuardar, self.botDeshacer)
        QWidget.setTabOrder(self.botDeshacer, self.btnKit)
        QWidget.setTabOrder(self.btnKit, self.botBorrar)
        QWidget.setTabOrder(self.botBorrar, self.btn_cerrar)
        QWidget.setTabOrder(self.btn_cerrar, self.Pestanas)
        QWidget.setTabOrder(self.Pestanas, self.tablaBusqueda)
        QWidget.setTabOrder(self.tablaBusqueda, self.txtOferta_Descripcion_promocion)

        self.retranslateUi(FrmArticulos)
        try:
            self.btn_cerrar.clicked.connect(FrmArticulos.accept)
        except Exception:
            try:
                self.btn_cerrar.clicked.connect(FrmArticulos.close)
            except Exception:
                pass

        self.stackedWidget.setCurrentIndex(0)
        self.Pestanas.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(FrmArticulos)

    # setupUi

    def retranslateUi(self, FrmArticulos):
        FrmArticulos.setWindowTitle(
            QCoreApplication.translate(
                "FrmArticulos", "Gesti\u00f3n de Art\u00edculos", None
            )
        )
        self.lblkit.setText(QCoreApplication.translate("FrmArticulos", "KIT", None))
        self.lbl_en_promocion.setText(
            QCoreApplication.translate("FrmArticulos", "En Promoci\u00f3n", None)
        )
        self.lblCodigo.setText(
            QCoreApplication.translate("FrmArticulos", "c\u00f3digo", None)
        )
        self.lblDescripcion.setText(
            QCoreApplication.translate("FrmArticulos", "Descripcion", None)
        )
        self.botAnadir.setText(
            QCoreApplication.translate("FrmArticulos", "Nuevo", None)
        )
        self.botSiguiente.setText(
            QCoreApplication.translate("FrmArticulos", "Siguiente", None)
        )
        self.botAnterior.setText(
            QCoreApplication.translate("FrmArticulos", "Anterior", None)
        )
        self.btnBuscar.setText(
            QCoreApplication.translate("FrmArticulos", "Buscar", None)
        )
        self.botEditar.setText(
            QCoreApplication.translate("FrmArticulos", "Editar", None)
        )
        self.botGuardar.setText(
            QCoreApplication.translate("FrmArticulos", "Guardar", None)
        )
        self.botDeshacer.setText(
            QCoreApplication.translate("FrmArticulos", "Deshacer", None)
        )
        self.btnKit.setText(
            QCoreApplication.translate(
                "FrmArticulos", " Ver/\n" "Editar\n" " Kit", None
            )
        )
        self.botBorrar.setText(
            QCoreApplication.translate("FrmArticulos", "Borrar", None)
        )
        self.btn_cerrar.setText(
            QCoreApplication.translate("FrmArticulos", "Cerrar", None)
        )
        self.txtCodigoProveedor.setPlaceholderText(
            QCoreApplication.translate("FrmArticulos", "Ctrl+F-Buscar", None)
        )
        self.label_16.setText(
            QCoreApplication.translate("FrmArticulos", "Tipo :", None)
        )
        self.lblProveedorHabitual.setText(
            QCoreApplication.translate("FrmArticulos", "Proveedor Habitual:", None)
        )
        self.btnEditartarifa.setText(
            QCoreApplication.translate("FrmArticulos", "Editar Tarifa", None)
        )
        self.label_15.setText(
            QCoreApplication.translate("FrmArticulos", "Precio venta:", None)
        )
        self.label_14.setText(
            QCoreApplication.translate("FrmArticulos", "Coste:", None)
        )
        self.txtcoste.setText(QCoreApplication.translate("FrmArticulos", "0,00", None))
        self.lblCodigoEAN.setText(
            QCoreApplication.translate("FrmArticulos", "C\u00f3digo EAN:", None)
        )
        self.txtcodigo_fabricante.setText("")
        self.label_18.setText(
            QCoreApplication.translate("FrmArticulos", "Comentarios:", None)
        )
        self.txtCodigoTipo.setPlaceholderText(
            QCoreApplication.translate("FrmArticulos", "Ctrl+F-Buscar", None)
        )
        self.label_2.setText(
            QCoreApplication.translate("FrmArticulos", "C\u00f3digo: ", None)
        )
        # if QT_CONFIG(tooltip)
        self.chkmostrar_web.setToolTip(
            QCoreApplication.translate(
                "FrmArticulos",
                "Seleccionar si se desea que el art\u00edculo aparezca en la tienda virtual en su web",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.chkmostrar_web.setText(
            QCoreApplication.translate("FrmArticulos", "Mostrar en web", None)
        )
        self.label_19.setText(
            QCoreApplication.translate("FrmArticulos", "Tipo IVA:", None)
        )
        self.txtdto.setText(QCoreApplication.translate("FrmArticulos", "0", None))
        self.label_5.setText(
            QCoreApplication.translate("FrmArticulos", "Coste Real:", None)
        )
        self.txtCoste_real.setText(
            QCoreApplication.translate("FrmArticulos", "0,00", None)
        )
        self.label_13.setText(
            QCoreApplication.translate("FrmArticulos", "Margen min:", None)
        )
        self.label_12.setText(
            QCoreApplication.translate("FrmArticulos", "Margen:", None)
        )
        self.label_20.setText(
            QCoreApplication.translate("FrmArticulos", "%Descuento Promocional:", None)
        )
        self.txtPrecioVenta.setText(
            QCoreApplication.translate("FrmArticulos", "0.00", None)
        )
        self.label_7.setText(
            QCoreApplication.translate("FrmArticulos", "Descripci\u00f3n", None)
        )
        self.label_6.setText(
            QCoreApplication.translate("FrmArticulos", "Art\u00edculo:", None)
        )
        self.chkcontrolar_stock.setText(
            QCoreApplication.translate("FrmArticulos", "Controlar stock", None)
        )
        self.lblCodigoenProveedor.setText(
            QCoreApplication.translate(
                "FrmArticulos", "C\u00f3digo en Proveedor:", None
            )
        )
        self.Pestanas.setTabText(
            self.Pestanas.indexOf(self.tab_articulo),
            QCoreApplication.translate("FrmArticulos", "Servicio/art\u00edculo", None),
        )

        __sortingEnabled = self.listColors.isSortingEnabled()
        self.listColors.setSortingEnabled(False)
        # if QT_CONFIG(tooltip)
        ___qlistwidgetitem = self.listColors.item(0)
        # endif
        # if QT_CONFIG(tooltip)
        ___qlistwidgetitem.setToolTip(
            QCoreApplication.translate("FrmArticulos", "Blanco", None)
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(tooltip)
        ___qlistwidgetitem1 = self.listColors.item(1)
        # endif
        # if QT_CONFIG(tooltip)
        ___qlistwidgetitem1.setToolTip(
            QCoreApplication.translate("FrmArticulos", "Negro", None)
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(tooltip)
        ___qlistwidgetitem2 = self.listColors.item(2)
        # endif
        # if QT_CONFIG(tooltip)
        ___qlistwidgetitem2.setToolTip(
            QCoreApplication.translate("FrmArticulos", "Rojo", None)
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(tooltip)
        ___qlistwidgetitem3 = self.listColors.item(3)
        # endif
        # if QT_CONFIG(tooltip)
        ___qlistwidgetitem3.setToolTip(
            QCoreApplication.translate("FrmArticulos", "Azul", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.listColors.setSortingEnabled(__sortingEnabled)

        self.Pestanas.setTabText(
            self.Pestanas.indexOf(self.TallasColores),
            QCoreApplication.translate("FrmArticulos", "Tallas y colores", None),
        )
        self.label_9.setText(
            QCoreApplication.translate("FrmArticulos", "Secci\u00f3n:", None)
        )
        # if QT_CONFIG(tooltip)
        self.botBuscarSeccion.setToolTip(
            QCoreApplication.translate(
                "FrmArticulos",
                "<html><head/><body><p>Asociar Secci\u00f3n.</p></body></html>",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.botBuscarSeccion.setText("")
        self.label_10.setText(
            QCoreApplication.translate("FrmArticulos", "Familia:", None)
        )
        self.botBuscarFamilia.setText("")
        self.label_11.setText(
            QCoreApplication.translate("FrmArticulos", "Subfamilia:", None)
        )
        self.botBuscarSubfamilia.setText("")
        self.Pestanas.setTabText(
            self.Pestanas.indexOf(self.tab),
            QCoreApplication.translate("FrmArticulos", "grupos", None),
        )
        self.label_23.setText(
            QCoreApplication.translate(
                "FrmArticulos", "Distribuidores frecuentes", None
            )
        )
        # if QT_CONFIG(tooltip)
        self.btnAnadirDistribuidores.setToolTip(
            QCoreApplication.translate(
                "FrmArticulos",
                '<html><head/><body><p><span style=" color:#ff0000;">A\u00f1adir proveedor frecuente a ficha de art\u00edculo</span></p><p><br/></p></body></html>',
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.btnAnadirDistribuidores.setText("")
        # if QT_CONFIG(tooltip)
        self.btnEditarDistribuidorFrecuente.setToolTip(
            QCoreApplication.translate(
                "FrmArticulos",
                '<html><head/><body><p><span style=" color:#ff0000;">Editar datos proveedor frecuente</span></p></body></html>',
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.btnEditarDistribuidorFrecuente.setText("")
        # if QT_CONFIG(tooltip)
        self.btnBorrarDistribuidores.setToolTip(
            QCoreApplication.translate(
                "FrmArticulos",
                '<html><head/><body><p><span style=" color:#ff0000;">Quitar proveedor frecuente de ficha de art\u00edculo</span></p></body></html>',
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.btnBorrarDistribuidores.setText("")
        # if QT_CONFIG(tooltip)
        self.btnAsignarDistribuidor.setToolTip(
            QCoreApplication.translate(
                "FrmArticulos",
                '<html><head/><body><p><span style=" color:#ff0000;">Asignar como proveedor principal.</span></p></body></html>',
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.btnAsignarDistribuidor.setText("")
        self.Pestanas.setTabText(
            self.Pestanas.indexOf(self.tab_distribuidores),
            QCoreApplication.translate("FrmArticulos", "Distrubuidores", None),
        )
        self.chkArticulo_promocionado.setText(
            QCoreApplication.translate(
                "FrmArticulos", "Art\u00edculo promocionado", None
            )
        )
        self.label_63.setText(
            QCoreApplication.translate("FrmArticulos", "OFERTA PRECIO FIJO", None)
        )
        self.lbl_oferta_importe.setText(
            QCoreApplication.translate("FrmArticulos", "Importe:", None)
        )
        self.txtofertaPvpFijo.setText(
            QCoreApplication.translate("FrmArticulos", "0,00", None)
        )
        self.lbl_por_cada.setText(
            QCoreApplication.translate("FrmArticulos", "Por cada: ", None)
        )
        self.txtOfertaPorCada.setText(
            QCoreApplication.translate("FrmArticulos", "0", None)
        )
        self.lbl_unidades.setText(
            QCoreApplication.translate("FrmArticulos", "Unidades", None)
        )
        self.lbl_regalo_de.setText(
            QCoreApplication.translate("FrmArticulos", "Regalo de:", None)
        )
        self.txtOfertaregaloUnidades.setText(
            QCoreApplication.translate("FrmArticulos", "0", None)
        )
        self.lbl_unidades_2.setText(
            QCoreApplication.translate("FrmArticulos", "Unidades", None)
        )
        self.label_57.setText(
            QCoreApplication.translate("FrmArticulos", "OFERTA TIPO 3*2", None)
        )
        self.txtOferta_Fecha_fin.setDisplayFormat(
            QCoreApplication.translate("FrmArticulos", "dd/MM/yyyy", None)
        )
        self.txtOferta_Fecha_ini.setDisplayFormat(
            QCoreApplication.translate("FrmArticulos", "dd/MM/yyyy", None)
        )
        self.label_61.setText(
            QCoreApplication.translate("FrmArticulos", "OFERTA DTO", None)
        )
        self.lbl_oferta_dto.setText(
            QCoreApplication.translate("FrmArticulos", "% Descuento:", None)
        )
        self.txtOfertaDtoOferta.setText(
            QCoreApplication.translate("FrmArticulos", "0", None)
        )
        self.lbl_dto_web.setText(
            QCoreApplication.translate("FrmArticulos", "Dto Especial web:", None)
        )
        self.lbl_dto_web2.setText(
            QCoreApplication.translate("FrmArticulos", "% Descuento:", None)
        )
        self.txtOfertaDtoWeb.setText(
            QCoreApplication.translate("FrmArticulos", "0", None)
        )
        self.label_68.setText(
            QCoreApplication.translate("FrmArticulos", "Hasta:", None)
        )
        self.label_21.setText(
            QCoreApplication.translate("FrmArticulos", "Desde:", None)
        )
        self.chkMostrar_en_cuadro.setText(
            QCoreApplication.translate("FrmArticulos", "Mostrar en cuadro", None)
        )
        self.lblDescripcion_oferta.setText(
            QCoreApplication.translate("FrmArticulos", "Descripci\u00f3n:", None)
        )
        self.btnAnadirOferta.setText(
            QCoreApplication.translate("FrmArticulos", "A\u00f1adir", None)
        )
        self.btnEditarOferta.setText(
            QCoreApplication.translate("FrmArticulos", "Editar", None)
        )
        self.btnguardar_oferta.setText(
            QCoreApplication.translate("FrmArticulos", "Guardar", None)
        )
        self.btnDeshacerOferta.setText(
            QCoreApplication.translate("FrmArticulos", "Deshacer", None)
        )
        self.chkOferta_32.setText(
            QCoreApplication.translate("FrmArticulos", " Oferta 3*2", None)
        )
        self.chkOferta_web.setText(
            QCoreApplication.translate("FrmArticulos", "Descuento especial web", None)
        )
        self.chkOferta_dto.setText(
            QCoreApplication.translate("FrmArticulos", "Oferta % dto", None)
        )
        self.chkOfertaPvp.setText(
            QCoreApplication.translate("FrmArticulos", "Oferta precio final", None)
        )
        self.label_65.setText(
            QCoreApplication.translate("FrmArticulos", "Comentarios", None)
        )
        self.label_72.setText(
            QCoreApplication.translate("FrmArticulos", "OFERTAS ART\u00cdCULO", None)
        )
        self.btnActivarOferta.setText(
            QCoreApplication.translate(
                "FrmArticulos", "Activar/Desactivar Oferta", None
            )
        )
        self.btnBorrarOferta.setText(
            QCoreApplication.translate("FrmArticulos", "Borrar", None)
        )
        self.label.setText(QCoreApplication.translate("FrmArticulos", "Tarifa:", None))
        self.Pestanas.setTabText(
            self.Pestanas.indexOf(self.tab_promociones),
            QCoreApplication.translate("FrmArticulos", "Promociones", None),
        )
        # if QT_CONFIG(tooltip)
        self.lblImagenArticulo_2.setToolTip(
            QCoreApplication.translate(
                "FrmArticulos",
                "La imagen introducida debe tener los mismos pixels horizontales que verticales",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.lblImagenArticulo_2.setText("")
        # if QT_CONFIG(tooltip)
        self.lblImagenArticulo_3.setToolTip(
            QCoreApplication.translate(
                "FrmArticulos",
                "La imagen introducida debe tener los mismos pixels horizontales que verticales",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.lblImagenArticulo_3.setText("")
        # if QT_CONFIG(tooltip)
        self.lblImagenArticulo_1.setToolTip(
            QCoreApplication.translate(
                "FrmArticulos",
                "La imagen introducida debe tener los mismos pixels horizontales que verticales",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.lblImagenArticulo_1.setText("")
        # if QT_CONFIG(tooltip)
        self.lblImagenArticulo_4.setToolTip(
            QCoreApplication.translate(
                "FrmArticulos",
                "La imagen introducida debe tener los mismos pixels horizontales que verticales",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.lblImagenArticulo_4.setText("")
        self.Pestanas.setTabText(
            self.Pestanas.indexOf(self.tab_imagenes),
            QCoreApplication.translate("FrmArticulos", "Imagenes", None),
        )
        self.label_28.setText(
            QCoreApplication.translate("FrmArticulos", "Unidades Compradas:", None)
        )
        self.label_29.setText(
            QCoreApplication.translate("FrmArticulos", "Unidades Vendidas:", None)
        )
        self.lblFechaVenta.setText(
            QCoreApplication.translate("FrmArticulos", "Fecha \u00falt. Venta:", None)
        )
        self.txtunidades_vendidas.setText(
            QCoreApplication.translate("FrmArticulos", "0", None)
        )
        self.txtimporte_acumulado_compras.setText(
            QCoreApplication.translate("FrmArticulos", "0,00", None)
        )
        self.txtunidades_compradas.setText(
            QCoreApplication.translate("FrmArticulos", "0", None)
        )
        self.label_43.setText(
            QCoreApplication.translate("FrmArticulos", "Acumulado Ventas:", None)
        )
        self.txtimporte_acumulado_ventas.setText(
            QCoreApplication.translate("FrmArticulos", "0,00", None)
        )
        self.label_42.setText(
            QCoreApplication.translate("FrmArticulos", "Acumulado Compras", None)
        )
        self.lblFechaCompra.setText(
            QCoreApplication.translate("FrmArticulos", "Fecha \u00falt. Compra:", None)
        )
        self.label_30.setText(
            QCoreApplication.translate("FrmArticulos", "Stock M\u00ednimo:", None)
        )
        self.label_45.setText(
            QCoreApplication.translate("FrmArticulos", "Cantidad reservada:", None)
        )
        self.label_31.setText(
            QCoreApplication.translate("FrmArticulos", "Stock M\u00e1ximo:", None)
        )
        self.label_32.setText(
            QCoreApplication.translate(
                "FrmArticulos", "Stock Real:\n" "(fisico+ pendiente recibir)", None
            )
        )
        self.label_44.setText(
            QCoreApplication.translate("FrmArticulos", "Pendientes recibir:", None)
        )
        self.txtstock_real_2.setText(
            QCoreApplication.translate("FrmArticulos", "0", None)
        )
        self.txtstock_minimo.setText(
            QCoreApplication.translate("FrmArticulos", "0", None)
        )
        self.txtunidades_reservadas.setText(
            QCoreApplication.translate("FrmArticulos", "0", None)
        )
        self.txtstock_maximo.setText(
            QCoreApplication.translate("FrmArticulos", "0", None)
        )
        self.lblFechaPrevistaEntrega.setText(
            QCoreApplication.translate("FrmArticulos", "Fecha Prev. Recepc.:", None)
        )
        self.txtcantidad_pendiente_recibir.setText(
            QCoreApplication.translate("FrmArticulos", "0", None)
        )
        self.txtstock_fisico_almacen.setText(
            QCoreApplication.translate("FrmArticulos", "0", None)
        )
        self.label_22.setText(
            QCoreApplication.translate("FrmArticulos", "Stock Fisico:", None)
        )
        self.Pestanas.setTabText(
            self.Pestanas.indexOf(self.tab_estadistica),
            QCoreApplication.translate("FrmArticulos", "Estadistica", None),
        )
        self.cboTipoGrafica.setItemText(
            0, QCoreApplication.translate("FrmArticulos", "Grafica de Barras", None)
        )
        self.cboTipoGrafica.setItemText(
            1,
            QCoreApplication.translate("FrmArticulos", "Grafica de L\u00edneas", None),
        )

        self.radGrafica_unidades.setText(
            QCoreApplication.translate("FrmArticulos", "Grafica de unidades", None)
        )
        self.radGrafica_importes.setText(
            QCoreApplication.translate("FrmArticulos", "Grafica de Importes", None)
        )
        self.chkValorGrafica.setText(
            QCoreApplication.translate("FrmArticulos", "Mostrar valores", None)
        )
        self.label_25.setText(
            QCoreApplication.translate("FrmArticulos", "COMPRAS", None)
        )
        self.txtImporte_compras_enero.setText(
            QCoreApplication.translate("FrmArticulos", "0,00", None)
        )
        self.txtImporte_compras_julio.setText(
            QCoreApplication.translate("FrmArticulos", "0,00", None)
        )
        self.txtImporte_compras_marzo.setText(
            QCoreApplication.translate("FrmArticulos", "0,00", None)
        )
        self.txtUnid_compras_febrero.setText(
            QCoreApplication.translate("FrmArticulos", "0", None)
        )
        self.txtUnid_compras_marzo.setText(
            QCoreApplication.translate("FrmArticulos", "0", None)
        )
        self.txtImporte_compras_septiembre.setText(
            QCoreApplication.translate("FrmArticulos", "0,00", None)
        )
        self.label_52.setText(
            QCoreApplication.translate("FrmArticulos", "Unidades", None)
        )
        self.txtImporte_compras_diciembre.setText(
            QCoreApplication.translate("FrmArticulos", "0,00", None)
        )
        self.txtUnid_compras_agosto.setText(
            QCoreApplication.translate("FrmArticulos", "0", None)
        )
        self.txtUnid_compras_diciembre.setText(
            QCoreApplication.translate("FrmArticulos", "0", None)
        )
        self.txtUnid_compras_junio.setText(
            QCoreApplication.translate("FrmArticulos", "0", None)
        )
        self.txtUnid_compras_mayo.setText(
            QCoreApplication.translate("FrmArticulos", "0", None)
        )
        self.txtUnid_compras_enero.setText(
            QCoreApplication.translate("FrmArticulos", "0", None)
        )
        self.txtImporte_compras_octubre.setText(
            QCoreApplication.translate("FrmArticulos", "0,00", None)
        )
        self.txtImporte_compras_noviembre.setText(
            QCoreApplication.translate("FrmArticulos", "0,00", None)
        )
        self.txtUnid_compras_noviembre.setText(
            QCoreApplication.translate("FrmArticulos", "0", None)
        )
        self.txtImporte_compras_agosto.setText(
            QCoreApplication.translate("FrmArticulos", "0,00", None)
        )
        self.txtImporte_compras_mayo.setText(
            QCoreApplication.translate("FrmArticulos", "0,00", None)
        )
        self.txtUnid_compras_septiembre.setText(
            QCoreApplication.translate("FrmArticulos", "0", None)
        )
        self.txtImporte_compras_febrero.setText(
            QCoreApplication.translate("FrmArticulos", "0,00", None)
        )
        self.txtUnid_compras_abril.setText(
            QCoreApplication.translate("FrmArticulos", "0", None)
        )
        self.txtImporte_compras_abril.setText(
            QCoreApplication.translate("FrmArticulos", "0,00", None)
        )
        self.label_53.setText(
            QCoreApplication.translate("FrmArticulos", "Importe", None)
        )
        self.txtUnid_compras_julio.setText(
            QCoreApplication.translate("FrmArticulos", "0", None)
        )
        self.txtImporte_compras_junio.setText(
            QCoreApplication.translate("FrmArticulos", "0,00", None)
        )
        self.txtUnid_compras_octubre.setText(
            QCoreApplication.translate("FrmArticulos", "0", None)
        )
        self.label_27.setText(
            QCoreApplication.translate("FrmArticulos", "Enero:", None)
        )
        self.label_35.setText(
            QCoreApplication.translate("FrmArticulos", "Febrero:", None)
        )
        self.label_36.setText(
            QCoreApplication.translate("FrmArticulos", "Marzo:", None)
        )
        self.label_37.setText(
            QCoreApplication.translate("FrmArticulos", "Abril:", None)
        )
        self.label_39.setText(QCoreApplication.translate("FrmArticulos", "Mayo:", None))
        self.label_40.setText(
            QCoreApplication.translate("FrmArticulos", "Junio:", None)
        )
        self.label_41.setText(
            QCoreApplication.translate("FrmArticulos", "Julio:", None)
        )
        self.label_46.setText(
            QCoreApplication.translate("FrmArticulos", "Agosto:", None)
        )
        self.label_47.setText(
            QCoreApplication.translate("FrmArticulos", "Septiembre:", None)
        )
        self.label_48.setText(
            QCoreApplication.translate("FrmArticulos", "Octubre:", None)
        )
        self.label_49.setText(
            QCoreApplication.translate("FrmArticulos", "Noviembre:", None)
        )
        self.label_50.setText(
            QCoreApplication.translate("FrmArticulos", "Diciembre:", None)
        )
        self.label_26.setText(
            QCoreApplication.translate("FrmArticulos", "VENTAS", None)
        )
        self.label_54.setText(
            QCoreApplication.translate("FrmArticulos", "Unidades", None)
        )
        self.label_55.setText(
            QCoreApplication.translate("FrmArticulos", "Importe", None)
        )
        self.txtUnid_ventas_enero.setText(
            QCoreApplication.translate("FrmArticulos", "0", None)
        )
        self.txtImporte_ventas_enero.setText(
            QCoreApplication.translate("FrmArticulos", "0,00", None)
        )
        self.txtUnid_ventas_febrero.setText(
            QCoreApplication.translate("FrmArticulos", "0", None)
        )
        self.txtImporte_ventas_febrero.setText(
            QCoreApplication.translate("FrmArticulos", "0,00", None)
        )
        self.txtUnid_ventas_marzo.setText(
            QCoreApplication.translate("FrmArticulos", "0", None)
        )
        self.txtImporte_ventas_marzo.setText(
            QCoreApplication.translate("FrmArticulos", "0,00", None)
        )
        self.txtUnid_ventas_abril.setText(
            QCoreApplication.translate("FrmArticulos", "0", None)
        )
        self.txtImporte_ventas_abril.setText(
            QCoreApplication.translate("FrmArticulos", "0,00", None)
        )
        self.txtUnid_ventas_mayo.setText(
            QCoreApplication.translate("FrmArticulos", "0", None)
        )
        self.txtImporte_ventas_mayo.setText(
            QCoreApplication.translate("FrmArticulos", "0,00", None)
        )
        self.txtUnid_ventas_junio.setText(
            QCoreApplication.translate("FrmArticulos", "0", None)
        )
        self.txtImporte_ventas_junio.setText(
            QCoreApplication.translate("FrmArticulos", "0,00", None)
        )
        self.txtUnid_ventas_julio.setText(
            QCoreApplication.translate("FrmArticulos", "0", None)
        )
        self.txtImporte_ventas_julio.setText(
            QCoreApplication.translate("FrmArticulos", "0,00", None)
        )
        self.txtUnid_ventas_agosto.setText(
            QCoreApplication.translate("FrmArticulos", "0", None)
        )
        self.txtImporte_ventas_agosto.setText(
            QCoreApplication.translate("FrmArticulos", "0,00", None)
        )
        self.txtUnid_ventas_septiembre.setText(
            QCoreApplication.translate("FrmArticulos", "0", None)
        )
        self.txtImporte_ventas_septiembre.setText(
            QCoreApplication.translate("FrmArticulos", "0,00", None)
        )
        self.txtUnid_ventas_octubre.setText(
            QCoreApplication.translate("FrmArticulos", "0", None)
        )
        self.txtImporte_ventas_octubre.setText(
            QCoreApplication.translate("FrmArticulos", "0,00", None)
        )
        self.txtUnid_ventas_noviembre.setText(
            QCoreApplication.translate("FrmArticulos", "0", None)
        )
        self.txtImporte_ventas_noviembre.setText(
            QCoreApplication.translate("FrmArticulos", "0,00", None)
        )
        self.txtUnid_ventas_diciembre.setText(
            QCoreApplication.translate("FrmArticulos", "0", None)
        )
        self.txtImporte_ventas_diciembre.setText(
            QCoreApplication.translate("FrmArticulos", "0,00", None)
        )
        self.Pestanas.setTabText(
            self.Pestanas.indexOf(self.tab_grafica),
            QCoreApplication.translate(
                "FrmArticulos", "Estad\u00edstica/Gr\u00e1fica", None
            ),
        )
        self.label_70.setText(
            QCoreApplication.translate(
                "FrmArticulos", "Gesti\u00f3n de Servicios/Articulos", None
            )
        )

    # retranslateUi
