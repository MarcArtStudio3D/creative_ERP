# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frmempresas.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject, QRect, QSize, Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QSpinBox,
    QStackedWidget,
    QTableView,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class Ui_FrmEmpresas(object):
    def setupUi(self, FrmEmpresas):
        if not FrmEmpresas.objectName():
            FrmEmpresas.setObjectName("FrmEmpresas")
        FrmEmpresas.resize(1261, 751)
        icon = QIcon()
        icon.addFile(
            ":/PNG/resources/icons/png/LogoIcono.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        FrmEmpresas.setWindowIcon(icon)
        self.gridLayout_2 = QGridLayout(FrmEmpresas)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.stackedWidget = QStackedWidget(FrmEmpresas)
        self.stackedWidget.setObjectName("stackedWidget")
        self.create_page_empresa = QWidget()
        self.create_page_empresa.setObjectName("create_page_empresa")
        self.gridLayout_14 = QGridLayout(self.create_page_empresa)
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.btn_guardar_nuevo = QPushButton(self.create_page_empresa)
        self.btn_guardar_nuevo.setObjectName("btn_guardar_nuevo")
        icon1 = QIcon()
        icon1.addFile(
            ":/Icons/PNG/Save.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.btn_guardar_nuevo.setIcon(icon1)

        self.gridLayout_14.addWidget(self.btn_guardar_nuevo, 4, 0, 1, 1)

        self.pushButton = QPushButton(self.create_page_empresa)
        self.pushButton.setObjectName("pushButton")

        self.gridLayout_14.addWidget(self.pushButton, 5, 0, 1, 1)

        self.btn_salir = QPushButton(self.create_page_empresa)
        self.btn_salir.setObjectName("btn_salir")
        self.btn_salir.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout_14.addWidget(self.btn_salir, 6, 0, 1, 1)

        self.tabWidget = QTabWidget(self.create_page_empresa)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setMaximumSize(QSize(1216, 16777215))
        self.tabWidget.setStyleSheet("")
        self.tabWidgetPage1 = QWidget()
        self.tabWidgetPage1.setObjectName("tabWidgetPage1")
        self.gridLayout_12 = QGridLayout(self.tabWidgetPage1)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label_50 = QLabel(self.tabWidgetPage1)
        self.label_50.setObjectName("label_50")

        self.gridLayout_6.addWidget(self.label_50, 4, 3, 1, 1)

        self.label_34 = QLabel(self.tabWidgetPage1)
        self.label_34.setObjectName("label_34")

        self.gridLayout_6.addWidget(self.label_34, 8, 7, 1, 1)

        self.cboGrupoEmpresa = QComboBox(self.tabWidgetPage1)
        self.cboGrupoEmpresa.setObjectName("cboGrupoEmpresa")
        self.cboGrupoEmpresa.setMinimumSize(QSize(152, 0))
        self.cboGrupoEmpresa.setEditable(False)

        self.gridLayout_6.addWidget(self.cboGrupoEmpresa, 0, 8, 1, 3)

        self.label_20 = QLabel(self.tabWidgetPage1)
        self.label_20.setObjectName("label_20")
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy)
        self.label_20.setMinimumSize(QSize(80, 0))

        self.gridLayout_6.addWidget(self.label_20, 12, 1, 1, 1)

        self.txtdireccion1 = QLineEdit(self.tabWidgetPage1)
        self.txtdireccion1.setObjectName("txtdireccion1")
        self.txtdireccion1.setClearButtonEnabled(True)

        self.gridLayout_6.addWidget(self.txtdireccion1, 3, 2, 1, 9)

        self.txtcif = QLineEdit(self.tabWidgetPage1)
        self.txtcif.setObjectName("txtcif")
        self.txtcif.setMaximumSize(QSize(16777215, 16777215))
        self.txtcif.setClearButtonEnabled(True)

        self.gridLayout_6.addWidget(self.txtcif, 8, 2, 1, 1)

        self.label_21 = QLabel(self.tabWidgetPage1)
        self.label_21.setObjectName("label_21")
        sizePolicy.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy)
        self.label_21.setMinimumSize(QSize(80, 0))

        self.gridLayout_6.addWidget(self.label_21, 12, 7, 1, 1)

        self.label_13 = QLabel(self.tabWidgetPage1)
        self.label_13.setObjectName("label_13")
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)

        self.gridLayout_6.addWidget(self.label_13, 3, 1, 1, 1)

        self.label_6 = QLabel(self.tabWidgetPage1)
        self.label_6.setObjectName("label_6")

        self.gridLayout_6.addWidget(self.label_6, 0, 7, 1, 1)

        self.label_22 = QLabel(self.tabWidgetPage1)
        self.label_22.setObjectName("label_22")
        sizePolicy.setHeightForWidth(self.label_22.sizePolicy().hasHeightForWidth())
        self.label_22.setSizePolicy(sizePolicy)
        self.label_22.setMinimumSize(QSize(66, 0))

        self.gridLayout_6.addWidget(self.label_22, 8, 1, 1, 1)

        self.txtAPE = QLineEdit(self.tabWidgetPage1)
        self.txtAPE.setObjectName("txtAPE")

        self.gridLayout_6.addWidget(self.txtAPE, 8, 8, 1, 3)

        self.txtSiret = QLineEdit(self.tabWidgetPage1)
        self.txtSiret.setObjectName("txtSiret")

        self.gridLayout_6.addWidget(self.txtSiret, 8, 6, 1, 1)

        self.chkTVA = QCheckBox(self.tabWidgetPage1)
        self.chkTVA.setObjectName("chkTVA")

        self.gridLayout_6.addWidget(self.chkTVA, 2, 8, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.gridLayout_6.addItem(self.verticalSpacer_3, 13, 2, 1, 1)

        self.label_43 = QLabel(self.tabWidgetPage1)
        self.label_43.setObjectName("label_43")

        self.gridLayout_6.addWidget(self.label_43, 0, 3, 1, 1)

        self.txtNombreComercial = QLineEdit(self.tabWidgetPage1)
        self.txtNombreComercial.setObjectName("txtNombreComercial")

        self.gridLayout_6.addWidget(self.txtNombreComercial, 0, 4, 1, 3)

        self.label_53 = QLabel(self.tabWidgetPage1)
        self.label_53.setObjectName("label_53")

        self.gridLayout_6.addWidget(self.label_53, 9, 1, 1, 1)

        self.txtprovincia = QLineEdit(self.tabWidgetPage1)
        self.txtprovincia.setObjectName("txtprovincia")
        self.txtprovincia.setClearButtonEnabled(True)

        self.gridLayout_6.addWidget(self.txtprovincia, 4, 10, 1, 1)

        self.txtcInscripcion = QLineEdit(self.tabWidgetPage1)
        self.txtcInscripcion.setObjectName("txtcInscripcion")
        self.txtcInscripcion.setClearButtonEnabled(True)

        self.gridLayout_6.addWidget(self.txtcInscripcion, 10, 2, 1, 5)

        self.label_19 = QLabel(self.tabWidgetPage1)
        self.label_19.setObjectName("label_19")
        sizePolicy.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy)
        self.label_19.setMinimumSize(QSize(80, 0))

        self.gridLayout_6.addWidget(self.label_19, 11, 7, 1, 1)

        self.label_16 = QLabel(self.tabWidgetPage1)
        self.label_16.setObjectName("label_16")
        sizePolicy.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy)

        self.gridLayout_6.addWidget(self.label_16, 2, 1, 1, 1)

        self.label_32 = QLabel(self.tabWidgetPage1)
        self.label_32.setObjectName("label_32")

        self.gridLayout_6.addWidget(self.label_32, 8, 5, 1, 1)

        self.txtcodigo = QLineEdit(self.tabWidgetPage1)
        self.txtcodigo.setObjectName("txtcodigo")
        self.txtcodigo.setMaximumSize(QSize(100, 16777215))
        self.txtcodigo.setReadOnly(False)
        self.txtcodigo.setClearButtonEnabled(True)

        self.gridLayout_6.addWidget(self.txtcodigo, 0, 2, 1, 1)

        self.label_23 = QLabel(self.tabWidgetPage1)
        self.label_23.setObjectName("label_23")
        sizePolicy.setHeightForWidth(self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy)

        self.gridLayout_6.addWidget(self.label_23, 10, 1, 1, 1)

        self.txtNRS = QLineEdit(self.tabWidgetPage1)
        self.txtNRS.setObjectName("txtNRS")

        self.gridLayout_6.addWidget(self.txtNRS, 9, 2, 1, 1)

        self.txtRM = QLineEdit(self.tabWidgetPage1)
        self.txtRM.setObjectName("txtRM")

        self.gridLayout_6.addWidget(self.txtRM, 9, 8, 1, 3)

        self.txtweb = QLineEdit(self.tabWidgetPage1)
        self.txtweb.setObjectName("txtweb")

        self.gridLayout_6.addWidget(self.txtweb, 12, 8, 1, 3)

        self.label_54 = QLabel(self.tabWidgetPage1)
        self.label_54.setObjectName("label_54")

        self.gridLayout_6.addWidget(self.label_54, 9, 5, 1, 1)

        self.txtMovil = QLineEdit(self.tabWidgetPage1)
        self.txtMovil.setObjectName("txtMovil")
        self.txtMovil.setMaximumSize(QSize(150, 16777215))

        self.gridLayout_6.addWidget(self.txtMovil, 11, 8, 1, 1)

        self.txttelefono1 = QLineEdit(self.tabWidgetPage1)
        self.txttelefono1.setObjectName("txttelefono1")
        self.txttelefono1.setMaximumSize(QSize(150, 16777215))
        self.txttelefono1.setClearButtonEnabled(True)

        self.gridLayout_6.addWidget(self.txttelefono1, 11, 2, 1, 1)

        self.label_17 = QLabel(self.tabWidgetPage1)
        self.label_17.setObjectName("label_17")
        sizePolicy.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy)
        self.label_17.setMinimumSize(QSize(80, 0))

        self.gridLayout_6.addWidget(self.label_17, 11, 1, 1, 1)

        self.txtCiudadRCS = QLineEdit(self.tabWidgetPage1)
        self.txtCiudadRCS.setObjectName("txtCiudadRCS")

        self.gridLayout_6.addWidget(self.txtCiudadRCS, 9, 6, 1, 1)

        self.txtEmpresa = QLineEdit(self.tabWidgetPage1)
        self.txtEmpresa.setObjectName("txtEmpresa")
        self.txtEmpresa.setMinimumSize(QSize(332, 0))
        self.txtEmpresa.setMaximumSize(QSize(16777215, 16777215))
        self.txtEmpresa.setReadOnly(False)
        self.txtEmpresa.setClearButtonEnabled(True)

        self.gridLayout_6.addWidget(self.txtEmpresa, 1, 4, 1, 3)

        self.label_14 = QLabel(self.tabWidgetPage1)
        self.label_14.setObjectName("label_14")
        sizePolicy.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy)

        self.gridLayout_6.addWidget(self.label_14, 4, 1, 1, 1)

        self.label_75 = QLabel(self.tabWidgetPage1)
        self.label_75.setObjectName("label_75")

        self.gridLayout_6.addWidget(self.label_75, 1, 3, 1, 1)

        self.label_74 = QLabel(self.tabWidgetPage1)
        self.label_74.setObjectName("label_74")

        self.gridLayout_6.addWidget(self.label_74, 0, 1, 1, 1)

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
        self.cboFormajuridica.setObjectName("cboFormajuridica")
        self.cboFormajuridica.setMaximumSize(QSize(205, 16777215))
        self.cboFormajuridica.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToContents
        )
        self.cboFormajuridica.setMinimumContentsLength(150)

        self.gridLayout_6.addWidget(self.cboFormajuridica, 1, 8, 1, 1)

        self.label_57 = QLabel(self.tabWidgetPage1)
        self.label_57.setObjectName("label_57")

        self.gridLayout_6.addWidget(self.label_57, 9, 7, 1, 1)

        self.label_24 = QLabel(self.tabWidgetPage1)
        self.label_24.setObjectName("label_24")

        self.gridLayout_6.addWidget(self.label_24, 1, 7, 1, 1)

        self.txtcp = QLineEdit(self.tabWidgetPage1)
        self.txtcp.setObjectName("txtcp")
        self.txtcp.setMaximumSize(QSize(100, 16777215))
        self.txtcp.setClearButtonEnabled(True)

        self.gridLayout_6.addWidget(self.txtcp, 4, 2, 1, 1)

        self.label_15 = QLabel(self.tabWidgetPage1)
        self.label_15.setObjectName("label_15")
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)

        self.gridLayout_6.addWidget(self.label_15, 4, 9, 1, 1)

        self.txtpoblacion = QLineEdit(self.tabWidgetPage1)
        self.txtpoblacion.setObjectName("txtpoblacion")
        self.txtpoblacion.setClearButtonEnabled(True)

        self.gridLayout_6.addWidget(self.txtpoblacion, 4, 4, 1, 5)

        self.label_18 = QLabel(self.tabWidgetPage1)
        self.label_18.setObjectName("label_18")
        sizePolicy.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy)
        self.label_18.setMinimumSize(QSize(80, 0))

        self.gridLayout_6.addWidget(self.label_18, 11, 3, 1, 1)

        self.txtcMail = QLineEdit(self.tabWidgetPage1)
        self.txtcMail.setObjectName("txtcMail")

        self.gridLayout_6.addWidget(self.txtcMail, 12, 2, 1, 4)

        self.cboPais = QComboBox(self.tabWidgetPage1)
        self.cboPais.setObjectName("cboPais")
        self.cboPais.setMinimumSize(QSize(168, 0))
        self.cboPais.setMaximumSize(QSize(250, 16777215))

        self.gridLayout_6.addWidget(self.cboPais, 2, 2, 1, 2)

        self.txttelefono2 = QLineEdit(self.tabWidgetPage1)
        self.txttelefono2.setObjectName("txttelefono2")
        self.txttelefono2.setMaximumSize(QSize(16777215, 16777215))
        self.txttelefono2.setClearButtonEnabled(True)

        self.gridLayout_6.addWidget(self.txttelefono2, 11, 5, 1, 1)

        self.gridLayout_12.addLayout(self.gridLayout_6, 2, 0, 1, 4)

        self.tabWidget.addTab(self.tabWidgetPage1, "")
        self.tab = QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_24 = QGridLayout(self.tab)
        self.gridLayout_24.setObjectName("gridLayout_24")
        self.tabWidget_2 = QTabWidget(self.tab)
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tabWidget_2.setEnabled(True)
        self.tabWidget_2.setMinimumSize(QSize(0, 0))
        self.tab_12 = QWidget()
        self.tab_12.setObjectName("tab_12")
        self.gridLayout_21 = QGridLayout(self.tab_12)
        self.gridLayout_21.setObjectName("gridLayout_21")
        self.groupBox_14 = QGroupBox(self.tab_12)
        self.groupBox_14.setObjectName("groupBox_14")
        sizePolicy1 = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBox_14.sizePolicy().hasHeightForWidth())
        self.groupBox_14.setSizePolicy(sizePolicy1)
        self.gridLayout_16 = QGridLayout(self.groupBox_14)
        self.gridLayout_16.setObjectName("gridLayout_16")
        self.cboDivisas = QComboBox(self.groupBox_14)
        self.cboDivisas.setObjectName("cboDivisas")

        self.gridLayout_16.addWidget(self.cboDivisas, 1, 1, 1, 1)

        self.chk_upate_divisas = QCheckBox(self.groupBox_14)
        self.chk_upate_divisas.setObjectName("chk_upate_divisas")

        self.gridLayout_16.addWidget(self.chk_upate_divisas, 0, 0, 1, 2)

        self.label_42 = QLabel(self.groupBox_14)
        self.label_42.setObjectName("label_42")
        sizePolicy.setHeightForWidth(self.label_42.sizePolicy().hasHeightForWidth())
        self.label_42.setSizePolicy(sizePolicy)

        self.gridLayout_16.addWidget(self.label_42, 1, 0, 1, 1)

        self.gridLayout_21.addWidget(self.groupBox_14, 2, 1, 1, 1)

        self.groupBox_4 = QGroupBox(self.tab_12)
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout_17 = QGridLayout(self.groupBox_4)
        self.gridLayout_17.setObjectName("gridLayout_17")
        self.chkIRPF = QCheckBox(self.groupBox_4)
        self.chkIRPF.setObjectName("chkIRPF")
        self.chkIRPF.setMaximumSize(QSize(135, 16777215))

        self.gridLayout_17.addWidget(self.chkIRPF, 1, 0, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_71 = QLabel(self.groupBox_4)
        self.label_71.setObjectName("label_71")

        self.horizontalLayout_5.addWidget(self.label_71)

        self.spinPorc_irpf = QDoubleSpinBox(self.groupBox_4)
        self.spinPorc_irpf.setObjectName("spinPorc_irpf")
        self.spinPorc_irpf.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.spinPorc_irpf.setMinimum(-999999.000000000000000)
        self.spinPorc_irpf.setMaximum(9999999.000000000000000)

        self.horizontalLayout_5.addWidget(self.spinPorc_irpf)

        self.gridLayout_17.addLayout(self.horizontalLayout_5, 2, 0, 1, 1)

        self.gridLayout_21.addWidget(self.groupBox_4, 3, 0, 1, 1)

        self.groupBox_12 = QGroupBox(self.tab_12)
        self.groupBox_12.setObjectName("groupBox_12")
        self.gridLayout_7 = QGridLayout(self.groupBox_12)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.label_222 = QLabel(self.groupBox_12)
        self.label_222.setObjectName("label_222")
        sizePolicy2 = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed
        )
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_222.sizePolicy().hasHeightForWidth())
        self.label_222.setSizePolicy(sizePolicy2)

        self.gridLayout_7.addWidget(self.label_222, 0, 0, 1, 1)

        self.txtDecimalesTotales = QSpinBox(self.groupBox_12)
        self.txtDecimalesTotales.setObjectName("txtDecimalesTotales")
        self.txtDecimalesTotales.setValue(2)

        self.gridLayout_7.addWidget(self.txtDecimalesTotales, 0, 1, 1, 2)

        self.label_85 = QLabel(self.groupBox_12)
        self.label_85.setObjectName("label_85")

        self.gridLayout_7.addWidget(self.label_85, 1, 0, 1, 1)

        self.txtDecimalesPrecios = QSpinBox(self.groupBox_12)
        self.txtDecimalesPrecios.setObjectName("txtDecimalesPrecios")
        self.txtDecimalesPrecios.setValue(2)

        self.gridLayout_7.addWidget(self.txtDecimalesPrecios, 1, 1, 1, 2)

        self.gridLayout_21.addWidget(self.groupBox_12, 0, 2, 1, 1)

        self.groupBox_3 = QGroupBox(self.tab_12)
        self.groupBox_3.setObjectName("groupBox_3")
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.gridLayout_11 = QGridLayout(self.groupBox_3)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.label_25 = QLabel(self.groupBox_3)
        self.label_25.setObjectName("label_25")

        self.gridLayout_11.addWidget(self.label_25, 0, 0, 1, 1)

        self.spinDigitos = QSpinBox(self.groupBox_3)
        self.spinDigitos.setObjectName("spinDigitos")
        self.spinDigitos.setMaximum(45)
        self.spinDigitos.setValue(7)

        self.gridLayout_11.addWidget(self.spinDigitos, 0, 1, 1, 1)

        self.cboSerie = QComboBox(self.groupBox_3)
        self.cboSerie.setObjectName("cboSerie")

        self.gridLayout_11.addWidget(self.cboSerie, 1, 1, 1, 1)

        self.label_26 = QLabel(self.groupBox_3)
        self.label_26.setObjectName("label_26")

        self.gridLayout_11.addWidget(self.label_26, 1, 0, 1, 1)

        self.gridLayout_21.addWidget(self.groupBox_3, 3, 1, 1, 1)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_68 = QLabel(self.tab_12)
        self.label_68.setObjectName("label_68")

        self.horizontalLayout_8.addWidget(self.label_68)

        self.txtDiaCierre = QSpinBox(self.tab_12)
        self.txtDiaCierre.setObjectName("txtDiaCierre")
        self.txtDiaCierre.setMinimum(1)
        self.txtDiaCierre.setMaximum(31)
        self.txtDiaCierre.setValue(31)

        self.horizontalLayout_8.addWidget(self.txtDiaCierre)

        self.tstMesCierre = QSpinBox(self.tab_12)
        self.tstMesCierre.setObjectName("tstMesCierre")
        self.tstMesCierre.setMinimum(1)
        self.tstMesCierre.setMaximum(12)
        self.tstMesCierre.setValue(12)

        self.horizontalLayout_8.addWidget(self.tstMesCierre)

        self.gridLayout_21.addLayout(self.horizontalLayout_8, 1, 0, 1, 1)

        self.groupBox_5 = QGroupBox(self.tab_12)
        self.groupBox_5.setObjectName("groupBox_5")
        self.chkEnlace_web = QCheckBox(self.groupBox_5)
        self.chkEnlace_web.setObjectName("chkEnlace_web")
        self.chkEnlace_web.setGeometry(QRect(0, 50, 307, 22))
        self.chkInternacional = QCheckBox(self.groupBox_5)
        self.chkInternacional.setObjectName("chkInternacional")
        self.chkInternacional.setGeometry(QRect(0, 80, 307, 22))

        self.gridLayout_21.addWidget(self.groupBox_5, 0, 0, 1, 1)

        self.groupBox_2 = QGroupBox(self.tab_12)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_10 = QGridLayout(self.groupBox_2)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.chkAutocodificiar = QCheckBox(self.groupBox_2)
        self.chkAutocodificiar.setObjectName("chkAutocodificiar")
        self.chkAutocodificiar.setChecked(True)

        self.gridLayout_10.addWidget(self.chkAutocodificiar, 0, 0, 1, 1)

        self.txttamano_codigoart = QSpinBox(self.groupBox_2)
        self.txttamano_codigoart.setObjectName("txttamano_codigoart")
        self.txttamano_codigoart.setMaximumSize(QSize(60, 16777215))
        self.txttamano_codigoart.setValue(15)

        self.gridLayout_10.addWidget(self.txttamano_codigoart, 1, 1, 1, 1)

        self.label_41 = QLabel(self.groupBox_2)
        self.label_41.setObjectName("label_41")
        sizePolicy.setHeightForWidth(self.label_41.sizePolicy().hasHeightForWidth())
        self.label_41.setSizePolicy(sizePolicy)

        self.gridLayout_10.addWidget(self.label_41, 1, 0, 1, 1)

        self.gridLayout_21.addWidget(self.groupBox_2, 2, 0, 1, 1)

        self.groupBox = QGroupBox(self.tab_12)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_9 = QGridLayout(self.groupBox)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.spinMargen = QDoubleSpinBox(self.groupBox)
        self.spinMargen.setObjectName("spinMargen")

        self.gridLayout_9.addWidget(self.spinMargen, 1, 3, 1, 1)

        self.label_33 = QLabel(self.groupBox)
        self.label_33.setObjectName("label_33")

        self.gridLayout_9.addWidget(self.label_33, 2, 1, 1, 1)

        self.cboTarifa = QComboBox(self.groupBox)
        self.cboTarifa.setObjectName("cboTarifa")

        self.gridLayout_9.addWidget(self.cboTarifa, 0, 3, 1, 1)

        self.label_31 = QLabel(self.groupBox)
        self.label_31.setObjectName("label_31")

        self.gridLayout_9.addWidget(self.label_31, 1, 1, 1, 1)

        self.spinMargen_minimo = QDoubleSpinBox(self.groupBox)
        self.spinMargen_minimo.setObjectName("spinMargen_minimo")

        self.gridLayout_9.addWidget(self.spinMargen_minimo, 2, 3, 1, 1)

        self.label_58 = QLabel(self.groupBox)
        self.label_58.setObjectName("label_58")

        self.gridLayout_9.addWidget(self.label_58, 0, 1, 1, 1)

        self.gridLayout_21.addWidget(self.groupBox, 0, 1, 2, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.btnDeleteLogo = QPushButton(self.tab_12)
        self.btnDeleteLogo.setObjectName("btnDeleteLogo")

        self.gridLayout.addWidget(self.btnDeleteLogo, 2, 0, 1, 1)

        self.btnAddLogo = QPushButton(self.tab_12)
        self.btnAddLogo.setObjectName("btnAddLogo")

        self.gridLayout.addWidget(self.btnAddLogo, 1, 0, 1, 1)

        self.gridLayout_21.addLayout(self.gridLayout, 4, 2, 1, 1)

        self.groupBox_6 = QGroupBox(self.tab_12)
        self.groupBox_6.setObjectName("groupBox_6")
        self.imgLogo = QLabel(self.groupBox_6)
        self.imgLogo.setObjectName("imgLogo")
        self.imgLogo.setGeometry(QRect(20, 40, 431, 221))
        self.imgLogo.setMaximumSize(QSize(1211, 348))
        self.imgLogo.setPixmap(QPixmap(":/PNG/resources/icons/png/LogoIcono.png"))
        self.imgLogo.setScaledContents(False)
        self.imgLogo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_21.addWidget(self.groupBox_6, 1, 2, 3, 1)

        self.tabWidget_2.addTab(self.tab_12, "")
        self.tab_6 = QWidget()
        self.tab_6.setObjectName("tab_6")
        self.verticalLayout_5 = QVBoxLayout(self.tab_6)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_36 = QLabel(self.tab_6)
        self.label_36.setObjectName("label_36")
        self.label_36.setStyleSheet(
            "background-color: rgb(0, 0, 127);\n" "color: rgb(255, 255, 255);"
        )
        self.label_36.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_5.addWidget(self.label_36)

        self.txtcCometarioAlbaran = QTextEdit(self.tab_6)
        self.txtcCometarioAlbaran.setObjectName("txtcCometarioAlbaran")

        self.verticalLayout_5.addWidget(self.txtcCometarioAlbaran)

        self.label_35 = QLabel(self.tab_6)
        self.label_35.setObjectName("label_35")
        self.label_35.setStyleSheet(
            "background-color: rgb(0, 0, 127);\n" "color: rgb(255, 255, 255);"
        )
        self.label_35.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_5.addWidget(self.label_35)

        self.txtccomentario_factura = QTextEdit(self.tab_6)
        self.txtccomentario_factura.setObjectName("txtccomentario_factura")

        self.verticalLayout_5.addWidget(self.txtccomentario_factura)

        self.tabWidget_2.addTab(self.tab_6, "")
        self.tab_8 = QWidget()
        self.tab_8.setObjectName("tab_8")
        self.gridLayout_15 = QGridLayout(self.tab_8)
        self.gridLayout_15.setObjectName("gridLayout_15")
        self.lineEdit_9 = QLineEdit(self.tab_8)
        self.lineEdit_9.setObjectName("lineEdit_9")

        self.gridLayout_15.addWidget(self.lineEdit_9, 5, 1, 1, 1)

        self.label_47 = QLabel(self.tab_8)
        self.label_47.setObjectName("label_47")

        self.gridLayout_15.addWidget(self.label_47, 1, 0, 1, 1)

        self.lineEdit_7 = QLineEdit(self.tab_8)
        self.lineEdit_7.setObjectName("lineEdit_7")

        self.gridLayout_15.addWidget(self.lineEdit_7, 3, 1, 1, 1)

        self.txt_horario_primer_dia = QLineEdit(self.tab_8)
        self.txt_horario_primer_dia.setObjectName("txt_horario_primer_dia")
        self.txt_horario_primer_dia.setClearButtonEnabled(True)

        self.gridLayout_15.addWidget(self.txt_horario_primer_dia, 0, 1, 1, 1)

        self.label_46 = QLabel(self.tab_8)
        self.label_46.setObjectName("label_46")

        self.gridLayout_15.addWidget(self.label_46, 0, 0, 1, 1)

        self.label_45 = QLabel(self.tab_8)
        self.label_45.setObjectName("label_45")

        self.gridLayout_15.addWidget(self.label_45, 4, 0, 1, 1)

        self.label_70 = QLabel(self.tab_8)
        self.label_70.setObjectName("label_70")

        self.gridLayout_15.addWidget(self.label_70, 6, 0, 1, 1)

        self.label_44 = QLabel(self.tab_8)
        self.label_44.setObjectName("label_44")

        self.gridLayout_15.addWidget(self.label_44, 3, 0, 1, 1)

        self.txt_horario_dia_normal = QLineEdit(self.tab_8)
        self.txt_horario_dia_normal.setObjectName("txt_horario_dia_normal")
        self.txt_horario_dia_normal.setClearButtonEnabled(True)

        self.gridLayout_15.addWidget(self.txt_horario_dia_normal, 1, 1, 1, 1)

        self.label_69 = QLabel(self.tab_8)
        self.label_69.setObjectName("label_69")

        self.gridLayout_15.addWidget(self.label_69, 5, 0, 1, 1)

        self.txt_horario_ultimo_dia = QLineEdit(self.tab_8)
        self.txt_horario_ultimo_dia.setObjectName("txt_horario_ultimo_dia")
        self.txt_horario_ultimo_dia.setClearButtonEnabled(True)

        self.gridLayout_15.addWidget(self.txt_horario_ultimo_dia, 2, 1, 1, 1)

        self.label_48 = QLabel(self.tab_8)
        self.label_48.setObjectName("label_48")

        self.gridLayout_15.addWidget(self.label_48, 2, 0, 1, 1)

        self.groupBox_7 = QGroupBox(self.tab_8)
        self.groupBox_7.setObjectName("groupBox_7")
        self.txtGoogleCalendarID = QLineEdit(self.groupBox_7)
        self.txtGoogleCalendarID.setObjectName("txtGoogleCalendarID")
        self.txtGoogleCalendarID.setGeometry(QRect(190, 40, 341, 32))
        self.txtOauthToken = QLineEdit(self.groupBox_7)
        self.txtOauthToken.setObjectName("txtOauthToken")
        self.txtOauthToken.setGeometry(QRect(190, 80, 341, 32))
        self.txtOauthRefreshToken = QLineEdit(self.groupBox_7)
        self.txtOauthRefreshToken.setObjectName("txtOauthRefreshToken")
        self.txtOauthRefreshToken.setGeometry(QRect(190, 120, 341, 32))
        self.txtTokenExpirity = QLineEdit(self.groupBox_7)
        self.txtTokenExpirity.setObjectName("txtTokenExpirity")
        self.txtTokenExpirity.setGeometry(QRect(190, 160, 341, 32))
        self.label_72 = QLabel(self.groupBox_7)
        self.label_72.setObjectName("label_72")
        self.label_72.setGeometry(QRect(20, 50, 161, 18))
        self.label_73 = QLabel(self.groupBox_7)
        self.label_73.setObjectName("label_73")
        self.label_73.setGeometry(QRect(20, 90, 161, 18))
        self.label_76 = QLabel(self.groupBox_7)
        self.label_76.setObjectName("label_76")
        self.label_76.setGeometry(QRect(20, 130, 161, 18))
        self.label_77 = QLabel(self.groupBox_7)
        self.label_77.setObjectName("label_77")
        self.label_77.setGeometry(QRect(20, 170, 161, 18))

        self.gridLayout_15.addWidget(self.groupBox_7, 7, 1, 1, 1)

        self.lineEdit_10 = QLineEdit(self.tab_8)
        self.lineEdit_10.setObjectName("lineEdit_10")

        self.gridLayout_15.addWidget(self.lineEdit_10, 6, 1, 1, 1)

        self.lineEdit_8 = QLineEdit(self.tab_8)
        self.lineEdit_8.setObjectName("lineEdit_8")

        self.gridLayout_15.addWidget(self.lineEdit_8, 4, 1, 1, 1)

        self.tabWidget_2.addTab(self.tab_8, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName("tab_5")
        self.verticalLayout = QVBoxLayout(self.tab_5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.chkContabilidad = QCheckBox(self.tab_5)
        self.chkContabilidad.setObjectName("chkContabilidad")
        self.chkContabilidad.setChecked(True)

        self.verticalLayout.addWidget(self.chkContabilidad)

        self.gridLayout_8 = QGridLayout()
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.txtCuenta_venta_servicios = QLineEdit(self.tab_5)
        self.txtCuenta_venta_servicios.setObjectName("txtCuenta_venta_servicios")
        self.txtCuenta_venta_servicios.setMaximumSize(QSize(200, 16777215))
        self.txtCuenta_venta_servicios.setClearButtonEnabled(True)

        self.gridLayout_8.addWidget(self.txtCuenta_venta_servicios, 5, 1, 1, 1)

        self.txtCuenta_venta_mercaderias = QLineEdit(self.tab_5)
        self.txtCuenta_venta_mercaderias.setObjectName("txtCuenta_venta_mercaderias")
        self.txtCuenta_venta_mercaderias.setMaximumSize(QSize(200, 16777215))
        self.txtCuenta_venta_mercaderias.setClearButtonEnabled(True)

        self.gridLayout_8.addWidget(self.txtCuenta_venta_mercaderias, 4, 1, 1, 1)

        self.txtcuenta_acreedores = QLineEdit(self.tab_5)
        self.txtcuenta_acreedores.setObjectName("txtcuenta_acreedores")
        self.txtcuenta_acreedores.setMaximumSize(QSize(200, 16777215))
        self.txtcuenta_acreedores.setClearButtonEnabled(True)

        self.gridLayout_8.addWidget(self.txtcuenta_acreedores, 3, 1, 1, 1)

        self.label_29 = QLabel(self.tab_5)
        self.label_29.setObjectName("label_29")
        self.label_29.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_8.addWidget(self.label_29, 3, 0, 1, 1)

        self.label_12 = QLabel(self.tab_5)
        self.label_12.setObjectName("label_12")
        self.label_12.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_8.addWidget(self.label_12, 4, 0, 1, 1)

        self.label_37 = QLabel(self.tab_5)
        self.label_37.setObjectName("label_37")
        self.label_37.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_8.addWidget(self.label_37, 5, 0, 1, 1)

        self.label_28 = QLabel(self.tab_5)
        self.label_28.setObjectName("label_28")
        self.label_28.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_8.addWidget(self.label_28, 2, 0, 1, 1)

        self.txtcuenta_proveedores = QLineEdit(self.tab_5)
        self.txtcuenta_proveedores.setObjectName("txtcuenta_proveedores")
        self.txtcuenta_proveedores.setMaximumSize(QSize(200, 16777215))
        self.txtcuenta_proveedores.setClearButtonEnabled(True)

        self.gridLayout_8.addWidget(self.txtcuenta_proveedores, 2, 1, 1, 1)

        self.txtdigitos_cuentas = QSpinBox(self.tab_5)
        self.txtdigitos_cuentas.setObjectName("txtdigitos_cuentas")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(
            self.txtdigitos_cuentas.sizePolicy().hasHeightForWidth()
        )
        self.txtdigitos_cuentas.setSizePolicy(sizePolicy3)
        self.txtdigitos_cuentas.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.txtdigitos_cuentas.setMaximum(20)
        self.txtdigitos_cuentas.setValue(8)

        self.gridLayout_8.addWidget(self.txtdigitos_cuentas, 0, 1, 1, 1)

        self.txtcuentaCliente = QLineEdit(self.tab_5)
        self.txtcuentaCliente.setObjectName("txtcuentaCliente")
        self.txtcuentaCliente.setMaximumSize(QSize(200, 16777215))
        self.txtcuentaCliente.setClearButtonEnabled(True)

        self.gridLayout_8.addWidget(self.txtcuentaCliente, 1, 1, 1, 1)

        self.label_30 = QLabel(self.tab_5)
        self.label_30.setObjectName("label_30")
        self.label_30.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_8.addWidget(self.label_30, 0, 0, 1, 1)

        self.label_27 = QLabel(self.tab_5)
        self.label_27.setObjectName("label_27")
        self.label_27.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_8.addWidget(self.label_27, 1, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.gridLayout_8.addItem(self.horizontalSpacer_2, 1, 2, 1, 1)

        self.verticalLayout.addLayout(self.gridLayout_8)

        self.gridLayout_13 = QGridLayout()
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.ivarepercutidore1 = QLineEdit(self.tab_5)
        self.ivarepercutidore1.setObjectName("ivarepercutidore1")
        self.ivarepercutidore1.setClearButtonEnabled(True)

        self.gridLayout_13.addWidget(self.ivarepercutidore1, 1, 5, 1, 1)

        self.ivarepercutido3 = QLineEdit(self.tab_5)
        self.ivarepercutido3.setObjectName("ivarepercutido3")
        self.ivarepercutido3.setClearButtonEnabled(True)

        self.gridLayout_13.addWidget(self.ivarepercutido3, 3, 4, 1, 1)

        self.label_65 = QLabel(self.tab_5)
        self.label_65.setObjectName("label_65")

        self.gridLayout_13.addWidget(self.label_65, 4, 3, 1, 1)

        self.txtIvasoportado4 = QLineEdit(self.tab_5)
        self.txtIvasoportado4.setObjectName("txtIvasoportado4")
        self.txtIvasoportado4.setClearButtonEnabled(True)

        self.gridLayout_13.addWidget(self.txtIvasoportado4, 4, 1, 1, 1)

        self.label_59 = QLabel(self.tab_5)
        self.label_59.setObjectName("label_59")

        self.gridLayout_13.addWidget(self.label_59, 2, 0, 1, 1)

        self.txtIvasoportado2 = QLineEdit(self.tab_5)
        self.txtIvasoportado2.setObjectName("txtIvasoportado2")
        self.txtIvasoportado2.setClearButtonEnabled(True)

        self.gridLayout_13.addWidget(self.txtIvasoportado2, 2, 1, 1, 1)

        self.label_63 = QLabel(self.tab_5)
        self.label_63.setObjectName("label_63")

        self.gridLayout_13.addWidget(self.label_63, 2, 3, 1, 1)

        self.label_38 = QLabel(self.tab_5)
        self.label_38.setObjectName("label_38")
        self.label_38.setMaximumSize(QSize(16777214, 15))
        self.label_38.setStyleSheet(
            "background-color: rgb(0, 0, 127);\n"
            "border-color: rgb(0, 0, 42);\n"
            "color: rgb(255, 255, 255);"
        )
        self.label_38.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_13.addWidget(self.label_38, 0, 1, 1, 1)

        self.ivasoportadore4 = QLineEdit(self.tab_5)
        self.ivasoportadore4.setObjectName("ivasoportadore4")
        self.ivasoportadore4.setClearButtonEnabled(True)

        self.gridLayout_13.addWidget(self.ivasoportadore4, 4, 2, 1, 1)

        self.ivasoportadore3 = QLineEdit(self.tab_5)
        self.ivasoportadore3.setObjectName("ivasoportadore3")
        self.ivasoportadore3.setClearButtonEnabled(True)

        self.gridLayout_13.addWidget(self.ivasoportadore3, 3, 2, 1, 1)

        self.label_39 = QLabel(self.tab_5)
        self.label_39.setObjectName("label_39")
        self.label_39.setMaximumSize(QSize(16777214, 15))
        self.label_39.setStyleSheet(
            "background-color: rgb(0, 0, 127);\n"
            "border-color: rgb(0, 0, 42);\n"
            "color: rgb(255, 255, 255);"
        )
        self.label_39.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_13.addWidget(self.label_39, 0, 4, 1, 1)

        self.label_40 = QLabel(self.tab_5)
        self.label_40.setObjectName("label_40")

        self.gridLayout_13.addWidget(self.label_40, 1, 0, 1, 1)

        self.label_62 = QLabel(self.tab_5)
        self.label_62.setObjectName("label_62")

        self.gridLayout_13.addWidget(self.label_62, 1, 3, 1, 1)

        self.txtIvasoportado1 = QLineEdit(self.tab_5)
        self.txtIvasoportado1.setObjectName("txtIvasoportado1")
        self.txtIvasoportado1.setClearButtonEnabled(True)

        self.gridLayout_13.addWidget(self.txtIvasoportado1, 1, 1, 1, 1)

        self.ivarepercutido1 = QLineEdit(self.tab_5)
        self.ivarepercutido1.setObjectName("ivarepercutido1")
        self.ivarepercutido1.setClearButtonEnabled(True)

        self.gridLayout_13.addWidget(self.ivarepercutido1, 1, 4, 1, 1)

        self.ivarepercutido4 = QLineEdit(self.tab_5)
        self.ivarepercutido4.setObjectName("ivarepercutido4")
        self.ivarepercutido4.setClearButtonEnabled(True)

        self.gridLayout_13.addWidget(self.ivarepercutido4, 4, 4, 1, 1)

        self.ivarepercutido2 = QLineEdit(self.tab_5)
        self.ivarepercutido2.setObjectName("ivarepercutido2")
        self.ivarepercutido2.setClearButtonEnabled(True)

        self.gridLayout_13.addWidget(self.ivarepercutido2, 2, 4, 1, 1)

        self.label_60 = QLabel(self.tab_5)
        self.label_60.setObjectName("label_60")

        self.gridLayout_13.addWidget(self.label_60, 3, 0, 1, 1)

        self.txtIvasoportado3 = QLineEdit(self.tab_5)
        self.txtIvasoportado3.setObjectName("txtIvasoportado3")
        self.txtIvasoportado3.setClearButtonEnabled(True)

        self.gridLayout_13.addWidget(self.txtIvasoportado3, 3, 1, 1, 1)

        self.label_64 = QLabel(self.tab_5)
        self.label_64.setObjectName("label_64")

        self.gridLayout_13.addWidget(self.label_64, 3, 3, 1, 1)

        self.label_61 = QLabel(self.tab_5)
        self.label_61.setObjectName("label_61")

        self.gridLayout_13.addWidget(self.label_61, 4, 0, 1, 1)

        self.ivasoportadore1 = QLineEdit(self.tab_5)
        self.ivasoportadore1.setObjectName("ivasoportadore1")
        self.ivasoportadore1.setClearButtonEnabled(True)

        self.gridLayout_13.addWidget(self.ivasoportadore1, 1, 2, 1, 1)

        self.ivasoportadore2 = QLineEdit(self.tab_5)
        self.ivasoportadore2.setObjectName("ivasoportadore2")
        self.ivasoportadore2.setClearButtonEnabled(True)

        self.gridLayout_13.addWidget(self.ivasoportadore2, 2, 2, 1, 1)

        self.label_66 = QLabel(self.tab_5)
        self.label_66.setObjectName("label_66")
        self.label_66.setMaximumSize(QSize(16777214, 15))
        self.label_66.setStyleSheet(
            "background-color: rgb(0, 0, 127);\n" "color: rgb(255, 255, 255);"
        )

        self.gridLayout_13.addWidget(self.label_66, 0, 2, 1, 1)

        self.label_67 = QLabel(self.tab_5)
        self.label_67.setObjectName("label_67")
        self.label_67.setMaximumSize(QSize(16777214, 15))
        self.label_67.setStyleSheet(
            "background-color: rgb(0, 0, 127);\n" "color: rgb(255, 255, 255);"
        )

        self.gridLayout_13.addWidget(self.label_67, 0, 5, 1, 1)

        self.ivarepercutidore3 = QLineEdit(self.tab_5)
        self.ivarepercutidore3.setObjectName("ivarepercutidore3")
        self.ivarepercutidore3.setClearButtonEnabled(True)

        self.gridLayout_13.addWidget(self.ivarepercutidore3, 3, 5, 1, 1)

        self.ivarepercutidore2 = QLineEdit(self.tab_5)
        self.ivarepercutidore2.setObjectName("ivarepercutidore2")
        self.ivarepercutidore2.setClearButtonEnabled(True)

        self.gridLayout_13.addWidget(self.ivarepercutidore2, 2, 5, 1, 1)

        self.ivarepercutidore4 = QLineEdit(self.tab_5)
        self.ivarepercutidore4.setObjectName("ivarepercutidore4")
        self.ivarepercutidore4.setClearButtonEnabled(True)

        self.gridLayout_13.addWidget(self.ivarepercutidore4, 4, 5, 1, 1)

        self.label_9 = QLabel(self.tab_5)
        self.label_9.setObjectName("label_9")

        self.gridLayout_13.addWidget(self.label_9, 5, 1, 1, 1)

        self.txtcuenta_cobros = QLineEdit(self.tab_5)
        self.txtcuenta_cobros.setObjectName("txtcuenta_cobros")

        self.gridLayout_13.addWidget(self.txtcuenta_cobros, 5, 2, 1, 1)

        self.label_10 = QLabel(self.tab_5)
        self.label_10.setObjectName("label_10")

        self.gridLayout_13.addWidget(self.label_10, 5, 4, 1, 1)

        self.txtcuenta_pagos = QLineEdit(self.tab_5)
        self.txtcuenta_pagos.setObjectName("txtcuenta_pagos")

        self.gridLayout_13.addWidget(self.txtcuenta_pagos, 5, 5, 1, 1)

        self.verticalLayout.addLayout(self.gridLayout_13)

        self.verticalSpacer_2 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.tabWidget_2.addTab(self.tab_5, "")

        self.gridLayout_24.addWidget(self.tabWidget_2, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab, "")
        self.tabWidgetPage2 = QWidget()
        self.tabWidgetPage2.setObjectName("tabWidgetPage2")
        self.gridLayout_5 = QGridLayout(self.tabWidgetPage2)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_2 = QLabel(self.tabWidgetPage2)
        self.label_2.setObjectName("label_2")

        self.gridLayout_5.addWidget(self.label_2, 0, 0, 1, 1)

        self.mysql_frame = QFrame(self.tabWidgetPage2)
        self.mysql_frame.setObjectName("mysql_frame")
        self.mysql_frame.setEnabled(True)
        sizePolicy4 = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum
        )
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.mysql_frame.sizePolicy().hasHeightForWidth())
        self.mysql_frame.setSizePolicy(sizePolicy4)
        self.mysql_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.mysql_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.mysql_frame)
        self.gridLayout_4.setObjectName("gridLayout_4")

        self.gridLayout_5.addWidget(self.mysql_frame, 6, 0, 1, 5)

        self.groupBox_8 = QGroupBox(self.tabWidgetPage2)
        self.groupBox_8.setObjectName("groupBox_8")
        self.gridLayoutWidget_2 = QWidget(self.groupBox_8)
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayoutWidget_2.setGeometry(QRect(100, 40, 373, 201))
        self.gridLayout_19 = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_19.setObjectName("gridLayout_19")
        self.gridLayout_19.setContentsMargins(0, 0, 0, 0)
        self.label_82 = QLabel(self.gridLayoutWidget_2)
        self.label_82.setObjectName("label_82")

        self.gridLayout_19.addWidget(self.label_82, 1, 0, 1, 2)

        self.txtUsuarioMariaDB = QLineEdit(self.gridLayoutWidget_2)
        self.txtUsuarioMariaDB.setObjectName("txtUsuarioMariaDB")

        self.gridLayout_19.addWidget(self.txtUsuarioMariaDB, 2, 3, 1, 2)

        self.txtPortMariadb = QLineEdit(self.gridLayoutWidget_2)
        self.txtPortMariadb.setObjectName("txtPortMariadb")

        self.gridLayout_19.addWidget(self.txtPortMariadb, 0, 4, 1, 1)

        self.txtPasswordMariaDB = QLineEdit(self.gridLayoutWidget_2)
        self.txtPasswordMariaDB.setObjectName("txtPasswordMariaDB")

        self.gridLayout_19.addWidget(self.txtPasswordMariaDB, 3, 3, 1, 2)

        self.label_87 = QLabel(self.gridLayoutWidget_2)
        self.label_87.setObjectName("label_87")

        self.gridLayout_19.addWidget(self.label_87, 2, 0, 1, 2)

        self.txtNombreBD_MariaDB = QLineEdit(self.gridLayoutWidget_2)
        self.txtNombreBD_MariaDB.setObjectName("txtNombreBD_MariaDB")

        self.gridLayout_19.addWidget(self.txtNombreBD_MariaDB, 1, 3, 1, 2)

        self.label_86 = QLabel(self.gridLayoutWidget_2)
        self.label_86.setObjectName("label_86")

        self.gridLayout_19.addWidget(self.label_86, 0, 0, 1, 1)

        self.txtHostMariaDB = QLineEdit(self.gridLayoutWidget_2)
        self.txtHostMariaDB.setObjectName("txtHostMariaDB")

        self.gridLayout_19.addWidget(self.txtHostMariaDB, 0, 1, 1, 1)

        self.label_84 = QLabel(self.gridLayoutWidget_2)
        self.label_84.setObjectName("label_84")

        self.gridLayout_19.addWidget(self.label_84, 0, 3, 1, 1)

        self.label_83 = QLabel(self.gridLayoutWidget_2)
        self.label_83.setObjectName("label_83")

        self.gridLayout_19.addWidget(self.label_83, 3, 0, 1, 2)

        self.btnTestBDMariaDB = QPushButton(self.gridLayoutWidget_2)
        self.btnTestBDMariaDB.setObjectName("btnTestBDMariaDB")

        self.gridLayout_19.addWidget(self.btnTestBDMariaDB, 5, 3, 1, 2)

        self.btnCrearDBMariaDb = QPushButton(self.gridLayoutWidget_2)
        self.btnCrearDBMariaDb.setObjectName("btnCrearDBMariaDb")

        self.gridLayout_19.addWidget(self.btnCrearDBMariaDb, 5, 0, 1, 2)

        self.gridLayout_5.addWidget(self.groupBox_8, 2, 0, 4, 1)

        self.comboBox = QComboBox(self.tabWidgetPage2)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName("comboBox")

        self.gridLayout_5.addWidget(self.comboBox, 0, 1, 1, 2)

        self.sqlite_frame = QFrame(self.tabWidgetPage2)
        self.sqlite_frame.setObjectName("sqlite_frame")
        self.sqlite_frame.setEnabled(True)
        sizePolicy4.setHeightForWidth(
            self.sqlite_frame.sizePolicy().hasHeightForWidth()
        )
        self.sqlite_frame.setSizePolicy(sizePolicy4)
        self.sqlite_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.sqlite_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.sqlite_frame)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_55 = QLabel(self.sqlite_frame)
        self.label_55.setObjectName("label_55")

        self.gridLayout_3.addWidget(self.label_55, 2, 0, 1, 1)

        self.btnSeleccionarBDSQLiteConta = QPushButton(self.sqlite_frame)
        self.btnSeleccionarBDSQLiteConta.setObjectName("btnSeleccionarBDSQLiteConta")

        self.gridLayout_3.addWidget(self.btnSeleccionarBDSQLiteConta, 2, 2, 1, 1)

        self.btn_migrar = QPushButton(self.sqlite_frame)
        self.btn_migrar.setObjectName("btn_migrar")

        self.gridLayout_3.addWidget(self.btn_migrar, 3, 0, 1, 1)

        self.btnSelecionarBDSQLite = QPushButton(self.sqlite_frame)
        self.btnSelecionarBDSQLite.setObjectName("btnSelecionarBDSQLite")

        self.gridLayout_3.addWidget(self.btnSelecionarBDSQLite, 1, 2, 1, 1)

        self.label_3 = QLabel(self.sqlite_frame)
        self.label_3.setObjectName("label_3")

        self.gridLayout_3.addWidget(self.label_3, 1, 0, 1, 1)

        self.label_4 = QLabel(self.sqlite_frame)
        self.label_4.setObjectName("label_4")

        self.gridLayout_3.addWidget(self.label_4, 0, 0, 1, 2)

        self.txtRutaBd = QLineEdit(self.sqlite_frame)
        self.txtRutaBd.setObjectName("txtRutaBd")
        self.txtRutaBd.setEnabled(False)
        self.txtRutaBd.setMaximumSize(QSize(16777215, 20))

        self.gridLayout_3.addWidget(self.txtRutaBd, 1, 1, 1, 1)

        self.txtruta_bd_conta = QLineEdit(self.sqlite_frame)
        self.txtruta_bd_conta.setObjectName("txtruta_bd_conta")
        self.txtruta_bd_conta.setEnabled(False)
        self.txtruta_bd_conta.setMaximumSize(QSize(16777215, 20))

        self.gridLayout_3.addWidget(self.txtruta_bd_conta, 2, 1, 1, 1)

        self.gridLayout_5.addWidget(self.sqlite_frame, 1, 0, 1, 3)

        self.groupBox_9 = QGroupBox(self.tabWidgetPage2)
        self.groupBox_9.setObjectName("groupBox_9")
        self.gridLayoutWidget = QWidget(self.groupBox_9)
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(80, 40, 471, 201))
        self.gridLayout_18 = QGridLayout(self.gridLayoutWidget)
        self.gridLayout_18.setObjectName("gridLayout_18")
        self.gridLayout_18.setContentsMargins(0, 0, 0, 0)
        self.txtHostPostgreSQL = QLineEdit(self.gridLayoutWidget)
        self.txtHostPostgreSQL.setObjectName("txtHostPostgreSQL")

        self.gridLayout_18.addWidget(self.txtHostPostgreSQL, 0, 1, 1, 1)

        self.label_79 = QLabel(self.gridLayoutWidget)
        self.label_79.setObjectName("label_79")

        self.gridLayout_18.addWidget(self.label_79, 1, 0, 1, 2)

        self.label_78 = QLabel(self.gridLayoutWidget)
        self.label_78.setObjectName("label_78")

        self.gridLayout_18.addWidget(self.label_78, 0, 3, 1, 1)

        self.label_81 = QLabel(self.gridLayoutWidget)
        self.label_81.setObjectName("label_81")

        self.gridLayout_18.addWidget(self.label_81, 3, 0, 1, 2)

        self.txtPasswordPostgreSQL = QLineEdit(self.gridLayoutWidget)
        self.txtPasswordPostgreSQL.setObjectName("txtPasswordPostgreSQL")

        self.gridLayout_18.addWidget(self.txtPasswordPostgreSQL, 3, 3, 1, 2)

        self.lineEdit = QLineEdit(self.gridLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")

        self.gridLayout_18.addWidget(self.lineEdit, 0, 4, 1, 1)

        self.label_56 = QLabel(self.gridLayoutWidget)
        self.label_56.setObjectName("label_56")

        self.gridLayout_18.addWidget(self.label_56, 0, 0, 1, 1)

        self.txtNombreBD_PostgreSQL = QLineEdit(self.gridLayoutWidget)
        self.txtNombreBD_PostgreSQL.setObjectName("txtNombreBD_PostgreSQL")

        self.gridLayout_18.addWidget(self.txtNombreBD_PostgreSQL, 1, 3, 1, 2)

        self.label_80 = QLabel(self.gridLayoutWidget)
        self.label_80.setObjectName("label_80")

        self.gridLayout_18.addWidget(self.label_80, 2, 0, 1, 2)

        self.txtUsuarioPostgreSQL = QLineEdit(self.gridLayoutWidget)
        self.txtUsuarioPostgreSQL.setObjectName("txtUsuarioPostgreSQL")

        self.gridLayout_18.addWidget(self.txtUsuarioPostgreSQL, 2, 3, 1, 2)

        self.btnCrearDBPostgreSQL = QPushButton(self.gridLayoutWidget)
        self.btnCrearDBPostgreSQL.setObjectName("btnCrearDBPostgreSQL")

        self.gridLayout_18.addWidget(self.btnCrearDBPostgreSQL, 4, 0, 1, 2)

        self.btnTestDBPostgreSQL = QPushButton(self.gridLayoutWidget)
        self.btnTestDBPostgreSQL.setObjectName("btnTestDBPostgreSQL")

        self.gridLayout_18.addWidget(self.btnTestDBPostgreSQL, 4, 3, 1, 2)

        self.gridLayout_5.addWidget(self.groupBox_9, 2, 1, 4, 4)

        self.tabWidget.addTab(self.tabWidgetPage2, "")

        self.gridLayout_14.addWidget(self.tabWidget, 2, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.gridLayout_14.addItem(self.verticalSpacer, 3, 0, 1, 1)

        self.stackedWidget.addWidget(self.create_page_empresa)
        self.page = QWidget()
        self.page.setObjectName("page")
        self.tableView = QTableView(self.page)
        self.tableView.setObjectName("tableView")
        self.tableView.setGeometry(QRect(5, 11, 1261, 681))
        self.stackedWidget.addWidget(self.page)

        self.gridLayout_2.addWidget(self.stackedWidget, 1, 0, 1, 1)

        self.label = QLabel(FrmEmpresas)
        self.label.setObjectName("label")
        self.label.setStyleSheet(
            "background-color: #304163;\n"
            'font: 14pt "Sans Serif";\n'
            "color: rgb(255, 255, 255);"
        )
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        QWidget.setTabOrder(self.txtcodigo, self.txtNombreComercial)
        QWidget.setTabOrder(self.txtNombreComercial, self.cboGrupoEmpresa)
        QWidget.setTabOrder(self.cboGrupoEmpresa, self.txtEmpresa)
        QWidget.setTabOrder(self.txtEmpresa, self.cboFormajuridica)
        QWidget.setTabOrder(self.cboFormajuridica, self.cboPais)
        QWidget.setTabOrder(self.cboPais, self.chkTVA)
        QWidget.setTabOrder(self.chkTVA, self.txtdireccion1)
        QWidget.setTabOrder(self.txtdireccion1, self.txtcp)
        QWidget.setTabOrder(self.txtcp, self.txtpoblacion)
        QWidget.setTabOrder(self.txtpoblacion, self.txtprovincia)
        QWidget.setTabOrder(self.txtprovincia, self.txtcif)
        QWidget.setTabOrder(self.txtcif, self.txtSiret)
        QWidget.setTabOrder(self.txtSiret, self.txtAPE)
        QWidget.setTabOrder(self.txtAPE, self.txtNRS)
        QWidget.setTabOrder(self.txtNRS, self.txtCiudadRCS)
        QWidget.setTabOrder(self.txtCiudadRCS, self.txtRM)
        QWidget.setTabOrder(self.txtRM, self.txtcInscripcion)
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
        QWidget.setTabOrder(self.cboSerie, self.txtDecimalesTotales)
        QWidget.setTabOrder(self.txtDecimalesTotales, self.txtDecimalesPrecios)
        QWidget.setTabOrder(self.txtDecimalesPrecios, self.btnAddLogo)
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
        QWidget.setTabOrder(self.lineEdit_10, self.txtGoogleCalendarID)
        QWidget.setTabOrder(self.txtGoogleCalendarID, self.txtOauthToken)
        QWidget.setTabOrder(self.txtOauthToken, self.txtOauthRefreshToken)
        QWidget.setTabOrder(self.txtOauthRefreshToken, self.txtTokenExpirity)
        QWidget.setTabOrder(self.txtTokenExpirity, self.txtdigitos_cuentas)
        QWidget.setTabOrder(self.txtdigitos_cuentas, self.txtcuentaCliente)
        QWidget.setTabOrder(self.txtcuentaCliente, self.txtcuenta_proveedores)
        QWidget.setTabOrder(self.txtcuenta_proveedores, self.txtcuenta_acreedores)
        QWidget.setTabOrder(self.txtcuenta_acreedores, self.txtCuenta_venta_mercaderias)
        QWidget.setTabOrder(
            self.txtCuenta_venta_mercaderias, self.txtCuenta_venta_servicios
        )
        QWidget.setTabOrder(self.txtCuenta_venta_servicios, self.txtIvasoportado1)
        QWidget.setTabOrder(self.txtIvasoportado1, self.txtIvasoportado2)
        QWidget.setTabOrder(self.txtIvasoportado2, self.txtIvasoportado3)
        QWidget.setTabOrder(self.txtIvasoportado3, self.txtIvasoportado4)
        QWidget.setTabOrder(self.txtIvasoportado4, self.ivasoportadore1)
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
        QWidget.setTabOrder(self.btn_migrar, self.txtHostMariaDB)
        QWidget.setTabOrder(self.txtHostMariaDB, self.txtPortMariadb)
        QWidget.setTabOrder(self.txtPortMariadb, self.txtNombreBD_MariaDB)
        QWidget.setTabOrder(self.txtNombreBD_MariaDB, self.txtUsuarioMariaDB)
        QWidget.setTabOrder(self.txtUsuarioMariaDB, self.txtPasswordMariaDB)
        QWidget.setTabOrder(self.txtPasswordMariaDB, self.txtHostPostgreSQL)
        QWidget.setTabOrder(self.txtHostPostgreSQL, self.lineEdit)
        QWidget.setTabOrder(self.lineEdit, self.txtNombreBD_PostgreSQL)
        QWidget.setTabOrder(self.txtNombreBD_PostgreSQL, self.txtUsuarioPostgreSQL)
        QWidget.setTabOrder(self.txtUsuarioPostgreSQL, self.txtPasswordPostgreSQL)
        QWidget.setTabOrder(self.txtPasswordPostgreSQL, self.btn_guardar_nuevo)
        QWidget.setTabOrder(self.btn_guardar_nuevo, self.pushButton)
        QWidget.setTabOrder(self.pushButton, self.btn_salir)
        QWidget.setTabOrder(self.btn_salir, self.chkContabilidad)
        QWidget.setTabOrder(self.chkContabilidad, self.tabWidget_2)
        QWidget.setTabOrder(self.tabWidget_2, self.tableView)
        QWidget.setTabOrder(self.tableView, self.tabWidget)

        self.retranslateUi(FrmEmpresas)
        try:
            self.btn_salir.clicked.connect(FrmEmpresas.accept)
        except Exception:
            try:
                self.btn_salir.clicked.connect(FrmEmpresas.close)
            except Exception:
                pass

        self.stackedWidget.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(FrmEmpresas)

    # setupUi

    def retranslateUi(self, FrmEmpresas):
        FrmEmpresas.setWindowTitle(
            QCoreApplication.translate("FrmEmpresas", "Gesti\u00f3n de empresas", None)
        )
        self.btn_guardar_nuevo.setText(
            QCoreApplication.translate("FrmEmpresas", "Guardar", None)
        )
        self.pushButton.setText(
            QCoreApplication.translate("FrmEmpresas", "Descartar", None)
        )
        self.btn_salir.setText(QCoreApplication.translate("FrmEmpresas", "Salir", None))
        self.label_50.setText(
            QCoreApplication.translate("FrmEmpresas", "Poblaci\u00f3n:", None)
        )
        self.label_34.setText(
            QCoreApplication.translate("FrmEmpresas", "APE/NAF:", None)
        )
        self.label_20.setText(QCoreApplication.translate("FrmEmpresas", "Mail:", None))
        self.label_21.setText(QCoreApplication.translate("FrmEmpresas", "Web:", None))
        self.label_13.setText(
            QCoreApplication.translate("FrmEmpresas", "Direcci\u00f3n:", None)
        )
        self.label_6.setText(QCoreApplication.translate("FrmEmpresas", "Grupo", None))
        self.label_22.setText(QCoreApplication.translate("FrmEmpresas", "Cif:", None))
        self.chkTVA.setText(
            QCoreApplication.translate("FrmEmpresas", "TVA non applicable", None)
        )
        self.label_43.setText(
            QCoreApplication.translate("FrmEmpresas", "Nombre comercial:", None)
        )
        self.label_53.setText(
            QCoreApplication.translate("FrmEmpresas", "N\u00ba RCS:", None)
        )
        self.label_19.setText(QCoreApplication.translate("FrmEmpresas", "Movil:", None))
        self.label_16.setText(QCoreApplication.translate("FrmEmpresas", "Pais:", None))
        self.label_32.setText(QCoreApplication.translate("FrmEmpresas", "SIRET:", None))
        self.label_23.setText(
            QCoreApplication.translate("FrmEmpresas", "Inscripci\u00f3n:", None)
        )
        self.label_54.setText(
            QCoreApplication.translate("FrmEmpresas", "Ciudad RCS:", None)
        )
        self.txttelefono1.setText("")
        self.label_17.setText(
            QCoreApplication.translate("FrmEmpresas", "Tel\u00e9fono 1:", None)
        )
        self.label_14.setText(QCoreApplication.translate("FrmEmpresas", "C.P.:", None))
        self.label_75.setText(
            QCoreApplication.translate("FrmEmpresas", "Nombre Fiscal:", None)
        )
        self.label_74.setText(
            QCoreApplication.translate("FrmEmpresas", "Codigo:", None)
        )
        self.cboFormajuridica.setItemText(
            0,
            QCoreApplication.translate(
                "FrmEmpresas", "EI (Entreprise Individuelle)", None
            ),
        )
        self.cboFormajuridica.setItemText(
            1, QCoreApplication.translate("FrmEmpresas", "EIRL", None)
        )
        self.cboFormajuridica.setItemText(
            2, QCoreApplication.translate("FrmEmpresas", "Micro-entrepreneur", None)
        )
        self.cboFormajuridica.setItemText(
            3, QCoreApplication.translate("FrmEmpresas", "SARL", None)
        )
        self.cboFormajuridica.setItemText(
            4, QCoreApplication.translate("FrmEmpresas", "EURL", None)
        )
        self.cboFormajuridica.setItemText(
            5, QCoreApplication.translate("FrmEmpresas", "SAS", None)
        )
        self.cboFormajuridica.setItemText(
            6, QCoreApplication.translate("FrmEmpresas", "SASU", None)
        )
        self.cboFormajuridica.setItemText(
            7, QCoreApplication.translate("FrmEmpresas", "SA", None)
        )
        self.cboFormajuridica.setItemText(
            8, QCoreApplication.translate("FrmEmpresas", "SCOP / SCIC", None)
        )
        self.cboFormajuridica.setItemText(
            9, QCoreApplication.translate("FrmEmpresas", "SEM", None)
        )
        self.cboFormajuridica.setItemText(
            10, QCoreApplication.translate("FrmEmpresas", "RM", None)
        )

        self.label_57.setText(
            QCoreApplication.translate("FrmEmpresas", "N\u00ba RM:", None)
        )
        self.label_24.setText(
            QCoreApplication.translate("FrmEmpresas", "Forma juridica:", None)
        )
        self.label_15.setText(
            QCoreApplication.translate("FrmEmpresas", "Provincia:", None)
        )
        self.label_18.setText(
            QCoreApplication.translate("FrmEmpresas", "Telefono 2:", None)
        )
        self.txttelefono2.setText("")
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tabWidgetPage1),
            QCoreApplication.translate(
                "FrmEmpresas", "Datos Fiscales y de Gesti\u00f3n", None
            ),
        )
        self.groupBox_14.setTitle(
            QCoreApplication.translate("FrmEmpresas", "Divisas", None)
        )
        self.chk_upate_divisas.setText(
            QCoreApplication.translate(
                "FrmEmpresas", "Actualizar divisas al entrar", None
            )
        )
        self.label_42.setText(
            QCoreApplication.translate("FrmEmpresas", "Divisa: ", None)
        )
        self.groupBox_4.setTitle(
            QCoreApplication.translate("FrmEmpresas", "IRPF", None)
        )
        self.chkIRPF.setText(
            QCoreApplication.translate("FrmEmpresas", "Autonomo / IRPF", None)
        )
        self.label_71.setText(QCoreApplication.translate("FrmEmpresas", "%IRPF:", None))
        self.groupBox_12.setTitle(
            QCoreApplication.translate("FrmEmpresas", "Decimales", None)
        )
        self.label_222.setText(
            QCoreApplication.translate("FrmEmpresas", "Decimales en totales", None)
        )
        self.label_85.setText(
            QCoreApplication.translate("FrmEmpresas", "Decimales precios:", None)
        )
        self.groupBox_3.setTitle(
            QCoreApplication.translate("FrmEmpresas", "Facturas", None)
        )
        self.label_25.setText(
            QCoreApplication.translate("FrmEmpresas", "Digitos Factura:", None)
        )
        self.label_26.setText(
            QCoreApplication.translate("FrmEmpresas", "Serie Factura:", None)
        )
        self.label_68.setText(
            QCoreApplication.translate("FrmEmpresas", "Cierre ejercicio fiscal:", None)
        )
        self.groupBox_5.setTitle(
            QCoreApplication.translate("FrmEmpresas", "Varios", None)
        )
        self.chkEnlace_web.setText(
            QCoreApplication.translate("FrmEmpresas", "Enlace Web.", None)
        )
        self.chkInternacional.setText(
            QCoreApplication.translate(
                "FrmEmpresas", "Gesti\u00f3n Internacional", None
            )
        )
        self.groupBox_2.setTitle(
            QCoreApplication.translate("FrmEmpresas", "Articulos", None)
        )
        self.chkAutocodificiar.setText(
            QCoreApplication.translate(
                "FrmEmpresas", "Auto codificar los nuevos art\u00edculos", None
            )
        )
        self.label_41.setText(
            QCoreApplication.translate(
                "FrmEmpresas", "Tama\u00f1o del c\u00f3digo en caracteres:", None
            )
        )
        self.groupBox.setTitle(
            QCoreApplication.translate("FrmEmpresas", "Tarifas", None)
        )
        self.label_33.setText(
            QCoreApplication.translate("FrmEmpresas", "Margen M\u00ednimo:", None)
        )
        self.label_31.setText(
            QCoreApplication.translate("FrmEmpresas", "Margen:", None)
        )
        self.label_58.setText(
            QCoreApplication.translate("FrmEmpresas", "Tarifa predeterminada:", None)
        )
        self.btnDeleteLogo.setText(
            QCoreApplication.translate("FrmEmpresas", "Borrar", None)
        )
        self.btnAddLogo.setText(
            QCoreApplication.translate("FrmEmpresas", "Cambiar", None)
        )
        self.groupBox_6.setTitle(
            QCoreApplication.translate("FrmEmpresas", "Logotipo", None)
        )
        self.imgLogo.setText("")
        self.tabWidget_2.setTabText(
            self.tabWidget_2.indexOf(self.tab_12),
            QCoreApplication.translate("FrmEmpresas", "Otros", None),
        )
        self.label_36.setText(
            QCoreApplication.translate("FrmEmpresas", "Comentarios en Albaranes", None)
        )
        self.label_35.setText(
            QCoreApplication.translate("FrmEmpresas", "Comentarios en Facturas:", None)
        )
        self.tabWidget_2.setTabText(
            self.tabWidget_2.indexOf(self.tab_6),
            QCoreApplication.translate("FrmEmpresas", "Comentarios", None),
        )
        self.label_47.setText(
            QCoreApplication.translate("FrmEmpresas", "Horario Martes:", None)
        )
        self.label_46.setText(
            QCoreApplication.translate("FrmEmpresas", "Horario Lunes:", None)
        )
        self.label_45.setText(
            QCoreApplication.translate("FrmEmpresas", "Horario Viernes:", None)
        )
        self.label_70.setText(
            QCoreApplication.translate("FrmEmpresas", "Horario Domingo:", None)
        )
        self.label_44.setText(
            QCoreApplication.translate("FrmEmpresas", "Horario Jueves:", None)
        )
        self.label_69.setText(
            QCoreApplication.translate("FrmEmpresas", "Horario Sabado:", None)
        )
        self.label_48.setText(
            QCoreApplication.translate("FrmEmpresas", "Horario Miercoles:", None)
        )
        self.groupBox_7.setTitle(
            QCoreApplication.translate("FrmEmpresas", "Acceso a Google Calendar", None)
        )
        self.label_72.setText(
            QCoreApplication.translate("FrmEmpresas", "Google Calendar ID:", None)
        )
        self.label_73.setText(
            QCoreApplication.translate("FrmEmpresas", "oauth Acces Token:", None)
        )
        self.label_76.setText(
            QCoreApplication.translate("FrmEmpresas", "oauth Refresh Token:", None)
        )
        self.label_77.setText(
            QCoreApplication.translate("FrmEmpresas", " Token Expirity:", None)
        )
        self.tabWidget_2.setTabText(
            self.tabWidget_2.indexOf(self.tab_8),
            QCoreApplication.translate("FrmEmpresas", "Agenda", None),
        )
        self.chkContabilidad.setText(
            QCoreApplication.translate("FrmEmpresas", "Activar contabilidad", None)
        )
        self.txtCuenta_venta_servicios.setText(
            QCoreApplication.translate("FrmEmpresas", "610", None)
        )
        self.txtCuenta_venta_servicios.setPlaceholderText(
            QCoreApplication.translate("FrmEmpresas", "(F1 - lista)", None)
        )
        self.txtCuenta_venta_mercaderias.setText(
            QCoreApplication.translate("FrmEmpresas", "600", None)
        )
        self.txtCuenta_venta_mercaderias.setPlaceholderText(
            QCoreApplication.translate("FrmEmpresas", "(F1 - lista)", None)
        )
        self.txtcuenta_acreedores.setText(
            QCoreApplication.translate("FrmEmpresas", "410", None)
        )
        self.txtcuenta_acreedores.setPlaceholderText(
            QCoreApplication.translate("FrmEmpresas", "(F1 - lista)", None)
        )
        self.label_29.setText(
            QCoreApplication.translate("FrmEmpresas", "Acreedores:", None)
        )
        self.label_12.setText(
            QCoreApplication.translate(
                "FrmEmpresas", "Cuenta de venta de mercader\u00edas:", None
            )
        )
        self.label_37.setText(
            QCoreApplication.translate(
                "FrmEmpresas", "Cuenta de venta (prestaci\u00f3n de servicios):", None
            )
        )
        self.label_28.setText(
            QCoreApplication.translate("FrmEmpresas", "Proveedores:", None)
        )
        self.txtcuenta_proveedores.setText(
            QCoreApplication.translate("FrmEmpresas", "400", None)
        )
        self.txtcuenta_proveedores.setPlaceholderText(
            QCoreApplication.translate("FrmEmpresas", "(F1 - lista)", None)
        )
        self.txtcuentaCliente.setText(
            QCoreApplication.translate("FrmEmpresas", "430", None)
        )
        self.txtcuentaCliente.setPlaceholderText(
            QCoreApplication.translate("FrmEmpresas", "(F1 - lista)", None)
        )
        self.label_30.setText(
            QCoreApplication.translate(
                "FrmEmpresas", "Digitos cuentas contables:", None
            )
        )
        self.label_27.setText(
            QCoreApplication.translate("FrmEmpresas", "Cientes:", None)
        )
        self.ivarepercutidore1.setPlaceholderText(
            QCoreApplication.translate("FrmEmpresas", "(F1 - lista)", None)
        )
        self.ivarepercutido3.setPlaceholderText(
            QCoreApplication.translate("FrmEmpresas", "(F1 - lista)", None)
        )
        self.label_65.setText(QCoreApplication.translate("FrmEmpresas", "E", None))
        self.txtIvasoportado4.setPlaceholderText(
            QCoreApplication.translate("FrmEmpresas", "(F1 - lista)", None)
        )
        self.label_59.setText(QCoreApplication.translate("FrmEmpresas", "R", None))
        self.txtIvasoportado2.setPlaceholderText(
            QCoreApplication.translate("FrmEmpresas", "(F1 - lista)", None)
        )
        self.label_63.setText(QCoreApplication.translate("FrmEmpresas", "R", None))
        self.label_38.setText(
            QCoreApplication.translate("FrmEmpresas", "Cuenta IVA soportado", None)
        )
        self.ivasoportadore4.setPlaceholderText(
            QCoreApplication.translate("FrmEmpresas", "(F1 - lista)", None)
        )
        self.ivasoportadore3.setPlaceholderText(
            QCoreApplication.translate("FrmEmpresas", "(F1 - lista)", None)
        )
        self.label_39.setText(
            QCoreApplication.translate("FrmEmpresas", "Cuenta IVA repercutido", None)
        )
        self.label_40.setText(QCoreApplication.translate("FrmEmpresas", "N", None))
        self.label_62.setText(QCoreApplication.translate("FrmEmpresas", "N", None))
        self.txtIvasoportado1.setPlaceholderText(
            QCoreApplication.translate("FrmEmpresas", "(F1 - lista)", None)
        )
        self.ivarepercutido1.setPlaceholderText(
            QCoreApplication.translate("FrmEmpresas", "(F1 - lista)", None)
        )
        self.ivarepercutido4.setPlaceholderText(
            QCoreApplication.translate("FrmEmpresas", "(F1 - lista)", None)
        )
        self.ivarepercutido2.setPlaceholderText(
            QCoreApplication.translate("FrmEmpresas", "(F1 - lista)", None)
        )
        self.label_60.setText(QCoreApplication.translate("FrmEmpresas", "SR", None))
        self.txtIvasoportado3.setPlaceholderText(
            QCoreApplication.translate("FrmEmpresas", "(F1 - lista)", None)
        )
        self.label_64.setText(QCoreApplication.translate("FrmEmpresas", "SR", None))
        self.label_61.setText(QCoreApplication.translate("FrmEmpresas", "E", None))
        self.ivasoportadore1.setPlaceholderText(
            QCoreApplication.translate("FrmEmpresas", "(F1 - lista)", None)
        )
        self.ivasoportadore2.setPlaceholderText(
            QCoreApplication.translate("FrmEmpresas", "(F1 - lista)", None)
        )
        self.label_66.setText(
            QCoreApplication.translate("FrmEmpresas", "IVA soportado RE", None)
        )
        self.label_67.setText(
            QCoreApplication.translate("FrmEmpresas", "IVA repercutido RE", None)
        )
        self.ivarepercutidore3.setPlaceholderText(
            QCoreApplication.translate("FrmEmpresas", "(F1 - lista)", None)
        )
        self.ivarepercutidore2.setPlaceholderText(
            QCoreApplication.translate("FrmEmpresas", "(F1 - lista)", None)
        )
        self.ivarepercutidore4.setPlaceholderText(
            QCoreApplication.translate("FrmEmpresas", "(F1 - lista)", None)
        )
        self.label_9.setText(
            QCoreApplication.translate("FrmEmpresas", "Cuenta cobros:", None)
        )
        self.txtcuenta_cobros.setPlaceholderText(
            QCoreApplication.translate("FrmEmpresas", "(F1 - lista)", None)
        )
        self.label_10.setText(
            QCoreApplication.translate("FrmEmpresas", "Cuenta Pagos:", None)
        )
        self.txtcuenta_pagos.setPlaceholderText(
            QCoreApplication.translate("FrmEmpresas", "(F1 - lista)", None)
        )
        self.tabWidget_2.setTabText(
            self.tabWidget_2.indexOf(self.tab_5),
            QCoreApplication.translate("FrmEmpresas", "Contabilidad", None),
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab),
            QCoreApplication.translate("FrmEmpresas", "Otros datos", None),
        )
        self.label_2.setText(
            QCoreApplication.translate(
                "FrmEmpresas", "Motor Activo de Base de Datos", None
            )
        )
        self.groupBox_8.setTitle(
            QCoreApplication.translate(
                "FrmEmpresas",
                "Datos Acceso MariaDB / MySQL ( Recomendado para empresas entre 2 y 10 ordenadores)",
                None,
            )
        )
        self.label_82.setText(
            QCoreApplication.translate("FrmEmpresas", "Nombre Base de Datos:", None)
        )
        self.label_87.setText(
            QCoreApplication.translate("FrmEmpresas", "Usuario:", None)
        )
        self.label_86.setText(QCoreApplication.translate("FrmEmpresas", "Host:", None))
        self.label_84.setText(
            QCoreApplication.translate("FrmEmpresas", "Puerto:", None)
        )
        self.label_83.setText(
            QCoreApplication.translate("FrmEmpresas", "Password:", None)
        )
        self.btnTestBDMariaDB.setText(
            QCoreApplication.translate("FrmEmpresas", "Test Database conexion", None)
        )
        self.btnCrearDBMariaDb.setText(
            QCoreApplication.translate("FrmEmpresas", "Crear DB", None)
        )
        self.comboBox.setItemText(
            0, QCoreApplication.translate("FrmEmpresas", "SQLite", None)
        )
        self.comboBox.setItemText(
            1, QCoreApplication.translate("FrmEmpresas", "MariaDB", None)
        )
        self.comboBox.setItemText(
            2, QCoreApplication.translate("FrmEmpresas", "PostgreSQL", None)
        )
        self.comboBox.setItemText(
            3, QCoreApplication.translate("FrmEmpresas", "MySQL", None)
        )

        self.label_55.setText(
            QCoreApplication.translate("FrmEmpresas", "Ruta BD: Contabilidad:", None)
        )
        self.btnSeleccionarBDSQLiteConta.setText(
            QCoreApplication.translate("FrmEmpresas", "...", None)
        )
        self.btn_migrar.setText(
            QCoreApplication.translate("FrmEmpresas", "Migrar a BD Multipuesto", None)
        )
        self.btnSelecionarBDSQLite.setText(
            QCoreApplication.translate("FrmEmpresas", "...", None)
        )
        self.label_3.setText(
            QCoreApplication.translate("FrmEmpresas", "Ruta SQLite Empresa", None)
        )
        self.label_4.setText(
            QCoreApplication.translate(
                "FrmEmpresas",
                '<html><head/><body><p><span style=" font-weight:700; color:#ffffff;">Acceso a SQLite (Para empresas con un solo ordenador)</span></p><p><span style=" font-weight:700; color:#ffffff;"><br/></span></p></body></html>',
                None,
            )
        )
        self.groupBox_9.setTitle(
            QCoreApplication.translate(
                "FrmEmpresas",
                "Datos Acceso Postgre SQL(Recomendado para empresas con m\u00e1s de 10 ordenadores)",
                None,
            )
        )
        self.label_79.setText(
            QCoreApplication.translate("FrmEmpresas", "Nombre Base de Datos:", None)
        )
        self.label_78.setText(
            QCoreApplication.translate("FrmEmpresas", "Puerto:", None)
        )
        self.label_81.setText(
            QCoreApplication.translate("FrmEmpresas", "Password:", None)
        )
        self.label_56.setText(QCoreApplication.translate("FrmEmpresas", "Host:", None))
        self.label_80.setText(
            QCoreApplication.translate("FrmEmpresas", "Usuario:", None)
        )
        self.btnCrearDBPostgreSQL.setText(
            QCoreApplication.translate("FrmEmpresas", "Crear BD", None)
        )
        self.btnTestDBPostgreSQL.setText(
            QCoreApplication.translate("FrmEmpresas", "Test Database conexion", None)
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tabWidgetPage2),
            QCoreApplication.translate(
                "FrmEmpresas", "Datos conexi\u00f3n Base de datos", None
            ),
        )
        self.label.setText(
            QCoreApplication.translate("FrmEmpresas", "Gesti\u00f3n de Empresas", None)
        )

    # retranslateUi
