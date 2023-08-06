from PySide6.QtWidgets import (QTextEdit, QSplitter, QVBoxLayout, QWidget, QLineEdit, QHBoxLayout, QTreeView, QAbstractItemView)
from PySide6.QtCore import (Qt, Slot)
from PySide6.QtGui import (QStandardItemModel, QStandardItem, QIcon)
import json
import os

class BoxGUI(QWidget):
    def __init__(self,GUILogger,DBObject):
        super().__init__()
        if(os.name == "nt"):
            self.setWindowIcon(QIcon(".\\resources\\adbox.png"))
        else:
            self.setWindowIcon(QIcon("./resources/adbox.png"))
        self.setStyleSheet('background-color: #cdcdc0')
        self.setWindowTitle("ADBOX")
        self.__GUILogger = GUILogger
        self.__DBObject = DBObject
        self.__TextEdit = QTextEdit()
        self.__TextEdit.setStyleSheet("""
        QTextEdit {background-color: #f1f1f2; border: 2px solid #1e434c; border-radius: 6px; padding: 5px;}
        QScrollBar {background: #f1f1f2;}
        QScrollBar::handle {background: #1e434c; border-radius: 6px;}  
        QScrollBar::up-arrow, QScrollBar::down-arrow {border: 3px solid #1e434c; border-radius: 3px; background: #f1f1f2;}
        """)
        self.__TextEdit.setAlignment(Qt.AlignLeft)
        #####
        self.__Edit = QLineEdit()
        self.__Edit.setStyleSheet("background-color: #f1f1f2; border: 2px solid #1e434c; border-radius: 6px;")
        self.__Edit.setPlaceholderText("Search")
        #####
        self.HLayout = QHBoxLayout(self)
        self.__SplitterR = QSplitter(Qt.Vertical)
        self.__SplitterR.addWidget(self.__Edit)
        self.__SplitterR.addWidget(self.__TextEdit)
        #####
        self.__Splitter = QSplitter(Qt.Horizontal)
        self.__TreeView = QTreeView()
        self.__TreeView.setStyleSheet("""
        QTreeView {background-color: #f1f1f2; border: 2px solid #1e434c; border-radius: 11px; padding: 5px;}
        QTreeView::item:selected {background-color: #cdcdc0; border-radius: 5px; color: #1e434c;}
        QTreeView::branch {background-color: #f1f1f2;}
        QScrollBar {background: #f1f1f2;}
        QScrollBar::handle {background: #1e434c; border-radius: 6px;}  
        QScrollBar::up-arrow, QScrollBar::down-arrow {border: 3px solid #1e434c; border-radius: 3px; background: #f1f1f2;}
        """)
        self.__TreeView.doubleClicked.connect(self.__TreeViewDoubleClick)
        self.__TreeView.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.__TreeView.setHeaderHidden(True)
        self.__Splitter.addWidget(self.__TreeView)
        self.__Splitter.addWidget(self.__SplitterR)
        self.__Splitter.setSizes([self.__Splitter.size().height() * 0.3, self.__Splitter.size().height() * 0.7])
        #####
        self.HLayout.addWidget(self.__Splitter)
        self.setLayout(self.HLayout)
        self.__Edit.returnPressed.connect(self.__SearchObjects)

    def __AddObject(self,Objects, ObjType):
        if (os.name == "nt"):
            OtherIcon = QIcon("{0}\\resources\\adbox.png".format(os.path.dirname(os.path.abspath(__file__))))
            MainIcon = QIcon("{0}\\resources\\{1}.png".format(os.path.dirname(os.path.abspath(__file__)), ObjType))
        else:
            OtherIcon = QIcon("{0}/resources/adbox.png".format(os.path.dirname(os.path.abspath(__file__))))
            MainIcon = QIcon("{0}/resources/{1}.png".format(os.path.dirname(os.path.abspath(__file__)), ObjType))
        ParentItem = self.__Model.invisibleRootItem()
        if (len(Objects) != 0):
            for Obj in Objects:
                OUArray = Obj[0].split(',')
                RootDC = ""
                LevelCount = 0
                for OUStr in reversed(OUArray):
                    if ("DC=" in OUStr):
                        RootDC = "{0}.{1}".format(OUStr[3:],RootDC)
                        LevelCount+=1
                RootDC = RootDC[:-1]
                ChildRowCount = ParentItem.rowCount()
                if (ChildRowCount != 0):
                    for i in range(0, ChildRowCount):
                        TmpChild = ParentItem.child(i)
                        if (TmpChild.text() == RootDC):
                            ParentItem = TmpChild
                        else:
                            TmpItem = QStandardItem(RootDC)
                            TmpItem.setIcon(OtherIcon)
                            TmpItem.setData("root")
                            ParentItem.appendRow(TmpItem)
                            ParentItem = TmpItem
                else:
                    TmpItem = QStandardItem(RootDC)
                    TmpItem.setIcon(OtherIcon)
                    TmpItem.setData("root")
                    ParentItem.appendRow(TmpItem)
                    ParentItem = TmpItem
                for OUStr in reversed(OUArray[:-LevelCount]):
                    try:
                        TmpStr = OUStr[3:]
                        ChildRowCount = ParentItem.rowCount()
                        AddItem = True
                        if (ChildRowCount != 0):
                            for i in range(0, ChildRowCount):
                                TmpChild = ParentItem.child(i)
                                if (TmpChild.text() == TmpStr):
                                    ParentItem = TmpChild
                                    ParentItem.setIcon(OtherIcon)
                                    AddItem = False
                                    break
                    except Exception as BoxExcept:
                        self.__GUILogger.error("BoxGUI:__AddObject: Exception {0}".format(BoxExcept))

                    if (AddItem):
                        TmpItem = QStandardItem(TmpStr)
                        TmpItem.setIcon(MainIcon)
                        TmpItem.setData(ObjType)
                        ParentItem.appendRow(TmpItem)
                        ParentItem = TmpItem
                ParentItem = self.__Model.invisibleRootItem()
        else:
            self.__GUILogger.info("BoxGUI:__AddObject: Objects not found")

    def _LoadObject(self):
        self.__Model = QStandardItemModel()
        Objects = self.__DBObject._LoadObject("users")
        self.__AddObject(Objects,"users")
        Objects = self.__DBObject._LoadObject("computers")
        self.__AddObject(Objects,"computers")
        Objects = self.__DBObject._LoadObject("groups")
        self.__AddObject(Objects,"groups")
        self.__TreeView.setModel(self.__Model)

    @Slot()
    def __TreeViewDoubleClick(self, DCObj):
        StObject = self.__TreeView.model().itemFromIndex(DCObj)
        ObjValue = StObject.text()
        if(StObject.rowCount() == 0):
            self.__GUILogger.debug("BoxGUI:__TreeViewDoubleClick: Object name '{0}'".format(ObjValue))
            ObjType = StObject.data()
            RawData = self.__DBObject._GetObject(ObjType, ObjValue)
            if(RawData == None):
                self.__TextEdit.setText("Object not found '{0}'".format(ObjValue))
            else:
                PrintStr = ""
                JsonData = json.loads(RawData[0])
                for RawKey in JsonData.keys():
                    if (isinstance(JsonData[RawKey], list)):
                        for RawValue in JsonData[RawKey]:
                            PrintStr += "{0}: {1}\n".format(RawKey, RawValue)
                    else:
                        PrintStr += "{0}: {1}\n".format(RawKey, JsonData[RawKey])
                self.__TextEdit.setText(PrintStr)

    def __ExpandedViewObject(self, Obj, ExpType):
        self.__TreeView.setExpanded(Obj.index(), ExpType)
        if(Obj.parent() != None):
            self.__ExpandedViewObject(Obj.parent(), ExpType)

    def __EnumViewObject(self, SearchText, ParentItem):
        ChildRowCount = ParentItem.rowCount()
        for i in range(0,ChildRowCount):
            TmpChild = ParentItem.child(i)
            if(TmpChild.rowCount() == 0):
                if(SearchText == ""):
                    self.__TreeView.setRowHidden(i, ParentItem.index(), False)
                    self.__ExpandedViewObject(ParentItem, False)
                else:
                    if(SearchText not in TmpChild.text()):
                        self.__TreeView.setRowHidden(i, ParentItem.index(), True)
                    else:
                        self.__TreeView.setRowHidden(i, ParentItem.index(), False)
                        self.__ExpandedViewObject(ParentItem, True)
            else:
                self.__EnumViewObject(SearchText, TmpChild)

    @Slot()
    def __SearchObjects(self):
        SearchText = self.__Edit.text()
        ParentItem = self.__Model.invisibleRootItem()
        self.__EnumViewObject(SearchText, ParentItem)
        pass