from ui.windows import search_filter, configurations_window, action_report, graph_window
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QFileDialog, QDialog, QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QFormLayout, QComboBox, QDateTimeEdit, QPushButton, QInputDialog, QLineEdit, QTextEdit, QLabel
import sys
import os
import json
sys.path.insert(1,os.path.dirname(__file__)+"/..")

from QGraphViz.QGraphViz import QGraphViz, QGraphVizManipulationMode
from QGraphViz.DotParser import Graph, GraphType, Node, Edge, DotParser
from QGraphViz.DotParser.Graph import Graph
from QGraphViz.DotParser.Node import Node
from QGraphViz.DotParser.Edge import Edge
from QGraphViz.Engines import Dot

from configuration.configurations import Configuration


class GraphWindow(object):
    def setupUi(self, graphWindow):
        self.graphWin = graphWindow.setObjectName("graphWindow")
        graphWindow.setObjectName("graphWindow")
        graphWindow.resize(1155, 895)
        graphWindow.setDockNestingEnabled(True)
        self.centralwidget = QtWidgets.QWidget(graphWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.configuration = Configuration.get_instance()

        #*-----------------------vector selection objects------------------------------------------------*#

        self.groupBoxVectorSelection = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxVectorSelection.sizePolicy().hasHeightForWidth())
        self.groupBoxVectorSelection.setSizePolicy(sizePolicy)
        self.groupBoxVectorSelection.setObjectName("groupBoxVectorSelection")
        self.gridLayout.addWidget(self.groupBoxVectorSelection, 0, 0, 1, 1)
        self.formLayoutVector = QtWidgets.QHBoxLayout(self.groupBoxVectorSelection)
        self.formLayoutVector.setObjectName("formLayoutVector")
        
        #vector label
        self.labelVector = QtWidgets.QLabel(self.groupBoxVectorSelection)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelVector.sizePolicy().hasHeightForWidth())
        self.labelVector.setSizePolicy(sizePolicy)
        self.labelVector.setObjectName("labelVector")
        self.formLayoutVector.addWidget(self.labelVector) 

        #vector combo box
        self.comboBoxVector = QtWidgets.QComboBox(self.groupBoxVectorSelection)
        self.comboBoxVector.setMinimumSize(QtCore.QSize(150, 0))
        self.comboBoxVector.setMaximumSize(QtCore.QSize(69, 16777215))
        self.comboBoxVector.setObjectName("comboBoxVector")
        self.formLayoutVector.addWidget(self.comboBoxVector)

        self.comboBoxVector.addItem("None")
        self.vectorList = Configuration.get_list_of_vector_dicts(self.configuration)
        for vector in self.vectorList:
            self.comboBoxVector.addItem(vector["name"])

        #vector description label
        self.labelVectorDesc = QtWidgets.QLabel(self.groupBoxVectorSelection)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelVectorDesc.sizePolicy().hasHeightForWidth())
        self.labelVectorDesc.setSizePolicy(sizePolicy)
        self.labelVectorDesc.setObjectName("labelVectorDesc")
        self.formLayoutVector.addWidget(self.labelVectorDesc)

        #vector description line edit
        self.lineEditVectorDesc = QtWidgets.QLineEdit(self.groupBoxVectorSelection)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditVectorDesc.sizePolicy().hasHeightForWidth())
        self.lineEditVectorDesc.setSizePolicy(sizePolicy)
        self.lineEditVectorDesc.setReadOnly(True)
        self.lineEditVectorDesc.setObjectName("lineEditVectorDesc")
        self.formLayoutVector.addWidget(self.lineEditVectorDesc)
        self.comboBoxVector.currentTextChanged.connect(lambda: self.changeVector())


        #*----------------------multi-document-area---------------------------------------------------------------*#
        self.mdiArea = QtWidgets.QMdiArea(self.centralwidget)
        self.mdiArea.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.mdiArea.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.mdiArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.mdiArea.setActivationOrder(QtWidgets.QMdiArea.ActivationHistoryOrder)
        self.mdiArea.setViewMode(QtWidgets.QMdiArea.SubWindowView)
        self.mdiArea.setDocumentMode(False)
        self.mdiArea.setTabsClosable(False)
        self.mdiArea.setTabsMovable(True)
        self.mdiArea.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.mdiArea.setTabPosition(QtWidgets.QTabWidget.North)
        self.mdiArea.setObjectName("mdiArea")


    #*-------------------------Graph Subwindow------------------------------------------------------------------*#

        self.subwindow_Graph = QtWidgets.QWidget()
        self.subwindow_Graph.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.subwindow_Graph.setObjectName("subwindow_Graph")

        self.gridLayout_3 = QtWidgets.QGridLayout(self.subwindow_Graph)
        self.gridLayout_3.setObjectName("gridLayout_3")
        
        # Interval Label and combo box
        self.IntervalLabel = QtWidgets.QLabel(self.subwindow_Graph)
        self.IntervalLabel.setObjectName("IntervalLabel")
        self.gridLayout_3.addWidget(self.IntervalLabel, 2, 1, 1, 1, QtCore.Qt.AlignRight)
        self.Interval = QtWidgets.QComboBox(self.subwindow_Graph)
        self.Interval.setObjectName("Interval")
        self.Interval.addItem("") # Select Interval
        self.Interval.addItem("") # Seconds
        self.Interval.addItem("") # Minutes 
        self.Interval.addItem("") # Hours
        self.gridLayout_3.addWidget(self.Interval, 2, 2, 1, 1)

        #Timeline orientation label and combo box
        self.TimelineOrientationLabel = QtWidgets.QLabel(self.subwindow_Graph)
        self.TimelineOrientationLabel.setObjectName("TimelineOrientationLabel")
        self.gridLayout_3.addWidget(self.TimelineOrientationLabel, 2, 3, 1, 1, QtCore.Qt.AlignRight)
        self.TimelineOrientation = QtWidgets.QComboBox(self.subwindow_Graph)
        self.TimelineOrientation.setObjectName("TimelineOrientation")
        self.TimelineOrientation.addItem("") # Selection Orientation
        self.TimelineOrientation.addItem("") # Horizontal
        self.TimelineOrientation.addItem("") # Vertical
        self.gridLayout_3.addWidget(self.TimelineOrientation, 2, 4, 1, 1)

        self.newRelationshipFlag = False
        # Events
        def node_selected(node):
            if(self.qgv.manipulation_mode==QGraphVizManipulationMode.Node_remove_Mode):
                print("Node {} removed".format(node))
                removeNode(node)
            else:
                print("Node selected {}".format(node))
                if(self.newRelationshipFlag == True):
                    update_json(node)
                    self.newRelationshipFlag = False

        def edge_selected(edge):
            if(self.qgv.manipulation_mode==QGraphVizManipulationMode.Edge_remove_Mode):
                print("Edge {} removed".format(edge))
                removeRelationship(edge)
            else:
                print("Edge selected {}".format(edge))

        def node_invoked(node):
            print("Node double clicked")
        def edge_invoked(node):
            print("Edge double clicked")
        def node_removed(node):
            print("Node removed")
        def edge_removed(node):
            print("Edge removed")

        # Create QGraphViz graph widget
        show_subgraphs=True
        self.qgv = QGraphViz(
            show_subgraphs=show_subgraphs,
            
            node_selected_callback=node_selected,
            edge_selected_callback=edge_selected,
            node_invoked_callback=node_invoked,
            edge_invoked_callback=edge_invoked,
            node_removed_callback=node_removed,
            edge_removed_callback=edge_removed,

            hilight_Nodes=True,
            hilight_Edges=True

        )

        self.nodeId = 0
        self.relationshipId = 0
        f = open('ui/windows/graph.json', 'r+')
        f.truncate(0)
        
        self.qgv.setStyleSheet("background-color:white;")

        # Create A new Graph using Dot layout engine
        self.qgv.new(Dot(Graph("Main_Graph"), show_subgraphs=show_subgraphs))


        # Build the graph (the layout engine organizes where the nodes and connections are)
        self.qgv.build()
        # Save it to a file to be loaded by Graphviz if needed
        self.qgv.save("test.gv")
        

        # Create a widget to handle the QGraphViz object
        graphWidget=QWidget()
        graphWidget.setLayout(QVBoxLayout())
        self.gridLayout_3.addWidget(graphWidget, 3, 0, 1, 6)
        # Add the QGraphViz object to the layout
        graphWidget.layout().addWidget(self.qgv)
        

        #Buttons Functionality
        def manipulate():
            self.qgv.manipulation_mode=QGraphVizManipulationMode.Nodes_Move_Mode

        #export as a CSV file
        def save():
            fname = QFileDialog.getSaveFileName(self.qgv, "Save", "", "*.csv")
            if(fname[0]!=""):
                self.qgv.save(fname[0])
                print(fname[0])
  

            #fname = QFileDialog.getSaveFileName(self.qgv, "Save", "", "*.gv")
            #if(fname[0]!=""):
            #    self.qgv.save(fname[0])
            
        def new():
            self.qgv.engine.graph = Graph("MainGraph")
            self.qgv.build()
            self.qgv.repaint()

            #clear all data from nodes table widget
            rowCount = self.tableWidgetNodes.rowCount()
            for x in range(1, rowCount):
                self.tableWidgetNodes.removeRow(x)
            self.tableWidgetNodes.removeRow(1)
            
            #clear all data from relationships table widget
            rowCount = self.tableWidgetRelationships.rowCount()
            for x in range(rowCount):
                self.tableWidgetRelationships.removeRow(x)

            #update json file
            fname = "ui/windows/graph.json"
            self.qgv.saveAsJson(fname)

        def load():
            fname = QFileDialog.getOpenFileName(self.qgv, "Open", "", "*.csv")
            if(fname[0]!=""):
                self.qgv.load_file(fname[0])

            #populate json file with new graph   
            fname = "ui/windows/graph.json"
            self.qgv.saveAsJson(fname)

            #open json file and load data
            with open('ui/windows/graph.json') as json_file:
                data = json.load(json_file)

            #iterate through each node and add it to the nodes table widget
            nodesData = data["nodes"]
            for node in nodesData:
                self.addNewNode(self.tableWidgetNodes, node["kwargs"]["id"], node["kwargs"]["label"], node["kwargs"]["timestamp"], node["kwargs"]["description"], node["kwargs"]["leReference"], node["kwargs"]["creator"], node["kwargs"]["shape"], node["kwargs"]["leSource"])

            #iterate through each edge and add it to the relationships table widget
            relationshipsData = data["edges"]
            for edge in relationshipsData:
                try:
                    label = edge["kwargs"]["label"]
                except KeyError:
                    label = ""
                self.addTableData(self.tableWidgetRelationships, label, edge["source"], edge["dest"])


        def add_node():


            #add node dialog
            addNodeDialog = QDialog()
            addNodeDialog.ok=False
            addNodeDialog.node_name=""
            addNodeDialog.node_label=""
            addNodeDialog.node_timestamp=""
            addNodeDialog.node_description=""
            addNodeDialog.node_logEntryReference=""
            addNodeDialog.node_logCreator=""
            addNodeDialog.node_logEntrySource=""
            addNodeDialog.node_type="None"

            # Layouts
            main_layout = QVBoxLayout()
            addNodeLayout = QFormLayout()
            buttons_layout = QHBoxLayout()
            
            main_layout.addLayout(addNodeLayout)
            main_layout.addLayout(buttons_layout)
            addNodeDialog.setLayout(main_layout)

            #line edits
            leNodeName = QLineEdit()
            leNodeLabel = QLineEdit()
            teNodeDescription = QTextEdit()
            dtNodeTimestamp = QDateTimeEdit()
            dtNodeTimestamp.setDate(QtCore.QDate(2020, 1, 1))
            dtNodeTimestamp.setCalendarPopup(True)
            leLogEntryReference = QLineEdit()
            cbxLogCreator = QComboBox()
            leLogEntrySource = QLineEdit()
            cbxNodeType = QComboBox()
            cbxImage = QComboBox()

            #buttons
            pbOK = QPushButton()
            pbCancel = QPushButton()


            cbxNodeType.addItems(["None","circle","box"])
            cbxLogCreator.addItems(["None","Red","Blue", "White"])
            cbxImage.addItem("None")
            self.iconList = Configuration.get_list_of_icon_dicts(self.configuration)
            for icon in self.iconList:
                cbxImage.addItem(icon["name"])
            pbOK.setText("&OK")
            pbCancel.setText("&Cancel")



            addNodeLayout.setWidget(0, QFormLayout.LabelRole, QLabel("Node Name"))
            addNodeLayout.setWidget(0, QFormLayout.FieldRole, leNodeName)
            addNodeLayout.setWidget(1, QFormLayout.LabelRole, QLabel("Node Description"))
            addNodeLayout.setWidget(1, QFormLayout.FieldRole, teNodeDescription)
            addNodeLayout.setWidget(2, QFormLayout.LabelRole, QLabel("Node Timestamp"))
            addNodeLayout.setWidget(2, QFormLayout.FieldRole, dtNodeTimestamp)
            addNodeLayout.setWidget(3, QFormLayout.LabelRole, QLabel("Log Entry Reference"))
            addNodeLayout.setWidget(3, QFormLayout.FieldRole, leLogEntryReference)
            addNodeLayout.setWidget(4, QFormLayout.LabelRole, QLabel("Log Creator"))
            addNodeLayout.setWidget(4, QFormLayout.FieldRole, cbxLogCreator)
            addNodeLayout.setWidget(5, QFormLayout.LabelRole, QLabel("Log Entry Source"))
            addNodeLayout.setWidget(5, QFormLayout.FieldRole, leLogEntrySource)
            addNodeLayout.setWidget(6, QFormLayout.LabelRole, QLabel("Node Type"))
            addNodeLayout.setWidget(6, QFormLayout.FieldRole, cbxNodeType)
            addNodeLayout.setWidget(7, QFormLayout.LabelRole, QLabel("Node Image"))
            addNodeLayout.setWidget(7, QFormLayout.FieldRole, cbxImage)

            #ok button handler
            def ok():
                addNodeDialog.OK=True
                addNodeDialog.node_name = leNodeName.text()
                addNodeDialog.node_label = leNodeName.text()
                addNodeDialog.node_timestamp= dtNodeTimestamp.text()
                addNodeDialog.node_description= teNodeDescription.toPlainText()
                addNodeDialog.node_logEntryReference = leLogEntryReference.text()
                addNodeDialog.node_logCreator= cbxLogCreator.currentText()
                addNodeDialog.node_logEntrySource= leLogEntrySource.text()
                if(cbxImage.currentText()): 
                    for icon in self.iconList:
                        if(cbxImage.currentText() == icon["name"]):
                            addNodeDialog.node_type = icon["source"]
                else: 
                    addNodeDialog.node_type = cbxNodeType.currentText()
                addNodeDialog.close()

            #cancel button handler
            def cancel():
                addNodeDialog.OK=False
                addNodeDialog.close()

            pbOK.clicked.connect(ok)
            pbOK.clicked.connect(lambda: self.addNewNode(self.tableWidgetNodes, str(self.nodeId), leNodeName.text(), dtNodeTimestamp.text(), teNodeDescription.toPlainText(), leLogEntryReference.text(), cbxLogCreator.currentText(), addNodeDialog.node_type, leLogEntrySource.text()))
            pbCancel.clicked.connect(cancel)

            buttons_layout.addWidget(pbOK)
            buttons_layout.addWidget(pbCancel)
            addNodeDialog.exec_()

            
            if addNodeDialog.OK and addNodeDialog.node_name != '':
                self.qgv.addNode(self.qgv.engine.graph, addNodeDialog.node_name, id=str(self.nodeId), label=addNodeDialog.node_label, description=addNodeDialog.node_description , timestamp=addNodeDialog.node_timestamp, leReference= addNodeDialog.node_logEntryReference, creator=addNodeDialog.node_logCreator, leSource=addNodeDialog.node_logEntrySource, shape=addNodeDialog.node_type)
                self.qgv.build()
                self.nodeId += 1
                    

        #remove node button event
        def rem_node():
            self.qgv.manipulation_mode=QGraphVizManipulationMode.Node_remove_Mode
            for btn in buttons_list:
                btn.setChecked(False)
            btnRemNode.setChecked(True)

        #remove edge button event
        def rem_edge():
            self.qgv.manipulation_mode=QGraphVizManipulationMode.Edge_remove_Mode
            for btn in buttons_list:
                btn.setChecked(False)
            btnRemEdge.setChecked(True)

        #add edge button event
        def add_edge():
            self.qgv.manipulation_mode=QGraphVizManipulationMode.Edges_Connect_Mode
            for btn in buttons_list:
                btn.setChecked(False)
            btnAddEdge.setChecked(True)
            self.newRelationshipFlag = True
            
        #updates json file with all graph properties (nodes & edges)
        def update_json(item):
            fname = "ui/windows/graph.json"
            self.qgv.saveAsJson(fname)
            addRelationshipToTable()

        #remove node from node table widget
        def removeNode(node):
            fname = "ui/windows/graph.json"
            self.qgv.saveAsJson(fname)
            self.row = getNodeRowNumber(self.tableWidgetNodes, node.name)
            self.tableWidgetNodes.removeRow(self.row)
      
        #remove relationship from relationship table widget
        def removeRelationship(edge):
            fname = "ui/windows/graph.json"
            self.qgv.saveAsJson(fname)
            self.row = getEdgeRowNumber(self.tableWidgetRelationships, edge.source.name, edge.dest.name)
            self.tableWidgetRelationships.removeRow(self.row)

        #return row number for given node
        def getNodeRowNumber(widget,nodeName):
            rowCount = widget.rowCount()
            for x in range(rowCount):
                node = widget.item(x, 2).text()
                if node == nodeName:
                    return x

        #return row number for given edge
        def getEdgeRowNumber(widget,edgeSource, edgeDestination):
            rowCount = widget.rowCount()
            for x in range(rowCount):
                edgeSrc = widget.item(x, 2).text()
                edgeDest = widget.item(x, 3).text()
                if edgeSrc == edgeSource and edgeDest == edgeDestination:
                    return x
        
        #add new relationship from graph onto relationship table
        def addRelationshipToTable():
            with open('ui/windows/graph.json') as json_file:
                data = json.load(json_file)

            self.index = len(data['edges']) - 1

            #new table widget item
            self.tableWidgetRelationships.insertRow(0)
            item = QtWidgets.QTableWidgetItem()
            item.setCheckState(QtCore.Qt.Unchecked)
            item.setFlags(QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            self.tableWidgetRelationships.setItem(0, 0, item)
            
            #write data on table widget in corresponding cells
            insert = QtCore.QCoreApplication.translate
            item = self.tableWidgetRelationships.item(0, 0)
            item.setText(insert("GraphWindow", str(self.relationshipId)))
            self.tableWidgetRelationships.setItem(0, 2, QtWidgets.QTableWidgetItem(data["edges"][self.index]["source"]))
            self.tableWidgetRelationships.setItem(0, 3, QtWidgets.QTableWidgetItem(data["edges"][self.index]["dest"]))

            self.relationshipId += 1


        
        # Add two horizontal layouts (pannels to hold buttons)
        hpanelTop=QHBoxLayout()
        graphWidget.layout().addLayout(hpanelTop)

        hpanelBottom=QHBoxLayout()
        graphWidget.layout().addLayout(hpanelBottom)

        # Add buttons 
        btnNew = QPushButton("New")    
        btnNew.clicked.connect(new)
        hpanelTop.addWidget(btnNew) 

        btnOpen = QPushButton("Open")    
        btnOpen.clicked.connect(load)
        hpanelTop.addWidget(btnOpen)

        btnSave = QPushButton("Export")    
        btnSave.clicked.connect(save)
        hpanelTop.addWidget(btnSave)

        
        buttons_list=[]
        btnManip = QPushButton("Manipulate")    
        btnManip.setCheckable(True)
        btnManip.setChecked(True)
        btnManip.clicked.connect(manipulate)
        hpanelTop.addWidget(btnManip)
        buttons_list.append(btnManip)

        btnAddNode = QPushButton("Add Node")    
        btnAddNode.clicked.connect(add_node)
        hpanelBottom.addWidget(btnAddNode)
        buttons_list.append(btnManip)

        btnRemNode = QPushButton("Rem Node")    
        btnRemNode.setCheckable(True)
        btnRemNode.clicked.connect(rem_node)
        hpanelBottom.addWidget(btnRemNode)
        buttons_list.append(btnRemNode)

        btnAddEdge = QPushButton("Add Relationship")    
        btnAddEdge.setCheckable(True)
        btnAddEdge.clicked.connect(add_edge)
        hpanelBottom.addWidget(btnAddEdge)
        buttons_list.append(btnAddEdge)

        btnRemEdge = QPushButton("Rem Relationship")    
        btnRemEdge.setCheckable(True)
        btnRemEdge.clicked.connect(rem_edge)
        hpanelBottom.addWidget(btnRemEdge)
        buttons_list.append(btnRemEdge)
       

    #*-------------------------Tabular View Subwindow------------------------------------------------------------------*#

        self.subwindow_Table = QtWidgets.QWidget()
        self.subwindow_Table.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.subwindow_Table.setObjectName("subwindow_Table")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.subwindow_Table)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        #table widget
        self.tableWidgetNodes = QtWidgets.QTableWidget(self.subwindow_Table)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidgetNodes.sizePolicy().hasHeightForWidth())
        self.tableWidgetNodes.setSizePolicy(sizePolicy)
        self.tableWidgetNodes.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tableWidgetNodes.setFrameShape(QtWidgets.QFrame.Box)
        self.tableWidgetNodes.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.tableWidgetNodes.setAlternatingRowColors(True)
        self.tableWidgetNodes.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.tableWidgetNodes.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.tableWidgetNodes.setTextElideMode(QtCore.Qt.ElideRight)
        self.tableWidgetNodes.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableWidgetNodes.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableWidgetNodes.setShowGrid(False)
        self.tableWidgetNodes.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidgetNodes.setCornerButtonEnabled(False)
        #table properties
        self.tableWidgetNodes.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidgetNodes.horizontalHeader().setDefaultSectionSize(142)
        self.tableWidgetNodes.horizontalHeader().setHighlightSections(True)
        self.tableWidgetNodes.horizontalHeader().setSortIndicatorShown(True)
        self.tableWidgetNodes.horizontalHeader().setStretchLastSection(True)
        self.tableWidgetNodes.verticalHeader().setVisible(True)
        self.tableWidgetNodes.verticalHeader().setMinimumSectionSize(30)
        self.tableWidgetNodes.verticalHeader().setSortIndicatorShown(False)
        self.tableWidgetNodes.verticalHeader().setStretchLastSection(False)
        self.verticalLayout_3.addWidget(self.tableWidgetNodes)

    #*-------------------------Relationship Table Subwindow------------------------------------------------------------------*#

        #subwindow and layout properties
        self.subwindow_Relationship = QtWidgets.QWidget()
        self.subwindow_Relationship.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.subwindow_Relationship.setObjectName("subwindow_Relationship")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.subwindow_Relationship)
        self.verticalLayout.setContentsMargins(-1, -1, 17, -1)
        self.verticalLayout.setObjectName("verticalLayout")

        #add relationship frame
        self.frameRelationship = QtWidgets.QFrame(self.subwindow_Relationship)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frameRelationship.sizePolicy().hasHeightForWidth())
        self.frameRelationship.setSizePolicy(sizePolicy)
        self.frameRelationship.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.frameRelationship.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameRelationship.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameRelationship.setObjectName("frameRelationship")
        self.verticalLayout.addWidget(self.frameRelationship)
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frameRelationship)
        self.gridLayout_2.setObjectName("gridLayout_2")

        #relationship label & line edit
        self.labelRelationship = QtWidgets.QLabel(self.frameRelationship)
        self.labelRelationship.setObjectName("labelRelationship")
        self.gridLayout_2.addWidget(self.labelRelationship, 0, 2, 1, 1)
        self.lineEditRelationship = QtWidgets.QLineEdit(self.frameRelationship)
        self.lineEditRelationship.setObjectName("lineEditRelationship")
        self.gridLayout_2.addWidget(self.lineEditRelationship, 0, 1, 1, 1)

        #parent node label & line edit
        self.labelParent = QtWidgets.QLabel(self.frameRelationship)
        self.labelParent.setObjectName("labelParent")
        self.gridLayout_2.addWidget(self.labelParent, 1, 2, 1, 1)
        self.lineEditParent = QtWidgets.QLineEdit(self.frameRelationship)
        self.lineEditParent.setObjectName("lineEditParent")
        self.gridLayout_2.addWidget(self.lineEditParent, 1, 1, 1, 1)

        #child node label & line edit
        self.labelChild = QtWidgets.QLabel(self.frameRelationship)
        self.labelChild.setObjectName("labelChild")
        self.gridLayout_2.addWidget(self.labelChild, 2, 2, 1, 1)
        self.lineEditChild = QtWidgets.QLineEdit(self.frameRelationship)
        self.lineEditChild.setObjectName("lineEditChild")
        self.gridLayout_2.addWidget(self.lineEditChild, 2, 1, 1, 1)

        #add relationship button
        self.pushButtonAddRelationship = QtWidgets.QPushButton(self.frameRelationship)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonAddRelationship.sizePolicy().hasHeightForWidth())
        self.pushButtonAddRelationship.setSizePolicy(sizePolicy)
        self.pushButtonAddRelationship.setObjectName("pushButtonAddRelationship")
        self.gridLayout_2.addWidget(self.pushButtonAddRelationship, 3, 1, 1, 1)

    

        #relationships table
        self.tableWidgetRelationships = QtWidgets.QTableWidget(self.subwindow_Relationship)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidgetRelationships.sizePolicy().hasHeightForWidth())
        self.tableWidgetRelationships.setSizePolicy(sizePolicy)
        self.tableWidgetRelationships.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tableWidgetRelationships.setAlternatingRowColors(True)
        self.tableWidgetRelationships.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableWidgetRelationships.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableWidgetRelationships.setShowGrid(False)
        self.tableWidgetRelationships.setObjectName("tableWidgetRelationships")
        self.tableWidgetRelationships.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)

        # a relationship is the length of a single relationship
        relationship = 4
        # relationships is the length of a set of relationships
        relationships = 0
        # setting the relationship table dimensions
        self.tableWidgetRelationships.setColumnCount(relationship)
        self.tableWidgetRelationships.setRowCount(relationships)
        # creating the row header for relationships
        for relation in range(relationship):
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignVCenter)
            self.tableWidgetRelationships.setHorizontalHeaderItem(relation, item)

        for relation in range(relationships):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidgetRelationships.setVerticalHeaderItem(relation, item)

        
        # creates the table
        for relation in range(relationships):
            # creates a checkbox in the column
            item = QtWidgets.QTableWidgetItem()
            item.setCheckState(QtCore.Qt.Unchecked)
            self.tableWidgetRelationships.setItem(relation, 0, item)
            for label in range(relationship):
                item = QtWidgets.QTableWidgetItem()
                self.tableWidgetRelationships.setItem(relation, label+1, item)

        self.tableWidgetRelationships.horizontalHeader().setVisible(True)
        self.tableWidgetRelationships.horizontalHeader().setMinimumSectionSize(39)
        self.tableWidgetRelationships.horizontalHeader().setSortIndicatorShown(True)
        self.tableWidgetRelationships.horizontalHeader().setStretchLastSection(True)
        self.tableWidgetRelationships.verticalHeader().setVisible(True)
        self.tableWidgetRelationships.verticalHeader().setDefaultSectionSize(30)
        self.tableWidgetRelationships.verticalHeader().setSortIndicatorShown(False)
        self.verticalLayout.addWidget(self.tableWidgetRelationships)
        self.mdiArea.addSubWindow(self.subwindow_Relationship)
        self.mdiArea.addSubWindow(self.subwindow_Table)
        self.gridLayout.addWidget(self.mdiArea, 1, 0, 1, 1)
        self.graphSubWin = self.mdiArea.addSubWindow(self.subwindow_Graph)

    #*------------------------------Menu Bar---------------------------------------------------*#
        graphWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(graphWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1155, 21))
        self.menubar.setObjectName("menubar")
        
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuOpen_Window = QtWidgets.QMenu(self.menuFile)
        self.menuOpen_Window.setObjectName("menuOpen_Window")
        self.menuSubwindow_Layout_2 = QtWidgets.QMenu(self.menuFile)
        self.menuSubwindow_Layout_2.setObjectName("menuSubwindow_Layout_2")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        graphWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(graphWindow)
        self.statusbar.setObjectName("statusbar")
        graphWindow.setStatusBar(self.statusbar)
        self.actionEvent_Configuration = QtWidgets.QAction(graphWindow)
        self.actionEvent_Configuration.setObjectName("actionEvent_Configuration")
        self.actionEnforcement_Action_Report = QtWidgets.QAction(graphWindow)
        self.actionEnforcement_Action_Report.setObjectName("actionEnforcement_Action_Report")
        self.actionManage_Graph = QtWidgets.QAction(graphWindow)
        self.actionManage_Graph.setObjectName("actionManage_Graph")
        self.actionFilter_Logs = QtWidgets.QAction(graphWindow)
        self.actionFilter_Logs.setObjectName("actionFilter_Logs")
        self.actionGraphical_View = QtWidgets.QAction(graphWindow)
        self.actionGraphical_View.setObjectName("actionGraphical_View")
        self.actionTabular_View = QtWidgets.QAction(graphWindow)
        self.actionTabular_View.setObjectName("actionTabular_View")
        self.actionRelationship_Table = QtWidgets.QAction(graphWindow)
        self.actionRelationship_Table.setObjectName("actionRelationship_Table")


        self.actionTile = QtWidgets.QAction(graphWindow)
        self.actionTile.setObjectName("actionTile")


        self.actionCascade = QtWidgets.QAction(graphWindow)
        self.actionCascade.setObjectName("actionCascade")
        self.actionCascade.triggered.connect(self.mdiArea.cascadeSubWindows)

        

        self.menuOpen_Window.addAction(self.actionGraphical_View)
        self.menuOpen_Window.addAction(self.actionTabular_View)
        self.menuOpen_Window.addAction(self.actionRelationship_Table)
        self.menuSubwindow_Layout_2.addAction(self.actionTile)
        self.menuSubwindow_Layout_2.addAction(self.actionCascade)
        self.menuFile.addAction(self.menuOpen_Window.menuAction())
        self.menuFile.addAction(self.menuSubwindow_Layout_2.menuAction())
        self.menuMenu.addAction(self.actionEvent_Configuration)
        self.menuMenu.addAction(self.actionEnforcement_Action_Report)
        self.menuMenu.addAction(self.actionManage_Graph)
        self.menuMenu.addAction(self.actionFilter_Logs)
        self.menubar.addAction(self.menuMenu.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.mdiArea.tileSubWindows()

        self.retranslateUi(graphWindow)
        self.actionTile.triggered.connect(self.mdiArea.tileSubWindows)
        QtCore.QMetaObject.connectSlotsByName(graphWindow)

    def retranslateUi(self, graphWindow):
        insert = QtCore.QCoreApplication.translate
        graphWindow.setWindowTitle(insert("graphWindow", "MainWindow"))

        #*-------------------------Menu Options------------------------------------------------------------------*#

        self.menuFile.setTitle(insert("graphWindow", "Window"))
        self.menuOpen_Window.setTitle(insert("graphWindow", "Open Window"))
        self.menuSubwindow_Layout_2.setTitle(insert("graphWindow", "Subwindow Layout"))
        self.menuMenu.setTitle(insert("graphWindow", "Menu"))
        self.actionEvent_Configuration.setText(insert("graphWindow", "Event  Configuration"))
        self.actionEnforcement_Action_Report.setText(insert("graphWindow", "Enforcement Action Report"))
        self.actionManage_Graph.setText(insert("graphWindow", "Manage Graph"))
        self.actionTile.setText(insert("graphWindow", "Tile"))
        self.actionCascade.setText(insert("graphWindow", "Cascade"))

        #*-------------------------Vector selection Options------------------------------------------------------------------*#

        self.groupBoxVectorSelection.setTitle(insert("graphWindow", "Vector Selection"))
        self.labelVector.setText(insert("graphWindow", "Vector:"))
        self.labelVectorDesc.setText(insert("graphWindow", "Vector Description"))

        #*-------------------------Graph Subwindow------------------------------------------------------------------*#
        self.actionGraphical_View.setText(insert("graphWindow", "Graphical View"))

        #Interval data
        self.IntervalLabel.setText(insert("MainWindow", "Interval:"))
        self.Interval.setItemText(0, insert("MainWindow", "Select an Interval"))
        self.Interval.setItemText(1, insert("MainWindow", "Seconds"))
        self.Interval.setItemText(2, insert("MainWindow", "Minutes"))
        self.Interval.setItemText(3, insert("MainWindow", "Hours"))

        #Timeline orientation data
        self.TimelineOrientationLabel.setText(insert("MainWindow", "Timeline Orientation:"))
        self.TimelineOrientation.setItemText(0, insert("MainWindow", "Select Orienatation"))
        self.TimelineOrientation.setItemText(1, insert("MainWindow", "Horizontal"))
        self.TimelineOrientation.setItemText(2, insert("MainWindow", "Vertical"))

        #*-------------------------Tabular View Subwindow------------------------------------------------------------------*#
        
        self.actionTabular_View.setText(insert("graphWindow", "Tabular View"))
        self.subwindow_Table.setWindowTitle(insert("graphWindow", "Tabular View"))
        __sortingEnabled = self.tableWidgetNodes.isSortingEnabled()
        self.tableWidgetNodes.setSortingEnabled(False)
        self.tableWidgetNodes.setSortingEnabled(__sortingEnabled)
        self.subwindow_Graph.setWindowTitle(insert("graphWindow", "Graphical View"))

        #*-------------------------Relationship Table Subwindow------------------------------------------------------------------*#

        self.actionRelationship_Table.setText(insert("graphWindow", "Relationship Table"))

        #add relationship labels
        self.subwindow_Relationship.setWindowTitle(insert("graphWindow", "Relationship Table"))

        self.pushButtonAddRelationship.setText(insert("graphWindow", "Add Relationship"))
        self.pushButtonAddRelationship.clicked.connect(lambda: self.addTableData(self.tableWidgetRelationships, self.lineEditRelationship.text(), self.lineEditParent.text(), self.lineEditChild.text()))
        self.pushButtonAddRelationship.clicked.connect(lambda: self.addNewRelationshipToGraph(self.qgv, self.lineEditRelationship.text(), self.lineEditParent.text(), self.lineEditChild.text()))
        self.pushButtonAddRelationship.clicked.connect(lambda: self.clearData(self.tableWidgetRelationships, self.lineEditRelationship, self.lineEditParent, self.lineEditChild))

        #self.pushButtonDeleteRelationship.setText(insert("graphWindow", "Delete Relationship"))
        #self.pushButtonDeleteRelationship.clicked.connect(lambda: self.deleteRelationship(self.tableWidgetRelationships))

        self.labelRelationship.setText(insert("graphWindow", "Relationship Label:"))
        self.labelParent.setText(insert("graphWindow", "Parent Node Name:"))
        self.labelChild.setText(insert("graphWindow", "Child Node Name:"))

        self.tableWidgetRelationships.setSortingEnabled(True)
        item = self.tableWidgetRelationships.horizontalHeaderItem(0)
        item.setText(insert("graphWindow", "Relationship ID"))
        item = self.tableWidgetRelationships.horizontalHeaderItem(1)
        item.setText(insert("graphWindow", "Label"))
        item = self.tableWidgetRelationships.horizontalHeaderItem(2)
        item.setText(insert("graphWindow", "Parent"))
        item = self.tableWidgetRelationships.horizontalHeaderItem(3)
        item.setText(insert("graphWindow", "Child"))
        __sortingEnabled = self.tableWidgetRelationships.isSortingEnabled()
        self.tableWidgetRelationships.setSortingEnabled(False)

        
        self.tableWidgetRelationships.setSortingEnabled(__sortingEnabled)

        

    #adds data to given tree widget with two columns
    def addTableData(self, table, label, parent, child):
        
        table.insertRow(0)

        item = QtWidgets.QTableWidgetItem()
        item.setCheckState(QtCore.Qt.Unchecked)
        item.setFlags(QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        table.setItem(0, 0, item)

        insert = QtCore.QCoreApplication.translate
        item = self.tableWidgetRelationships.item(0, 0)
        item.setText(insert("GraphWindow", str(self.relationshipId)))
        
        table.setItem(0, 1, QtWidgets.QTableWidgetItem(label))
        table.setItem(0, 2, QtWidgets.QTableWidgetItem(parent))
        table.setItem(0, 3, QtWidgets.QTableWidgetItem(child))

        self.relationshipId += 1

    #clears data from line/text edits after adding to tree widget
    def clearData(self, table, col1, col2, col3):
            col1.clear()
            col2.clear()
            col3.clear()
    
    #removes selected items from given tree widget
    def deleteRelationship(self, table):
        selectedItems = table.selectionModel().selectedRows() 
        for item in sorted(selectedItems):
            table.removeRow(item.row())

        

    #add new node to tabular view
    def addNewNode(self, table, nodeId, name, timestamp, description, reference, creator, icon, source):
    
        table.insertRow(1)

        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        item.setCheckState(QtCore.Qt.Checked)
        table.setItem(1, 0, item)

        table.setItem(1, 1, QtWidgets.QTableWidgetItem(nodeId))
        table.setItem(1, 2, QtWidgets.QTableWidgetItem(name))
        table.setItem(1, 3, QtWidgets.QTableWidgetItem(timestamp))
        table.setItem(1, 4, QtWidgets.QTableWidgetItem(description))
        table.setItem(1, 5, QtWidgets.QTableWidgetItem(reference))
        table.setItem(1, 6, QtWidgets.QTableWidgetItem(creator))
        table.setItem(1, 7, QtWidgets.QTableWidgetItem(icon))
        table.setItem(1, 8, QtWidgets.QTableWidgetItem(source))


    #add new relationship from relationship table to graph
    def addNewRelationshipToGraph(self, graph, relationshipLabel, parent, child):
        #retrive node objects given node names
        parentNode = Graph.findNode(self.qgv.engine.graph, parent)
        childNode = Graph.findNode(self.qgv.engine.graph, child)

        #add edge to graph
        self.qgv.addEdge(parentNode, childNode, {"label": relationshipLabel})
        self.qgv.build()

        #update json file to keep track of all edges
        fname = "ui/windows/graph.json"
        self.qgv.saveAsJson(fname)
        
        self.mdiArea.setActiveSubWindow(self.graphSubWin)

    def changeVector(self):
        for vector in self.vectorList:
            if (vector["name"] == self.comboBoxVector.currentText()):
                self.lineEditVectorDesc.setText(vector["description"])
                self.table_items(self.tableWidgetNodes, self.comboBoxVector.currentText())

    def insert_log_entry_table_view(self, vector_name):
        self.tableWidgetNodes.clearContents()
        selectedVector = None
        for vector in self.configuration.vectors:
            if vector.name == vector_name:
                selectedVector = vector
        if selectedVector is None:
            return

        self.nodes = len(selectedVector.log_entries) + 1
        self.node_properties = 9
        self.tableWidgetNodes.setObjectName("tableWidgetNodes")
        self.tableWidgetNodes.setColumnCount(self.node_properties)
        self.tableWidgetNodes.setRowCount(self.nodes)

        # creates node table row header
        for node in range(self.nodes):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidgetNodes.setVerticalHeaderItem(node, item)

        # creates node table column header
        for property in range(self.node_properties):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidgetNodes.setHorizontalHeaderItem(property, item)

        # creates the first column in the first row without a check box (0,0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetNodes.setItem(0, 0, item)

        # creates the rest of the columns in the first row with checkboxes (0,1) to (0,n)
        for property in range(8):
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Checked)
            self.tableWidgetNodes.setItem(0, property + 1, item)

        # # creates the rest of the table starting at (1,0)
        for node in range(self.nodes):
            # creates the checkbox for every row in the first column
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Checked)
            self.tableWidgetNodes.setItem(node + 1, 0, item)
            for property in range(8):
                item = QtWidgets.QTableWidgetItem()
                self.tableWidgetNodes.setItem(node + 1, property + 1, item)

        # add actual data
        for i in range(len(selectedVector.log_entries)):
            # self.tableWidgetNodes.insertRow(i+1)
            item = QtWidgets.QTableWidgetItem()
            item.setText(selectedVector.log_entries[i].time)
            self.tableWidgetNodes.setItem(i + 1, 3, item)
            item = QtWidgets.QTableWidgetItem()
            item.setText(selectedVector.log_entries[i].data)
            self.tableWidgetNodes.setItem(i + 1, 4, item)
            item = QtWidgets.QTableWidgetItem()
            item.setText(selectedVector.log_entries[i].source_file)
            self.tableWidgetNodes.setItem(i + 1, 5, item)

        insert = QtCore.QCoreApplication.translate
        item = self.tableWidgetNodes.verticalHeaderItem(0)
        item.setText(insert("graphWindow", "Property Visibility"))
        item = self.tableWidgetNodes.horizontalHeaderItem(0)
        item.setText(insert("graphWindow", "Node Visibility"))
        item = self.tableWidgetNodes.horizontalHeaderItem(1)
        item.setText(insert("graphWindow", "Node Id"))
        item = self.tableWidgetNodes.horizontalHeaderItem(2)
        item.setText(insert("graphWindow", "Node Name"))
        item = self.tableWidgetNodes.horizontalHeaderItem(3)
        item.setText(insert("graphWindow", "Node Timestamp"))
        item = self.tableWidgetNodes.horizontalHeaderItem(4)
        item.setText(insert("graphWindow", "Node Description"))
        item = self.tableWidgetNodes.horizontalHeaderItem(5)
        item.setText(insert("graphWindow", "Log Entry Reference"))
        item = self.tableWidgetNodes.horizontalHeaderItem(6)
        item.setText(insert("graphWindow", "Log Creator"))
        item = self.tableWidgetNodes.horizontalHeaderItem(7)
        item.setText(insert("graphWindow", "Icon Type"))
        item = self.tableWidgetNodes.horizontalHeaderItem(8)
        item.setText(insert("graphWindow", "Source"))

    def table_items(self, tableWidgetNodes, vector_name):
        selected_vector = None
        for vector in self.configuration.vectors:
            if vector.name == vector_name:
                selected_vector = vector
        if selected_vector is None:
            return
        self.insert_log_entry_table_view(vector_name)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    graphWindow = QtWidgets.QMainWindow()
    ui = GraphWindow()
    ui.setupUi(graphWindow)
    graphWindow.show()
    sys.exit(app.exec_())
