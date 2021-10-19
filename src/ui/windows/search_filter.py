import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from ui.common import menu_bar
from configuration.configurations import Configuration
from threading import Thread
from ingestion.splunk_interface import SplunkInterface
from ingestion.logentry import LogEntry


class Search_Filter_Window(object):

    def setupUi(self, SearchFilterWindow):
        SearchFilterWindow.setObjectName("SearchFilterWindow")
        SearchFilterWindow.resize(870, 690)

        self.configuration = Configuration.get_instance()

        # Create layouts in this window
        self.mainVerticalView = QtWidgets.QWidget(SearchFilterWindow)
        self.mainVerticalView.setObjectName("mainVerticalView")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.mainVerticalView)
        self.verticalLayout.setObjectName("verticalLayout")
        self.filterConfigurationLayout = QtWidgets.QGroupBox(self.mainVerticalView)
        self.filterConfigurationLayout.setObjectName("filterConfigurationLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.filterConfigurationLayout)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.filterFormLayout = QtWidgets.QFormLayout()
        self.filterFormLayout.setObjectName("filterFormLayout")

        # Add widgets to the filter Form Layout
        self.keywordSearchLabel = QtWidgets.QLabel(self.filterConfigurationLayout)
        self.keywordSearchLabel.setObjectName("keywordSearchLabel")
        self.filterFormLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.keywordSearchLabel)
        self.keywordSearchBox = QtWidgets.QLineEdit(self.filterConfigurationLayout)
        self.keywordSearchBox.setObjectName("keywordSearchBox")
        self.filterFormLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.keywordSearchBox)
        self.creatorLabel = QtWidgets.QLabel(self.filterConfigurationLayout)
        self.creatorLabel.setObjectName("creatorLabel")
        self.filterFormLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.creatorLabel)
        self.creatorWhiteCheck = QtWidgets.QCheckBox(self.filterConfigurationLayout)
        self.creatorWhiteCheck.setObjectName("creatorWhiteCheck")
        self.filterFormLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.creatorWhiteCheck)
        self.creatorRedCheck = QtWidgets.QCheckBox(self.filterConfigurationLayout)
        self.creatorRedCheck.setObjectName("creatorRedCheck")
        self.filterFormLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.creatorRedCheck)
        self.creatorBlueCheck = QtWidgets.QCheckBox(self.filterConfigurationLayout)
        self.creatorBlueCheck.setObjectName("creatorBlueCheck")
        self.filterFormLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.creatorBlueCheck)
        self.eventTypeLabel = QtWidgets.QLabel(self.filterConfigurationLayout)
        self.eventTypeLabel.setObjectName("eventTypeLabel")
        self.filterFormLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.eventTypeLabel)
        self.eventTypeRedCheck = QtWidgets.QCheckBox(self.filterConfigurationLayout)
        self.eventTypeRedCheck.setObjectName("eventTypeRedCheck")
        self.filterFormLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.eventTypeRedCheck)
        self.eventTypeWhiteCheck = QtWidgets.QCheckBox(self.filterConfigurationLayout)
        self.eventTypeWhiteCheck.setObjectName("eventTypeWhiteCheck")
        self.filterFormLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.eventTypeWhiteCheck)
        self.eventTypeBlueCheck = QtWidgets.QCheckBox(self.filterConfigurationLayout)
        self.eventTypeBlueCheck.setObjectName("eventTypeBlueCheck")
        self.filterFormLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.eventTypeBlueCheck)
        self.startTimestampLabel = QtWidgets.QLabel(self.filterConfigurationLayout)
        self.startTimestampLabel.setObjectName("startTimestampLabel")
        self.filterFormLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.startTimestampLabel)
        self.startTimestampEdit = QtWidgets.QDateTimeEdit(self.filterConfigurationLayout)
        self.startTimestampEdit.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.startTimestampEdit.setProperty("showGroupSeparator", False)
        self.startTimestampEdit.setDateTime(QtCore.QDateTime(QtCore.QDate(2020, 1, 1), QtCore.QTime(0, 0, 0)))
        self.startTimestampEdit.setDate(QtCore.QDate(2020, 1, 1))
        self.startTimestampEdit.setCalendarPopup(True)
        self.startTimestampEdit.setCurrentSectionIndex(0)
        self.startTimestampEdit.setObjectName("startTimestampEdit")
        self.filterFormLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.startTimestampEdit)
        self.endTimestampLabel = QtWidgets.QLabel(self.filterConfigurationLayout)
        self.endTimestampLabel.setObjectName("endTimestampLabel")
        self.filterFormLayout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.endTimestampLabel)
        self.endTimestampEdit = QtWidgets.QDateTimeEdit(self.filterConfigurationLayout)
        self.endTimestampEdit.setDate(QtCore.QDate(2020, 1, 1))
        self.endTimestampEdit.setCalendarPopup(True)
        self.endTimestampEdit.setCurrentSectionIndex(0)
        self.endTimestampEdit.setObjectName("endTimestampEdit")
        self.filterFormLayout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.endTimestampEdit)
        self.applyFilterButton = QtWidgets.QPushButton(self.filterConfigurationLayout)
        self.applyFilterButton.setObjectName("applyFilterButton")
        self.filterFormLayout.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.applyFilterButton)
        self.horizontalLayout_3.addLayout(self.filterFormLayout)

        self.verticalLayout2 = QtWidgets.QVBoxLayout()
        self.verticalLayout2.setObjectName("verticalLayout2")
        self.horizontalLayout_3.addLayout(self.verticalLayout2)

        self.filterView = QtWidgets.QTreeWidget(self.filterConfigurationLayout)
        self.filterView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.filterView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.filterView.setAlternatingRowColors(True)
        self.filterView.setHeaderHidden(False)
        self.filterView.setObjectName("searchResultsView")
        self.filterView.setSortingEnabled(True)
        self.filterView.header().setSortIndicatorShown(True)
        self.verticalLayout2.addWidget(self.filterView)

        self.associateButton = QtWidgets.QPushButton(self.filterConfigurationLayout)
        self.associateButton.setObjectName("associateButton")
        self.verticalLayout2.addWidget(self.associateButton)

        # Add vector select combo box and select button
        self.verticalLayout.addWidget(self.filterConfigurationLayout)
        self.vectorViewLayout = QtWidgets.QGroupBox(self.mainVerticalView)
        self.vectorViewLayout.setObjectName("vectorViewLayout")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.vectorViewLayout)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.vectorSelectButtonLayout = QtWidgets.QHBoxLayout()
        self.vectorSelectButtonLayout.setObjectName("vectorSelectButtonLayout")
        self.vectorSelectCombo = QtWidgets.QComboBox(self.vectorViewLayout)
        self.vectorSelectCombo.setObjectName("vectorSelectCombo")
        
        self.vectorSelectCombo.addItem("None")
        self.vectorList = self.configuration.vectors
        for vector in self.vectorList:
            self.vectorSelectCombo.addItem(vector.name)

        self.vectorSelectButtonLayout.addWidget(self.vectorSelectCombo)
        self.vectorSelectConfirmButton = QtWidgets.QPushButton(self.vectorViewLayout)
        self.vectorSelectConfirmButton.setCheckable(False)
        self.vectorSelectConfirmButton.setObjectName("vectorSelectConfirmButton")
        self.vectorSelectButtonLayout.addWidget(self.vectorSelectConfirmButton)
        self.vectorSelectConfirmButton.clicked.connect(lambda: self.insert_log_entry_vector_view(self.vectorSelectCombo.currentText()))

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.vectorSelectButtonLayout.addItem(spacerItem)
        self.verticalLayout_4.addLayout(self.vectorSelectButtonLayout)

        # Add the Tree widget to display selected vector
        self.vectorView = QtWidgets.QTreeWidget(self.vectorViewLayout)
        self.vectorView.setAlternatingRowColors(True)
        self.vectorView.setWordWrap(False)
        self.vectorView.setObjectName("vectorView")
        self.vectorView.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)

        self.vectorView.header().setHighlightSections(False)
        self.verticalLayout_4.addWidget(self.vectorView)
        self.verticalLayout.addWidget(self.vectorViewLayout)
        SearchFilterWindow.setCentralWidget(self.mainVerticalView)

        self.menubar = menu_bar.PickMenuBar(SearchFilterWindow, omit=menu_bar.FILTER)
        SearchFilterWindow.setMenuBar(self.menubar)

        self.addData(SearchFilterWindow)
        QtCore.QMetaObject.connectSlotsByName(SearchFilterWindow)

    def addData(self, SearchFilterWindow):
        configuration = Configuration.get_instance()

        insert = QtCore.QCoreApplication.translate
        SearchFilterWindow.setWindowTitle(insert("SearchFilterWindow", "Search/Filter Log Entries"))

        # Add labels to UI elements
        self.filterConfigurationLayout.setTitle(insert("SearchFilterWindow", "Filter Configuration"))
        self.keywordSearchLabel.setText(insert("SearchFilterWindow", "Keyword search"))
        self.creatorLabel.setText(insert("SearchFilterWindow", "Creator"))
        self.creatorWhiteCheck.setText(insert("SearchFilterWindow", "White"))
        self.creatorRedCheck.setText(insert("SearchFilterWindow", "Red"))
        self.creatorBlueCheck.setText(insert("SearchFilterWindow", "Blue"))
        self.eventTypeLabel.setText(insert("SearchFilterWindow", "Event Type"))
        self.eventTypeRedCheck.setText(insert("SearchFilterWindow", "Red"))
        self.eventTypeWhiteCheck.setText(insert("SearchFilterWindow", "White"))
        self.eventTypeBlueCheck.setText(insert("SearchFilterWindow", "Blue"))
        self.startTimestampLabel.setText(insert("SearchFilterWindow", "Start Timestamp"))
        self.endTimestampLabel.setText(insert("SearchFilterWindow", "End Timestamp"))
        self.applyFilterButton.setText(insert("SearchFilterWindow", "Apply Filter"))
        self.associateButton.setText(insert("SearchFilterWindow", "Associate to Vector"))
        self.associateButton.clicked.connect(lambda: self.associate(self.vectorSelectCombo.currentText()))

        # Add labels to filter view
        self.filterView.setSortingEnabled(True)
        self.filterView.headerItem().setText(0, insert("SearchFilterWindow", "Log ID"))
        self.filterView.headerItem().setText(1, insert("SearchFilterWindow", "Time of Occurance"))
        self.filterView.headerItem().setText(2, insert("SearchFilterWindow", "Description"))
        self.filterView.headerItem().setText(3, insert("SearchFilterWindow", "Log Entry Reference"))
        self.filterView.headerItem().setText(4, insert("SearchFilterWindow", "Log Creator"))
        self.filterView.headerItem().setText(5, insert("SearchFilterWindow", "Action Type"))
        self.filterView.headerItem().setText(6, insert("SearchFilterWindow", "Artifact"))
        __sortingEnabled = self.filterView.isSortingEnabled()
        self.filterView.setSortingEnabled(False)

        # Add sample data to filter view
        messsage = QMessageBox()
        messsage.setWindowTitle("Please wait...")
        messsage.setText("Retrieving log entries from splunk. Log entries might take a sec to load.\n\nClick OK")
        messsage.setIcon(QMessageBox.Information)
        messsage.exec_()
        Thread(target=self.get_log_entries_thread, args=(configuration,)).start()

        self.filterView.setSortingEnabled(__sortingEnabled)
        self.vectorViewLayout.setTitle(insert("SearchFilterWindow", "Vector View"))

        # Add sample options to vector select combo box
        self.vectorSelectConfirmButton.setText(insert("SearchFilterWindow", "Select Vector"))

        # Add labels to vector view
        self.vectorView.setSortingEnabled(True)
        self.vectorView.headerItem().setText(0, insert("SearchFilterWindow", "Log ID"))
        self.vectorView.headerItem().setText(1, insert("SearchFilterWindow", "Time of Occurance"))
        self.vectorView.headerItem().setText(2, insert("SearchFilterWindow", "Description"))
        self.vectorView.headerItem().setText(3, insert("SearchFilterWindow", "Log Entry Reference"))
        self.vectorView.headerItem().setText(4, insert("SearchFilterWindow", "Log Creator"))
        self.vectorView.headerItem().setText(5, insert("SearchFilterWindow", "Action Type"))
        self.vectorView.headerItem().setText(6, insert("SearchFilterWindow", "Artifact"))
        __sortingEnabled = self.vectorView.isSortingEnabled()
        self.vectorView.setSortingEnabled(False)

        self.vectorView.setSortingEnabled(__sortingEnabled)

    # Get log entries from splunk. Use a thread because this can take a while.
    def get_log_entries_thread(self, configuration):
        if configuration.splunk:
            self.all_log_entries = configuration.splunk.get_log_entries()
            self.insert_log_entry_search_data(self.all_log_entries)

    # Insert the list of log entries to the search results
    def insert_log_entry_search_data(self, log_entries):
        insert = QtCore.QCoreApplication.translate
        # Add empty spaces to Search Results view to enter sample data
        for i in range(len(log_entries)):
            QtWidgets.QTreeWidgetItem(self.filterView)

        # add actual data
        for i in range(len(log_entries)):
            self.filterView.topLevelItem(i).setText(0, insert("SearchFilterWindow", log_entries[i].id))
            self.filterView.topLevelItem(i).setText(1, insert("SearchFilterWindow", log_entries[i].time))
            self.filterView.topLevelItem(i).setText(2, insert("SearchFilterWindow", log_entries[i].data))
            self.filterView.topLevelItem(i).setText(3, insert("SearchFilterWindow", log_entries[i].source_file))
            self.filterView.topLevelItem(i).setText(4, insert("SearchFilterWindow", "-"))
            self.filterView.topLevelItem(i).setText(5, insert("SearchFilterWindow", "-"))
            self.filterView.topLevelItem(i).setText(6, insert("SearchFilterWindow", "-"))

    # Insert associated log entries from a vector
    def insert_log_entry_vector_view(self, vector_name):
        self.vectorView.clear()
        selectedVector = None
        for vector in self.configuration.vectors:
            if vector.name == vector_name:
                selectedVector = vector
        if selectedVector is None:
            return
        insert = QtCore.QCoreApplication.translate

        # add actual data
        for i in range(len(selectedVector.log_entries)):
            item_to_insert = QtWidgets.QTreeWidgetItem(self.vectorView)
            item_to_insert.setText(0, insert("SearchFilterWindow", selectedVector.log_entries[i].id))
            item_to_insert.setText(1, insert("SearchFilterWindow", selectedVector.log_entries[i].time))
            item_to_insert.setText(2, insert("SearchFilterWindow", selectedVector.log_entries[i].data))
            item_to_insert.setText(3, insert("SearchFilterWindow", selectedVector.log_entries[i].source_file))
            item_to_insert.setText(4, insert("SearchFilterWindow", "-"))
            item_to_insert.setText(5, insert("SearchFilterWindow", "-"))
            item_to_insert.setText(6, insert("SearchFilterWindow", "-"))
            self.vectorView.addTopLevelItem(item_to_insert)

    # Associate the selected log entry to the vector with the given name.
    def associate(self, vector_name):
        selected_vector = None
        for vector in self.configuration.vectors:
            if vector.name == vector_name:
                selected_vector = vector
        if selected_vector is None:
            return
        # associate logic
        selected_items = self.filterView.selectedItems()
        for log_entry in selected_items:
            print("SELECTED ITEM " + log_entry.text(0) + " " + log_entry.text(2) + " " + log_entry.text(1))
            selected_vector.add_log_entry(LogEntry(log_entry.text(0), log_entry.text(2), log_entry.text(1), "", log_entry.text(3), ""))
        self.insert_log_entry_vector_view(vector_name)

    # Replace displayed log search results with filtered results
    def filter(self):
        # Get all the entered criteria
        entered_keyword = self.keywordSearchBox.text()
        creator_white = self.creatorWhiteCheck.isChecked()
        creator_red = self.creatorRedCheck.isChecked()
        creator_blue = self.creatorBlueCheck.isChecked()
        event_red = self.eventTypeRedCheck.isChecked()
        event_white = self.eventTypeWhiteCheck.isChecked()
        event_blue = self.eventTypeBlueCheck.isChecked()
        start_time = self.startTimestampEdit.text()
        ent_time = self.endTimestampEdit.text()

        # Display filtered log entries


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    SearchFilterWindow = QtWidgets.QMainWindow()
    ui = Search_Filter_Window()
    ui.setupUi(SearchFilterWindow)
    SearchFilterWindow.show()
    sys.exit(app.exec_())
