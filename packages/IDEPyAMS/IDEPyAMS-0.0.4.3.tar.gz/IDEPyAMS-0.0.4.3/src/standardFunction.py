#-------------------------------------------------------------------------------
# Name:        Standard Function
# Author:      d.fathi
# Created:     13/04/2020
# Copyright:   (c) PyAMS 2020
# Licence:     unlicense
#-------------------------------------------------------------------------------

from PyAMS import time,getStepTime,temp,tnom
from option import simulationOption
from math import sqrt,exp


#-------------------------------------------------------------------------------
# def acSim:AC stimulus function
#-------------------------------------------------------------------------------

def acSim(mag,phase):
    if ModAnaly.getSource:
        return 1
    return 0
    #return   mag*(cos(phase)+sin(phase)*(1j))


#-------------------------------------------------------------------------------
# def temperature: get temperature of circuit in Kelvin
#-------------------------------------------------------------------------------
def temperature():
    return 273.15+temp;


#-------------------------------------------------------------------------------
# def vth: get thermal voltage
#-------------------------------------------------------------------------------
def vth(t=tnom):
    #thermal voltage
    return 8.6173303e-5*t

#-------------------------------------------------------------------------------
# def qtemp: get quadratic temperature
#-------------------------------------------------------------------------------
def qtemp(TC1,TC2):
    return (1+TC1*(temp-tnom)+TC2*(temp-tnom)*(temp-tnom))


#-------------------------------------------------------------------------------
# def explim: exponential limit function
#-------------------------------------------------------------------------------
def  explim(a):
     if a>=100.0:
          return (a-99.0)*exp(100.0)
     return exp(a)


#Computer Aided Engineering for Integrated Circuits
#ECE 570

ITL4=0;
ListSignalDdt=[];

dt1=1e-12;
Err=1e-18;
dt0=1e-7
dtr=0.0
h=[0.0,0.0,0.0,0.0]


#-------------------------------------------------------------------------------
# def ddt: calculate the signal derivative by time.
#-------------------------------------------------------------------------------

def ddt(Signal,InitialValue=0.0):

    if ModAnaly.ModeDC:
        return 0.0
    if ModAnaly.ModeAC:
        return Signal.Valac

    try:
        dt=abs(SimulationOption.t1-SimulationOption.t0);#;

        if dt >0.0:
            #Method Integration Trapezoidal order 2
            if SimulationOption.Trapezoidal:
             Signal.V1=Signal.Val;
             Signal.dVr=(Signal.V1-Signal.V0)/dt
             Signal.dV=2*Signal.dVr-Signal.dV0

        return Signal.dV
    except:
        global ListSignalDdt
        ListSignalDdt+=[Signal]
        SimulationOption.ldt=len(ListSignalDdt)
        if  (type(InitialValue)==int) or  (type(InitialValue)==float) :
            Signal.V0=InitialValue
        else:
            Signal.V0=InitialValue.Val
        Signal.V1=0.0
        Signal.dV0=0.0
        Signal.DD1=[0.0,0.0]
        Signal.DD2=[0.0,0.0]
        Signal.DD3=[0.0,0.0]
        Signal.dt=[0.0,0.0,0.0]
        Signal.dV=0.0
        Signal.dVr=0.0
        if dt >0.0:
             Signal.dVr=(Signal.V1-Signal.V0)/dt
             Signal.dV=2*Signal.dVr-Signal.dV0
        return Signal.dV


#-------------------------------------------------------------------------------
# def control: find step time
#-------------------------------------------------------------------------------
def controlStepTime(UsedTime):

        if (simulationOption.ldt==0):
            simulationOption.t0=time.Val;
            simulationOption.t1=simulationOption.t1+simulationOption.TimeStep;
            return True

        global ListSignalDdt,dt0,dt1,h,ITL4,Err,dtr


        if SimulationOption.t1==0.0:
           dt1=SimulationOption.TimeStep
           dtr=min(1e-16,  SimulationOption.TimeStep/100);
           SimulationOption.t0=Time.Val;
           SimulationOption.t1=min(1e-16,SimulationOption.TimeStep/100);
           SimulationOption.UsedThise=True
           print('ust1=',SimulationOption.t1)
           return True;

        '''
        if UsedTime:


            for i in range(len(ListSignalDdt)):
              Signal=ListSignalDdt[i]
              Signal.DD1[0]=Signal.DD1[1]
              Signal.DD2[0]=Signal.DD2[1]
              Signal.dV0=Signal.dV
              Signal.V0=Signal.V1

            h[0]=h[1]
            h[1]=h[2]
            dtr=min(h);
            if(dtr < Err):
                dtr=SimulationOption.TimeStep/1e+6;

            SimulationOption.t0=Time.Val;
            SimulationOption.t1=SimulationOption.t1+dtr;
            Time_Selection=True
            return True


        '''

        dt=SimulationOption.t1-SimulationOption.t0;
        if dt <=Err:
            if(dtr > Err):
              dt=dtr
            else:
              dt=SimulationOption.TimeStep/1e+8


        LTE=[dt]

        h[2]=dt
        t1=h[2]+h[1]
        t2=h[2]+h[1]+h[0]
       # print('t1',t1)

        for i in range(len(ListSignalDdt)):
          Signal=ListSignalDdt[i]
          Signal.DD1[1]=Signal.dVr


          if t1 > Err:
            Signal.DD2[1]=(Signal.DD1[1]-Signal.DD1[0])/t1
            Signal.DD3[1]=(Signal.DD2[1]-Signal.DD2[0])/t2
            if (h[2]>Err):
             Ex=SimulationOption.RELTOL*max(abs(Signal.V0),abs(Signal.V1),Signal.Chgtol)/h[2]
             Edx=(Signal.Abstol+SimulationOption.RELTOL*max(abs(Signal.dV),abs(Signal.dV0)))
             EB=max(Ex,Edx)
             er=sqrt(EB/max(Signal.Abstol,abs(Signal.DD3[1])/12))
             if (er>0.0):
                  LTE+=[er]


        DH=min(LTE);
        #print(LTE)
        #print('DH=',DH)
        #print('0.9*dt=',0.9*dt)

        Time_Selection=False;
        if (0.9*dt>DH):
            SimulationOption.t1=SimulationOption.t0+DH
            Time_Selection=False;
            ITL4=ITL4+1
            if(ITL4>SimulationOption.ITL4):
                ITL4=0;
                Time_Selection=True;
        else:
            if ITL4 > 10:
              print(ITL4)
            dtr=dt;
            dt=min(2*dt,SimulationOption.TimeStep)
            Time_Selection=True;
            #print(dt)
            ITL4=0;





        if Time_Selection or UsedTime:

            for i in range(len(ListSignalDdt)):
              Signal=ListSignalDdt[i]
              Signal.DD1[0]=Signal.DD1[1]
              Signal.DD2[0]=Signal.DD2[1]
              Signal.dV0=Signal.dV
              Signal.V0=Signal.V1

            h[0]=h[1]
            h[1]=h[2]


            SimulationOption.t0=Time.Val
            SimulationOption.t1=SimulationOption.t1+dt;
            Time_Selection=True



        return Time_Selection;



#-------------------------------------------------------------------------------
# def trap: trap function
#-------------------------------------------------------------------------------

def trap(V1,V2,Td,Tr,Pw,Tf,T):
        global GetStepTime,Time
        b=(V1,V2,Td,Tr,Pw,Tf,T)
        v=GetStepTime.indexTrap(b)
        [S,T,a,b,c]=GetStepTime.List[v]
        len_=len(b)
        y2=0.0
        for i in range(len_-1):
            y1,x1=c[i],a[i]
            y2,x2=c[i+1],a[i+1]
            u1,u2=b[i],b[i+1]
            if u2:
              if x1==x2:
                if u1:
                    return V1
                else:
                    return V2
              else:
                   a_=(y1-y2)/(x1-x2)
                   b_=y1-a_*x1
                   return a_*Time+b_
        return y2


#-------------------------------------------------------------------------------
# def puls: puls function
#-------------------------------------------------------------------------------
def puls(Va,T):
    dT=T/1e+7;
    return trap(Va,0,dT,dT,T/2,dT,T)



#-------------------------------------------------------------------------------
# def realTime: get real time
#-------------------------------------------------------------------------------
def realTime():
     global time
     return time;

