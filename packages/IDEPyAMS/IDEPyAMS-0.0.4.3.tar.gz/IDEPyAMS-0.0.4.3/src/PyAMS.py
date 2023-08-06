#-------------------------------------------------------------------------------
# Name:        PyAMS
# Author:      d.fathi
# Created:     20/03/2015
# Update:      02/10/2021
# Copyright:   (c) pyams
# Web:         www.PyAMS.org
# Licence:     free
#-------------------------------------------------------------------------------

import math;

#-------------------------------------------------------------------------------
# def floatToStr: convert float to string
#-------------------------------------------------------------------------------
def floatToStr(value):
    units={'f':1e-15,'p':1e-12,'n':1e-9,'µ':1e-6,'m':1e-3,' ':1.0,'k':1e+3,'M':1e+6,'T':1e+9}
    v=list(units.values())
    k=list(units.keys())
    sign=math.copysign(1, value)
    value=abs(value)
    for i in range(len(v)-1, 0, -1):
       if(value>=(v[i])):
        f=format(sign*value/v[i],'.2f')
        lf=len(f)
        if(f[lf-1]=='0'):
          f=f[:lf-1]
        lf=len(f)
        if(f[lf-1]=='0'):
          f=f[:lf-1]
          f=f[:lf-2]
        return f+k[i]
    return str(sign*value);

#-------------------------------------------------------------------------------
# def strToFloat: convert string to  float
#-------------------------------------------------------------------------------

def strToFloat(value):
    num='0'
    uni=''
    units={'f':1e-15,'p':1e-12,'n':1e-9,'µ':1e-6,'m':1e-3,' ':1.0,'k':1e+3,'K':1e+3,'M':1e+6,'T':1e+9}
    m=1.0;
    value=value+' ';

    for i in range(len(value)):
        if value[i] in ['0','1','2','3','4','5','6','7','8','9','+','-','e','.']:
           num=num+value[i];
        else:
           uni=value[i];
           m=float(num);
           if uni in units:
             m=m*units[uni];
           break;
    return m;



#-------------------------------------------------------------------------------
# class model: object of model
#-------------------------------------------------------------------------------


class model(object):
    def __init__(self):
        self.Values='';

    def getSignals(self):
        self.signals=[]
        a=dir(self);
        for i in range(0,len(a)):
          f=eval('self.'+a[i])
          if type(f).__name__=='signal':
            self.signals+=[eval('self.'+a[i])]
        return self.signals;

    def getParamaters(self):
        self.params=[]
        a=dir(self);
        for i in range(0,len(a)):
          f=eval('self.'+a[i])
          if type(f).__name__=='param':
            self.params+=[eval('self.'+a[i])]
        return self.params;

    def getIndex(self,node):
        n=len(self.signals)
        for i in range(n):
            if self.signals[i].Porta in node:
               self.signals[i].Indxa=node.index(self.signals[i].Porta)
            if self.signals[i].Portb in node:
               self.listSignals[i].Indxb=node.index(self.signals[i].Portb)



    def getout(self):
        print(dir(self))
    def getparams(self):
        Sout=[]
        a=dir(self);
        for i in range(0,len(a)):
          f=eval('self.'+a[i])
          if type(f).__name__=='param':
            Sout+=[a[i]]
            Sout+=[f.Val]
            Sout+=[f.Unit]
            Sout+=[f.Description]
        return Sout
    def getlparams(self):
        Sout=[]
        a=dir(self);
        for i in range(0,len(a)):
          f=eval('self.'+a[i])
          if type(f).__name__=='param':
            Sout+=[a[i]]
            Sout+=[f.Val]
            Sout+=[f.Unit]
            Sout+=[f.Description]
            Sout+=[f.TypeList]
            Sout+=[str(f.List)]
        return Sout
    def getparamsname(self,name):
        Sout=[]
        a=dir(self);
        for i in range(0,len(a)):
          f=eval('self.'+a[i])
          if type(f).__name__=='param':
            Sout+=[name+'.'+a[i],f.Unit]
        return Sout
    def getsignalsname(self,name):
        Sout=[]
        a=dir(self);
        for i in range(0,len(a)):
          f=eval('self.'+a[i])
          if type(f).__name__=='signal':
            Sout+=[name+'.'+a[i]]
            Sout+=[f.Unit]
            Sout+=[f.dir]
        return Sout

    def getsignaldir(self):
        Sout=[]
        a=dir(self);
        for i in range(0,len(a)):
          f=eval('self.'+a[i])
          if type(f).__name__=='signal':
            Sout+=[a[i]]
            Sout+=[f.sys]
            Sout+=[f.dir]
            Sout+=[f.Porta]
            Sout+=[f.Portb]
        return Sout


#-------------------------------------------------------------------------------
# class param: parameter object
#-------------------------------------------------------------------------------

class param (object):
      def __init__(self,Value=0.0, Unit='', Description='',List=[]):
          self.Val=Value
          self.Unit=Unit
          self.Description=Description
          if len(List)==0:
            self.TypeList=False
          else:
            self.TypeList=True
          self.List=List
      def __name__(self):
          return 'param'
      def __Str__(self):
           return floatToStr(self.Val)+self.Unit

      def SetParam(self,Value):
          self.Val=Value
      def __truediv__(self, other):
          if type(other).__name__ in ['signal','param']:
               return self.Val/other.Val
          return self.Val/other
      def __rtruediv__(self, other):
          if type(other).__name__ in ['signal','param']:
               return other.Val/self.Val
          return other/self.Val
      def __add__(self, other):
          if type(other).__name__ in ['signal','param']:
               return self.Val+other.Val
          return self.Val+other
      def __radd__(self, other):
          if type(other).__name__ in ['signal','param']:
               return self.Val+other.Val
          return self.Val+other
      def __sub__(self, other):
          if type(other).__name__ in ['signal','param']:
               return self.Val-other.Val
          return self.Val-other
      def __rsub__(self, other):
          if type(other).__name__ in ['signal','param']:
               return -self.Val+other.Val
          return -self.Val+other
      def __mul__(self, other):
          if type(other).__name__ in ['signal','param']:
               return self.Val*other.Val
          return self.Val*other
      def __rmul__(self, other):
          if type(other).__name__ in ['signal','param']:
               return self.Val*other.Val
          return self.Val*other
      def __rpow__(self, other):
          if type(other).__name__ in ['signal','param']:
               return other.Val**self.Val
          return other**self.Val
      def __pow____(self, other):
          if type(other).__name__ in ['signal','param']:
               return self.Val**other.Val
          return self.Val**other
      def __neg__(self):
          return -self.Val
      def __pos__(self):
          return self.Val
      def __iadd__(self, other):
           if type(other).__name__ in ['signal','param']:
                self.Val=other.Val;
           else:
                self.Val=other;
           return self
      def __lt__(self, other):
          if type(other).__name__ in ['signal','param']:
               return self.Val<other.Val
          return self.Val<other
      def __gt__(self, other):
          if type(other).__name__ in ['signal','param']:
               return self.Val>other.Val
          return self.Val>other
      def __le__(self, other):
          if type(other).__name__ in ['signal','param']:
               return self.Val<=other.Val
          return self.Val<=other
      def __ge__(self, other):
          if type(other).__name__ in ['signal','param']:
               return self.Val>=other.Val
          return self.Val>=other
      def __ne__(self, other):
          if type(other).__name__ in ['signal','param']:
               return self.Val!=other.Val
          return self.Val!=other
      def __eq__(self, other):
          if type(other).__name__ in ['signal','param']:
               return self.Val==other.Val
          return self.Val==other


#-------------------------------------------------------------------------------
# class signal: signal object
#-------------------------------------------------------------------------------

class signal(object):
     def __init__(self,dir_,pf,Porta='0', Portb='0'):
         self.dir=dir_
         self.pf=pf['nature']
         self.Unit='A'
         self.Porta = Porta
         self.Portb = Portb
         self.Indxa = 0
         self.Indxb = 0
         self.value=1.0
         self.Val=0.0
         self.Valo=0.0
         self.ValAC=0.0
         self.pos=0
         self.adr=(0,0)
         self.abstol=pf['abstol']
         self.chgtol=pf['chgtol']
         self.discipline=pf['discipline']
         self.type=pf['signalType']
         self.nature=pf['nature']
         self.Unit=pf['unit']
         self.posImp=[]
         self.p=self.pf=='potential'

         self.I=0.0
         self.sys=False
         self.privat=False
         self.Name=' '

     def __name__(self):
         return 'signal'

     def getValue(self):
        return floatToStr(self.Val)+self.Unit

     def __str__(self):
         return floatToStr(self.Val)+self.Unit

     def __truediv__(self, other):
         if type(other).__name__ in ['signal','param']:
              return self.Val/other.Val
         return self.Val/other
     def __rtruediv__(self, other):
         if type(other).__name__ in ['signal','param']:
              return other.Val/self.Val
         return other/self.Val
     def __add__(self, other):
         if type(other).__name__ in ['signal','param']:
              return self.Val+other.Val
         return self.Val+other
     def __radd__(self, other):
         if type(other).__name__ in ['signal','param']:
              return self.Val+other.Val
         return self.Val+other
     def __sub__(self, other):
         if type(other).__name__ in ['signal','param']:
              return self.Val-other.Val
         return self.Val-other
     def __rsub__(self, other):
         if type(other).__name__ in ['signal','param']:
              return -self.Val+other.Val
         return -self.Val+other
     def __mul__(self, other):
         if type(other).__name__ in ['signal','param']:
              return self.Val*other.Val
         return self.Val*other
     def __rmul__(self, other):
         if type(other).__name__ in ['signal','param']:
              return self.Val*other.Val
         return self.Val*other
     def __neg__(self):
         return -self.Val
     def __pos__(self):
         return self.Val
     def __iadd__(self, other):
          if type(other).__name__ in ['signal','param']:
               self.Val=other.Val;
          else:
                self.Val=other;
          return self
     def __lt__(self, other):
          if type(other).__name__ in ['signal','param']:
               return self.Val<other.Val
          return self.Val<other
     def __gt__(self, other):
          if type(other).__name__ in ['signal','param']:
               return self.Val>other.Val
          return self.Val>other
     def __le__(self, other):
          if type(other).__name__ in ['signal','param']:
               return self.Val<=other.Val
          return self.Val<=other
     def __ge__(self, other):
          if type(other).__name__ in ['signal','param']:
               return self.Val>=other.Val
          return self.Val>=other
     def __ne__(self, other):
          if type(other).__name__ in ['signal','param']:
               return self.Val!=other.Val
          return self.Val!=other
     def __eq__(self, other):
          if type(other).__name__ in ['signal','param']:
               return self.Val==other.Val
          return self.Val==other
     def solved(self):
          return abs(self.Val-self.Valo)<=(self.RealTol*self.Val+self.AbsTol)
     def get_(self):
          return self.Val
     def set_(self,SetVal):
            self.Val=SetVal



#-------------------------------------------------------------------------------
# inf,gnd,version: List of constant
#-------------------------------------------------------------------------------

inf=1.0e+8
gnd='0'
version='0.0.1'


#-------------------------------------------------------------------------------
# time..temp: List of paramatres
#-------------------------------------------------------------------------------

time=param(0.0,'Sec','Time')
freq=param(0.0,'Hz','Freq')
tnom=param(300.0,'K','Temperature')
temp=param(27.0,'°C','Temperature')

temp.name='Temperature'
time.name='Time'
freq.name='Freq'


#-------------------------------------------------------------------------------
#Class analysis: used to convert the netlist or structur of circuit into
#                an array according to the type of analysis.
#-------------------------------------------------------------------------------

class analysis:
      def __init__(self,circuit,method,output=[]):

           self.TR=(method['mode']=='tr') or (method['mode']=='int')
           self.AC=method['mode']=='ac'
           self.DC=(method['mode']=='dc') or (method['mode']=='op')

           self.Stop=0.0
           self.c=circuit
           self.output=output
           self.out=[]
           self.Node=['0']
           self.Lin=[]
           self.Lout=[]
           self.fout=[]
           self.LIV=[]
           self.len=0
           self.x=[]
           self.ListSignal=[]
           self.VectsDesc=[]
           self.SVGElement=[]
           global  List,Val
           List=[]
           Val=[]

           l=len(self.c)
           i=0

           while i<l:
                     d=self.c[i]
                     a=dir(d)
                     if ('sub' in a):
                       r=d.sub()
                       #AddRefToSub(d)
                       if not(len(r)==0):
                         # self.c.remove(self.c[i])
                          for j in range(len(r)):
                              self.c.append(r[j])
                     l=len(self.c)
                     i=i+1

           l=len(self.c)
           i=0
           while i<l:
                #try:
                     d=self.c[i]
                     a=dir(d)
                     if ('start' in a):
                        d.start()
                     i=i+1#except:
                    # i=i+1

           l=len(self.c)
           i=0
           while i < l:
                     d=self.c[i]
                     d.analog()
                     i=i+1


           l=len(self.c)
           i=0
           while i<=l:
                try:
                     d=self.c[i]
                     a=dir(d);
                     if 'output' in a:
                       self.fout.append(d)
                     i=i+1;
                except:
                     i=i+1


           self.List=[]
           self.Val=[]
           self.adr= id(self)/800

           def  addToList(list,val,dir_,pf,a, b='0'):
            #  if not (dir_,pf,a, b) in List:
                list+=[(dir_,pf,a, b)]
                val+=[0]
                return len(list)-1

           for i in range(len(self.c)):
                L=dir(self.c[i])
                for j in range(len(L)):
                     # if L[j]=='__doc__':
                     #      break;
                      f=eval('self.c['+str(i)+'].'+L[j])
                      if type(f).__name__=='signal':
                           f.pos=addToList(self.List,self.Val,f.dir,f.pf,f.Porta,f.Portb)
                           f.adr=(self.adr,f.pos)
                           self.ListSignal+=[f]

                      if type(f).__name__=='SVGElement':
                           self.SVGElement+=[f];
                           a=len(self.SVGElement);
                           self.SVGElement[a-1].namePart=self.c[i].name;
                           self.SVGElement[a-1].id=self.SVGElement[a-1].namePart+'.'+self.SVGElement[a-1].ref


           for i in range(len(self.List)):
                v=self.List[i]
                if not v[2] in self.Node:
                     self.Node+=[v[2]]
                if not v[3] in self.Node:
                     self.Node+=[v[3]]
           for i in range(len(self.List)):
                v=self.List[i]
                if v[0]=='in':
                     self.Lin+=[(v[1]=='potential',self.Node.index(v[2]),self.Node.index(v[3]),i)]
                else:
                     self.Lout+=[(v[1]=='potential',self.Node.index(v[2]),self.Node.index(v[3]),i)]

           for i in range(len(self.Lin)):
                vin=self.Lin[i]
                inList=False
                if not(vin[0]):
                     addlen=len(self.Node)-1
                     for j in range(len(self.Lout)):
                          vout=self.Lout[j]
                          if vout[0]:
                               addlen=addlen+1
                               if (vout[1]==vin[1]) and (vout[2]==vin[2]):
                                    self.Lin[i]=(False,addlen,-1,vin[3])
                                    inList=True
                                    break
                               elif (vout[1]==vin[2]) and (vout[2]==vin[1]):
                                    self.Lin[i]=(False,addlen,1,vin[3])
                                    inList=True
                                    break
                     if not(inList):
                          addlen=addlen+1
                          self.Val+=[0]
                          self.Lout+=[(True,vin[1],vin[2],len(self.Val)-1)]
                          self.Lin[i]=(False,addlen,1,vin[3])



           self.len=len(self.Node)
           self.les=0

           self.nde=self.len
           for i in range(len(self.Lout)):
               v=self.Lout[i]
               if v[0]:
                    self.len+=1
                    self.LIV+=[(self.len-1,v[3])]
                    self.les+=1

           for i in range(self.len):
                self.x+=[0]

           #print ('Numbre of signals:       ',len(self.ListSignal))
           #print ('Numbre of nodes:         ',  self.len-self.les)
           #print ('Numbre of source out:    ',self.les)

           i=0
           l=len(self.c)
           global GetStepTime;
           while i<=l:
                try:
                     d=self.c[i]
                     a=d.period()
                     getStepTime.addPer(a);
                     i=i+1;
                except:
                     i=i+1


      def getoutput_(self,out_):

                 if type(out_)==str:
                    j=self.Node.index(out_)
                    return self.x[j]
                 elif  type(out_).__name__=='signal':
                    return self.Val[out_.pos]
                 elif  type(out_).__name__=='param':
                    return out_.Val
                 else:
                    return 0

      def getunits_(self,out_):
                 if type(out_)==str:
                    j=self.Node.index(out_)
                    return 'V'
                 elif  type(out_).__name__=='signal':
                    return out_.Unit
                 elif  type(out_).__name__=='param':
                    return out_.Unit
                 else:
                    return 0


      def set(self,x):
           x[0]=0;

           for i in range(len(self.LIV)):
                p,s=self.LIV[i]
                if(s<len(self.ListSignal)):
                  #print(p)
                  #print(x[p])
                  self.ListSignal[s].I=x[p]
           for i in range(len(self.Lin)):
               p,n1,n2,v=self.Lin[i]
               if p:
                    self.Val[v]=x[n1]-x[n2]
               else:
                    self.Val[v]=x[n1]
           for i in range(len(self.ListSignal)):
                self.ListSignal[i].Val=self.Val[self.ListSignal[i].pos]

           for i in range(len(self.c)):
               self.c[i].analog()

           for i in range(len(self.ListSignal)):
                self.Val[self.ListSignal[i].pos]=self.ListSignal[i].Val

      def favel(self,x):
           x[0]=0
           self.set(x)
           addlen=len(self.Node)-1
           y=[]
           for i in range(self.len):
                y+=[0]
           for i in range(len(self.Lout)):
               p,n1,n2,k=self.Lout[i]
               v=self.Val[k]
               if p:
                    addlen+=1
                    y[addlen]+=x[n1]-x[n2]-v
                    y[n1]+=x[addlen]
                    y[n2]-=x[addlen]
               else:
                    y[n1]+=v
                    y[n2]-=v


           y[0]=0
           self.x=[];
           self.x+=x;
           return y


      def getoutputl(self):
           Lout=self.output;
           self.out=[]
           for i in range(len(Lout)):
                 if type(Lout[i])==str:
                        j=self.Node.index(Lout[i])
                        self.out+=[self.x[j]]
                 elif type(Lout[i]).__name__=='signal':
                    self.out+=[self.Val[Lout[i].pos]]
                 else:
                    self.out+=[Lout[i]]
           return self.out



      def getunit_(self,out_):

                 if type(out_)==str:
                        return 'Volt'
                 if type(out_)==tuple:
                        return out_[1].Un
                 else:
                        return ' '


      def getoutputPosNS(self):
           self.out=[]
           for i in range(len(self.output)):
                 if type(self.output[i])==str:
                    j=self.Node.index(self.output[i])
                    self.out+=['N:'+str(j)]
                 else:
                    a=self.Node.index(self.output[i].Porta);
                    b=self.Node.index(self.output[i].Portb);
                    self.out+=['S:'+str(self.output[i].pos)+':'+self.output[i].dir+':'+self.output[i].pf+':'+str(a) +':'+str(b)]

      def getListSignal(self):

           self.AllSignal=[]
           for i in range(len(self.c)):
                L=dir(self.c[i])
                lout=[]
                lin=[]
                for j in range(len(L)):
                      if L[j]=='__doc__':
                           break;
                      f=eval('self.c['+str(i)+'].'+L[j])
                      if type(f).__name__=='signal':
                           if f.dir=='out':
                                lout+=[f]
                           else:
                                lin+=[f]
                self.AllSignal+=[[i,lin,lout]]
      def printout(self):
        for i in range(len(self.fout)):
            self.fout[i].output();

      def pageWeb(self,page):
         for i in range(len(self.SVGElement)):
            self.SVGElement[i].page=page;







#--------------------------------------------------------------------------------------------
listNewNode=[]

def newNode():
        NodeName='SN00'
        i=1
        while i>=1:
            if not(NodeName+str(i) in ListNewNode):
                ListNewNode.append(NodeName+str(i))
                return NodeName+str(i)
            i=i+1


#-------------------------------------------------------------------------------
#class getStepTime: used to find step time from models
#-------------------------------------------------------------------------------


class getStepTime:
    def __init__(self):
        self.List=[]
        self.ndivPer=24;
        self.ListTrap=[]
        self.ListTrapPos=[]

    def indexTrap(self,v):
        try:
          i=self.ListTrap.index(v)
          return self.ListTrapPos[i]
        except:
          self.ListTrap+=[v]
          (V2,V1,Td,Tr,Pw,Tf,T)=v
          a=[0.0,Td+0.0,Td+Tr+0.0,Td+Tr+Pw+0.0,Td+Tr+Pw+Tf+0.0,Td+Tr+Pw+Tf+0.0,T+0.0]
          b=[True,True,True,True,True,True,True]
          c=[V1,V1,V2,V2,V1,V1,V1]
          self.List+=[['trap',T+0.0,a,b,c]]
          Pos=len(self.List)-1;
          self.ListTrapPos+=[Pos]
          return Pos

    def addPer(self,Values):
        len_=len(Values)
        for i in range(len_):
         T= Values[i][0]+(Values[i][1]*Values[i][0]/360)
         a=[]
         b=[]
         for r in range(self.ndivPer):
            a+=[r*T/self.ndivPer]
            b+=[True]
         self.List+=[['pr',T,a,b]]

    def  IncPer(self):
        len_=len(self.List)
        for i in range(len_):
            d=self.List[i]
            T=d[1]
            a=d[2]
            b=d[3]
            lenb=len(b)
            R=True
            for r in range(lenb):
                R=R and not(b[r])
            if R:
                for r in range(lenb):
                    a[r]=a[r]+T
                    b[r]=True

    def  GetStepTime(self,MinTime):
        len_=len(self.List)
        for i in range(len_):
            d=self.List[i]
            T=d[1]/(2*self.ndivPer)
            if (MinTime > T) and (T!=0.0):
                MinTime=T
        print ('MinStepTime=',MinTime);
        return MinTime

    def ControlPer(self):
        self.IncPer()
        global time
        TimeVal=0.0
        UsedTime=False;
        ResultPer=(TimeVal,-1,-1)
        len_=len(self.List)
        for i in range(len_):
            d=self.List[i]
            a=d[2]
            b=d[3]
            lenb=len(b)
            for r in range(lenb):
                if b[r]:
                  if time.Val >= a[r]:
                    time.Val = a[r]
                    ResultPer=(a[r],i,r)

        if(ResultPer[1]!=-1):
          UsedTime=True;
          (t,i,r)=ResultPer
          time.Val=t
          d=self.List[i]
          a=d[2]
          b=d[3]
          b[r]=False;
        return UsedTime;

getStepTime=getStepTime()



