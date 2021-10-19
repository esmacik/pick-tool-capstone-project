import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from ui.common import menu_bar
from configuration.configurations import Configuration
from threading import Thread
from ingestion.splunk_interface import SplunkInterface


class EARWindow(object):
    app = QtWidgets.QApplication([])
    app.setStyle('Fusion')

    def generateUi(self, actionReportWindow):
        actionReportWindow.setObjectName("actionReportWindow")
        # row, column
        actionReportWindow.resize(2500, 950)
        actionReportWindow.setAutoFillBackground(False)

        self.windowBackground = QtWidgets.QWidget(actionReportWindow)
        self.windowBackground.setObjectName("windowBackground")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.windowBackground)
        self.verticalLayout.setObjectName("verticalLayout")
        # action report table properties
        self.reportTableTitle = QtWidgets.QGroupBox(self.windowBackground)
        self.reportTableTitle.setObjectName("reportTableTitle")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.reportTableTitle)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.reportTable = QtWidgets.QTreeWidget(self.reportTableTitle)
        self.reportTable.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.reportTable.setDefaultDropAction(QtCore.Qt.ActionMask)
        # seperates the rows with grey coloring
        self.reportTable.setAlternatingRowColors(True)
        self.reportTable.setRootIsDecorated(True)
        self.reportTable.setHeaderHidden(False)
        self.reportTable.setObjectName("reportTable")
        
        # creating space to add data later
        for i in range(4):
            QtWidgets.QTreeWidgetItem(self.reportTable)
       

        # changes the header space in between (like log file from source path)
        self.reportTable.header().setDefaultSectionSize(350)
        self.reportTable.header().setHighlightSections(True)

        # gives action report table the vertical layout
        self.verticalLayout_3.addWidget(self.reportTable)
        self.verticalLayout.addWidget(self.reportTableTitle)

        # selected log file table properties (Error Description table)
        self.selectedLogFile = QtWidgets.QGroupBox(self.windowBackground)
        self.selectedLogFile.setObjectName("selectedLogFile")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.selectedLogFile)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.errorDescription = QtWidgets.QTreeWidget(self.selectedLogFile)
        self.errorDescription.setEnabled(True)
        # seperates the rows with grey coloring
        self.errorDescription.setAlternatingRowColors(True)
        self.errorDescription.setUniformRowHeights(False)
        # option to hide header or keep it 
        self.errorDescription.setHeaderHidden(False)
        # can expand table on double click
        self.errorDescription.setExpandsOnDoubleClick(False)
        # errorDescription is the name of the table object
        self.errorDescription.setObjectName("errorDescription")
        
        # creating space to add data later
        for i in range(5):
            QtWidgets.QTreeWidgetItem(self.errorDescription)
        
        # option to hide header or keep it 
        self.errorDescription.header().setVisible(True)
        # changes the table to move along with the cursor. (like the override button)
        self.errorDescription.header().setCascadingSectionResizes(True)
        
        # changes the header space in between (like log file from source path)
        self.errorDescription.header().setDefaultSectionSize(450)
        self.errorDescription.header().setHighlightSections(False)
        # gives the error description table the vertical layout
        self.verticalLayout_2.addWidget(self.errorDescription)
        self.verticalLayout.addWidget(self.selectedLogFile)

        # creating an expand button at the bottom of the 2 tables
        self.validateButton = QtWidgets.QPushButton(self.windowBackground)
        self.validateButton.setObjectName("validateButton")
        self.verticalLayout.addWidget(self.validateButton)

        # creating an override button at the bottom of the 2 tables
        self.cancelButton = QtWidgets.QPushButton(self.windowBackground)
        self.cancelButton.setObjectName("cancelButton")
        self.verticalLayout.addWidget(self.cancelButton)
    

        actionReportWindow.setCentralWidget(self.windowBackground)
        # this is creating the menu bar options
        self.menubar = menu_bar.PickMenuBar(actionReportWindow, omit=menu_bar.ACTIONREPORT)
        actionReportWindow.setMenuBar(self.menubar)

        # adds the data to the window
        self.addData(actionReportWindow)
        
        # whenever an item is pressed in the action report table, hide the error description table.
        #self.reportTable.itemPressed['QTreeWidgetItem*','int'].connect(self.errorDescription.expandAll)
        
        # whenever the override button is pressed, hide the error description table.
        self.cancelButton.pressed.connect(self.selectedLogFile.hide)

        # whenever an item is pressed in the action report table, hide the error description table.
        #self.reportTable.itemPressed['QTreeWidgetItem*','int'].connect(self.errorDescription.expandAll)
        
        # whenever the expand button is pressed, expand the error description table.
        self.validateButton.pressed.connect(self.selectedLogFile.show)

        QtCore.QMetaObject.connectSlotsByName(actionReportWindow)
        # sets the tab order for the user
        actionReportWindow.setTabOrder(self.reportTable, self.errorDescription)
        actionReportWindow.setTabOrder(self.errorDescription, self.cancelButton)

    def addData(self, actionReportWindow):
        insert = QtCore.QCoreApplication.translate
        actionReportWindow.setWindowTitle(insert("actionReportWindow", "Log Configuration"))
        # Filling in the action report headers
        self.reportTableTitle.setTitle(insert("actionReportWindow", "Enforcement Action Report"))
        self.reportTable.headerItem().setText(0, insert("actionReportWindow", "Log File"))
        self.reportTable.headerItem().setText(1, insert("actionReportWindow", "Source Path"))
        self.reportTable.headerItem().setText(2, insert("actionReportWindow", "Cleansing Status"))
        self.reportTable.headerItem().setText(3, insert("actionReportWindow", "Validation Status"))
        self.reportTable.headerItem().setText(4, insert("actionReportWindow", "Ingestion Status"))
        __sortingEnabled = self.reportTable.isSortingEnabled()
        self.reportTable.setSortingEnabled(False)
        # Filling in the table contents 

        #self.reportTable.topLevelItem(0).setText(0, insert("actionReportWindow", log_entries[i].logs))
        #self.reportTable.topLevelItem(0).setText(1, insert("actionReportWindow", log_entries[i].source_file))
        self.reportTable.topLevelItem(0).setText(2, insert("actionReportWindow", "+"))
        self.reportTable.topLevelItem(0).setText(3, insert("actionReportWindow", "+"))
        self.reportTable.topLevelItem(0).setText(4, insert("actionReportWindow", "+"))
        #self.reportTable.topLevelItem(1).setText(0, insert("actionReportWindow", "Log File 2"))
        #self.reportTable.topLevelItem(1).setText(1, insert("actionReportWindow", "/path/incident_report.pd"))
        #self.reportTable.topLevelItem(1).setText(2, insert("actionReportWindow", "+"))
        #self.reportTable.topLevelItem(1).setText(3, insert("actionReportWindow", "-"))
        #self.reportTable.topLevelItem(1).setText(4, insert("actionReportWindow", "-"))
        #self.reportTable.topLevelItem(2).setText(0, insert("actionReportWindow", "Log File 3"))
        #self.reportTable.topLevelItem(2).setText(1, insert("actionReportWindow", "/path/observer_notes.osv"))
        #self.reportTable.topLevelItem(2).setText(2, insert("actionReportWindow", "+"))
        #self.reportTable.topLevelItem(2).setText(3, insert("actionReportWindow", "+"))
        #self.reportTable.topLevelItem(2).setText(4, insert("actionReportWindow", "+"))
        #self.reportTable.topLevelItem(3).setText(0, insert("actionReportWindow", "Log File 4"))
        #self.reportTable.topLevelItem(3).setText(1, insert("actionReportWindow", "/path/incident_report.pd"))
        #self.reportTable.topLevelItem(3).setText(2, insert("actionReportWindow", "-"))
        #self.reportTable.topLevelItem(3).setText(3, insert("actionReportWindow", "-"))
        #self.reportTable.topLevelItem(3).setText(4, insert("actionReportWindow", "-"))
        #self.reportTable.setSortingEnabled(__sortingEnabled)

        # hardcoding the error description title
        self.selectedLogFile.setTitle(insert("actionReportWindow", "Log File 2"))
        # naming the error description headers
        self.errorDescription.headerItem().setText(0, insert("actionReportWindow", "Line Number"))
        self.errorDescription.headerItem().setText(1, insert("actionReportWindow", "Error Description"))

        __sortingEnabled = self.errorDescription.isSortingEnabled()
        self.errorDescription.setSortingEnabled(False)
        # adding information to the error description table
        self.errorDescription.topLevelItem(0).setText(0, insert("actionReportWindow", "0-001"))
        self.errorDescription.topLevelItem(0).setText(1, insert("actionReportWindow", "Time is invalid format...."))
        self.errorDescription.topLevelItem(1).setText(0, insert("actionReportWindow", "0-009"))
        self.errorDescription.topLevelItem(1).setText(1, insert("actionReportWindow", "No date is found ...."))
        self.errorDescription.topLevelItem(2).setText(0, insert("actionReportWindow", "0-015"))
        self.errorDescription.topLevelItem(2).setText(1, insert("actionReportWindow", "Date is in invalid format...."))
        self.errorDescription.topLevelItem(3).setText(0, insert("actionReportWindow", "0-026"))
        self.errorDescription.topLevelItem(3).setText(1, insert("actionReportWindow", "Time is invalid format...."))
        self.errorDescription.topLevelItem(4).setText(0, insert("actionReportWindow", "0-099"))
        self.errorDescription.topLevelItem(4).setText(1, insert("actionReportWindow", "No date is found ...."))
        self.errorDescription.setSortingEnabled(__sortingEnabled)
        # adding data to the buttons. (Filling them in)
        self.cancelButton.setText(insert("actionReportWindow", "Cancel Selected Log File"))
        self.validateButton.setText(insert("actionReportWindow", "Validate Selected Log File"))

        configuration = Configuration.get_instance()
        if configuration.splunk != None:
            all_log_entries = configuration.splunk.get_log_entries()
            self.insert_log_entry_search_data(all_log_entries)    

    def get_log_entries_thread(self, configuration):
        if configuration.splunk:
            all_log_entries = configuration.splunk.get_log_entries()
            self.insert_log_entry_search_data(all_log_entries)

    def insert_log_entry_search_data(self, log_entries):
        insert = QtCore.QCoreApplication.translate
        # makes it display all of the log files by using (i) inside the topLevelItem.
        for i in range(len(log_entries)):
            QtWidgets.QTreeWidgetItem(self.reportTable)
            QtWidgets.QTreeWidgetItem(self.errorDescription)

        # adding the actual data to action report
        for i in range(len(log_entries)):
            self.reportTable.topLevelItem(i).setText(0, insert("actionReportWindow", log_entries[i].id))            
            self.reportTable.topLevelItem(i).setText(1, insert("actionReportWindow", log_entries[i].source_file))
            self.reportTable.topLevelItem(i).setText(2, insert("actionReportWindow", "+"))
            self.reportTable.topLevelItem(i).setText(3, insert("actionReportWindow", "-"))
            self.reportTable.topLevelItem(i).setText(4, insert("actionReportWindow", "-"))

        # fills in the error description
            self.errorDescription.topLevelItem(i).setText(0, insert("actionReportWindow", log_entries[i].id))
            self.errorDescription.topLevelItem(i).setText(1, insert("actionReportWindow", log_entries[i].data))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    actionReportWindow = QtWidgets.QMainWindow()
    ui = EARWindow()
    ui.generateUi(actionReportWindow)
    actionReportWindow.show()
    sys.exit(app.exec_())
