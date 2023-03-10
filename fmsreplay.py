# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './fmsreplay.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtChart import QChartView


class Ui_FMSReplay(object):
    def setupUi(self, FMSReplay):
        FMSReplay.setObjectName("FMSReplay")
        FMSReplay.resize(1300, 702)
        self.centralwidget = QtWidgets.QWidget(FMSReplay)
        self.centralwidget.setMinimumSize(QtCore.QSize(1300, 0))
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_Top = QtWidgets.QHBoxLayout()
        self.horizontalLayout_Top.setSpacing(10)
        self.horizontalLayout_Top.setObjectName("horizontalLayout_Top")
        self.pBtn_Open = QtWidgets.QPushButton(self.centralwidget)
        icon = QtGui.QIcon.fromTheme("fileopen")
        self.pBtn_Open.setIcon(icon)
        self.pBtn_Open.setObjectName("pBtn_Open")
        self.horizontalLayout_Top.addWidget(self.pBtn_Open)
        self.lbl_FileName = QtWidgets.QLabel(self.centralwidget)
        self.lbl_FileName.setMinimumSize(QtCore.QSize(20, 0))
        self.lbl_FileName.setObjectName("lbl_FileName")
        self.horizontalLayout_Top.addWidget(self.lbl_FileName)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_Top.addItem(spacerItem)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_Top.addItem(spacerItem1)
        self.lbl_PStart = QtWidgets.QLabel(self.centralwidget)
        self.lbl_PStart.setAutoFillBackground(True)
        self.lbl_PStart.setObjectName("lbl_PStart")
        self.horizontalLayout_Top.addWidget(self.lbl_PStart)
        self.lnEd_SetProgStartTime = QtWidgets.QLineEdit(self.centralwidget)
        self.lnEd_SetProgStartTime.setMinimumSize(QtCore.QSize(185, 0))
        self.lnEd_SetProgStartTime.setAutoFillBackground(True)
        self.lnEd_SetProgStartTime.setObjectName("lnEd_SetProgStartTime")
        self.horizontalLayout_Top.addWidget(self.lnEd_SetProgStartTime)
        self.lbl_Ignition = QtWidgets.QLabel(self.centralwidget)
        self.lbl_Ignition.setObjectName("lbl_Ignition")
        self.horizontalLayout_Top.addWidget(self.lbl_Ignition)
        self.lbl_IgnitionTime = QtWidgets.QLabel(self.centralwidget)
        self.lbl_IgnitionTime.setMinimumSize(QtCore.QSize(185, 0))
        self.lbl_IgnitionTime.setText("")
        self.lbl_IgnitionTime.setObjectName("lbl_IgnitionTime")
        self.horizontalLayout_Top.addWidget(self.lbl_IgnitionTime)
        self.pBtn_ZoomReset = QtWidgets.QPushButton(self.centralwidget)
        self.pBtn_ZoomReset.setObjectName("pBtn_ZoomReset")
        self.horizontalLayout_Top.addWidget(self.pBtn_ZoomReset)
        self.pBtn_Help = QtWidgets.QPushButton(self.centralwidget)
        self.pBtn_Help.setObjectName("pBtn_Help")
        self.horizontalLayout_Top.addWidget(self.pBtn_Help)
        self.verticalLayout_6.addLayout(self.horizontalLayout_Top)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_6.addWidget(self.line)
        self.horizontalLayout_Main = QtWidgets.QHBoxLayout()
        self.horizontalLayout_Main.setObjectName("horizontalLayout_Main")
        self.verticalLayout_Tabs = QtWidgets.QVBoxLayout()
        self.verticalLayout_Tabs.setObjectName("verticalLayout_Tabs")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setMinimumSize(QtCore.QSize(800, 0))
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_Log = QtWidgets.QWidget()
        self.tab_Log.setObjectName("tab_Log")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.tab_Log)
        self.verticalLayout_7.setContentsMargins(9, -1, -1, -1)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.pTxtEd = QtWidgets.QPlainTextEdit(self.tab_Log)
        self.pTxtEd.setEnabled(True)
        self.pTxtEd.setReadOnly(True)
        self.pTxtEd.setObjectName("pTxtEd")
        self.verticalLayout_7.addWidget(self.pTxtEd)
        self.tabWidget.addTab(self.tab_Log, "")
        self.tab_Analiz = QtWidgets.QWidget()
        self.tab_Analiz.setObjectName("tab_Analiz")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.tab_Analiz)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.splitter = QtWidgets.QSplitter(self.tab_Analiz)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.tblWidget = QtWidgets.QTableWidget(self.splitter)
        self.tblWidget.setObjectName("tblWidget")
        self.tblWidget.setColumnCount(5)
        self.tblWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tblWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblWidget.setHorizontalHeaderItem(4, item)
        self.tblWidget.horizontalHeader().setVisible(False)
        self.tblWidget.verticalHeader().setStretchLastSection(False)
        self.pTxtEd_Report = QtWidgets.QPlainTextEdit(self.splitter)
        self.pTxtEd_Report.setReadOnly(True)
        self.pTxtEd_Report.setObjectName("pTxtEd_Report")
        self.verticalLayout_8.addWidget(self.splitter)
        self.tabWidget.addTab(self.tab_Analiz, "")
        self.tab_LevelF1 = QtWidgets.QWidget()
        self.tab_LevelF1.setEnabled(True)
        self.tab_LevelF1.setObjectName("tab_LevelF1")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.tab_LevelF1)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.graphView_F = QChartView(self.tab_LevelF1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphView_F.sizePolicy().hasHeightForWidth())
        self.graphView_F.setSizePolicy(sizePolicy)
        self.graphView_F.setObjectName("graphView_F")
        self.verticalLayout_9.addWidget(self.graphView_F)
        self.tabWidget.addTab(self.tab_LevelF1, "")
        self.tab_LevelO1 = QtWidgets.QWidget()
        self.tab_LevelO1.setObjectName("tab_LevelO1")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.tab_LevelO1)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.graphView_O = QChartView(self.tab_LevelO1)
        self.graphView_O.setObjectName("graphView_O")
        self.verticalLayout_10.addWidget(self.graphView_O)
        self.tabWidget.addTab(self.tab_LevelO1, "")
        self.tab_LevelF1_UTC = QtWidgets.QWidget()
        self.tab_LevelF1_UTC.setObjectName("tab_LevelF1_UTC")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.tab_LevelF1_UTC)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.graphView_FU = QChartView(self.tab_LevelF1_UTC)
        self.graphView_FU.setObjectName("graphView_FU")
        self.verticalLayout_11.addWidget(self.graphView_FU)
        self.tabWidget.addTab(self.tab_LevelF1_UTC, "")
        self.tab_LevelO1_UTC = QtWidgets.QWidget()
        self.tab_LevelO1_UTC.setObjectName("tab_LevelO1_UTC")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.tab_LevelO1_UTC)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.graphView_OU = QChartView(self.tab_LevelO1_UTC)
        self.graphView_OU.setObjectName("graphView_OU")
        self.verticalLayout_12.addWidget(self.graphView_OU)
        self.tabWidget.addTab(self.tab_LevelO1_UTC, "")
        self.tab_TempF1_UTC = QtWidgets.QWidget()
        self.tab_TempF1_UTC.setObjectName("tab_TempF1_UTC")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab_TempF1_UTC)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.graphView_TFU = QChartView(self.tab_TempF1_UTC)
        self.graphView_TFU.setObjectName("graphView_TFU")
        self.verticalLayout_5.addWidget(self.graphView_TFU)
        self.tabWidget.addTab(self.tab_TempF1_UTC, "")
        self.verticalLayout_Tabs.addWidget(self.tabWidget)
        self.horizontalLayout_Main.addLayout(self.verticalLayout_Tabs)
        self.verticalLayout_6.addLayout(self.horizontalLayout_Main)
        FMSReplay.setCentralWidget(self.centralwidget)

        self.retranslateUi(FMSReplay)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(FMSReplay)

    def retranslateUi(self, FMSReplay):
        _translate = QtCore.QCoreApplication.translate
        FMSReplay.setWindowTitle(_translate("FMSReplay", "FMSReplay"))
        self.lbl_FileName.setText(_translate("FMSReplay", "<html><head/><body><p>&lt;FMS log file not loaded&gt;</p></body></html>"))
        self.lbl_PStart.setText(_translate("FMSReplay", "PROGRAM START:"))
        self.lnEd_SetProgStartTime.setInputMask(_translate("FMSReplay", "99.99.9999 / 99:99:99.999"))
        self.lbl_Ignition.setText(_translate("FMSReplay", "IGNITION:"))
        self.pBtn_ZoomReset.setText(_translate("FMSReplay", "Zoom reset"))
        self.pBtn_Help.setText(_translate("FMSReplay", "Help"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Log), _translate("FMSReplay", "FMS log"))
        item = self.tblWidget.horizontalHeaderItem(0)
        item.setText(_translate("FMSReplay", "??????????"))
        item = self.tblWidget.horizontalHeaderItem(1)
        item.setText(_translate("FMSReplay", "????????????????"))
        item = self.tblWidget.horizontalHeaderItem(2)
        item.setText(_translate("FMSReplay", "????????????????"))
        item = self.tblWidget.horizontalHeaderItem(3)
        item.setText(_translate("FMSReplay", "??????????????"))
        item = self.tblWidget.horizontalHeaderItem(4)
        item.setText(_translate("FMSReplay", "New Column"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Analiz), _translate("FMSReplay", "Report"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_LevelF1), _translate("FMSReplay", "Level F1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_LevelO1), _translate("FMSReplay", "Level O1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_LevelF1_UTC), _translate("FMSReplay", "Level F1(UTC)"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_LevelO1_UTC), _translate("FMSReplay", "Level O1 (UTC)"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_TempF1_UTC), _translate("FMSReplay", "Temperature (UTC)"))
# from QtCharts import QChartView
