#-------------------------------------------------------------------------------
# Name:        Resistor
# Author:      PyAMS
# Created:     20/03/2015
# Modified:    01/04/2020
# Copyright:   (c) PyAMS
# Licence:     free
#-------------------------------------------------------------------------------

from PyAMS import model,signal,param
from signalType import voltage,current

#Resistor Model-----------------------------------------------------------------
class Resistor(model):
    def __init__(self, p, n):
        #Signals declarations---------------------------------------------------
        self.V = signal('in',voltage,p,n)
        self.I = signal('out',current,p,n)

        #Parameters declarations------------------------------------------------
        self.R=param(1000.0,'Ω','Resistance value')


    def analog(self):
        #Resistor equation-low hom (I=V/R)------------------------------------
        self.I+=self.V/self.R
