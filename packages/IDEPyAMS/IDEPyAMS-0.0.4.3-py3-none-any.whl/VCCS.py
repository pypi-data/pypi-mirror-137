#-------------------------------------------------------------------------------
# Name:        VCCS
# Author:      PyAMS
# Created:     10/03/2017
# Modified:    25/01/2020
# Copyright:   (c) PyAMS
# Licence:     CC-BY-SA
#-------------------------------------------------------------------------------

from PyAMS import model,signal,param
from signalType import voltage,current

#Voltage-controlled current source Model----------------------------------------
class VCCS(model):
     def __init__(self,n1,n2,p1,p2):
        #Signals declarations---------------------------------------------------
         self.Vn = signal('in',voltage,n1,n2)
         self.Ip = signal('out',current,p1,p2)
        #Parameter declarations-------------------------------------------------
         self.G=param(1.0,' ','Gain multiplier')

     def analog(self):
         self.Ip+=self.G*self.Vn


