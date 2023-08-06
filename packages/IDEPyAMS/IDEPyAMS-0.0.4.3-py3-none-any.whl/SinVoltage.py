#-------------------------------------------------------------------------------
# Name:        Sine wave Voltage
# Author:      Dhiabi Fathi
# Created:     20/03/2015
# Modified:    30/10/2021
# Copyright:   (c) PyAMS
# Licence:     CC-BY-SA
#-------------------------------------------------------------------------------

from PyAMS import signal, param, model
from standardFunction import realTime
from signalType import voltage
from math  import sin, pi

#Sine wave Voltage  source------------------------------------------------------
class SinVoltage(model):
     def __init__(self, p, n):
         #Signal  declaration--------------------------------------------------
         self.V = signal('out',voltage,p,n)

         #Parameters declarations----------------------------------------------
         self.Fr=param(100.0,'Hz','Frequency of sine wave')
         self.Va=param(10.0,'V','Amplitude of sine wave')
         self.Ph=param(0.0,'Deg','Phase of sine wave')
         self.Voff=param(0.0,'V','Voltage offset')
     def period(self):
          #Get per by cycle and phase-----------------------------------------
          return [(1/self.Fr,self.Ph*pi/180.0)]
     def analog(self):
          self.V+=self.Va*sin(pi*2.0*self.Fr*realTime()+self.Ph*pi/180.0)+self.Voff
