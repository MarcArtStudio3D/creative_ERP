# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frmtipocliente.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QListView, QPushButton,
    QSizePolicy, QSpacerItem, QWidget)

class Ui_frmTipoCliente(object):
    def setupUi(self, frmTipoCliente):
        if not frmTipoCliente.objectName():
            frmTipoCliente.setObjectName(u"frmTipoCliente")
        frmTipoCliente.resize(676, 459)
        self.gridLayout_4 = QGridLayout(frmTipoCliente)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label = QLabel(frmTipoCliente)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)

        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)

        self.txtNombre = QLineEdit(frmTipoCliente)
        self.txtNombre.setObjectName(u"txtNombre")

        self.gridLayout_3.addWidget(self.txtNombre, 0, 1, 1, 1)

        self.label_2 = QLabel(frmTipoCliente)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_3.addWidget(self.label_2, 1, 0, 1, 1)

        self.txtDesc = QLineEdit(frmTipoCliente)
        self.txtDesc.setObjectName(u"txtDesc")

        self.gridLayout_3.addWidget(self.txtDesc, 1, 1, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_3, 2, 0, 1, 2)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.btnBorrarSubTipo = QPushButton(frmTipoCliente)
        self.btnBorrarSubTipo.setObjectName(u"btnBorrarSubTipo")

        self.gridLayout_2.addWidget(self.btnBorrarSubTipo, 2, 1, 1, 1)

        self.btnEditarSubTipo = QPushButton(frmTipoCliente)
        self.btnEditarSubTipo.setObjectName(u"btnEditarSubTipo")

        self.gridLayout_2.addWidget(self.btnEditarSubTipo, 2, 0, 1, 1)

        self.lista_subtipos = QListView(frmTipoCliente)
        self.lista_subtipos.setObjectName(u"lista_subtipos")

        self.gridLayout_2.addWidget(self.lista_subtipos, 1, 0, 1, 2)

        self.label_4 = QLabel(frmTipoCliente)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_2, 0, 1, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(287, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btnInsertarenFichaCliente = QPushButton(frmTipoCliente)
        self.btnInsertarenFichaCliente.setObjectName(u"btnInsertarenFichaCliente")

        self.horizontalLayout.addWidget(self.btnInsertarenFichaCliente)

        self.pushButton_3 = QPushButton(frmTipoCliente)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout.addWidget(self.pushButton_3)


        self.gridLayout_4.addLayout(self.horizontalLayout, 3, 0, 1, 2)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.lista_tipos = QListView(frmTipoCliente)
        self.lista_tipos.setObjectName(u"lista_tipos")

        self.gridLayout.addWidget(self.lista_tipos, 1, 0, 1, 2)

        self.btnBorrarTipo = QPushButton(frmTipoCliente)
        self.btnBorrarTipo.setObjectName(u"btnBorrarTipo")

        self.gridLayout.addWidget(self.btnBorrarTipo, 2, 1, 1, 1)

        self.btnEditarTipo = QPushButton(frmTipoCliente)
        self.btnEditarTipo.setObjectName(u"btnEditarTipo")

        self.gridLayout.addWidget(self.btnEditarTipo, 2, 0, 1, 1)

        self.label_3 = QLabel(frmTipoCliente)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.btnAddTipo = QPushButton(frmTipoCliente)
        self.btnAddTipo.setObjectName(u"btnAddTipo")

        self.gridLayout_4.addWidget(self.btnAddTipo, 1, 0, 1, 1)

        self.btnAddSubTipo = QPushButton(frmTipoCliente)
        self.btnAddSubTipo.setObjectName(u"btnAddSubTipo")

        self.gridLayout_4.addWidget(self.btnAddSubTipo, 1, 1, 1, 1)


        self.retranslateUi(frmTipoCliente)

        QMetaObject.connectSlotsByName(frmTipoCliente)
    # setupUi

    def retranslateUi(self, frmTipoCliente):
        frmTipoCliente.setWindowTitle(QCoreApplication.translate("frmTipoCliente", u"Tipos de Cliente", None))
        self.label.setText(QCoreApplication.translate("frmTipoCliente", u"Nombre", None))
        self.label_2.setText(QCoreApplication.translate("frmTipoCliente", u"Descripci\u00f3n", None))
        self.btnBorrarSubTipo.setText(QCoreApplication.translate("frmTipoCliente", u"Borrar", None))
        self.btnEditarSubTipo.setText(QCoreApplication.translate("frmTipoCliente", u"Guardar cambios", None))
        self.label_4.setText(QCoreApplication.translate("frmTipoCliente", u"SUBTIPO CLIENTE", None))
        self.btnInsertarenFichaCliente.setText(QCoreApplication.translate("frmTipoCliente", u"Insertar en ficha cliente", None))
        self.pushButton_3.setText(QCoreApplication.translate("frmTipoCliente", u"Salir", None))
        self.btnBorrarTipo.setText(QCoreApplication.translate("frmTipoCliente", u"Borrar", None))
        self.btnEditarTipo.setText(QCoreApplication.translate("frmTipoCliente", u"Guardar cambios", None))
        self.label_3.setText(QCoreApplication.translate("frmTipoCliente", u"TIPO CLIENTE", None))
        self.btnAddTipo.setText(QCoreApplication.translate("frmTipoCliente", u"A\u00f1adir Tipo cliente", None))
        self.btnAddSubTipo.setText(QCoreApplication.translate("frmTipoCliente", u"A\u00f1adir Subtipo cliente", None))
    # retranslateUi

