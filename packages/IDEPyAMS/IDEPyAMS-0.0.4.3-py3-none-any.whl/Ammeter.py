#-------------------------------------------------------------------------------
# Name:        Voltmeter
# Author:      PyAMS
# Created:     16/12/2021
# Copyright:   (c) PyAMS
# Licence:     free
#-------------------------------------------------------------------------------

from PyAMS import model,signal,param
from signalType import current
from svg import svgElement

#Ammeter Model----------------------------------------------------------------
class Ammeter(model):
    def __init__(self, p, n):
        #Signal declarations----------------------------------------------------
        self.I = signal('in',current,p,n)

        #Get SVG Element By Id to desplay current value-------------------------
        self.display=svgElement('display');

    def output(self):
        #Desplay current value in SVG Element-----------------------------------
        self.display.textContent(self.I.getValue());

    def analog(self):
        pass;