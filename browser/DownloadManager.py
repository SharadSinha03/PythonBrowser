import sys
import ctypes
import subprocess
import os

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
from urllib2 import urlopen
from urllib2 import *
from Config import Setting


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class TitleBar(QtGui.QDialog):
    def __init__(self, Title,parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setWindowFlags(Qt.FramelessWindowHint);
        self.box=parent
        self.setObjectName(_fromUtf8("TitleBarWidget"))
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QtGui.QPalette.Highlight)

        self.DownloadFolder=QtGui.QPushButton(self);
        self.DownloadFolder.setObjectName(_fromUtf8("DownloadFolder"))
        self.Close=QtGui.QPushButton(self);
        self.Close.setObjectName(_fromUtf8("close"))
        self.Close.setMinimumHeight(15);
        label=QtGui.QLabel(self);
        label.setText(Title);
        label.setObjectName("TitleBarName")
        self.setWindowTitle(Title);
        hbox=QtGui.QHBoxLayout(self);
        hbox.addWidget(label);
        hbox.addWidget(self.DownloadFolder);
        hbox.addWidget(self.Close);
        hbox.insertStretch(1,100);
        hbox.setSpacing(0);

        self.setStyleSheet(open("./Style/Style.qss", "r").read())
        self.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed);
        self.Close.clicked.connect(self.close);
        self.DownloadFolder.clicked.connect(self.OpenFolder);

    def OpenFolder(self):
        try:
            subprocess.check_call(['explorer', Setting.ConfigData["DOWNLOAD_FOLDER"]])
        except:
            pass


    def close(self):
        self.box.close()


class DownloadPageWidget(QtGui.QFrame):
    def __init__(self, parent=None):
            QtGui.QFrame.__init__(self, parent)

            self.Layout      = QtGui.QGridLayout(self)
            self.ProgressBar = QtGui.QProgressBar(self)
            self.FileName    = QtGui.QLabel(self)
            self.FileName.setText("")

            font = QtGui.QFont()
            font.setPointSize(11)
            font.setBold(False)
            font.setWeight(50)

            self.Status      = QtGui.QLabel(self)
            #self.Status.setFrameShape(QtGui.QFrame.Box)
            #self.Status.setFrameShadow(QtGui.QFrame.Plain)
            self.Status.setText(_fromUtf8(""))
            self.Status.setAlignment(QtCore.Qt.AlignCenter)
            self.Status.setFont(font)



            self.ProgressBar.setProperty("value", 0)
            self.Layout.addWidget(self.FileName)
            self.Layout.addWidget(self.ProgressBar)
            self.Layout.addWidget(self.Status)
            self.setLayout(self.layout())

            self.setAutoFillBackground(True)

            self.setObjectName("DownloadPage")
            self.setStyleSheet("background-color : black; color : white; ")



class DownloadManager(QtGui.QFrame):
    def __init__(self,parent):
        self.DownloadQueue = {}
        QtGui.QFrame.__init__(self, parent)
        self.m_mouse_down = False;
        self.resize(800,600)
        self.setFrameShape(QtGui.QFrame.StyledPanel)
        css = """
                QFrame{
                    background-color : #E1F4F3;
                    color:white;
                    font:13px ;
                    font-weight:bold;
                    }
                """
        self.setStyleSheet(css)
        self.setWindowFlags(Qt.FramelessWindowHint);
        self.setMouseTracking(True);
        self.m_titleBar = TitleBar("Download Manager",self);
        self.mainLayout = QtGui.QVBoxLayout(self)

        self.scrollLayout = QtGui.QFormLayout()
        self.scrollWidget = QtGui.QWidget()
        self.scrollWidget.setLayout(self.scrollLayout)
        self.scrollWidget.setObjectName("DownloadManagerLayout")
        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollWidget)
        self.mainLayout.addWidget(self.m_titleBar)
        self.mainLayout.addWidget(self.scrollArea)
        self.setLayout(self.mainLayout)
        self.location_on_the_screen()

    def location_on_the_screen(self):
            ag = QtGui.QDesktopWidget().availableGeometry()
            sg = QtGui.QDesktopWidget().screenGeometry()

            widget = self.geometry()
            x = ag.width() - widget.width()
            y = 2 * ag.height() - sg.height() - widget.height()
            self.move(x, y)

    def NewDownloadWidget(self,NewDownload):
        self.scrollLayout.addRow(NewDownload)



    def AddNewDownload(self,url):
         NewDownload = DownloadPageWidget(self)
         DownloadThread = UrlDownloader(NewDownload)
         self.DownloadQueue[url]=[NewDownload,DownloadThread]
         DownloadThread.doneSig.connect(NewDownload.ProgressBar.reset)
         DownloadThread.progSig.connect(NewDownload.ProgressBar.setValue)
         DownloadThread.progStat[str].connect(NewDownload.Status.setText)
         DownloadThread.doneSig.connect(lambda: NewDownload.Status.setText(NewDownload.Status.text().replace("Saving", "Saved") + " - <b>Download Complete</b>."))
         DownloadThread.setUrl(url)
         self.NewDownloadWidget(NewDownload)
         DownloadThread.start()
         self.show()

    def AddTorrentMagnet(self,URL):
		print "Downloading Torrent : "+URL
		subprocess.Popen(Setting.ConfigData["TORRENT_APPLICATION"]+URL)



class UrlDownloader(QThread):
  doneSig = pyqtSignal()
  progSig = pyqtSignal(int)
  progStat = pyqtSignal(str)
  sendNext = pyqtSignal(str)
  def __init__(self, Widget,parent=None):
    super(UrlDownloader, self).__init__(parent)
    self.url0 = str("")
    self.Widget=Widget

  def setUrl(self, u):
    self.url0 = str(u)

  def run(self):
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    hdr = {'User-Agent': user_agent}
    url =  self.url0
    print("Downloading from: {}".format(url))
    request = Request(url, None, hdr)
    rq = urlopen(request)
    fSize = int(rq.info()['Content-Length'])/1000
    fileName = url.split("/")[-1]
    self.Widget.FileName.setText("Filename : %s" % str(fileName))
    downloadedChunk = 0
    blockSize = 2048
    with open(Setting.ConfigData["DOWNLOAD_FOLDER"]+"/"+str(fileName), "wb") as sura:
      while True:
        chunk = rq.read(blockSize)
        if not chunk:
          print("\nDownload Complete.")
          self.sendNext.emit(url)
          break
        downloadedChunk += len(chunk)
        downloadedChunkKb = int(downloadedChunk/1000)
        sura.write(chunk)
        progress = float(downloadedChunkKb) / fSize
        self.progSig.emit(progress * 100)
        stat = r" Saving: {0} [{1:.2%}] of {2} bytes.".format(downloadedChunk, progress, fSize)
        stat2 = "<b> {0} [{1:.1%}] <b>of</b> {2} <b>Kb</b>.".format(downloadedChunkKb,progress, fSize)
        self.progStat.emit(stat2)
        stat = stat + chr(8) * (len(stat) + 1)
    self.doneSig.emit()
