# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Karapuzo\PycharmProjects\Tarkov-Parser\Tarkov-Helper.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(353, 389)
        MainWindow.setWindowTitle("Tarkov Helper")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.btn_sort_barters = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Bender")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btn_sort_barters.setFont(font)
        self.btn_sort_barters.setObjectName("btn_sort_barters")
        self.gridLayout.addWidget(self.btn_sort_barters, 2, 1, 1, 1)
        self.Title = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Bender")
        font.setPointSize(38)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.Title.setFont(font)
        self.Title.setMouseTracking(True)
        self.Title.setFocusPolicy(QtCore.Qt.NoFocus)
        self.Title.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.Title.setToolTip("")
        self.Title.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Title.setAutoFillBackground(True)
        self.Title.setObjectName("Title")
        self.gridLayout.addWidget(self.Title, 0, 0, 1, 2)
        self.btn_refresh_price = QtWidgets.QPushButton(self.centralwidget)
        self.btn_refresh_price.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Bender")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.btn_refresh_price.setFont(font)
        self.btn_refresh_price.setObjectName("btn_refresh_price")
        self.gridLayout.addWidget(self.btn_refresh_price, 1, 0, 1, 2)
        self.btn_make_table = QtWidgets.QPushButton(self.centralwidget)
        self.btn_make_table.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Bender")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.btn_make_table.setFont(font)
        self.btn_make_table.setObjectName("btn_make_table")
        self.gridLayout.addWidget(self.btn_make_table, 4, 0, 1, 2)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 6, 0, 1, 2)
        self.btn_open_table = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Bender")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btn_open_table.setFont(font)
        self.btn_open_table.setObjectName("btn_open_table")
        self.gridLayout.addWidget(self.btn_open_table, 7, 1, 1, 1)
        self.btn_make_crafts = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Bender")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btn_make_crafts.setFont(font)
        self.btn_make_crafts.setObjectName("btn_make_crafts")
        self.gridLayout.addWidget(self.btn_make_crafts, 5, 0, 1, 1)
        self.btn_make_barters = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Bender")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btn_make_barters.setFont(font)
        self.btn_make_barters.setObjectName("btn_make_barters")
        self.gridLayout.addWidget(self.btn_make_barters, 5, 1, 1, 1)
        self.btn_sort_crafts = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Bender")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btn_sort_crafts.setFont(font)
        self.btn_sort_crafts.setObjectName("btn_sort_crafts")
        self.gridLayout.addWidget(self.btn_sort_crafts, 2, 0, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 3, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 353, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.toolBar_2 = QtWidgets.QToolBar(MainWindow)
        self.toolBar_2.setObjectName("toolBar_2")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar_2)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.btn_sort_barters.setText(_translate("MainWindow", "?????????????????????? ??????????????"))
        self.Title.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">EFT Helper</p></body></html>"))
        self.btn_refresh_price.setText(_translate("MainWindow", "???????????????? ????????"))
        self.btn_make_table.setText(_translate("MainWindow", "?????????????????????? ?????? ??????????????"))
        self.btn_open_table.setText(_translate("MainWindow", "?????????????? ??????????????"))
        self.btn_make_crafts.setText(_translate("MainWindow", "???????????????? ????????????"))
        self.btn_make_barters.setText(_translate("MainWindow", "???????????????? ??????????????"))
        self.btn_sort_crafts.setText(_translate("MainWindow", "?????????????????????? ????????????"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.toolBar_2.setWindowTitle(_translate("MainWindow", "toolBar_2"))
