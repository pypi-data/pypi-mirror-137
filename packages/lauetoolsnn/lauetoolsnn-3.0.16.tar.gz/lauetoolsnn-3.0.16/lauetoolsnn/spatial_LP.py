#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 29 21:53:26 2022

@author: opd32

Small tool to look at the LauePatterns Raw as a funtion of their spatial location
"""
import warnings
warnings.filterwarnings('ignore')
import matplotlib
matplotlib.use('Qt5Agg')
matplotlib.rcParams.update({'font.size': 14})
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
import os
import re
import glob
import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, \
                            QVBoxLayout, QSlider, \
                                QLineEdit
import LaueTools.dict_LaueTools as dictLT
import LaueTools.IOimagefile as IOimage

#########################################################################################
#%%%%%%%%%%%%%%%%%%%%%%%%%  USER INPUT %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
filenameDirec = r"/mnt/multipath-shares/data/visitor/ma4959/bm32/20220129/900Csaturday"
experimental_prefix = r'Zr900_'
format_file = "tif"
ccd_label = "sCMOS_16M"
lim_x, lim_y = 121, 121
#########################################################################################




minn, maxx = 0, 65000
## Number of files to generate
filenm = np.chararray((lim_x,lim_y), itemsize=2000)
filenm = filenm.ravel()
count_global = lim_x * lim_y
format_file = dictLT.dict_CCD[ccd_label][7]
### READ FILES FROM THE FOLDER
list_of_files = glob.glob(filenameDirec+'//'+experimental_prefix+'*.'+format_file)
## sort files
## TypeError: '<' not supported between instances of 'str' and 'int'
list_of_files.sort(key=lambda var:[int(x) if x.isdigit() else x for x in re.findall(r'[^0-9]|[0-9]+', var)[-5:-4]])

if len(list_of_files) == count_global:
    for ii in range(len(list_of_files)):
        filenm[ii] = list_of_files[ii]               
else:
    print("expected "+str(count_global)+" files based on the XY grid ("+str(lim_x)+","+str(lim_y)+") defined by user")
    print("But found "+str(len(list_of_files))+" files (either all data is not written yet or maybe XY grid definition is not proper)")
    digits = len(str(count_global))
    digits = max(digits,4)
    for ii in range(count_global):
        text = str(ii)
        if ii < 10000:
            string = text.zfill(4)
        else:
            string = text.zfill(5)
        file_name_temp = filenameDirec+'//'+experimental_prefix+string+'.'+format_file
        ## store it in a grid 
        filenm[ii] = file_name_temp

class Window(QWidget):#QWidget QScrollArea
    def __init__(self, winx=None, winy=None):
        super(Window, self).__init__()
        if winx==None or winy==None:
            self.setFixedSize(16777215,16777215)
        else:
            self.setFixedSize(winx, winy)
        self.setWindowTitle("Laue plot module")
        # self.myQMenuBar = QMenuBar(self) 
        self.layout = QVBoxLayout() # QGridLayout()
        self.canvas = MplCanvas(self, width=10, height=10, dpi=100)
        self.toolbar = NavigationToolbar(self.canvas, self)        
        self.canvas.mpl_connect('button_press_event', self.onclickImage)
        # set the layout
        self.popups = []
        self.layout.addWidget(self.toolbar, 0)
        self.layout.addWidget(self.canvas, 100)
        
        self.image_grid = QLineEdit()
        self.image_grid.setText("10,10")
        
        self.path_folder = QLineEdit()
        self.path_folder.setText("")
        
        # formLayout = QFormLayout()
        # # formLayout.setVerticalSpacing(5)
        # formLayout.addRow('Image XY grid size',self.image_grid)
        # formLayout.addRow('Directory of experimental images', self.path_folder)

        # self.layout.addLayout(formLayout)
        self.setLayout(self.layout)

        self.setLayout(self.layout)    
        self.draw_something()
        self.setFixedSize(16777215,16777215)
        
    def draw_something(self):
    # Drop off the first y element, append a new one.
        self.canvas.axes.cla()
        self.canvas.axes.set_title("Spatial scan Laue map", loc='center', fontsize=10)
        arr = np.random.randint(low = 0, high = 255, size = (lim_x, lim_y))
        self.canvas.axes.imshow(arr.astype('uint8'), origin='lower')        
        self.canvas.draw()
        
    def onclickImage(self, event123):
        if event123.button == 3:
            ix, iy = event123.xdata, event123.ydata
            try:
                ## read the saved COR file and extract exp spots info.## avoid zero index problem
                ix = int(round(ix))
                iy = int(round(iy))
                try:
                    # self.lim_x * self.lim_y
                    if iy == 0 and ix == 0:
                        image_no = 0
                    elif iy == 0 and ix != 0:
                        image_no = ix
                    elif iy != 0 and ix == 0:
                        image_no = iy * lim_y
                    elif iy != 0 and ix != 0:
                        image_no = iy * lim_y + ix
                        
                    path = os.path.normpath(filenm[image_no].decode())                    
                    Data, framedim, fliprot = IOimage.readCCDimage(path,
                                                                    stackimageindex=-1,
                                                                    CCDLabel=ccd_label,
                                                                    dirname=None,
                                                                    verbose=-1)   
                except:
                    print(path)
                    print('chosen pixel coords are x = %d, y = %d'%(ix, iy))
                    print("No IMAGE file could be found for the selected pixel")
                    return
                      
                w = MyPopup_image(ix, iy, path, Data)
                w.show()       
                self.popups.append(w)
                print('chosen pixel coords are x = %d, y = %d'%(ix, iy))
            except:
                return
        else:
            print("Right click for plotting the pixel values")

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)     
       
class MplCanvas1(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas1, self).__init__(self.fig)
        
class MyPopup_image(QWidget):
    def __init__(self, ix, iy, file, data):
        QWidget.__init__(self)

        self.layout = QVBoxLayout() # QGridLayout()
        self.canvas = MplCanvas1(self, width=10, height=10, dpi=100)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.iy,self.ix,self.file = iy, ix, file
        self.data = data
        # set the layout
        self.layout.addWidget(self.toolbar, 0)
        self.layout.addWidget(self.canvas, 100)

        self.ImaxDisplayed = np.max(data) - 0.1*np.max(data)
        self.IminDisplayed = np.average(data) - 0.1*np.average(data)

        self.slider = QSlider(QtCore.Qt.Horizontal, self)
        self.slider.setRange(minn, maxx)
        self.layout.addWidget(self.slider)
        self.slider.setValue(self.IminDisplayed)
        self.slider.valueChanged[int].connect(self.sliderMin)
        
        self.slider1 = QSlider(QtCore.Qt.Horizontal, self)
        self.slider1.setRange(minn, maxx)
        self.layout.addWidget(self.slider1)
        self.slider1.setValue(self.ImaxDisplayed)
        self.slider1.valueChanged[int].connect(self.sliderMax)

        self.setLayout(self.layout)
        self.draw_something()
    
    def draw_something(self):
        # Drop off the first y element, append a new one.
        self.canvas.axes.cla()
        self.canvas.axes.set_title("Laue pattern of pixel x=%d, y=%d (file: %s)"%(self.iy,self.ix,self.file), loc='center', fontsize=8)
        self.canvas.axes.set_ylabel(r'Y pixel',fontsize=8)
        self.canvas.axes.set_xlabel(r'X pixel', fontsize=8)
        # self.canvas.axes.imshow(data, origin='lower') 
        self.canvas.axes.imshow(self.data,interpolation="nearest",vmin=self.IminDisplayed, vmax=self.ImaxDisplayed)
                                 # norm=LogNorm(vmin=self.IminDisplayed, vmax=self.ImaxDisplayed))
                                 # Trigger the canvas to update and redraw.
        self.canvas.draw()
        
    def sliderMin(self, val):
        try:
            #slider control function
            if val > self.ImaxDisplayed:
                print("Min value cannot be greater than Max")
                self.draw_something()
                return
            self.IminDisplayed= val
            self.draw_something()
        except:
            print("Error: value", val)
            
    def sliderMax(self, val):
        try:
            #slider control function
            if val < self.IminDisplayed:
                print("Max value cannot be less than Min")
                self.draw_something()
                return
            self.ImaxDisplayed= val
            self.draw_something()
        except:
            print("Error: value", val)
            
def start():
    """ start of GUI for module launch"""
    app = QApplication(sys.argv)
    try:
        screen = app.primaryScreen()
        print('Screen: %s' % screen.name())
        size = screen.size()
        print('Size: %d x %d' % (size.width(), size.height()))
        rect = screen.availableGeometry()
        print('Available: %d x %d' % (rect.width(), rect.height()))
        win = Window(rect.width()//3, rect.height()//2)
    except:
        win = Window()
    win.show()
    sys.exit(app.exec_()) 

if __name__ == "__main__":
    start()

