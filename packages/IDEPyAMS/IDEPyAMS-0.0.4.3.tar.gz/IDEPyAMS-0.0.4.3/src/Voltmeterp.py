#-------------------------------------------------------------------------------
# Name:        Voltmeter
# Author:      PyAMS
# Created:     16/12/2021
# Copyright:   (c) PyAMS
# Licence:     free
#-------------------------------------------------------------------------------

from PyAMS import model,signal,param
from signalType import voltage
from svg import svgElement

#Voltmeter Model----------------------------------------------------------------
class Voltmeterp(model):
    def __init__(self, p, n):
        #Signal declarations---------------------------------------------------
        self.V = signal('in',voltage,p,n)

        #Get SVG Element By Id to desplay voltage value-------------------------
        self.display=svgElement('display');

    def output(self):
        #Desplay voltage value in SVG Element-----------------------------------
        self.display.textContent(self.V.getValue());

    def analog(self):
        pass;
