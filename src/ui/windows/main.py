import sys
from ui.windows import search_filter, configurations_window, action_report, graph_window
from PyQt5 import QtCore, QtGui, QtWidgets

class Main_Window(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(400, 340)
        MainWindow.setAutoFillBackground(True)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_5.setObjectName("gridLayout_5")

        # pick icon
        dir = "ui/windows/"
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.img2 = QtWidgets.QLabel(self.centralwidget)
        self.img2.setPixmap(QtGui.QPixmap(dir+"pick.png"))
        self.gridLayout_2.addWidget(self.img2, 0, 0, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_2, 0, 3, 3, 2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem, 0, 5, 1, 1)
        self.formLayout = QtWidgets.QFormLayout()
        self.img1 = QtWidgets.QLabel(self.centralwidget)
        self.img1.setPixmap(QtGui.QPixmap(dir+"pick.png"))

        # Layout of main window
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.img1)
        self.gridLayout_5.addLayout(self.formLayout, 0, 1, 3, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 146, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem1, 3, 3, 2, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 146, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem2, 3, 1, 2, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem3, 0, 0, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(20, 142, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem4, 4, 2, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.app_name = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.app_name.setFont(font)
        self.app_name.setAlignment(QtCore.Qt.AlignCenter)

        # Manage Graph Button
        self.gridLayout_3.addWidget(self.app_name, 0, 0, 1, 1)
        self.manageGraphButton = QtWidgets.QPushButton(self.centralwidget)
        self.manageGraphButton.clicked.connect(self.open_graphWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.manageGraphButton.sizePolicy().hasHeightForWidth())
        self.manageGraphButton.setSizePolicy(sizePolicy)

        # Search/Filter Button
        self.gridLayout_3.addWidget(self.manageGraphButton, 4, 0, 1, 1)
        self.searchFilterButton = QtWidgets.QPushButton(self.centralwidget)
        self.searchFilterButton.clicked.connect(self.open_SearchFilterWindow)

        # Enforcement Action Report Button
        self.gridLayout_3.addWidget(self.searchFilterButton, 3, 0, 1, 1)
        self.actionReportButton = QtWidgets.QPushButton(self.centralwidget)
        self.actionReportButton.clicked.connect(self.open_EAR)

        # Event Configuration Button
        self.gridLayout_3.addWidget(self.actionReportButton, 2, 0, 1, 1)
        self.eventConfigButton = QtWidgets.QPushButton(self.centralwidget)
        self.eventConfigButton.clicked.connect(self.open_configurationsWindow)
        self.gridLayout_3.addWidget(self.eventConfigButton, 1, 0, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_3, 0, 2, 4, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

# Opens Search/Filter Window
    def open_SearchFilterWindow(self):
        self.filterWindow = QtWidgets.QMainWindow()
        search_filter.Search_Filter_Window().setupUi(self.filterWindow)
        self.filterWindow.show()

# Opens Manage Graph Window
    def open_graphWindow(self):
        self.graphWindow = QtWidgets.QMainWindow()
        graph_window.GraphWindow().setupUi(self.graphWindow)
        self.graphWindow.show()

# Opens Event Configuration Window
    def open_configurationsWindow(self):
        self.eventConfigWindow = QtWidgets.QMainWindow()
        configurations_window.ConfigurationsWindow().generateUi(self.eventConfigWindow)
        self.eventConfigWindow.show()

# Opens Enforcement Action Report Window
    def open_EAR(self):
        self.actionReportWindow = QtWidgets.QMainWindow()
        action_report.EARWindow().generateUi(self.actionReportWindow)
        self.actionReportWindow.show()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.app_name.setText(_translate("MainWindow", "PICK Tool"))
        self.manageGraphButton.setText(_translate("MainWindow", "Manage Graph"))
        self.searchFilterButton.setText(_translate("MainWindow", "Search/Filter"))
        self.actionReportButton.setText(_translate("MainWindow", "Enforcement Action Report"))
        self.eventConfigButton.setText(_translate("MainWindow", "Event Configuration"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Main_Window()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
