import sys
import ctypes
from PyQt4 import QtCore, QtGui, QtWebKit
from PyQt4.QtNetwork import *
from DesignPattern import singleton

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

#Windows 7 TaskBar Icon
myappid = u'pyBrowser.SaurabhBhushan.TorrentFunction.1.2'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)




class Proxy(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Proxy, self).__init__(parent)
        Dialog=self
        self.setWindowIcon(QtGui.QIcon("./icon/url.ico"))
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(640, 480)
        self.setStyleSheet(open("./Style/Style.qss", "r").read())
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setTitle("Current Proxy")
        self.groupBox.setGeometry(QtCore.QRect(20, 10, 591, 50))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.CurrentProxy = QtGui.QLabel("", self.groupBox)
        self.CurrentProxy.setGeometry(QtCore.QRect(190, 10, 341, 20))
        self.CurrentProxy.setObjectName(_fromUtf8("CurrentProxy"))

        self.ProxyListDetails = QtGui.QGroupBox(Dialog)
        self.ProxyListDetails.setTitle("Select From Proxy List")
        self.ProxyListDetails.setGeometry(QtCore.QRect(20, 100, 591, 141))
        self.ProxyListDetails.setObjectName(_fromUtf8("ProxyListDetails"))
        self.ProxyList = QtGui.QComboBox(self.ProxyListDetails)
        self.ProxyList.setGeometry(QtCore.QRect(60, 40, 491, 22))
        self.ProxyList.setObjectName(_fromUtf8("ProxyList"))
        self.bActivateProxy = QtGui.QPushButton(self.ProxyListDetails)
        self.bActivateProxy.setObjectName(_fromUtf8("ActivateProxy"))
        self.bActivateProxy.setText("Activate")
        self.bActivateProxy.setGeometry(QtCore.QRect(200, 80, 191, 22))

        self.NewProyBox = QtGui.QGroupBox(Dialog)
        self.NewProyBox.setTitle("Add New Proxy")
        self.NewProyBox.setGeometry(QtCore.QRect(20, 280, 591, 141))
        self.NewProyBox.setObjectName(_fromUtf8("ProxyListDetails"))
        self.NewProxy = QtGui.QLineEdit(self.NewProyBox)
        self.NewProxy.setGeometry(QtCore.QRect(60, 40, 491, 22))
        self.NewProxy.setObjectName(_fromUtf8("NewProxy"))
        self.bSaveProxy = QtGui.QPushButton(self.NewProyBox)
        self.bSaveProxy.setObjectName(_fromUtf8("SaveProxy"))
        self.bSaveProxy.setText("Save Proxy")
        self.bSaveProxy.setGeometry(QtCore.QRect(200, 80, 191, 22))

        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.LoadProxies()
        self.GetCurrentProxy()
        self.connect(self.bSaveProxy, QtCore.SIGNAL("clicked()"), self.SaveProxy)
        self.connect(self.bActivateProxy, QtCore.SIGNAL("clicked()"), self.ActivateProxy)
        self.OnProxy(self.GetCurrentProxy())

    def LoadProxies(self):
        f = open("./AppData/proxy.dat", "r")
        myProxyList = f.read().split("\n")
        f.close()
        self.ProxyList.addItems(myProxyList)

    def GetCurrentProxy(self):
        f = open("./AppData/curProxy.tmp", "r")
        cur_proxy = f.read()
        f.close()
        self.CurrentProxy.setText(cur_proxy)
        return cur_proxy

    def SaveProxy(self):
        hostPort = self.NewProxy.text()
        f = open("./AppData/proxy.dat", "a")
        f.write("\n%s" % hostPort)
        f.close()
        self.Inform(QtGui.QMessageBox.Information,"New Proxy Details Added \n %s" % hostPort)

    def Inform(self,Type,Message):
        msg = QtGui.QMessageBox(self)
        msg.setIcon(Type)
        msg.setText(Message)
        msg.setWindowTitle("Proxy Alert")
        msg.setStandardButtons(QtGui.QMessageBox.Ok)
        msg.exec_()

    def ActivateProxy(self):
        ProxyDetails = str(self.ProxyList.currentText())
        f = open("./AppData/curProxy.tmp", "w")
        f.write(ProxyDetails)
        f.close()
        self.Inform(QtGui.QMessageBox.Information, "Proxy Activated!\n %s" % ProxyDetails)


    def OnProxy(self,ProxyDetails):
        if int(ProxyDetails.split(":")[1]) == 0:
            QNetworkProxy.setApplicationProxy(QNetworkProxy(QNetworkProxy.NoProxy))
        else:
            QNetworkProxy.setApplicationProxy(QNetworkProxy(QNetworkProxy.HttpProxy, ProxyDetails.split(":")[0], int(ProxyDetails.split(":")[1])))


def ProxyStart():
    app = QtGui.QApplication(sys.argv)
    app.setStyle('cleanlooks') #motif , cde , cleanlooks , windows , windowsxp ,windowsvista , macintosh , plastique
    main = Proxy()
    main.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    ProxyStart()