# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frmeditaravisos.ui'
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
from PySide6.QtWidgets import (QApplication, QDateTimeEdit, QDialog, QFrame,
    QGridLayout, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QTextEdit, QWidget)
from modules import designer_rc

class Ui_FrmEditarAvisos(object):
    def setupUi(self, FrmEditarAvisos):
        if not FrmEditarAvisos.objectName():
            FrmEditarAvisos.setObjectName(u"FrmEditarAvisos")
        FrmEditarAvisos.resize(478, 304)
        self.gridLayout = QGridLayout(FrmEditarAvisos)
        self.gridLayout.setObjectName(u"gridLayout")
        self.btnCancelar = QPushButton(FrmEditarAvisos)
        self.btnCancelar.setObjectName(u"btnCancelar")
        icon = QIcon()
        icon.addFile(u":/Icons/PNG/close.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnCancelar.setIcon(icon)

        self.gridLayout.addWidget(self.btnCancelar, 2, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(282, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 2, 0, 1, 1)

        self.btnAceptar = QPushButton(FrmEditarAvisos)
        self.btnAceptar.setObjectName(u"btnAceptar")
        icon1 = QIcon()
        icon1.addFile(u":/Icons/PNG/OK.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnAceptar.setIcon(icon1)

        self.gridLayout.addWidget(self.btnAceptar, 2, 2, 1, 1)

        self.frame = QFrame(FrmEditarAvisos)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setStyleSheet(u"font: 75 10pt \"Cantarell\";")

        self.gridLayout_2.addWidget(self.label_3, 2, 2, 1, 1)

        self.label_6 = QLabel(self.frame)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_2.addWidget(self.label_6, 4, 3, 1, 1)

        self.dtFechaHora = QDateTimeEdit(self.frame)
        self.dtFechaHora.setObjectName(u"dtFechaHora")
        self.dtFechaHora.setDateTime(QDateTime(QDate(2026, 1, 1), QTime(0, 0, 0)))

        self.gridLayout_2.addWidget(self.dtFechaHora, 1, 3, 1, 2)

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 1, 2, 1, 1)

        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.spinDias = QSpinBox(self.frame)
        self.spinDias.setObjectName(u"spinDias")
        self.spinDias.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.spinDias, 2, 4, 1, 1)

        self.label_5 = QLabel(self.frame)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_2.addWidget(self.label_5, 3, 3, 1, 1)

        self.spinHoras = QSpinBox(self.frame)
        self.spinHoras.setObjectName(u"spinHoras")
        self.spinHoras.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.spinHoras, 3, 4, 1, 1)

        self.txtAviso = QTextEdit(self.frame)
        self.txtAviso.setObjectName(u"txtAviso")

        self.gridLayout_2.addWidget(self.txtAviso, 0, 1, 1, 4)

        self.spinMinutos = QSpinBox(self.frame)
        self.spinMinutos.setObjectName(u"spinMinutos")
        self.spinMinutos.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.spinMinutos, 4, 4, 1, 1)

        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_2.addWidget(self.label_4, 2, 3, 1, 1)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 3)

        self.btnCerrar = QPushButton(FrmEditarAvisos)
        self.btnCerrar.setObjectName(u"btnCerrar")
        icon2 = QIcon()
        icon2.addFile(u":/Icons/PNG/blue.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnCerrar.setIcon(icon2)

        self.gridLayout.addWidget(self.btnCerrar, 1, 0, 1, 3)


        self.retranslateUi(FrmEditarAvisos)
        self.btnCancelar.clicked.connect(FrmEditarAvisos.close)

        QMetaObject.connectSlotsByName(FrmEditarAvisos)
    # setupUi

    def retranslateUi(self, FrmEditarAvisos):
        FrmEditarAvisos.setWindowTitle(QCoreApplication.translate("FrmEditarAvisos", u"Dialog", None))
        self.btnCancelar.setText(QCoreApplication.translate("FrmEditarAvisos", u"Cancelar", None))
        self.btnAceptar.setText(QCoreApplication.translate("FrmEditarAvisos", u"Aceptar", None))
        self.label_3.setText(QCoreApplication.translate("FrmEditarAvisos", u"Postergar:", None))
        self.label_6.setText(QCoreApplication.translate("FrmEditarAvisos", u"minutos:", None))
        self.label_2.setText(QCoreApplication.translate("FrmEditarAvisos", u"Fecha/hora:", None))
        self.label.setText(QCoreApplication.translate("FrmEditarAvisos", u"Aviso:", None))
        self.label_5.setText(QCoreApplication.translate("FrmEditarAvisos", u"horas:", None))
        self.label_4.setText(QCoreApplication.translate("FrmEditarAvisos", u"dias:", None))
        self.btnCerrar.setText(QCoreApplication.translate("FrmEditarAvisos", u"Dar aviso por cerrado/Recibido.", None))
    # retranslateUi

