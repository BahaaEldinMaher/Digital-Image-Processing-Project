#%%
import sys, os
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QLabel, QVBoxLayout
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QImage, QPixmap
import matplotlib.pyplot as plt
import matplotlib as lb
# import matplotlib.image as img
# from keras_preprocessing.image import array_to_img
import numpy as np
from skimage.transform import resize
import cv2 

class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()

        self.setAlignment(Qt.AlignCenter)
        self.setMinimumHeight(150)
        self.setMinimumWidth(300)
        
        self.setText('\n\n Drop Image Here \n\n')
        self.setFont(QFont('Arial',20))
        self.setStyleSheet('''
            QLabel{
                border: 4px dashed #aaa
            }
        ''')

    def setPixmap(self, image):
        super().setPixmap(image)

class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(600, 610)
        self.setAcceptDrops(True)
        mainLayout = QVBoxLayout()
        self.photoViewer = ImageLabel()
        mainLayout.addWidget(self.photoViewer)
        mainLayout.setAlignment(Qt.AlignCenter)
        self.setLayout(mainLayout)
        self.btn=QtWidgets.QPushButton("Glass",self)
        self.btn.setGeometry(QtCore.QRect(210, 560, 93, 28))
        self.btn2=QtWidgets.QPushButton("Blur",self)
        self.btn2.setGeometry(QtCore.QRect(310, 560, 93, 28))
        

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
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.set_image(file_path)
            event.accept()
            self.btn2.clicked.connect(lambda:self.bluring_image(file_path))
            self.btn.clicked.connect(lambda:self.glass(file_path))

            
        else:
            event.ignore()

    def set_image(self, file_path):
        self.photoViewer.setPixmap(QPixmap(file_path))

    def bluring_image(self, file_path):
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
        face = cv2.CascadeClassifier('C:\\Users\\HTG\\Desktop\\haarcascade_frontalface_default.xml')
        im=cv2.imread(file_path)
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        ey=face.detectMultiScale(gray,1.09,6)
        glass=cv2.imread('C:\\Users\\HTG\\Desktop\\g.png')
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
        image=QImage(ll,ll.shape[1],ll.shape[0],ll.strides[0],QImage.Format_RGB888)
        self.photoViewer.setPixmap(QPixmap.fromImage(image))

        
        


app = QApplication(sys.argv)
demo = AppDemo()
demo.show()
sys.exit(app.exec_())

# %%