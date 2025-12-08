# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'db_consulta_view.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject, QSize, Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QTableView,
    QWidget,
)


class Ui_db_consulta_view(object):
    def setupUi(self, db_consulta_view):
        if not db_consulta_view.objectName():
            db_consulta_view.setObjectName("db_consulta_view")
        db_consulta_view.setWindowModality(Qt.WindowModality.WindowModal)
        db_consulta_view.resize(1214, 567)
        db_consulta_view.setModal(False)
        self.gridLayout_2 = QGridLayout(db_consulta_view)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lbltabla = QLabel(db_consulta_view)
        self.lbltabla.setObjectName("lbltabla")
        self.lbltabla.setMaximumSize(QSize(16777215, 22))
        self.lbltabla.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lbltabla, 0, 0, 1, 1)

        self.frame = QFrame(db_consulta_view)
        self.frame.setObjectName("frame")
        self.frame.setMaximumSize(QSize(250, 16777215))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.label_2.setMaximumSize(QSize(128, 128))
        self.label_2.setPixmap(QPixmap(":/Icons/PNG/find2.png"))

        self.gridLayout.addWidget(self.label_2, 1, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(
            20, 259, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.gridLayout.addItem(self.verticalSpacer, 5, 1, 1, 1)

        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName("label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.lineaTextoBuscar = QLineEdit(self.frame)
        self.lineaTextoBuscar.setObjectName("lineaTextoBuscar")

        self.gridLayout.addWidget(self.lineaTextoBuscar, 4, 1, 1, 1)

        self.label = QLabel(self.frame)
        self.label.setObjectName("label")

        self.gridLayout.addWidget(self.label, 4, 0, 1, 1)

        self.cboCampoBusqueda = QComboBox(self.frame)
        self.cboCampoBusqueda.setObjectName("cboCampoBusqueda")

        self.gridLayout.addWidget(self.cboCampoBusqueda, 2, 1, 1, 1)

        self.cboSentido = QComboBox(self.frame)
        self.cboSentido.setObjectName("cboSentido")

        self.gridLayout.addWidget(self.cboSentido, 3, 1, 1, 1)

        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName("label_4")

        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)

        self.gridLayout_2.addWidget(self.frame, 0, 1, 2, 1)

        self.resultado_list = QTableView(db_consulta_view)
        self.resultado_list.setObjectName("resultado_list")
        self.resultado_list.setAlternatingRowColors(True)
        self.resultado_list.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.resultado_list.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.resultado_list.horizontalHeader().setStretchLastSection(True)
        self.resultado_list.verticalHeader().setVisible(False)

        self.gridLayout_2.addWidget(self.resultado_list, 1, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btn_aceptar = QPushButton(db_consulta_view)
        self.btn_aceptar.setObjectName("btn_aceptar")
        icon = QIcon()
        icon.addFile(":/Icons/PNG/OK.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_aceptar.setIcon(icon)

        self.horizontalLayout.addWidget(self.btn_aceptar)

        self.btn_cancelar = QPushButton(db_consulta_view)
        self.btn_cancelar.setObjectName("btn_cancelar")
        icon1 = QIcon()
        icon1.addFile(
            ":/Icons/PNG/Cancel.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
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
        try:
            self.btn_aceptar.clicked.connect(db_consulta_view.accept)
        except Exception:
            try:
                self.btn_aceptar.clicked.connect(db_consulta_view.close)
            except Exception:
                pass

        QMetaObject.connectSlotsByName(db_consulta_view)

    # setupUi

    def retranslateUi(self, db_consulta_view):
        db_consulta_view.setWindowTitle(
            QCoreApplication.translate("db_consulta_view", "Buscar...", None)
        )
        self.lbltabla.setText(
            QCoreApplication.translate("db_consulta_view", "TextLabel", None)
        )
        self.label_2.setText("")
        self.label_3.setText(
            QCoreApplication.translate("db_consulta_view", "Ordenar Por:", None)
        )
        self.label.setText(
            QCoreApplication.translate("db_consulta_view", "Buscar:", None)
        )
        self.label_4.setText(
            QCoreApplication.translate("db_consulta_view", "Sentido:", None)
        )
        self.btn_aceptar.setText(
            QCoreApplication.translate("db_consulta_view", "Aceptar", None)
        )
        self.btn_cancelar.setText(
            QCoreApplication.translate("db_consulta_view", "Cancelar", None)
        )

    # retranslateUi
