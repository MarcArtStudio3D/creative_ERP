# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'db_consulta_view.ui'
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
    QFrame, QGridLayout, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QTableView, QWidget)
from . import maya_rc

class Ui_db_consulta_view(object):
    def setupUi(self, db_consulta_view):
        if not db_consulta_view.objectName():
            db_consulta_view.setObjectName(u"db_consulta_view")
        db_consulta_view.setWindowModality(Qt.WindowModal)
        db_consulta_view.resize(1214, 567)
        db_consulta_view.setModal(False)
        self.gridLayout_2 = QGridLayout(db_consulta_view)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.lbltabla = QLabel(db_consulta_view)
        self.lbltabla.setObjectName(u"lbltabla")
        self.lbltabla.setMaximumSize(QSize(16777215, 22))
        self.lbltabla.setStyleSheet(u"background-color: rgb(0, 0, 57);\n"
"font: 14pt \"Sans Serif\";\n"
"color: rgb(255,255,255);")
        self.lbltabla.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.lbltabla, 0, 0, 1, 1)

        self.frame = QFrame(db_consulta_view)
        self.frame.setObjectName(u"frame")
        self.frame.setMaximumSize(QSize(250, 16777215))
        self.frame.setStyleSheet(u"background-color: rgb(170, 170, 127);")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(128, 128))
        self.label_2.setPixmap(QPixmap(u":/Icons/PNG/find2.png"))

        self.gridLayout.addWidget(self.label_2, 1, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 259, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 5, 1, 1, 1)

        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.lineaTextoBuscar = QLineEdit(self.frame)
        self.lineaTextoBuscar.setObjectName(u"lineaTextoBuscar")
        self.lineaTextoBuscar.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")

        self.gridLayout.addWidget(self.lineaTextoBuscar, 4, 1, 1, 1)

        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 4, 0, 1, 1)

        self.cboCampoBusqueda = QComboBox(self.frame)
        self.cboCampoBusqueda.setObjectName(u"cboCampoBusqueda")

        self.gridLayout.addWidget(self.cboCampoBusqueda, 2, 1, 1, 1)

        self.cboSentido = QComboBox(self.frame)
        self.cboSentido.setObjectName(u"cboSentido")

        self.gridLayout.addWidget(self.cboSentido, 3, 1, 1, 1)

        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame, 0, 1, 2, 1)

        self.resultado_list = QTableView(db_consulta_view)
        self.resultado_list.setObjectName(u"resultado_list")
        self.resultado_list.setStyleSheet(u"alternate-background-color: rgb(255, 255, 255);\n"
"background-color: rgb(248, 245, 194);\n"
"font: 8pt \"Sans\";")
        self.resultado_list.setAlternatingRowColors(True)
        self.resultado_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.resultado_list.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.resultado_list.horizontalHeader().setStretchLastSection(True)
        self.resultado_list.verticalHeader().setVisible(False)

        self.gridLayout_2.addWidget(self.resultado_list, 1, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btn_aceptar = QPushButton(db_consulta_view)
        self.btn_aceptar.setObjectName(u"btn_aceptar")
        icon = QIcon()
        icon.addFile(u":/Icons/PNG/OK.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_aceptar.setIcon(icon)

        self.horizontalLayout.addWidget(self.btn_aceptar)

        self.btn_cancelar = QPushButton(db_consulta_view)
        self.btn_cancelar.setObjectName(u"btn_cancelar")
        icon1 = QIcon()
        icon1.addFile(u":/Icons/PNG/Cancel.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_cancelar.setIcon(icon1)

        self.horizontalLayout.addWidget(self.btn_cancelar)


        self.gridLayout_2.addLayout(self.horizontalLayout, 2, 0, 1, 2)

        QWidget.setTabOrder(self.lineaTextoBuscar, self.cboCampoBusqueda)
        QWidget.setTabOrder(self.cboCampoBusqueda, self.cboSentido)
        QWidget.setTabOrder(self.cboSentido, self.resultado_list)
        QWidget.setTabOrder(self.resultado_list, self.btn_aceptar)
        QWidget.setTabOrder(self.btn_aceptar, self.btn_cancelar)

        self.retranslateUi(db_consulta_view)
        self.btn_cancelar.clicked.connect(db_consulta_view.close)
        self.btn_aceptar.clicked.connect(db_consulta_view.accept)

        QMetaObject.connectSlotsByName(db_consulta_view)
    # setupUi

    def retranslateUi(self, db_consulta_view):
        db_consulta_view.setWindowTitle(QCoreApplication.translate("db_consulta_view", u"Buscar...", None))
        self.lbltabla.setText(QCoreApplication.translate("db_consulta_view", u"TextLabel", None))
        self.label_2.setText("")
        self.label_3.setText(QCoreApplication.translate("db_consulta_view", u"Ordenar Por:", None))
        self.label.setText(QCoreApplication.translate("db_consulta_view", u"Buscar:", None))
        self.label_4.setText(QCoreApplication.translate("db_consulta_view", u"Sentido:", None))
        self.btn_aceptar.setText(QCoreApplication.translate("db_consulta_view", u"Aceptar", None))
        self.btn_cancelar.setText(QCoreApplication.translate("db_consulta_view", u"Cancelar", None))
    # retranslateUi

