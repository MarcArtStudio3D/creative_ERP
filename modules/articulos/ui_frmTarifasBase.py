# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frmTarifasBase.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QGridLayout,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QPlainTextEdit, QPushButton, QSizePolicy, QSpacerItem,
    QStackedWidget, QTableWidget, QTableWidgetItem, QWidget)
from modules import designer_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1050, 516)
        self.stackedWidget = QStackedWidget(Dialog)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(10, 20, 1041, 491))
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.gridLayoutWidget = QWidget(self.page)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(0, 0, 1031, 221))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)

        self.lineEdit = QLineEdit(self.gridLayoutWidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMaximumSize(QSize(120, 16777215))

        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)

        self.label_2 = QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)

        self.label_3 = QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)

        self.plainTextEdit = QPlainTextEdit(self.gridLayoutWidget)
        self.plainTextEdit.setObjectName(u"plainTextEdit")

        self.gridLayout.addWidget(self.plainTextEdit, 2, 1, 1, 4)

        self.label = QLabel(self.gridLayoutWidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.lineEdit_2 = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.gridLayout.addWidget(self.lineEdit_2, 0, 4, 1, 1)

        self.comboBox = QComboBox(self.gridLayoutWidget)
        self.comboBox.setObjectName(u"comboBox")

        self.gridLayout.addWidget(self.comboBox, 1, 1, 1, 3)

        self.horizontalLayoutWidget = QWidget(self.page)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(0, 440, 1031, 51))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.btnAnadir = QPushButton(self.horizontalLayoutWidget)
        self.btnAnadir.setObjectName(u"btnAnadir")
        icon = QIcon()
        icon.addFile(u":/PNG/resources/icons/png/Add.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnAnadir.setIcon(icon)

        self.horizontalLayout.addWidget(self.btnAnadir)

        self.btnSiguente = QPushButton(self.horizontalLayoutWidget)
        self.btnSiguente.setObjectName(u"btnSiguente")
        icon1 = QIcon()
        icon1.addFile(u":/PNG/resources/icons/png/Next.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnSiguente.setIcon(icon1)

        self.horizontalLayout.addWidget(self.btnSiguente)

        self.btnAnterior = QPushButton(self.horizontalLayoutWidget)
        self.btnAnterior.setObjectName(u"btnAnterior")
        icon2 = QIcon()
        icon2.addFile(u":/PNG/resources/icons/png/Previous.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnAnterior.setIcon(icon2)

        self.horizontalLayout.addWidget(self.btnAnterior)

        self.btnBuscar = QPushButton(self.horizontalLayoutWidget)
        self.btnBuscar.setObjectName(u"btnBuscar")
        icon3 = QIcon()
        icon3.addFile(u":/PNG/resources/icons/png/search.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnBuscar.setIcon(icon3)

        self.horizontalLayout.addWidget(self.btnBuscar)

        self.btnEditar = QPushButton(self.horizontalLayoutWidget)
        self.btnEditar.setObjectName(u"btnEditar")
        icon4 = QIcon()
        icon4.addFile(u":/PNG/resources/icons/png/Edit.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnEditar.setIcon(icon4)

        self.horizontalLayout.addWidget(self.btnEditar)

        self.btnGuardar = QPushButton(self.horizontalLayoutWidget)
        self.btnGuardar.setObjectName(u"btnGuardar")
        self.btnGuardar.setEnabled(False)
        icon5 = QIcon()
        icon5.addFile(u":/PNG/resources/icons/png/Save.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnGuardar.setIcon(icon5)

        self.horizontalLayout.addWidget(self.btnGuardar)

        self.btnDeshacer = QPushButton(self.horizontalLayoutWidget)
        self.btnDeshacer.setObjectName(u"btnDeshacer")
        self.btnDeshacer.setEnabled(False)
        icon6 = QIcon()
        icon6.addFile(u":/PNG/resources/icons/png/undo.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnDeshacer.setIcon(icon6)

        self.horizontalLayout.addWidget(self.btnDeshacer)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btnBorrar = QPushButton(self.horizontalLayoutWidget)
        self.btnBorrar.setObjectName(u"btnBorrar")
        icon7 = QIcon()
        icon7.addFile(u":/PNG/resources/icons/png/delete.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnBorrar.setIcon(icon7)

        self.horizontalLayout.addWidget(self.btnBorrar)

        self.pushButton = QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName(u"pushButton")
        icon8 = QIcon()
        icon8.addFile(u":/PNG/resources/icons/png/close.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton.setIcon(icon8)

        self.horizontalLayout.addWidget(self.pushButton)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.tableWidget = QTableWidget(self.page_2)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(0, 0, 1031, 491))
        self.tableWidget.verticalHeader().setVisible(False)
        self.stackedWidget.addWidget(self.page_2)

        self.retranslateUi(Dialog)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Gesti\u00f3n de tarifas base", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Descripci\u00f3n:", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Nombre:", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Moneda:", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"C\u00f3digo:", None))
        self.btnAnadir.setText(QCoreApplication.translate("Dialog", u"Nueva", None))
        self.btnSiguente.setText(QCoreApplication.translate("Dialog", u"Siguiente", None))
        self.btnAnterior.setText(QCoreApplication.translate("Dialog", u"Anterior", None))
        self.btnBuscar.setText(QCoreApplication.translate("Dialog", u"Buscar", None))
        self.btnEditar.setText(QCoreApplication.translate("Dialog", u"Editar", None))
        self.btnGuardar.setText(QCoreApplication.translate("Dialog", u"Guardar", None))
        self.btnDeshacer.setText(QCoreApplication.translate("Dialog", u"Deshacer", None))
        self.btnBorrar.setText(QCoreApplication.translate("Dialog", u"Borrar", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog", u"Cerrar", None))
    # retranslateUi

