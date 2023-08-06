#-------------------------------------------------------------------------------
# Name:        Sine wave Current
# Author:      Dhiabi Fathi
# Created:     20/03/2015
# Modified:    05/04/2020
# Copyright:   (c) PyAMS
# Licence:     CC-BY-SA
#-------------------------------------------------------------------------------

from PyAMS import signal, param, model
from standardFunction import realTime
from signalType import current
from math  import sin, pi

#Sine wave Voltage  source------------------------------------------------------
class SinCurrent(model):
     def __init__(self, p, n):
         #Signal  declaration--------------------------------------------------
         self.I = signal('out',current,p,n)

         #Parameters declarations----------------------------------------------
         self.Fr=param(100.0,'Hz','Frequency of sine wave')
         self.Ia=param(10.0,'V','Amplitude of sine wave')
         self.Ph=param(0.0,'Deg','Phase of sine wave')
         self.Voff=param(0.0,'V','Voltage offset')
     def period(self):
          #Get per by cycle and phase-----------------------------------------
          return [(1/self.Fr,self.Ph*pi/180.0)]
     def analog(self):
          self.I+=self.Ia*sin(pi*2.0*self.Fr*realTime()+self.Ph*pi/180.0)+self.Voff
