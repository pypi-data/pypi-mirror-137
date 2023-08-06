#-------------------------------------------------------------------------------
# Name:        VCVS
# Author:      PyAMS
# Created:     10/03/2017
# Modified:    25/01/2020
# Copyright:   (c) PyAMS
# Licence:     CC-BY-SA
#-------------------------------------------------------------------------------

from PyAMS import model,signal,param
from signalType import voltage


#Voltage-controlled voltage source Model----------------------------------------
class VCVS(model):
     def __init__(self,n1,n2,p1,p2):
        #Signals declarations---------------------------------------------------
         self.Vn = signal('in',voltage,n1,n2)
         self.Vp = signal('out',voltage,p1,p2)
        #Parameter declarations-------------------------------------------------
         self.G=param(1.0,' ','Gain multiplier')

     def analog(self):
         self.Vp+=self.G*self.Vn


