import ctypes
import  sys
from PyQt4 import QtCore, QtGui, QtWebKit
from PyQt4.QtNetwork import *
from browser.NewTab import Tab
from browser.Proxy import Proxy
from browser.DownloadManager import DownloadManager
from PyQt4.QtCore import *
from PyQt4.QtGui import *


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

#Windows 7 TaskBar Icon
myappid = u'pyBrowser.SaurabhBhushan.TorrentFunction.1.2'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)



class Browser(QtGui.QTabWidget):

    def __init__(self,*args, **kwargs):
        QtGui.QTabWidget.__init__(self)
        super(Browser, self).__init__(*args, **kwargs)
        #self.resize(1200, 900)
        self.setWindowState(QtCore.Qt.WindowMaximized)
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowTitle("PyBrowser V1.2 - Dev : [Saurabh Bhushan]")
        self.setObjectName(_fromUtf8("MainWindow"))
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowIcon(QtGui.QIcon("./icon/url.ico"))
      #  self.centralwidget = QtGui.QWidget(self)
       # self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.Tabs = self#QtGui.QTabWidget(self.centralwidget)
        self.Tabs.setObjectName(_fromUtf8("Tabs"))



#############################
        self.tabButton = QtGui.QToolButton(self)
        self.tabButton.setObjectName(_fromUtf8("new_tab"))

        '''
        self.minimize = QtGui.QToolButton(self);
        self.minimize.setObjectName(_fromUtf8("minimize"))

        self.maximize = QtGui.QToolButton(self);
        self.maximize.setObjectName(_fromUtf8("maximize"))

        self.close = QtGui.QToolButton(self);
        self.close.setObjectName(_fromUtf8("close"))

        self.minimize.setMinimumHeight(15);
        self.close.setMinimumHeight(15);
        self.tabButton.setMinimumHeight(15);
        self.maximize.setMinimumHeight(15);

        self.tabButton.resize(10,20)
        self.close.resize(10, 20)
        self.minimize.resize(10, 20)
        self.maximize.resize(10, 20)
        self.t = QtGui.QTabBar(self)
        self.t.ad
        self.setTabBar(self.t)

        hbox = QtGui.QHBoxLayout(self);
        hbox.addWidget(self.tabButton);
        hbox.addWidget(self.minimize);
        hbox.addWidget(self.maximize);
        hbox.addWidget(self.close);
        hbox.insertStretch(1, 100);
        hbox.setSpacing(0);
        hbox.setAlignment(QtCore.Qt.AlignLeft)
        hbox.setAlignment(QtCore.Qt.AlignTop)

        self.cWid = QtGui.QWidget()
        self.cWid.setLayout(hbox)
        '''
        self.setStyleSheet(open("./Style/Style.qss", "r").read())
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed);
#############################
        self.Tabs.setCornerWidget(self.tabButton)
        self.Tabs.setTabsClosable(True)
        self.Tabs.tabCloseRequested.connect(self.closeTab)
        self.add_page()


        QtCore.QMetaObject.connectSlotsByName(self)
        self.setAutoFillBackground(True)

        #Download Manager
        self.DownloadManager = DownloadManager(self)
        self.DownloadManager.hide()
        self.maxNormal = True;
        #self.close.clicked.connect(app.exit);
        #self.minimize.clicked.connect(self.showSmall);
        #self.maximize.clicked.connect(self.showMaxRestore);
        self.tabButton.clicked.connect(self.add_page)

    def showSmall(self):
        self.showMinimized();

    def showMaxRestore(self):
        self.setGeometry(app.desktop().availableGeometry())


    def ShowDownloadManager(self):
        if(self.DownloadManager.isVisible()):
            self.DownloadManager.hide()
        else:
            self.DownloadManager.show()

    def mouseDoubleClickEvent(self,event):
        self.add_page()

    def closeTab(self, currentIndex):
        self.Tabs.removeTab(currentIndex)

    def add_page(self,URL=None):
        nTab = Tab(self.Tabs.currentIndex(),self,URL)
        Title  = nTab.GetTitle()
        self.Tabs.addTab(nTab, Title)




if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    app.setStyle('cleanlooks') #motif , cde , cleanlooks , windows , windowsxp ,windowsvista , macintosh , plastique
    main = Browser()
    main.show()
    sys.exit(app.exec_())