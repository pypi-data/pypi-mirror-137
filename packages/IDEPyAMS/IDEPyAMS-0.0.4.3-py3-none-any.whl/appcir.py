#-------------------------------------------------------------------------------
# Name:        convert schema of circuit to PyAMS netlist
# Author:      d.fathi
# Created:     17/09/2021
# Copyright:   (c) PyAMS 2021-2022
# Licence:
#-------------------------------------------------------------------------------

global usedtest;
global svgout;
usedtest=True;
'''
def itNet(net):
    a=net.split(".")
    if a[0]=='net':
        return '"'+a[1]+'"'
    return net
'''

#-------------------------------------------------------------------------------
# def pyamscircuit: convert schema of circuit to PyAMS netlist
#-------------------------------------------------------------------------------
def pyamscircuit(result,getdata):
    netList=result[3]
    option=str(result[4]);

    data=[]
    data=['from sys import path;'];
    data+=['path+=["lib/analysis"];'];

    elems=[];

    for i in range(len(netList)):
        s='path+=["symbols/'+netList[i]['directory']+'"];'
        if not(s in data):
            data+=[s];

    libs=['from PyAMS import strToFloat;']
    libs+=['from simu import AppPyAMS;']
    cir=[];
    parms=[];

    for i in range(len(netList)):
        pins='","'.join(netList[i]['pins']);
        pins='("'+pins+'");';

        elems+=[netList[i]['ref']+'='+netList[i]['modelname']+pins]
        cir+=['"'+netList[i]['ref']+'":'+netList[i]['ref']]

        s='from '+netList[i]['modelname']+' import '+netList[i]['modelname'];
        if not(s in libs):
            libs+=[s]

        p=netList[i]['params'];
        for k in range(len(p)):
            x = p[k].split('=');
            parms+=[netList[i]['ref']+'.'+x[0]+'+='+'strToFloat("'+x[1]+'");'];


    if(getdata):
       temp=result[0];
       probe=','.join(temp);
    else:
       temp=result[1];
       probe=','.join(temp);




    data+=[];
    data+=[];
    data+=["#------------------------------------------------------------------"];
    for i in range(len(libs)):
        data+=[libs[i]]

    data+=[];
    data+=[];
    data+=["#------------------------------------------------------------------"];
    for i in range(len(elems)):
        data+=[elems[i]]

    data+=["#------------------------------------------------------------------"];
    for i in range(len(parms)):
        data+=[parms[i]]

    data+=[];
    data+=[];
    data+=["#------------------------------------------------------------------"];


    data+=['AppPyAMS.setOption('+option+')'];
    data+=['AppPyAMS.setOut('+probe+')'];
    data+=['AppPyAMS.circuit({'+','.join(cir)+'});'];
    return data





#-------------------------------------------------------------------------------
# def opAnalysis: operating Point Analysis
#-------------------------------------------------------------------------------

def opAnalysis(self,result):
    data=pyamscircuit(result,True);
    data+=['AppPyAMS.analysis(mode="op",start=0.0,stop=0.1,step=0.1);'];
    data+=['AppPyAMS.run(True);'];


    file = open("test.py", "w", encoding="utf-8")
    for element in data:
        file.write(element + "\n")
    file.close();
    from sys import path;
    import importlib
    path+=["lib\\"];

    L='global test;import test; ';
    no_error=True;
    global usedtest;
    try:
       if usedtest:
        exec(L);
       else:
        importlib.reload(test);
       usedtest=False;
    except Exception as e: # work on python 3.x
       str_error='Error: '+ str(e);
       no_error=False;


    if  no_error:
      a=str(test.AppPyAMS.getOut());
      self.ui.m_webview.page().runJavaScript("ioSetProbeValue("+a+");");
    else:
      self.message('Error',str_error);


#-------------------------------------------------------------------------------
# def trAnalysis: transite Analysis
#-------------------------------------------------------------------------------

def tranAnalysis(self,result):
    data=pyamscircuit(result,False);
    data+=['AppPyAMS.analysis(mode="tran",start=0.0,stop=1e+1000,step=1.0);'];
    data+=['AppPyAMS.run(False);'];


    file = open("test.py", "w", encoding="utf-8")
    for element in data:
        file.write(element + "\n")
    file.close();
    from sys import path;
    import importlib
    path+=["lib\\"];

    L='global test;import test;';
    no_error=True;
    global usedtest;
    try:
       if usedtest:
        exec(L);
       else:
        importlib.reload(test);
       usedtest=False;
    except Exception as e: # work on python 3.x
       str_error='Error: '+ str(e);
       no_error=False;


    if  no_error:
      a=str(test.AppPyAMS.getUnit());
      self.ui.m_webview.page().runJavaScript("ioStartInter("+a+");");
      test.AppPyAMS.setPageWeb(self.ui.m_webview.page());
    else:
      self.message('Error',str_error);

def interAnalysis(l,win):
    test.AppPyAMS.update();
    win.lbl3.setText('Time='+test.AppPyAMS.getTime());
    return  test.AppPyAMS.getDataPlot()




#-------------------------------------------------------------------------------
# def getListSignalsNodeParams: get list of signals from symboles in circuit.
#-------------------------------------------------------------------------------

def getListSignalsNodeParams(self,result):
    data=pyamscircuit(result,False);
    n=len(data)
    data[n-2]='';

    file = open("test.py", "w", encoding="utf-8")
    for element in data:
        file.write(element + "\n")
    file.close();
    from sys import path;
    import importlib
    path+=["lib\\"];

    L='global test;import test; ';
    global usedtest;
    if usedtest:
      exec(L);
    else:
      importlib.reload(test);
    usedtest=False;

    id=1;
    data=[{'unique_id': 1, 'parent_id': 0, 'short_name': '', 'type': ' ', 'description': ' '}];
    v=list(test.AppPyAMS.elements.values())
    k=list(test.AppPyAMS.elements.keys())


    net=result[2]


    id=id+1;
    r=id;
    data += [{'unique_id': id, 'parent_id': 1, 'short_name': 'Wire', 'type': ' ', 'description': ' '}]
    for j in range(len(net)):
          id=id+1;
          data += [{'unique_id': id, 'parent_id': r, 'short_name':net[j]+'.V', 'type': 'wire', 'description': ''}]



    for i in range(len(v)):
       signals=v[i].getSignals();
       params=v[i].getParamaters();
       id=id+1;
       r=id
       data += [{'unique_id': id, 'parent_id': 1, 'short_name': k[i], 'type': ' ', 'description': ' '}]
       for j in range(len(signals)):
          id=id+1;
          data += [{'unique_id': id, 'parent_id': r, 'short_name': signals[j].name, 'type': 'signal', 'description': signals[j].type, 'dir': signals[j].dir}]
       for j in range(len(params)):
          id=id+1;
          data += [{'unique_id': id, 'parent_id': r, 'short_name': params[j].name, 'type': 'paramater', 'description': ''}]
    return data;

