
#-------------------------------------------------------------------------------
# Name:        SymbolEditor
# Author:      d.fathi
# Created:     19/08/2021
# Update:      01/01/2022
# Copyright:   (c) pyams 2022
# Web:         www.PyAMS.org
# Version:     0.0.4 (Pre-alpha)
# Licence:     free
# info:        Symbol Editor
#-------------------------------------------------------------------------------

import sys
sys.path+=["lib"]
sys.path+=["lib\\ui"]

from PyQt5.QtWidgets import QApplication,QMainWindow
from mainwindow import Ui_MainWindow
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebChannel import QWebChannel
from appcir import getListSignalsNodeParams,interAnalysis
from dialogs import *
import appcir


#-------------------------------------------------------------------------------
# class Document: Used to connect to a web document (index.html)
#-------------------------------------------------------------------------------
class Document(QObject):

    def __init__(self,setWin):
        super(Document, self).__init__()
        self.setWin=setWin;
        self.typeSym=True

    @pyqtSlot(list)
    def getRef(self, o):
        d=o[0]
        self.setWin.updatWin(d);

    @pyqtSlot(result=bool)
    def newPage(self):
        return self.typeSym

    @pyqtSlot(list,result=list)
    def return_list(self,l):
        return appcir.interAnalysis(l,self.setWin);



    @pyqtSlot(int)
    def setInt(self, i):
        print(i+1)

    @pyqtSlot(list)
    def setList(self, i):
        print(sum(i))

    @pyqtSlot(bool)
    def itRun(self,bool_arg):
        self.setWin.ui.actionRun.setEnabled(not(bool_arg));
        self.setWin.ui.actionPause.setEnabled(bool_arg);

    @pyqtSlot(str, result=str)
    def jscallme(self, str_args):
        print('call received')
        print('resolving......init home..')
        print(str_args)

    @pyqtSlot(str, result=str)
    def getProbeValue(self, str_args):
        print(str_args);
        self.setWin.updatePosProbe();


#-------------------------------------------------------------------------------
# class Frame: create a frame in the status bar
#-------------------------------------------------------------------------------
class VLine(QFrame):
    def __init__(self):
        super(VLine, self).__init__()
        self.setFrameShape(self.VLine|self.Sunken)

#-------------------------------------------------------------------------------
# class Mainwindow: intrface of symbol editor
#-------------------------------------------------------------------------------
class Mainwindow:
    def __init__(self):
        self.w = QMainWindow()

        self.path='';
        self.pathLib='';

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.w)
        self.filetype="symbol file (*.sym)";
        self.filenew='NewFile.sym';
        self.filename='NewFile.sym';
        self.title='Symbol Editor';
        self.pagetype='sym';
        self.modified=False;
        self.typeAction='none';

        self.ui.m_webview.page().setUrl(QUrl("qrc:/index.html"));
        self.ui.statusbar.showMessage('Message in statusbar.');
        self.updateStatubar();
        self.my_document= Document(self);
        self.channel = QWebChannel();
        self.channel.registerObject('document', self.my_document)
        self.ui.m_webview.page().setWebChannel(self.channel);

        self.ui.actionOpen.triggered.connect(self.open);
        self.ui.actionSave.triggered.connect(self.save);
        self.ui.actionSave_as.triggered.connect(self.saveAs);
        self.ui.actionNew.triggered.connect(self.new);
        self.ui.actionPolarity.triggered.connect(self.showPolarity);
        self.ui.actionShow_grid.triggered.connect(self.showGrid);

        self.ui.menuTools.menuAction().setVisible(True);
        self.ui.ToolsToolBar.setVisible(False);
        self.ui.menuRun.menuAction().setVisible(False);
        self.ui.RunToolBar.setVisible(False);
        self.ui.actionFlipHorizontal.setVisible(False);
        self.ui.actionFlipVertically.setVisible(False);
        self.ui.actionRotate.setVisible(False);

        self.ui.actionZoom_In.triggered.connect(lambda: self.ui.m_webview.page().runJavaScript("ioZoomIn();"));
        self.ui.actionZoom_Out.triggered.connect(lambda: self.ui.m_webview.page().runJavaScript("ioZoomOut();"));
        self.ui.actionUndo.triggered.connect(lambda: self.ui.m_webview.page().runJavaScript("ioUndo();"));
        self.ui.actionRedo.triggered.connect(lambda: self.ui.m_webview.page().runJavaScript("ioRedo();"));
        self.ui.actionCopy.triggered.connect(lambda: self.ui.m_webview.page().runJavaScript("ioCopy();"));
        self.ui.actionCut.triggered.connect(lambda: self.ui.m_webview.page().runJavaScript("ioCut();"));
        self.ui.actionPaste.triggered.connect(lambda: self.ui.m_webview.page().runJavaScript("ioPast();"));

        self.ui.actionPin.triggered.connect(lambda: self.ui.m_webview.page().runJavaScript("addShape('pin');"));
        self.ui.actionReference_2.triggered.connect(lambda: self.ui.m_webview.page().runJavaScript("addShape('ref');"));
        self.ui.actionRect.triggered.connect(lambda: self.ui.m_webview.page().runJavaScript("addShape('rect');"));
        self.ui.actionEllipse.triggered.connect(lambda: self.ui.m_webview.page().runJavaScript("addShape('ellipse');"));
        self.ui.actionParamater.triggered.connect(lambda: self.ui.m_webview.page().runJavaScript("addShape('param');"));
        self.ui.actionPolyline.triggered.connect(lambda: self.ui.m_webview.page().runJavaScript("addShape('polyline');"));
        self.ui.actionWire.triggered.connect(lambda: self.ui.m_webview.page().runJavaScript("addShape('net');"));
        self.ui.actionText.triggered.connect(lambda: self.ui.m_webview.page().runJavaScript("addShape('text');"));
        self.ui.actionOscilloscope.triggered.connect(lambda: self.ui.m_webview.page().runJavaScript("addShape('oscilloscope');"));
        self.ui.actionPolygon.triggered.connect(lambda: self.ui.m_webview.page().runJavaScript("addShape('polygon');"));
        self.ui.actionArc.triggered.connect(lambda: self.ui.m_webview.page().runJavaScript("addShape('arc');"));
        self.ui.actionGnd.triggered.connect(lambda: self.ui.m_webview.page().runJavaScript("addGnd();"));
        self.ui.actionProbe.triggered.connect(lambda: self.ui.m_webview.page().runJavaScript("addShape('probe');"));
        self.ui.actionEnd.triggered.connect(lambda: self.ui.m_webview.page().runJavaScript("ioEndDrawing();"));
        self.ui.actionSVGExport.triggered.connect(lambda: self.ui.m_webview.page().runJavaScript("savePageToSVG(1.5)",self.exportSVG));
        self.ui.actionFlipHorizontal.triggered.connect(lambda: self.ui.m_webview.page().runJavaScript("ioTypeRotation('flipHorizontal');"));
        self.ui.actionFlipVertically.triggered.connect(lambda: self.ui.m_webview.page().runJavaScript("ioTypeRotation('flipVertical');"));
        self.ui.actionRotate.triggered.connect(lambda: self.ui.m_webview.page().runJavaScript("ioTypeRotation('rotate');"));
        self.ui.m_webview.setContextMenuPolicy(Qt.CustomContextMenu);
        self.ui.m_webview.customContextMenuRequested.connect(self.openMenu);
  #actionShow_grid
        self.ui.actionAbout.triggered.connect(self.about);
        self.w.closeEvent=self.closeEvent


    def openMenu(self,position):
        contextMenu = QMenu();
        contextMenu.addAction(self.ui.actionEnd);
        contextMenu.addSeparator();
        contextMenu.addAction(self.ui.actionCopy);
        contextMenu.addAction(self.ui.actionCut);
        contextMenu.addAction(self.ui.actionPaste);
        action = contextMenu.exec_(self.ui.m_webview.mapToGlobal(position))




    def caption(self):
        self.ui.actionSave.setEnabled(self.modified);
        if self.modified :
            f=self.filename+'*';
        else:
            f=self.filename;
        self.w.setWindowTitle(self.title+"["+f+"]");


    def dialogeListSignalsNodeParamsFromCircuit(self,result):
        data=getListSignalsNodeParams(self,result);
        dialog =dialogListSignalsParamaters(data);
        dialog.w.setWindowTitle("Lists of signals paramatres and nodes");
        dialog.w.setWindowIcon(QIcon(":/image/logo.png"));
        if dialog.w.exec_():
            self.ui.m_webview.page().runJavaScript("ioSetPosProbe('"+dialog.pos+"');");

    def about(self):
        dialog =about();
        dialog.w.exec_();


    def updatePosProbe(self):
        self.ui.m_webview.page().runJavaScript("ioGetProbesWithNetList();", self.dialogeListSignalsNodeParamsFromCircuit);


    def updatWin(self,dic):
        self.lbl1.setText('(X,Y)='+str(dic['x'])+','+str(dic['y']));
        self.lbl2.setText('Zoom='+dic['zoom']);
        self.ui.actionCut.setEnabled(dic['select']);
        self.ui.actionCopy.setEnabled(dic['select']);
        self.ui.actionPaste.setEnabled(dic['past']);
        self.ui.actionUndo.setEnabled(dic['undo']);
        self.ui.actionRedo.setEnabled(dic['redo']);
        self.ui.actionEnd.setChecked(dic['endDrawing']);
        self.ui.actionFlipHorizontal.setEnabled(dic['selectPart']);
        self.ui.actionFlipVertically.setEnabled(dic['selectPart']);
        self.ui.actionRotate.setEnabled(dic['selectPart']);
        self.ui.actionPolarity.setChecked(dic['showPolarity']);
        self.modified=dic['modified'];
        self.ui.statusbar.showMessage(dic['undoPos']);
        self.caption();


    def __save(self, response):
        file = open(self.filename,'w', encoding="utf-8")
        file.write(response)
        file.close();
        self.getTypeAction();

    def getTypeAction(self):
        if self.typeAction=='open':
           self.open();
        elif self.typeAction=='new':
           self.new();
        self.typeAction='none';


    def shakeSave(self):
        if self.modified:
            ret = QMessageBox.question(None, 'MessageBox', "Save changes ", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
            if ret == QMessageBox.Yes:
                self.save();
                return not(self.modified);
            elif ret == QMessageBox.No:
                return True;
            else:
                self.typeAction='none';
                return False;
        return True;

    def show(self):
        self.w.show()


    def new(self):
        self.typeAction='new';
        if self.shakeSave():
            self.typeAction='none';
            self.filename=self.filenew;
            self.ui.m_webview.page().runJavaScript("ioNewPage('"+self.pagetype+"');");


    def open(self):
        self.typeAction='open';
        if self.shakeSave():
            fname = QFileDialog.getOpenFileName(None, 'Open file',self.pathLib,self.filetype)
            if(fname[0]!=''):
                self.typeAction='none';
                self.filename=fname[0];
                f = open(fname[0], 'r', encoding="utf-8")
                s=f.read()
                self.ui.m_webview.page().runJavaScript("ioSetSymbol(`"+s+"`);");


    def save(self):
        if  self.filename==self.filenew:
            self.saveAs();
        else:
            self.ui.m_webview.page().runJavaScript("ioGetSymbol();", self.__save);


    def saveAs(self):
        fname = QFileDialog.getSaveFileName(None, 'Save File',self.pathLib,self.filetype)
        if(fname[0]!=''):
            self.filename=fname[0];
            self.ui.m_webview.page().runJavaScript("ioGetSymbol();", self.__save);
        else:
            self.typeAction='none';

    def exportSVG(self, response):
        fname = QFileDialog.getSaveFileName(None, 'Save File to SVG form',' ',"svg file (*.svg)")
        if(fname[0]!=''):
            response=response;
            file = open(fname[0],'w', encoding="utf-8")
            file.write(response)
            file.close()

    def updateStatubar(self):
        self.lbl1 = QLabel("Pos: ")
        self.lbl1.setStyleSheet('border: 0; color:  blue;')
        self.lbl2 = QLabel("zoom: ")
        self.lbl2.setStyleSheet('border: 0; color:  red;')
        self.lbl3 = QLabel("___")
        self.lbl3.setStyleSheet('border: 0; color:  red;')

        self.ui.statusbar.reformat()
        self.ui.statusbar.setStyleSheet('border: 0; background-color: #FFF8DC;')
        self.ui.statusbar.setStyleSheet("QStatusBar::item {border: none;}")

        self.ui.statusbar.addPermanentWidget(VLine())
        self.ui.statusbar.addPermanentWidget(self.lbl3)
        self.ui.statusbar.addPermanentWidget(VLine())
        self.ui.statusbar.addPermanentWidget(self.lbl1)
        self.ui.statusbar.addPermanentWidget(VLine())
        self.ui.statusbar.addPermanentWidget(self.lbl2)



    def copy(self):
        self.r=Mainwindow();
        self.r.show();

    def showPolarity(self):
        if self.ui.actionPolarity.isChecked():
            self.ui.m_webview.page().runJavaScript("showPolarity(true);");
        else:
            self.ui.m_webview.page().runJavaScript("showPolarity(false);");

    def showGrid(self):
        if self.ui.actionShow_grid.isChecked():
            self.ui.m_webview.page().runJavaScript("drawing.showGrid(true);");
        else:
            self.ui.m_webview.page().runJavaScript("drawing.showGrid(false);");

    def closeEvent(self, event):
        if self.shakeSave():
            event.accept()
        else:
            event.ignore()



#-------------------------------------------------------------------------------
# __main__: start Symbol Editor software
#-------------------------------------------------------------------------------

def exec():
        app=QApplication(sys.argv);
        import os
        import mainwindow
        path = os.path.dirname(mainwindow.__file__)
        path=path.lower();
        r=path.replace('\\','/');
        w=Mainwindow();
        w.show();
        w.path=r
        w.pathLib=r+'/symbols'
        sys.exit(app.exec_());

