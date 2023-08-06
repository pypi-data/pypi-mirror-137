from sys import path;
path+=["lib/analysis"];
path+=["symbols/basic"];
path+=["symbols/source"];
#------------------------------------------------------------------
from PyAMS import strToFloat;
from simu import AppPyAMS;
from Resistor import Resistor
from SinVoltage import SinVoltage
#------------------------------------------------------------------
R1=Resistor("Vin","Vout");
R2=Resistor("Vout","0");
V1=SinVoltage("Vin","0");
#------------------------------------------------------------------
R1.R+=strToFloat("100Ω ");
R2.R+=strToFloat("100Ω ");
V1.Va+=strToFloat("10V");
V1.Fr+=strToFloat("100Hz");
#------------------------------------------------------------------
AppPyAMS.setOption({'abstol': 1e-25, 'interval': 400, 'itl1': 250, 'reltol': 0.001, 'vntol': 1e-06})
AppPyAMS.setOut("Vout","Vin")
AppPyAMS.circuit({"R1":R1,"R2":R2,"V1":V1});
AppPyAMS.analysis(mode="tran",start=0.0,stop=1e+1000,step=1.0);
AppPyAMS.run(False);
