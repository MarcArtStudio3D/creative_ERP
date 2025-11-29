# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frmformas_pago.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDialog, QDoubleSpinBox,
    QFrame, QGridLayout, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QRadioButton, QSizePolicy, QSpacerItem, QSpinBox,
    QStackedWidget, QTableView, QTextEdit, QVBoxLayout,
    QWidget)
from modules import designer_rc

class Ui_FrmFormas_pago(object):
    def setupUi(self, FrmFormas_pago):
        if not FrmFormas_pago.objectName():
            FrmFormas_pago.setObjectName(u"FrmFormas_pago")
        FrmFormas_pago.resize(1031, 657)
        self.gridLayout_2 = QGridLayout(FrmFormas_pago)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_36 = QLabel(FrmFormas_pago)
        self.label_36.setObjectName(u"label_36")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_36.sizePolicy().hasHeightForWidth())
        self.label_36.setSizePolicy(sizePolicy)
        self.label_36.setMinimumSize(QSize(300, 23))
        self.label_36.setStyleSheet(u"font: 14pt \"Sans Serif\";\n"
"color: rgb(255, 255, 255);\n"
"background-color: #304163;")
        self.label_36.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label_36, 0, 0, 1, 1)

        self.stackedWidget = QStackedWidget(FrmFormas_pago)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.gridLayout = QGridLayout(self.page)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, -1, 20, -1)
        self.tabla_buscar = QTableView(self.page)
        self.tabla_buscar.setObjectName(u"tabla_buscar")
        self.tabla_buscar.setStyleSheet(u"alternate-\n"
"font: 8pt \"Sans\";")
        self.tabla_buscar.setAlternatingRowColors(True)
        self.tabla_buscar.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tabla_buscar.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabla_buscar.horizontalHeader().setStretchLastSection(True)
        self.tabla_buscar.verticalHeader().setVisible(False)

        self.gridLayout.addWidget(self.tabla_buscar, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.gridLayout_6 = QGridLayout(self.page_2)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(-1, -1, 20, -1)
        self.frame = QFrame(self.page_2)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.groupBox_2 = QGroupBox(self.frame)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.txtPorcentajeInicial = QDoubleSpinBox(self.groupBox_2)
        self.txtPorcentajeInicial.setObjectName(u"txtPorcentajeInicial")
        self.txtPorcentajeInicial.setEnabled(False)
        self.txtPorcentajeInicial.setGeometry(QRect(70, 30, 91, 32))
        self.txtPorcentajeFinal = QDoubleSpinBox(self.groupBox_2)
        self.txtPorcentajeFinal.setObjectName(u"txtPorcentajeFinal")
        self.txtPorcentajeFinal.setEnabled(False)
        self.txtPorcentajeFinal.setGeometry(QRect(220, 30, 81, 32))
        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 30, 58, 31))
        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(170, 30, 51, 31))

        self.gridLayout_5.addWidget(self.groupBox_2, 2, 1, 1, 2)

        self.frame_4 = QFrame(self.frame)
        self.frame_4.setObjectName(u"frame_4")
        sizePolicy.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy)
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_4)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, 2, -1, -1)
        self.btnAnadir_3 = QPushButton(self.frame_4)
        self.btnAnadir_3.setObjectName(u"btnAnadir_3")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btnAnadir_3.sizePolicy().hasHeightForWidth())
        self.btnAnadir_3.setSizePolicy(sizePolicy1)
        self.btnAnadir_3.setMinimumSize(QSize(0, 27))
        icon = QIcon()
        icon.addFile(u":/PNG/resources/icons/png/Add.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnAnadir_3.setIcon(icon)
        self.btnAnadir_3.setIconSize(QSize(24, 24))

        self.verticalLayout.addWidget(self.btnAnadir_3)

        self.btnSiguiente_2 = QPushButton(self.frame_4)
        self.btnSiguiente_2.setObjectName(u"btnSiguiente_2")
        sizePolicy1.setHeightForWidth(self.btnSiguiente_2.sizePolicy().hasHeightForWidth())
        self.btnSiguiente_2.setSizePolicy(sizePolicy1)
        self.btnSiguiente_2.setMinimumSize(QSize(0, 27))
        icon1 = QIcon()
        icon1.addFile(u":/PNG/resources/icons/png/Next.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnSiguiente_2.setIcon(icon1)
        self.btnSiguiente_2.setIconSize(QSize(24, 24))

        self.verticalLayout.addWidget(self.btnSiguiente_2)

        self.btnAnterior_2 = QPushButton(self.frame_4)
        self.btnAnterior_2.setObjectName(u"btnAnterior_2")
        sizePolicy1.setHeightForWidth(self.btnAnterior_2.sizePolicy().hasHeightForWidth())
        self.btnAnterior_2.setSizePolicy(sizePolicy1)
        self.btnAnterior_2.setMinimumSize(QSize(0, 27))
        icon2 = QIcon()
        icon2.addFile(u":/PNG/resources/icons/png/Previous.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnAnterior_2.setIcon(icon2)
        self.btnAnterior_2.setIconSize(QSize(24, 24))

        self.verticalLayout.addWidget(self.btnAnterior_2)

        self.btnEditar_3 = QPushButton(self.frame_4)
        self.btnEditar_3.setObjectName(u"btnEditar_3")
        sizePolicy1.setHeightForWidth(self.btnEditar_3.sizePolicy().hasHeightForWidth())
        self.btnEditar_3.setSizePolicy(sizePolicy1)
        self.btnEditar_3.setMinimumSize(QSize(0, 27))
        icon3 = QIcon()
        icon3.addFile(u":/PNG/resources/icons/png/Edit.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnEditar_3.setIcon(icon3)
        self.btnEditar_3.setIconSize(QSize(24, 24))

        self.verticalLayout.addWidget(self.btnEditar_3)

        self.btnGuardar_2 = QPushButton(self.frame_4)
        self.btnGuardar_2.setObjectName(u"btnGuardar_2")
        sizePolicy1.setHeightForWidth(self.btnGuardar_2.sizePolicy().hasHeightForWidth())
        self.btnGuardar_2.setSizePolicy(sizePolicy1)
        self.btnGuardar_2.setMinimumSize(QSize(0, 27))
        icon4 = QIcon()
        icon4.addFile(u":/PNG/resources/icons/png/Save.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnGuardar_2.setIcon(icon4)
        self.btnGuardar_2.setIconSize(QSize(24, 24))

        self.verticalLayout.addWidget(self.btnGuardar_2)

        self.btndeshacer_2 = QPushButton(self.frame_4)
        self.btndeshacer_2.setObjectName(u"btndeshacer_2")
        self.btndeshacer_2.setMinimumSize(QSize(0, 27))
        icon5 = QIcon()
        icon5.addFile(u":/PNG/resources/icons/png/undo.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btndeshacer_2.setIcon(icon5)

        self.verticalLayout.addWidget(self.btndeshacer_2)

        self.btnBuscar_2 = QPushButton(self.frame_4)
        self.btnBuscar_2.setObjectName(u"btnBuscar_2")
        sizePolicy1.setHeightForWidth(self.btnBuscar_2.sizePolicy().hasHeightForWidth())
        self.btnBuscar_2.setSizePolicy(sizePolicy1)
        self.btnBuscar_2.setMinimumSize(QSize(0, 27))
        icon6 = QIcon()
        icon6.addFile(u":/PNG/resources/icons/png/search.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnBuscar_2.setIcon(icon6)
        self.btnBuscar_2.setIconSize(QSize(24, 24))

        self.verticalLayout.addWidget(self.btnBuscar_2)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.btn_borrar = QPushButton(self.frame_4)
        self.btn_borrar.setObjectName(u"btn_borrar")
        sizePolicy1.setHeightForWidth(self.btn_borrar.sizePolicy().hasHeightForWidth())
        self.btn_borrar.setSizePolicy(sizePolicy1)
        self.btn_borrar.setMinimumSize(QSize(0, 27))
        icon7 = QIcon()
        icon7.addFile(u":/PNG/resources/icons/png/delete.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_borrar.setIcon(icon7)
        self.btn_borrar.setIconSize(QSize(24, 24))

        self.verticalLayout.addWidget(self.btn_borrar)


        self.gridLayout_5.addWidget(self.frame_4, 0, 0, 7, 1)

        self.textEdit = QTextEdit(self.frame)
        self.textEdit.setObjectName(u"textEdit")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy2)
        self.textEdit.setReadOnly(True)

        self.gridLayout_5.addWidget(self.textEdit, 0, 5, 7, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.rdbContado = QRadioButton(self.frame)
        self.rdbContado.setObjectName(u"rdbContado")
        self.rdbContado.setEnabled(False)
        self.rdbContado.setChecked(True)

        self.horizontalLayout.addWidget(self.rdbContado)

        self.radioButton_2 = QRadioButton(self.frame)
        self.radioButton_2.setObjectName(u"radioButton_2")
        self.radioButton_2.setEnabled(False)

        self.horizontalLayout.addWidget(self.radioButton_2)


        self.gridLayout_5.addLayout(self.horizontalLayout, 1, 1, 1, 2)

        self.groupBox = QGroupBox(self.frame)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setEnabled(True)
        self.groupBox.setCheckable(False)
        self.gridLayout_3 = QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_14 = QLabel(self.groupBox)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMaximumSize(QSize(16777215, 17))
        self.label_14.setStyleSheet(u"background-color: #304163;\n"
"color: rgb(255, 255, 255);")
        self.label_14.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.label_14, 0, 0, 1, 8)

        self.spinDia_pago4 = QSpinBox(self.groupBox)
        self.spinDia_pago4.setObjectName(u"spinDia_pago4")
        self.spinDia_pago4.setEnabled(False)

        self.gridLayout_3.addWidget(self.spinDia_pago4, 1, 7, 1, 1)

        self.label_13 = QLabel(self.groupBox)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_13, 1, 6, 1, 1)

        self.spinDia_pago1 = QSpinBox(self.groupBox)
        self.spinDia_pago1.setObjectName(u"spinDia_pago1")
        self.spinDia_pago1.setEnabled(False)
        self.spinDia_pago1.setMinimum(1)

        self.gridLayout_3.addWidget(self.spinDia_pago1, 1, 1, 1, 1)

        self.label_12 = QLabel(self.groupBox)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_12, 1, 4, 1, 1)

        self.label_11 = QLabel(self.groupBox)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_11, 1, 2, 1, 1)

        self.spinDia_pago3 = QSpinBox(self.groupBox)
        self.spinDia_pago3.setObjectName(u"spinDia_pago3")
        self.spinDia_pago3.setEnabled(False)

        self.gridLayout_3.addWidget(self.spinDia_pago3, 1, 5, 1, 1)

        self.spinDia_pago2 = QSpinBox(self.groupBox)
        self.spinDia_pago2.setObjectName(u"spinDia_pago2")
        self.spinDia_pago2.setEnabled(False)

        self.gridLayout_3.addWidget(self.spinDia_pago2, 1, 3, 1, 1)

        self.label_16 = QLabel(self.groupBox)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMaximumSize(QSize(16777215, 17))
        self.label_16.setStyleSheet(u"background-color: #304163;\n"
"color: rgb(255, 255, 255);")
        self.label_16.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.label_16, 2, 0, 1, 8)

        self.label_10 = QLabel(self.groupBox)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_10, 1, 0, 1, 1)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_3.addWidget(self.label_3, 3, 0, 1, 1)

        self.dias_hasta_pago = QSpinBox(self.groupBox)
        self.dias_hasta_pago.setObjectName(u"dias_hasta_pago")
        self.dias_hasta_pago.setEnabled(False)
        self.dias_hasta_pago.setMaximum(365)

        self.gridLayout_3.addWidget(self.dias_hasta_pago, 3, 1, 1, 1)

        self.spinDias_entre_plazos = QSpinBox(self.groupBox)
        self.spinDias_entre_plazos.setObjectName(u"spinDias_entre_plazos")
        self.spinDias_entre_plazos.setEnabled(False)
        self.spinDias_entre_plazos.setMaximumSize(QSize(60, 16777215))

        self.gridLayout_3.addWidget(self.spinDias_entre_plazos, 3, 7, 1, 1)

        self.spinNumero_plazos = QSpinBox(self.groupBox)
        self.spinNumero_plazos.setObjectName(u"spinNumero_plazos")
        self.spinNumero_plazos.setEnabled(False)
        self.spinNumero_plazos.setMaximumSize(QSize(60, 16777215))

        self.gridLayout_3.addWidget(self.spinNumero_plazos, 3, 4, 1, 1)

        self.label_18 = QLabel(self.groupBox)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout_3.addWidget(self.label_18, 3, 2, 1, 2)

        self.label_15 = QLabel(self.groupBox)
        self.label_15.setObjectName(u"label_15")
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)
        self.label_15.setMinimumSize(QSize(120, 0))
        self.label_15.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_15, 3, 5, 1, 2)


        self.gridLayout_5.addWidget(self.groupBox, 3, 1, 1, 4)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label, 1, 0, 1, 2)

        self.txtForma_pago = QLineEdit(self.frame)
        self.txtForma_pago.setObjectName(u"txtForma_pago")
        self.txtForma_pago.setEnabled(False)

        self.gridLayout_4.addWidget(self.txtForma_pago, 1, 2, 1, 1)

        self.txtcod_forma_pago = QLineEdit(self.frame)
        self.txtcod_forma_pago.setObjectName(u"txtcod_forma_pago")
        self.txtcod_forma_pago.setEnabled(False)

        self.gridLayout_4.addWidget(self.txtcod_forma_pago, 0, 2, 1, 1)

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_2, 0, 0, 1, 2)


        self.gridLayout_5.addLayout(self.gridLayout_4, 0, 1, 1, 4)

        self.groupBox_3 = QGroupBox(self.frame)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.horizontalLayoutWidget = QWidget(self.groupBox_3)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(20, 40, 448, 41))
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.LblCuentaContable = QLabel(self.horizontalLayoutWidget)
        self.LblCuentaContable.setObjectName(u"LblCuentaContable")

        self.horizontalLayout_2.addWidget(self.LblCuentaContable)

        self.txtCuenta_contable = QLineEdit(self.horizontalLayoutWidget)
        self.txtCuenta_contable.setObjectName(u"txtCuenta_contable")
        sizePolicy1.setHeightForWidth(self.txtCuenta_contable.sizePolicy().hasHeightForWidth())
        self.txtCuenta_contable.setSizePolicy(sizePolicy1)
        self.txtCuenta_contable.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_2.addWidget(self.txtCuenta_contable)

        self.btnBuscarCuentaContable = QPushButton(self.horizontalLayoutWidget)
        self.btnBuscarCuentaContable.setObjectName(u"btnBuscarCuentaContable")
        self.btnBuscarCuentaContable.setEnabled(False)
        self.btnBuscarCuentaContable.setIcon(icon6)

        self.horizontalLayout_2.addWidget(self.btnBuscarCuentaContable)


        self.gridLayout_5.addWidget(self.groupBox_3, 4, 1, 2, 3)


        self.gridLayout_6.addWidget(self.frame, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_2)

        self.gridLayout_2.addWidget(self.stackedWidget, 1, 0, 1, 1)

        QWidget.setTabOrder(self.btnAnadir_3, self.btnSiguiente_2)
        QWidget.setTabOrder(self.btnSiguiente_2, self.btnAnterior_2)
        QWidget.setTabOrder(self.btnAnterior_2, self.btnEditar_3)
        QWidget.setTabOrder(self.btnEditar_3, self.btnGuardar_2)
        QWidget.setTabOrder(self.btnGuardar_2, self.btndeshacer_2)
        QWidget.setTabOrder(self.btndeshacer_2, self.btnBuscar_2)
        QWidget.setTabOrder(self.btnBuscar_2, self.txtcod_forma_pago)
        QWidget.setTabOrder(self.txtcod_forma_pago, self.txtForma_pago)
        QWidget.setTabOrder(self.txtForma_pago, self.rdbContado)
        QWidget.setTabOrder(self.rdbContado, self.radioButton_2)
        QWidget.setTabOrder(self.radioButton_2, self.txtPorcentajeInicial)
        QWidget.setTabOrder(self.txtPorcentajeInicial, self.txtPorcentajeFinal)
        QWidget.setTabOrder(self.txtPorcentajeFinal, self.spinDia_pago1)
        QWidget.setTabOrder(self.spinDia_pago1, self.spinDia_pago2)
        QWidget.setTabOrder(self.spinDia_pago2, self.spinDia_pago3)
        QWidget.setTabOrder(self.spinDia_pago3, self.spinDia_pago4)
        QWidget.setTabOrder(self.spinDia_pago4, self.dias_hasta_pago)
        QWidget.setTabOrder(self.dias_hasta_pago, self.spinNumero_plazos)
        QWidget.setTabOrder(self.spinNumero_plazos, self.spinDias_entre_plazos)
        QWidget.setTabOrder(self.spinDias_entre_plazos, self.txtCuenta_contable)
        QWidget.setTabOrder(self.txtCuenta_contable, self.btnBuscarCuentaContable)
        QWidget.setTabOrder(self.btnBuscarCuentaContable, self.btn_borrar)
        QWidget.setTabOrder(self.btn_borrar, self.textEdit)
        QWidget.setTabOrder(self.textEdit, self.tabla_buscar)

        self.retranslateUi(FrmFormas_pago)
        self.radioButton_2.toggled.connect(self.groupBox.setEnabled)

        self.stackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(FrmFormas_pago)
    # setupUi

    def retranslateUi(self, FrmFormas_pago):
        FrmFormas_pago.setWindowTitle(QCoreApplication.translate("FrmFormas_pago", u"Gesti\u00f3n de Formas de Pago", None))
        self.label_36.setText(QCoreApplication.translate("FrmFormas_pago", u"Formas de Pago", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("FrmFormas_pago", u"% Inicial / % al finalizar proyecto", None))
        self.label_4.setText(QCoreApplication.translate("FrmFormas_pago", u"Inicial:", None))
        self.label_5.setText(QCoreApplication.translate("FrmFormas_pago", u"Final:", None))
        self.btnAnadir_3.setText(QCoreApplication.translate("FrmFormas_pago", u"&Nueva", None))
        self.btnSiguiente_2.setText(QCoreApplication.translate("FrmFormas_pago", u"Siguient&e", None))
        self.btnAnterior_2.setText(QCoreApplication.translate("FrmFormas_pago", u"&Anterior", None))
        self.btnEditar_3.setText(QCoreApplication.translate("FrmFormas_pago", u"Editar", None))
#if QT_CONFIG(shortcut)
        self.btnEditar_3.setShortcut(QCoreApplication.translate("FrmFormas_pago", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.btnGuardar_2.setText(QCoreApplication.translate("FrmFormas_pago", u"Guardar", None))
        self.btndeshacer_2.setText(QCoreApplication.translate("FrmFormas_pago", u"Deshacer", None))
        self.btnBuscar_2.setText(QCoreApplication.translate("FrmFormas_pago", u"Buscar", None))
        self.btn_borrar.setText(QCoreApplication.translate("FrmFormas_pago", u"Borrar", None))
        self.textEdit.setHtml(QCoreApplication.translate("FrmFormas_pago", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Noto Sans'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:600; text-decoration: underline;\">Dias de Pago:</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Sans Serif'; font-size:9pt; font-weight:600; text-decoration: underline;\"><br /></p>\n"
"<p style=\" margin-top:"
                        "0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt;\">Introducir los d\u00edas en los que se va a generar un vencimiento.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt;\">Cretive ERP se encargar\u00e1 de calcular la fecha del proximo vencimiento considerando el d\u00eda mayor m\u00e1s cercano.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Sans Serif'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:600; text-decoration: underline;\">Plazos:</span></p>\n"
"<p style=\"-qt-para"
                        "graph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Sans Serif'; font-size:9pt; font-weight:600; text-decoration: underline;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:600;\">D\u00edas entre plazos: Creative ERP</span><span style=\" font-family:'Sans Serif'; font-size:9pt;\">sumar\u00e1 estos d\u00edas al ultimo vencimiento y buscar\u00e1 el d\u00eda mayor m\u00e1s cercano.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Sans Serif'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt; font-"
                        "weight:600;\">Numero de Plazos:</span><span style=\" font-family:'Sans Serif'; font-size:9pt;\"> Valor m\u00ednimo 1, correspondiente a un solo vencimiento, incrementar hasta alcanzar el numero de vencimientos deseados. Creative ERP se encargar\u00e1 de generar todos los vencimientos con la fecha correspondiente.</span></p></body></html>", None))
        self.rdbContado.setText(QCoreApplication.translate("FrmFormas_pago", u"Pago al contado", None))
        self.radioButton_2.setText(QCoreApplication.translate("FrmFormas_pago", u"Pago aplazado", None))
        self.groupBox.setTitle(QCoreApplication.translate("FrmFormas_pago", u"Configuracion de pago aplazado", None))
        self.label_14.setText(QCoreApplication.translate("FrmFormas_pago", u"D\u00edas de pago", None))
        self.label_13.setText(QCoreApplication.translate("FrmFormas_pago", u"Dia pago 4:", None))
        self.label_12.setText(QCoreApplication.translate("FrmFormas_pago", u"Dia pago 3:", None))
        self.label_11.setText(QCoreApplication.translate("FrmFormas_pago", u"Dia pago 2:", None))
        self.label_16.setText(QCoreApplication.translate("FrmFormas_pago", u"Plazos", None))
        self.label_10.setText(QCoreApplication.translate("FrmFormas_pago", u"Dia pago 1:", None))
        self.label_3.setText(QCoreApplication.translate("FrmFormas_pago", u"Dias hasta el primer pago:", None))
        self.label_18.setText(QCoreApplication.translate("FrmFormas_pago", u"Numero de Plazos:", None))
        self.label_15.setText(QCoreApplication.translate("FrmFormas_pago", u"Dias entre plazos:", None))
        self.label.setText(QCoreApplication.translate("FrmFormas_pago", u"Descripci\u00f3n", None))
        self.label_2.setText(QCoreApplication.translate("FrmFormas_pago", u"Codigo", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("FrmFormas_pago", u"Contablilidad", None))
        self.LblCuentaContable.setText(QCoreApplication.translate("FrmFormas_pago", u"Cuenta contable:", None))
        self.btnBuscarCuentaContable.setText(QCoreApplication.translate("FrmFormas_pago", u"Buscar cuenta contable", None))
    # retranslateUi

