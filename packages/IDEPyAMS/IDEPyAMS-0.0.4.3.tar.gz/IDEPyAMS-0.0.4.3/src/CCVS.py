#-------------------------------------------------------------------------------
# Name:        CCVS
# Author:      Dhiabi Fathi
# Created:     10/03/2017
# Modified:    24/01/2020
# Copyright:   (c) PyAMS
# Licence:     CC-BY-SA
#-------------------------------------------------------------------------------

from PyAMS import model,signal,param
from signalType import voltage,current


#Current-controlled voltage source Model----------------------------------------
class CCVS(model):
     def __init__(self,n1,n2,p1,p2):
        #Signals declarations---------------------------------------------------
         self.In = signal('in',current,n1,n2)
         self.Vp = signal('out',voltage,p1,p2)
        #Parameter declarations-------------------------------------------------
         self.G=param(1.0,'Ohm','Gain multiplier')

     def analog(self):
         self.Vp+=self.G*self.In


