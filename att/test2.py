


from sqlite3.dbapi2 import Cursor
from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
from PyQt5.QtGui import QFont, QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
import numpy as np
import os
import sqlite3
import random

file_path=None
filtered=None
user='hesham'

class image_lbl(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumHeight(150)
        self.setMinimumWidth(150)
        self.setAcceptDrops(True)
        self.setText('\n\n Drop Image Here \n\n')
        self.setFont(QFont('Arial',15))
        self.setStyleSheet('''
            QLabel{
                border: 4px dashed #fff;
                color: rgb(255, 255, 255);
            }
        ''')

    def setPixmap(self, image):
        super().setPixmap(image)

class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(300, 300)
        self.setMinimumWidth(300)
        self.setMaximumHeight(300)
        self.setAcceptDrops(True)
        mainLayout = QVBoxLayout()
        self.photoViewer = image_lbl()
        mainLayout.addWidget(self.photoViewer)
        mainLayout.setAlignment(Qt.AlignCenter)
        self.setLayout(mainLayout)
        

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            global file_path
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.set_image(file_path)
            event.accept()
            
        else:
            event.ignore()

    def ret_file():
        return file_path

    def set_image(self, file_path):
        self.photoViewer.setPixmap(QPixmap(file_path))

    def bluring_image(self, file_path):
        if file_path is None:
            return
        im=cv2.imread(file_path)
        
        bl=im.copy()
        # k= np.array([[ 1,  1,  1, 1, 1],
        #              [ 1,  1,  1, 1, 1],
        #              [ 1,  1,  1, 1, 1],
        #              [ 1,  1,  1, 1, 1],
        #              [ 1,  1,  1, 1, 1]
        #              ])
        # for q in range(3):
        #     for i in range((k.shape[0]//2),im.shape[0]-(k.shape[0]//2)):
        #         for j in range((k.shape[1]//2),im.shape[1]-(k.shape[1]//2)):
        #             m=0
        #             for o in range(-(k.shape[0]//2),(k.shape[0]//2)+1):
        #                 for u in range(-(k.shape[1]//2),(k.shape[1]//2)+1):
        #                     m+=im[i+o][j+u][q]*k[o][u]/25
        #             bl[i][j][q]=m
        bl = cv2.blur(bl,(5,5)) 
        ll=cv2.cvtColor(bl,cv2.COLOR_BGR2RGB)
        image=QImage(ll,ll.shape[1],ll.shape[0],ll.strides[0],QImage.Format_RGB888)
        self.photoViewer.setPixmap(QPixmap.fromImage(image))
        


        
    
    def glass(self,file_path):
        if file_path is None:
            return
        path=os.getcwd().replace("\\","\\\\")
        face = cv2.CascadeClassifier(path+'\\haarcascade_frontalface_default.xml')
        im=cv2.imread(file_path)
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        ey=face.detectMultiScale(gray,1.09,6)
        glass=cv2.imread(path+'\\g.png')
        ss=np.copy(im)
        for (x, y, w, h) in ey:
            face_width = w
            face_height = h
            new_width = face_width + 1
            new_height = int(0.45 * face_height) + 1
            glass = cv2.resize(glass, (new_width, new_height))
            for i in range(new_height):
                for j in range(new_width):
                    for k in range(3):
                        if glass[i][j][k] < 200:
                            ss[y + i - int(-0.20 * face_height)][x + j][k] = glass[i][j][k]
        
        ll=cv2.cvtColor(ss,cv2.COLOR_BGR2RGB)
        # global filtered
        # filtered=ss.copy()
        # cv2.imwrite("C:\\Users\\HTG\\Desktop\\jeje.png",filtered)
        image=QImage(ll,ll.shape[1],ll.shape[0],ll.strides[0],QImage.Format_RGB888)
        self.photoViewer.setPixmap(QPixmap.fromImage(image))


    def ret(self):
        connection=sqlite3.connect('k.db')
        global user
        query='SELECT im FROM h where name="%s" order by number desc limit 1'%(user)
        Cur=connection.cursor()
        Cur.execute(query)
        res=Cur.fetchone()
        connection.commit()
        connection.close()
        img=res[0]
        # names=[]
        # numbers=[]
        # for row in res:
        #     names.append(row[0])
        #     numbers.append(row[1])
        # print(names,numbers)
        pix=QtGui.QPixmap()
        pix.loadFromData(img,"png")
        self.photoViewer.setPixmap(pix)
        print(file_path)
    
    def st(self,file_path):
        if file_path is None:
            return
        i=cv2.imread(file_path)
        q=cv2.imwrite("img.png",i)
        im=open('img.png',"rb").read()
        connection=sqlite3.connect('C:\\Users\\HTG\\Desktop\\BMD303-project\\database\\bmd303.db')
        Cur=connection.cursor()
        Cur.execute("INSERT INTO Staff VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",(None,'hesham',sqlite3.Binary(im),'rjjr','admin','hatef33666@gmail.com','Male','7pm',200,2000,21,12,'other',))
        connection.commit()
        connection.close()



        






class Ui_image_w(object):
    def setupUi(self, image_w):
        image_w.setObjectName("image_w")
        image_w.resize(500, 500)
        image_w.setMinimumSize(QtCore.QSize(500, 500))
        image_w.setMaximumSize(QtCore.QSize(500, 500))
        image_w.setStyleSheet("background-color: rgb(0, 0, 0);")
        
        self.main = QtWidgets.QWidget(image_w)
        self.main.setMinimumSize(QtCore.QSize(500, 500))
        self.main.setMaximumSize(QtCore.QSize(500, 500))
        self.main.setObjectName("main")
        self.container = QtWidgets.QStackedWidget(self.main)
        self.container.setGeometry(QtCore.QRect(60, 30, 400, 400))
        self.container.setMinimumSize(QtCore.QSize(400, 400))
        self.container.setMaximumSize(QtCore.QSize(400, 400))
        self.container.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.container.setObjectName("container")
        self.home_page = QtWidgets.QWidget()
        self.home_page.setObjectName("home_page")
        self.label_2 = QtWidgets.QLabel(self.home_page)
        self.label_2.setGeometry(QtCore.QRect(160, 190, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.container.addWidget(self.home_page)
        self.filter_page = QtWidgets.QWidget()
        self.filter_page.setObjectName("filter_page")
        self.layoutWidget = QtWidgets.QWidget(self.filter_page)
        self.layoutWidget.setGeometry(QtCore.QRect(60, 40, 300, 300))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.view = AppDemo()
        self.gridLayout.addWidget(self.view, 0, 0, 0, 0)
        self.container.addWidget(self.filter_page)
        self.move1 = QtWidgets.QPushButton(self.main)
        self.move1.setGeometry(QtCore.QRect(120, 470, 75, 23))
        self.move1.setFont(QFont("Arial", 12))
        self.move1.setStyleSheet("\n"
"QPushButton{\n"
"color: rgb(255, 255, 255);\n"
"\n"
"background-color: rgb(255, 0, 0);\n"
"border-style:outset;\n"
"border-radius:10px;\n"
"font-weight: bold;"
"}\n"
"\n"
"QPushButton::pressed{\n"
"\n"
"    background-color: #add8e6;\n"
"color:black;\n"
"    border-style:inset;\n"
"\n"
"}")
        self.move1.setObjectName("move1")
        self.move2 = QtWidgets.QPushButton(self.main)
        self.move2.setFont(QFont("Arial", 12))
        self.move2.setGeometry(QtCore.QRect(340, 470, 75, 23))
        self.move2.setStyleSheet("\n"
"QPushButton{\n"
"color: rgb(255, 255, 255);\n"
"\n"
"background-color: rgb(0, 0, 255);\n"
"border-style:outset;\n"
"border-radius:10px;\n"
"font-weight: bold;"
"}\n"
"\n"
"QPushButton::pressed{\n"
"\n"
"    background-color: #add8e6;\n"
"color:black;\n"
"    border-style:inset;\n"
"\n"
"}")
        self.move2.setObjectName("move2")
        image_w.setCentralWidget(self.main)

        self.retranslateUi(image_w)
        self.container.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(image_w)



        
        


    def retranslateUi(self, image_w):
        _translate = QtCore.QCoreApplication.translate
        image_w.setWindowTitle(_translate("image_w", "MainWindow"))
        self.label_2.setText(_translate("image_w", "Home"))
        self.move1.setText(_translate("image_w", "store"))
        self.move2.setText(_translate("image_w", "retrieve"))
        self.move1.clicked.connect(lambda:self.view.st(file_path))
        self.move2.clicked.connect(lambda:self.view.ret())

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    image_w = QtWidgets.QMainWindow()
    ui = Ui_image_w()
    ui.setupUi(image_w)
    image_w.show()
    sys.exit(app.exec_())
   