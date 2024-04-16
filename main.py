
from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
from PyQt5.QtGui import QFont, QImage, QPixmap
from PySide2.QtGui import QFont, QImage, QPixmap
from PySide2 import QtWidgets,QtCore, QtGui
import pandas as pd
from PyQt5.QtWidgets import QMessageBox,QDialog,QPushButton,QLineEdit, QWidget, QLabel, QVBoxLayout
from PySide2.QtWidgets import QMessageBox,QDialog,QPushButton,QLineEdit, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from PySide2.QtCore import Qt
import numpy as np
import os
import random
import skimage







file_path=None
filtered=None
brightness_value_now = 0  
blur_value_now = 0

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
        self.photoViewer.setPixmap(QPixmap(file_path).scaled(300,300,Qt.KeepAspectRatio))

    def edge_image(self, file_path):
        if file_path is None:
            return
        im=cv2.imread(file_path)
        # lap=im.copy()
        # k= np.array([[ -1,  -1,  -1],
        #              [ -1,   8,  -1],
        #              [ -1,  -1,  -1]
        #              ])
        # for q in range(3):
        #     for i in range((k.shape[0]//2),im.shape[0]-(k.shape[0]//2)):
        #         for j in range((k.shape[1]//2),im.shape[1]-(k.shape[1]//2)):
        #             m=0
        #             for o in range(-(k.shape[0]//2),(k.shape[0]//2)+1):
        #                 for u in range(-(k.shape[1]//2),(k.shape[1]//2)+1):
        #                     m+=im[i+o][j+u][q]*k[o][u]
        #             lap[i][j][q]=m
        im=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        lap=cv2.Laplacian(im,-1)
        ll=cv2.cvtColor(lap,cv2.COLOR_BGR2RGB)
        global filtered
        filtered=lap.copy()
        image=QImage(ll,ll.shape[1],ll.shape[0],ll.strides[0],QImage.Format_RGB888)
        self.photoViewer.setPixmap(QPixmap.fromImage(image).scaled(300,300,Qt.KeepAspectRatio))
        


        
    def glass(self,file_path):
        if file_path is None:
            return
        path=os.getcwd().replace("\\","\\\\")
        face = cv2.CascadeClassifier(path+'\\haarcascade_frontalface_default.xml')
        im=cv2.imread(file_path)
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        ey=face.detectMultiScale(gray,1.09,6)
        glass=cv2.imread(path+'\\g1.png')
        ss=np.copy(im)
        for (x, y, w, h) in ey:
            face_width = w
            face_height = h
            new_width = face_width + 1
            new_height = face_height+ 1
            # new_height = int(0.45*face_height)+ 1
            glass = cv2.resize(glass, (new_width, new_height))
            for i in range(new_height):
                for j in range(new_width):
                    for k in range(3):
                        # if glass[i][j][k]!=255:
                        #     ss[y + i - int(-0.20 * face_height)][x + j][k] = glass[i][j][k]
                        if glass[i][j][k] >200 or glass[i][j][k] < 20:
                            ss[y + i - int(0.10 * face_height)][x + j][k] = glass[i][j][k]
        
        ll=cv2.cvtColor(ss,cv2.COLOR_BGR2GRAY)

        # convert image from rgb to grayscale
        # r, g, b = img[:,:,0], img[:,:,1], img[:,:,2]
        # gray =  0.299 * r + 0.587 * g + 0.114 *b
        
        global filtered
        filtered=ll.copy()
        # cv2.imwrite("C:\\Users\\HTG\\Desktop\\jeje.png",filtered)
        image=QImage(ll,ll.shape[1],ll.shape[0],ll.strides[0],QImage.Format_Grayscale8)
        self.photoViewer.setPixmap(QPixmap.fromImage(image).scaled(300,300,Qt.KeepAspectRatio))



    def binary(self,file_path):
        if file_path is None:
            return
        img = cv2.imread(file_path)

        # convert image from rgb to grayscale
        # r, g, b = img[:,:,0], img[:,:,1], img[:,:,2]
        # gray =  0.299 * r + 0.587 * g + 0.114 *b

        img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        # thresholding function
        # bw= cv2.threshold(img,140,255,cv2.THRESH_BINARY)[1]

        bw=img.copy()
        row=bw.shape[0]
        col=bw.shape[1]
        for i in range(row):
            for j in range(col):
                if img[i][j]>=140: 
                    bw[i][j]=255
                else:
                    bw[i][j]=0
        
        ll=bw.copy()
        global filtered
        filtered=ll.copy()
        image=QImage(ll,ll.shape[1],ll.shape[0],ll.strides[0],QImage.Format_Grayscale8)
        self.photoViewer.setPixmap(QPixmap.fromImage(image).scaled(300,300,Qt.KeepAspectRatio))


    def cartoon(self,file_path):
        if file_path is None:
            return
        img = cv2.imread(file_path)

        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        # convert image from rgb to grayscale
        # r, g, b = img[:,:,0], img[:,:,1], img[:,:,2]
        # gray =  0.299 * r + 0.587 * g + 0.114 *b

        gray=cv2.medianBlur(gray,5)

        # median blur implementation

        # k= np.array([[ 1,  1,  1],
        #              [ 1,  1,  1],
        #              [ 1,  1,  1]
        #              ])
        # for i in range((k.shape[0]//2),gray.shape[0]-(k.shape[0]//2)):
        #     for j in range((k.shape[1]//2),gray.shape[1]-(k.shape[1]//2)):
        #         m=[]
        #         med=0
        #         for o in range(-(k.shape[0]//2),(k.shape[0]//2)+1):
        #             for u in range(-(k.shape[1]//2),(k.shape[1]//2)+1):
        #                 m.append(gray[i+o][j+u]*k[o][u])
        #         m.sort()
        #         med=np.median(m)
        #         gray[i][j]=med
                    

        edges=cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,9,9)

        color=cv2.bilateralFilter(img,9,250,250)
        # we can use mean filter, too
        # color=img.copy()
        # k= np.array([[ 1,  1,  1],
        #                  [ 1,  1,  1],
        #                  [ 1,  1,  1]
        #                  ])
        # for q in range(3):
        #     for i in range((k.shape[0]//2),img.shape[0]-(k.shape[0]//2)):
        #         for j in range((k.shape[1]//2),img.shape[1]-(k.shape[1]//2)):
        #             m=0
        #             for o in range(-(k.shape[0]//2),(k.shape[0]//2)+1):
        #                 for u in range(-(k.shape[1]//2),(k.shape[1]//2)+1):
        #                     m+=img[i+o][j+u][q]*k[o][u]/9
        #             color[i][j][q]=m


        car=cv2.bitwise_and(color,color,mask=edges)
        global filtered
        filtered=car.copy()
        car=cv2.cvtColor(car,cv2.COLOR_BGR2RGB)
        ll=car.copy()
        image=QImage(ll,ll.shape[1],ll.shape[0],ll.strides[0],QImage.Format_RGB888)
        self.photoViewer.setPixmap(QPixmap.fromImage(image).scaled(300,300,Qt.KeepAspectRatio))

    
    def warm(self,file_path):
        if file_path is None:
            return
        img = cv2.imread(file_path)
        res = img
        res = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
        res = np.array(res, dtype=np.float64)
        res = cv2.transform(res, np.matrix([[0.393, 0.769, 0.189],

                                        [0.349, 0.686, 0.168],

                                        [0.272, 0.534, 0.131]]))
        res[np.where(res > 255)] = 255
        res = np.array(res, dtype=np.uint8)
        ll=res.copy()
        res2 = cv2.cvtColor(res, cv2.COLOR_RGB2BGR)
        global filtered
        filtered=res2.copy()
        image=QImage(ll,ll.shape[1],ll.shape[0],ll.strides[0],QImage.Format_RGB888)
        self.photoViewer.setPixmap(QPixmap.fromImage(image).scaled(300,300,Qt.KeepAspectRatio))


    def noise(self,file_path):
        if file_path is None:
            return
        img = cv2.imread(file_path)
        row = img.shape[0]
        col = img.shape[1]  
        number_of_pixels = random.randint(300, 10000)
        for i in range(number_of_pixels):
            y_coord = random.randint(0, row - 1)
            x_coord = random.randint(0, col - 1)
            img[y_coord][x_coord] = 255
            number_of_pixels = random.randint(300, 10000)
        for i in range(number_of_pixels):
            y_coord = random.randint(0, row - 1)
            x_coord = random.randint(0, col - 1)
            img[y_coord][x_coord] = 0
        ll=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        global filtered
        filtered=img.copy()
        # cv2.imwrite("C:\\Users\\HTG\\Desktop\\jeje.png",filtered)
        image=QImage(ll,ll.shape[1],ll.shape[0],ll.strides[0],QImage.Format_RGB888)
        self.photoViewer.setPixmap(QPixmap.fromImage(image).scaled(300,300,Qt.KeepAspectRatio))
        



    def invert(self,file_path):
        if file_path is None:
            return
        img = cv2.imread(file_path)
        com=1-img
        global filtered
        filtered=com.copy()
        ll=cv2.cvtColor(com,cv2.COLOR_BGR2RGB)
        # cv2.imwrite("C:\\Users\\HTG\\Desktop\\jeje.png",filtered)
        image=QImage(ll,ll.shape[1],ll.shape[0],ll.strides[0],QImage.Format_RGB888)
        self.photoViewer.setPixmap(QPixmap.fromImage(image).scaled(300,300,Qt.KeepAspectRatio))
        

    
    def Border(self,file_path):
        if file_path is None:
            return
        img = cv2.imread(file_path)
        BLACK = [0, 0, 0]
        br = cv2.copyMakeBorder(img, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=BLACK)
        ll=cv2.cvtColor(br,cv2.COLOR_BGR2RGB)
        global filtered
        filtered=br.copy()
        image=QImage(ll,ll.shape[1],ll.shape[0],ll.strides[0],QImage.Format_RGB888)
        self.photoViewer.setPixmap(QPixmap.fromImage(image).scaled(300,300,Qt.KeepAspectRatio))


    def blur_image(self,file_path,val):
            if file_path is None:
                return
            im=cv2.imread(file_path)
            bl=im.copy()
            # k= np.array([[ 1,  1,  1],
            #              [ 1,  1,  1],
            #              [ 1,  1,  1]
            #              ])
            # for q in range(3):
            #     for i in range((k.shape[0]//2),im.shape[0]-(k.shape[0]//2)):
            #         for j in range((k.shape[1]//2),im.shape[1]-(k.shape[1]//2)):
            #             m=0
            #             for o in range(-(k.shape[0]//2),(k.shape[0]//2)+1):
            #                 for u in range(-(k.shape[1]//2),(k.shape[1]//2)+1):
            #                     m+=im[i+o][j+u][q]*k[o][u]/9
            #             bl[i][j][q]=m
            kernel_size = (val + 1, val + 1)  
            bl= cv2.blur(bl, kernel_size)
            ll=cv2.cvtColor(bl,cv2.COLOR_BGR2RGB)
            global filtered
            filtered=bl.copy()
            image=QImage(ll,ll.shape[1],ll.shape[0],ll.strides[0],QImage.Format_RGB888)
            self.photoViewer.setPixmap(QPixmap.fromImage(image).scaled(300,300,Qt.KeepAspectRatio))


    def bright_image(self,file_path, value):
        if file_path is None:
            return
        im=cv2.imread(file_path)
        br=im.copy()
        hsv = cv2.cvtColor(br, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        lim = 255 - value
        v[v > lim] = 255
        v[v <= lim] += value
        final_hsv = cv2.merge((h, s, v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        ll=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        global filtered
        filtered=img.copy()
        image=QImage(ll,ll.shape[1],ll.shape[0],ll.strides[0],QImage.Format_RGB888)
        self.photoViewer.setPixmap(QPixmap.fromImage(image).scaled(300,300,Qt.KeepAspectRatio))
        

    def blur_value(self, value):
        global blur_value_now
        blur_value_now = value
        #print('Blur: ', value)
        self.update()

    
    def brightness_value(self, value):
        global brightness_value_now
        brightness_value_now = value
        #print('Brightness: ', value)
        self.update2()

    def update(self):
        self.blur_image(file_path,blur_value_now)

    def update2(self): 
        self.bright_image(file_path,brightness_value_now)

    def save_image(self,filtered):
            if filtered is None:
                    return
            else:
                    path=os.getcwd().replace("\\","\\\\")
                    cv2.imwrite(path+"\\filtered_images\\filtered_image_"+str(random.randint(0,9999))+".png",filtered)
                    

    def clear_image(self):
            self.photoViewer.clear()
            self.photoViewer.setText('\n\n Drop Image Here \n\n')
            self.photoViewer.setFont(QFont('Arial',15))
            self.photoViewer.setStyleSheet('''
            QLabel{
                border: 4px dashed #fff;
                color: rgb(255, 255, 255);
            } ''')
            global filtered
            filtered=None
            global file_path
            file_path=None
























class Ui_IMG(object):
    def setupUi(self, IMG):
        IMG.setObjectName("IMG")
        IMG.resize(820, 550)
        IMG.setMinimumSize(QtCore.QSize(820, 550))
        IMG.setMaximumSize(QtCore.QSize(820, 550))
        IMG.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.main = QtWidgets.QWidget(IMG)
        self.main.setStyleSheet("background-color: rgb(45, 45, 45);")
        self.main.setObjectName("main")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.main)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.top_bar = QtWidgets.QFrame(self.main)
        self.top_bar.setMaximumSize(QtCore.QSize(16777215, 40))
        self.top_bar.setStyleSheet("background-color: rgb(4, 4, 4);")
        self.top_bar.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.top_bar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.top_bar.setObjectName("top_bar")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.top_bar)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tog_frm = QtWidgets.QFrame(self.top_bar)
        self.tog_frm.setMinimumSize(QtCore.QSize(70, 0))
        self.tog_frm.setMaximumSize(QtCore.QSize(90, 16777215))
        self.tog_frm.setStyleSheet("QPushButton::hover{\n"
"\n"
"    background-color: rgb(145, 143, 143);\n"
"\n"
"}")
        self.tog_frm.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tog_frm.setFrameShadow(QtWidgets.QFrame.Raised)
        self.tog_frm.setObjectName("tog_frm")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tog_frm)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tgl_btn = QtWidgets.QPushButton(self.tog_frm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tgl_btn.sizePolicy().hasHeightForWidth())
        self.tgl_btn.setSizePolicy(sizePolicy)
        self.tgl_btn.setMinimumSize(QtCore.QSize(0, 30))
        self.tgl_btn.setMaximumSize(QtCore.QSize(90, 90))
        self.tgl_btn.setStyleSheet("QPushButton{\n"
"color: rgb(255, 255, 255);\n"
"\n"
"border-style:outset;\n"
"border-radius:10px;\n"
"}\n"
"\n"
"QPushButton::pressed{\n"
"background-color: rgb(224, 255, 238);\n"
"    border-style:inset;\n"
"\n"
"}")
        self.tgl_btn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/ii/images/men.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.tgl_btn.setIcon(icon)
        self.tgl_btn.setIconSize(QtCore.QSize(24, 24))
        self.tgl_btn.setFlat(True)
        self.tgl_btn.setObjectName("tgl_btn")
        self.verticalLayout_2.addWidget(self.tgl_btn)
        self.horizontalLayout.addWidget(self.tog_frm)
        self.frame_top = QtWidgets.QFrame(self.top_bar)
        self.frame_top.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_top.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_top.setObjectName("frame_top")
        self.horizontalLayout.addWidget(self.frame_top)
        self.cntrl_frm = QtWidgets.QFrame(self.top_bar)
        self.cntrl_frm.setMinimumSize(QtCore.QSize(110, 40))
        self.cntrl_frm.setMaximumSize(QtCore.QSize(90, 50))
        self.cntrl_frm.setStyleSheet("")
        self.cntrl_frm.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.cntrl_frm.setFrameShadow(QtWidgets.QFrame.Raised)
        self.cntrl_frm.setObjectName("cntrl_frm")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.cntrl_frm)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.minimize_btn = QtWidgets.QPushButton(self.cntrl_frm)
        self.minimize_btn.setMinimumSize(QtCore.QSize(0, 26))
        self.minimize_btn.setStyleSheet("QPushButton{\n"
"color: rgb(255, 255, 255);\n"
"\n"
"border-style:outset;\n"
"border-radius:10px;\n"
"}\n"
"\n"
"QPushButton::pressed{\n"
"background-color: rgb(224, 255, 238);\n"
"    border-style:inset;\n"
"\n"
"}")
        self.minimize_btn.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/ii/images/minus_2.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.minimize_btn.setIcon(icon1)
        self.minimize_btn.setIconSize(QtCore.QSize(15, 15))
        self.minimize_btn.setFlat(True)
        self.minimize_btn.setObjectName("minimize_btn")
        self.horizontalLayout_3.addWidget(self.minimize_btn)
        self.cls_btn = QtWidgets.QPushButton(self.cntrl_frm)
        self.cls_btn.setMinimumSize(QtCore.QSize(0, 26))
        self.cls_btn.setStyleSheet("\n"
"QPushButton{\n"
"color: rgb(255, 255, 255);\n"
"\n"
"border-style:outset;\n"
"border-radius:10px;\n"
"}\n"
"\n"
"QPushButton::pressed{\n"
"\n"
"    background-color: rgb(255, 0, 0);\n"
"    border-style:inset;\n"
"\n"
"}")
        self.cls_btn.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/ii/images/white_x.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.cls_btn.setIcon(icon2)
        self.cls_btn.setIconSize(QtCore.QSize(24, 30))
        self.cls_btn.setFlat(True)
        self.cls_btn.setObjectName("cls_btn")
        self.horizontalLayout_3.addWidget(self.cls_btn)
        self.horizontalLayout.addWidget(self.cntrl_frm)
        self.verticalLayout.addWidget(self.top_bar)
        self.cont_1 = QtWidgets.QFrame(self.main)
        self.cont_1.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.cont_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.cont_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.cont_1.setObjectName("cont_1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.cont_1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.nav_drw = QtWidgets.QFrame(self.cont_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nav_drw.sizePolicy().hasHeightForWidth())
        self.nav_drw.setSizePolicy(sizePolicy)
        self.nav_drw.setMinimumSize(QtCore.QSize(70, 70))
        self.nav_drw.setMaximumSize(QtCore.QSize(210, 510))
        self.nav_drw.setStyleSheet("background-color: rgb(4, 4, 4);")
        self.nav_drw.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.nav_drw.setFrameShadow(QtWidgets.QFrame.Raised)
        self.nav_drw.setObjectName("nav_drw")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.nav_drw)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.nav_mnu = QtWidgets.QFrame(self.nav_drw)
        self.nav_mnu.setMinimumSize(QtCore.QSize(0, 0))
        self.nav_mnu.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.nav_mnu.setStyleSheet("QFrame{background-color: rgb(4, 4, 4);}\n"
"\n"
"QPushButton{\n"
"padding: 10px 10px;\n"
"background-color: rgb(4, 4, 4);\n"
"color:#ffffff;\n"
"border-style:outset;\n"
"border-radius:10px;\n"
"font-weight: bold;\n"
"font-size:12px;\n"
"}\n"
"\n"
"\n"
"QPushButton::pressed{\n"
"background-color: rgb(224, 255, 238);\n"
"    border-style:inset;\n"
"\n"
"}")
        self.nav_mnu.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.nav_mnu.setFrameShadow(QtWidgets.QFrame.Raised)
        self.nav_mnu.setObjectName("nav_mnu")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.nav_mnu)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.home = QtWidgets.QPushButton(self.nav_mnu)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.home.sizePolicy().hasHeightForWidth())
        self.home.setSizePolicy(sizePolicy)
        self.home.setMinimumSize(QtCore.QSize(70, 0))
        self.home.setMaximumSize(QtCore.QSize(210, 16777215))
        self.home.setStyleSheet("padding-left:70px;")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/ii/images/home.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.home.setIcon(icon3)
        self.home.setIconSize(QtCore.QSize(25, 25))
        self.home.setFlat(True)
        self.home.setObjectName("home")
        self.verticalLayout_4.addWidget(self.home)
        self.filtering = QtWidgets.QPushButton(self.nav_mnu)
        self.filtering.setStyleSheet("padding-left:70px;")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/ii/images/filter.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.filtering.setIcon(icon4)
        self.filtering.setIconSize(QtCore.QSize(25, 25))
        self.filtering.setFlat(True)
        self.filtering.setObjectName("filtering")
        self.verticalLayout_4.addWidget(self.filtering)
        self.about = QtWidgets.QPushButton(self.nav_mnu)
        self.about.setStyleSheet("padding-left:80px;")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/ii/images/info.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.about.setIcon(icon5)
        self.about.setIconSize(QtCore.QSize(25, 25))
        self.about.setFlat(True)
        self.about.setObjectName("about")
        self.verticalLayout_4.addWidget(self.about)
        self.verticalLayout_3.addWidget(self.nav_mnu)
        self.horizontalLayout_2.addWidget(self.nav_drw)
        self.pages_frm = QtWidgets.QFrame(self.cont_1)
        self.pages_frm.setMinimumSize(QtCore.QSize(800, 0))
        self.pages_frm.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.pages_frm.setStyleSheet("QFrame{background-color: rgb(4, 4, 4);}\n"
"\n"
"")
        self.pages_frm.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.pages_frm.setFrameShadow(QtWidgets.QFrame.Raised)
        self.pages_frm.setObjectName("pages_frm")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.pages_frm)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.main_pages_vwr = QtWidgets.QStackedWidget(self.pages_frm)
        self.main_pages_vwr.setMaximumSize(QtCore.QSize(740, 480))
        self.main_pages_vwr.setStyleSheet("background-color: rgb(0,0,0);")
        self.main_pages_vwr.setObjectName("main_pages_vwr")
        self.Home_pg = QtWidgets.QWidget()
        self.Home_pg.setStyleSheet("background-color: #feb09a;\n"
"\n"
"")
        self.Home_pg.setObjectName("Home_pg")
        self.home_backg = QtWidgets.QLabel(self.Home_pg)
        self.home_backg.setGeometry(QtCore.QRect(5, 20, 721, 451))
        self.home_backg.setText("")
        self.home_backg.setPixmap(QtGui.QPixmap(":/ii/images/home_back.jpg"))
        self.home_backg.setAlignment(QtCore.Qt.AlignCenter)
        self.home_backg.setObjectName("home_backg")
        self.go_filters_btn = QtWidgets.QPushButton(self.Home_pg)
        self.go_filters_btn.setGeometry(QtCore.QRect(200, 380, 331, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.go_filters_btn.setFont(font)
        self.go_filters_btn.setStyleSheet("QPushButton{\n"
"color: rgb(0, 0, 0);\n"
"    background-color: rgb(255, 255, 0);\n"
"border-radius:10px;\n"
"border-color: rgb(0, 0, 0);\n"
"border-width:2px;\n"
"border-style:solid;\n"
"}\n"
"\n"
"QPushButton::pressed{\n"
"background-color: rgb(224, 255, 238);\n"
"color:purple;\n"
" border-style:inset;\n"
"\n"
"}")
        self.go_filters_btn.setObjectName("go_filters_btn")
        self.main_pages_vwr.addWidget(self.Home_pg)
        self.Filters_pg = QtWidgets.QWidget()
        self.Filters_pg.setStyleSheet("background-color: rgb(4, 4, 4);")
        self.Filters_pg.setObjectName("Filters_pg")
        self.layoutWidget = QtWidgets.QWidget(self.Filters_pg)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 50, 300, 300))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.view = AppDemo()
        self.gridLayout.addWidget(self.view, 0, 0, 0, 0)
        self.clear_img_btn = QtWidgets.QPushButton(self.Filters_pg)
        self.clear_img_btn.setGeometry(QtCore.QRect(200, 380, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.clear_img_btn.setFont(font)
        self.clear_img_btn.setStyleSheet("QPushButton{\n"
"color: rgb(255, 255, 255);\n"
"    background-color: rgb(195, 11, 146);\n"
"border-style:outset;\n"
"border-radius:10px;\n"
"}\n"
"\n"
"QPushButton::pressed{\n"
"background-color: rgb(224, 255, 238);\n"
"color:black;\n"
" border-style:inset;\n"
"\n"
"}")
        self.clear_img_btn.setObjectName("clear_img_btn")
        self.save_img_btn = QtWidgets.QPushButton(self.Filters_pg)
        self.save_img_btn.setGeometry(QtCore.QRect(10, 380, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.save_img_btn.setFont(font)
        self.save_img_btn.setStyleSheet("QPushButton{\n"
"color: rgb(255, 255, 255);\n"
"    background-color: rgb(0, 148, 0);\n"
"border-style:outset;\n"
"border-radius:10px;\n"
"}\n"
"\n"
"QPushButton::pressed{\n"
"background-color: rgb(224, 255, 238);\n"
"color:black;\n"
" border-style:inset;\n"
"\n"
"}")
        self.save_img_btn.setObjectName("save_img_btn")
        self.frame = QtWidgets.QFrame(self.Filters_pg)
        self.frame.setGeometry(QtCore.QRect(410, 59, 300, 381))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.filters_drw = QtWidgets.QFrame(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filters_drw.sizePolicy().hasHeightForWidth())
        self.filters_drw.setSizePolicy(sizePolicy)
        self.filters_drw.setMinimumSize(QtCore.QSize(280, 0))
        self.filters_drw.setMaximumSize(QtCore.QSize(210, 0))
        self.filters_drw.setStyleSheet("background-color: rgb(4, 4, 4);")
        self.filters_drw.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.filters_drw.setFrameShadow(QtWidgets.QFrame.Raised)
        self.filters_drw.setObjectName("filters_drw")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.filters_drw)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.filters_mnu = QtWidgets.QScrollArea(self.filters_drw)
        self.filters_mnu.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.filters_mnu.setStyleSheet("QFrame{background-color: rgb(4, 4, 4);}\n"
"\n"
"QPushButton{\n"
"padding: 10px 10px;\n"
"background-color: rgb(255, 255, 255);\n"
"color:black;\n"
"border-style:outset;\n"
"border-radius:10px;\n"
"font-weight: bold;\n"
"font-size:12px;\n"
"}\n"
"\n"
"\n"
"QPushButton::pressed{\n"
"background-color:#7F00FF; color:white;\n"
"    border-style:inset;\n"
"\n"
"}\n"
"\n"
"QScrollArea{border-style:none;}\n"
"\n"
)
        self.filters_mnu.setWidgetResizable(True)
        self.filters_mnu.setAlignment(QtCore.Qt.AlignCenter)
        self.filters_mnu.setObjectName("filters_mnu")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 260, 384))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setSpacing(10)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.blur_btn = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.blur_btn.sizePolicy().hasHeightForWidth())
        self.blur_btn.setSizePolicy(sizePolicy)
        self.blur_btn.setMinimumSize(QtCore.QSize(70, 0))
        self.blur_btn.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.blur_btn.setFont(font)
        self.blur_btn.setStyleSheet("\n"
"Font-size:15px;")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/ii/images/edge.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.blur_btn.setIcon(icon6)
        self.blur_btn.setIconSize(QtCore.QSize(40, 40))
        self.blur_btn.setFlat(True)
        self.blur_btn.setObjectName("blur_btn")
        self.verticalLayout_7.addWidget(self.blur_btn)
        self.cartoon_btn = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.cartoon_btn.setMaximumSize(QtCore.QSize(16777215, 40))
        self.cartoon_btn.setStyleSheet("\n"
"Font-size:15px;")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/ii/images/cartoon.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.cartoon_btn.setIcon(icon7)
        self.cartoon_btn.setIconSize(QtCore.QSize(90, 35))
        self.cartoon_btn.setObjectName("cartoon_btn")
        self.verticalLayout_7.addWidget(self.cartoon_btn)
        self.glasses_btn = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.glasses_btn.setMaximumSize(QtCore.QSize(16777215, 40))
        self.glasses_btn.setStyleSheet("padding-left:20px;\n"
"Font-size:15px;")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/ii/images/glass.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.glasses_btn.setIcon(icon8)
        self.glasses_btn.setIconSize(QtCore.QSize(30, 30))
        self.glasses_btn.setFlat(True)
        self.glasses_btn.setObjectName("glasses_btn")
        self.verticalLayout_7.addWidget(self.glasses_btn)
        self.binary_btn = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.binary_btn.setMaximumSize(QtCore.QSize(16777215, 40))
        self.binary_btn.setStyleSheet("\n"
"Font-size:15px;")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/ii/images/binary.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.binary_btn.setIcon(icon9)
        self.binary_btn.setIconSize(QtCore.QSize(25, 25))
        self.binary_btn.setObjectName("binary_btn")
        self.verticalLayout_7.addWidget(self.binary_btn)
        self.negative_btn = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.negative_btn.setStyleSheet("font-size:15px;")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/ii/images/invert.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.negative_btn.setIcon(icon10)
        self.negative_btn.setIconSize(QtCore.QSize(20, 20))
        self.negative_btn.setObjectName("negative_btn")
        self.verticalLayout_7.addWidget(self.negative_btn)
        self.filter5_btn = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.filter5_btn.setStyleSheet("\n"
"Font-size:15px;")
        self.filter5_btn.setObjectName("filter5_btn")
        self.verticalLayout_7.addWidget(self.filter5_btn)
        self.filter6_btn = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.filter6_btn.setStyleSheet("\n"
"Font-size:15px;")
        self.filter6_btn.setObjectName("filter6_btn")
        self.verticalLayout_7.addWidget(self.filter6_btn)
        self.filter7_btn = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.filter7_btn.setStyleSheet("\n"
"Font-size:15px;")
        self.filter7_btn.setObjectName("filter7_btn")
        self.verticalLayout_7.addWidget(self.filter7_btn)
        self.filters_mnu.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_6.addWidget(self.filters_mnu)
        self.verticalLayout_8.addWidget(self.filters_drw)
        self.effects_btn = QtWidgets.QPushButton(self.Filters_pg)
        self.effects_btn.setGeometry(QtCore.QRect(410, 2, 290, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.effects_btn.setFont(font)
        self.effects_btn.setStyleSheet("QPushButton{\n"
"color: rgb(0, 0, 0);\n"
"    background-color:rgb(255, 255, 255);\n"
"border-style:outset;\n"
"border-radius:10px;\n"
"}\n"
"\n"
"QPushButton::pressed{\n"
"background-color: rgb(224, 255, 238);\n"
"color:purple;\n"
" border-style:inset;\n"
"\n"
"}")
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/ii/images/effects.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.effects_btn.setIcon(icon11)
        self.effects_btn.setIconSize(QtCore.QSize(30, 30))
        self.effects_btn.setObjectName("effects_btn")
        self.frame_sld = QtWidgets.QFrame(self.Filters_pg)
        self.frame_sld.setGeometry(QtCore.QRect(315, 50, 84, 300))
        self.frame_sld.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_sld.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_sld.setObjectName("frame_sld")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.frame_sld)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.filters_sliders = QtWidgets.QFrame(self.frame_sld)
        self.filters_sliders.setMaximumSize(QtCore.QSize(16777215, 0))
        self.filters_sliders.setStyleSheet("")
        self.filters_sliders.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.filters_sliders.setFrameShadow(QtWidgets.QFrame.Raised)
        self.filters_sliders.setObjectName("filters_sliders")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.filters_sliders)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.blur_sld = QtWidgets.QSlider(self.filters_sliders)
        self.blur_sld.setOrientation(QtCore.Qt.Vertical)
        self.blur_sld.setObjectName("blur_sld")
        self.horizontalLayout_4.addWidget(self.blur_sld)
        self.bright_sld = QtWidgets.QSlider(self.filters_sliders)
        self.bright_sld.setOrientation(QtCore.Qt.Vertical)
        self.bright_sld.setObjectName("bright_sld")
        self.horizontalLayout_4.addWidget(self.bright_sld)
        self.verticalLayout_9.addWidget(self.filters_sliders)
        self.brightness_lbl = QtWidgets.QLabel(self.Filters_pg)
        self.brightness_lbl.setGeometry(QtCore.QRect(355, 10, 31, 31))
        self.brightness_lbl.setText("")
        self.brightness_lbl.setPixmap(QtGui.QPixmap(":/ii/images/brightness.png"))
        self.brightness_lbl.setScaledContents(True)
        self.brightness_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.brightness_lbl.setObjectName("brightness_lbl")
        self.blur_lbl = QtWidgets.QLabel(self.Filters_pg)
        self.blur_lbl.setGeometry(QtCore.QRect(325, 10, 31, 31))
        self.blur_lbl.setText("")
        self.blur_lbl.setPixmap(QtGui.QPixmap(":/ii/images/blur.png"))
        self.blur_lbl.setScaledContents(True)
        self.blur_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.blur_lbl.setObjectName("blur_lbl")
        self.main_pages_vwr.addWidget(self.Filters_pg)
        self.About_pg = QtWidgets.QWidget()
        self.About_pg.setObjectName("About_pg")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.About_pg)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label = QtWidgets.QLabel(self.About_pg)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("./images/back4.jpg"))
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_10.addWidget(self.label)
        self.main_pages_vwr.addWidget(self.About_pg)
        self.verticalLayout_5.addWidget(self.main_pages_vwr)
        self.horizontalLayout_2.addWidget(self.pages_frm)
        self.verticalLayout.addWidget(self.cont_1)
        IMG.setCentralWidget(self.main)

        self.retranslateUi(IMG)
        self.main_pages_vwr.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(IMG)

    def retranslateUi(self, IMG):
        _translate = QtCore.QCoreApplication.translate
        IMG.setWindowTitle(_translate("IMG", "MainWindow"))
        self.home.setText(_translate("IMG", "Home"))
        self.filtering.setText(_translate("IMG", "Filters"))
        self.about.setText(_translate("IMG", "About"))
        self.go_filters_btn.setText(_translate("IMG", "Let\'s Make Some Funny Images"))
        self.clear_img_btn.setText(_translate("IMG", "Clear"))
        self.save_img_btn.setText(_translate("IMG", "Save"))
        self.blur_btn.setText(_translate("IMG", "Edge"))
        self.cartoon_btn.setText(_translate("IMG", "Cartoon"))
        self.glasses_btn.setText(_translate("IMG", "Glasses"))
        self.binary_btn.setText(_translate("IMG", "Binary"))
        self.negative_btn.setText(_translate("IMG", "Invert"))
        self.filter5_btn.setText(_translate("IMG", "Border"))
        self.filter6_btn.setText(_translate("IMG", "Warm"))
        self.filter7_btn.setText(_translate("IMG", "Noise"))
        self.effects_btn.setText(_translate("IMG", "Effects"))

        self.tgl_btn.clicked.connect(lambda:ac.Interface_actions.menu_slide(self))
        self.cls_btn.clicked.connect(lambda:ac.Interface_actions.Close(self))
        self.minimize_btn.clicked.connect(lambda:ac.Interface_actions.minimize(self))
        self.filtering.clicked.connect(lambda:ac.Interface_actions.change_page(self,1))
        self.home.clicked.connect(lambda:ac.Interface_actions.change_page(self,0))
        self.about.clicked.connect(lambda:ac.Interface_actions.change_page(self,2))
        self.effects_btn.clicked.connect(lambda:ac.Interface_actions.show_filters(self))
        self.blur_btn.clicked.connect(lambda:self.view.edge_image(file_path))
        self.glasses_btn.clicked.connect(lambda:self.view.glass(file_path))
        self.clear_img_btn.clicked.connect(lambda:self.view.clear_image())
        self.save_img_btn.clicked.connect(lambda:self.view.save_image(filtered))
        self.blur_sld.valueChanged['int'].connect(self.view.blur_value)
        self.bright_sld.valueChanged['int'].connect(self.view.brightness_value)
        self.filter5_btn.clicked.connect(lambda: self.view.Border(file_path))
        self.negative_btn.clicked.connect(lambda: self.view.invert(file_path))
        self.binary_btn.clicked.connect(lambda: self.view.binary(file_path))
        self.cartoon_btn.clicked.connect(lambda: self.view.cartoon(file_path))
        self.filter6_btn.clicked.connect(lambda: self.view.warm(file_path))
        self.filter7_btn.clicked.connect(lambda: self.view.noise(file_path))
        self.go_filters_btn.clicked.connect(lambda:ac.Interface_actions.change_page(self,1))
        self.brightness_lbl.hide()
        self.blur_lbl.hide()

import images
import interface_actions as ac


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w=ac.Interface_actions()
    w.show()
    sys.exit(app.exec_())
