# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frmnuevosavisos.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QDate, QDateTime, QMetaObject, QSize, QTime
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QFrame,
    QGridLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QTextEdit,
    QTimeEdit,
)

try:
    # Prefer packaged resource module under modules/ when present (compile_ui.sh writes this form)
    pass
except Exception:
    # Fallback to plain import if modules.designer_rc doesn't exist
    pass


class Ui_frmNuevosAvisos(object):
    def setupUi(self, frmNuevosAvisos):
        if not frmNuevosAvisos.objectName():
            frmNuevosAvisos.setObjectName("frmNuevosAvisos")
        frmNuevosAvisos.resize(456, 357)
        self.gridLayout_2 = QGridLayout(frmNuevosAvisos)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.btnAceptar = QPushButton(frmNuevosAvisos)
        self.btnAceptar.setObjectName("btnAceptar")
        icon = QIcon()
        icon.addFile(":/Icons/PNG/OK.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnAceptar.setIcon(icon)

        self.gridLayout_2.addWidget(self.btnAceptar, 1, 1, 1, 1)

        self.btnCancelar = QPushButton(frmNuevosAvisos)
        self.btnCancelar.setObjectName("btnCancelar")
        icon1 = QIcon()
        icon1.addFile(
            ":/Icons/PNG/close.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.btnCancelar.setIcon(icon1)

        self.gridLayout_2.addWidget(self.btnCancelar, 1, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.gridLayout_2.addItem(self.horizontalSpacer, 1, 0, 1, 1)

        self.frame = QFrame(frmNuevosAvisos)
        self.frame.setObjectName("frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName("label_2")

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.txtFecha = QDateEdit(self.frame)
        self.txtFecha.setObjectName("txtFecha")
        self.txtFecha.setStyleSheet(
            "color: rgb(0, 0, 0);\n" "background-color: rgb(239, 239, 239);"
        )
        self.txtFecha.setDateTime(QDateTime(QDate(2026, 1, 1), QTime(0, 0, 0)))

        self.gridLayout.addWidget(self.txtFecha, 2, 1, 1, 1)

        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName("label_3")

        self.gridLayout.addWidget(self.label_3, 2, 2, 1, 1)

        self.txtHora = QTimeEdit(self.frame)
        self.txtHora.setObjectName("txtHora")

        self.gridLayout.addWidget(self.txtHora, 2, 3, 1, 1)

        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName("label_4")

        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)

        self.txtAviso = QTextEdit(self.frame)
        self.txtAviso.setObjectName("txtAviso")

        self.gridLayout.addWidget(self.txtAviso, 3, 1, 1, 3)

        self.label_5 = QLabel(self.frame)
        self.label_5.setObjectName("label_5")

        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)

        self.cboEmpresa = QComboBox(self.frame)
        self.cboEmpresa.setObjectName("cboEmpresa")

        self.gridLayout.addWidget(self.cboEmpresa, 4, 1, 1, 3)

        self.label = QLabel(self.frame)
        self.label.setObjectName("label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.cboUsuarios = QComboBox(self.frame)
        self.cboUsuarios.setObjectName("cboUsuarios")

        self.gridLayout.addWidget(self.cboUsuarios, 1, 1, 1, 3)

        self.label_6 = QLabel(self.frame)
        self.label_6.setObjectName("label_6")

        self.gridLayout.addWidget(self.label_6, 0, 0, 1, 1)

        self.cboTipoAviso = QComboBox(self.frame)
        self.cboTipoAviso.setObjectName("cboTipoAviso")

        self.gridLayout.addWidget(self.cboTipoAviso, 0, 1, 1, 3)

        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 3)

        self.retranslateUi(frmNuevosAvisos)
        try:
            self.btnAceptar.clicked.connect(frmNuevosAvisos.accept)
        except Exception:
            try:
                self.btnAceptar.clicked.connect(frmNuevosAvisos.close)
            except Exception:
                pass
        self.btnCancelar.clicked.connect(frmNuevosAvisos.close)

        QMetaObject.connectSlotsByName(frmNuevosAvisos)

    # setupUi

    def retranslateUi(self, frmNuevosAvisos):
        frmNuevosAvisos.setWindowTitle(
            QCoreApplication.translate("frmNuevosAvisos", "Dialog", None)
        )
        self.btnAceptar.setText(
            QCoreApplication.translate("frmNuevosAvisos", "Aceptar", None)
        )
        self.btnCancelar.setText(
            QCoreApplication.translate("frmNuevosAvisos", "Cancelar", None)
        )
        self.label_2.setText(
            QCoreApplication.translate("frmNuevosAvisos", "Fecha:", None)
        )
        self.label_3.setText(
            QCoreApplication.translate("frmNuevosAvisos", "Hora:", None)
        )
        self.label_4.setText(
            QCoreApplication.translate("frmNuevosAvisos", "Aviso:", None)
        )
        self.label_5.setText(
            QCoreApplication.translate("frmNuevosAvisos", "Empresa:", None)
        )
        self.label.setText(
            QCoreApplication.translate("frmNuevosAvisos", "Avisar a:", None)
        )
        self.label_6.setText(
            QCoreApplication.translate("frmNuevosAvisos", "Tipo de aviso:", None)
        )

    # retranslateUi
