import sys
import logging
import argparse
import os
from ADBox import BoxLdap
from ADBox import BoxSql
from ADBox import BoxGUI

from PySide6.QtWidgets import (QApplication)

__version__ = "0.1.0"
__author__ = 'Ping-P0ng'

if __name__ == "__main__":

    BoxParser = argparse.ArgumentParser(description='ADBox')
    BoxParser.add_argument("-m", dest="module", type=str, help="ADBox module", choices=["dump","gui"])
    BoxParser.add_argument("-s", dest="srv", type=str, help="Active Directory server")
    BoxParser.add_argument("-u", dest="user", type=str, help="Domain user name")
    BoxParser.add_argument("-p", dest="passwd", type=str, help="Domain user password")
    BoxParser.add_argument('-ssl', type=bool, default=False, help='Use ldap ssl')
    BoxParser.add_argument('-debug', dest='debug', action='store_true', help='Set debug print')
    BoxParser.add_argument("-db", dest="dbfile", type=str, default="adbox.sqlite", help="DB file name")
    BoxParser.add_argument("-v", dest="version", action='store_true', help="Show version")
    BoxParser.set_defaults(debug=False)
    BoxArgs = BoxParser.parse_args()

    MainLogger = logging.getLogger("ADBox")
    if(BoxArgs.debug):
        logLevel = logging.DEBUG
    else:
        logLevel = logging.INFO
    MainLogger.setLevel(logLevel)
    ChLogger = logging.StreamHandler()
    ChLogger.setLevel(logLevel)
    ChLogger.setFormatter(logging.Formatter('%(levelname)s:%(name)s:%(message)s'))
    MainLogger.addHandler(ChLogger)

    if(BoxArgs.module == "dump"): # -s 192.168.27.129 -u "TEST\Administrator" -p Qwerty12345
        if((BoxArgs.srv != None) and (BoxArgs.user != None) and (BoxArgs.passwd != None)):
            MainBoxLdap = BoxLdap.BoxLdap(BoxArgs.srv, BoxArgs.user, BoxArgs.passwd, BoxArgs.ssl, MainLogger)
            if(MainBoxLdap._ConnectStatus):
                MainBoxSql = BoxSql.BoxSql(BoxArgs.dbfile, MainLogger)
                if(MainBoxSql._ChceckDB):
                    # Users
                    MainBoxLdap.GetUsers(MainBoxSql)
                    # Computers
                    MainBoxLdap.GetComputers(MainBoxSql)
                    # Groups
                    MainBoxLdap.GetGroups(MainBoxSql)
                else:
                    MainLogger.info("ADBox.main: Fail initialized DB")
            else:
                MainLogger.info("ADBox.main: Fail connection, program close")
        else:
            MainLogger.info("ADBox.main: User/Server/Passwd not set")
    elif(BoxArgs.module == "gui"):
        if (os.path.exists(BoxArgs.dbfile)):
            MainBoxSql = BoxSql.BoxSql(BoxArgs.dbfile, MainLogger)
            BoxApp = QApplication()
            GUI = BoxGUI.BoxGUI(MainLogger,MainBoxSql)
            GUI.resize(1200, 800)
            GUI._LoadObject()
            GUI.show()
            sys.exit(BoxApp.exec())
        else:
            MainLogger.info("ADBox.main: DB file not found: {0}".format(BoxArgs.dbfile))
    elif(BoxArgs.version):
        print("ADBox version {0}".format(__version__))
    else:
        BoxParser.print_help()