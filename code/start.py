import sys
import MySQLdb
from PyQt4 import QtGui, QtCore, uic
from tokens import *
 
class TestApp(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = uic.loadUi('nltk.ui')
        
        self.ui.show()
        self.connect(self.ui.pushButton, QtCore.SIGNAL('clicked()'), self.execSQL)
        self.connect(self.ui.commandLinkButton, QtCore.SIGNAL('clicked()'), self.getSQL)
        self.connect(self.ui.pushButton_3, QtCore.SIGNAL('clicked()'), self.popMaxFlow)
        self.connect(self.ui.pushButton_2, QtCore.SIGNAL('clicked()'), self.popDigraph)
        
    def popMaxFlow(self):
        self.mui = uic.loadUi('image.ui')
        self.mui.label.setPixmap(QtGui.QPixmap('maxflow.png'))
        self.mui.label.setScaledContents(True)
        self.mui.show()

    def popDigraph(self):
        self.mui = uic.loadUi('image.ui')
        self.mui.label.setPixmap(QtGui.QPixmap('digraph.png'))
        self.mui.label.setScaledContents(True)
        self.mui.show()
        
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
        self.rui.textBrowser.append('<font color="darkblue">'+question)
        self.rui.lcdNumber.display(len(rows))
        self.rui.listWidget.setAlternatingRowColors(True)
        #Appending results to GUI
        for row in rows:
            answer=row
            self.rui.listWidget.addItem(str(answer[0]))
        
    
    def getSQL(self):
        question  = str(self.ui.queryEditText.toPlainText())
        try:
            result = convert(question)
            sql_query= result['query']
            attach = result['attach']
            rest = result['rest']
            
            self.ui.SQLEditText.clear()
            self.ui.SQLEditText.insertPlainText(sql_query)
            
            self.ui.tokenEditText.clear()
            self.ui.tokenEditText.insertPlainText(str(attach)+str(rest))
            
            self.ui.label_2.setPixmap(QtGui.QPixmap('maxflow.png'))
            self.ui.label_2.setScaledContents(True)

            self.ui.label_5.setPixmap(QtGui.QPixmap('digraph.png'))
            self.ui.label_5.setScaledContents(True)
            
        except:
            self.eui = uic.loadUi('error.ui')
            self.eui.show()
                    
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    win = TestApp()
    sys.exit(app.exec_())
