# -*- coding: utf-8 -*-
"""
ELS 1-asset by Monte Carlo simulation 

@author: Minhyun Yoo
"""
import time
import numpy as np
from math import exp, sqrt, ceil

S0 = 100.0; # underlying price
E = 100.0; # strike price
T = 3.0; # maturity
r = 0.0165; # riskless interest rate
discr = 0.0165; # discount rate
sig = 0.3; # volatility
ns = 10000;  # # of simulations
dateConv = 360; # 1 year
nStep = int(dateConv * T); # # of time steps

Kib = 60.0;
cpy = 0.025;
dummy = cpy*T;
face = 10000.0;
B = [95, 90, 85, 80, 75, 70];
numExercise = len(B);
obsDate = np.array([ceil(nStep / numExercise), ceil(2.0*nStep/numExercise), ceil(3.0*nStep/numExercise),
           ceil(4.0*nStep / numExercise), ceil(5.0*nStep / numExercise), ceil(nStep)]);
payment = face*(1.0+np.array([cpy*0.5, cpy*1.0, cpy*1.5, cpy*2.0, cpy*2.5, cpy*3.0]));

# functions call
dt = T / nStep;
t0 = time.clock();

sumPayoff = 0.0;
idx = np.zeros(numExercise);

drift = (r - 0.5*sig**2)*dt;
sigsqdt = sig*sqrt(dt);

for i in xrange(ns):
    s = S0; kievent = False; tag = False;
    cnt1 = 0; cnt2 = 0;
    payoff = 0.0; idx[:] = 0.0;
    
    z = np.random.normal(size = [nStep]);
    for j in xrange(nStep):
        s = s * exp(drift + sigsqdt*z[j]);
        
        kievent = True if s < Kib else kievent;
        
        if ((j+1) == obsDate[cnt1]):
            idx[cnt1] = s;
            cnt1 += 1;
            
    for k in xrange(numExercise):
        if (idx[k] >= B[k]):
            payoff = payment[k];
            tag = True;
            cnt2 = k;
            break;
            
    if (tag == False):
        payoff = 100.0 * s;
        if (kievent == False):
            if (s >= Kib):
                payoff = face * (1.0 + dummy);
    sumPayoff += payoff * exp(-discr * obsDate[cnt2] / dateConv);   

    
els1 = sumPayoff / ns;
t1 = time.clock();
del z;
    
print 'Monte Carlo Call Price : %.5f' % els1
print 'CPU time in Python(sec) : %.4f' % (t1-t0)