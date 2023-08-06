#-------------------------------------------------------------------------------
# Name:        Signals types (voltage and current)
# Author:      d.Fathi
# Created:     31/03/2020
# Modified:    19/09/2021
# Copyright:   (c) PyAMS 2020
# Licence:     unlicense
#-------------------------------------------------------------------------------




voltage={'discipline':'electrical',
         'nature':'potential',
         'abstol': 1e-8,
         'chgtol':1e-14,
         'signalType':'voltage',
         'unit':'V'
         }



current={'discipline':'electrical',
         'nature':'flow',
         'abstol': 1e-8,
         'chgtol':1e-14,
         'signalType':'current',
         'unit':'A'
         }


electrical={
            'potential':voltage,
            'flow':current
            }

