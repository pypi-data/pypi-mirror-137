#-------------------------------------------------------------------------------
# Name:        simu
# Author:      d.fathi
# Created:     20/06/2017
# Update:      06/10/2021
# Copyright:   (c) pyams
# Web:         www.PyAMS.org
# Licence:     free
#-------------------------------------------------------------------------------


from PyAMS import  analysis,getStepTime
from newton import solven
from option import simulationOption
from saveData import SaveInData,AddToData
from standardFunction import controlStepTime
import PyAMS
import time


#-------------------------------------------------------------------------------
# def addRefToModel: add reference to signals and parameters
#-------------------------------------------------------------------------------
def addRefToModel(R,M):
    M.name=R
    a=dir(M)
    for i in range(len(a)):
      f=eval('M.'+a[i])
      if type(f).__name__=='signal':
        f.name=R+'.'+a[i];
      if type(f).__name__=='param':
        f.name=R+'.'+a[i];

#-------------------------------------------------------------------------------
# class simu: circuit simulation
#-------------------------------------------------------------------------------
class simu:
    def __init__(self,cir,output,method,Option={}):
      getStepTime.__init__();
      simulationOption.setOption(Option)
      simulationOption.Run=False;
      self.n=0;
      self.method=method
      self.output=output
      self.GetResult=False;
      self.SweepUsed=False;
      self.SweepName='';
      self.SweepPos=0;
      self.SweepList=[]
      self.cir=cir
      self.method=method
      self.ProgressPosition=0
      self.LenSweepList=1;
      self.UsedTimeInter=False;
      self.stop=False;
      if 'sweep' in method:
          self.Sweep=method['sweep']
          self.SweepUsed=True;
          self.SweepPos=0;
          self.SweepParam=self.Sweep['param'];
          self.SweepList=self.Sweep['list'];
          self.LenSweepList=len(self.SweepList)
          self.SweepParam+=self.SweepList[0];
          self.SweepName=self.Sweep['param'].name+'='+str(self.SweepList[0])+self.Sweep['param'].Unit;
      self.StartTime = time.time()
      self.StartSimu();

    def StartSimu(self):

      if  self.method['mode']=='tran':

          PyAMS.time+=0.0
          self.Timestart=self.method['start'];
          self.Timestep=self.method['step'];
          self.Timestop=self.method['stop'];
          self.param=PyAMS.time;
          self.a=analysis(self.cir,self.method)
          self.leng=[self.a.len,self.a.les];
          simulationOption.SetTimeStep(self.Timestep)
          self.analyse_tr();

      if self.method['mode']=='int':
          Time+=0.0
          self.Timestart=self.method['start'];
          self.Timestep=self.method['step'];
          self.Timestop=self.method['stop'];
          self.UsedTimeInter=True;
          self.param=Time;
          self.a=analysis(self.cir,self.method)
          self.leng=[self.a.len,self.a.les];
          simulationOption.SetTimeStep(self.Timestep)
          self.analyse_InteractiveSimulation();


      if self. method['mode']=='dc':
              PyAMS.Time+=0.0
              self.DCstart=self.method['start'];
              self.DCstep=self.method['step'];
              self.DCstop=self.method['stop'];
              self.param=self.method['param'];
              self.a=analysis(self.cir,self.method)
              self.leng=[self.a.len,self.a.les];
              self.analyse_dc();

      if self. method['mode']=='ac':
              PyAMS.Time+=0.0
              self.ACstart=self.method['start'];
              a=pow(10.0,1/self.method['nstep']);
              self.ACstep=pow(10.0,a);
              self.ACstop=self.method['stop'];
              if 'interval' in self.method:
                if self.method['interval'] =='oct':
                    self.ACstep=pow(8.0,1/self.method['nstep']);
                elif self.method['interval'] =='lin':
                    self.ACstep=(self.ACstop-self.ACstart)/self.method['nstep'];

              self.a=analysis(self.cir,self.method)
              self.leng=[self.a.len,self.a.les];
              self.analyse_ac();



      if self.method['mode']=='op':
              PyAMS.time+=0.0
              self.method['mode']='op'
              self.a=analysis(self.cir,self.method)
              self.leng=[self.a.len,self.a.les];
              self.analyse_op();
#---------------------------------------------------------------------------
    def analyse_ac(self):
        self.analyse_op();
        self.a.getImpdence();
        self.ACVal=self.ACstart
        self.stop=False;
        def update():
            self.a.favelac(self.ACVal)
            SaveInData(self.a,self.SweepPos);
            self.ProgressPosition=self.ACVal*100/self.ACstop;
            if self.ACstop  < self.ACVal:
              self.StopAnalyse()
            self.ACVal+=self.ACstep;
        self.update=update


    def analyse_op(self):
          self.x=[]
          for i in range(self.a.len):
             self.x+=[0.0]
          self.y=self.a.favel;
          self.stop=False;

          def update():
            self.UsedResult=True
            self.x,s=solven(self.x,self.y)
            self.stop=True
          self.EndTime= time.time()
          self.update=update


#---------------------------------------------------------------------------
    def updaet_analyses(self):
              PyAMS.Time+=0.0
              self.a=analysis(self.cir,self.method)
              self.leng=[self.a.len,self.a.les];

    def analyse_tr(self):
          self.x=[]
          for i in range(self.a.len):
             self.x+=[0.0]
          self.y=self.a.favel;
          self.param.Val=0.0
          self.stop=False;
          simulationOption.start=True
          if simulationOption.ldt>0:
             simulationOption.TimeStep=GetStepTime.GetStepTime(SimulationOption.TimeStep)



          def update():
           # SimulationOption.TimeStep=0.00001;
            self.n=self.n+1
            PyAMS.time.Val=simulationOption.t1
            UsedTime=getStepTime.ControlPer();
            simulationOption.t1=PyAMS.time.Val
            self.x,s=solven(self.x,self.y)
            Time_Selection=controlStepTime(UsedTime)
            simulationOption.GetStep=simulationOption.t1-simulationOption.t0
            if Time_Selection or SimulationOption.Start:
                SaveInData(self.output,self.method)
            simulationOption.Start=False;
            self.ProgressPosition=((self.SweepPos+1)/self.LenSweepList)*self.param.Val*100/self.Timestop;

            if self.Timestop  < self.param.Val:
               self.StopAnalyse()

          self.update=update

    def analyse_InteractiveSimulation(self):
          self.x=[]
          for i in range(self.a.len):
             self.x+=[0.0]
          self.y=self.a.favel;
          self.param.Val=0.0
          self.stop=False;
          SimulationOption.Start=True
          if SimulationOption.ldt>0:
             SimulationOption.TimeStep=GetStepTime.GetStepTime(SimulationOption.TimeStep)



          def update():
            self.UsedResult=False;
            Time.Val=SimulationOption.t1
            print('Time.Val=',Time.Val)
            UsedTime=GetStepTime.ControlPer();
            self.x,s=solven(self.x,self.y)
            Time_Selection=ControlStepTime(UsedTime)
            SimulationOption.GetStep=SimulationOption.t1-SimulationOption.t0
            if Time_Selection or SimulationOption.Start:
                self.UsedResult=True;
            SimulationOption.Start=False;
          self.update=update


    def analyse_dc(self):
          self.x=[]
          for i in range(self.a.len):
             self.x+=[0.0]
          self.y=self.a.favel;
          self.DCVal_=self.DCstart
          self.stop=False;
          def update():
            self.n=self.n+1
            self.param.Val=self.DCVal_
            if not(solven(self.x,self.y)):
                hsolven(self.x,self.y);
            SaveInData(self.a,self.SweepPos);
            self.ProgressPosition=((self.SweepPos+1)/self.LenSweepList)*self.DCVal_*100/self.DCstop;
            if self.DCstop  < self.DCVal_:
              self.StopAnalyse()
            self.DCVal_+=self.DCstep;
          self.update=update






    def StopAnalyse(self):
        if not(self.SweepUsed):
           self.stop=True
        else:
         self.SweepPos=self.SweepPos+1
         if len(self.SweepList) > self.SweepPos:
          self.SweepParam+=self.SweepList[self.SweepPos];
          self.SweepName=self.Sweep['param'].name+'='+str(self.SweepList[self.SweepPos])+self.Sweep['param'].Unit;
          self.StartSimu();
         else:
              self.stop=True
        if self.stop:
            self.EndTime= time.time()
        #-------------




#-------------------------------------------------------------------------------
# class AppPyAMS: Application  PyAMS for: In and out data
#-------------------------------------------------------------------------------

class AppPyAMS:

    def __init__(self,UsedPyAMSSoft=True):
        self.UsedPyAMSSoft=UsedPyAMSSoft
        self.cir=[]
        self.option={}
        self.Result_=[]
        self.LenOut=0
        self.SweepMethod=''
        self.OutPut=[]


    def circuit(self,*elements):
        n=len(elements);
        self.cir=[]

        self.elements={}
        if n==1:
            self.elements=elements[0];
        elif n>1:
            for i in range(n):
                k='E'+str(i+1);
                self.elements[k]=elements[i];


        a=list(self.elements.values())
        k=list(self.elements.keys())
        for i in range(0,len(a)):
            addRefToModel(k[i],a[i])
            self.cir+=[a[i]]


    def setOut(self,*outPuts):
            self.outPuts=outPuts;

    def getOut(self):
        self.Result_=[]
        for i in range(len(self.outPuts)):
            if(type(self.outPuts[i])==str):
                t=self.sium.a.getoutput_(self.outPuts[i])
                self.Result_+=[PyAMS.floatToStr(t)+'V']
            else:
                self.Result_+=[self.outPuts[i].__str__()]
        return self.Result_;

    def getTime(self):
        return PyAMS.time.__Str__();

    def getDataPlot(self):
        self.Result_=[]
        for i in range(len(self.outPuts)):
            t=self.outPuts[i]
            if (type(t)==str):
              self.Result_+=[self.sium.a.getoutput_(t)]
            else:
              self.Result_+=[self.outPuts[i].Val]

        self.Result_+=[PyAMS.time.Val];
        return self.Result_;


    def getUnit(self):
        a=self.outPuts;
        self.Units=[]
        for i in range(0,len(a)):
         self.Units+=[self.sium.a.getunits_(a[i])]
        return self.Units

    def sweep(self,SweepMethod):
            self.SweepMethod=SweepMethod

    def analysis(self,**analysisMethod):
            self.Analysis=analysisMethod

    def setOption(self,option):
            self.option=option




    def run(self,Exc=False,File='',saveToFile=False):
        if self.SweepMethod !='':
           self.Analysis['sweep']=self.SweepMethod
        AddToData(self.outPuts,self.Analysis);
        self.sium=simu(self.cir,self.outPuts,self.Analysis,self.option)
        simulationOption.len=self.sium.a.len-self.sium.a.les
        simulationOption.les=self.sium.a.les
        self.feavl=self.sium.update
        if Exc:
          import sys
          fill = '█'
          j=0;
          while not(self.sium.stop):
              self.feavl()
              i=int(self.sium.ProgressPosition)
              if(i>=j):
               sys.stdout.write('\r')
               sys.stdout.write("Progress: %-99s %d%%" % (fill*i, i))
               sys.stdout.flush()
               j=j+20;

          if saveToFile:
            self.saveAllDataToFile(File)
          print("\n ---------------------------------------------------------------------------------------------")
          print("\nElapsed (with compilation and simulation) = %s" % (self.sium.EndTime - self.sium.StartTime))
          print("\n ---------------------------------------------------------------------------------------------")

          #print("Length ="+str(self.sium.n))
          #SaveDataInSignalParam()

    def setPageWeb(self,page):
        self.sium.a.pageWeb(page)
    def update(self):
         self.feavl();
         self.sium.a.printout();

    def getValTran(self,l):
        '''
        t=[]
        for i in range(len(l)):
            r=l[i]+'.Val';
            t+=[eval(r)];
        '''
        return [self.cir['V1'].V.Val];



    def SaveResultToFile(self,FileName):
        print(FileName);
        SaveDataToFile(FileName)

    def data(self,name):
        if type(name)==str:
          return getData(name)
        else:
          return getData(name.name)


    def unit(self,name):
        if type(name)==str:
          return 'V'
        else:
          return name.Unit

    def saveAllDataToFile(self,File):
           Units=[];
           with open(File, 'w') as output:
                    output.write(str(100) + '\n')
                    if self.Analysis['mode']=='dc':
                      output.write(str(self.data(self.Analysis['param'])) + '\n')
                      Units+=[self.unit(self.Analysis['param'])]
                    else:
                      output.write(str(self.data('Time')) + '\n')
                      Units+=['Sec']
                    for i in range(len(self.OutPut)):
                        output.write(str(self.data(self.OutPut[i])) + '\n')
                        Units+=[self.unit(self.OutPut[i])]
                    output.write(str(Units) + '\n')
                    output.write(str(101) + '\n')


    def dataAmplitude(self,name):
        if type(name)==str:
          a=getData(name)
        else:
          a=getData(name.name)
        d=[abs(number) for number in a]
        return d

    def datadB(self,name):
        from math import log10
        if type(name)==str:
          a=getData(name)
        else:
          a=getData(name.name)
        d=[20*log10(abs(number)) for number in a]
        return d

    def dataPhase(self,name):
        from math import atan,pi
        from cmath import phase
        if type(name)==str:
          a=getData(name)
        else:
          a=getData(name.name)
        d=[phase(num)*180/pi for num in a]
        return d


AppPyAMS=AppPyAMS()

