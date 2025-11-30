# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frmDivisiones.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGridLayout,
    QGroupBox, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QSpacerItem,
    QWidget)
from modules import designer_rc

class Ui_DlgDivisionesAlmacen(object):
    def setupUi(self, DlgDivisionesAlmacen):
        if not DlgDivisionesAlmacen.objectName():
            DlgDivisionesAlmacen.setObjectName(u"DlgDivisionesAlmacen")
        DlgDivisionesAlmacen.resize(996, 549)
        self.gridLayout_2 = QGridLayout(DlgDivisionesAlmacen)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_2 = QLabel(DlgDivisionesAlmacen)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"background-color: #304163;\n"
"color: rgb(255, 255, 255);")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label_2, 0, 3, 1, 2)

        self.listFamilias = QListWidget(DlgDivisionesAlmacen)
        self.listFamilias.setObjectName(u"listFamilias")

        self.gridLayout_2.addWidget(self.listFamilias, 1, 3, 1, 2)

        self.btnBorrarSub = QPushButton(DlgDivisionesAlmacen)
        self.btnBorrarSub.setObjectName(u"btnBorrarSub")
        icon = QIcon()
        icon.addFile(u":/PNG/resources/icons/png/delete.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnBorrarSub.setIcon(icon)

        self.gridLayout_2.addWidget(self.btnBorrarSub, 3, 5, 1, 1)

        self.btnBorrarFam = QPushButton(DlgDivisionesAlmacen)
        self.btnBorrarFam.setObjectName(u"btnBorrarFam")
        self.btnBorrarFam.setIcon(icon)

        self.gridLayout_2.addWidget(self.btnBorrarFam, 3, 3, 1, 1)

        self.label_6 = QLabel(DlgDivisionesAlmacen)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setStyleSheet(u"background-color: #304163;\n"
"color: rgb(255, 255, 255);")
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label_6, 0, 5, 1, 2)

        self.listSubfamilias = QListWidget(DlgDivisionesAlmacen)
        self.listSubfamilias.setObjectName(u"listSubfamilias")

        self.gridLayout_2.addWidget(self.listSubfamilias, 1, 5, 1, 2)

        self.btnActualizarSeccion = QPushButton(DlgDivisionesAlmacen)
        self.btnActualizarSeccion.setObjectName(u"btnActualizarSeccion")
        icon1 = QIcon()
        icon1.addFile(u":/PNG/resources/icons/png/Save.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnActualizarSeccion.setIcon(icon1)

        self.gridLayout_2.addWidget(self.btnActualizarSeccion, 2, 2, 1, 1)

        self.btnActualizarSubfamilia = QPushButton(DlgDivisionesAlmacen)
        self.btnActualizarSubfamilia.setObjectName(u"btnActualizarSubfamilia")
        self.btnActualizarSubfamilia.setIcon(icon1)

        self.gridLayout_2.addWidget(self.btnActualizarSubfamilia, 2, 6, 1, 1)

        self.btnBorrarSec = QPushButton(DlgDivisionesAlmacen)
        self.btnBorrarSec.setObjectName(u"btnBorrarSec")
        self.btnBorrarSec.setIcon(icon)

        self.gridLayout_2.addWidget(self.btnBorrarSec, 3, 1, 1, 1)

        self.frame = QFrame(DlgDivisionesAlmacen)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.btnCerrar = QPushButton(self.frame)
        self.btnCerrar.setObjectName(u"btnCerrar")
        self.btnCerrar.setEnabled(False)
        icon2 = QIcon()
        icon2.addFile(u":/PNG/resources/icons/png/close.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnCerrar.setIcon(icon2)

        self.gridLayout.addWidget(self.btnCerrar, 5, 4, 1, 1)

        self.lbl_imagen = QLabel(self.frame)
        self.lbl_imagen.setObjectName(u"lbl_imagen")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_imagen.sizePolicy().hasHeightForWidth())
        self.lbl_imagen.setSizePolicy(sizePolicy)
        self.lbl_imagen.setMaximumSize(QSize(250, 250))
        self.lbl_imagen.setPixmap(QPixmap(u":/Icons/PNG/Box.png"))
        self.lbl_imagen.setScaledContents(True)

        self.gridLayout.addWidget(self.lbl_imagen, 2, 0, 3, 2)

        self.lbl_tree = QLabel(self.frame)
        self.lbl_tree.setObjectName(u"lbl_tree")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lbl_tree.sizePolicy().hasHeightForWidth())
        self.lbl_tree.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.lbl_tree, 0, 0, 1, 5)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 2, 3, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 2, 2, 1, 1)


        self.gridLayout_2.addWidget(self.frame, 5, 1, 1, 6)

        self.btnActualizarFamilia = QPushButton(DlgDivisionesAlmacen)
        self.btnActualizarFamilia.setObjectName(u"btnActualizarFamilia")
        self.btnActualizarFamilia.setIcon(icon1)

        self.gridLayout_2.addWidget(self.btnActualizarFamilia, 2, 4, 1, 1)

        self.label = QLabel(DlgDivisionesAlmacen)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(16777215, 21))
        self.label.setStyleSheet(u"background-color: #304163;\n"
"color: rgb(255, 255, 255);")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label, 0, 1, 1, 2)

        self.btnAddSeccion = QPushButton(DlgDivisionesAlmacen)
        self.btnAddSeccion.setObjectName(u"btnAddSeccion")
        self.btnAddSeccion.setEnabled(True)
        icon3 = QIcon()
        icon3.addFile(u":/PNG/resources/icons/png/Add.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnAddSeccion.setIcon(icon3)

        self.gridLayout_2.addWidget(self.btnAddSeccion, 2, 1, 1, 1)

        self.btnAddSub = QPushButton(DlgDivisionesAlmacen)
        self.btnAddSub.setObjectName(u"btnAddSub")
        self.btnAddSub.setEnabled(False)
        self.btnAddSub.setIcon(icon3)

        self.gridLayout_2.addWidget(self.btnAddSub, 2, 5, 1, 1)

        self.listSecciones = QListWidget(DlgDivisionesAlmacen)
        self.listSecciones.setObjectName(u"listSecciones")

        self.gridLayout_2.addWidget(self.listSecciones, 1, 1, 1, 2)

        self.btnAddFamily = QPushButton(DlgDivisionesAlmacen)
        self.btnAddFamily.setObjectName(u"btnAddFamily")
        self.btnAddFamily.setEnabled(False)
        self.btnAddFamily.setIcon(icon3)

        self.gridLayout_2.addWidget(self.btnAddFamily, 2, 3, 1, 1)

        self.groupBox = QGroupBox(DlgDivisionesAlmacen)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy2)
        self.gridLayoutWidget = QWidget(self.groupBox)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(20, 50, 611, 41))
        self.gridLayout_3 = QGridLayout(self.gridLayoutWidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_5 = QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_3.addWidget(self.label_5, 0, 2, 1, 1)

        self.label_3 = QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 1)

        self.txtcodigo = QLineEdit(self.gridLayoutWidget)
        self.txtcodigo.setObjectName(u"txtcodigo")
        self.txtcodigo.setMaximumSize(QSize(300, 16777215))
        self.txtcodigo.setReadOnly(True)

        self.gridLayout_3.addWidget(self.txtcodigo, 0, 1, 1, 1)

        self.txtnombre = QLineEdit(self.gridLayoutWidget)
        self.txtnombre.setObjectName(u"txtnombre")
        self.txtnombre.setMinimumSize(QSize(350, 0))
        self.txtnombre.setMaximumSize(QSize(16777215, 16777215))
        self.txtnombre.setReadOnly(True)

        self.gridLayout_3.addWidget(self.txtnombre, 0, 3, 1, 1)


        self.gridLayout_2.addWidget(self.groupBox, 4, 2, 1, 4)


        self.retranslateUi(DlgDivisionesAlmacen)

        QMetaObject.connectSlotsByName(DlgDivisionesAlmacen)
    # setupUi

    def retranslateUi(self, DlgDivisionesAlmacen):
        DlgDivisionesAlmacen.setWindowTitle(QCoreApplication.translate("DlgDivisionesAlmacen", u"Divisiones del almac\u00e9n", None))
        self.label_2.setText(QCoreApplication.translate("DlgDivisionesAlmacen", u"Familias", None))
        self.btnBorrarSub.setText(QCoreApplication.translate("DlgDivisionesAlmacen", u"Borrar subfamilia", None))
        self.btnBorrarFam.setText(QCoreApplication.translate("DlgDivisionesAlmacen", u"Borrar familia", None))
        self.label_6.setText(QCoreApplication.translate("DlgDivisionesAlmacen", u"Subfamilias", None))
        self.btnActualizarSeccion.setText(QCoreApplication.translate("DlgDivisionesAlmacen", u"Actualizar", None))
        self.btnActualizarSubfamilia.setText(QCoreApplication.translate("DlgDivisionesAlmacen", u"Actualizar", None))
        self.btnBorrarSec.setText(QCoreApplication.translate("DlgDivisionesAlmacen", u"Borrar secci\u00f3n", None))
        self.btnCerrar.setText(QCoreApplication.translate("DlgDivisionesAlmacen", u"Cerrar", None))
        self.lbl_imagen.setText("")
        self.lbl_tree.setText("")
        self.btnActualizarFamilia.setText(QCoreApplication.translate("DlgDivisionesAlmacen", u"Actualizar", None))
        self.label.setText(QCoreApplication.translate("DlgDivisionesAlmacen", u"Secciones", None))
        self.btnAddSeccion.setText(QCoreApplication.translate("DlgDivisionesAlmacen", u"A\u00f1adir secci\u00f3n", None))
        self.btnAddSub.setText(QCoreApplication.translate("DlgDivisionesAlmacen", u"A\u00f1adir subfamilia", None))
        self.btnAddFamily.setText(QCoreApplication.translate("DlgDivisionesAlmacen", u"A\u00f1adir familia", None))
        self.groupBox.setTitle(QCoreApplication.translate("DlgDivisionesAlmacen", u"VALORES EN EDICI\u00d3N", None))
        self.label_5.setText(QCoreApplication.translate("DlgDivisionesAlmacen", u"Nombre", None))
        self.label_3.setText(QCoreApplication.translate("DlgDivisionesAlmacen", u"Codigo", None))
    # retranslateUi

