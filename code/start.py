import sys
import MySQLdb
from PyQt4 import QtGui, QtCore, uic
from tokens import *
 
class TestApp(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = uic.loadUi('nltk.ui')
        self.ui.label_2.setPixmap(QtGui.QPixmap('maxflow.png'))
        self.ui.label_2.setScaledContents(True)
        self.ui.show()
        self.connect(self.ui.pushButton, QtCore.SIGNAL('clicked()'), self.execSQL)
        self.connect(self.ui.commandLinkButton, QtCore.SIGNAL('clicked()'), self.getSQL)
        
        
    def execSQL(self):
        
        #Loading UI
        self.rui = uic.loadUi('results.ui')
        
        #MYSQL connection
        conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "msdhoni", db = "imdb")
        cursor = conn.cursor ()
        
        #Showing screen
        self.rui.show()

        #Getting SQL from GUI
        question  = str(self.ui.SQLEditText.toPlainText())
        
        #Executing SQL
        cursor.execute(question)
        rows=cursor.fetchall()        

        #Appending results to GUI
        for row in rows:
            answer=row
            self.rui.listWidget.addItem(str(answer[0]))
        
    
    def getSQL(self):
        question  = str(self.ui.queryEditText.toPlainText())
        sql_query = convert(question)
        self.ui.SQLEditText.clear()
        self.ui.SQLEditText.insertPlainText(sql_query)
        
 
        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    win = TestApp()
    sys.exit(app.exec_())
