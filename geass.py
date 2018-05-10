#PROJECT CC: Eye Disorder Recognition Program
#GUI Main
#Designed by Mark Nolledo, laid out using PyQt5

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

#Import methods from other scripts
from sibyl import *
import test2 as tester

class CCMain(QMainWindow):
    #Window initialization
    def __init__(self, parent = None):
        super(CCMain, self).__init__(parent)
        self.title = 'Project CC: Eye Disease Recognition Program'
        self.top = 100
        self.left = 100
        self.width = 400
        self.height = 390
        self.drawUI()

    def drawUI(self):
        #Centers window
        qtRectangle = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(center)

        #Draw userbar
        userbar = QLabel(self)
        pixmap = QPixmap('cc-pastel-ubar-resized.png')
        userbar.setPixmap(pixmap)
        userbar.resize(pixmap.width(), pixmap.height())

        #Draw status message
        self.statusBar().showMessage('v.1.0 initial')
        self.statusBar().setFont(QFont("Arial",9,QFont.Normal))

        #Draw Import button
        importBtn = QPushButton('Import Image', self)
        importBtn.setToolTip('Import an image into the system.')
        importBtn.resize(125,45)
        importBtn.move(10,userbar.height() + 5)

        #Draw Camera button
        cameraBtn = QPushButton('Capture Photo', self)
        cameraBtn.setToolTip('Capture a photo using an attached webcam.')
        cameraBtn.resize(importBtn.width(), importBtn.height())
        #cameraBtn.move(135,105)
        cameraBtn.move(10, 255)

        #Draw Test button
        testBtn = QPushButton('System Tools', self)
        testBtn.setToolTip('Test system features.')
        testBtn.resize(importBtn.width(), importBtn.height())
        testBtn.move(10, 305)
        testBtn.clicked.connect(self.diagnostics_click)

        #Draw text box
        logBox = QPlainTextEdit(self)  #creates the textbox
        logBox.move(145,userbar.height() + 5)
        logBox.resize(self.width - 155, (importBtn.height() + cameraBtn.height() + testBtn.height() + 10))
        logBox.setReadOnly(True)

        #Draw window
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.size())  # Prevent window resize
        self.move(qtRectangle.topLeft())

        #Show window
        self.show()

    #Click listeners
    @pyqtSlot()
    def import_click(self):
        pass
    
    @pyqtSlot()
    def camera_click(self):
        pass
    
    @pyqtSlot()
    def diagnostics_click(self):
        CCTools(self).show()

class CCTools(QMainWindow):
    #Window initialization
    def __init__(self, parent = None):
        super(CCTools, self).__init__(parent)
        self.title = 'System Tools'
        self.top = 200
        self.left = 800
        self.width = 200
        self.height = 300
        self.drawUI()

    def drawUI(self):
        #Draw statusbar
        self.statusBar().showMessage('System Tools - v.1.0 initial')
        self.statusBar().setFont(QFont("Arial",9,QFont.Normal))

        #Draw label
        header = QLabel('System Tools', self)
        header.setFont(QFont("Arial",16))
        header.resize(self.width, 20)
        header.move(10,10)

        #Draw Diagnostics button
        diagnosticsBtn = QPushButton('Run Image Test', self)
        diagnosticsBtn.setToolTip('Performs a simple image recognition test')
        diagnosticsBtn.resize(180,45)
        diagnosticsBtn.move(10, header.height()+20)
        diagnosticsBtn.clicked.connect(self.run_test)
        
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
    def run_test(self):
        tester.runTest()
        
    @pyqtSlot()
    def show_about(self):
        CCAbout(self).show()
    
class CCAbout(QMainWindow):    
    #Window initialization
    def __init__(self, parent = None):
        super(CCAbout, self).__init__(parent)
        self.title = 'About'
        self.top = 200
        self.left = 400
        self.width = 400
        self.height = 500
        self.drawUI()

    def drawUI(self):
        #Center window
        #qtRectangle = self.frameGeometry()
        #center = QDesktopWidget().availableGeometry().center()
        #qtRectangle.moveCenter(center)

        #Draw statusbar
        self.statusBar().showMessage('v.1.0 initial')
        self.statusBar().setFont(QFont("Arial",9,QFont.Normal))

        #Draw banner
        banner = QLabel(self)
        pixmap = QPixmap('cc-pastel-big-resized.png')
        banner.setPixmap(pixmap)
        banner.resize(pixmap.width(), pixmap.height()) #RESET TO PIXMAP WIDTHxHEIGHT ONCE IMAGE IS EDITED

        #Draw header label
        header = QLabel('Project CC', self)
        header.move(10, banner.height()+10)
        header.setFont(QFont("Arial",12,QFont.Bold))
        header.resize(self.width, 14)

        #Draw subheader 1
        subHead1 = QLabel('A recognition system specifically designed to determine the condition of an individual’s eyes.'
                         +' By using a scanned image or a photograph, the system can determine the condition of the eye in the given image.', self)
        subHead1.setWordWrap(True)
        subHead1.move(10, (banner.height()+header.height())+15)
        subHead1.setMinimumSize(self.width-10, subHead1.height()+20)
        subHead1.setFont(QFont("Arial",9,QFont.Normal))
        subHead1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        #Draw subheader 2
        subHead2 = QLabel('Proponents:\n'
                           + 'Lucky Combinido\nKeysha Pareja\nMark Nolledo', self)
        subHead2.setWordWrap(True)
        subHead2.move(10, banner.height()+(subHead1.height()*2))
        subHead2.setMinimumSize(self.width, subHead2.height()+25)
        subHead2.setFont(QFont("Arial",9,QFont.Normal))
        subHead2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        #Draw OK button
        okBtn = QPushButton('OK', self)
        okBtn.resize(70,30)
        okBtn.move((self.width-okBtn.width())-10, self.height-45)
        okBtn.clicked.connect(self.close_window)

        #Draw window
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.size())
        #self.move(qtRectangle.topLeft()

        #Show window
        self.show()

    #Click listeners
    @pyqtSlot()
    def close_window(self):
        self.close()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CCMain()
    sys.exit(app.exec())
