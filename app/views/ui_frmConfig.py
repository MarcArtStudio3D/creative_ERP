# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frmConfig.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QGroupBox, QSizePolicy, QWidget)

class Ui_frmConfig(object):
    def setupUi(self, frmConfig):
        if not frmConfig.objectName():
            frmConfig.setObjectName(u"frmConfig")
        frmConfig.resize(804, 474)
        self.buttonBox = QDialogButtonBox(frmConfig)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(450, 430, 341, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.groupBox = QGroupBox(frmConfig)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(20, 20, 271, 111))
        self.cboIdioma = QComboBox(self.groupBox)
        self.cboIdioma.addItem("")
        self.cboIdioma.addItem("")
        self.cboIdioma.addItem("")
        self.cboIdioma.addItem("")
        self.cboIdioma.setObjectName(u"cboIdioma")
        self.cboIdioma.setGeometry(QRect(10, 40, 241, 32))
        self.groupBox_2 = QGroupBox(frmConfig)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(300, 20, 241, 111))
        self.cboValoresFiscales = QComboBox(self.groupBox_2)
        self.cboValoresFiscales.addItem("")
        self.cboValoresFiscales.addItem("")
        self.cboValoresFiscales.setObjectName(u"cboValoresFiscales")
        self.cboValoresFiscales.setGeometry(QRect(20, 40, 201, 32))

        self.retranslateUi(frmConfig)
        self.buttonBox.accepted.connect(frmConfig.accept)
        self.buttonBox.rejected.connect(frmConfig.reject)

        QMetaObject.connectSlotsByName(frmConfig)
    # setupUi

    def retranslateUi(self, frmConfig):
        frmConfig.setWindowTitle(QCoreApplication.translate("frmConfig", u"Configuraci\u00f3n de Creative ERP", None))
        self.groupBox.setTitle(QCoreApplication.translate("frmConfig", u"Idioma", None))
        self.cboIdioma.setItemText(0, QCoreApplication.translate("frmConfig", u"Espa\u00f1ol", None))
        self.cboIdioma.setItemText(1, QCoreApplication.translate("frmConfig", u"Fran\u00e7aise", None))
        self.cboIdioma.setItemText(2, QCoreApplication.translate("frmConfig", u"Catal\u00e0", None))
        self.cboIdioma.setItemText(3, QCoreApplication.translate("frmConfig", u"English", None))

        self.groupBox_2.setTitle(QCoreApplication.translate("frmConfig", u"Normativa Pais", None))
        self.cboValoresFiscales.setItemText(0, QCoreApplication.translate("frmConfig", u"Francia", None))
        self.cboValoresFiscales.setItemText(1, QCoreApplication.translate("frmConfig", u"Espa\u00f1a", None))

    # retranslateUi

