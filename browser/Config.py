from DesignPattern import singleton
import ConfigParser, os
import sys
import logging
import ast


@singleton
class Configuration:
    __ConfFile = "./setting.ini"
    __confFileHandle = None
    ConfigData = {}

    def __init__(self):

        self.__confFileHandle = ConfigParser.ConfigParser()
        self.__confFileHandle.readfp(open(self.__ConfFile, "r"))
        self.LoadConfiguration()

    def LoadConfiguration(self):
            print "Loading Config.."
            for section in self.__confFileHandle.sections():
                for option in self.__confFileHandle.options(section):
                    self.ConfigData[option.upper()]=self.__confFileHandle.get(section, option)
                    print "[%s] %s => %s" % (section.upper(),option.upper(),self.ConfigData[option.upper()])

Setting =Configuration()