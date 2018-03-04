import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class CCTester(QMainWindow):
    #Window initialization
    def __init__(self, parent = None):
        super(CCTester, self).__init__(parent)
        self.title = 'System Tools'
        self.top = 200
        self.left = 800
        self.width = 200
        self.height = 300
        self.drawUI()

    def drawUI(self):
        #Draw statusbar
        self.statusBar().showMessage('System Tools - v.1.0 initial')

        #Draw label
        header = QLabel('System Tools', self)
        header.setFont(QFont("Arial",16))
        header.resize(self.width, 20)
        header.move(10,10)

        #Draw Diagnostics button
        diagnosticsBtn = QPushButton('Diagnostics', self)
        diagnosticsBtn.setToolTip('System diagnostics tools')
        diagnosticsBtn.resize(180,45)
        diagnosticsBtn.move(10, header.height()+20)
        
        #Draw About button
        aboutBtn = QPushButton('About', self)
        aboutBtn.setToolTip('About Project CC')
        aboutBtn.resize(diagnosticsBtn.width(), diagnosticsBtn.height())
        aboutBtn.move(10, diagnosticsBtn.height()*2)
        aboutBtn.clicked.connect(self.show_about)
        
        #Draw window
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.size())
        self.show()

    #Click listeners
    @pyqtSlot()
    def show_about:
        CCAbout(self).show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CCTester()
    sys.exit(app.exec())
