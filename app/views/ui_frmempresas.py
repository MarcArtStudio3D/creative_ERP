# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frmempresas.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QDoubleSpinBox, QFrame, QGridLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QStackedWidget, QTabWidget, QTableView, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_FrmEmpresas(object):
    def setupUi(self, FrmEmpresas):
        if not FrmEmpresas.objectName():
            FrmEmpresas.setObjectName(u"FrmEmpresas")
        FrmEmpresas.resize(1261, 751)
        icon = QIcon()
        icon.addFile(u":/Icons/PNG/NeuX.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        FrmEmpresas.setWindowIcon(icon)
        self.gridLayout_2 = QGridLayout(FrmEmpresas)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.stackedWidget = QStackedWidget(FrmEmpresas)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.create_page_empresa = QWidget()
        self.create_page_empresa.setObjectName(u"create_page_empresa")
        self.gridLayout_14 = QGridLayout(self.create_page_empresa)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.btn_guardar_nuevo = QPushButton(self.create_page_empresa)
        self.btn_guardar_nuevo.setObjectName(u"btn_guardar_nuevo")
        icon1 = QIcon()
        icon1.addFile(u":/Icons/PNG/Save.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_guardar_nuevo.setIcon(icon1)

        self.gridLayout_14.addWidget(self.btn_guardar_nuevo, 3, 0, 1, 1)

        self.pushButton = QPushButton(self.create_page_empresa)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout_14.addWidget(self.pushButton, 4, 0, 1, 1)

        self.tabWidget = QTabWidget(self.create_page_empresa)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setMaximumSize(QSize(1216, 16777215))
        self.tabWidget.setStyleSheet(u"")
        self.tabWidgetPage1 = QWidget()
        self.tabWidgetPage1.setObjectName(u"tabWidgetPage1")
        self.gridLayout_12 = QGridLayout(self.tabWidgetPage1)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.label_22 = QLabel(self.tabWidgetPage1)
        self.label_22.setObjectName(u"label_22")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_22.sizePolicy().hasHeightForWidth())
        self.label_22.setSizePolicy(sizePolicy)
        self.label_22.setMinimumSize(QSize(66, 0))

        self.gridLayout_12.addWidget(self.label_22, 6, 0, 1, 1)

        self.label_17 = QLabel(self.tabWidgetPage1)
        self.label_17.setObjectName(u"label_17")
        sizePolicy.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy)
        self.label_17.setMinimumSize(QSize(80, 0))

        self.gridLayout_12.addWidget(self.label_17, 10, 0, 1, 2)

        self.txtcMail = QLineEdit(self.tabWidgetPage1)
        self.txtcMail.setObjectName(u"txtcMail")

        self.gridLayout_12.addWidget(self.txtcMail, 15, 3, 1, 1)

        self.label_53 = QLabel(self.tabWidgetPage1)
        self.label_53.setObjectName(u"label_53")

        self.gridLayout_12.addWidget(self.label_53, 7, 0, 1, 1)

        self.label_74 = QLabel(self.tabWidgetPage1)
        self.label_74.setObjectName(u"label_74")

        self.gridLayout_12.addWidget(self.label_74, 0, 0, 1, 1)

        self.txttelefono1 = QLineEdit(self.tabWidgetPage1)
        self.txttelefono1.setObjectName(u"txttelefono1")
        self.txttelefono1.setMaximumSize(QSize(150, 16777215))
        self.txttelefono1.setClearButtonEnabled(True)

        self.gridLayout_12.addWidget(self.txttelefono1, 10, 3, 1, 1)

        self.label_15 = QLabel(self.tabWidgetPage1)
        self.label_15.setObjectName(u"label_15")
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)

        self.gridLayout_12.addWidget(self.label_15, 5, 0, 1, 2)

        self.txtcInscripcion = QLineEdit(self.tabWidgetPage1)
        self.txtcInscripcion.setObjectName(u"txtcInscripcion")
        self.txtcInscripcion.setClearButtonEnabled(True)

        self.gridLayout_12.addWidget(self.txtcInscripcion, 9, 3, 1, 1)

        self.txtMovil = QLineEdit(self.tabWidgetPage1)
        self.txtMovil.setObjectName(u"txtMovil")
        self.txtMovil.setMaximumSize(QSize(150, 16777215))

        self.gridLayout_12.addWidget(self.txtMovil, 13, 3, 1, 1)

        self.txttelefono2 = QLineEdit(self.tabWidgetPage1)
        self.txttelefono2.setObjectName(u"txttelefono2")
        self.txttelefono2.setMaximumSize(QSize(150, 16777215))
        self.txttelefono2.setClearButtonEnabled(True)

        self.gridLayout_12.addWidget(self.txttelefono2, 11, 3, 1, 1)

        self.txtweb = QLineEdit(self.tabWidgetPage1)
        self.txtweb.setObjectName(u"txtweb")

        self.gridLayout_12.addWidget(self.txtweb, 16, 3, 1, 1)

        self.label_19 = QLabel(self.tabWidgetPage1)
        self.label_19.setObjectName(u"label_19")
        sizePolicy.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy)
        self.label_19.setMinimumSize(QSize(80, 0))

        self.gridLayout_12.addWidget(self.label_19, 13, 0, 1, 1)

        self.txtNombreComercial = QLineEdit(self.tabWidgetPage1)
        self.txtNombreComercial.setObjectName(u"txtNombreComercial")

        self.gridLayout_12.addWidget(self.txtNombreComercial, 1, 3, 1, 1)

        self.label_23 = QLabel(self.tabWidgetPage1)
        self.label_23.setObjectName(u"label_23")
        sizePolicy.setHeightForWidth(self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy)

        self.gridLayout_12.addWidget(self.label_23, 9, 0, 1, 2)

        self.label_13 = QLabel(self.tabWidgetPage1)
        self.label_13.setObjectName(u"label_13")
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)

        self.gridLayout_12.addWidget(self.label_13, 3, 0, 1, 2)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.lineEdit_4 = QLineEdit(self.tabWidgetPage1)
        self.lineEdit_4.setObjectName(u"lineEdit_4")

        self.horizontalLayout_7.addWidget(self.lineEdit_4)

        self.label_54 = QLabel(self.tabWidgetPage1)
        self.label_54.setObjectName(u"label_54")

        self.horizontalLayout_7.addWidget(self.label_54)

        self.lineEdit_5 = QLineEdit(self.tabWidgetPage1)
        self.lineEdit_5.setObjectName(u"lineEdit_5")

        self.horizontalLayout_7.addWidget(self.lineEdit_5)

        self.label_57 = QLabel(self.tabWidgetPage1)
        self.label_57.setObjectName(u"label_57")

        self.horizontalLayout_7.addWidget(self.label_57)

        self.lineEdit_6 = QLineEdit(self.tabWidgetPage1)
        self.lineEdit_6.setObjectName(u"lineEdit_6")

        self.horizontalLayout_7.addWidget(self.lineEdit_6)


        self.gridLayout_12.addLayout(self.horizontalLayout_7, 7, 3, 1, 1)

        self.label_20 = QLabel(self.tabWidgetPage1)
        self.label_20.setObjectName(u"label_20")
        sizePolicy.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy)
        self.label_20.setMinimumSize(QSize(80, 0))

        self.gridLayout_12.addWidget(self.label_20, 15, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.txtprovincia = QLineEdit(self.tabWidgetPage1)
        self.txtprovincia.setObjectName(u"txtprovincia")
        self.txtprovincia.setClearButtonEnabled(True)

        self.horizontalLayout_2.addWidget(self.txtprovincia)

        self.label_16 = QLabel(self.tabWidgetPage1)
        self.label_16.setObjectName(u"label_16")
        sizePolicy.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.label_16)

        self.cboPais_create = QComboBox(self.tabWidgetPage1)
        self.cboPais_create.setObjectName(u"cboPais_create")
        self.cboPais_create.setMinimumSize(QSize(168, 0))
        self.cboPais_create.setMaximumSize(QSize(250, 16777215))

        self.horizontalLayout_2.addWidget(self.cboPais_create)


        self.gridLayout_12.addLayout(self.horizontalLayout_2, 5, 3, 1, 1)

        self.label_18 = QLabel(self.tabWidgetPage1)
        self.label_18.setObjectName(u"label_18")
        sizePolicy.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy)
        self.label_18.setMinimumSize(QSize(80, 0))

        self.gridLayout_12.addWidget(self.label_18, 11, 0, 1, 2)

        self.label_21 = QLabel(self.tabWidgetPage1)
        self.label_21.setObjectName(u"label_21")
        sizePolicy.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy)
        self.label_21.setMinimumSize(QSize(80, 0))

        self.gridLayout_12.addWidget(self.label_21, 16, 0, 1, 2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.txtcodigo = QLineEdit(self.tabWidgetPage1)
        self.txtcodigo.setObjectName(u"txtcodigo")
        self.txtcodigo.setMaximumSize(QSize(100, 16777215))
        self.txtcodigo.setReadOnly(False)
        self.txtcodigo.setClearButtonEnabled(True)

        self.horizontalLayout_4.addWidget(self.txtcodigo)

        self.label_75 = QLabel(self.tabWidgetPage1)
        self.label_75.setObjectName(u"label_75")

        self.horizontalLayout_4.addWidget(self.label_75)

        self.txtEmpresa = QLineEdit(self.tabWidgetPage1)
        self.txtEmpresa.setObjectName(u"txtEmpresa")
        self.txtEmpresa.setMinimumSize(QSize(332, 0))
        self.txtEmpresa.setMaximumSize(QSize(16777215, 16777215))
        self.txtEmpresa.setReadOnly(False)
        self.txtEmpresa.setClearButtonEnabled(True)

        self.horizontalLayout_4.addWidget(self.txtEmpresa)

        self.label_24 = QLabel(self.tabWidgetPage1)
        self.label_24.setObjectName(u"label_24")

        self.horizontalLayout_4.addWidget(self.label_24)

        self.cboFormajuridica = QComboBox(self.tabWidgetPage1)
        self.cboFormajuridica.addItem("")
        self.cboFormajuridica.addItem("")
        self.cboFormajuridica.addItem("")
        self.cboFormajuridica.addItem("")
        self.cboFormajuridica.addItem("")
        self.cboFormajuridica.addItem("")
        self.cboFormajuridica.addItem("")
        self.cboFormajuridica.addItem("")
        self.cboFormajuridica.addItem("")
        self.cboFormajuridica.addItem("")
        self.cboFormajuridica.addItem("")
        self.cboFormajuridica.setObjectName(u"cboFormajuridica")
        self.cboFormajuridica.setMaximumSize(QSize(205, 16777215))
        self.cboFormajuridica.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.cboFormajuridica.setMinimumContentsLength(150)

        self.horizontalLayout_4.addWidget(self.cboFormajuridica)

        self.label_6 = QLabel(self.tabWidgetPage1)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_4.addWidget(self.label_6)

        self.cboGrupoEmpresa = QComboBox(self.tabWidgetPage1)
        self.cboGrupoEmpresa.setObjectName(u"cboGrupoEmpresa")
        self.cboGrupoEmpresa.setMinimumSize(QSize(152, 0))
        self.cboGrupoEmpresa.setEditable(False)

        self.horizontalLayout_4.addWidget(self.cboGrupoEmpresa)


        self.gridLayout_12.addLayout(self.horizontalLayout_4, 0, 3, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.txtcif = QLineEdit(self.tabWidgetPage1)
        self.txtcif.setObjectName(u"txtcif")
        self.txtcif.setMaximumSize(QSize(150, 16777215))
        self.txtcif.setClearButtonEnabled(True)

        self.horizontalLayout_6.addWidget(self.txtcif)

        self.label_32 = QLabel(self.tabWidgetPage1)
        self.label_32.setObjectName(u"label_32")

        self.horizontalLayout_6.addWidget(self.label_32)

        self.lineEdit_2 = QLineEdit(self.tabWidgetPage1)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.horizontalLayout_6.addWidget(self.lineEdit_2)

        self.label_34 = QLabel(self.tabWidgetPage1)
        self.label_34.setObjectName(u"label_34")

        self.horizontalLayout_6.addWidget(self.label_34)

        self.lineEdit_3 = QLineEdit(self.tabWidgetPage1)
        self.lineEdit_3.setObjectName(u"lineEdit_3")

        self.horizontalLayout_6.addWidget(self.lineEdit_3)

        self.chkTVA = QCheckBox(self.tabWidgetPage1)
        self.chkTVA.setObjectName(u"chkTVA")

        self.horizontalLayout_6.addWidget(self.chkTVA)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_9)


        self.gridLayout_12.addLayout(self.horizontalLayout_6, 6, 3, 1, 1)

        self.label_14 = QLabel(self.tabWidgetPage1)
        self.label_14.setObjectName(u"label_14")
        sizePolicy.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy)

        self.gridLayout_12.addWidget(self.label_14, 2, 0, 1, 1)

        self.label_43 = QLabel(self.tabWidgetPage1)
        self.label_43.setObjectName(u"label_43")

        self.gridLayout_12.addWidget(self.label_43, 1, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.txtcp = QLineEdit(self.tabWidgetPage1)
        self.txtcp.setObjectName(u"txtcp")
        self.txtcp.setMaximumSize(QSize(100, 16777215))
        self.txtcp.setClearButtonEnabled(True)

        self.horizontalLayout.addWidget(self.txtcp)

        self.label_50 = QLabel(self.tabWidgetPage1)
        self.label_50.setObjectName(u"label_50")

        self.horizontalLayout.addWidget(self.label_50)

        self.txtpoblacion = QLineEdit(self.tabWidgetPage1)
        self.txtpoblacion.setObjectName(u"txtpoblacion")
        self.txtpoblacion.setClearButtonEnabled(True)

        self.horizontalLayout.addWidget(self.txtpoblacion)


        self.gridLayout_12.addLayout(self.horizontalLayout, 2, 3, 1, 1)

        self.txtdireccion1 = QLineEdit(self.tabWidgetPage1)
        self.txtdireccion1.setObjectName(u"txtdireccion1")
        self.txtdireccion1.setClearButtonEnabled(True)

        self.gridLayout_12.addWidget(self.txtdireccion1, 3, 3, 1, 1)

        self.tabWidget.addTab(self.tabWidgetPage1, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_24 = QGridLayout(self.tab)
        self.gridLayout_24.setObjectName(u"gridLayout_24")
        self.tabWidget_2 = QTabWidget(self.tab)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        self.tabWidget_2.setEnabled(True)
        self.tabWidget_2.setMinimumSize(QSize(0, 0))
        self.tab_12 = QWidget()
        self.tab_12.setObjectName(u"tab_12")
        self.gridLayout_21 = QGridLayout(self.tab_12)
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.groupBox_14 = QGroupBox(self.tab_12)
        self.groupBox_14.setObjectName(u"groupBox_14")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBox_14.sizePolicy().hasHeightForWidth())
        self.groupBox_14.setSizePolicy(sizePolicy1)
        self.gridLayout_16 = QGridLayout(self.groupBox_14)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.cboDivisas = QComboBox(self.groupBox_14)
        self.cboDivisas.setObjectName(u"cboDivisas")

        self.gridLayout_16.addWidget(self.cboDivisas, 1, 1, 1, 1)

        self.chk_upate_divisas = QCheckBox(self.groupBox_14)
        self.chk_upate_divisas.setObjectName(u"chk_upate_divisas")

        self.gridLayout_16.addWidget(self.chk_upate_divisas, 0, 0, 1, 2)

        self.label_42 = QLabel(self.groupBox_14)
        self.label_42.setObjectName(u"label_42")
        sizePolicy.setHeightForWidth(self.label_42.sizePolicy().hasHeightForWidth())
        self.label_42.setSizePolicy(sizePolicy)

        self.gridLayout_16.addWidget(self.label_42, 1, 0, 1, 1)


        self.gridLayout_21.addWidget(self.groupBox_14, 2, 1, 1, 1)

        self.groupBox_4 = QGroupBox(self.tab_12)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.gridLayout_17 = QGridLayout(self.groupBox_4)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.chkIRPF = QCheckBox(self.groupBox_4)
        self.chkIRPF.setObjectName(u"chkIRPF")
        self.chkIRPF.setMaximumSize(QSize(135, 16777215))

        self.gridLayout_17.addWidget(self.chkIRPF, 1, 0, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_71 = QLabel(self.groupBox_4)
        self.label_71.setObjectName(u"label_71")

        self.horizontalLayout_5.addWidget(self.label_71)

        self.spinPorc_irpf = QDoubleSpinBox(self.groupBox_4)
        self.spinPorc_irpf.setObjectName(u"spinPorc_irpf")
        self.spinPorc_irpf.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.spinPorc_irpf.setMinimum(-999999.000000000000000)
        self.spinPorc_irpf.setMaximum(9999999.000000000000000)

        self.horizontalLayout_5.addWidget(self.spinPorc_irpf)


        self.gridLayout_17.addLayout(self.horizontalLayout_5, 2, 0, 1, 1)


        self.gridLayout_21.addWidget(self.groupBox_4, 3, 0, 1, 1)

        self.groupBox_12 = QGroupBox(self.tab_12)
        self.groupBox_12.setObjectName(u"groupBox_12")
        self.gridLayout_7 = QGridLayout(self.groupBox_12)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.label_222 = QLabel(self.groupBox_12)
        self.label_222.setObjectName(u"label_222")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_222.sizePolicy().hasHeightForWidth())
        self.label_222.setSizePolicy(sizePolicy2)

        self.gridLayout_7.addWidget(self.label_222, 0, 0, 1, 1)

        self.spinDecimales_create = QSpinBox(self.groupBox_12)
        self.spinDecimales_create.setObjectName(u"spinDecimales_create")
        self.spinDecimales_create.setValue(2)

        self.gridLayout_7.addWidget(self.spinDecimales_create, 0, 1, 1, 2)

        self.label_85 = QLabel(self.groupBox_12)
        self.label_85.setObjectName(u"label_85")

        self.gridLayout_7.addWidget(self.label_85, 1, 0, 1, 1)

        self.spinDecimales_precios_create = QSpinBox(self.groupBox_12)
        self.spinDecimales_precios_create.setObjectName(u"spinDecimales_precios_create")
        self.spinDecimales_precios_create.setValue(2)

        self.gridLayout_7.addWidget(self.spinDecimales_precios_create, 1, 1, 1, 2)


        self.gridLayout_21.addWidget(self.groupBox_12, 0, 2, 1, 1)

        self.groupBox_3 = QGroupBox(self.tab_12)
        self.groupBox_3.setObjectName(u"groupBox_3")
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.gridLayout_11 = QGridLayout(self.groupBox_3)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.label_25 = QLabel(self.groupBox_3)
        self.label_25.setObjectName(u"label_25")

        self.gridLayout_11.addWidget(self.label_25, 0, 0, 1, 1)

        self.spinDigitos = QSpinBox(self.groupBox_3)
        self.spinDigitos.setObjectName(u"spinDigitos")
        self.spinDigitos.setMaximum(45)
        self.spinDigitos.setValue(7)

        self.gridLayout_11.addWidget(self.spinDigitos, 0, 1, 1, 1)

        self.cboSerie = QComboBox(self.groupBox_3)
        self.cboSerie.setObjectName(u"cboSerie")

        self.gridLayout_11.addWidget(self.cboSerie, 1, 1, 1, 1)

        self.label_26 = QLabel(self.groupBox_3)
        self.label_26.setObjectName(u"label_26")

        self.gridLayout_11.addWidget(self.label_26, 1, 0, 1, 1)


        self.gridLayout_21.addWidget(self.groupBox_3, 3, 1, 1, 1)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_68 = QLabel(self.tab_12)
        self.label_68.setObjectName(u"label_68")

        self.horizontalLayout_8.addWidget(self.label_68)

        self.txtDiaCierre = QSpinBox(self.tab_12)
        self.txtDiaCierre.setObjectName(u"txtDiaCierre")
        self.txtDiaCierre.setMinimum(1)
        self.txtDiaCierre.setMaximum(31)
        self.txtDiaCierre.setValue(31)

        self.horizontalLayout_8.addWidget(self.txtDiaCierre)

        self.tstMesCierre = QSpinBox(self.tab_12)
        self.tstMesCierre.setObjectName(u"tstMesCierre")
        self.tstMesCierre.setMinimum(1)
        self.tstMesCierre.setMaximum(12)
        self.tstMesCierre.setValue(12)

        self.horizontalLayout_8.addWidget(self.tstMesCierre)


        self.gridLayout_21.addLayout(self.horizontalLayout_8, 1, 0, 1, 1)

        self.groupBox_5 = QGroupBox(self.tab_12)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.chkEnlace_web = QCheckBox(self.groupBox_5)
        self.chkEnlace_web.setObjectName(u"chkEnlace_web")
        self.chkEnlace_web.setGeometry(QRect(0, 50, 307, 22))
        self.chkInternacional = QCheckBox(self.groupBox_5)
        self.chkInternacional.setObjectName(u"chkInternacional")
        self.chkInternacional.setGeometry(QRect(0, 80, 307, 22))

        self.gridLayout_21.addWidget(self.groupBox_5, 0, 0, 1, 1)

        self.groupBox_2 = QGroupBox(self.tab_12)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_10 = QGridLayout(self.groupBox_2)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.chkAutocodificiar = QCheckBox(self.groupBox_2)
        self.chkAutocodificiar.setObjectName(u"chkAutocodificiar")
        self.chkAutocodificiar.setChecked(True)

        self.gridLayout_10.addWidget(self.chkAutocodificiar, 0, 0, 1, 1)

        self.txttamano_codigoart = QSpinBox(self.groupBox_2)
        self.txttamano_codigoart.setObjectName(u"txttamano_codigoart")
        self.txttamano_codigoart.setMaximumSize(QSize(60, 16777215))
        self.txttamano_codigoart.setValue(15)

        self.gridLayout_10.addWidget(self.txttamano_codigoart, 1, 1, 1, 1)

        self.label_41 = QLabel(self.groupBox_2)
        self.label_41.setObjectName(u"label_41")
        sizePolicy.setHeightForWidth(self.label_41.sizePolicy().hasHeightForWidth())
        self.label_41.setSizePolicy(sizePolicy)

        self.gridLayout_10.addWidget(self.label_41, 1, 0, 1, 1)


        self.gridLayout_21.addWidget(self.groupBox_2, 2, 0, 1, 1)

        self.groupBox = QGroupBox(self.tab_12)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_9 = QGridLayout(self.groupBox)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.spinMargen = QDoubleSpinBox(self.groupBox)
        self.spinMargen.setObjectName(u"spinMargen")

        self.gridLayout_9.addWidget(self.spinMargen, 1, 3, 1, 1)

        self.label_33 = QLabel(self.groupBox)
        self.label_33.setObjectName(u"label_33")

        self.gridLayout_9.addWidget(self.label_33, 2, 1, 1, 1)

        self.cboTarifa = QComboBox(self.groupBox)
        self.cboTarifa.setObjectName(u"cboTarifa")

        self.gridLayout_9.addWidget(self.cboTarifa, 0, 3, 1, 1)

        self.label_31 = QLabel(self.groupBox)
        self.label_31.setObjectName(u"label_31")

        self.gridLayout_9.addWidget(self.label_31, 1, 1, 1, 1)

        self.spinMargen_minimo = QDoubleSpinBox(self.groupBox)
        self.spinMargen_minimo.setObjectName(u"spinMargen_minimo")

        self.gridLayout_9.addWidget(self.spinMargen_minimo, 2, 3, 1, 1)

        self.label_58 = QLabel(self.groupBox)
        self.label_58.setObjectName(u"label_58")

        self.gridLayout_9.addWidget(self.label_58, 0, 1, 1, 1)


        self.gridLayout_21.addWidget(self.groupBox, 0, 1, 2, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.btnDeleteLogo = QPushButton(self.tab_12)
        self.btnDeleteLogo.setObjectName(u"btnDeleteLogo")

        self.gridLayout.addWidget(self.btnDeleteLogo, 2, 0, 1, 1)

        self.btnAddLogo = QPushButton(self.tab_12)
        self.btnAddLogo.setObjectName(u"btnAddLogo")

        self.gridLayout.addWidget(self.btnAddLogo, 1, 0, 1, 1)


        self.gridLayout_21.addLayout(self.gridLayout, 4, 2, 1, 1)

        self.groupBox_6 = QGroupBox(self.tab_12)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.imgLogo = QLabel(self.groupBox_6)
        self.imgLogo.setObjectName(u"imgLogo")
        self.imgLogo.setGeometry(QRect(20, 40, 431, 221))
        self.imgLogo.setMaximumSize(QSize(1211, 348))
        self.imgLogo.setPixmap(QPixmap(u":/Icons/PNG/Neux_red_fox.png"))
        self.imgLogo.setScaledContents(True)

        self.gridLayout_21.addWidget(self.groupBox_6, 1, 2, 3, 1)

        self.tabWidget_2.addTab(self.tab_12, "")
        self.tab_6 = QWidget()
        self.tab_6.setObjectName(u"tab_6")
        self.verticalLayout_5 = QVBoxLayout(self.tab_6)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_36 = QLabel(self.tab_6)
        self.label_36.setObjectName(u"label_36")
        self.label_36.setStyleSheet(u"background-color: rgb(0, 0, 127);\n"
"color: rgb(255, 255, 255);")
        self.label_36.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_5.addWidget(self.label_36)

        self.txtcCometarioAlbaran = QTextEdit(self.tab_6)
        self.txtcCometarioAlbaran.setObjectName(u"txtcCometarioAlbaran")

        self.verticalLayout_5.addWidget(self.txtcCometarioAlbaran)

        self.label_35 = QLabel(self.tab_6)
        self.label_35.setObjectName(u"label_35")
        self.label_35.setStyleSheet(u"background-color: rgb(0, 0, 127);\n"
"color: rgb(255, 255, 255);")
        self.label_35.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_5.addWidget(self.label_35)

        self.txtccomentario_factura = QTextEdit(self.tab_6)
        self.txtccomentario_factura.setObjectName(u"txtccomentario_factura")

        self.verticalLayout_5.addWidget(self.txtccomentario_factura)

        self.tabWidget_2.addTab(self.tab_6, "")
        self.tab_8 = QWidget()
        self.tab_8.setObjectName(u"tab_8")
        self.gridLayout_15 = QGridLayout(self.tab_8)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.lineEdit_9 = QLineEdit(self.tab_8)
        self.lineEdit_9.setObjectName(u"lineEdit_9")

        self.gridLayout_15.addWidget(self.lineEdit_9, 5, 1, 1, 1)

        self.label_47 = QLabel(self.tab_8)
        self.label_47.setObjectName(u"label_47")

        self.gridLayout_15.addWidget(self.label_47, 1, 0, 1, 1)

        self.lineEdit_7 = QLineEdit(self.tab_8)
        self.lineEdit_7.setObjectName(u"lineEdit_7")

        self.gridLayout_15.addWidget(self.lineEdit_7, 3, 1, 1, 1)

        self.txt_horario_primer_dia = QLineEdit(self.tab_8)
        self.txt_horario_primer_dia.setObjectName(u"txt_horario_primer_dia")
        self.txt_horario_primer_dia.setClearButtonEnabled(True)

        self.gridLayout_15.addWidget(self.txt_horario_primer_dia, 0, 1, 1, 1)

        self.label_46 = QLabel(self.tab_8)
        self.label_46.setObjectName(u"label_46")

        self.gridLayout_15.addWidget(self.label_46, 0, 0, 1, 1)

        self.label_45 = QLabel(self.tab_8)
        self.label_45.setObjectName(u"label_45")

        self.gridLayout_15.addWidget(self.label_45, 4, 0, 1, 1)

        self.label_70 = QLabel(self.tab_8)
        self.label_70.setObjectName(u"label_70")

        self.gridLayout_15.addWidget(self.label_70, 6, 0, 1, 1)

        self.label_44 = QLabel(self.tab_8)
        self.label_44.setObjectName(u"label_44")

        self.gridLayout_15.addWidget(self.label_44, 3, 0, 1, 1)

        self.txt_horario_dia_normal = QLineEdit(self.tab_8)
        self.txt_horario_dia_normal.setObjectName(u"txt_horario_dia_normal")
        self.txt_horario_dia_normal.setClearButtonEnabled(True)

        self.gridLayout_15.addWidget(self.txt_horario_dia_normal, 1, 1, 1, 1)

        self.label_69 = QLabel(self.tab_8)
        self.label_69.setObjectName(u"label_69")

        self.gridLayout_15.addWidget(self.label_69, 5, 0, 1, 1)

        self.txt_horario_ultimo_dia = QLineEdit(self.tab_8)
        self.txt_horario_ultimo_dia.setObjectName(u"txt_horario_ultimo_dia")
        self.txt_horario_ultimo_dia.setClearButtonEnabled(True)

        self.gridLayout_15.addWidget(self.txt_horario_ultimo_dia, 2, 1, 1, 1)

        self.label_48 = QLabel(self.tab_8)
        self.label_48.setObjectName(u"label_48")

        self.gridLayout_15.addWidget(self.label_48, 2, 0, 1, 1)

        self.groupBox_7 = QGroupBox(self.tab_8)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.lineEdit_11 = QLineEdit(self.groupBox_7)
        self.lineEdit_11.setObjectName(u"lineEdit_11")
        self.lineEdit_11.setGeometry(QRect(190, 40, 341, 32))
        self.lineEdit_12 = QLineEdit(self.groupBox_7)
        self.lineEdit_12.setObjectName(u"lineEdit_12")
        self.lineEdit_12.setGeometry(QRect(190, 80, 341, 32))
        self.lineEdit_13 = QLineEdit(self.groupBox_7)
        self.lineEdit_13.setObjectName(u"lineEdit_13")
        self.lineEdit_13.setGeometry(QRect(190, 120, 341, 32))
        self.lineEdit_14 = QLineEdit(self.groupBox_7)
        self.lineEdit_14.setObjectName(u"lineEdit_14")
        self.lineEdit_14.setGeometry(QRect(190, 160, 341, 32))
        self.label_72 = QLabel(self.groupBox_7)
        self.label_72.setObjectName(u"label_72")
        self.label_72.setGeometry(QRect(20, 50, 161, 18))
        self.label_73 = QLabel(self.groupBox_7)
        self.label_73.setObjectName(u"label_73")
        self.label_73.setGeometry(QRect(20, 90, 161, 18))
        self.label_76 = QLabel(self.groupBox_7)
        self.label_76.setObjectName(u"label_76")
        self.label_76.setGeometry(QRect(20, 130, 161, 18))
        self.label_77 = QLabel(self.groupBox_7)
        self.label_77.setObjectName(u"label_77")
        self.label_77.setGeometry(QRect(20, 170, 161, 18))

        self.gridLayout_15.addWidget(self.groupBox_7, 7, 1, 1, 1)

        self.lineEdit_10 = QLineEdit(self.tab_8)
        self.lineEdit_10.setObjectName(u"lineEdit_10")

        self.gridLayout_15.addWidget(self.lineEdit_10, 6, 1, 1, 1)

        self.lineEdit_8 = QLineEdit(self.tab_8)
        self.lineEdit_8.setObjectName(u"lineEdit_8")

        self.gridLayout_15.addWidget(self.lineEdit_8, 4, 1, 1, 1)

        self.tabWidget_2.addTab(self.tab_8, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.verticalLayout = QVBoxLayout(self.tab_5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.chkContabilidad = QCheckBox(self.tab_5)
        self.chkContabilidad.setObjectName(u"chkContabilidad")
        self.chkContabilidad.setChecked(True)

        self.verticalLayout.addWidget(self.chkContabilidad)

        self.gridLayout_8 = QGridLayout()
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.txtCuenta_venta_servicios = QLineEdit(self.tab_5)
        self.txtCuenta_venta_servicios.setObjectName(u"txtCuenta_venta_servicios")
        self.txtCuenta_venta_servicios.setMaximumSize(QSize(200, 16777215))
        self.txtCuenta_venta_servicios.setClearButtonEnabled(True)

        self.gridLayout_8.addWidget(self.txtCuenta_venta_servicios, 5, 1, 1, 1)

        self.txtCuenta_venta_mercaderias = QLineEdit(self.tab_5)
        self.txtCuenta_venta_mercaderias.setObjectName(u"txtCuenta_venta_mercaderias")
        self.txtCuenta_venta_mercaderias.setMaximumSize(QSize(200, 16777215))
        self.txtCuenta_venta_mercaderias.setClearButtonEnabled(True)

        self.gridLayout_8.addWidget(self.txtCuenta_venta_mercaderias, 4, 1, 1, 1)

        self.txtcuenta_acreedores = QLineEdit(self.tab_5)
        self.txtcuenta_acreedores.setObjectName(u"txtcuenta_acreedores")
        self.txtcuenta_acreedores.setMaximumSize(QSize(200, 16777215))
        self.txtcuenta_acreedores.setClearButtonEnabled(True)

        self.gridLayout_8.addWidget(self.txtcuenta_acreedores, 3, 1, 1, 1)

        self.label_29 = QLabel(self.tab_5)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_29, 3, 0, 1, 1)

        self.label_12 = QLabel(self.tab_5)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_12, 4, 0, 1, 1)

        self.label_37 = QLabel(self.tab_5)
        self.label_37.setObjectName(u"label_37")
        self.label_37.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_37, 5, 0, 1, 1)

        self.label_28 = QLabel(self.tab_5)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_28, 2, 0, 1, 1)

        self.txtcuenta_proveedores = QLineEdit(self.tab_5)
        self.txtcuenta_proveedores.setObjectName(u"txtcuenta_proveedores")
        self.txtcuenta_proveedores.setMaximumSize(QSize(200, 16777215))
        self.txtcuenta_proveedores.setClearButtonEnabled(True)

        self.gridLayout_8.addWidget(self.txtcuenta_proveedores, 2, 1, 1, 1)

        self.txtdigitos_cuentas = QSpinBox(self.tab_5)
        self.txtdigitos_cuentas.setObjectName(u"txtdigitos_cuentas")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.txtdigitos_cuentas.sizePolicy().hasHeightForWidth())
        self.txtdigitos_cuentas.setSizePolicy(sizePolicy3)
        self.txtdigitos_cuentas.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.txtdigitos_cuentas.setMaximum(20)
        self.txtdigitos_cuentas.setValue(8)

        self.gridLayout_8.addWidget(self.txtdigitos_cuentas, 0, 1, 1, 1)

        self.txtcuentaCliente = QLineEdit(self.tab_5)
        self.txtcuentaCliente.setObjectName(u"txtcuentaCliente")
        self.txtcuentaCliente.setMaximumSize(QSize(200, 16777215))
        self.txtcuentaCliente.setClearButtonEnabled(True)

        self.gridLayout_8.addWidget(self.txtcuentaCliente, 1, 1, 1, 1)

        self.label_30 = QLabel(self.tab_5)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_30, 0, 0, 1, 1)

        self.label_27 = QLabel(self.tab_5)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_27, 1, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_2, 1, 2, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_8)

        self.gridLayout_13 = QGridLayout()
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.ivarepercutidore1 = QLineEdit(self.tab_5)
        self.ivarepercutidore1.setObjectName(u"ivarepercutidore1")
        self.ivarepercutidore1.setClearButtonEnabled(True)

        self.gridLayout_13.addWidget(self.ivarepercutidore1, 1, 5, 1, 1)

        self.ivarepercutido3 = QLineEdit(self.tab_5)
        self.ivarepercutido3.setObjectName(u"ivarepercutido3")
        self.ivarepercutido3.setClearButtonEnabled(True)

        self.gridLayout_13.addWidget(self.ivarepercutido3, 3, 4, 1, 1)

        self.label_65 = QLabel(self.tab_5)
        self.label_65.setObjectName(u"label_65")

        self.gridLayout_13.addWidget(self.label_65, 4, 3, 1, 1)

        self.ivasoportado4 = QLineEdit(self.tab_5)
        self.ivasoportado4.setObjectName(u"ivasoportado4")
        self.ivasoportado4.setClearButtonEnabled(True)

        self.gridLayout_13.addWidget(self.ivasoportado4, 4, 1, 1, 1)

        self.label_59 = QLabel(self.tab_5)
        self.label_59.setObjectName(u"label_59")

        self.gridLayout_13.addWidget(self.label_59, 2, 0, 1, 1)

        self.ivasoportado2 = QLineEdit(self.tab_5)
        self.ivasoportado2.setObjectName(u"ivasoportado2")
        self.ivasoportado2.setClearButtonEnabled(True)

        self.gridLayout_13.addWidget(self.ivasoportado2, 2, 1, 1, 1)

        self.label_63 = QLabel(self.tab_5)
        self.label_63.setObjectName(u"label_63")

        self.gridLayout_13.addWidget(self.label_63, 2, 3, 1, 1)

        self.label_38 = QLabel(self.tab_5)
        self.label_38.setObjectName(u"label_38")
        self.label_38.setMaximumSize(QSize(16777214, 15))
        self.label_38.setStyleSheet(u"background-color: rgb(0, 0, 127);\n"
"border-color: rgb(0, 0, 42);\n"
"color: rgb(255, 255, 255);")
        self.label_38.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_13.addWidget(self.label_38, 0, 1, 1, 1)

        self.ivasoportadore4 = QLineEdit(self.tab_5)
        self.ivasoportadore4.setObjectName(u"ivasoportadore4")
        self.ivasoportadore4.setClearButtonEnabled(True)

        self.gridLayout_13.addWidget(self.ivasoportadore4, 4, 2, 1, 1)

        self.ivasoportadore3 = QLineEdit(self.tab_5)
        self.ivasoportadore3.setObjectName(u"ivasoportadore3")
        self.ivasoportadore3.setClearButtonEnabled(True)

        self.gridLayout_13.addWidget(self.ivasoportadore3, 3, 2, 1, 1)

        self.label_39 = QLabel(self.tab_5)
        self.label_39.setObjectName(u"label_39")
        self.label_39.setMaximumSize(QSize(16777214, 15))
        self.label_39.setStyleSheet(u"background-color: rgb(0, 0, 127);\n"
"border-color: rgb(0, 0, 42);\n"
"color: rgb(255, 255, 255);")
        self.label_39.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_13.addWidget(self.label_39, 0, 4, 1, 1)

        self.label_40 = QLabel(self.tab_5)
        self.label_40.setObjectName(u"label_40")

        self.gridLayout_13.addWidget(self.label_40, 1, 0, 1, 1)

        self.label_62 = QLabel(self.tab_5)
        self.label_62.setObjectName(u"label_62")

        self.gridLayout_13.addWidget(self.label_62, 1, 3, 1, 1)

        self.ivasoportado1 = QLineEdit(self.tab_5)
        self.ivasoportado1.setObjectName(u"ivasoportado1")
        self.ivasoportado1.setClearButtonEnabled(True)

        self.gridLayout_13.addWidget(self.ivasoportado1, 1, 1, 1, 1)

        self.ivarepercutido1 = QLineEdit(self.tab_5)
        self.ivarepercutido1.setObjectName(u"ivarepercutido1")
        self.ivarepercutido1.setClearButtonEnabled(True)

        self.gridLayout_13.addWidget(self.ivarepercutido1, 1, 4, 1, 1)

        self.ivarepercutido4 = QLineEdit(self.tab_5)
        self.ivarepercutido4.setObjectName(u"ivarepercutido4")
        self.ivarepercutido4.setClearButtonEnabled(True)

        self.gridLayout_13.addWidget(self.ivarepercutido4, 4, 4, 1, 1)

        self.ivarepercutido2 = QLineEdit(self.tab_5)
        self.ivarepercutido2.setObjectName(u"ivarepercutido2")
        self.ivarepercutido2.setClearButtonEnabled(True)

        self.gridLayout_13.addWidget(self.ivarepercutido2, 2, 4, 1, 1)

        self.label_60 = QLabel(self.tab_5)
        self.label_60.setObjectName(u"label_60")

        self.gridLayout_13.addWidget(self.label_60, 3, 0, 1, 1)

        self.ivasoportado3 = QLineEdit(self.tab_5)
        self.ivasoportado3.setObjectName(u"ivasoportado3")
        self.ivasoportado3.setClearButtonEnabled(True)

        self.gridLayout_13.addWidget(self.ivasoportado3, 3, 1, 1, 1)

        self.label_64 = QLabel(self.tab_5)
        self.label_64.setObjectName(u"label_64")

        self.gridLayout_13.addWidget(self.label_64, 3, 3, 1, 1)

        self.label_61 = QLabel(self.tab_5)
        self.label_61.setObjectName(u"label_61")

        self.gridLayout_13.addWidget(self.label_61, 4, 0, 1, 1)

        self.ivasoportadore1 = QLineEdit(self.tab_5)
        self.ivasoportadore1.setObjectName(u"ivasoportadore1")
        self.ivasoportadore1.setClearButtonEnabled(True)

        self.gridLayout_13.addWidget(self.ivasoportadore1, 1, 2, 1, 1)

        self.ivasoportadore2 = QLineEdit(self.tab_5)
        self.ivasoportadore2.setObjectName(u"ivasoportadore2")
        self.ivasoportadore2.setClearButtonEnabled(True)

        self.gridLayout_13.addWidget(self.ivasoportadore2, 2, 2, 1, 1)

        self.label_66 = QLabel(self.tab_5)
        self.label_66.setObjectName(u"label_66")
        self.label_66.setMaximumSize(QSize(16777214, 15))
        self.label_66.setStyleSheet(u"background-color: rgb(0, 0, 127);\n"
"color: rgb(255, 255, 255);")

        self.gridLayout_13.addWidget(self.label_66, 0, 2, 1, 1)

        self.label_67 = QLabel(self.tab_5)
        self.label_67.setObjectName(u"label_67")
        self.label_67.setMaximumSize(QSize(16777214, 15))
        self.label_67.setStyleSheet(u"background-color: rgb(0, 0, 127);\n"
"color: rgb(255, 255, 255);")

        self.gridLayout_13.addWidget(self.label_67, 0, 5, 1, 1)

        self.ivarepercutidore3 = QLineEdit(self.tab_5)
        self.ivarepercutidore3.setObjectName(u"ivarepercutidore3")
        self.ivarepercutidore3.setClearButtonEnabled(True)

        self.gridLayout_13.addWidget(self.ivarepercutidore3, 3, 5, 1, 1)

        self.ivarepercutidore2 = QLineEdit(self.tab_5)
        self.ivarepercutidore2.setObjectName(u"ivarepercutidore2")
        self.ivarepercutidore2.setClearButtonEnabled(True)

        self.gridLayout_13.addWidget(self.ivarepercutidore2, 2, 5, 1, 1)

        self.ivarepercutidore4 = QLineEdit(self.tab_5)
        self.ivarepercutidore4.setObjectName(u"ivarepercutidore4")
        self.ivarepercutidore4.setClearButtonEnabled(True)

        self.gridLayout_13.addWidget(self.ivarepercutidore4, 4, 5, 1, 1)

        self.label_9 = QLabel(self.tab_5)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_13.addWidget(self.label_9, 5, 1, 1, 1)

        self.txtcuenta_cobros = QLineEdit(self.tab_5)
        self.txtcuenta_cobros.setObjectName(u"txtcuenta_cobros")

        self.gridLayout_13.addWidget(self.txtcuenta_cobros, 5, 2, 1, 1)

        self.label_10 = QLabel(self.tab_5)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_13.addWidget(self.label_10, 5, 4, 1, 1)

        self.txtcuenta_pagos = QLineEdit(self.tab_5)
        self.txtcuenta_pagos.setObjectName(u"txtcuenta_pagos")

        self.gridLayout_13.addWidget(self.txtcuenta_pagos, 5, 5, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_13)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.tabWidget_2.addTab(self.tab_5, "")

        self.gridLayout_24.addWidget(self.tabWidget_2, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab, "")
        self.tabWidgetPage2 = QWidget()
        self.tabWidgetPage2.setObjectName(u"tabWidgetPage2")
        self.gridLayout_5 = QGridLayout(self.tabWidgetPage2)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_2 = QLabel(self.tabWidgetPage2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_5.addWidget(self.label_2, 0, 0, 1, 1)

        self.mysql_frame = QFrame(self.tabWidgetPage2)
        self.mysql_frame.setObjectName(u"mysql_frame")
        self.mysql_frame.setEnabled(True)
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.mysql_frame.sizePolicy().hasHeightForWidth())
        self.mysql_frame.setSizePolicy(sizePolicy4)
        self.mysql_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.mysql_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.mysql_frame)
        self.gridLayout_4.setObjectName(u"gridLayout_4")

        self.gridLayout_5.addWidget(self.mysql_frame, 6, 0, 1, 5)

        self.groupBox_8 = QGroupBox(self.tabWidgetPage2)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.gridLayoutWidget_2 = QWidget(self.groupBox_8)
        self.gridLayoutWidget_2.setObjectName(u"gridLayoutWidget_2")
        self.gridLayoutWidget_2.setGeometry(QRect(100, 50, 367, 188))
        self.gridLayout_19 = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.gridLayout_19.setContentsMargins(0, 0, 0, 0)
        self.label_84 = QLabel(self.gridLayoutWidget_2)
        self.label_84.setObjectName(u"label_84")

        self.gridLayout_19.addWidget(self.label_84, 0, 3, 1, 1)

        self.pushButton_5 = QPushButton(self.gridLayoutWidget_2)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.gridLayout_19.addWidget(self.pushButton_5, 4, 0, 1, 5)

        self.txtUsuarioMariaDB_2 = QLineEdit(self.gridLayoutWidget_2)
        self.txtUsuarioMariaDB_2.setObjectName(u"txtUsuarioMariaDB_2")

        self.gridLayout_19.addWidget(self.txtUsuarioMariaDB_2, 2, 3, 1, 2)

        self.label_82 = QLabel(self.gridLayoutWidget_2)
        self.label_82.setObjectName(u"label_82")

        self.gridLayout_19.addWidget(self.label_82, 1, 0, 1, 2)

        self.label_86 = QLabel(self.gridLayoutWidget_2)
        self.label_86.setObjectName(u"label_86")

        self.gridLayout_19.addWidget(self.label_86, 0, 0, 1, 1)

        self.txtHostMariaDB_2 = QLineEdit(self.gridLayoutWidget_2)
        self.txtHostMariaDB_2.setObjectName(u"txtHostMariaDB_2")

        self.gridLayout_19.addWidget(self.txtHostMariaDB_2, 0, 1, 1, 1)

        self.lineEdit_17 = QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_17.setObjectName(u"lineEdit_17")

        self.gridLayout_19.addWidget(self.lineEdit_17, 0, 4, 1, 1)

        self.txtPasswordMariaDB_2 = QLineEdit(self.gridLayoutWidget_2)
        self.txtPasswordMariaDB_2.setObjectName(u"txtPasswordMariaDB_2")

        self.gridLayout_19.addWidget(self.txtPasswordMariaDB_2, 3, 3, 1, 2)

        self.label_87 = QLabel(self.gridLayoutWidget_2)
        self.label_87.setObjectName(u"label_87")

        self.gridLayout_19.addWidget(self.label_87, 2, 0, 1, 2)

        self.lineEdit_16 = QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_16.setObjectName(u"lineEdit_16")

        self.gridLayout_19.addWidget(self.lineEdit_16, 1, 3, 1, 2)

        self.label_83 = QLabel(self.gridLayoutWidget_2)
        self.label_83.setObjectName(u"label_83")

        self.gridLayout_19.addWidget(self.label_83, 3, 0, 1, 2)


        self.gridLayout_5.addWidget(self.groupBox_8, 2, 0, 4, 1)

        self.comboBox = QComboBox(self.tabWidgetPage2)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.gridLayout_5.addWidget(self.comboBox, 0, 1, 1, 2)

        self.sqlite_frame = QFrame(self.tabWidgetPage2)
        self.sqlite_frame.setObjectName(u"sqlite_frame")
        self.sqlite_frame.setEnabled(True)
        sizePolicy4.setHeightForWidth(self.sqlite_frame.sizePolicy().hasHeightForWidth())
        self.sqlite_frame.setSizePolicy(sizePolicy4)
        self.sqlite_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.sqlite_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.sqlite_frame)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_55 = QLabel(self.sqlite_frame)
        self.label_55.setObjectName(u"label_55")

        self.gridLayout_3.addWidget(self.label_55, 2, 0, 1, 1)

        self.btnSeleccionarBDSQLiteConta = QPushButton(self.sqlite_frame)
        self.btnSeleccionarBDSQLiteConta.setObjectName(u"btnSeleccionarBDSQLiteConta")

        self.gridLayout_3.addWidget(self.btnSeleccionarBDSQLiteConta, 2, 2, 1, 1)

        self.btn_migrar = QPushButton(self.sqlite_frame)
        self.btn_migrar.setObjectName(u"btn_migrar")

        self.gridLayout_3.addWidget(self.btn_migrar, 3, 0, 1, 1)

        self.btnSelecionarBDSQLite = QPushButton(self.sqlite_frame)
        self.btnSelecionarBDSQLite.setObjectName(u"btnSelecionarBDSQLite")

        self.gridLayout_3.addWidget(self.btnSelecionarBDSQLite, 1, 2, 1, 1)

        self.label_3 = QLabel(self.sqlite_frame)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_3.addWidget(self.label_3, 1, 0, 1, 1)

        self.label_4 = QLabel(self.sqlite_frame)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_3.addWidget(self.label_4, 0, 0, 1, 2)

        self.txtRutaBd = QLineEdit(self.sqlite_frame)
        self.txtRutaBd.setObjectName(u"txtRutaBd")
        self.txtRutaBd.setEnabled(False)
        self.txtRutaBd.setMaximumSize(QSize(16777215, 20))

        self.gridLayout_3.addWidget(self.txtRutaBd, 1, 1, 1, 1)

        self.txtruta_bd_conta = QLineEdit(self.sqlite_frame)
        self.txtruta_bd_conta.setObjectName(u"txtruta_bd_conta")
        self.txtruta_bd_conta.setEnabled(False)
        self.txtruta_bd_conta.setMaximumSize(QSize(16777215, 20))

        self.gridLayout_3.addWidget(self.txtruta_bd_conta, 2, 1, 1, 1)


        self.gridLayout_5.addWidget(self.sqlite_frame, 1, 0, 1, 3)

        self.groupBox_9 = QGroupBox(self.tabWidgetPage2)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.gridLayoutWidget = QWidget(self.groupBox_9)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(90, 50, 471, 188))
        self.gridLayout_18 = QGridLayout(self.gridLayoutWidget)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.gridLayout_18.setContentsMargins(0, 0, 0, 0)
        self.txtUsuarioMariaDB = QLineEdit(self.gridLayoutWidget)
        self.txtUsuarioMariaDB.setObjectName(u"txtUsuarioMariaDB")

        self.gridLayout_18.addWidget(self.txtUsuarioMariaDB, 2, 3, 1, 2)

        self.lineEdit_15 = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_15.setObjectName(u"lineEdit_15")

        self.gridLayout_18.addWidget(self.lineEdit_15, 1, 3, 1, 2)

        self.lineEdit = QLineEdit(self.gridLayoutWidget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.gridLayout_18.addWidget(self.lineEdit, 0, 4, 1, 1)

        self.label_79 = QLabel(self.gridLayoutWidget)
        self.label_79.setObjectName(u"label_79")

        self.gridLayout_18.addWidget(self.label_79, 1, 0, 1, 2)

        self.label_81 = QLabel(self.gridLayoutWidget)
        self.label_81.setObjectName(u"label_81")

        self.gridLayout_18.addWidget(self.label_81, 3, 0, 1, 2)

        self.txtHostMariaDB = QLineEdit(self.gridLayoutWidget)
        self.txtHostMariaDB.setObjectName(u"txtHostMariaDB")

        self.gridLayout_18.addWidget(self.txtHostMariaDB, 0, 1, 1, 1)

        self.txtPasswordMariaDB = QLineEdit(self.gridLayoutWidget)
        self.txtPasswordMariaDB.setObjectName(u"txtPasswordMariaDB")

        self.gridLayout_18.addWidget(self.txtPasswordMariaDB, 3, 3, 1, 2)

        self.label_78 = QLabel(self.gridLayoutWidget)
        self.label_78.setObjectName(u"label_78")

        self.gridLayout_18.addWidget(self.label_78, 0, 3, 1, 1)

        self.label_56 = QLabel(self.gridLayoutWidget)
        self.label_56.setObjectName(u"label_56")

        self.gridLayout_18.addWidget(self.label_56, 0, 0, 1, 1)

        self.label_80 = QLabel(self.gridLayoutWidget)
        self.label_80.setObjectName(u"label_80")

        self.gridLayout_18.addWidget(self.label_80, 2, 0, 1, 2)

        self.pushButton_4 = QPushButton(self.gridLayoutWidget)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.gridLayout_18.addWidget(self.pushButton_4, 4, 0, 1, 5)


        self.gridLayout_5.addWidget(self.groupBox_9, 2, 1, 4, 4)

        self.tabWidget.addTab(self.tabWidgetPage2, "")

        self.gridLayout_14.addWidget(self.tabWidget, 2, 0, 1, 1)

        self.btn_salir = QPushButton(self.create_page_empresa)
        self.btn_salir.setObjectName(u"btn_salir")
        self.btn_salir.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout_14.addWidget(self.btn_salir, 5, 0, 1, 1)

        self.stackedWidget.addWidget(self.create_page_empresa)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.tableView = QTableView(self.page)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setGeometry(QRect(5, 11, 1261, 681))
        self.stackedWidget.addWidget(self.page)

        self.gridLayout_2.addWidget(self.stackedWidget, 1, 0, 1, 1)

        self.label = QLabel(FrmEmpresas)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"background-color: #304163;\n"
"font: 14pt \"Sans Serif\";\n"
"color: rgb(255, 255, 255);")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        QWidget.setTabOrder(self.txtcodigo, self.txtEmpresa)
        QWidget.setTabOrder(self.txtEmpresa, self.cboFormajuridica)
        QWidget.setTabOrder(self.cboFormajuridica, self.cboGrupoEmpresa)
        QWidget.setTabOrder(self.cboGrupoEmpresa, self.txtNombreComercial)
        QWidget.setTabOrder(self.txtNombreComercial, self.txtcp)
        QWidget.setTabOrder(self.txtcp, self.txtpoblacion)
        QWidget.setTabOrder(self.txtpoblacion, self.txtdireccion1)
        QWidget.setTabOrder(self.txtdireccion1, self.txtprovincia)
        QWidget.setTabOrder(self.txtprovincia, self.cboPais_create)
        QWidget.setTabOrder(self.cboPais_create, self.txtcif)
        QWidget.setTabOrder(self.txtcif, self.lineEdit_2)
        QWidget.setTabOrder(self.lineEdit_2, self.lineEdit_3)
        QWidget.setTabOrder(self.lineEdit_3, self.chkTVA)
        QWidget.setTabOrder(self.chkTVA, self.lineEdit_4)
        QWidget.setTabOrder(self.lineEdit_4, self.lineEdit_5)
        QWidget.setTabOrder(self.lineEdit_5, self.lineEdit_6)
        QWidget.setTabOrder(self.lineEdit_6, self.txtcInscripcion)
        QWidget.setTabOrder(self.txtcInscripcion, self.txttelefono1)
        QWidget.setTabOrder(self.txttelefono1, self.txttelefono2)
        QWidget.setTabOrder(self.txttelefono2, self.txtMovil)
        QWidget.setTabOrder(self.txtMovil, self.txtcMail)
        QWidget.setTabOrder(self.txtcMail, self.txtweb)
        QWidget.setTabOrder(self.txtweb, self.chkEnlace_web)
        QWidget.setTabOrder(self.chkEnlace_web, self.chkInternacional)
        QWidget.setTabOrder(self.chkInternacional, self.txtDiaCierre)
        QWidget.setTabOrder(self.txtDiaCierre, self.tstMesCierre)
        QWidget.setTabOrder(self.tstMesCierre, self.chkAutocodificiar)
        QWidget.setTabOrder(self.chkAutocodificiar, self.txttamano_codigoart)
        QWidget.setTabOrder(self.txttamano_codigoart, self.chkIRPF)
        QWidget.setTabOrder(self.chkIRPF, self.spinPorc_irpf)
        QWidget.setTabOrder(self.spinPorc_irpf, self.cboTarifa)
        QWidget.setTabOrder(self.cboTarifa, self.spinMargen)
        QWidget.setTabOrder(self.spinMargen, self.spinMargen_minimo)
        QWidget.setTabOrder(self.spinMargen_minimo, self.chk_upate_divisas)
        QWidget.setTabOrder(self.chk_upate_divisas, self.cboDivisas)
        QWidget.setTabOrder(self.cboDivisas, self.spinDigitos)
        QWidget.setTabOrder(self.spinDigitos, self.cboSerie)
        QWidget.setTabOrder(self.cboSerie, self.spinDecimales_create)
        QWidget.setTabOrder(self.spinDecimales_create, self.spinDecimales_precios_create)
        QWidget.setTabOrder(self.spinDecimales_precios_create, self.btnAddLogo)
        QWidget.setTabOrder(self.btnAddLogo, self.btnDeleteLogo)
        QWidget.setTabOrder(self.btnDeleteLogo, self.txtcCometarioAlbaran)
        QWidget.setTabOrder(self.txtcCometarioAlbaran, self.txtccomentario_factura)
        QWidget.setTabOrder(self.txtccomentario_factura, self.txt_horario_primer_dia)
        QWidget.setTabOrder(self.txt_horario_primer_dia, self.txt_horario_dia_normal)
        QWidget.setTabOrder(self.txt_horario_dia_normal, self.txt_horario_ultimo_dia)
        QWidget.setTabOrder(self.txt_horario_ultimo_dia, self.lineEdit_7)
        QWidget.setTabOrder(self.lineEdit_7, self.lineEdit_8)
        QWidget.setTabOrder(self.lineEdit_8, self.lineEdit_9)
        QWidget.setTabOrder(self.lineEdit_9, self.lineEdit_10)
        QWidget.setTabOrder(self.lineEdit_10, self.lineEdit_11)
        QWidget.setTabOrder(self.lineEdit_11, self.lineEdit_12)
        QWidget.setTabOrder(self.lineEdit_12, self.lineEdit_13)
        QWidget.setTabOrder(self.lineEdit_13, self.lineEdit_14)
        QWidget.setTabOrder(self.lineEdit_14, self.txtdigitos_cuentas)
        QWidget.setTabOrder(self.txtdigitos_cuentas, self.txtcuentaCliente)
        QWidget.setTabOrder(self.txtcuentaCliente, self.txtcuenta_proveedores)
        QWidget.setTabOrder(self.txtcuenta_proveedores, self.txtcuenta_acreedores)
        QWidget.setTabOrder(self.txtcuenta_acreedores, self.txtCuenta_venta_mercaderias)
        QWidget.setTabOrder(self.txtCuenta_venta_mercaderias, self.txtCuenta_venta_servicios)
        QWidget.setTabOrder(self.txtCuenta_venta_servicios, self.ivasoportado1)
        QWidget.setTabOrder(self.ivasoportado1, self.ivasoportado2)
        QWidget.setTabOrder(self.ivasoportado2, self.ivasoportado3)
        QWidget.setTabOrder(self.ivasoportado3, self.ivasoportado4)
        QWidget.setTabOrder(self.ivasoportado4, self.ivasoportadore1)
        QWidget.setTabOrder(self.ivasoportadore1, self.ivasoportadore2)
        QWidget.setTabOrder(self.ivasoportadore2, self.ivasoportadore3)
        QWidget.setTabOrder(self.ivasoportadore3, self.ivasoportadore4)
        QWidget.setTabOrder(self.ivasoportadore4, self.txtcuenta_cobros)
        QWidget.setTabOrder(self.txtcuenta_cobros, self.ivarepercutido1)
        QWidget.setTabOrder(self.ivarepercutido1, self.ivarepercutido2)
        QWidget.setTabOrder(self.ivarepercutido2, self.ivarepercutido3)
        QWidget.setTabOrder(self.ivarepercutido3, self.ivarepercutido4)
        QWidget.setTabOrder(self.ivarepercutido4, self.ivarepercutidore1)
        QWidget.setTabOrder(self.ivarepercutidore1, self.ivarepercutidore2)
        QWidget.setTabOrder(self.ivarepercutidore2, self.ivarepercutidore3)
        QWidget.setTabOrder(self.ivarepercutidore3, self.ivarepercutidore4)
        QWidget.setTabOrder(self.ivarepercutidore4, self.txtcuenta_pagos)
        QWidget.setTabOrder(self.txtcuenta_pagos, self.comboBox)
        QWidget.setTabOrder(self.comboBox, self.txtRutaBd)
        QWidget.setTabOrder(self.txtRutaBd, self.btnSelecionarBDSQLite)
        QWidget.setTabOrder(self.btnSelecionarBDSQLite, self.txtruta_bd_conta)
        QWidget.setTabOrder(self.txtruta_bd_conta, self.btnSeleccionarBDSQLiteConta)
        QWidget.setTabOrder(self.btnSeleccionarBDSQLiteConta, self.btn_migrar)
        QWidget.setTabOrder(self.btn_migrar, self.txtHostMariaDB_2)
        QWidget.setTabOrder(self.txtHostMariaDB_2, self.lineEdit_17)
        QWidget.setTabOrder(self.lineEdit_17, self.lineEdit_16)
        QWidget.setTabOrder(self.lineEdit_16, self.txtUsuarioMariaDB_2)
        QWidget.setTabOrder(self.txtUsuarioMariaDB_2, self.txtPasswordMariaDB_2)
        QWidget.setTabOrder(self.txtPasswordMariaDB_2, self.pushButton_5)
        QWidget.setTabOrder(self.pushButton_5, self.txtHostMariaDB)
        QWidget.setTabOrder(self.txtHostMariaDB, self.lineEdit)
        QWidget.setTabOrder(self.lineEdit, self.lineEdit_15)
        QWidget.setTabOrder(self.lineEdit_15, self.txtUsuarioMariaDB)
        QWidget.setTabOrder(self.txtUsuarioMariaDB, self.txtPasswordMariaDB)
        QWidget.setTabOrder(self.txtPasswordMariaDB, self.pushButton_4)
        QWidget.setTabOrder(self.pushButton_4, self.btn_guardar_nuevo)
        QWidget.setTabOrder(self.btn_guardar_nuevo, self.pushButton)
        QWidget.setTabOrder(self.pushButton, self.btn_salir)
        QWidget.setTabOrder(self.btn_salir, self.tableView)
        QWidget.setTabOrder(self.tableView, self.tabWidget)
        QWidget.setTabOrder(self.tabWidget, self.tabWidget_2)
        QWidget.setTabOrder(self.tabWidget_2, self.chkContabilidad)

        self.retranslateUi(FrmEmpresas)
        self.btn_salir.clicked.connect(FrmEmpresas.accept)

        self.stackedWidget.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(FrmEmpresas)
    # setupUi

    def retranslateUi(self, FrmEmpresas):
        FrmEmpresas.setWindowTitle(QCoreApplication.translate("FrmEmpresas", u"Gesti\u00f3n de empresas", None))
        self.btn_guardar_nuevo.setText(QCoreApplication.translate("FrmEmpresas", u"Guardar", None))
        self.pushButton.setText(QCoreApplication.translate("FrmEmpresas", u"Descartar", None))
        self.label_22.setText(QCoreApplication.translate("FrmEmpresas", u"Cif:", None))
        self.label_17.setText(QCoreApplication.translate("FrmEmpresas", u"Tel\u00e9fono 1:", None))
        self.label_53.setText(QCoreApplication.translate("FrmEmpresas", u"N\u00ba RCS:", None))
        self.label_74.setText(QCoreApplication.translate("FrmEmpresas", u"Codigo:", None))
        self.txttelefono1.setText("")
        self.label_15.setText(QCoreApplication.translate("FrmEmpresas", u"Provincia:", None))
        self.txttelefono2.setText("")
        self.label_19.setText(QCoreApplication.translate("FrmEmpresas", u"Movil:", None))
        self.label_23.setText(QCoreApplication.translate("FrmEmpresas", u"Inscripci\u00f3n:", None))
        self.label_13.setText(QCoreApplication.translate("FrmEmpresas", u"Direcci\u00f3n:", None))
        self.label_54.setText(QCoreApplication.translate("FrmEmpresas", u"Ciudad RCS:", None))
        self.label_57.setText(QCoreApplication.translate("FrmEmpresas", u"N\u00ba RM:", None))
        self.label_20.setText(QCoreApplication.translate("FrmEmpresas", u"Mail:", None))
        self.label_16.setText(QCoreApplication.translate("FrmEmpresas", u"Pais:", None))
        self.label_18.setText(QCoreApplication.translate("FrmEmpresas", u"Telefono 2:", None))
        self.label_21.setText(QCoreApplication.translate("FrmEmpresas", u"Web:", None))
        self.label_75.setText(QCoreApplication.translate("FrmEmpresas", u"Nombre:", None))
        self.label_24.setText(QCoreApplication.translate("FrmEmpresas", u"Forma juridica:", None))
        self.cboFormajuridica.setItemText(0, QCoreApplication.translate("FrmEmpresas", u"EI (Entreprise Individuelle)", None))
        self.cboFormajuridica.setItemText(1, QCoreApplication.translate("FrmEmpresas", u"EIRL", None))
        self.cboFormajuridica.setItemText(2, QCoreApplication.translate("FrmEmpresas", u"Micro-entrepreneur", None))
        self.cboFormajuridica.setItemText(3, QCoreApplication.translate("FrmEmpresas", u"SARL", None))
        self.cboFormajuridica.setItemText(4, QCoreApplication.translate("FrmEmpresas", u"EURL", None))
        self.cboFormajuridica.setItemText(5, QCoreApplication.translate("FrmEmpresas", u"SAS", None))
        self.cboFormajuridica.setItemText(6, QCoreApplication.translate("FrmEmpresas", u"SASU", None))
        self.cboFormajuridica.setItemText(7, QCoreApplication.translate("FrmEmpresas", u"SA", None))
        self.cboFormajuridica.setItemText(8, QCoreApplication.translate("FrmEmpresas", u"SCOP / SCIC", None))
        self.cboFormajuridica.setItemText(9, QCoreApplication.translate("FrmEmpresas", u"SEM", None))
        self.cboFormajuridica.setItemText(10, QCoreApplication.translate("FrmEmpresas", u"RM", None))

        self.label_6.setText(QCoreApplication.translate("FrmEmpresas", u"Grupo", None))
        self.label_32.setText(QCoreApplication.translate("FrmEmpresas", u"SIRET:", None))
        self.label_34.setText(QCoreApplication.translate("FrmEmpresas", u"APE/NAF:", None))
        self.chkTVA.setText(QCoreApplication.translate("FrmEmpresas", u"TVA non applicable", None))
        self.label_14.setText(QCoreApplication.translate("FrmEmpresas", u"C.P.:", None))
        self.label_43.setText(QCoreApplication.translate("FrmEmpresas", u"Nombre comercial:", None))
        self.label_50.setText(QCoreApplication.translate("FrmEmpresas", u"Poblaci\u00f3n:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPage1), QCoreApplication.translate("FrmEmpresas", u"Datos Fiscales y de Gesti\u00f3n", None))
        self.groupBox_14.setTitle(QCoreApplication.translate("FrmEmpresas", u"Divisas", None))
        self.chk_upate_divisas.setText(QCoreApplication.translate("FrmEmpresas", u"Actualizar divisas al entrar", None))
        self.label_42.setText(QCoreApplication.translate("FrmEmpresas", u"Divisa: ", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("FrmEmpresas", u"IRPF", None))
        self.chkIRPF.setText(QCoreApplication.translate("FrmEmpresas", u"Autonomo / IRPF", None))
        self.label_71.setText(QCoreApplication.translate("FrmEmpresas", u"%IRPF:", None))
        self.groupBox_12.setTitle(QCoreApplication.translate("FrmEmpresas", u"Decimales", None))
        self.label_222.setText(QCoreApplication.translate("FrmEmpresas", u"Decimales en totales", None))
        self.label_85.setText(QCoreApplication.translate("FrmEmpresas", u"Decimales precios:", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("FrmEmpresas", u"Facturas", None))
        self.label_25.setText(QCoreApplication.translate("FrmEmpresas", u"Digitos Factura:", None))
        self.label_26.setText(QCoreApplication.translate("FrmEmpresas", u"Serie Factura:", None))
        self.label_68.setText(QCoreApplication.translate("FrmEmpresas", u"Cierre ejercicio fiscal:", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("FrmEmpresas", u"Varios", None))
        self.chkEnlace_web.setText(QCoreApplication.translate("FrmEmpresas", u"Enlace Web.", None))
        self.chkInternacional.setText(QCoreApplication.translate("FrmEmpresas", u"Gesti\u00f3n Internacional", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("FrmEmpresas", u"Articulos", None))
        self.chkAutocodificiar.setText(QCoreApplication.translate("FrmEmpresas", u"Auto codificar los nuevos art\u00edculos", None))
        self.label_41.setText(QCoreApplication.translate("FrmEmpresas", u"Tama\u00f1o del c\u00f3digo en caracteres:", None))
        self.groupBox.setTitle(QCoreApplication.translate("FrmEmpresas", u"Tarifas", None))
        self.label_33.setText(QCoreApplication.translate("FrmEmpresas", u"Margen M\u00ednimo:", None))
        self.label_31.setText(QCoreApplication.translate("FrmEmpresas", u"Margen:", None))
        self.label_58.setText(QCoreApplication.translate("FrmEmpresas", u"Tarifa predeterminada:", None))
        self.btnDeleteLogo.setText(QCoreApplication.translate("FrmEmpresas", u"Borrar", None))
        self.btnAddLogo.setText(QCoreApplication.translate("FrmEmpresas", u"Cambiar", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("FrmEmpresas", u"Logotipo", None))
        self.imgLogo.setText("")
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_12), QCoreApplication.translate("FrmEmpresas", u"Otros", None))
        self.label_36.setText(QCoreApplication.translate("FrmEmpresas", u"Comentarios en Albaranes", None))
        self.label_35.setText(QCoreApplication.translate("FrmEmpresas", u"Comentarios en Facturas:", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_6), QCoreApplication.translate("FrmEmpresas", u"Comentarios", None))
        self.label_47.setText(QCoreApplication.translate("FrmEmpresas", u"Horario Martes:", None))
        self.label_46.setText(QCoreApplication.translate("FrmEmpresas", u"Horario Lunes:", None))
        self.label_45.setText(QCoreApplication.translate("FrmEmpresas", u"Horario Viernes:", None))
        self.label_70.setText(QCoreApplication.translate("FrmEmpresas", u"Horario Domingo:", None))
        self.label_44.setText(QCoreApplication.translate("FrmEmpresas", u"Horario Jueves:", None))
        self.label_69.setText(QCoreApplication.translate("FrmEmpresas", u"Horario Sabado:", None))
        self.label_48.setText(QCoreApplication.translate("FrmEmpresas", u"Horario Miercoles:", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("FrmEmpresas", u"Acceso a Google Calendar", None))
        self.label_72.setText(QCoreApplication.translate("FrmEmpresas", u"Google Calendar ID:", None))
        self.label_73.setText(QCoreApplication.translate("FrmEmpresas", u"oauth Acces Token:", None))
        self.label_76.setText(QCoreApplication.translate("FrmEmpresas", u"oauth Refresh Token:", None))
        self.label_77.setText(QCoreApplication.translate("FrmEmpresas", u" Token Expirity:", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_8), QCoreApplication.translate("FrmEmpresas", u"Agenda", None))
        self.chkContabilidad.setText(QCoreApplication.translate("FrmEmpresas", u"Activar contabilidad", None))
        self.txtCuenta_venta_servicios.setText(QCoreApplication.translate("FrmEmpresas", u"610", None))
        self.txtCuenta_venta_servicios.setPlaceholderText(QCoreApplication.translate("FrmEmpresas", u"(F1 - lista)", None))
        self.txtCuenta_venta_mercaderias.setText(QCoreApplication.translate("FrmEmpresas", u"600", None))
        self.txtCuenta_venta_mercaderias.setPlaceholderText(QCoreApplication.translate("FrmEmpresas", u"(F1 - lista)", None))
        self.txtcuenta_acreedores.setText(QCoreApplication.translate("FrmEmpresas", u"410", None))
        self.txtcuenta_acreedores.setPlaceholderText(QCoreApplication.translate("FrmEmpresas", u"(F1 - lista)", None))
        self.label_29.setText(QCoreApplication.translate("FrmEmpresas", u"Acreedores:", None))
        self.label_12.setText(QCoreApplication.translate("FrmEmpresas", u"Cuenta de venta de mercader\u00edas:", None))
        self.label_37.setText(QCoreApplication.translate("FrmEmpresas", u"Cuenta de venta (prestaci\u00f3n de servicios):", None))
        self.label_28.setText(QCoreApplication.translate("FrmEmpresas", u"Proveedores:", None))
        self.txtcuenta_proveedores.setText(QCoreApplication.translate("FrmEmpresas", u"400", None))
        self.txtcuenta_proveedores.setPlaceholderText(QCoreApplication.translate("FrmEmpresas", u"(F1 - lista)", None))
        self.txtcuentaCliente.setText(QCoreApplication.translate("FrmEmpresas", u"430", None))
        self.txtcuentaCliente.setPlaceholderText(QCoreApplication.translate("FrmEmpresas", u"(F1 - lista)", None))
        self.label_30.setText(QCoreApplication.translate("FrmEmpresas", u"Digitos cuentas contables:", None))
        self.label_27.setText(QCoreApplication.translate("FrmEmpresas", u"Cientes:", None))
        self.ivarepercutidore1.setPlaceholderText(QCoreApplication.translate("FrmEmpresas", u"(F1 - lista)", None))
        self.ivarepercutido3.setPlaceholderText(QCoreApplication.translate("FrmEmpresas", u"(F1 - lista)", None))
        self.label_65.setText(QCoreApplication.translate("FrmEmpresas", u"E", None))
        self.ivasoportado4.setPlaceholderText(QCoreApplication.translate("FrmEmpresas", u"(F1 - lista)", None))
        self.label_59.setText(QCoreApplication.translate("FrmEmpresas", u"R", None))
        self.ivasoportado2.setPlaceholderText(QCoreApplication.translate("FrmEmpresas", u"(F1 - lista)", None))
        self.label_63.setText(QCoreApplication.translate("FrmEmpresas", u"R", None))
        self.label_38.setText(QCoreApplication.translate("FrmEmpresas", u"Cuenta IVA soportado", None))
        self.ivasoportadore4.setPlaceholderText(QCoreApplication.translate("FrmEmpresas", u"(F1 - lista)", None))
        self.ivasoportadore3.setPlaceholderText(QCoreApplication.translate("FrmEmpresas", u"(F1 - lista)", None))
        self.label_39.setText(QCoreApplication.translate("FrmEmpresas", u"Cuenta IVA repercutido", None))
        self.label_40.setText(QCoreApplication.translate("FrmEmpresas", u"N", None))
        self.label_62.setText(QCoreApplication.translate("FrmEmpresas", u"N", None))
        self.ivasoportado1.setPlaceholderText(QCoreApplication.translate("FrmEmpresas", u"(F1 - lista)", None))
        self.ivarepercutido1.setPlaceholderText(QCoreApplication.translate("FrmEmpresas", u"(F1 - lista)", None))
        self.ivarepercutido4.setPlaceholderText(QCoreApplication.translate("FrmEmpresas", u"(F1 - lista)", None))
        self.ivarepercutido2.setPlaceholderText(QCoreApplication.translate("FrmEmpresas", u"(F1 - lista)", None))
        self.label_60.setText(QCoreApplication.translate("FrmEmpresas", u"SR", None))
        self.ivasoportado3.setPlaceholderText(QCoreApplication.translate("FrmEmpresas", u"(F1 - lista)", None))
        self.label_64.setText(QCoreApplication.translate("FrmEmpresas", u"SR", None))
        self.label_61.setText(QCoreApplication.translate("FrmEmpresas", u"E", None))
        self.ivasoportadore1.setPlaceholderText(QCoreApplication.translate("FrmEmpresas", u"(F1 - lista)", None))
        self.ivasoportadore2.setPlaceholderText(QCoreApplication.translate("FrmEmpresas", u"(F1 - lista)", None))
        self.label_66.setText(QCoreApplication.translate("FrmEmpresas", u"IVA soportado RE", None))
        self.label_67.setText(QCoreApplication.translate("FrmEmpresas", u"IVA repercutido RE", None))
        self.ivarepercutidore3.setPlaceholderText(QCoreApplication.translate("FrmEmpresas", u"(F1 - lista)", None))
        self.ivarepercutidore2.setPlaceholderText(QCoreApplication.translate("FrmEmpresas", u"(F1 - lista)", None))
        self.ivarepercutidore4.setPlaceholderText(QCoreApplication.translate("FrmEmpresas", u"(F1 - lista)", None))
        self.label_9.setText(QCoreApplication.translate("FrmEmpresas", u"Cuenta cobros:", None))
        self.txtcuenta_cobros.setPlaceholderText(QCoreApplication.translate("FrmEmpresas", u"(F1 - lista)", None))
        self.label_10.setText(QCoreApplication.translate("FrmEmpresas", u"Cuenta Pagos:", None))
        self.txtcuenta_pagos.setPlaceholderText(QCoreApplication.translate("FrmEmpresas", u"(F1 - lista)", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_5), QCoreApplication.translate("FrmEmpresas", u"Contabilidad", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("FrmEmpresas", u"Otros datos", None))
        self.label_2.setText(QCoreApplication.translate("FrmEmpresas", u"Motor Activo de Base de Datos", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("FrmEmpresas", u"Datos Acceso MariaDB / MySQL ( Recomendado para empresas entre 2 y 10 ordenadores)", None))
        self.label_84.setText(QCoreApplication.translate("FrmEmpresas", u"Puerto:", None))
        self.pushButton_5.setText(QCoreApplication.translate("FrmEmpresas", u"Test Database conexion", None))
        self.label_82.setText(QCoreApplication.translate("FrmEmpresas", u"Nombre Base de Datos:", None))
        self.label_86.setText(QCoreApplication.translate("FrmEmpresas", u"Host:", None))
        self.label_87.setText(QCoreApplication.translate("FrmEmpresas", u"Usuario:", None))
        self.label_83.setText(QCoreApplication.translate("FrmEmpresas", u"Password:", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("FrmEmpresas", u"SQLite", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("FrmEmpresas", u"MariaDB", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("FrmEmpresas", u"PostgreSQL", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("FrmEmpresas", u"MySQL", None))

        self.label_55.setText(QCoreApplication.translate("FrmEmpresas", u"Ruta BD: Contabilidad:", None))
        self.btnSeleccionarBDSQLiteConta.setText(QCoreApplication.translate("FrmEmpresas", u"...", None))
        self.btn_migrar.setText(QCoreApplication.translate("FrmEmpresas", u"Migrar a BD Multipuesto", None))
        self.btnSelecionarBDSQLite.setText(QCoreApplication.translate("FrmEmpresas", u"...", None))
        self.label_3.setText(QCoreApplication.translate("FrmEmpresas", u"Ruta SQLite Empresa", None))
        self.label_4.setText(QCoreApplication.translate("FrmEmpresas", u"<html><head/><body><p><span style=\" font-weight:700; color:#ffffff;\">Acceso a SQLite (Para empresas con un solo ordenador)</span></p><p><span style=\" font-weight:700; color:#ffffff;\"><br/></span></p></body></html>", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("FrmEmpresas", u"Datos Acceso Postgre SQL(Recomendado para empresas con m\u00e1s de 10 ordenadores)", None))
        self.label_79.setText(QCoreApplication.translate("FrmEmpresas", u"Nombre Base de Datos:", None))
        self.label_81.setText(QCoreApplication.translate("FrmEmpresas", u"Password:", None))
        self.label_78.setText(QCoreApplication.translate("FrmEmpresas", u"Puerto:", None))
        self.label_56.setText(QCoreApplication.translate("FrmEmpresas", u"Host:", None))
        self.label_80.setText(QCoreApplication.translate("FrmEmpresas", u"Usuario:", None))
        self.pushButton_4.setText(QCoreApplication.translate("FrmEmpresas", u"Test Database conexion", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPage2), QCoreApplication.translate("FrmEmpresas", u"Datos conexi\u00f3n Base de datos", None))
        self.btn_salir.setText(QCoreApplication.translate("FrmEmpresas", u"Salir", None))
        self.label.setText(QCoreApplication.translate("FrmEmpresas", u"Gesti\u00f3n de Empresas", None))
    # retranslateUi

