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







file_path=None
filtered=None


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
        global filtered
        filtered=bl.copy()
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
        global filtered
        filtered=ll.copy()
        # cv2.imwrite("C:\\Users\\HTG\\Desktop\\jeje.png",filtered)
        image=QImage(ll,ll.shape[1],ll.shape[0],ll.strides[0],QImage.Format_Grayscale8)
        self.photoViewer.setPixmap(QPixmap.fromImage(image).scaled(300,300,Qt.KeepAspectRatio))

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
        IMG.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        IMG.setMinimumSize(QtCore.QSize(820, 550))
        IMG.setMaximumSize(QtCore.QSize(820, 550))
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
        self.main_pages_vwr.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.main_pages_vwr.setObjectName("main_pages_vwr")
        self.Home_pg = QtWidgets.QWidget()
        self.Home_pg.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"\n"
"")
        self.Home_pg.setObjectName("Home_pg")
        self.label_2 = QtWidgets.QLabel(self.Home_pg)
        self.label_2.setGeometry(QtCore.QRect(340, 190, 81, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.main_pages_vwr.addWidget(self.Home_pg)
        self.Filters_pg = QtWidgets.QWidget()
        self.Filters_pg.setStyleSheet("background-color: rgb(4, 4, 4);")
        self.Filters_pg.setObjectName("Filters_pg")
        self.layoutWidget = QtWidgets.QWidget(self.Filters_pg)
        self.layoutWidget.setGeometry(QtCore.QRect(70, 40, 300, 300))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.view = AppDemo()
        self.gridLayout.addWidget(self.view, 0, 0, 0, 0)
        self.clear_img_btn = QtWidgets.QPushButton(self.Filters_pg)
        self.clear_img_btn.setGeometry(QtCore.QRect(280, 360, 101, 31))
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
        self.save_img_btn.setGeometry(QtCore.QRect(50, 360, 101, 31))
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
        self.frame.setGeometry(QtCore.QRect(410, 59, 300, 390))
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
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.filters_mnu = QtWidgets.QFrame(self.filters_drw)
        self.filters_mnu.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.filters_mnu.setStyleSheet("QFrame{background-color: rgb(4, 4, 4);}\n"
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
        self.filters_mnu.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.filters_mnu.setFrameShadow(QtWidgets.QFrame.Raised)
        self.filters_mnu.setObjectName("filters_mnu")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.filters_mnu)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.blur_btn = QtWidgets.QPushButton(self.filters_mnu)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.blur_btn.sizePolicy().hasHeightForWidth())
        self.blur_btn.setSizePolicy(sizePolicy)
        self.blur_btn.setMinimumSize(QtCore.QSize(0, 0))
        self.blur_btn.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.blur_btn.setFont(font)
        self.blur_btn.setStyleSheet("padding-left:10px;\n"
"Font-size:15px;")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/ii/images/blur.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.blur_btn.setIcon(icon6)
        self.blur_btn.setIconSize(QtCore.QSize(30, 30))
        self.blur_btn.setFlat(True)
        self.blur_btn.setObjectName("blur_btn")
        self.verticalLayout_7.addWidget(self.blur_btn)
        self.glasses_btn = QtWidgets.QPushButton(self.filters_mnu)
        self.glasses_btn.setStyleSheet("padding-left:20px;\n"
"Font-size:15px;")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/ii/images/glass.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.glasses_btn.setIcon(icon7)
        self.glasses_btn.setIconSize(QtCore.QSize(30, 30))
        self.glasses_btn.setFlat(True)
        self.glasses_btn.setObjectName("glasses_btn")
        self.verticalLayout_7.addWidget(self.glasses_btn)
        self.verticalLayout_6.addWidget(self.filters_mnu)
        self.verticalLayout_8.addWidget(self.filters_drw)
        self.clear_img_btn_2 = QtWidgets.QPushButton(self.Filters_pg)
        self.clear_img_btn_2.setGeometry(QtCore.QRect(410, 2, 290, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.clear_img_btn_2.setFont(font)
        self.clear_img_btn_2.setStyleSheet("QPushButton{\n"
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
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/ii/images/effects.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.clear_img_btn_2.setIcon(icon8)
        self.clear_img_btn_2.setIconSize(QtCore.QSize(30, 30))
        self.clear_img_btn_2.setObjectName("clear_img_btn_2")
        self.main_pages_vwr.addWidget(self.Filters_pg)
        self.About_pg = QtWidgets.QWidget()
        self.About_pg.setObjectName("About_pg")
        self.label = QtWidgets.QLabel(self.About_pg)
        self.label.setGeometry(QtCore.QRect(330, 190, 81, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.main_pages_vwr.addWidget(self.About_pg)
        self.verticalLayout_5.addWidget(self.main_pages_vwr)
        self.horizontalLayout_2.addWidget(self.pages_frm)
        self.verticalLayout.addWidget(self.cont_1)
        IMG.setCentralWidget(self.main)

        self.retranslateUi(IMG)
        self.main_pages_vwr.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(IMG)

    def retranslateUi(self, IMG):
        _translate = QtCore.QCoreApplication.translate
        IMG.setWindowTitle(_translate("IMG", "MainWindow"))
        self.home.setText(_translate("IMG", "Home"))
        self.filtering.setText(_translate("IMG", "Filters"))
        self.about.setText(_translate("IMG", "About"))
        self.label_2.setText(_translate("IMG", "Home"))
        self.clear_img_btn.setText(_translate("IMG", "Clear"))
        self.save_img_btn.setText(_translate("IMG", "Save"))
        self.blur_btn.setText(_translate("IMG", "Blur"))
        self.glasses_btn.setText(_translate("IMG", "Glasses"))
        self.clear_img_btn_2.setText(_translate("IMG", "Effects"))
        self.label.setText(_translate("IMG", "About"))
        
        self.tgl_btn.clicked.connect(lambda:ac.Interface_actions.menu_slide(self))
        self.cls_btn.clicked.connect(lambda:ac.Interface_actions.Close(self))
        self.minimize_btn.clicked.connect(lambda:ac.Interface_actions.minimize(self))
        self.filtering.clicked.connect(lambda:ac.Interface_actions.change_page(self,1))
        self.home.clicked.connect(lambda:ac.Interface_actions.change_page(self,0))
        self.about.clicked.connect(lambda:ac.Interface_actions.change_page(self,2))
        self.clear_img_btn_2.clicked.connect(lambda:ac.Interface_actions.show_filters(self))
        self.blur_btn.clicked.connect(lambda:self.view.bluring_image(file_path))
        self.glasses_btn.clicked.connect(lambda:self.view.glass(file_path))
        self.clear_img_btn.clicked.connect(lambda:self.view.clear_image())
        self.save_img_btn.clicked.connect(lambda:self.view.save_image(filtered))
import ii
import interface_actions as ac



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w=ac.Interface_actions()
    w.show()
    sys.exit(app.exec_())
