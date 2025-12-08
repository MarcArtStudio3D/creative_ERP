# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frmConfig.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject, QRect, Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDialogButtonBox,
    QGroupBox,
    QLabel,
    QPushButton,
    QSpinBox,
)


class Ui_frmConfig(object):
    def setupUi(self, frmConfig):
        if not frmConfig.objectName():
            frmConfig.setObjectName("frmConfig")
        frmConfig.resize(804, 474)
        self.buttonBox = QDialogButtonBox(frmConfig)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.setGeometry(QRect(450, 430, 341, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok
        )
        self.groupBox = QGroupBox(frmConfig)
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setGeometry(QRect(20, 20, 271, 111))
        self.cboIdioma = QComboBox(self.groupBox)
        self.cboIdioma.addItem("")
        self.cboIdioma.addItem("")
        self.cboIdioma.addItem("")
        self.cboIdioma.addItem("")
        self.cboIdioma.setObjectName("cboIdioma")
        self.cboIdioma.setGeometry(QRect(10, 40, 241, 32))
        self.groupBox_2 = QGroupBox(frmConfig)
        self.groupBox_2.setObjectName("groupBox_2")
        self.groupBox_2.setGeometry(QRect(300, 20, 241, 111))
        self.cboValoresFiscales = QComboBox(self.groupBox_2)
        self.cboValoresFiscales.addItem("")
        self.cboValoresFiscales.addItem("")
        self.cboValoresFiscales.setObjectName("cboValoresFiscales")
        self.cboValoresFiscales.setGeometry(QRect(20, 40, 201, 32))
        self.groupBox_3 = QGroupBox(frmConfig)
        self.groupBox_3.setObjectName("groupBox_3")
        self.groupBox_3.setGeometry(QRect(20, 150, 521, 161))
        self.label = QLabel(self.groupBox_3)
        self.label.setObjectName("label")
        self.label.setGeometry(QRect(10, 30, 491, 31))
        self.label.setWordWrap(True)
        self.spinMaxModulos = QSpinBox(self.groupBox_3)
        self.spinMaxModulos.setObjectName("spinMaxModulos")
        self.spinMaxModulos.setGeometry(QRect(10, 65, 101, 32))
        self.spinMaxModulos.setMinimum(1)
        self.spinMaxModulos.setMaximum(20)
        self.spinMaxModulos.setValue(5)
        self.label_2 = QLabel(self.groupBox_3)
        self.label_2.setObjectName("label_2")
        self.label_2.setGeometry(QRect(120, 65, 381, 31))
        self.btnLimpiarCache = QPushButton(self.groupBox_3)
        self.btnLimpiarCache.setObjectName("btnLimpiarCache")
        self.btnLimpiarCache.setGeometry(QRect(10, 110, 241, 35))
        self.label_3 = QLabel(self.groupBox_3)
        self.label_3.setObjectName("label_3")
        self.label_3.setGeometry(QRect(260, 110, 251, 31))

        self.retranslateUi(frmConfig)
        try:
            self.buttonBox.accepted.connect(frmConfig.accept)
        except Exception:
            try:
                self.buttonBox.accepted.connect(frmConfig.close)
            except Exception:
                pass
        self.buttonBox.rejected.connect(frmConfig.reject)

        QMetaObject.connectSlotsByName(frmConfig)

    # setupUi

    def retranslateUi(self, frmConfig):
        frmConfig.setWindowTitle(
            QCoreApplication.translate(
                "frmConfig", "Configuraci\u00f3n de Creative ERP", None
            )
        )
        self.groupBox.setTitle(QCoreApplication.translate("frmConfig", "Idioma", None))
        self.cboIdioma.setItemText(
            0, QCoreApplication.translate("frmConfig", "Espa\u00f1ol", None)
        )
        self.cboIdioma.setItemText(
            1, QCoreApplication.translate("frmConfig", "Fran\u00e7aise", None)
        )
        self.cboIdioma.setItemText(
            2, QCoreApplication.translate("frmConfig", "Catal\u00e0", None)
        )
        self.cboIdioma.setItemText(
            3, QCoreApplication.translate("frmConfig", "English", None)
        )

        self.groupBox_2.setTitle(
            QCoreApplication.translate("frmConfig", "Normativa Pais", None)
        )
        self.cboValoresFiscales.setItemText(
            0, QCoreApplication.translate("frmConfig", "Francia", None)
        )
        self.cboValoresFiscales.setItemText(
            1, QCoreApplication.translate("frmConfig", "Espa\u00f1a", None)
        )

        self.groupBox_3.setTitle(
            QCoreApplication.translate(
                "frmConfig",
                "Gesti\u00f3n de Memoria (Cach\u00e9 de M\u00f3dulos)",
                None,
            )
        )
        self.label.setText(
            QCoreApplication.translate(
                "frmConfig",
                "N\u00famero m\u00e1ximo de m\u00f3dulos a mantener en memoria simult\u00e1neamente:",
                None,
            )
        )
        self.label_2.setText(
            QCoreApplication.translate(
                "frmConfig", "m\u00f3dulos (Recomendado: 3-8)", None
            )
        )
        self.btnLimpiarCache.setText(
            QCoreApplication.translate("frmConfig", "Limpiar Cach\u00e9 Ahora", None)
        )
        self.label_3.setText(
            QCoreApplication.translate(
                "frmConfig", "(Libera memoria de m\u00f3dulos no activos)", None
            )
        )

    # retranslateUi
