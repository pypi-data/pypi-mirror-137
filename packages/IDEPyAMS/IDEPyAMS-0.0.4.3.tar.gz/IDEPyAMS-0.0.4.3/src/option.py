#-------------------------------------------------------------------------------
# Name:        simulation options
# Author:      d.fathi
# Created:     20/03/2015
# Update:      29/12/2021
# Copyright:   (c) pyams 2022
# Web:         www.PyAMS.org
# Licence:     free
# info:        initial conditions of simulation
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# class simulationOption: pyams simulation options
#-------------------------------------------------------------------------------



class simulationOption(object):
    def __init__(self):
        self.reltol=1e-3    #"Relative accuracy of V's and I's    (RELTOL)"
        self.vntol=1e-6    #'Volts',"Best accuracy of voltages    (VNTOL)"
        self.abstol=1e-8   #'Amps',"Best accuracy of currents    (ABSTOL)"
        self.itl1=200
        self.CHGTOL=1e-14
        self.ITL4=40
        self.RELTOL=1.0e-3
        self.MaxiNumbPnt=900000
        self.MInteg=1
        self.MSolve=1
        self.ITLC=60
        self.len=0
        self.les=0
        self.ldt=0
        self.niter=0
        self.nStep=0
        self.Run=True
        self.MethodIntegration='BR'
        self.Trapezoidal=True
        self.t1=0.0;
        self.t0=0.0;
        self.start=True
        self.SegnalUsedSameTime=False
        self.TimeStep=1.2;
        self.GetStep=0.0;
        self.SaveSignalsInData=True;
    def setOption(self,option):
        #Get Option of simulation

        if 'reltol' in option:
            self.reltol=option['reltol'];
           # print('reltol =',self.reltol)

        if 'vntol' in option:
            self.vntol=option['vntol'];
            #print('vntol =',self.vntol)

        if 'abstol' in option:
            self.abstol=option['abstol'];
            #print('abstol =',self.abstol)

        if 'itl1' in option:
            self.itl1=option['itl1'];
            #print('ITL1 =',self.itl1)



    def Result(self):
        print('numbre of iteration: ',self.niter)
        print('numbre of step: ',self.nStep)
    def SetTimeStep(self,T):
        self.TimeStep=T;
        self.TimeStepMax=T;

simulationOption=simulationOption()

'''
if UniteToValeur(Edit_Step.Text) <= 0 then
  ListOfErrors.Add('[Error] E6004:TR Statmet error "Step time" must be positive');

if UniteToValeur(Edit_Stop.Text) <= 0 then
  ListOfErrors.Add('[Error] E6005:TR Statmet error "Stop time" must be positive');

if UniteToValeur(Edit_Step.Text) > UniteToValeur(Edit_Stop.Text) then
  ListOfErrors.Add('[Error] E6006:TR Statmet error "Stop time" must be greater than "Step time"');

if abstol <=0  then
  ListOfErrors.Add('[Error] E6007:TR Statmet error "AbsToL" must be positive');

if reltol <=0  then
  ListOfErrors.Add('[Error] E6008:TR Statmet error "RelToL" must be positive');

if ChgTol <=0  then
  ListOfErrors.Add('[Error] E6009:TR Statmet error "ChgToL" must be positive');

if TrTol <=0  then
  ListOfErrors.Add('[Error] E6009:TR Statmet error "TrToL" must be positive');

if Vntol <=0  then
  ListOfErrors.Add('[Error] E6010:TR Statmet error "VnToL" must be positive');

if ITL1 <=0  then
  ListOfErrors.Add('[Error] E6011:TR Statmet error "ITL1" must be positive');

if ITL2 <=0  then
  ListOfErrors.Add('[Error] E6012:TR Statmet error "ITL2" must be positive');

if ITL2 > ITL1 then
  ListOfErrors.Add('[Error] E6013:TR Statmet error "ITL1" must be greater than "ITL2"');

if ITL3 <=0  then
  ListOfErrors.Add('[Error] E6014:TR Statmet error "ITL3" must be positive');

if ITL4 <=0  then
  ListOfErrors.Add('[Error] E6015:TR Statmet error "ITL4" must be positive');

if ITL3 > ITL4 then
  ListOfErrors.Add('[Error] E6016:TR Statmet error "ITL4" must be greater than "ITL3"');
'''