import typing

from PyQt5.QtWidgets import QMenuBar, QWidget, QMenu, QAction
from PyQt5 import QtCore

ACTIONREPORT = 'ACTIONREPORT'
CONFIGURATIONS = 'CONFIGURATIONS'
FILTER = 'FILTER'
GRAPH = 'GRAPH'


class PickMenuBar(QMenuBar):

    # USE IN WINDOW YOU WANT TO USE MENU BAR IN
    # self.menubar = Common.PickMenuBar(<WINDOW NAME>, omit=Common.<WINDOW ENUM>)
    # <WINDOW NAME>.setMenuBar(self.menubar)

    def __init__(self, parent: typing.Optional[QWidget] = ..., omit='') -> None:
        super().__init__(parent)
        self.setGeometry(QtCore.QRect(0, 0, 870, 22))
        self.setObjectName("menubar")
        self.menuMain = QMenu(self)
        self.menuMain.setObjectName("menuMain")
        self.actionEvent_Configuration = QAction(parent)
        self.actionEvent_Configuration.setObjectName("actionEvent_Configuration")
        self.actionEnforcement_Action_Report = QAction(parent)
        self.actionEnforcement_Action_Report.setObjectName("actionEnforcement_Action_Report")
        self.actionSearch_Filter_Log_Entries = QAction(parent)
        self.actionSearch_Filter_Log_Entries.setObjectName("actionSearch_Filter_Log_Entries")
        self.actionManage_Graph = QAction(parent)
        self.actionManage_Graph.setObjectName("actionManage_Graph")
        self.menuMain.addAction(self.actionEvent_Configuration)
        self.menuMain.addAction(self.actionEnforcement_Action_Report)
        self.menuMain.addAction(self.actionManage_Graph)
        self.menuMain.addAction(self.actionSearch_Filter_Log_Entries)
        self.addAction(self.menuMain.menuAction())

        self.addData(parent)

        if omit == ACTIONREPORT:
            self.actionEnforcement_Action_Report.setDisabled(True)
        if omit == CONFIGURATIONS:
            self.actionEvent_Configuration.setDisabled(True)
        if omit == FILTER:
            self.actionSearch_Filter_Log_Entries.setDisabled(True)
        if omit == GRAPH:
            self.actionManage_Graph.setDisabled(True)

    def addData(self, parent):
        insert = QtCore.QCoreApplication.translate
        parentClassName = parent.objectName()
        self.menuMain.setTitle("Menu")
        self.actionEvent_Configuration.setText(insert(parentClassName, "Event Configuration"))
        self.actionEnforcement_Action_Report.setText(insert(parentClassName, "Enforcement Action Report"))
        self.actionSearch_Filter_Log_Entries.setText(insert(parentClassName, "Filter Logs"))
        self.actionManage_Graph.setText(insert(parentClassName, "Manage Graph"))
