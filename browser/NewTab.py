import sys
from Cache import History
from Cache import Bookmark
from PyQt4 import QtCore, QtGui, QtWebKit
from PyQt4.QtNetwork import *
from PyQt4.QtGui import QCompleter , QStringListModel
from Proxy import Proxy
import validators

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class Tab(QtGui.QWidget):
    def __init__(self,CurrentIndex,GUI,setURL=None):
        self.GUI = GUI
        self.CurrentIndex = CurrentIndex
        QtGui.QWidget.__init__(self)
        self.centralwidget = self
        self.mainLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setMargin(0)

        self.frame = QtGui.QFrame(self.centralwidget)
        self.gridLayout = QtGui.QVBoxLayout(self.frame)
        self.gridLayout.setMargin(1)
        self.gridLayout.setSpacing(5)
        # Controls
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.tb_url = QtGui.QLineEdit(self.frame)
        self.bt_back = QtGui.QPushButton(self.frame)
        self.bt_ahead = QtGui.QPushButton(self.frame)
        self.bt_reload = QtGui.QPushButton(self.frame)
        # self.bt_u           = QtGui.QPushButton(self.frame)
        self.bt_bookmark = QtGui.QPushButton(self.frame)
        self.bt_history = QtGui.QPushButton(self.frame)
        self.bt_proxy = QtGui.QPushButton(self.frame)
        self.bt_download = QtGui.QPushButton(self.frame)
        self.bt_ahead.setObjectName("FORWARD")
        self.bt_back.setObjectName("BACK")
        self.bt_reload.setObjectName("RELOAD")
        # self.bt_u.setObjectName("URL")
        self.bt_bookmark.setObjectName("BOOKMARK")
        self.bt_history.setObjectName("HISTORY")
        self.bt_proxy.setObjectName("PROXY")
        self.bt_download.setObjectName("DOWNLOAD")
        self.tb_url.setObjectName("HTTP_LINK")
        # self.bt_u.setEnabled(False)
        self.Proxy = Proxy()

        # BookMark & History
        self.popMenu = QtGui.QMenu(self)
        self.popMenuBookMark = QtGui.QMenu(self)
        self.bt_history.setMenu(self.popMenu)
        self.bt_bookmark.setMenu(self.popMenuBookMark)

        self.horizontalLayout.addWidget(self.bt_back)
        self.horizontalLayout.addWidget(self.bt_ahead)
        self.horizontalLayout.addWidget(self.bt_reload)
        self.horizontalLayout.addWidget(self.tb_url)
        self.horizontalLayout.addWidget(self.bt_bookmark)
        self.horizontalLayout.addWidget(self.bt_history)
        self.horizontalLayout.addWidget(self.bt_download)
        self.horizontalLayout.addWidget(self.bt_proxy)
        self.gridLayout.addLayout(self.horizontalLayout)

        # Webpage Progress
        self.status = QtGui.QStatusBar(self.frame)
        self.status.setSizeGripEnabled(True)
        self.status.setMaximumHeight(15)
        self.Progress = QtGui.QLabel("")
        self.status.addWidget(self.Progress, 1)

        #Download Box
        #self.DownloadBox = QtGui.QPushButton("Downloading Manager")
        #self.status.addWidget(self.DownloadBox,1)

        self.html = QtWebKit.QWebView()
        self.gridLayout.addWidget(self.html)
        self.gridLayout.addWidget(self.status)
        self.mainLayout.addWidget(self.frame)


        self.connect(self.tb_url, QtCore.SIGNAL("returnPressed()"), self.browse)
        self.connect(self.bt_back, QtCore.SIGNAL("clicked()"), self.html.back)
        self.connect(self.bt_ahead, QtCore.SIGNAL("clicked()"), self.html.forward)
        self.connect(self.bt_proxy, QtCore.SIGNAL("clicked()"), self.ShowProxy)
        self.connect(self.html, QtCore.SIGNAL("urlChanged(const QUrl)"), self.url_changed)
        self.connect(self.bt_reload, QtCore.SIGNAL("clicked()"), self.html.reload)
        self.connect(self.html, QtCore.SIGNAL("loadFinished(bool)"), self.loadFinished)
        self.connect(self.html, QtCore.SIGNAL("loadProgress(int)"), self.loading)
        self.connect(self.bt_download, QtCore.SIGNAL("clicked()"), self.GUI.ShowDownloadManager)


        self.newTabAction = QtGui.QAction('Open in new tab', self)
        self.html.addAction(self.newTabAction)
        self.newTabAction.triggered.connect(self.createNewTab)

        self.SearchInGoogle = QtGui.QAction('Search In Google', self)
        self.html.addAction(self.SearchInGoogle)
        self.SearchInGoogle.triggered.connect(self.GoogleSelected)
        self.html.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.html.customContextMenuRequested.connect(self.WebPagecontextMenuEvent)

        self.default_url = setURL if setURL else "http://google.com/"
        self.tb_url.setText(self.default_url)
        self.setStyleSheet(open("./Style/Style.qss", "r").read())
        self.setAutoFillBackground(True)
        self.LoadBookMark()

       #URL Suggestion
        self.URLSuggestion= QCompleter()
        self.URLSuggestion.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.tb_url.setCompleter(self.URLSuggestion)
        self.URLSuggestionModel = QStringListModel()
        self.URLSuggestion.setModel(self.URLSuggestionModel)
        self.SetURLSuggestion()

        #Setup Download Manager
        self.html.page().setForwardUnsupportedContent(True)
        self.html.page().unsupportedContent.connect(self.DownloadFile)

        self.browse()
        #self.html.selectionChanged.connect(self.slot)

    def DownloadFile(self,reply):
            self.GUI.DownloadManager.AddNewDownload(reply.url().toString())

    def GetSelectedText(self):
        try:
            return str(self.html.selectedText())
        except:
            try:
                return str(self.html.selectedText())
            except:
                return ""

        #New Tab Eveng Handle
    ############################################################################
    def WebPagecontextMenuEvent(self, pos):
        menu = self.html.page().createStandardContextMenu()
        hit = self.html.page().currentFrame().hitTestContent(pos)
        url = hit.linkUrl()
        menu.addAction(self.SearchInGoogle)
        if url.isValid():
            self.newTabAction.setData(url)
            menu.addAction(self.newTabAction)
        menu.exec_(pos)

    def createNewTab(self):
        url = self.newTabAction.data()
        self.GUI.add_page(url.toString())
        #print('create new tab:', url.toString())

    def GoogleSelected(self):
        Text = self.GetSelectedText()
        self.GUI.add_page("https://www.google.co.in/search?q=%s" % Text)


    ############################################################################
    def SetURLSuggestion(self):
        BrowserHistory = History()
        l= BrowserHistory.Get()
        self.URLSuggestionModel.setStringList(l)

    def keyPressEvent(self, event):
        modifiers = int(event.modifiers())
        if event.key() == QtCore.Qt.Key_D and modifiers == QtCore.Qt.AltModifier:
            self.tb_url.selectAll()
            self.tb_url.setFocus()

    def ShowProxy(self):
        mProxy = Proxy()
        mProxy.exec_()

    def browse(self):
        BrowserHistory = History()
        url = self.tb_url.text() if self.tb_url.text() else self.default_url
        url = self.GetValidURL(str(url))
        if url.startswith("magnet"):
            self.GUI.DownloadManager.AddTorrentMagnet(url)
            return
        self.html.load(QtCore.QUrl(url))
        BrowserHistory.Save(url)
        self.LoadHistory()
        self.html.show()
        self.Title = self.GetTitle()
        self.SetURLSuggestion()



    def loadFinished(self, flag):
        self.Progress.setText("Done")
        self.Title = self.GetTitle()
        self.GUI.Tabs.setTabText(self.CurrentIndex+1,self.Title )


    def loading(self, percent):
        self.Progress.setText("Loading %d%%" % percent)

    def GetTitle(self):
        try:
            if self.html.title():
                self.OriginalTitle = str(self.html.title())
                self.Title = str(self.html.title())[0:20]
            else:
                self.Title  = "New Tab"
            return self.Title
        except:
            return "New Tab"

    def url_changed(self, url):
        self.tb_url.setText(url.toString())

    def LoadHistory(self):
        BrowserHistory = History()
        self.popMenu.clear()
        for URL in BrowserHistory.Get():
            self.popMenu.addSeparator()
            action = QtGui.QAction(URL, self)
            self.popMenu.addAction(action)
            action.triggered[()].connect(lambda item=URL: self.BrowseHistorySelected(item))

    def LoadBookMark(self):
        BookMarkList = Bookmark()
        self.popMenuBookMark.clear()
        for URL in BookMarkList.Get():
            self.popMenuBookMark.addSeparator()
            action = QtGui.QAction(URL, self)
            self.popMenuBookMark.addAction(action)
            action.triggered[()].connect(lambda item=URL: self.BookmarkSelected(item))

    def BookmarkSelected(self,URL):
        if(str(URL) == "SAVE CURRENT URL"):
            BookMarkList = Bookmark()
            BookMarkList.Save(str(self.tb_url.text()))
        else:
            self.tb_url.setText(URL)
            self.browse()
        self.LoadBookMark()

    def BrowseHistorySelected(self, URL):
        self.tb_url.setText(URL)
        self.browse()

    # Validate URL
    GetValidURL = lambda self,url : url if url.startswith("http") or url.startswith("magnet") else (
                        ("https://www.google.co.in/search?q=" + url) if not validators.url("http://" + str(url))
                        else  "http://" + url
                    )
