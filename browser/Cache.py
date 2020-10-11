import os,sys
from collections import OrderedDict
from Config import Setting



class History():
    __history = []
    __hFile   = Setting.ConfigData["HISTORY"]
    def __init__(self):
        self.Load()

    def Save(self,URL):
        if URL not in self.__history:
            self.__history.append(URL)
            f = open(self.__hFile, "a")
            f.write("\n"+URL)
            f.close()

    def Get(self):
        return self.__history

    def Load(self):
        if os.path.isfile(self.__hFile):
             f = open(self.__hFile,"r")
             self.__history = f.read().split("\n")
             self.__history.reverse()
             f.close()
             self.__history=OrderedDict((x, 1) for x in self.__history).keys()


class Bookmark():
    __bookmark = []
    __bFile   = Setting.ConfigData["BOOKMARK"]
    def __init__(self):
        self.Load()

    def Save(self,URL):
        self.__bookmark.append(URL)
        f = open(self.__bFile, "a")
        f.write("\n"+URL)
        f.close()

    def Get(self):
        return self.__bookmark

    def Load(self):
        if os.path.isfile(self.__bFile):
             f = open(self.__bFile,"r")
             self.__bookmark = f.read().split("\n")
             self.__bookmark.reverse()
             f.close()
             self.__bookmark=OrderedDict((x, 1) for x in self.__bookmark).keys()
             self.__bookmark.insert(0,"SAVE CURRENT URL")