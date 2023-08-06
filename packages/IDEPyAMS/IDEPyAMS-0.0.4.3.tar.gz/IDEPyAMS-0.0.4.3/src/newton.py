#-------------------------------------------------------------------------------
# Name:        newton
# Author:      d.fathi
# Created:     01/03/2015
# Update:      04/10/2021
# Copyright:   (c) pyams
# Web:         www.PyAMS.org
# Licence:     free
# info:        solving systems of nonlinear equations newton raphson method
#-------------------------------------------------------------------------------

from math import fabs,sqrt;
from armijo import armijo
from option import simulationOption


#-------------------------------------------------------------------------------
# def norm: the norm of a vector
#-------------------------------------------------------------------------------

def norm(x):
    return sqrt(sum(i**2 for i in x))


#-------------------------------------------------------------------------------
# def solve_LU: solving a system with an LU-Factorization
#-------------------------------------------------------------------------------
def solve_LU(at,bt):
    n= len(bt);
    a= [[0 for j in range(n)] for i in range(n)];
    b= [0 for i in range(n)];
    v= [0 for i in range(n)];
    indx = [0 for i in range(n)];
    d = 1;
    tiny = 1e-20;
    imax=0;

    for i in range(0,n):
        for j in range(0,n):
            a[i][j] =at[i][j];
        b[i] =bt[i];

    for  i in  range(1,n):
         big = 0.0;
         for  j in  range(1,n):
             temp = abs(a[i][j]);
             if (temp > big):
                 big = temp;
         if (big != 0.0):
            v[i] = 1.0 / big;
         else:
            v[i] = 100000000.0;

    for  j in  range(1,n):
        for  i in  range(1,j):
             sum_ = a[i][j];
             for  k in  range(0,i):
                sum_ = sum_ - (a[i][k]*a[k][j]);
             a[i][j] = sum_;

        big = 0.0;
        for  i in  range(j,n):
         sum_ = a[i][j];
         for  k in  range(1,j):
                sum_ = sum_ - (a[i][k] * a[k][j]);
         a[i][j] = sum_;
         dum = v[i] * abs(sum_);
         if (dum >= big):
             big = dum;
             imax = i;
        if (j != imax):
            for  k in  range(1,n):
                dum = a[imax][k];
                a[imax][k] = a[j][k];
                a[j][k] =dum;
            d = -d;
            v[imax] = v[j];

        indx[j] = imax;

        if (a[j][j]== 0.0):
            a[j][j] = tiny;

        if (j != n):
            dum =1.0/a[j][j];
            for  i in  range(j+1,n):
                a[i][j] = a[i][j] * dum;

    ii = 0;
    for  i in  range(1,n):
        ip = indx[i];
        sum_ = b[ip];
        b[ip] = b[i];
        if (ii != 0):
            for  j in  range(ii,i):
                sum_ = sum_ -a[i][j]*b[j];
        else:
            if (sum_ !=0.0):
                ii = i;
        b[i]=sum_;

    i=n-1;
    while (i >= 1):
        sum_ = b[i];
        for  j in  range(i+1,n):
             sum_ = sum_ - a[i][j]*b[j];
        if (a[i][i] != 0.0):
             b[i]=sum_/a[i][i];
        else:
             b[i]=sum_/tiny;
        i=i-1;
    return b;



#-------------------------------------------------------------------------------
# def jac: Jacobian matrix
#-------------------------------------------------------------------------------
def jac(x,f):
    n= len(x);
    delta=1e-8;

    J= [[0 for j in range(n)] for i in range(n)];
    f2= [0 for i in range(n)];
    f3= [0 for i in range(n)];
    for i in range(1,n):
        tmp= x[i];
        x[i]= tmp+delta;
        f2=f(x);
        x[i]= tmp-delta;
        f3=f(x);
        x[i]= tmp;
        for k in range(1,n):
          J[k][i]=(f2[k]-f3[k])/(2*delta);
    return J


#-------------------------------------------------------------------------------
# def convergence: convergence systems of nonlinear equations
#-------------------------------------------------------------------------------
def convergence(xo,x,y):
    a=len(x)
    r=True
    if (len(xo)!=len(x)):
        return False
    else:
        for i in range(a):
            if (i <= simulationOption.len):
              r=r and (abs(xo[i]-x[i])<=(simulationOption.reltol*max(abs(xo[i]),abs(x[i]))+simulationOption.vntol))
            elif (i <= simulationOption.len+simulationOption.les):
              r=r and (abs(xo[i]-x[i])<=(simulationOption.reltol*max(abs(xo[i]),abs(x[i]))+simulationOption.abstol))
    r=r and (abs(sum(y(x)))<1e-10)
    return r


#-------------------------------------------------------------------------------
# def solven: solving systems of nonlinear equations by newton raphson method
#-------------------------------------------------------------------------------
def solven(x,y):
 ii=0;
 xo=[]
 while(not(convergence(xo,x,y))):
      xo=[]
      xo+=x
      J=jac(x,y);

      F=y(x);
      dx=solve_LU(J,F);##
      n=len(x);
      ii=ii+1;

      x=armijo(dx,x,F,simulationOption.ITLC,y);
      if ii > simulationOption.itl1:
          print('Error of convergence: ',ii,':',fabs(sum(y(x))))
          return x,False
 return x,True;

