# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frmarticulos.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QComboBox,
    QDateEdit, QDialog, QDoubleSpinBox, QFrame,
    QGridLayout, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QStackedWidget, QTabWidget, QTableView,
    QTextEdit, QVBoxLayout, QWidget)

from modules.common.chartviewwidget import ChartViewWidget
from modules.common.openchart import OpenChart
from modules import designer_rc

class Ui_FrmArticulos(object):
    def setupUi(self, FrmArticulos):
        if not FrmArticulos.objectName():
            FrmArticulos.setObjectName(u"FrmArticulos")
        FrmArticulos.resize(1147, 630)
        FrmArticulos.setMaximumSize(QSize(16777215, 16777215))
        icon = QIcon()
        icon.addFile(u":/Icons/PNG/Maya.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        FrmArticulos.setWindowIcon(icon)
        self.gridLayout_10 = QGridLayout(FrmArticulos)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.stackedWidget = QStackedWidget(FrmArticulos)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.gridLayout_2 = QGridLayout(self.page)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(-1, -1, 20, -1)
        self.frame_16 = QFrame(self.page)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setMinimumSize(QSize(132, 0))
        self.frame_16.setMaximumSize(QSize(140, 16777215))
        self.frame_16.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_16.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_16)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.botAnadir = QPushButton(self.frame_16)
        self.botAnadir.setObjectName(u"botAnadir")
        self.botAnadir.setMinimumSize(QSize(115, 40))
        self.botAnadir.setMaximumSize(QSize(118, 16777215))
        icon1 = QIcon()
        icon1.addFile(u":/PNG/resources/icons/png/Add.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.botAnadir.setIcon(icon1)
        self.botAnadir.setIconSize(QSize(24, 24))

        self.verticalLayout.addWidget(self.botAnadir)

        self.botSiguiente = QPushButton(self.frame_16)
        self.botSiguiente.setObjectName(u"botSiguiente")
        self.botSiguiente.setMinimumSize(QSize(115, 40))
        self.botSiguiente.setMaximumSize(QSize(118, 16777215))
        icon2 = QIcon()
        icon2.addFile(u":/PNG/resources/icons/png/Next.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.botSiguiente.setIcon(icon2)
        self.botSiguiente.setIconSize(QSize(24, 24))

        self.verticalLayout.addWidget(self.botSiguiente)

        self.botAnterior = QPushButton(self.frame_16)
        self.botAnterior.setObjectName(u"botAnterior")
        self.botAnterior.setMinimumSize(QSize(115, 40))
        self.botAnterior.setMaximumSize(QSize(118, 16777215))
        icon3 = QIcon()
        icon3.addFile(u":/PNG/resources/icons/png/Previous.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.botAnterior.setIcon(icon3)
        self.botAnterior.setIconSize(QSize(24, 24))

        self.verticalLayout.addWidget(self.botAnterior)

        self.btnBuscar = QPushButton(self.frame_16)
        self.btnBuscar.setObjectName(u"btnBuscar")
        self.btnBuscar.setMinimumSize(QSize(0, 40))
        icon4 = QIcon()
        icon4.addFile(u":/PNG/resources/icons/png/search.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnBuscar.setIcon(icon4)
        self.btnBuscar.setIconSize(QSize(24, 24))

        self.verticalLayout.addWidget(self.btnBuscar)

        self.botEditar = QPushButton(self.frame_16)
        self.botEditar.setObjectName(u"botEditar")
        self.botEditar.setMinimumSize(QSize(115, 40))
        self.botEditar.setMaximumSize(QSize(118, 16777215))
        icon5 = QIcon()
        icon5.addFile(u":/PNG/resources/icons/png/Edit.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.botEditar.setIcon(icon5)
        self.botEditar.setIconSize(QSize(24, 24))

        self.verticalLayout.addWidget(self.botEditar)

        self.botGuardar = QPushButton(self.frame_16)
        self.botGuardar.setObjectName(u"botGuardar")
        self.botGuardar.setEnabled(False)
        self.botGuardar.setMinimumSize(QSize(115, 40))
        self.botGuardar.setMaximumSize(QSize(118, 16777215))
        icon6 = QIcon()
        icon6.addFile(u":/PNG/resources/icons/png/Save.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.botGuardar.setIcon(icon6)
        self.botGuardar.setIconSize(QSize(24, 24))

        self.verticalLayout.addWidget(self.botGuardar)

        self.botDeshacer = QPushButton(self.frame_16)
        self.botDeshacer.setObjectName(u"botDeshacer")
        self.botDeshacer.setEnabled(False)
        self.botDeshacer.setMinimumSize(QSize(115, 40))
        self.botDeshacer.setMaximumSize(QSize(118, 16777215))
        icon7 = QIcon()
        icon7.addFile(u":/PNG/resources/icons/png/undo.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.botDeshacer.setIcon(icon7)
        self.botDeshacer.setIconSize(QSize(24, 24))

        self.verticalLayout.addWidget(self.botDeshacer)

        self.botBorrar = QPushButton(self.frame_16)
        self.botBorrar.setObjectName(u"botBorrar")
        self.botBorrar.setMinimumSize(QSize(115, 40))
        self.botBorrar.setMaximumSize(QSize(118, 16777215))
        icon8 = QIcon()
        icon8.addFile(u":/PNG/resources/icons/png/delete.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.botBorrar.setIcon(icon8)
        self.botBorrar.setIconSize(QSize(24, 24))

        self.verticalLayout.addWidget(self.botBorrar)

        self.btnExcepciones_3 = QPushButton(self.frame_16)
        self.btnExcepciones_3.setObjectName(u"btnExcepciones_3")
        self.btnExcepciones_3.setMinimumSize(QSize(0, 40))
        icon9 = QIcon()
        icon9.addFile(u":/Icons/PNG/excepciones.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnExcepciones_3.setIcon(icon9)
        self.btnExcepciones_3.setIconSize(QSize(24, 24))

        self.verticalLayout.addWidget(self.btnExcepciones_3)

        self.btnKit = QPushButton(self.frame_16)
        self.btnKit.setObjectName(u"btnKit")
        self.btnKit.setMinimumSize(QSize(0, 40))
        icon10 = QIcon()
        icon10.addFile(u":/Icons/PNG/kits.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnKit.setIcon(icon10)
        self.btnKit.setIconSize(QSize(24, 24))

        self.verticalLayout.addWidget(self.btnKit)

        self.btn_cerrar = QPushButton(self.frame_16)
        self.btn_cerrar.setObjectName(u"btn_cerrar")
        self.btn_cerrar.setMinimumSize(QSize(115, 40))
        icon11 = QIcon()
        icon11.addFile(u":/PNG/resources/icons/png/Exit.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_cerrar.setIcon(icon11)
        self.btn_cerrar.setIconSize(QSize(24, 24))

        self.verticalLayout.addWidget(self.btn_cerrar)


        self.gridLayout_2.addWidget(self.frame_16, 0, 0, 2, 1)

        self.lblkit = QLabel(self.page)
        self.lblkit.setObjectName(u"lblkit")
        self.lblkit.setMinimumSize(QSize(120, 0))
        self.lblkit.setMaximumSize(QSize(150, 16777215))
        self.lblkit.setStyleSheet(u"background-color: rgb(0, 0, 127);\n"
"color: rgb(255, 255, 255);")
        self.lblkit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lblkit, 0, 5, 1, 1)

        self.lbl_en_promocion = QLabel(self.page)
        self.lbl_en_promocion.setObjectName(u"lbl_en_promocion")
        self.lbl_en_promocion.setMinimumSize(QSize(120, 0))
        self.lbl_en_promocion.setMaximumSize(QSize(150, 19))
        self.lbl_en_promocion.setStyleSheet(u"background-color: rgb(255, 85, 0);\n"
"color: rgb(255, 255, 255);")
        self.lbl_en_promocion.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lbl_en_promocion, 0, 4, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_9, 0, 3, 1, 1)

        self.lblCodigo = QLabel(self.page)
        self.lblCodigo.setObjectName(u"lblCodigo")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblCodigo.sizePolicy().hasHeightForWidth())
        self.lblCodigo.setSizePolicy(sizePolicy)
        self.lblCodigo.setMaximumSize(QSize(130, 16777215))

        self.gridLayout_2.addWidget(self.lblCodigo, 0, 1, 1, 1)

        self.lblDescripcion = QLabel(self.page)
        self.lblDescripcion.setObjectName(u"lblDescripcion")
        sizePolicy.setHeightForWidth(self.lblDescripcion.sizePolicy().hasHeightForWidth())
        self.lblDescripcion.setSizePolicy(sizePolicy)
        self.lblDescripcion.setMinimumSize(QSize(0, 0))
        self.lblDescripcion.setMaximumSize(QSize(425, 16777215))

        self.gridLayout_2.addWidget(self.lblDescripcion, 0, 2, 1, 1)

        self.Pestanas = QTabWidget(self.page)
        self.Pestanas.setObjectName(u"Pestanas")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.Pestanas.sizePolicy().hasHeightForWidth())
        self.Pestanas.setSizePolicy(sizePolicy1)
        self.Pestanas.setMinimumSize(QSize(0, 46))
        font = QFont()
        font.setKerning(False)
        self.Pestanas.setFont(font)
        self.tab_articulo = QWidget()
        self.tab_articulo.setObjectName(u"tab_articulo")
        self.tab_articulo.setStyleSheet(u"")
        self.gridLayout_8 = QGridLayout(self.tab_articulo)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.frame_11 = QFrame(self.tab_articulo)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setMaximumSize(QSize(16777215, 45))
        self.frame_11.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_14 = QGridLayout(self.frame_11)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.label_4 = QLabel(self.frame_11)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_14.addWidget(self.label_4, 0, 0, 1, 1)

        self.txtcodigo_fabricante = QLineEdit(self.frame_11)
        self.txtcodigo_fabricante.setObjectName(u"txtcodigo_fabricante")
        self.txtcodigo_fabricante.setMaximumSize(QSize(120, 16777215))
        self.txtcodigo_fabricante.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.txtcodigo_fabricante, 0, 1, 1, 1)


        self.gridLayout_8.addWidget(self.frame_11, 1, 4, 1, 3)

        self.frame_13 = QFrame(self.tab_articulo)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setMaximumSize(QSize(16777215, 45))
        self.frame_13.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_13.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_16 = QGridLayout(self.frame_13)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.label_2 = QLabel(self.frame_13)
        self.label_2.setObjectName(u"label_2")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy2)

        self.gridLayout_16.addWidget(self.label_2, 0, 0, 1, 1)

        self.txtcodigo = QLineEdit(self.frame_13)
        self.txtcodigo.setObjectName(u"txtcodigo")
        sizePolicy.setHeightForWidth(self.txtcodigo.sizePolicy().hasHeightForWidth())
        self.txtcodigo.setSizePolicy(sizePolicy)
        self.txtcodigo.setProperty(u"codeField", True)

        self.gridLayout_16.addWidget(self.txtcodigo, 0, 1, 1, 1)


        self.gridLayout_8.addWidget(self.frame_13, 1, 0, 1, 2)

        self.frame_12 = QFrame(self.tab_articulo)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setMaximumSize(QSize(16777215, 45))
        self.frame_12.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_12.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_15 = QGridLayout(self.frame_12)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.label_3 = QLabel(self.frame_12)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_15.addWidget(self.label_3, 0, 0, 1, 1)

        self.txtcodigo_barras = QLineEdit(self.frame_12)
        self.txtcodigo_barras.setObjectName(u"txtcodigo_barras")
        sizePolicy.setHeightForWidth(self.txtcodigo_barras.sizePolicy().hasHeightForWidth())
        self.txtcodigo_barras.setSizePolicy(sizePolicy)
        self.txtcodigo_barras.setMinimumSize(QSize(148, 0))
        self.txtcodigo_barras.setMaximumSize(QSize(120, 16777215))
        self.txtcodigo_barras.setProperty(u"testField", True)

        self.gridLayout_15.addWidget(self.txtcodigo_barras, 0, 1, 1, 1)

        self.txtcodigo_barras.raise_()
        self.label_3.raise_()

        self.gridLayout_8.addWidget(self.frame_12, 1, 2, 1, 2)

        self.txtdescripcionResumida = QLineEdit(self.tab_articulo)
        self.txtdescripcionResumida.setObjectName(u"txtdescripcionResumida")
        self.txtdescripcionResumida.setMaximumSize(QSize(16777215, 27))

        self.gridLayout_8.addWidget(self.txtdescripcionResumida, 2, 1, 1, 6)

        self.label_6 = QLabel(self.tab_articulo)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_8.addWidget(self.label_6, 2, 0, 1, 1)

        self.label_8 = QLabel(self.tab_articulo)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_8.addWidget(self.label_8, 3, 0, 1, 1)

        self.txtproveedor = QLineEdit(self.tab_articulo)
        self.txtproveedor.setObjectName(u"txtproveedor")
        self.txtproveedor.setMaximumSize(QSize(16777215, 24))

        self.gridLayout_8.addWidget(self.txtproveedor, 3, 2, 1, 4)

        self.txtcodigo_proveedor = QLineEdit(self.tab_articulo)
        self.txtcodigo_proveedor.setObjectName(u"txtcodigo_proveedor")
        sizePolicy.setHeightForWidth(self.txtcodigo_proveedor.sizePolicy().hasHeightForWidth())
        self.txtcodigo_proveedor.setSizePolicy(sizePolicy)
        self.txtcodigo_proveedor.setMinimumSize(QSize(100, 0))
        self.txtcodigo_proveedor.setMaximumSize(QSize(100, 24))
        self.txtcodigo_proveedor.setProperty(u"locateField", True)

        self.gridLayout_8.addWidget(self.txtcodigo_proveedor, 3, 1, 1, 1)

        self.btnBuscarProveedor = QPushButton(self.tab_articulo)
        self.btnBuscarProveedor.setObjectName(u"btnBuscarProveedor")
        self.btnBuscarProveedor.setEnabled(False)
        self.btnBuscarProveedor.setMaximumSize(QSize(16777215, 24))
        icon12 = QIcon()
        icon12.addFile(u":/Icons/PNG/search.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnBuscarProveedor.setIcon(icon12)
        self.btnBuscarProveedor.setIconSize(QSize(16, 16))

        self.gridLayout_8.addWidget(self.btnBuscarProveedor, 3, 6, 1, 1)

        self.FrameRF = QFrame(self.tab_articulo)
        self.FrameRF.setObjectName(u"FrameRF")
        self.FrameRF.setFrameShape(QFrame.Shape.StyledPanel)
        self.FrameRF.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_7 = QGridLayout(self.FrameRF)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.txtcomentario = QTextEdit(self.FrameRF)
        self.txtcomentario.setObjectName(u"txtcomentario")
        sizePolicy1.setHeightForWidth(self.txtcomentario.sizePolicy().hasHeightForWidth())
        self.txtcomentario.setSizePolicy(sizePolicy1)

        self.gridLayout_7.addWidget(self.txtcomentario, 2, 1, 1, 1)

        self.label_18 = QLabel(self.FrameRF)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout_7.addWidget(self.label_18, 1, 1, 1, 1)


        self.gridLayout_8.addWidget(self.FrameRF, 7, 7, 2, 1)

        self.frame_20 = QFrame(self.tab_articulo)
        self.frame_20.setObjectName(u"frame_20")
        self.frame_20.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_20.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_42 = QGridLayout(self.frame_20)
        self.gridLayout_42.setObjectName(u"gridLayout_42")
        self.txtdescripcion = QTextEdit(self.frame_20)
        self.txtdescripcion.setObjectName(u"txtdescripcion")

        self.gridLayout_42.addWidget(self.txtdescripcion, 1, 0, 1, 1)

        self.label_7 = QLabel(self.frame_20)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_42.addWidget(self.label_7, 0, 0, 1, 1)


        self.gridLayout_8.addWidget(self.frame_20, 1, 7, 6, 1)

        self.frame_4 = QFrame(self.tab_articulo)
        self.frame_4.setObjectName(u"frame_4")
        sizePolicy.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy)
        self.frame_4.setMaximumSize(QSize(16777215, 40))
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_19 = QLabel(self.frame_4)
        self.label_19.setObjectName(u"label_19")

        self.horizontalLayout_4.addWidget(self.label_19)

        self.cboTipoIVA = QComboBox(self.frame_4)
        self.cboTipoIVA.setObjectName(u"cboTipoIVA")

        self.horizontalLayout_4.addWidget(self.cboTipoIVA)


        self.gridLayout_8.addWidget(self.frame_4, 4, 0, 1, 1)

        self.frame_8 = QFrame(self.tab_articulo)
        self.frame_8.setObjectName(u"frame_8")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.frame_8.sizePolicy().hasHeightForWidth())
        self.frame_8.setSizePolicy(sizePolicy3)
        self.frame_8.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_8)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.TablaTarifas = QTableView(self.frame_8)
        self.TablaTarifas.setObjectName(u"TablaTarifas")
        sizePolicy1.setHeightForWidth(self.TablaTarifas.sizePolicy().hasHeightForWidth())
        self.TablaTarifas.setSizePolicy(sizePolicy1)
        self.TablaTarifas.setAlternatingRowColors(True)
        self.TablaTarifas.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.TablaTarifas.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.gridLayout_4.addWidget(self.TablaTarifas, 0, 0, 1, 3)

        self.btnEditartarifa = QPushButton(self.frame_8)
        self.btnEditartarifa.setObjectName(u"btnEditartarifa")
        self.btnEditartarifa.setEnabled(False)
        sizePolicy.setHeightForWidth(self.btnEditartarifa.sizePolicy().hasHeightForWidth())
        self.btnEditartarifa.setSizePolicy(sizePolicy)
        self.btnEditartarifa.setIcon(icon5)

        self.gridLayout_4.addWidget(self.btnEditartarifa, 1, 2, 1, 1)


        self.gridLayout_8.addWidget(self.frame_8, 6, 0, 3, 7)

        self.frame_2 = QFrame(self.tab_articulo)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_2)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.chkcontrolar_stock = QCheckBox(self.frame_2)
        self.chkcontrolar_stock.setObjectName(u"chkcontrolar_stock")

        self.gridLayout_5.addWidget(self.chkcontrolar_stock, 0, 0, 1, 1)


        self.gridLayout_8.addWidget(self.frame_2, 4, 4, 1, 3)

        self.frame_10 = QFrame(self.tab_articulo)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_13 = QGridLayout(self.frame_10)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.chkmostrar_web = QCheckBox(self.frame_10)
        self.chkmostrar_web.setObjectName(u"chkmostrar_web")

        self.gridLayout_13.addWidget(self.chkmostrar_web, 0, 0, 1, 1)


        self.gridLayout_8.addWidget(self.frame_10, 4, 3, 1, 1)

        self.frame_5 = QFrame(self.tab_articulo)
        self.frame_5.setObjectName(u"frame_5")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy4)
        self.frame_5.setMinimumSize(QSize(0, 0))
        self.frame_5.setMaximumSize(QSize(16777215, 80))
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame_5)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_13 = QLabel(self.frame_5)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout.addWidget(self.label_13, 0, 4, 1, 1)

        self.txtMargen = QDoubleSpinBox(self.frame_5)
        self.txtMargen.setObjectName(u"txtMargen")
        self.txtMargen.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.txtMargen.setDecimals(2)
        self.txtMargen.setMinimum(-1000.000000000000000)
        self.txtMargen.setMaximum(9999.989999999999782)
        self.txtMargen.setValue(0.000000000000000)

        self.gridLayout.addWidget(self.txtMargen, 0, 3, 1, 1)

        self.label_5 = QLabel(self.frame_5)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)

        self.txtCoste_real = QLineEdit(self.frame_5)
        self.txtCoste_real.setObjectName(u"txtCoste_real")
        self.txtCoste_real.setMinimumSize(QSize(87, 0))
        self.txtCoste_real.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.txtCoste_real.setReadOnly(True)

        self.gridLayout.addWidget(self.txtCoste_real, 0, 1, 1, 1)

        self.txtdto = QLineEdit(self.frame_5)
        self.txtdto.setObjectName(u"txtdto")
        self.txtdto.setMinimumSize(QSize(62, 0))
        self.txtdto.setMaximumSize(QSize(80, 16777215))
        self.txtdto.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.txtdto, 0, 8, 1, 1)

        self.label_12 = QLabel(self.frame_5)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout.addWidget(self.label_12, 0, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(315, 17, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 6, 1, 1)

        self.txtMargen_min = QDoubleSpinBox(self.frame_5)
        self.txtMargen_min.setObjectName(u"txtMargen_min")
        self.txtMargen_min.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.txtMargen_min.setMinimum(-1000.000000000000000)
        self.txtMargen_min.setMaximum(9999.000000000000000)
        self.txtMargen_min.setValue(0.000000000000000)

        self.gridLayout.addWidget(self.txtMargen_min, 0, 5, 1, 1)

        self.label_20 = QLabel(self.frame_5)
        self.label_20.setObjectName(u"label_20")

        self.gridLayout.addWidget(self.label_20, 0, 7, 1, 1)


        self.gridLayout_8.addWidget(self.frame_5, 5, 0, 1, 7)

        self.frame_7 = QFrame(self.tab_articulo)
        self.frame_7.setObjectName(u"frame_7")
        sizePolicy4.setHeightForWidth(self.frame_7.sizePolicy().hasHeightForWidth())
        self.frame_7.setSizePolicy(sizePolicy4)
        self.frame_7.setMinimumSize(QSize(180, 0))
        self.frame_7.setMaximumSize(QSize(16777215, 40))
        self.frame_7.setAutoFillBackground(False)
        self.frame_7.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_7)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_14 = QLabel(self.frame_7)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setAutoFillBackground(False)

        self.horizontalLayout_5.addWidget(self.label_14)

        self.txtcoste = QLineEdit(self.frame_7)
        self.txtcoste.setObjectName(u"txtcoste")
        self.txtcoste.setMaximumSize(QSize(120, 16777215))
        self.txtcoste.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.txtcoste)


        self.gridLayout_8.addWidget(self.frame_7, 4, 1, 1, 2)

        self.Pestanas.addTab(self.tab_articulo, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_32 = QGridLayout(self.tab)
        self.gridLayout_32.setObjectName(u"gridLayout_32")
        self.FrameRF_2 = QFrame(self.tab)
        self.FrameRF_2.setObjectName(u"FrameRF_2")
        self.FrameRF_2.setMinimumSize(QSize(0, 0))
        self.FrameRF_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.FrameRF_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.FrameRF_2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_9 = QLabel(self.FrameRF_2)
        self.label_9.setObjectName(u"label_9")

        self.verticalLayout_5.addWidget(self.label_9)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.txtseccion = QLineEdit(self.FrameRF_2)
        self.txtseccion.setObjectName(u"txtseccion")
        self.txtseccion.setEnabled(True)
        self.txtseccion.setAutoFillBackground(False)
        self.txtseccion.setReadOnly(True)
        self.txtseccion.setProperty(u"locateField", True)

        self.horizontalLayout_2.addWidget(self.txtseccion)

        self.botBuscarSeccion = QPushButton(self.FrameRF_2)
        self.botBuscarSeccion.setObjectName(u"botBuscarSeccion")
        self.botBuscarSeccion.setEnabled(False)
        sizePolicy.setHeightForWidth(self.botBuscarSeccion.sizePolicy().hasHeightForWidth())
        self.botBuscarSeccion.setSizePolicy(sizePolicy)
        self.botBuscarSeccion.setMaximumSize(QSize(25, 16777215))
        self.botBuscarSeccion.setIcon(icon4)
        self.botBuscarSeccion.setIconSize(QSize(16, 16))

        self.horizontalLayout_2.addWidget(self.botBuscarSeccion)


        self.verticalLayout_5.addLayout(self.horizontalLayout_2)

        self.label_10 = QLabel(self.FrameRF_2)
        self.label_10.setObjectName(u"label_10")

        self.verticalLayout_5.addWidget(self.label_10)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.txtfamilia = QLineEdit(self.FrameRF_2)
        self.txtfamilia.setObjectName(u"txtfamilia")
        self.txtfamilia.setEnabled(True)
        self.txtfamilia.setAutoFillBackground(False)
        self.txtfamilia.setReadOnly(True)
        self.txtfamilia.setProperty(u"locateField", True)

        self.horizontalLayout_6.addWidget(self.txtfamilia)

        self.botBuscarFamilia = QPushButton(self.FrameRF_2)
        self.botBuscarFamilia.setObjectName(u"botBuscarFamilia")
        self.botBuscarFamilia.setEnabled(False)
        sizePolicy.setHeightForWidth(self.botBuscarFamilia.sizePolicy().hasHeightForWidth())
        self.botBuscarFamilia.setSizePolicy(sizePolicy)
        self.botBuscarFamilia.setMaximumSize(QSize(25, 16777215))
        self.botBuscarFamilia.setIcon(icon4)
        self.botBuscarFamilia.setIconSize(QSize(16, 16))

        self.horizontalLayout_6.addWidget(self.botBuscarFamilia)


        self.verticalLayout_5.addLayout(self.horizontalLayout_6)

        self.label_11 = QLabel(self.FrameRF_2)
        self.label_11.setObjectName(u"label_11")

        self.verticalLayout_5.addWidget(self.label_11)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.txtsubfamilia = QLineEdit(self.FrameRF_2)
        self.txtsubfamilia.setObjectName(u"txtsubfamilia")
        self.txtsubfamilia.setEnabled(True)
        self.txtsubfamilia.setAutoFillBackground(False)
        self.txtsubfamilia.setReadOnly(True)
        self.txtsubfamilia.setProperty(u"locateField", True)

        self.horizontalLayout_7.addWidget(self.txtsubfamilia)

        self.botBuscarSubfamilia = QPushButton(self.FrameRF_2)
        self.botBuscarSubfamilia.setObjectName(u"botBuscarSubfamilia")
        self.botBuscarSubfamilia.setEnabled(False)
        sizePolicy.setHeightForWidth(self.botBuscarSubfamilia.sizePolicy().hasHeightForWidth())
        self.botBuscarSubfamilia.setSizePolicy(sizePolicy)
        self.botBuscarSubfamilia.setMaximumSize(QSize(25, 16777215))
        self.botBuscarSubfamilia.setIcon(icon4)
        self.botBuscarSubfamilia.setIconSize(QSize(16, 16))

        self.horizontalLayout_7.addWidget(self.botBuscarSubfamilia)


        self.verticalLayout_5.addLayout(self.horizontalLayout_7)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_7)


        self.gridLayout_32.addWidget(self.FrameRF_2, 0, 0, 1, 1)

        self.Pestanas.addTab(self.tab, "")
        self.tab_distribuidores = QWidget()
        self.tab_distribuidores.setObjectName(u"tab_distribuidores")
        self.verticalLayout_4 = QVBoxLayout(self.tab_distribuidores)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tablaProveedores = QTableView(self.tab_distribuidores)
        self.tablaProveedores.setObjectName(u"tablaProveedores")
        self.tablaProveedores.setMaximumSize(QSize(16777215, 299))
        self.tablaProveedores.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tablaProveedores.setAlternatingRowColors(True)
        self.tablaProveedores.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tablaProveedores.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tablaProveedores.setGridStyle(Qt.PenStyle.DotLine)
        self.tablaProveedores.setSortingEnabled(False)
        self.tablaProveedores.horizontalHeader().setCascadingSectionResizes(False)
        self.tablaProveedores.horizontalHeader().setProperty(u"showSortIndicator", False)
        self.tablaProveedores.horizontalHeader().setStretchLastSection(True)
        self.tablaProveedores.verticalHeader().setVisible(False)

        self.verticalLayout_2.addWidget(self.tablaProveedores)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_23 = QLabel(self.tab_distribuidores)
        self.label_23.setObjectName(u"label_23")

        self.horizontalLayout_3.addWidget(self.label_23)

        self.btnAnadirDistribuidores = QPushButton(self.tab_distribuidores)
        self.btnAnadirDistribuidores.setObjectName(u"btnAnadirDistribuidores")
        self.btnAnadirDistribuidores.setEnabled(False)
        self.btnAnadirDistribuidores.setIcon(icon1)
        self.btnAnadirDistribuidores.setIconSize(QSize(15, 15))

        self.horizontalLayout_3.addWidget(self.btnAnadirDistribuidores)

        self.btnEditarDistribuidorFrecuente = QPushButton(self.tab_distribuidores)
        self.btnEditarDistribuidorFrecuente.setObjectName(u"btnEditarDistribuidorFrecuente")
        self.btnEditarDistribuidorFrecuente.setEnabled(False)
        self.btnEditarDistribuidorFrecuente.setIcon(icon5)
        self.btnEditarDistribuidorFrecuente.setIconSize(QSize(15, 15))

        self.horizontalLayout_3.addWidget(self.btnEditarDistribuidorFrecuente)

        self.btnBorrarDistribuidores = QPushButton(self.tab_distribuidores)
        self.btnBorrarDistribuidores.setObjectName(u"btnBorrarDistribuidores")
        self.btnBorrarDistribuidores.setEnabled(False)
        self.btnBorrarDistribuidores.setMaximumSize(QSize(25, 16777215))
        self.btnBorrarDistribuidores.setIcon(icon8)
        self.btnBorrarDistribuidores.setIconSize(QSize(15, 15))

        self.horizontalLayout_3.addWidget(self.btnBorrarDistribuidores)

        self.btnAsignarDistribuidor = QPushButton(self.tab_distribuidores)
        self.btnAsignarDistribuidor.setObjectName(u"btnAsignarDistribuidor")
        self.btnAsignarDistribuidor.setEnabled(False)
        self.btnAsignarDistribuidor.setIcon(icon6)
        self.btnAsignarDistribuidor.setIconSize(QSize(15, 15))

        self.horizontalLayout_3.addWidget(self.btnAsignarDistribuidor)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)


        self.verticalLayout_4.addLayout(self.verticalLayout_2)

        self.graf_prov = OpenChart(self.tab_distribuidores)
        self.graf_prov.setObjectName(u"graf_prov")
        sizePolicy3.setHeightForWidth(self.graf_prov.sizePolicy().hasHeightForWidth())
        self.graf_prov.setSizePolicy(sizePolicy3)
        self.graf_prov.setMinimumSize(QSize(0, 232))
        self.graf_prov.setProperty(u"Etiquetas", True)
        self.graf_prov.setProperty(u"ValoresEjeY", True)
        self.graf_prov.setProperty(u"Leyenda", False)
        self.graf_prov.setProperty(u"animationDuration", 700)

        self.verticalLayout_4.addWidget(self.graf_prov)

        self.Pestanas.addTab(self.tab_distribuidores, "")
        self.tab_promociones = QWidget()
        self.tab_promociones.setObjectName(u"tab_promociones")
        self.gridLayout_39 = QGridLayout(self.tab_promociones)
        self.gridLayout_39.setObjectName(u"gridLayout_39")
        self.chkArticulo_promocionado = QCheckBox(self.tab_promociones)
        self.chkArticulo_promocionado.setObjectName(u"chkArticulo_promocionado")

        self.gridLayout_39.addWidget(self.chkArticulo_promocionado, 0, 0, 1, 1)

        self.frame_pvp_fijo = QFrame(self.tab_promociones)
        self.frame_pvp_fijo.setObjectName(u"frame_pvp_fijo")
        self.frame_pvp_fijo.setEnabled(False)
        self.frame_pvp_fijo.setMaximumSize(QSize(16777215, 70))
        self.frame_pvp_fijo.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_pvp_fijo.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_26 = QGridLayout(self.frame_pvp_fijo)
        self.gridLayout_26.setObjectName(u"gridLayout_26")
        self.label_63 = QLabel(self.frame_pvp_fijo)
        self.label_63.setObjectName(u"label_63")
        self.label_63.setMinimumSize(QSize(0, 25))
        self.label_63.setMaximumSize(QSize(16777215, 27))
        self.label_63.setStyleSheet(u"background-color: #304163;\n"
"color: rgb(255, 255, 255);")
        self.label_63.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_26.addWidget(self.label_63, 0, 0, 1, 3)

        self.horizontalSpacer_7 = QSpacerItem(224, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_26.addItem(self.horizontalSpacer_7, 1, 0, 1, 1)

        self.lbl_oferta_importe = QLabel(self.frame_pvp_fijo)
        self.lbl_oferta_importe.setObjectName(u"lbl_oferta_importe")

        self.gridLayout_26.addWidget(self.lbl_oferta_importe, 1, 1, 1, 1)

        self.txtoferta_pvp_fijo = QLineEdit(self.frame_pvp_fijo)
        self.txtoferta_pvp_fijo.setObjectName(u"txtoferta_pvp_fijo")
        self.txtoferta_pvp_fijo.setMinimumSize(QSize(0, 27))
        self.txtoferta_pvp_fijo.setMaximumSize(QSize(110, 27))
        self.txtoferta_pvp_fijo.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_26.addWidget(self.txtoferta_pvp_fijo, 1, 2, 1, 1)


        self.gridLayout_39.addWidget(self.frame_pvp_fijo, 6, 0, 1, 2)

        self.frame_tipo_32 = QFrame(self.tab_promociones)
        self.frame_tipo_32.setObjectName(u"frame_tipo_32")
        self.frame_tipo_32.setEnabled(False)
        self.frame_tipo_32.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_tipo_32.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_24 = QGridLayout(self.frame_tipo_32)
        self.gridLayout_24.setObjectName(u"gridLayout_24")
        self.lbl_por_cada = QLabel(self.frame_tipo_32)
        self.lbl_por_cada.setObjectName(u"lbl_por_cada")
        self.lbl_por_cada.setEnabled(False)
        self.lbl_por_cada.setMaximumSize(QSize(16777215, 27))

        self.gridLayout_24.addWidget(self.lbl_por_cada, 1, 0, 1, 1)

        self.txtOferta_por_cada = QLineEdit(self.frame_tipo_32)
        self.txtOferta_por_cada.setObjectName(u"txtOferta_por_cada")
        self.txtOferta_por_cada.setEnabled(False)
        self.txtOferta_por_cada.setMinimumSize(QSize(0, 27))
        self.txtOferta_por_cada.setMaximumSize(QSize(50, 27))
        self.txtOferta_por_cada.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_24.addWidget(self.txtOferta_por_cada, 1, 1, 1, 1)

        self.lbl_unidades = QLabel(self.frame_tipo_32)
        self.lbl_unidades.setObjectName(u"lbl_unidades")
        self.lbl_unidades.setEnabled(False)
        self.lbl_unidades.setMaximumSize(QSize(16777215, 27))

        self.gridLayout_24.addWidget(self.lbl_unidades, 1, 2, 1, 1)

        self.lbl_regalo_de = QLabel(self.frame_tipo_32)
        self.lbl_regalo_de.setObjectName(u"lbl_regalo_de")
        self.lbl_regalo_de.setEnabled(False)
        self.lbl_regalo_de.setMaximumSize(QSize(16777215, 27))

        self.gridLayout_24.addWidget(self.lbl_regalo_de, 1, 3, 1, 1)

        self.txtOfertaregalo_de = QLineEdit(self.frame_tipo_32)
        self.txtOfertaregalo_de.setObjectName(u"txtOfertaregalo_de")
        self.txtOfertaregalo_de.setEnabled(False)
        self.txtOfertaregalo_de.setMinimumSize(QSize(0, 27))
        self.txtOfertaregalo_de.setMaximumSize(QSize(50, 27))
        self.txtOfertaregalo_de.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_24.addWidget(self.txtOfertaregalo_de, 1, 4, 1, 1)

        self.lbl_unidades_2 = QLabel(self.frame_tipo_32)
        self.lbl_unidades_2.setObjectName(u"lbl_unidades_2")
        self.lbl_unidades_2.setEnabled(False)
        self.lbl_unidades_2.setMaximumSize(QSize(16777215, 27))

        self.gridLayout_24.addWidget(self.lbl_unidades_2, 1, 5, 1, 1)

        self.label_57 = QLabel(self.frame_tipo_32)
        self.label_57.setObjectName(u"label_57")
        self.label_57.setEnabled(False)
        self.label_57.setMinimumSize(QSize(0, 27))
        self.label_57.setMaximumSize(QSize(16777215, 27))
        self.label_57.setStyleSheet(u"background-color: #304163;\n"
"color: rgb(255, 255, 255);")
        self.label_57.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_24.addWidget(self.label_57, 0, 0, 1, 6)


        self.gridLayout_39.addWidget(self.frame_tipo_32, 3, 0, 1, 2)

        self.txtOferta_Fecha_fin = QDateEdit(self.tab_promociones)
        self.txtOferta_Fecha_fin.setObjectName(u"txtOferta_Fecha_fin")
        self.txtOferta_Fecha_fin.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_39.addWidget(self.txtOferta_Fecha_fin, 0, 5, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_39.addItem(self.verticalSpacer_3, 7, 0, 1, 1)

        self.txtOferta_Fecha_ini = QDateEdit(self.tab_promociones)
        self.txtOferta_Fecha_ini.setObjectName(u"txtOferta_Fecha_ini")
        self.txtOferta_Fecha_ini.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_39.addWidget(self.txtOferta_Fecha_ini, 0, 3, 1, 1)

        self.frame_dto = QFrame(self.tab_promociones)
        self.frame_dto.setObjectName(u"frame_dto")
        self.frame_dto.setEnabled(False)
        self.frame_dto.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_dto.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_25 = QGridLayout(self.frame_dto)
        self.gridLayout_25.setObjectName(u"gridLayout_25")
        self.label_61 = QLabel(self.frame_dto)
        self.label_61.setObjectName(u"label_61")
        self.label_61.setMinimumSize(QSize(0, 27))
        self.label_61.setMaximumSize(QSize(16777215, 27))
        self.label_61.setStyleSheet(u"background-color: #304163;\n"
"color: rgb(255, 255, 255);")
        self.label_61.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_25.addWidget(self.label_61, 0, 0, 1, 3)

        self.horizontalSpacer_5 = QSpacerItem(249, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_25.addItem(self.horizontalSpacer_5, 1, 0, 1, 1)

        self.lbl_oferta_dto = QLabel(self.frame_dto)
        self.lbl_oferta_dto.setObjectName(u"lbl_oferta_dto")

        self.gridLayout_25.addWidget(self.lbl_oferta_dto, 1, 1, 1, 1)

        self.txtOfertaDtoOferta = QLineEdit(self.frame_dto)
        self.txtOfertaDtoOferta.setObjectName(u"txtOfertaDtoOferta")
        self.txtOfertaDtoOferta.setMinimumSize(QSize(0, 27))
        self.txtOfertaDtoOferta.setMaximumSize(QSize(50, 27))
        self.txtOfertaDtoOferta.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_25.addWidget(self.txtOfertaDtoOferta, 1, 2, 1, 1)


        self.gridLayout_39.addWidget(self.frame_dto, 4, 0, 1, 2)

        self.frame_ofertaweb = QFrame(self.tab_promociones)
        self.frame_ofertaweb.setObjectName(u"frame_ofertaweb")
        self.frame_ofertaweb.setEnabled(False)
        self.frame_ofertaweb.setMinimumSize(QSize(0, 49))
        self.frame_ofertaweb.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_ofertaweb.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_ofertaweb)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_8)

        self.lbl_dto_web = QLabel(self.frame_ofertaweb)
        self.lbl_dto_web.setObjectName(u"lbl_dto_web")

        self.horizontalLayout.addWidget(self.lbl_dto_web)

        self.lbl_dto_web2 = QLabel(self.frame_ofertaweb)
        self.lbl_dto_web2.setObjectName(u"lbl_dto_web2")

        self.horizontalLayout.addWidget(self.lbl_dto_web2)

        self.txtOferta_dto_web = QLineEdit(self.frame_ofertaweb)
        self.txtOferta_dto_web.setObjectName(u"txtOferta_dto_web")
        self.txtOferta_dto_web.setMinimumSize(QSize(0, 27))
        self.txtOferta_dto_web.setMaximumSize(QSize(50, 27))
        self.txtOferta_dto_web.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout.addWidget(self.txtOferta_dto_web)


        self.gridLayout_39.addWidget(self.frame_ofertaweb, 5, 0, 1, 2)

        self.label_68 = QLabel(self.tab_promociones)
        self.label_68.setObjectName(u"label_68")
        self.label_68.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_39.addWidget(self.label_68, 0, 4, 1, 1)

        self.label_21 = QLabel(self.tab_promociones)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_39.addWidget(self.label_21, 0, 2, 1, 1)

        self.chkMostrar_en_cuadro = QCheckBox(self.tab_promociones)
        self.chkMostrar_en_cuadro.setObjectName(u"chkMostrar_en_cuadro")

        self.gridLayout_39.addWidget(self.chkMostrar_en_cuadro, 0, 1, 1, 1)

        self.framePromocion = QFrame(self.tab_promociones)
        self.framePromocion.setObjectName(u"framePromocion")
        self.framePromocion.setEnabled(False)
        self.framePromocion.setFrameShape(QFrame.Shape.StyledPanel)
        self.framePromocion.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_34 = QGridLayout(self.framePromocion)
        self.gridLayout_34.setObjectName(u"gridLayout_34")
        self.lblDescripcion_oferta = QLabel(self.framePromocion)
        self.lblDescripcion_oferta.setObjectName(u"lblDescripcion_oferta")
        self.lblDescripcion_oferta.setEnabled(False)

        self.gridLayout_34.addWidget(self.lblDescripcion_oferta, 3, 0, 1, 1)

        self.txtOferta_Descripcion_promocion = QLineEdit(self.framePromocion)
        self.txtOferta_Descripcion_promocion.setObjectName(u"txtOferta_Descripcion_promocion")
        self.txtOferta_Descripcion_promocion.setEnabled(False)
        self.txtOferta_Descripcion_promocion.setProperty(u"mandatoryField", False)

        self.gridLayout_34.addWidget(self.txtOferta_Descripcion_promocion, 3, 1, 1, 1)

        self.btnAnadir_oferta = QPushButton(self.framePromocion)
        self.btnAnadir_oferta.setObjectName(u"btnAnadir_oferta")
        self.btnAnadir_oferta.setEnabled(False)
        sizePolicy4.setHeightForWidth(self.btnAnadir_oferta.sizePolicy().hasHeightForWidth())
        self.btnAnadir_oferta.setSizePolicy(sizePolicy4)
        self.btnAnadir_oferta.setIcon(icon1)

        self.gridLayout_34.addWidget(self.btnAnadir_oferta, 0, 0, 1, 1)

        self.btnEditarOferta = QPushButton(self.framePromocion)
        self.btnEditarOferta.setObjectName(u"btnEditarOferta")
        self.btnEditarOferta.setEnabled(False)
        sizePolicy4.setHeightForWidth(self.btnEditarOferta.sizePolicy().hasHeightForWidth())
        self.btnEditarOferta.setSizePolicy(sizePolicy4)
        self.btnEditarOferta.setIcon(icon5)

        self.gridLayout_34.addWidget(self.btnEditarOferta, 1, 0, 1, 1)

        self.btnguardar_oferta = QPushButton(self.framePromocion)
        self.btnguardar_oferta.setObjectName(u"btnguardar_oferta")
        self.btnguardar_oferta.setEnabled(False)
        self.btnguardar_oferta.setIcon(icon6)

        self.gridLayout_34.addWidget(self.btnguardar_oferta, 0, 1, 1, 1)

        self.btnDeshacer_oferta = QPushButton(self.framePromocion)
        self.btnDeshacer_oferta.setObjectName(u"btnDeshacer_oferta")
        self.btnDeshacer_oferta.setEnabled(False)
        self.btnDeshacer_oferta.setIcon(icon7)

        self.gridLayout_34.addWidget(self.btnDeshacer_oferta, 1, 1, 1, 1)

        self.chkOferta_32 = QRadioButton(self.framePromocion)
        self.chkOferta_32.setObjectName(u"chkOferta_32")
        self.chkOferta_32.setStyleSheet(u"")
        self.chkOferta_32.setCheckable(True)
        self.chkOferta_32.setChecked(True)

        self.gridLayout_34.addWidget(self.chkOferta_32, 4, 0, 1, 1)

        self.chkOferta_web = QRadioButton(self.framePromocion)
        self.chkOferta_web.setObjectName(u"chkOferta_web")
        self.chkOferta_web.setStyleSheet(u"")

        self.gridLayout_34.addWidget(self.chkOferta_web, 4, 1, 1, 1)

        self.chkOferta_dto = QRadioButton(self.framePromocion)
        self.chkOferta_dto.setObjectName(u"chkOferta_dto")
        self.chkOferta_dto.setEnabled(False)
        self.chkOferta_dto.setStyleSheet(u"")
        self.chkOferta_dto.setChecked(False)

        self.gridLayout_34.addWidget(self.chkOferta_dto, 5, 0, 1, 1)

        self.chkOferta_pvp = QRadioButton(self.framePromocion)
        self.chkOferta_pvp.setObjectName(u"chkOferta_pvp")
        self.chkOferta_pvp.setStyleSheet(u"")

        self.gridLayout_34.addWidget(self.chkOferta_pvp, 5, 1, 1, 1)


        self.gridLayout_39.addWidget(self.framePromocion, 1, 0, 2, 2)

        self.frame_comentarios = QFrame(self.tab_promociones)
        self.frame_comentarios.setObjectName(u"frame_comentarios")
        self.frame_comentarios.setEnabled(False)
        self.frame_comentarios.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_comentarios.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_27 = QGridLayout(self.frame_comentarios)
        self.gridLayout_27.setObjectName(u"gridLayout_27")
        self.txtOferta_comentarios_promocion = QTextEdit(self.frame_comentarios)
        self.txtOferta_comentarios_promocion.setObjectName(u"txtOferta_comentarios_promocion")

        self.gridLayout_27.addWidget(self.txtOferta_comentarios_promocion, 2, 0, 1, 1)

        self.label_65 = QLabel(self.frame_comentarios)
        self.label_65.setObjectName(u"label_65")
        self.label_65.setMinimumSize(QSize(0, 27))
        self.label_65.setStyleSheet(u"background-color: #304163;\n"
"color: rgb(255, 255, 255);")
        self.label_65.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_27.addWidget(self.label_65, 1, 0, 1, 1)


        self.gridLayout_39.addWidget(self.frame_comentarios, 4, 2, 3, 5)

        self.frame_tabla_ofertas = QFrame(self.tab_promociones)
        self.frame_tabla_ofertas.setObjectName(u"frame_tabla_ofertas")
        self.frame_tabla_ofertas.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_tabla_ofertas.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_9 = QGridLayout(self.frame_tabla_ofertas)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.label_72 = QLabel(self.frame_tabla_ofertas)
        self.label_72.setObjectName(u"label_72")
        self.label_72.setMinimumSize(QSize(0, 27))
        self.label_72.setStyleSheet(u"background-color: #304163;\n"
"color: rgb(255, 255, 255);")
        self.label_72.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.label_72, 0, 0, 1, 5)

        self.btnActivarOferta = QPushButton(self.frame_tabla_ofertas)
        self.btnActivarOferta.setObjectName(u"btnActivarOferta")
        self.btnActivarOferta.setEnabled(False)
        icon13 = QIcon()
        icon13.addFile(u":/Icons/PNG/OK.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnActivarOferta.setIcon(icon13)

        self.gridLayout_6.addWidget(self.btnActivarOferta, 3, 0, 1, 2)

        self.tabla_ofertas = QTableView(self.frame_tabla_ofertas)
        self.tabla_ofertas.setObjectName(u"tabla_ofertas")
        self.tabla_ofertas.setAlternatingRowColors(True)
        self.tabla_ofertas.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tabla_ofertas.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabla_ofertas.horizontalHeader().setStretchLastSection(True)
        self.tabla_ofertas.verticalHeader().setVisible(False)

        self.gridLayout_6.addWidget(self.tabla_ofertas, 2, 0, 1, 5)

        self.btnBorrar_oferta = QPushButton(self.frame_tabla_ofertas)
        self.btnBorrar_oferta.setObjectName(u"btnBorrar_oferta")
        self.btnBorrar_oferta.setEnabled(False)
        sizePolicy4.setHeightForWidth(self.btnBorrar_oferta.sizePolicy().hasHeightForWidth())
        self.btnBorrar_oferta.setSizePolicy(sizePolicy4)
        icon14 = QIcon()
        icon14.addFile(u":/Icons/PNG/borrar.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnBorrar_oferta.setIcon(icon14)

        self.gridLayout_6.addWidget(self.btnBorrar_oferta, 3, 3, 1, 2)

        self.label = QLabel(self.frame_tabla_ofertas)
        self.label.setObjectName(u"label")

        self.gridLayout_6.addWidget(self.label, 1, 0, 1, 1)

        self.cboTarifaOferta = QComboBox(self.frame_tabla_ofertas)
        self.cboTarifaOferta.setObjectName(u"cboTarifaOferta")

        self.gridLayout_6.addWidget(self.cboTarifaOferta, 1, 1, 1, 2)


        self.gridLayout_9.addLayout(self.gridLayout_6, 0, 0, 1, 1)


        self.gridLayout_39.addWidget(self.frame_tabla_ofertas, 1, 2, 3, 5)

        self.Pestanas.addTab(self.tab_promociones, "")
        self.tab_web = QWidget()
        self.tab_web.setObjectName(u"tab_web")
        self.gridLayout_43 = QGridLayout(self.tab_web)
        self.gridLayout_43.setObjectName(u"gridLayout_43")
        self.txtDescWebIdioma = QTextEdit(self.tab_web)
        self.txtDescWebIdioma.setObjectName(u"txtDescWebIdioma")

        self.gridLayout_43.addWidget(self.txtDescWebIdioma, 4, 1, 1, 6)

        self.imagen3_web_idioma = QLabel(self.tab_web)
        self.imagen3_web_idioma.setObjectName(u"imagen3_web_idioma")
        self.imagen3_web_idioma.setMaximumSize(QSize(72, 72))
        self.imagen3_web_idioma.setPixmap(QPixmap(u":/Icons/PNG/Box.png"))
        self.imagen3_web_idioma.setScaledContents(True)

        self.gridLayout_43.addWidget(self.imagen3_web_idioma, 5, 6, 2, 1)

        self.label_66 = QLabel(self.tab_web)
        self.label_66.setObjectName(u"label_66")
        self.label_66.setStyleSheet(u"background-color: #304163;\n"
"color: rgb(255, 255, 255);")
        self.label_66.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_43.addWidget(self.label_66, 0, 0, 1, 1)

        self.label_51 = QLabel(self.tab_web)
        self.label_51.setObjectName(u"label_51")

        self.gridLayout_43.addWidget(self.label_51, 2, 1, 1, 1)

        self.tablaPaises_web = QTableView(self.tab_web)
        self.tablaPaises_web.setObjectName(u"tablaPaises_web")
        self.tablaPaises_web.setMaximumSize(QSize(239, 16777215))

        self.gridLayout_43.addWidget(self.tablaPaises_web, 1, 0, 8, 1)

        self.btnImg_web3_delete = QPushButton(self.tab_web)
        self.btnImg_web3_delete.setObjectName(u"btnImg_web3_delete")
        self.btnImg_web3_delete.setIcon(icon8)

        self.gridLayout_43.addWidget(self.btnImg_web3_delete, 6, 5, 1, 1)

        self.label_56 = QLabel(self.tab_web)
        self.label_56.setObjectName(u"label_56")

        self.gridLayout_43.addWidget(self.label_56, 1, 1, 1, 1)

        self.btnImg_web3_add = QPushButton(self.tab_web)
        self.btnImg_web3_add.setObjectName(u"btnImg_web3_add")
        self.btnImg_web3_add.setIcon(icon1)

        self.gridLayout_43.addWidget(self.btnImg_web3_add, 5, 5, 1, 1)

        self.btnImg_web4_add = QPushButton(self.tab_web)
        self.btnImg_web4_add.setObjectName(u"btnImg_web4_add")
        self.btnImg_web4_add.setIcon(icon1)

        self.gridLayout_43.addWidget(self.btnImg_web4_add, 7, 5, 1, 1)

        self.imagen4_web_idioma = QLabel(self.tab_web)
        self.imagen4_web_idioma.setObjectName(u"imagen4_web_idioma")
        self.imagen4_web_idioma.setMaximumSize(QSize(72, 72))
        self.imagen4_web_idioma.setPixmap(QPixmap(u":/Icons/PNG/Box.png"))
        self.imagen4_web_idioma.setScaledContents(True)

        self.gridLayout_43.addWidget(self.imagen4_web_idioma, 7, 6, 2, 1)

        self.label_64 = QLabel(self.tab_web)
        self.label_64.setObjectName(u"label_64")
        self.label_64.setStyleSheet(u"background-color: #304163;\n"
"color: rgb(255, 255, 255);")
        self.label_64.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_43.addWidget(self.label_64, 3, 1, 1, 6)

        self.btnImg_web4_delete = QPushButton(self.tab_web)
        self.btnImg_web4_delete.setObjectName(u"btnImg_web4_delete")
        self.btnImg_web4_delete.setIcon(icon8)

        self.gridLayout_43.addWidget(self.btnImg_web4_delete, 8, 5, 1, 1)

        self.txtArticulowebidioma = QLineEdit(self.tab_web)
        self.txtArticulowebidioma.setObjectName(u"txtArticulowebidioma")

        self.gridLayout_43.addWidget(self.txtArticulowebidioma, 2, 2, 1, 5)

        self.cboIdiomasweb = QComboBox(self.tab_web)
        self.cboIdiomasweb.setObjectName(u"cboIdiomasweb")

        self.gridLayout_43.addWidget(self.cboIdiomasweb, 1, 2, 1, 5)

        self.imagen1_web_idioma = QLabel(self.tab_web)
        self.imagen1_web_idioma.setObjectName(u"imagen1_web_idioma")
        self.imagen1_web_idioma.setMaximumSize(QSize(72, 72))
        self.imagen1_web_idioma.setPixmap(QPixmap(u":/Icons/PNG/Box.png"))
        self.imagen1_web_idioma.setScaledContents(True)

        self.gridLayout_43.addWidget(self.imagen1_web_idioma, 5, 4, 2, 1)

        self.imagen2_web_idioma = QLabel(self.tab_web)
        self.imagen2_web_idioma.setObjectName(u"imagen2_web_idioma")
        self.imagen2_web_idioma.setMaximumSize(QSize(72, 72))
        self.imagen2_web_idioma.setPixmap(QPixmap(u":/Icons/PNG/Box.png"))
        self.imagen2_web_idioma.setScaledContents(True)

        self.gridLayout_43.addWidget(self.imagen2_web_idioma, 7, 4, 2, 1)

        self.btnImg_web1_add = QPushButton(self.tab_web)
        self.btnImg_web1_add.setObjectName(u"btnImg_web1_add")
        self.btnImg_web1_add.setIcon(icon1)

        self.gridLayout_43.addWidget(self.btnImg_web1_add, 5, 3, 1, 1)

        self.btnImg_web1_delete = QPushButton(self.tab_web)
        self.btnImg_web1_delete.setObjectName(u"btnImg_web1_delete")
        self.btnImg_web1_delete.setIcon(icon8)

        self.gridLayout_43.addWidget(self.btnImg_web1_delete, 6, 3, 1, 1)

        self.btnImg_web2_add = QPushButton(self.tab_web)
        self.btnImg_web2_add.setObjectName(u"btnImg_web2_add")
        self.btnImg_web2_add.setIcon(icon1)

        self.gridLayout_43.addWidget(self.btnImg_web2_add, 7, 3, 1, 1)

        self.btnImg_web2_delete = QPushButton(self.tab_web)
        self.btnImg_web2_delete.setObjectName(u"btnImg_web2_delete")
        self.btnImg_web2_delete.setIcon(icon8)

        self.gridLayout_43.addWidget(self.btnImg_web2_delete, 8, 3, 1, 1)

        self.frame_21 = QFrame(self.tab_web)
        self.frame_21.setObjectName(u"frame_21")
        self.frame_21.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_21.setFrameShadow(QFrame.Shadow.Raised)
        self.pushButton = QPushButton(self.frame_21)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(10, 10, 151, 30))
        self.pushButton.setIcon(icon1)
        self.pushButton_2 = QPushButton(self.frame_21)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(170, 10, 81, 30))
        self.pushButton_2.setIcon(icon5)
        self.pushButton_3 = QPushButton(self.frame_21)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(10, 40, 151, 30))
        self.pushButton_3.setIcon(icon6)
        self.pushButton_4 = QPushButton(self.frame_21)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(170, 40, 81, 30))
        self.pushButton_4.setIcon(icon7)
        self.pushButton_5 = QPushButton(self.frame_21)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setGeometry(QRect(10, 100, 241, 30))
        self.pushButton_5.setIcon(icon8)
        self.checkBox = QCheckBox(self.frame_21)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setGeometry(QRect(10, 70, 241, 30))

        self.gridLayout_43.addWidget(self.frame_21, 5, 1, 4, 2)

        self.Pestanas.addTab(self.tab_web, "")
        self.tab_imagenes = QWidget()
        self.tab_imagenes.setObjectName(u"tab_imagenes")
        self.gridLayout_23 = QGridLayout(self.tab_imagenes)
        self.gridLayout_23.setObjectName(u"gridLayout_23")
        self.lblImagenArticulo_1 = QLabel(self.tab_imagenes)
        self.lblImagenArticulo_1.setObjectName(u"lblImagenArticulo_1")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(255)
        sizePolicy5.setVerticalStretch(255)
        sizePolicy5.setHeightForWidth(self.lblImagenArticulo_1.sizePolicy().hasHeightForWidth())
        self.lblImagenArticulo_1.setSizePolicy(sizePolicy5)
        self.lblImagenArticulo_1.setMaximumSize(QSize(256, 256))
        self.lblImagenArticulo_1.setPixmap(QPixmap(u":/Icons/PNG/paquete.png"))
        self.lblImagenArticulo_1.setScaledContents(True)

        self.gridLayout_23.addWidget(self.lblImagenArticulo_1, 0, 0, 1, 1)

        self.lblImagenArticulo_2 = QLabel(self.tab_imagenes)
        self.lblImagenArticulo_2.setObjectName(u"lblImagenArticulo_2")
        sizePolicy5.setHeightForWidth(self.lblImagenArticulo_2.sizePolicy().hasHeightForWidth())
        self.lblImagenArticulo_2.setSizePolicy(sizePolicy5)
        self.lblImagenArticulo_2.setMaximumSize(QSize(256, 256))
        self.lblImagenArticulo_2.setPixmap(QPixmap(u":/Icons/PNG/paquete.png"))
        self.lblImagenArticulo_2.setScaledContents(True)

        self.gridLayout_23.addWidget(self.lblImagenArticulo_2, 0, 1, 1, 1)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.botCambiarImagen = QPushButton(self.tab_imagenes)
        self.botCambiarImagen.setObjectName(u"botCambiarImagen")
        self.botCambiarImagen.setEnabled(False)
        self.botCambiarImagen.setMaximumSize(QSize(256, 16777215))
        icon15 = QIcon()
        icon15.addFile(u":/Icons/PNG/image.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.botCambiarImagen.setIcon(icon15)
        self.botCambiarImagen.setIconSize(QSize(32, 32))

        self.horizontalLayout_8.addWidget(self.botCambiarImagen)

        self.btnBorrarImagen_1 = QPushButton(self.tab_imagenes)
        self.btnBorrarImagen_1.setObjectName(u"btnBorrarImagen_1")
        self.btnBorrarImagen_1.setEnabled(False)
        self.btnBorrarImagen_1.setMaximumSize(QSize(100, 16777215))
        self.btnBorrarImagen_1.setIcon(icon14)
        self.btnBorrarImagen_1.setIconSize(QSize(32, 32))

        self.horizontalLayout_8.addWidget(self.btnBorrarImagen_1)


        self.gridLayout_23.addLayout(self.horizontalLayout_8, 1, 0, 1, 1)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.botCambiarImagen_2 = QPushButton(self.tab_imagenes)
        self.botCambiarImagen_2.setObjectName(u"botCambiarImagen_2")
        self.botCambiarImagen_2.setEnabled(False)
        self.botCambiarImagen_2.setIcon(icon15)
        self.botCambiarImagen_2.setIconSize(QSize(32, 32))

        self.horizontalLayout_10.addWidget(self.botCambiarImagen_2)

        self.btnBorrarimagen_2 = QPushButton(self.tab_imagenes)
        self.btnBorrarimagen_2.setObjectName(u"btnBorrarimagen_2")
        self.btnBorrarimagen_2.setEnabled(False)
        self.btnBorrarimagen_2.setMaximumSize(QSize(100, 16777215))
        self.btnBorrarimagen_2.setIcon(icon14)
        self.btnBorrarimagen_2.setIconSize(QSize(32, 32))

        self.horizontalLayout_10.addWidget(self.btnBorrarimagen_2)


        self.gridLayout_23.addLayout(self.horizontalLayout_10, 1, 1, 1, 1)

        self.lblImagenArticulo_3 = QLabel(self.tab_imagenes)
        self.lblImagenArticulo_3.setObjectName(u"lblImagenArticulo_3")
        sizePolicy5.setHeightForWidth(self.lblImagenArticulo_3.sizePolicy().hasHeightForWidth())
        self.lblImagenArticulo_3.setSizePolicy(sizePolicy5)
        self.lblImagenArticulo_3.setMaximumSize(QSize(256, 256))
        self.lblImagenArticulo_3.setPixmap(QPixmap(u":/Icons/PNG/paquete.png"))
        self.lblImagenArticulo_3.setScaledContents(True)

        self.gridLayout_23.addWidget(self.lblImagenArticulo_3, 2, 0, 1, 1)

        self.lblImagenArticulo_4 = QLabel(self.tab_imagenes)
        self.lblImagenArticulo_4.setObjectName(u"lblImagenArticulo_4")
        sizePolicy5.setHeightForWidth(self.lblImagenArticulo_4.sizePolicy().hasHeightForWidth())
        self.lblImagenArticulo_4.setSizePolicy(sizePolicy5)
        self.lblImagenArticulo_4.setMaximumSize(QSize(256, 256))
        self.lblImagenArticulo_4.setPixmap(QPixmap(u":/Icons/PNG/paquete.png"))
        self.lblImagenArticulo_4.setScaledContents(True)

        self.gridLayout_23.addWidget(self.lblImagenArticulo_4, 2, 1, 1, 1)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.botCambiarImagen_3 = QPushButton(self.tab_imagenes)
        self.botCambiarImagen_3.setObjectName(u"botCambiarImagen_3")
        self.botCambiarImagen_3.setEnabled(False)
        self.botCambiarImagen_3.setMaximumSize(QSize(256, 16777215))
        self.botCambiarImagen_3.setIcon(icon15)
        self.botCambiarImagen_3.setIconSize(QSize(32, 32))

        self.horizontalLayout_9.addWidget(self.botCambiarImagen_3)

        self.btnBorrarImagen_3 = QPushButton(self.tab_imagenes)
        self.btnBorrarImagen_3.setObjectName(u"btnBorrarImagen_3")
        self.btnBorrarImagen_3.setEnabled(False)
        self.btnBorrarImagen_3.setMaximumSize(QSize(100, 16777215))
        self.btnBorrarImagen_3.setIcon(icon14)
        self.btnBorrarImagen_3.setIconSize(QSize(32, 32))

        self.horizontalLayout_9.addWidget(self.btnBorrarImagen_3)


        self.gridLayout_23.addLayout(self.horizontalLayout_9, 3, 0, 1, 1)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.botCambiarImagen_4 = QPushButton(self.tab_imagenes)
        self.botCambiarImagen_4.setObjectName(u"botCambiarImagen_4")
        self.botCambiarImagen_4.setEnabled(False)
        self.botCambiarImagen_4.setIcon(icon15)
        self.botCambiarImagen_4.setIconSize(QSize(32, 32))

        self.horizontalLayout_11.addWidget(self.botCambiarImagen_4)

        self.btnBorrarimagen_4 = QPushButton(self.tab_imagenes)
        self.btnBorrarimagen_4.setObjectName(u"btnBorrarimagen_4")
        self.btnBorrarimagen_4.setEnabled(False)
        self.btnBorrarimagen_4.setMaximumSize(QSize(100, 16777215))
        self.btnBorrarimagen_4.setIcon(icon14)
        self.btnBorrarimagen_4.setIconSize(QSize(32, 32))

        self.horizontalLayout_11.addWidget(self.btnBorrarimagen_4)


        self.gridLayout_23.addLayout(self.horizontalLayout_11, 3, 1, 1, 1)

        self.Pestanas.addTab(self.tab_imagenes, "")
        self.tab_estadistica = QWidget()
        self.tab_estadistica.setObjectName(u"tab_estadistica")
        self.gridLayout_37 = QGridLayout(self.tab_estadistica)
        self.gridLayout_37.setObjectName(u"gridLayout_37")
        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_37.addItem(self.verticalSpacer_4, 5, 0, 1, 1)

        self.frame = QFrame(self.tab_estadistica)
        self.frame.setObjectName(u"frame")
        self.gridLayout_12 = QGridLayout(self.frame)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.txtunidades_vendidas = QLineEdit(self.frame)
        self.txtunidades_vendidas.setObjectName(u"txtunidades_vendidas")
        self.txtunidades_vendidas.setEnabled(True)
        sizePolicy3.setHeightForWidth(self.txtunidades_vendidas.sizePolicy().hasHeightForWidth())
        self.txtunidades_vendidas.setSizePolicy(sizePolicy3)
        self.txtunidades_vendidas.setMaximumSize(QSize(120, 27))
        self.txtunidades_vendidas.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_12.addWidget(self.txtunidades_vendidas, 0, 3, 1, 1)

        self.label_29 = QLabel(self.frame)
        self.label_29.setObjectName(u"label_29")

        self.gridLayout_12.addWidget(self.label_29, 0, 2, 1, 1)

        self.label_28 = QLabel(self.frame)
        self.label_28.setObjectName(u"label_28")

        self.gridLayout_12.addWidget(self.label_28, 0, 0, 1, 1)

        self.txtunidades_compradas = QLineEdit(self.frame)
        self.txtunidades_compradas.setObjectName(u"txtunidades_compradas")
        self.txtunidades_compradas.setEnabled(True)
        sizePolicy.setHeightForWidth(self.txtunidades_compradas.sizePolicy().hasHeightForWidth())
        self.txtunidades_compradas.setSizePolicy(sizePolicy)
        self.txtunidades_compradas.setMaximumSize(QSize(120, 27))
        self.txtunidades_compradas.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_12.addWidget(self.txtunidades_compradas, 0, 1, 1, 1)

        self.label_42 = QLabel(self.frame)
        self.label_42.setObjectName(u"label_42")

        self.gridLayout_12.addWidget(self.label_42, 1, 0, 1, 1)

        self.txtfecha_fecha_ultima_compra = QDateEdit(self.frame)
        self.txtfecha_fecha_ultima_compra.setObjectName(u"txtfecha_fecha_ultima_compra")
        self.txtfecha_fecha_ultima_compra.setEnabled(True)
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.txtfecha_fecha_ultima_compra.sizePolicy().hasHeightForWidth())
        self.txtfecha_fecha_ultima_compra.setSizePolicy(sizePolicy6)
        self.txtfecha_fecha_ultima_compra.setMaximumSize(QSize(120, 27))
        self.txtfecha_fecha_ultima_compra.setDateTime(QDateTime(QDate(2000, 9, 13), QTime(0, 0, 0)))
        self.txtfecha_fecha_ultima_compra.setMinimumDateTime(QDateTime(QDate(1900, 9, 13), QTime(0, 0, 0)))
        self.txtfecha_fecha_ultima_compra.setCalendarPopup(True)
        self.txtfecha_fecha_ultima_compra.setDate(QDate(2000, 9, 13))

        self.gridLayout_12.addWidget(self.txtfecha_fecha_ultima_compra, 2, 1, 1, 1)

        self.txtimporte_acumulado_compras = QLineEdit(self.frame)
        self.txtimporte_acumulado_compras.setObjectName(u"txtimporte_acumulado_compras")
        self.txtimporte_acumulado_compras.setEnabled(True)
        sizePolicy3.setHeightForWidth(self.txtimporte_acumulado_compras.sizePolicy().hasHeightForWidth())
        self.txtimporte_acumulado_compras.setSizePolicy(sizePolicy3)
        self.txtimporte_acumulado_compras.setMaximumSize(QSize(120, 27))
        self.txtimporte_acumulado_compras.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_12.addWidget(self.txtimporte_acumulado_compras, 1, 1, 1, 1)

        self.label_43 = QLabel(self.frame)
        self.label_43.setObjectName(u"label_43")

        self.gridLayout_12.addWidget(self.label_43, 1, 2, 1, 1)

        self.txtimporte_acumulado_ventas = QLineEdit(self.frame)
        self.txtimporte_acumulado_ventas.setObjectName(u"txtimporte_acumulado_ventas")
        self.txtimporte_acumulado_ventas.setEnabled(True)
        sizePolicy3.setHeightForWidth(self.txtimporte_acumulado_ventas.sizePolicy().hasHeightForWidth())
        self.txtimporte_acumulado_ventas.setSizePolicy(sizePolicy3)
        self.txtimporte_acumulado_ventas.setMaximumSize(QSize(120, 27))
        self.txtimporte_acumulado_ventas.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_12.addWidget(self.txtimporte_acumulado_ventas, 1, 3, 1, 1)

        self.lblFechaCompra = QLabel(self.frame)
        self.lblFechaCompra.setObjectName(u"lblFechaCompra")

        self.gridLayout_12.addWidget(self.lblFechaCompra, 2, 0, 1, 1)

        self.lblFechaVenta = QLabel(self.frame)
        self.lblFechaVenta.setObjectName(u"lblFechaVenta")

        self.gridLayout_12.addWidget(self.lblFechaVenta, 2, 2, 1, 1)

        self.txtfechaUltimaVenta = QDateEdit(self.frame)
        self.txtfechaUltimaVenta.setObjectName(u"txtfechaUltimaVenta")
        self.txtfechaUltimaVenta.setEnabled(True)
        self.txtfechaUltimaVenta.setMaximumSize(QSize(120, 27))
        self.txtfechaUltimaVenta.setCalendarPopup(True)

        self.gridLayout_12.addWidget(self.txtfechaUltimaVenta, 2, 3, 1, 1)


        self.gridLayout_37.addWidget(self.frame, 0, 0, 1, 1)

        self.btnResArt2 = QPushButton(self.tab_estadistica)
        self.btnResArt2.setObjectName(u"btnResArt2")

        self.gridLayout_37.addWidget(self.btnResArt2, 3, 0, 1, 1)

        self.frame_6 = QFrame(self.tab_estadistica)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_33 = QGridLayout(self.frame_6)
        self.gridLayout_33.setObjectName(u"gridLayout_33")
        self.txtstock_fisico_almacen = QLineEdit(self.frame_6)
        self.txtstock_fisico_almacen.setObjectName(u"txtstock_fisico_almacen")
        self.txtstock_fisico_almacen.setMaximumSize(QSize(120, 27))
        self.txtstock_fisico_almacen.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_33.addWidget(self.txtstock_fisico_almacen, 1, 1, 1, 1)

        self.label_30 = QLabel(self.frame_6)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setAutoFillBackground(False)

        self.gridLayout_33.addWidget(self.label_30, 0, 0, 1, 1)

        self.label_22 = QLabel(self.frame_6)
        self.label_22.setObjectName(u"label_22")

        self.gridLayout_33.addWidget(self.label_22, 1, 0, 1, 1)

        self.txtstock_minimo = QLineEdit(self.frame_6)
        self.txtstock_minimo.setObjectName(u"txtstock_minimo")
        sizePolicy3.setHeightForWidth(self.txtstock_minimo.sizePolicy().hasHeightForWidth())
        self.txtstock_minimo.setSizePolicy(sizePolicy3)
        self.txtstock_minimo.setMaximumSize(QSize(120, 27))
        self.txtstock_minimo.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_33.addWidget(self.txtstock_minimo, 0, 1, 1, 1)

        self.label_31 = QLabel(self.frame_6)
        self.label_31.setObjectName(u"label_31")

        self.gridLayout_33.addWidget(self.label_31, 0, 2, 1, 1)

        self.txtstock_maximo = QLineEdit(self.frame_6)
        self.txtstock_maximo.setObjectName(u"txtstock_maximo")
        sizePolicy3.setHeightForWidth(self.txtstock_maximo.sizePolicy().hasHeightForWidth())
        self.txtstock_maximo.setSizePolicy(sizePolicy3)
        self.txtstock_maximo.setMaximumSize(QSize(120, 27))
        self.txtstock_maximo.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_33.addWidget(self.txtstock_maximo, 0, 5, 1, 1)

        self.label_44 = QLabel(self.frame_6)
        self.label_44.setObjectName(u"label_44")

        self.gridLayout_33.addWidget(self.label_44, 2, 0, 1, 1)

        self.txtcantidad_pendiente_recibir = QLineEdit(self.frame_6)
        self.txtcantidad_pendiente_recibir.setObjectName(u"txtcantidad_pendiente_recibir")
        self.txtcantidad_pendiente_recibir.setEnabled(True)
        sizePolicy3.setHeightForWidth(self.txtcantidad_pendiente_recibir.sizePolicy().hasHeightForWidth())
        self.txtcantidad_pendiente_recibir.setSizePolicy(sizePolicy3)
        self.txtcantidad_pendiente_recibir.setMaximumSize(QSize(120, 27))
        self.txtcantidad_pendiente_recibir.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_33.addWidget(self.txtcantidad_pendiente_recibir, 2, 1, 1, 1)

        self.txtstock_real_2 = QLineEdit(self.frame_6)
        self.txtstock_real_2.setObjectName(u"txtstock_real_2")
        self.txtstock_real_2.setEnabled(True)
        sizePolicy3.setHeightForWidth(self.txtstock_real_2.sizePolicy().hasHeightForWidth())
        self.txtstock_real_2.setSizePolicy(sizePolicy3)
        self.txtstock_real_2.setMinimumSize(QSize(0, 27))
        self.txtstock_real_2.setMaximumSize(QSize(120, 27))
        self.txtstock_real_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_33.addWidget(self.txtstock_real_2, 4, 1, 1, 1)

        self.label_32 = QLabel(self.frame_6)
        self.label_32.setObjectName(u"label_32")

        self.gridLayout_33.addWidget(self.label_32, 4, 0, 1, 1)

        self.label_45 = QLabel(self.frame_6)
        self.label_45.setObjectName(u"label_45")

        self.gridLayout_33.addWidget(self.label_45, 3, 0, 1, 1)

        self.txtunidades_reservadas = QLineEdit(self.frame_6)
        self.txtunidades_reservadas.setObjectName(u"txtunidades_reservadas")
        self.txtunidades_reservadas.setEnabled(True)
        sizePolicy3.setHeightForWidth(self.txtunidades_reservadas.sizePolicy().hasHeightForWidth())
        self.txtunidades_reservadas.setSizePolicy(sizePolicy3)
        self.txtunidades_reservadas.setMaximumSize(QSize(120, 27))
        self.txtunidades_reservadas.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_33.addWidget(self.txtunidades_reservadas, 3, 1, 1, 1)

        self.lblFechaPrevistaRecepcion = QLabel(self.frame_6)
        self.lblFechaPrevistaRecepcion.setObjectName(u"lblFechaPrevistaRecepcion")

        self.gridLayout_33.addWidget(self.lblFechaPrevistaRecepcion, 2, 2, 1, 1)

        self.txtfecha_prevista_recepcion = QDateEdit(self.frame_6)
        self.txtfecha_prevista_recepcion.setObjectName(u"txtfecha_prevista_recepcion")
        self.txtfecha_prevista_recepcion.setEnabled(True)
        sizePolicy6.setHeightForWidth(self.txtfecha_prevista_recepcion.sizePolicy().hasHeightForWidth())
        self.txtfecha_prevista_recepcion.setSizePolicy(sizePolicy6)
        self.txtfecha_prevista_recepcion.setMaximumSize(QSize(120, 27))
        self.txtfecha_prevista_recepcion.setMaximumDateTime(QDateTime(QDate(7999, 12, 31), QTime(23, 59, 59)))
        self.txtfecha_prevista_recepcion.setCalendarPopup(True)

        self.gridLayout_33.addWidget(self.txtfecha_prevista_recepcion, 2, 5, 1, 1)


        self.gridLayout_37.addWidget(self.frame_6, 1, 0, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_37.addItem(self.horizontalSpacer_3, 1, 1, 1, 1)

        self.btnResArt = QPushButton(self.tab_estadistica)
        self.btnResArt.setObjectName(u"btnResArt")

        self.gridLayout_37.addWidget(self.btnResArt, 4, 0, 1, 1)

        self.Pestanas.addTab(self.tab_estadistica, "")
        self.tab_grafica = QWidget()
        self.tab_grafica.setObjectName(u"tab_grafica")
        self.gridLayout_3 = QGridLayout(self.tab_grafica)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.frame_9 = QFrame(self.tab_grafica)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_9)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.ChartViewWidget = ChartViewWidget(self.frame_9)
        self.ChartViewWidget.setObjectName(u"ChartViewWidget")

        self.verticalLayout_3.addWidget(self.ChartViewWidget)

        self.cboTipoGrafica = QComboBox(self.frame_9)
        self.cboTipoGrafica.addItem("")
        self.cboTipoGrafica.addItem("")
        self.cboTipoGrafica.setObjectName(u"cboTipoGrafica")

        self.verticalLayout_3.addWidget(self.cboTipoGrafica)

        self.radGrafica_unidades = QRadioButton(self.frame_9)
        self.radGrafica_unidades.setObjectName(u"radGrafica_unidades")
        self.radGrafica_unidades.setChecked(True)

        self.verticalLayout_3.addWidget(self.radGrafica_unidades)

        self.radGrafica_importes = QRadioButton(self.frame_9)
        self.radGrafica_importes.setObjectName(u"radGrafica_importes")

        self.verticalLayout_3.addWidget(self.radGrafica_importes)

        self.chkValorGrafica = QCheckBox(self.frame_9)
        self.chkValorGrafica.setObjectName(u"chkValorGrafica")
        self.chkValorGrafica.setAutoFillBackground(False)
        self.chkValorGrafica.setChecked(True)

        self.verticalLayout_3.addWidget(self.chkValorGrafica)


        self.gridLayout_3.addWidget(self.frame_9, 0, 0, 1, 1)

        self.cajaValores = QFrame(self.tab_grafica)
        self.cajaValores.setObjectName(u"cajaValores")
        self.cajaValores.setMinimumSize(QSize(512, 0))
        self.cajaValores.setFrameShape(QFrame.Shape.StyledPanel)
        self.cajaValores.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_22 = QGridLayout(self.cajaValores)
        self.gridLayout_22.setObjectName(u"gridLayout_22")
        self.frame_14 = QFrame(self.cajaValores)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setStyleSheet(u"")
        self.frame_14.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_14.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_18 = QGridLayout(self.frame_14)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.label_25 = QLabel(self.frame_14)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setStyleSheet(u"")

        self.gridLayout_18.addWidget(self.label_25, 0, 0, 1, 1)

        self.gridLayout_20 = QGridLayout()
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.txtImporte_compras_enero = QLineEdit(self.frame_14)
        self.txtImporte_compras_enero.setObjectName(u"txtImporte_compras_enero")
        self.txtImporte_compras_enero.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_compras_enero.setStyleSheet(u"")
        self.txtImporte_compras_enero.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_20.addWidget(self.txtImporte_compras_enero, 1, 2, 1, 1)

        self.txtImporte_compras_julio = QLineEdit(self.frame_14)
        self.txtImporte_compras_julio.setObjectName(u"txtImporte_compras_julio")
        self.txtImporte_compras_julio.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_compras_julio.setStyleSheet(u"")
        self.txtImporte_compras_julio.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_20.addWidget(self.txtImporte_compras_julio, 7, 2, 1, 1)

        self.txtImporte_compras_marzo = QLineEdit(self.frame_14)
        self.txtImporte_compras_marzo.setObjectName(u"txtImporte_compras_marzo")
        self.txtImporte_compras_marzo.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_compras_marzo.setStyleSheet(u"")
        self.txtImporte_compras_marzo.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_20.addWidget(self.txtImporte_compras_marzo, 3, 2, 1, 1)

        self.txtUnid_compras_febrero = QLineEdit(self.frame_14)
        self.txtUnid_compras_febrero.setObjectName(u"txtUnid_compras_febrero")
        self.txtUnid_compras_febrero.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_compras_febrero.setStyleSheet(u"")
        self.txtUnid_compras_febrero.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_20.addWidget(self.txtUnid_compras_febrero, 2, 1, 1, 1)

        self.txtUnid_compras_marzo = QLineEdit(self.frame_14)
        self.txtUnid_compras_marzo.setObjectName(u"txtUnid_compras_marzo")
        self.txtUnid_compras_marzo.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_compras_marzo.setStyleSheet(u"")
        self.txtUnid_compras_marzo.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_20.addWidget(self.txtUnid_compras_marzo, 3, 1, 1, 1)

        self.txtImporte_compras_septiembre = QLineEdit(self.frame_14)
        self.txtImporte_compras_septiembre.setObjectName(u"txtImporte_compras_septiembre")
        self.txtImporte_compras_septiembre.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_compras_septiembre.setStyleSheet(u"")
        self.txtImporte_compras_septiembre.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_20.addWidget(self.txtImporte_compras_septiembre, 9, 2, 1, 1)

        self.label_52 = QLabel(self.frame_14)
        self.label_52.setObjectName(u"label_52")
        self.label_52.setStyleSheet(u"")

        self.gridLayout_20.addWidget(self.label_52, 0, 1, 1, 1)

        self.txtImporte_compras_diciembre = QLineEdit(self.frame_14)
        self.txtImporte_compras_diciembre.setObjectName(u"txtImporte_compras_diciembre")
        self.txtImporte_compras_diciembre.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_compras_diciembre.setStyleSheet(u"")
        self.txtImporte_compras_diciembre.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_20.addWidget(self.txtImporte_compras_diciembre, 12, 2, 1, 1)

        self.txtUnid_compras_agosto = QLineEdit(self.frame_14)
        self.txtUnid_compras_agosto.setObjectName(u"txtUnid_compras_agosto")
        self.txtUnid_compras_agosto.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_compras_agosto.setStyleSheet(u"")
        self.txtUnid_compras_agosto.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_20.addWidget(self.txtUnid_compras_agosto, 8, 1, 1, 1)

        self.txtUnid_compras_diciembre = QLineEdit(self.frame_14)
        self.txtUnid_compras_diciembre.setObjectName(u"txtUnid_compras_diciembre")
        self.txtUnid_compras_diciembre.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_compras_diciembre.setStyleSheet(u"")
        self.txtUnid_compras_diciembre.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_20.addWidget(self.txtUnid_compras_diciembre, 12, 1, 1, 1)

        self.txtUnid_compras_junio = QLineEdit(self.frame_14)
        self.txtUnid_compras_junio.setObjectName(u"txtUnid_compras_junio")
        self.txtUnid_compras_junio.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_compras_junio.setStyleSheet(u"")
        self.txtUnid_compras_junio.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_20.addWidget(self.txtUnid_compras_junio, 6, 1, 1, 1)

        self.txtUnid_compras_mayo = QLineEdit(self.frame_14)
        self.txtUnid_compras_mayo.setObjectName(u"txtUnid_compras_mayo")
        self.txtUnid_compras_mayo.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_compras_mayo.setStyleSheet(u"")
        self.txtUnid_compras_mayo.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_20.addWidget(self.txtUnid_compras_mayo, 5, 1, 1, 1)

        self.txtUnid_compras_enero = QLineEdit(self.frame_14)
        self.txtUnid_compras_enero.setObjectName(u"txtUnid_compras_enero")
        self.txtUnid_compras_enero.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_compras_enero.setStyleSheet(u"")
        self.txtUnid_compras_enero.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_20.addWidget(self.txtUnid_compras_enero, 1, 1, 1, 1)

        self.txtImporte_compras_octubre = QLineEdit(self.frame_14)
        self.txtImporte_compras_octubre.setObjectName(u"txtImporte_compras_octubre")
        self.txtImporte_compras_octubre.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_compras_octubre.setStyleSheet(u"")
        self.txtImporte_compras_octubre.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_20.addWidget(self.txtImporte_compras_octubre, 10, 2, 1, 1)

        self.txtImporte_compras_noviembre = QLineEdit(self.frame_14)
        self.txtImporte_compras_noviembre.setObjectName(u"txtImporte_compras_noviembre")
        self.txtImporte_compras_noviembre.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_compras_noviembre.setStyleSheet(u"")
        self.txtImporte_compras_noviembre.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_20.addWidget(self.txtImporte_compras_noviembre, 11, 2, 1, 1)

        self.txtUnid_compras_noviembre = QLineEdit(self.frame_14)
        self.txtUnid_compras_noviembre.setObjectName(u"txtUnid_compras_noviembre")
        self.txtUnid_compras_noviembre.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_compras_noviembre.setStyleSheet(u"")
        self.txtUnid_compras_noviembre.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_20.addWidget(self.txtUnid_compras_noviembre, 11, 1, 1, 1)

        self.txtImporte_compras_agosto = QLineEdit(self.frame_14)
        self.txtImporte_compras_agosto.setObjectName(u"txtImporte_compras_agosto")
        self.txtImporte_compras_agosto.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_compras_agosto.setStyleSheet(u"")
        self.txtImporte_compras_agosto.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_20.addWidget(self.txtImporte_compras_agosto, 8, 2, 1, 1)

        self.txtImporte_compras_mayo = QLineEdit(self.frame_14)
        self.txtImporte_compras_mayo.setObjectName(u"txtImporte_compras_mayo")
        self.txtImporte_compras_mayo.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_compras_mayo.setStyleSheet(u"")
        self.txtImporte_compras_mayo.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_20.addWidget(self.txtImporte_compras_mayo, 5, 2, 1, 1)

        self.txtUnid_compras_septiembre = QLineEdit(self.frame_14)
        self.txtUnid_compras_septiembre.setObjectName(u"txtUnid_compras_septiembre")
        self.txtUnid_compras_septiembre.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_compras_septiembre.setStyleSheet(u"")
        self.txtUnid_compras_septiembre.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_20.addWidget(self.txtUnid_compras_septiembre, 9, 1, 1, 1)

        self.txtImporte_compras_febrero = QLineEdit(self.frame_14)
        self.txtImporte_compras_febrero.setObjectName(u"txtImporte_compras_febrero")
        self.txtImporte_compras_febrero.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_compras_febrero.setStyleSheet(u"")
        self.txtImporte_compras_febrero.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_20.addWidget(self.txtImporte_compras_febrero, 2, 2, 1, 1)

        self.txtUnid_compras_abril = QLineEdit(self.frame_14)
        self.txtUnid_compras_abril.setObjectName(u"txtUnid_compras_abril")
        self.txtUnid_compras_abril.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_compras_abril.setStyleSheet(u"")
        self.txtUnid_compras_abril.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_20.addWidget(self.txtUnid_compras_abril, 4, 1, 1, 1)

        self.txtImporte_compras_abril = QLineEdit(self.frame_14)
        self.txtImporte_compras_abril.setObjectName(u"txtImporte_compras_abril")
        self.txtImporte_compras_abril.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_compras_abril.setStyleSheet(u"")
        self.txtImporte_compras_abril.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_20.addWidget(self.txtImporte_compras_abril, 4, 2, 1, 1)

        self.label_53 = QLabel(self.frame_14)
        self.label_53.setObjectName(u"label_53")
        self.label_53.setStyleSheet(u"")

        self.gridLayout_20.addWidget(self.label_53, 0, 2, 1, 1)

        self.txtUnid_compras_julio = QLineEdit(self.frame_14)
        self.txtUnid_compras_julio.setObjectName(u"txtUnid_compras_julio")
        self.txtUnid_compras_julio.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_compras_julio.setStyleSheet(u"")
        self.txtUnid_compras_julio.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_20.addWidget(self.txtUnid_compras_julio, 7, 1, 1, 1)

        self.txtImporte_compras_junio = QLineEdit(self.frame_14)
        self.txtImporte_compras_junio.setObjectName(u"txtImporte_compras_junio")
        self.txtImporte_compras_junio.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_compras_junio.setStyleSheet(u"")
        self.txtImporte_compras_junio.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_20.addWidget(self.txtImporte_compras_junio, 6, 2, 1, 1)

        self.txtUnid_compras_octubre = QLineEdit(self.frame_14)
        self.txtUnid_compras_octubre.setObjectName(u"txtUnid_compras_octubre")
        self.txtUnid_compras_octubre.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_compras_octubre.setStyleSheet(u"")
        self.txtUnid_compras_octubre.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_20.addWidget(self.txtUnid_compras_octubre, 10, 1, 1, 1)

        self.label_27 = QLabel(self.frame_14)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setStyleSheet(u"")

        self.gridLayout_20.addWidget(self.label_27, 1, 0, 1, 1)

        self.label_35 = QLabel(self.frame_14)
        self.label_35.setObjectName(u"label_35")
        self.label_35.setStyleSheet(u"")

        self.gridLayout_20.addWidget(self.label_35, 2, 0, 1, 1)

        self.label_36 = QLabel(self.frame_14)
        self.label_36.setObjectName(u"label_36")
        self.label_36.setStyleSheet(u"")

        self.gridLayout_20.addWidget(self.label_36, 3, 0, 1, 1)

        self.label_37 = QLabel(self.frame_14)
        self.label_37.setObjectName(u"label_37")
        self.label_37.setStyleSheet(u"")

        self.gridLayout_20.addWidget(self.label_37, 4, 0, 1, 1)

        self.label_39 = QLabel(self.frame_14)
        self.label_39.setObjectName(u"label_39")
        self.label_39.setStyleSheet(u"")

        self.gridLayout_20.addWidget(self.label_39, 5, 0, 1, 1)

        self.label_40 = QLabel(self.frame_14)
        self.label_40.setObjectName(u"label_40")
        self.label_40.setStyleSheet(u"")

        self.gridLayout_20.addWidget(self.label_40, 6, 0, 1, 1)

        self.label_41 = QLabel(self.frame_14)
        self.label_41.setObjectName(u"label_41")
        self.label_41.setStyleSheet(u"")

        self.gridLayout_20.addWidget(self.label_41, 7, 0, 1, 1)

        self.label_46 = QLabel(self.frame_14)
        self.label_46.setObjectName(u"label_46")
        self.label_46.setStyleSheet(u"")

        self.gridLayout_20.addWidget(self.label_46, 8, 0, 1, 1)

        self.label_47 = QLabel(self.frame_14)
        self.label_47.setObjectName(u"label_47")
        self.label_47.setStyleSheet(u"")

        self.gridLayout_20.addWidget(self.label_47, 9, 0, 1, 1)

        self.label_48 = QLabel(self.frame_14)
        self.label_48.setObjectName(u"label_48")
        self.label_48.setStyleSheet(u"")

        self.gridLayout_20.addWidget(self.label_48, 10, 0, 1, 1)

        self.label_49 = QLabel(self.frame_14)
        self.label_49.setObjectName(u"label_49")
        self.label_49.setStyleSheet(u"")

        self.gridLayout_20.addWidget(self.label_49, 11, 0, 1, 1)

        self.label_50 = QLabel(self.frame_14)
        self.label_50.setObjectName(u"label_50")
        self.label_50.setStyleSheet(u"")

        self.gridLayout_20.addWidget(self.label_50, 12, 0, 1, 1)


        self.gridLayout_18.addLayout(self.gridLayout_20, 1, 0, 2, 3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_18.addItem(self.verticalSpacer, 3, 0, 1, 1)


        self.gridLayout_22.addWidget(self.frame_14, 0, 0, 1, 1)

        self.frame_15 = QFrame(self.cajaValores)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setStyleSheet(u"")
        self.frame_15.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_15.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_19 = QGridLayout(self.frame_15)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.label_26 = QLabel(self.frame_15)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setStyleSheet(u"")

        self.gridLayout_19.addWidget(self.label_26, 0, 0, 1, 1)

        self.gridLayout_21 = QGridLayout()
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.label_54 = QLabel(self.frame_15)
        self.label_54.setObjectName(u"label_54")
        self.label_54.setStyleSheet(u"")

        self.gridLayout_21.addWidget(self.label_54, 0, 0, 1, 1)

        self.label_55 = QLabel(self.frame_15)
        self.label_55.setObjectName(u"label_55")
        self.label_55.setStyleSheet(u"")

        self.gridLayout_21.addWidget(self.label_55, 0, 1, 1, 1)

        self.txtUnid_ventas_enero = QLineEdit(self.frame_15)
        self.txtUnid_ventas_enero.setObjectName(u"txtUnid_ventas_enero")
        self.txtUnid_ventas_enero.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_ventas_enero.setStyleSheet(u"")
        self.txtUnid_ventas_enero.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_21.addWidget(self.txtUnid_ventas_enero, 1, 0, 1, 1)

        self.txtImporte_ventas_enero = QLineEdit(self.frame_15)
        self.txtImporte_ventas_enero.setObjectName(u"txtImporte_ventas_enero")
        self.txtImporte_ventas_enero.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_ventas_enero.setStyleSheet(u"")
        self.txtImporte_ventas_enero.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_21.addWidget(self.txtImporte_ventas_enero, 1, 1, 1, 1)

        self.txtUnid_ventas_febrero = QLineEdit(self.frame_15)
        self.txtUnid_ventas_febrero.setObjectName(u"txtUnid_ventas_febrero")
        self.txtUnid_ventas_febrero.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_ventas_febrero.setStyleSheet(u"")
        self.txtUnid_ventas_febrero.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_21.addWidget(self.txtUnid_ventas_febrero, 2, 0, 1, 1)

        self.txtImporte_ventas_febrero = QLineEdit(self.frame_15)
        self.txtImporte_ventas_febrero.setObjectName(u"txtImporte_ventas_febrero")
        self.txtImporte_ventas_febrero.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_ventas_febrero.setStyleSheet(u"")
        self.txtImporte_ventas_febrero.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_21.addWidget(self.txtImporte_ventas_febrero, 2, 1, 1, 1)

        self.txtUnid_ventas_marzo = QLineEdit(self.frame_15)
        self.txtUnid_ventas_marzo.setObjectName(u"txtUnid_ventas_marzo")
        self.txtUnid_ventas_marzo.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_ventas_marzo.setStyleSheet(u"")
        self.txtUnid_ventas_marzo.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_21.addWidget(self.txtUnid_ventas_marzo, 3, 0, 1, 1)

        self.txtImporte_ventas_marzo = QLineEdit(self.frame_15)
        self.txtImporte_ventas_marzo.setObjectName(u"txtImporte_ventas_marzo")
        self.txtImporte_ventas_marzo.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_ventas_marzo.setStyleSheet(u"")
        self.txtImporte_ventas_marzo.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_21.addWidget(self.txtImporte_ventas_marzo, 3, 1, 1, 1)

        self.txtUnid_ventas_abril = QLineEdit(self.frame_15)
        self.txtUnid_ventas_abril.setObjectName(u"txtUnid_ventas_abril")
        self.txtUnid_ventas_abril.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_ventas_abril.setStyleSheet(u"")
        self.txtUnid_ventas_abril.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_21.addWidget(self.txtUnid_ventas_abril, 4, 0, 1, 1)

        self.txtImporte_ventas_abril = QLineEdit(self.frame_15)
        self.txtImporte_ventas_abril.setObjectName(u"txtImporte_ventas_abril")
        self.txtImporte_ventas_abril.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_ventas_abril.setStyleSheet(u"")
        self.txtImporte_ventas_abril.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_21.addWidget(self.txtImporte_ventas_abril, 4, 1, 1, 1)

        self.txtUnid_ventas_mayo = QLineEdit(self.frame_15)
        self.txtUnid_ventas_mayo.setObjectName(u"txtUnid_ventas_mayo")
        self.txtUnid_ventas_mayo.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_ventas_mayo.setStyleSheet(u"")
        self.txtUnid_ventas_mayo.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_21.addWidget(self.txtUnid_ventas_mayo, 5, 0, 1, 1)

        self.txtImporte_ventas_mayo = QLineEdit(self.frame_15)
        self.txtImporte_ventas_mayo.setObjectName(u"txtImporte_ventas_mayo")
        self.txtImporte_ventas_mayo.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_ventas_mayo.setStyleSheet(u"")
        self.txtImporte_ventas_mayo.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_21.addWidget(self.txtImporte_ventas_mayo, 5, 1, 1, 1)

        self.txtUnid_ventas_junio = QLineEdit(self.frame_15)
        self.txtUnid_ventas_junio.setObjectName(u"txtUnid_ventas_junio")
        self.txtUnid_ventas_junio.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_ventas_junio.setStyleSheet(u"")
        self.txtUnid_ventas_junio.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_21.addWidget(self.txtUnid_ventas_junio, 6, 0, 1, 1)

        self.txtImporte_ventas_junio = QLineEdit(self.frame_15)
        self.txtImporte_ventas_junio.setObjectName(u"txtImporte_ventas_junio")
        self.txtImporte_ventas_junio.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_ventas_junio.setStyleSheet(u"")
        self.txtImporte_ventas_junio.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_21.addWidget(self.txtImporte_ventas_junio, 6, 1, 1, 1)

        self.txtUnid_ventas_julio = QLineEdit(self.frame_15)
        self.txtUnid_ventas_julio.setObjectName(u"txtUnid_ventas_julio")
        self.txtUnid_ventas_julio.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_ventas_julio.setStyleSheet(u"")
        self.txtUnid_ventas_julio.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_21.addWidget(self.txtUnid_ventas_julio, 7, 0, 1, 1)

        self.txtImporte_ventas_julio = QLineEdit(self.frame_15)
        self.txtImporte_ventas_julio.setObjectName(u"txtImporte_ventas_julio")
        self.txtImporte_ventas_julio.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_ventas_julio.setStyleSheet(u"")
        self.txtImporte_ventas_julio.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_21.addWidget(self.txtImporte_ventas_julio, 7, 1, 1, 1)

        self.txtUnid_ventas_agosto = QLineEdit(self.frame_15)
        self.txtUnid_ventas_agosto.setObjectName(u"txtUnid_ventas_agosto")
        self.txtUnid_ventas_agosto.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_ventas_agosto.setStyleSheet(u"")
        self.txtUnid_ventas_agosto.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_21.addWidget(self.txtUnid_ventas_agosto, 8, 0, 1, 1)

        self.txtImporte_ventas_agosto = QLineEdit(self.frame_15)
        self.txtImporte_ventas_agosto.setObjectName(u"txtImporte_ventas_agosto")
        self.txtImporte_ventas_agosto.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_ventas_agosto.setStyleSheet(u"")
        self.txtImporte_ventas_agosto.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_21.addWidget(self.txtImporte_ventas_agosto, 8, 1, 1, 1)

        self.txtUnid_ventas_septiembre = QLineEdit(self.frame_15)
        self.txtUnid_ventas_septiembre.setObjectName(u"txtUnid_ventas_septiembre")
        self.txtUnid_ventas_septiembre.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_ventas_septiembre.setStyleSheet(u"")
        self.txtUnid_ventas_septiembre.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_21.addWidget(self.txtUnid_ventas_septiembre, 9, 0, 1, 1)

        self.txtImporte_ventas_septiembre = QLineEdit(self.frame_15)
        self.txtImporte_ventas_septiembre.setObjectName(u"txtImporte_ventas_septiembre")
        self.txtImporte_ventas_septiembre.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_ventas_septiembre.setStyleSheet(u"")
        self.txtImporte_ventas_septiembre.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_21.addWidget(self.txtImporte_ventas_septiembre, 9, 1, 1, 1)

        self.txtUnid_ventas_octubre = QLineEdit(self.frame_15)
        self.txtUnid_ventas_octubre.setObjectName(u"txtUnid_ventas_octubre")
        self.txtUnid_ventas_octubre.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_ventas_octubre.setStyleSheet(u"")
        self.txtUnid_ventas_octubre.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_21.addWidget(self.txtUnid_ventas_octubre, 10, 0, 1, 1)

        self.txtImporte_ventas_octubre = QLineEdit(self.frame_15)
        self.txtImporte_ventas_octubre.setObjectName(u"txtImporte_ventas_octubre")
        self.txtImporte_ventas_octubre.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_ventas_octubre.setStyleSheet(u"")
        self.txtImporte_ventas_octubre.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_21.addWidget(self.txtImporte_ventas_octubre, 10, 1, 1, 1)

        self.txtUnid_ventas_noviembre = QLineEdit(self.frame_15)
        self.txtUnid_ventas_noviembre.setObjectName(u"txtUnid_ventas_noviembre")
        self.txtUnid_ventas_noviembre.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_ventas_noviembre.setStyleSheet(u"")
        self.txtUnid_ventas_noviembre.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_21.addWidget(self.txtUnid_ventas_noviembre, 11, 0, 1, 1)

        self.txtImporte_ventas_noviembre = QLineEdit(self.frame_15)
        self.txtImporte_ventas_noviembre.setObjectName(u"txtImporte_ventas_noviembre")
        self.txtImporte_ventas_noviembre.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_ventas_noviembre.setStyleSheet(u"")
        self.txtImporte_ventas_noviembre.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_21.addWidget(self.txtImporte_ventas_noviembre, 11, 1, 1, 1)

        self.txtUnid_ventas_diciembre = QLineEdit(self.frame_15)
        self.txtUnid_ventas_diciembre.setObjectName(u"txtUnid_ventas_diciembre")
        self.txtUnid_ventas_diciembre.setMaximumSize(QSize(50, 16777215))
        self.txtUnid_ventas_diciembre.setStyleSheet(u"")
        self.txtUnid_ventas_diciembre.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_21.addWidget(self.txtUnid_ventas_diciembre, 12, 0, 1, 1)

        self.txtImporte_ventas_diciembre = QLineEdit(self.frame_15)
        self.txtImporte_ventas_diciembre.setObjectName(u"txtImporte_ventas_diciembre")
        self.txtImporte_ventas_diciembre.setMaximumSize(QSize(98, 16777215))
        self.txtImporte_ventas_diciembre.setStyleSheet(u"")
        self.txtImporte_ventas_diciembre.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_21.addWidget(self.txtImporte_ventas_diciembre, 12, 1, 1, 1)


        self.gridLayout_19.addLayout(self.gridLayout_21, 1, 0, 2, 3)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_19.addItem(self.verticalSpacer_2, 3, 0, 1, 1)


        self.gridLayout_22.addWidget(self.frame_15, 0, 1, 1, 1)


        self.gridLayout_3.addWidget(self.cajaValores, 0, 1, 1, 1)

        self.Pestanas.addTab(self.tab_grafica, "")

        self.gridLayout_2.addWidget(self.Pestanas, 1, 1, 1, 5)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.gridLayout_38 = QGridLayout(self.page_2)
        self.gridLayout_38.setObjectName(u"gridLayout_38")
        self.gridLayout_38.setContentsMargins(-1, -1, 20, -1)
        self.tablaBusqueda = QTableView(self.page_2)
        self.tablaBusqueda.setObjectName(u"tablaBusqueda")
        self.tablaBusqueda.setStyleSheet(u"alternate-\n"
"font: 8pt \"Sans\";")
        self.tablaBusqueda.setAlternatingRowColors(True)
        self.tablaBusqueda.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tablaBusqueda.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tablaBusqueda.horizontalHeader().setStretchLastSection(True)
        self.tablaBusqueda.verticalHeader().setVisible(False)

        self.gridLayout_38.addWidget(self.tablaBusqueda, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_2)

        self.gridLayout_10.addWidget(self.stackedWidget, 1, 0, 1, 5)

        self.label_70 = QLabel(FrmArticulos)
        self.label_70.setObjectName(u"label_70")
        self.label_70.setMaximumSize(QSize(16777215, 22))
        self.label_70.setStyleSheet(u"background: #304163;\n"
"color: rgb(255,255,255);\n"
"font: 14pt \"Sans Serif\";")
        self.label_70.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.label_70, 0, 0, 1, 5)

        QWidget.setTabOrder(self.botAnadir, self.botSiguiente)
        QWidget.setTabOrder(self.botSiguiente, self.botAnterior)
        QWidget.setTabOrder(self.botAnterior, self.btnBuscar)
        QWidget.setTabOrder(self.btnBuscar, self.botEditar)
        QWidget.setTabOrder(self.botEditar, self.botGuardar)
        QWidget.setTabOrder(self.botGuardar, self.botDeshacer)
        QWidget.setTabOrder(self.botDeshacer, self.botBorrar)
        QWidget.setTabOrder(self.botBorrar, self.btnExcepciones_3)
        QWidget.setTabOrder(self.btnExcepciones_3, self.btnKit)
        QWidget.setTabOrder(self.btnKit, self.btn_cerrar)
        QWidget.setTabOrder(self.btn_cerrar, self.Pestanas)
        QWidget.setTabOrder(self.Pestanas, self.txtcodigo)
        QWidget.setTabOrder(self.txtcodigo, self.txtcodigo_barras)
        QWidget.setTabOrder(self.txtcodigo_barras, self.txtcodigo_fabricante)
        QWidget.setTabOrder(self.txtcodigo_fabricante, self.txtdescripcionResumida)
        QWidget.setTabOrder(self.txtdescripcionResumida, self.txtcodigo_proveedor)
        QWidget.setTabOrder(self.txtcodigo_proveedor, self.txtproveedor)
        QWidget.setTabOrder(self.txtproveedor, self.btnBuscarProveedor)
        QWidget.setTabOrder(self.btnBuscarProveedor, self.cboTipoIVA)
        QWidget.setTabOrder(self.cboTipoIVA, self.txtcoste)
        QWidget.setTabOrder(self.txtcoste, self.chkmostrar_web)
        QWidget.setTabOrder(self.chkmostrar_web, self.chkcontrolar_stock)
        QWidget.setTabOrder(self.chkcontrolar_stock, self.txtCoste_real)
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
        QWidget.setTabOrder(self.btnAnadirDistribuidores, self.btnEditarDistribuidorFrecuente)
        QWidget.setTabOrder(self.btnEditarDistribuidorFrecuente, self.btnBorrarDistribuidores)
        QWidget.setTabOrder(self.btnBorrarDistribuidores, self.btnAsignarDistribuidor)
        QWidget.setTabOrder(self.btnAsignarDistribuidor, self.chkArticulo_promocionado)
        QWidget.setTabOrder(self.chkArticulo_promocionado, self.chkMostrar_en_cuadro)
        QWidget.setTabOrder(self.chkMostrar_en_cuadro, self.txtOferta_Fecha_ini)
        QWidget.setTabOrder(self.txtOferta_Fecha_ini, self.txtOferta_Fecha_fin)
        QWidget.setTabOrder(self.txtOferta_Fecha_fin, self.btnAnadir_oferta)
        QWidget.setTabOrder(self.btnAnadir_oferta, self.btnguardar_oferta)
        QWidget.setTabOrder(self.btnguardar_oferta, self.btnEditarOferta)
        QWidget.setTabOrder(self.btnEditarOferta, self.btnDeshacer_oferta)
        QWidget.setTabOrder(self.btnDeshacer_oferta, self.txtOferta_Descripcion_promocion)
        QWidget.setTabOrder(self.txtOferta_Descripcion_promocion, self.chkOferta_32)
        QWidget.setTabOrder(self.chkOferta_32, self.chkOferta_web)
        QWidget.setTabOrder(self.chkOferta_web, self.chkOferta_dto)
        QWidget.setTabOrder(self.chkOferta_dto, self.chkOferta_pvp)
        QWidget.setTabOrder(self.chkOferta_pvp, self.txtOferta_por_cada)
        QWidget.setTabOrder(self.txtOferta_por_cada, self.txtOfertaregalo_de)
        QWidget.setTabOrder(self.txtOfertaregalo_de, self.txtOfertaDtoOferta)
        QWidget.setTabOrder(self.txtOfertaDtoOferta, self.txtOferta_dto_web)
        QWidget.setTabOrder(self.txtOferta_dto_web, self.txtoferta_pvp_fijo)
        QWidget.setTabOrder(self.txtoferta_pvp_fijo, self.tabla_ofertas)
        QWidget.setTabOrder(self.tabla_ofertas, self.btnActivarOferta)
        QWidget.setTabOrder(self.btnActivarOferta, self.btnBorrar_oferta)
        QWidget.setTabOrder(self.btnBorrar_oferta, self.txtOferta_comentarios_promocion)
        QWidget.setTabOrder(self.txtOferta_comentarios_promocion, self.tablaPaises_web)
        QWidget.setTabOrder(self.tablaPaises_web, self.cboIdiomasweb)
        QWidget.setTabOrder(self.cboIdiomasweb, self.txtArticulowebidioma)
        QWidget.setTabOrder(self.txtArticulowebidioma, self.txtDescWebIdioma)
        QWidget.setTabOrder(self.txtDescWebIdioma, self.pushButton)
        QWidget.setTabOrder(self.pushButton, self.pushButton_2)
        QWidget.setTabOrder(self.pushButton_2, self.pushButton_3)
        QWidget.setTabOrder(self.pushButton_3, self.pushButton_4)
        QWidget.setTabOrder(self.pushButton_4, self.checkBox)
        QWidget.setTabOrder(self.checkBox, self.pushButton_5)
        QWidget.setTabOrder(self.pushButton_5, self.btnImg_web1_add)
        QWidget.setTabOrder(self.btnImg_web1_add, self.btnImg_web1_delete)
        QWidget.setTabOrder(self.btnImg_web1_delete, self.btnImg_web2_add)
        QWidget.setTabOrder(self.btnImg_web2_add, self.btnImg_web2_delete)
        QWidget.setTabOrder(self.btnImg_web2_delete, self.btnImg_web3_add)
        QWidget.setTabOrder(self.btnImg_web3_add, self.btnImg_web3_delete)
        QWidget.setTabOrder(self.btnImg_web3_delete, self.btnImg_web4_add)
        QWidget.setTabOrder(self.btnImg_web4_add, self.btnImg_web4_delete)
        QWidget.setTabOrder(self.btnImg_web4_delete, self.botCambiarImagen)
        QWidget.setTabOrder(self.botCambiarImagen, self.botCambiarImagen_2)
        QWidget.setTabOrder(self.botCambiarImagen_2, self.btnBorrarimagen_2)
        QWidget.setTabOrder(self.btnBorrarimagen_2, self.botCambiarImagen_3)
        QWidget.setTabOrder(self.botCambiarImagen_3, self.botCambiarImagen_4)
        QWidget.setTabOrder(self.botCambiarImagen_4, self.btnBorrarimagen_4)
        QWidget.setTabOrder(self.btnBorrarimagen_4, self.txtunidades_compradas)
        QWidget.setTabOrder(self.txtunidades_compradas, self.txtunidades_vendidas)
        QWidget.setTabOrder(self.txtunidades_vendidas, self.txtimporte_acumulado_compras)
        QWidget.setTabOrder(self.txtimporte_acumulado_compras, self.txtimporte_acumulado_ventas)
        QWidget.setTabOrder(self.txtimporte_acumulado_ventas, self.txtfecha_fecha_ultima_compra)
        QWidget.setTabOrder(self.txtfecha_fecha_ultima_compra, self.txtfechaUltimaVenta)
        QWidget.setTabOrder(self.txtfechaUltimaVenta, self.txtstock_minimo)
        QWidget.setTabOrder(self.txtstock_minimo, self.txtstock_maximo)
        QWidget.setTabOrder(self.txtstock_maximo, self.txtstock_fisico_almacen)
        QWidget.setTabOrder(self.txtstock_fisico_almacen, self.txtcantidad_pendiente_recibir)
        QWidget.setTabOrder(self.txtcantidad_pendiente_recibir, self.txtfecha_prevista_recepcion)
        QWidget.setTabOrder(self.txtfecha_prevista_recepcion, self.txtunidades_reservadas)
        QWidget.setTabOrder(self.txtunidades_reservadas, self.txtstock_real_2)
        QWidget.setTabOrder(self.txtstock_real_2, self.btnResArt2)
        QWidget.setTabOrder(self.btnResArt2, self.txtUnid_ventas_diciembre)
        QWidget.setTabOrder(self.txtUnid_ventas_diciembre, self.txtImporte_ventas_diciembre)
        QWidget.setTabOrder(self.txtImporte_ventas_diciembre, self.txtImporte_ventas_septiembre)
        QWidget.setTabOrder(self.txtImporte_ventas_septiembre, self.txtUnid_ventas_octubre)
        QWidget.setTabOrder(self.txtUnid_ventas_octubre, self.txtImporte_ventas_octubre)
        QWidget.setTabOrder(self.txtImporte_ventas_octubre, self.txtUnid_ventas_noviembre)
        QWidget.setTabOrder(self.txtUnid_ventas_noviembre, self.txtImporte_ventas_noviembre)
        QWidget.setTabOrder(self.txtImporte_ventas_noviembre, self.txtImporte_compras_mayo)
        QWidget.setTabOrder(self.txtImporte_compras_mayo, self.txtUnid_compras_septiembre)
        QWidget.setTabOrder(self.txtUnid_compras_septiembre, self.txtImporte_compras_febrero)
        QWidget.setTabOrder(self.txtImporte_compras_febrero, self.txtImporte_compras_abril)
        QWidget.setTabOrder(self.txtImporte_compras_abril, self.txtUnid_compras_abril)
        QWidget.setTabOrder(self.txtUnid_compras_abril, self.txtImporte_compras_agosto)
        QWidget.setTabOrder(self.txtImporte_compras_agosto, self.txtUnid_compras_julio)
        QWidget.setTabOrder(self.txtUnid_compras_julio, self.txtImporte_compras_junio)
        QWidget.setTabOrder(self.txtImporte_compras_junio, self.txtUnid_compras_octubre)
        QWidget.setTabOrder(self.txtUnid_compras_octubre, self.txtUnid_ventas_enero)
        QWidget.setTabOrder(self.txtUnid_ventas_enero, self.txtImporte_ventas_enero)
        QWidget.setTabOrder(self.txtImporte_ventas_enero, self.txtUnid_compras_noviembre)
        QWidget.setTabOrder(self.txtUnid_compras_noviembre, self.txtImporte_compras_julio)
        QWidget.setTabOrder(self.txtImporte_compras_julio, self.txtUnid_ventas_abril)
        QWidget.setTabOrder(self.txtUnid_ventas_abril, self.txtUnid_compras_marzo)
        QWidget.setTabOrder(self.txtUnid_compras_marzo, self.txtImporte_ventas_mayo)
        QWidget.setTabOrder(self.txtImporte_ventas_mayo, self.txtUnid_compras_febrero)
        QWidget.setTabOrder(self.txtUnid_compras_febrero, self.txtUnid_ventas_julio)
        QWidget.setTabOrder(self.txtUnid_ventas_julio, self.txtImporte_compras_enero)
        QWidget.setTabOrder(self.txtImporte_compras_enero, self.txtUnid_ventas_febrero)
        QWidget.setTabOrder(self.txtUnid_ventas_febrero, self.txtUnid_ventas_marzo)
        QWidget.setTabOrder(self.txtUnid_ventas_marzo, self.txtImporte_ventas_febrero)
        QWidget.setTabOrder(self.txtImporte_ventas_febrero, self.txtImporte_ventas_marzo)
        QWidget.setTabOrder(self.txtImporte_ventas_marzo, self.txtImporte_ventas_abril)
        QWidget.setTabOrder(self.txtImporte_ventas_abril, self.txtUnid_ventas_mayo)
        QWidget.setTabOrder(self.txtUnid_ventas_mayo, self.txtUnid_ventas_junio)
        QWidget.setTabOrder(self.txtUnid_ventas_junio, self.txtImporte_ventas_junio)
        QWidget.setTabOrder(self.txtImporte_ventas_junio, self.txtUnid_ventas_agosto)
        QWidget.setTabOrder(self.txtUnid_ventas_agosto, self.txtImporte_ventas_julio)
        QWidget.setTabOrder(self.txtImporte_ventas_julio, self.txtUnid_ventas_septiembre)
        QWidget.setTabOrder(self.txtUnid_ventas_septiembre, self.txtImporte_ventas_agosto)
        QWidget.setTabOrder(self.txtImporte_ventas_agosto, self.txtImporte_compras_marzo)
        QWidget.setTabOrder(self.txtImporte_compras_marzo, self.txtImporte_compras_septiembre)
        QWidget.setTabOrder(self.txtImporte_compras_septiembre, self.txtImporte_compras_diciembre)
        QWidget.setTabOrder(self.txtImporte_compras_diciembre, self.txtUnid_compras_agosto)
        QWidget.setTabOrder(self.txtUnid_compras_agosto, self.tablaBusqueda)
        QWidget.setTabOrder(self.tablaBusqueda, self.chkValorGrafica)
        QWidget.setTabOrder(self.chkValorGrafica, self.cboTipoGrafica)
        QWidget.setTabOrder(self.cboTipoGrafica, self.radGrafica_unidades)
        QWidget.setTabOrder(self.radGrafica_unidades, self.radGrafica_importes)
        QWidget.setTabOrder(self.radGrafica_importes, self.txtUnid_compras_diciembre)
        QWidget.setTabOrder(self.txtUnid_compras_diciembre, self.txtUnid_compras_enero)
        QWidget.setTabOrder(self.txtUnid_compras_enero, self.txtUnid_compras_mayo)
        QWidget.setTabOrder(self.txtUnid_compras_mayo, self.txtUnid_compras_junio)
        QWidget.setTabOrder(self.txtUnid_compras_junio, self.txtImporte_compras_octubre)
        QWidget.setTabOrder(self.txtImporte_compras_octubre, self.txtImporte_compras_noviembre)

        self.retranslateUi(FrmArticulos)
        self.btn_cerrar.clicked.connect(FrmArticulos.accept)

        self.stackedWidget.setCurrentIndex(0)
        self.Pestanas.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(FrmArticulos)
    # setupUi

    def retranslateUi(self, FrmArticulos):
        FrmArticulos.setWindowTitle(QCoreApplication.translate("FrmArticulos", u"Gesti\u00f3n de Art\u00edculos", None))
        self.botAnadir.setText(QCoreApplication.translate("FrmArticulos", u"A\u00f1adir", None))
        self.botSiguiente.setText(QCoreApplication.translate("FrmArticulos", u"Siguiente", None))
        self.botAnterior.setText(QCoreApplication.translate("FrmArticulos", u"Anterior", None))
        self.btnBuscar.setText(QCoreApplication.translate("FrmArticulos", u"Buscar", None))
        self.botEditar.setText(QCoreApplication.translate("FrmArticulos", u"Editar", None))
        self.botGuardar.setText(QCoreApplication.translate("FrmArticulos", u"Guardar", None))
        self.botDeshacer.setText(QCoreApplication.translate("FrmArticulos", u"Deshacer", None))
        self.botBorrar.setText(QCoreApplication.translate("FrmArticulos", u"Borrar", None))
        self.btnExcepciones_3.setText(QCoreApplication.translate("FrmArticulos", u"Excepciones", None))
        self.btnKit.setText(QCoreApplication.translate("FrmArticulos", u" Ver/\n"
"Editar\n"
" Kit", None))
        self.btn_cerrar.setText(QCoreApplication.translate("FrmArticulos", u"Cerrar", None))
        self.lblkit.setText(QCoreApplication.translate("FrmArticulos", u"KIT", None))
        self.lbl_en_promocion.setText(QCoreApplication.translate("FrmArticulos", u"En Promoci\u00f3n", None))
        self.lblCodigo.setText(QCoreApplication.translate("FrmArticulos", u"c\u00f3digo", None))
        self.lblDescripcion.setText(QCoreApplication.translate("FrmArticulos", u"Descripcion", None))
        self.label_4.setText(QCoreApplication.translate("FrmArticulos", u"C\u00f3digo en Proveedor:", None))
        self.txtcodigo_fabricante.setText("")
        self.label_2.setText(QCoreApplication.translate("FrmArticulos", u"C\u00f3digo: ", None))
        self.label_3.setText(QCoreApplication.translate("FrmArticulos", u"C\u00f3digo EAN:", None))
        self.label_6.setText(QCoreApplication.translate("FrmArticulos", u"Art\u00edculo:", None))
        self.label_8.setText(QCoreApplication.translate("FrmArticulos", u"Proveedor Habitual:", None))
        self.txtcodigo_proveedor.setPlaceholderText(QCoreApplication.translate("FrmArticulos", u"F1-Buscar", None))
        self.btnBuscarProveedor.setText("")
        self.label_18.setText(QCoreApplication.translate("FrmArticulos", u"Comentarios:", None))
        self.label_7.setText(QCoreApplication.translate("FrmArticulos", u"Descripci\u00f3n", None))
        self.label_19.setText(QCoreApplication.translate("FrmArticulos", u"Tipo IVA:", None))
        self.btnEditartarifa.setText(QCoreApplication.translate("FrmArticulos", u"Editar Tarifa", None))
        self.chkcontrolar_stock.setText(QCoreApplication.translate("FrmArticulos", u"Controlar stock", None))
#if QT_CONFIG(tooltip)
        self.chkmostrar_web.setToolTip(QCoreApplication.translate("FrmArticulos", u"Seleccionar si se desea que el art\u00edculo aparezca en la tienda virtual en su web", None))
#endif // QT_CONFIG(tooltip)
        self.chkmostrar_web.setText(QCoreApplication.translate("FrmArticulos", u"Mostrar en web", None))
        self.label_13.setText(QCoreApplication.translate("FrmArticulos", u"Margen min:", None))
        self.label_5.setText(QCoreApplication.translate("FrmArticulos", u"Coste Real:", None))
        self.txtCoste_real.setText(QCoreApplication.translate("FrmArticulos", u"0,00", None))
        self.txtdto.setText(QCoreApplication.translate("FrmArticulos", u"0", None))
        self.label_12.setText(QCoreApplication.translate("FrmArticulos", u"Margen:", None))
        self.label_20.setText(QCoreApplication.translate("FrmArticulos", u"%Descuento Promocional:", None))
        self.label_14.setText(QCoreApplication.translate("FrmArticulos", u"Coste:", None))
        self.txtcoste.setText(QCoreApplication.translate("FrmArticulos", u"0,00", None))
        self.Pestanas.setTabText(self.Pestanas.indexOf(self.tab_articulo), QCoreApplication.translate("FrmArticulos", u"Art\u00edculo", None))
        self.label_9.setText(QCoreApplication.translate("FrmArticulos", u"Secci\u00f3n:", None))
#if QT_CONFIG(tooltip)
        self.botBuscarSeccion.setToolTip(QCoreApplication.translate("FrmArticulos", u"<html><head/><body><p>Asociar Secci\u00f3n.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.botBuscarSeccion.setText("")
        self.label_10.setText(QCoreApplication.translate("FrmArticulos", u"Familia:", None))
        self.botBuscarFamilia.setText("")
        self.label_11.setText(QCoreApplication.translate("FrmArticulos", u"Subfamilia:", None))
        self.botBuscarSubfamilia.setText("")
        self.Pestanas.setTabText(self.Pestanas.indexOf(self.tab), QCoreApplication.translate("FrmArticulos", u"grupos", None))
        self.label_23.setText(QCoreApplication.translate("FrmArticulos", u"Distribuidores frecuentes", None))
#if QT_CONFIG(tooltip)
        self.btnAnadirDistribuidores.setToolTip(QCoreApplication.translate("FrmArticulos", u"<html><head/><body><p><span style=\" color:#ff0000;\">A\u00f1adir proveedor frecuente a ficha de art\u00edculo</span></p><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.btnAnadirDistribuidores.setText("")
#if QT_CONFIG(tooltip)
        self.btnEditarDistribuidorFrecuente.setToolTip(QCoreApplication.translate("FrmArticulos", u"<html><head/><body><p><span style=\" color:#ff0000;\">Editar datos proveedor frecuente</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.btnEditarDistribuidorFrecuente.setText("")
#if QT_CONFIG(tooltip)
        self.btnBorrarDistribuidores.setToolTip(QCoreApplication.translate("FrmArticulos", u"<html><head/><body><p><span style=\" color:#ff0000;\">Quitar proveedor frecuente de ficha de art\u00edculo</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.btnBorrarDistribuidores.setText("")
#if QT_CONFIG(tooltip)
        self.btnAsignarDistribuidor.setToolTip(QCoreApplication.translate("FrmArticulos", u"<html><head/><body><p><span style=\" color:#ff0000;\">Asignar como proveedor principal.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.btnAsignarDistribuidor.setText("")
        self.graf_prov.setProperty(u"Title", QCoreApplication.translate("FrmArticulos", u"PVD Distribuidores", None))
        self.Pestanas.setTabText(self.Pestanas.indexOf(self.tab_distribuidores), QCoreApplication.translate("FrmArticulos", u"Distrubuidores", None))
        self.chkArticulo_promocionado.setText(QCoreApplication.translate("FrmArticulos", u"Art\u00edculo promocionado", None))
        self.label_63.setText(QCoreApplication.translate("FrmArticulos", u"OFERTA PRECIO FIJO", None))
        self.lbl_oferta_importe.setText(QCoreApplication.translate("FrmArticulos", u"Importe:", None))
        self.txtoferta_pvp_fijo.setText(QCoreApplication.translate("FrmArticulos", u"0,00", None))
        self.lbl_por_cada.setText(QCoreApplication.translate("FrmArticulos", u"Por cada: ", None))
        self.txtOferta_por_cada.setText(QCoreApplication.translate("FrmArticulos", u"0", None))
        self.lbl_unidades.setText(QCoreApplication.translate("FrmArticulos", u"Unidades", None))
        self.lbl_regalo_de.setText(QCoreApplication.translate("FrmArticulos", u"Regalo de:", None))
        self.txtOfertaregalo_de.setText(QCoreApplication.translate("FrmArticulos", u"0", None))
        self.lbl_unidades_2.setText(QCoreApplication.translate("FrmArticulos", u"Unidades", None))
        self.label_57.setText(QCoreApplication.translate("FrmArticulos", u"OFERTA TIPO 3*2", None))
        self.txtOferta_Fecha_fin.setDisplayFormat(QCoreApplication.translate("FrmArticulos", u"dd/MM/yyyy", None))
        self.txtOferta_Fecha_ini.setDisplayFormat(QCoreApplication.translate("FrmArticulos", u"dd/MM/yyyy", None))
        self.label_61.setText(QCoreApplication.translate("FrmArticulos", u"OFERTA DTO", None))
        self.lbl_oferta_dto.setText(QCoreApplication.translate("FrmArticulos", u"% Descuento:", None))
        self.txtOfertaDtoOferta.setText(QCoreApplication.translate("FrmArticulos", u"0", None))
        self.lbl_dto_web.setText(QCoreApplication.translate("FrmArticulos", u"Dto Especial web:", None))
        self.lbl_dto_web2.setText(QCoreApplication.translate("FrmArticulos", u"% Descuento:", None))
        self.txtOferta_dto_web.setText(QCoreApplication.translate("FrmArticulos", u"0", None))
        self.label_68.setText(QCoreApplication.translate("FrmArticulos", u"Hasta:", None))
        self.label_21.setText(QCoreApplication.translate("FrmArticulos", u"Desde:", None))
        self.chkMostrar_en_cuadro.setText(QCoreApplication.translate("FrmArticulos", u"Mostrar en cuadro", None))
        self.lblDescripcion_oferta.setText(QCoreApplication.translate("FrmArticulos", u"Descripci\u00f3n:", None))
        self.btnAnadir_oferta.setText(QCoreApplication.translate("FrmArticulos", u"A\u00f1adir", None))
        self.btnEditarOferta.setText(QCoreApplication.translate("FrmArticulos", u"Editar", None))
        self.btnguardar_oferta.setText(QCoreApplication.translate("FrmArticulos", u"Guardar", None))
        self.btnDeshacer_oferta.setText(QCoreApplication.translate("FrmArticulos", u"Deshacer", None))
        self.chkOferta_32.setText(QCoreApplication.translate("FrmArticulos", u" Oferta 3*2", None))
        self.chkOferta_web.setText(QCoreApplication.translate("FrmArticulos", u"Descuento especial web", None))
        self.chkOferta_dto.setText(QCoreApplication.translate("FrmArticulos", u"Oferta % dto", None))
        self.chkOferta_pvp.setText(QCoreApplication.translate("FrmArticulos", u"Oferta precio final", None))
        self.label_65.setText(QCoreApplication.translate("FrmArticulos", u"Comentarios", None))
        self.label_72.setText(QCoreApplication.translate("FrmArticulos", u"OFERTAS ART\u00cdCULO", None))
        self.btnActivarOferta.setText(QCoreApplication.translate("FrmArticulos", u"Activar", None))
        self.btnBorrar_oferta.setText(QCoreApplication.translate("FrmArticulos", u"Borrar", None))
        self.label.setText(QCoreApplication.translate("FrmArticulos", u"Tarifa:", None))
        self.Pestanas.setTabText(self.Pestanas.indexOf(self.tab_promociones), QCoreApplication.translate("FrmArticulos", u"Promociones art\u00edculo", None))
        self.imagen3_web_idioma.setText("")
        self.label_66.setText(QCoreApplication.translate("FrmArticulos", u"Pais", None))
        self.label_51.setText(QCoreApplication.translate("FrmArticulos", u"Articulo:", None))
        self.btnImg_web3_delete.setText("")
        self.label_56.setText(QCoreApplication.translate("FrmArticulos", u"Idioma", None))
        self.btnImg_web3_add.setText("")
        self.btnImg_web4_add.setText("")
        self.imagen4_web_idioma.setText("")
        self.label_64.setText(QCoreApplication.translate("FrmArticulos", u"Descripci\u00f3n:", None))
        self.btnImg_web4_delete.setText("")
        self.imagen1_web_idioma.setText("")
        self.imagen2_web_idioma.setText("")
        self.btnImg_web1_add.setText("")
        self.btnImg_web1_delete.setText("")
        self.btnImg_web2_add.setText("")
        self.btnImg_web2_delete.setText("")
        self.pushButton.setText(QCoreApplication.translate("FrmArticulos", u"Agregar a pais", None))
        self.pushButton_2.setText(QCoreApplication.translate("FrmArticulos", u"Editar", None))
        self.pushButton_3.setText(QCoreApplication.translate("FrmArticulos", u"Guardar", None))
        self.pushButton_4.setText(QCoreApplication.translate("FrmArticulos", u"Deshacer", None))
        self.pushButton_5.setText(QCoreApplication.translate("FrmArticulos", u"Borrar de pais", None))
        self.checkBox.setText(QCoreApplication.translate("FrmArticulos", u"Mostrar en web", None))
        self.Pestanas.setTabText(self.Pestanas.indexOf(self.tab_web), QCoreApplication.translate("FrmArticulos", u"Web", None))
#if QT_CONFIG(tooltip)
        self.lblImagenArticulo_1.setToolTip(QCoreApplication.translate("FrmArticulos", u"La imagen introducida debe tener los mismos pixels horizontales que verticales", None))
#endif // QT_CONFIG(tooltip)
        self.lblImagenArticulo_1.setText("")
#if QT_CONFIG(tooltip)
        self.lblImagenArticulo_2.setToolTip(QCoreApplication.translate("FrmArticulos", u"La imagen introducida debe tener los mismos pixels horizontales que verticales", None))
#endif // QT_CONFIG(tooltip)
        self.lblImagenArticulo_2.setText("")
        self.botCambiarImagen.setText(QCoreApplication.translate("FrmArticulos", u"Cambiar\n"
"Imagen.", None))
        self.btnBorrarImagen_1.setText(QCoreApplication.translate("FrmArticulos", u"Borrar", None))
        self.botCambiarImagen_2.setText(QCoreApplication.translate("FrmArticulos", u"Cambiar\n"
"Imagen.", None))
        self.btnBorrarimagen_2.setText(QCoreApplication.translate("FrmArticulos", u"Borrar", None))
#if QT_CONFIG(tooltip)
        self.lblImagenArticulo_3.setToolTip(QCoreApplication.translate("FrmArticulos", u"La imagen introducida debe tener los mismos pixels horizontales que verticales", None))
#endif // QT_CONFIG(tooltip)
        self.lblImagenArticulo_3.setText("")
#if QT_CONFIG(tooltip)
        self.lblImagenArticulo_4.setToolTip(QCoreApplication.translate("FrmArticulos", u"La imagen introducida debe tener los mismos pixels horizontales que verticales", None))
#endif // QT_CONFIG(tooltip)
        self.lblImagenArticulo_4.setText("")
        self.botCambiarImagen_3.setText(QCoreApplication.translate("FrmArticulos", u"Cambiar\n"
"Imagen.", None))
        self.btnBorrarImagen_3.setText(QCoreApplication.translate("FrmArticulos", u"Borrar", None))
        self.botCambiarImagen_4.setText(QCoreApplication.translate("FrmArticulos", u"Cambiar\n"
"Imagen.", None))
        self.btnBorrarimagen_4.setText(QCoreApplication.translate("FrmArticulos", u"Borrar", None))
        self.Pestanas.setTabText(self.Pestanas.indexOf(self.tab_imagenes), QCoreApplication.translate("FrmArticulos", u"Imagenes Art\u00edculo", None))
        self.txtunidades_vendidas.setText(QCoreApplication.translate("FrmArticulos", u"0", None))
        self.label_29.setText(QCoreApplication.translate("FrmArticulos", u"Unidades Vendidas:", None))
        self.label_28.setText(QCoreApplication.translate("FrmArticulos", u"Unidades Compradas:", None))
        self.txtunidades_compradas.setText(QCoreApplication.translate("FrmArticulos", u"0", None))
        self.label_42.setText(QCoreApplication.translate("FrmArticulos", u"Acumulado Compras", None))
        self.txtfecha_fecha_ultima_compra.setDisplayFormat(QCoreApplication.translate("FrmArticulos", u"dd/MM/yyyy", None))
        self.txtimporte_acumulado_compras.setText(QCoreApplication.translate("FrmArticulos", u"0,00", None))
        self.label_43.setText(QCoreApplication.translate("FrmArticulos", u"Acumulado Ventas:", None))
        self.txtimporte_acumulado_ventas.setText(QCoreApplication.translate("FrmArticulos", u"0,00", None))
        self.lblFechaCompra.setText(QCoreApplication.translate("FrmArticulos", u"Fecha \u00falt. Compra:", None))
        self.lblFechaVenta.setText(QCoreApplication.translate("FrmArticulos", u"Fecha \u00falt. Venta:", None))
        self.txtfechaUltimaVenta.setDisplayFormat(QCoreApplication.translate("FrmArticulos", u"dd/MM/yyyy", None))
        self.btnResArt2.setText(QCoreApplication.translate("FrmArticulos", u"Referencia-descripcion-pvp-tipo iva - ODS", None))
        self.txtstock_fisico_almacen.setText(QCoreApplication.translate("FrmArticulos", u"0", None))
        self.label_30.setText(QCoreApplication.translate("FrmArticulos", u"Stock M\u00ednimo:", None))
        self.label_22.setText(QCoreApplication.translate("FrmArticulos", u"Stock Fisico:", None))
        self.txtstock_minimo.setText(QCoreApplication.translate("FrmArticulos", u"0", None))
        self.label_31.setText(QCoreApplication.translate("FrmArticulos", u"Stock M\u00e1ximo:", None))
        self.txtstock_maximo.setText(QCoreApplication.translate("FrmArticulos", u"0", None))
        self.label_44.setText(QCoreApplication.translate("FrmArticulos", u"Pendientes recibir:", None))
        self.txtcantidad_pendiente_recibir.setText(QCoreApplication.translate("FrmArticulos", u"0", None))
        self.txtstock_real_2.setText(QCoreApplication.translate("FrmArticulos", u"0", None))
        self.label_32.setText(QCoreApplication.translate("FrmArticulos", u"Stock Real:\n"
"(fisico+ pendiente recibir)", None))
        self.label_45.setText(QCoreApplication.translate("FrmArticulos", u"Cantidad reservada:", None))
        self.txtunidades_reservadas.setText(QCoreApplication.translate("FrmArticulos", u"0", None))
        self.lblFechaPrevistaRecepcion.setText(QCoreApplication.translate("FrmArticulos", u"Fecha Prev. Recepc.:", None))
        self.txtfecha_prevista_recepcion.setDisplayFormat(QCoreApplication.translate("FrmArticulos", u"dd/MM/yyyy", None))
        self.btnResArt.setText(QCoreApplication.translate("FrmArticulos", u"resumen articulos /Stock - ODS", None))
        self.Pestanas.setTabText(self.Pestanas.indexOf(self.tab_estadistica), QCoreApplication.translate("FrmArticulos", u"Estadistica", None))
        self.cboTipoGrafica.setItemText(0, QCoreApplication.translate("FrmArticulos", u"Grafica de Barras", None))
        self.cboTipoGrafica.setItemText(1, QCoreApplication.translate("FrmArticulos", u"Grafica de L\u00edneas", None))

        self.radGrafica_unidades.setText(QCoreApplication.translate("FrmArticulos", u"Grafica de unidades", None))
        self.radGrafica_importes.setText(QCoreApplication.translate("FrmArticulos", u"Grafica de Importes", None))
        self.chkValorGrafica.setText(QCoreApplication.translate("FrmArticulos", u"Mostrar valores", None))
        self.label_25.setText(QCoreApplication.translate("FrmArticulos", u"COMPRAS", None))
        self.txtImporte_compras_enero.setText(QCoreApplication.translate("FrmArticulos", u"0,00", None))
        self.txtImporte_compras_julio.setText(QCoreApplication.translate("FrmArticulos", u"0,00", None))
        self.txtImporte_compras_marzo.setText(QCoreApplication.translate("FrmArticulos", u"0,00", None))
        self.txtUnid_compras_febrero.setText(QCoreApplication.translate("FrmArticulos", u"0", None))
        self.txtUnid_compras_marzo.setText(QCoreApplication.translate("FrmArticulos", u"0", None))
        self.txtImporte_compras_septiembre.setText(QCoreApplication.translate("FrmArticulos", u"0,00", None))
        self.label_52.setText(QCoreApplication.translate("FrmArticulos", u"Unidades", None))
        self.txtImporte_compras_diciembre.setText(QCoreApplication.translate("FrmArticulos", u"0,00", None))
        self.txtUnid_compras_agosto.setText(QCoreApplication.translate("FrmArticulos", u"0", None))
        self.txtUnid_compras_diciembre.setText(QCoreApplication.translate("FrmArticulos", u"0", None))
        self.txtUnid_compras_junio.setText(QCoreApplication.translate("FrmArticulos", u"0", None))
        self.txtUnid_compras_mayo.setText(QCoreApplication.translate("FrmArticulos", u"0", None))
        self.txtUnid_compras_enero.setText(QCoreApplication.translate("FrmArticulos", u"0", None))
        self.txtImporte_compras_octubre.setText(QCoreApplication.translate("FrmArticulos", u"0,00", None))
        self.txtImporte_compras_noviembre.setText(QCoreApplication.translate("FrmArticulos", u"0,00", None))
        self.txtUnid_compras_noviembre.setText(QCoreApplication.translate("FrmArticulos", u"0", None))
        self.txtImporte_compras_agosto.setText(QCoreApplication.translate("FrmArticulos", u"0,00", None))
        self.txtImporte_compras_mayo.setText(QCoreApplication.translate("FrmArticulos", u"0,00", None))
        self.txtUnid_compras_septiembre.setText(QCoreApplication.translate("FrmArticulos", u"0", None))
        self.txtImporte_compras_febrero.setText(QCoreApplication.translate("FrmArticulos", u"0,00", None))
        self.txtUnid_compras_abril.setText(QCoreApplication.translate("FrmArticulos", u"0", None))
        self.txtImporte_compras_abril.setText(QCoreApplication.translate("FrmArticulos", u"0,00", None))
        self.label_53.setText(QCoreApplication.translate("FrmArticulos", u"Importe", None))
        self.txtUnid_compras_julio.setText(QCoreApplication.translate("FrmArticulos", u"0", None))
        self.txtImporte_compras_junio.setText(QCoreApplication.translate("FrmArticulos", u"0,00", None))
        self.txtUnid_compras_octubre.setText(QCoreApplication.translate("FrmArticulos", u"0", None))
        self.label_27.setText(QCoreApplication.translate("FrmArticulos", u"Enero:", None))
        self.label_35.setText(QCoreApplication.translate("FrmArticulos", u"Febrero:", None))
        self.label_36.setText(QCoreApplication.translate("FrmArticulos", u"Marzo:", None))
        self.label_37.setText(QCoreApplication.translate("FrmArticulos", u"Abril:", None))
        self.label_39.setText(QCoreApplication.translate("FrmArticulos", u"Mayo:", None))
        self.label_40.setText(QCoreApplication.translate("FrmArticulos", u"Junio:", None))
        self.label_41.setText(QCoreApplication.translate("FrmArticulos", u"Julio:", None))
        self.label_46.setText(QCoreApplication.translate("FrmArticulos", u"Agosto:", None))
        self.label_47.setText(QCoreApplication.translate("FrmArticulos", u"Septiembre:", None))
        self.label_48.setText(QCoreApplication.translate("FrmArticulos", u"Octubre:", None))
        self.label_49.setText(QCoreApplication.translate("FrmArticulos", u"Noviembre:", None))
        self.label_50.setText(QCoreApplication.translate("FrmArticulos", u"Diciembre:", None))
        self.label_26.setText(QCoreApplication.translate("FrmArticulos", u"VENTAS", None))
        self.label_54.setText(QCoreApplication.translate("FrmArticulos", u"Unidades", None))
        self.label_55.setText(QCoreApplication.translate("FrmArticulos", u"Importe", None))
        self.txtUnid_ventas_enero.setText(QCoreApplication.translate("FrmArticulos", u"0", None))
        self.txtImporte_ventas_enero.setText(QCoreApplication.translate("FrmArticulos", u"0,00", None))
        self.txtUnid_ventas_febrero.setText(QCoreApplication.translate("FrmArticulos", u"0", None))
        self.txtImporte_ventas_febrero.setText(QCoreApplication.translate("FrmArticulos", u"0,00", None))
        self.txtUnid_ventas_marzo.setText(QCoreApplication.translate("FrmArticulos", u"0", None))
        self.txtImporte_ventas_marzo.setText(QCoreApplication.translate("FrmArticulos", u"0,00", None))
        self.txtUnid_ventas_abril.setText(QCoreApplication.translate("FrmArticulos", u"0", None))
        self.txtImporte_ventas_abril.setText(QCoreApplication.translate("FrmArticulos", u"0,00", None))
        self.txtUnid_ventas_mayo.setText(QCoreApplication.translate("FrmArticulos", u"0", None))
        self.txtImporte_ventas_mayo.setText(QCoreApplication.translate("FrmArticulos", u"0,00", None))
        self.txtUnid_ventas_junio.setText(QCoreApplication.translate("FrmArticulos", u"0", None))
        self.txtImporte_ventas_junio.setText(QCoreApplication.translate("FrmArticulos", u"0,00", None))
        self.txtUnid_ventas_julio.setText(QCoreApplication.translate("FrmArticulos", u"0", None))
        self.txtImporte_ventas_julio.setText(QCoreApplication.translate("FrmArticulos", u"0,00", None))
        self.txtUnid_ventas_agosto.setText(QCoreApplication.translate("FrmArticulos", u"0", None))
        self.txtImporte_ventas_agosto.setText(QCoreApplication.translate("FrmArticulos", u"0,00", None))
        self.txtUnid_ventas_septiembre.setText(QCoreApplication.translate("FrmArticulos", u"0", None))
        self.txtImporte_ventas_septiembre.setText(QCoreApplication.translate("FrmArticulos", u"0,00", None))
        self.txtUnid_ventas_octubre.setText(QCoreApplication.translate("FrmArticulos", u"0", None))
        self.txtImporte_ventas_octubre.setText(QCoreApplication.translate("FrmArticulos", u"0,00", None))
        self.txtUnid_ventas_noviembre.setText(QCoreApplication.translate("FrmArticulos", u"0", None))
        self.txtImporte_ventas_noviembre.setText(QCoreApplication.translate("FrmArticulos", u"0,00", None))
        self.txtUnid_ventas_diciembre.setText(QCoreApplication.translate("FrmArticulos", u"0", None))
        self.txtImporte_ventas_diciembre.setText(QCoreApplication.translate("FrmArticulos", u"0,00", None))
        self.Pestanas.setTabText(self.Pestanas.indexOf(self.tab_grafica), QCoreApplication.translate("FrmArticulos", u"Estad\u00edstica/Gr\u00e1fica", None))
        self.label_70.setText(QCoreApplication.translate("FrmArticulos", u"Gesti\u00f3n de Articulos", None))
    # retranslateUi

