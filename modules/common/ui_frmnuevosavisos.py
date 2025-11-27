# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frmnuevosavisos.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDateEdit, QDialog,
    QFrame, QGridLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QTextEdit, QTimeEdit,
    QWidget)
from modules import designer_rc

class Ui_frmNuevosAvisos(object):
    def setupUi(self, frmNuevosAvisos):
        if not frmNuevosAvisos.objectName():
            frmNuevosAvisos.setObjectName(u"frmNuevosAvisos")
        frmNuevosAvisos.resize(456, 357)
        self.gridLayout_2 = QGridLayout(frmNuevosAvisos)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.btnAceptar = QPushButton(frmNuevosAvisos)
        self.btnAceptar.setObjectName(u"btnAceptar")
        icon = QIcon()
        icon.addFile(u":/Icons/PNG/OK.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnAceptar.setIcon(icon)

        self.gridLayout_2.addWidget(self.btnAceptar, 1, 1, 1, 1)

        self.btnCancelar = QPushButton(frmNuevosAvisos)
        self.btnCancelar.setObjectName(u"btnCancelar")
        icon1 = QIcon()
        icon1.addFile(u":/Icons/PNG/close.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnCancelar.setIcon(icon1)

        self.gridLayout_2.addWidget(self.btnCancelar, 1, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 1, 0, 1, 1)

        self.frame = QFrame(frmNuevosAvisos)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.txtFecha = QDateEdit(self.frame)
        self.txtFecha.setObjectName(u"txtFecha")
        self.txtFecha.setDateTime(QDateTime(QDate(2026, 1, 1), QTime(0, 0, 0)))

        self.gridLayout.addWidget(self.txtFecha, 2, 1, 1, 1)

        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 2, 1, 1)

        self.txtHora = QTimeEdit(self.frame)
        self.txtHora.setObjectName(u"txtHora")

        self.gridLayout.addWidget(self.txtHora, 2, 3, 1, 1)

        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)

        self.txtAviso = QTextEdit(self.frame)
        self.txtAviso.setObjectName(u"txtAviso")

        self.gridLayout.addWidget(self.txtAviso, 3, 1, 1, 3)

        self.label_5 = QLabel(self.frame)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)

        self.cboEmpresa = QComboBox(self.frame)
        self.cboEmpresa.setObjectName(u"cboEmpresa")

        self.gridLayout.addWidget(self.cboEmpresa, 4, 1, 1, 3)

        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.cboUsuarios = QComboBox(self.frame)
        self.cboUsuarios.setObjectName(u"cboUsuarios")

        self.gridLayout.addWidget(self.cboUsuarios, 1, 1, 1, 3)

        self.label_6 = QLabel(self.frame)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 0, 0, 1, 1)

        self.cboTipoAviso = QComboBox(self.frame)
        self.cboTipoAviso.setObjectName(u"cboTipoAviso")

        self.gridLayout.addWidget(self.cboTipoAviso, 0, 1, 1, 3)


        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 3)


        self.retranslateUi(frmNuevosAvisos)
        self.btnAceptar.clicked.connect(frmNuevosAvisos.accept)
        self.btnCancelar.clicked.connect(frmNuevosAvisos.close)

        QMetaObject.connectSlotsByName(frmNuevosAvisos)
    # setupUi

    def retranslateUi(self, frmNuevosAvisos):
        frmNuevosAvisos.setWindowTitle(QCoreApplication.translate("frmNuevosAvisos", u"Dialog", None))
        self.btnAceptar.setText(QCoreApplication.translate("frmNuevosAvisos", u"Aceptar", None))
        self.btnCancelar.setText(QCoreApplication.translate("frmNuevosAvisos", u"Cancelar", None))
        self.label_2.setText(QCoreApplication.translate("frmNuevosAvisos", u"Fecha:", None))
        self.label_3.setText(QCoreApplication.translate("frmNuevosAvisos", u"Hora:", None))
        self.label_4.setText(QCoreApplication.translate("frmNuevosAvisos", u"Aviso:", None))
        self.label_5.setText(QCoreApplication.translate("frmNuevosAvisos", u"Empresa:", None))
        self.label.setText(QCoreApplication.translate("frmNuevosAvisos", u"Avisar a:", None))
        self.label_6.setText(QCoreApplication.translate("frmNuevosAvisos", u"Tipo de aviso:", None))
    # retranslateUi

