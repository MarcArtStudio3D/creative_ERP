# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frmkit.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QDialog,
    QDoubleSpinBox, QFrame, QGridLayout, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QTableView,
    QWidget)
from modules import designer_rc

class Ui_FrmKit(object):
    def setupUi(self, FrmKit):
        if not FrmKit.objectName():
            FrmKit.setObjectName(u"FrmKit")
        FrmKit.resize(1077, 722)
        self.gridLayout_3 = QGridLayout(FrmKit)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.tabla = QTableView(FrmKit)
        self.tabla.setObjectName(u"tabla")
        self.tabla.setAutoFillBackground(True)
        self.tabla.setAlternatingRowColors(True)
        self.tabla.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabla.horizontalHeader().setStretchLastSection(True)

        self.gridLayout_3.addWidget(self.tabla, 1, 0, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.txtCodigo_kit = QLineEdit(FrmKit)
        self.txtCodigo_kit.setObjectName(u"txtCodigo_kit")
        self.txtCodigo_kit.setMaximumSize(QSize(120, 16777215))
        self.txtCodigo_kit.setReadOnly(True)

        self.gridLayout_2.addWidget(self.txtCodigo_kit, 0, 1, 1, 1)

        self.label_7 = QLabel(FrmKit)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_2.addWidget(self.label_7, 0, 0, 1, 1)

        self.txtDesc_kit = QLineEdit(FrmKit)
        self.txtDesc_kit.setObjectName(u"txtDesc_kit")
        self.txtDesc_kit.setReadOnly(True)

        self.gridLayout_2.addWidget(self.txtDesc_kit, 0, 2, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 2)

        self.btnQuitar = QPushButton(FrmKit)
        self.btnQuitar.setObjectName(u"btnQuitar")
        icon = QIcon()
        icon.addFile(u":/Icons/PNG/borrar.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnQuitar.setIcon(icon)

        self.gridLayout_3.addWidget(self.btnQuitar, 2, 0, 1, 1)

        self.frame = QFrame(FrmKit)
        self.frame.setObjectName(u"frame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMaximumSize(QSize(500, 16777215))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton = QPushButton(self.frame)
        self.pushButton.setObjectName(u"pushButton")
        icon1 = QIcon()
        icon1.addFile(u":/Icons/PNG/Exit.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton.setIcon(icon1)

        self.horizontalLayout.addWidget(self.pushButton)


        self.gridLayout.addLayout(self.horizontalLayout, 12, 0, 1, 2)

        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setStyleSheet(u"")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_3)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.spinCantidad = QDoubleSpinBox(self.frame_3)
        self.spinCantidad.setObjectName(u"spinCantidad")
        self.spinCantidad.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.spinCantidad.setMinimum(1.000000000000000)
        self.spinCantidad.setMaximum(999999999.990000009536743)

        self.gridLayout_5.addWidget(self.spinCantidad, 1, 3, 1, 1)

        self.txtDescripcion = QLineEdit(self.frame_3)
        self.txtDescripcion.setObjectName(u"txtDescripcion")
        self.txtDescripcion.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")

        self.gridLayout_5.addWidget(self.txtDescripcion, 2, 1, 1, 3)

        self.label_8 = QLabel(self.frame_3)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_5.addWidget(self.label_8, 4, 2, 1, 1)

        self.txtCodigo = QLineEdit(self.frame_3)
        self.txtCodigo.setObjectName(u"txtCodigo")
        self.txtCodigo.setMinimumSize(QSize(139, 0))
        self.txtCodigo.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")

        self.gridLayout_5.addWidget(self.txtCodigo, 1, 1, 1, 1)

        self.label_5 = QLabel(self.frame_3)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_5.addWidget(self.label_5, 2, 0, 1, 1)

        self.label_4 = QLabel(self.frame_3)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_5.addWidget(self.label_4, 1, 0, 1, 1)

        self.label_6 = QLabel(self.frame_3)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_5.addWidget(self.label_6, 3, 2, 1, 1)

        self.spinCoste = QDoubleSpinBox(self.frame_3)
        self.spinCoste.setObjectName(u"spinCoste")
        self.spinCoste.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.spinCoste.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.spinCoste.setMinimum(-10000000.000000000000000)
        self.spinCoste.setMaximum(1000000000.000000000000000)

        self.gridLayout_5.addWidget(self.spinCoste, 3, 1, 1, 1)

        self.label_3 = QLabel(self.frame_3)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_5.addWidget(self.label_3, 1, 2, 1, 1)

        self.lblCoste = QLabel(self.frame_3)
        self.lblCoste.setObjectName(u"lblCoste")
        self.lblCoste.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.lblCoste, 4, 3, 1, 1)

        self.label_9 = QLabel(self.frame_3)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_5.addWidget(self.label_9, 3, 0, 1, 1)

        self.spinDto = QDoubleSpinBox(self.frame_3)
        self.spinDto.setObjectName(u"spinDto")
        # self.spinDto.setStyleSheet(u"background-color: rgb(255, 255, 255);") # Removed hardcoded background color
        self.spinDto.setMaximum(100.000000000000000)

        self.gridLayout_5.addWidget(self.spinDto, 3, 3, 1, 1)


        self.gridLayout.addWidget(self.frame_3, 5, 0, 1, 2)

        self.cboSentido = QComboBox(self.frame)
        self.cboSentido.setObjectName(u"cboSentido")
        self.cboSentido.setStyleSheet(u"color: rgb(0, 0, 0);")

        self.gridLayout.addWidget(self.cboSentido, 1, 1, 1, 1)

        self.btnGuardar = QPushButton(self.frame)
        self.btnGuardar.setObjectName(u"btnGuardar")
        self.btnGuardar.setEnabled(True)
        icon2 = QIcon()
        icon2.addFile(u":/PNG/resources/icons/png/Previous.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnGuardar.setIcon(icon2)

        self.gridLayout.addWidget(self.btnGuardar, 8, 0, 1, 2)

        self.txtBuscar = QLineEdit(self.frame)
        self.txtBuscar.setObjectName(u"txtBuscar")

        self.gridLayout.addWidget(self.txtBuscar, 2, 1, 1, 1)

        self.frame_4 = QFrame(self.frame)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setEnabled(True)
        self.frame_4.setStyleSheet(u"")
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_4)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.btnRomperKit = QPushButton(self.frame_4)
        self.btnRomperKit.setObjectName(u"btnRomperKit")
        icon3 = QIcon()
        icon3.addFile(u":/PNG/resources/icons/png/delete.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnRomperKit.setIcon(icon3)

        self.gridLayout_6.addWidget(self.btnRomperKit, 2, 1, 1, 1)

        self.label_12 = QLabel(self.frame_4)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.gridLayout_6.addWidget(self.label_12, 1, 0, 2, 1)

        self.spinCantRomper = QSpinBox(self.frame_4)
        self.spinCantRomper.setObjectName(u"spinCantRomper")
        self.spinCantRomper.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.spinCantRomper, 1, 1, 1, 1)


        self.gridLayout.addWidget(self.frame_4, 10, 0, 1, 2)

        self.label_10 = QLabel(self.frame)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 1, 0, 1, 1)

        self.btnAnadir = QPushButton(self.frame)
        self.btnAnadir.setObjectName(u"btnAnadir")
        icon4 = QIcon()
        icon4.addFile(u":/PNG/resources/icons/png/down_arrow.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnAnadir.setIcon(icon4)

        self.gridLayout.addWidget(self.btnAnadir, 4, 0, 1, 2)

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.cboOrden = QComboBox(self.frame)
        self.cboOrden.setObjectName(u"cboOrden")
        self.cboOrden.setStyleSheet(u"color: rgb(0, 0, 0);")

        self.gridLayout.addWidget(self.cboOrden, 0, 1, 1, 1)

        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)

        self.tabla_buscar = QTableView(self.frame)
        self.tabla_buscar.setObjectName(u"tabla_buscar")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tabla_buscar.sizePolicy().hasHeightForWidth())
        self.tabla_buscar.setSizePolicy(sizePolicy1)
        self.tabla_buscar.setMinimumSize(QSize(0, 92))
        self.tabla_buscar.setAlternatingRowColors(True)
        self.tabla_buscar.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tabla_buscar.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabla_buscar.verticalHeader().setVisible(False)

        self.gridLayout.addWidget(self.tabla_buscar, 3, 0, 1, 2)

        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setStyleSheet(u"")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.btnAnadirKits = QPushButton(self.frame_2)
        self.btnAnadirKits.setObjectName(u"btnAnadirKits")
        icon5 = QIcon()
        icon5.addFile(u":/PNG/resources/icons/png/Add.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnAnadirKits.setIcon(icon5)

        self.gridLayout_4.addWidget(self.btnAnadirKits, 1, 1, 1, 1)

        self.label_11 = QLabel(self.frame_2)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.gridLayout_4.addWidget(self.label_11, 0, 0, 2, 1)

        self.spinCant = QSpinBox(self.frame_2)
        self.spinCant.setObjectName(u"spinCant")
        self.spinCant.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.spinCant, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.frame_2, 9, 0, 1, 2)


        self.gridLayout_3.addWidget(self.frame, 1, 1, 2, 1)

        QWidget.setTabOrder(self.txtCodigo_kit, self.txtDesc_kit)
        QWidget.setTabOrder(self.txtDesc_kit, self.cboOrden)
        QWidget.setTabOrder(self.cboOrden, self.cboSentido)
        QWidget.setTabOrder(self.cboSentido, self.txtBuscar)
        QWidget.setTabOrder(self.txtBuscar, self.tabla_buscar)
        QWidget.setTabOrder(self.tabla_buscar, self.btnAnadir)
        QWidget.setTabOrder(self.btnAnadir, self.txtCodigo)
        QWidget.setTabOrder(self.txtCodigo, self.spinCantidad)
        QWidget.setTabOrder(self.spinCantidad, self.txtDescripcion)
        QWidget.setTabOrder(self.txtDescripcion, self.spinCoste)
        QWidget.setTabOrder(self.spinCoste, self.spinDto)
        QWidget.setTabOrder(self.spinDto, self.btnGuardar)
        QWidget.setTabOrder(self.btnGuardar, self.spinCant)
        QWidget.setTabOrder(self.spinCant, self.btnAnadirKits)
        QWidget.setTabOrder(self.btnAnadirKits, self.spinCantRomper)
        QWidget.setTabOrder(self.spinCantRomper, self.btnRomperKit)
        QWidget.setTabOrder(self.btnRomperKit, self.pushButton)
        QWidget.setTabOrder(self.pushButton, self.btnQuitar)
        QWidget.setTabOrder(self.btnQuitar, self.tabla)

        self.retranslateUi(FrmKit)
        self.pushButton.clicked.connect(FrmKit.accept)

        QMetaObject.connectSlotsByName(FrmKit)
    # setupUi

    def retranslateUi(self, FrmKit):
        FrmKit.setWindowTitle(QCoreApplication.translate("FrmKit", u"Gesti\u00f3n de Kits de producto.", None))
        self.label_7.setText(QCoreApplication.translate("FrmKit", u"C\u00f3digo:", None))
        self.btnQuitar.setText(QCoreApplication.translate("FrmKit", u"Quitar producto", None))
        self.pushButton.setText(QCoreApplication.translate("FrmKit", u"Cerrar", None))
        self.label_8.setText(QCoreApplication.translate("FrmKit", u"Coste en Kit", None))
        self.label_5.setText(QCoreApplication.translate("FrmKit", u"Descripci\u00f3n:", None))
        self.label_4.setText(QCoreApplication.translate("FrmKit", u"C\u00f3digo:", None))
        self.label_6.setText(QCoreApplication.translate("FrmKit", u"Dto:", None))
        self.label_3.setText(QCoreApplication.translate("FrmKit", u"Cantidad:", None))
        self.lblCoste.setText(QCoreApplication.translate("FrmKit", u"0,0", None))
        self.label_9.setText(QCoreApplication.translate("FrmKit", u"Coste:", None))
        self.btnGuardar.setText(QCoreApplication.translate("FrmKit", u"<<Agregar(2)", None))
        self.btnRomperKit.setText(QCoreApplication.translate("FrmKit", u"Romper Kit", None))
        self.label_12.setText(QCoreApplication.translate("FrmKit", u"Romper Kits (A\u00f1adir\u00e1 stock\n"
"a los productos del kit):", None))
        self.label_10.setText(QCoreApplication.translate("FrmKit", u"Sentido:", None))
        self.btnAnadir.setText(QCoreApplication.translate("FrmKit", u"Preparar componente kit (1)", None))
        self.label_2.setText(QCoreApplication.translate("FrmKit", u"Buscar por:", None))
        self.label.setText(QCoreApplication.translate("FrmKit", u"Filtro:", None))
        self.btnAnadirKits.setText(QCoreApplication.translate("FrmKit", u"A\u00f1adir stock Kit (3)", None))
        self.label_11.setText(QCoreApplication.translate("FrmKit", u"Crear Kits (Descontar\u00e1 stock\n"
"de los productos kit):", None))
    # retranslateUi

