#-------------------------------------------------------------------------------
# Name:        armijo
# Author:      d.fathi
# Created:     01/03/2015
# Update:      04/10/2021
# Copyright:   (c) pyams 2021
# Web:         www.PyAMS.org
# Licence:     unlicense
# info:        line search by armijo method
#-------------------------------------------------------------------------------


from math import fabs,sqrt;


#-------------------------------------------------------------------------------
# def norm: the norm of a vector
#-------------------------------------------------------------------------------
def norm(x):
    try:
      return sqrt(sum(i**2 for i in x))
    except:
      #print x
      return sqrt(1e+6)


#-------------------------------------------------------------------------------
# def parab3p: Apply three-point safeguarded parabolic model for a line search
#-------------------------------------------------------------------------------
def parab3p(lambdac, lambdam, ff0, ffc, ffm):
    sigma0 = 0.1;
    sigma1 = 0.9;
    c2= lambdam*(ffc-ff0)-lambdac*(ffm-ff0);
    if c2 >= 0:
        return sigma1*lambdac;
    c1 = (lambdac*lambdac*(ffm-ff0))-(lambdam*lambdam*(ffc-ff0));
    a= -c1*0.5/c2;
    if (a < sigma0*lambdac):
        a= sigma0*lambdac;
    if(a > sigma1*lambdac):
        a= sigma1*lambdac;
    return a;

#-------------------------------------------------------------------------------
# def armijo: line search by armijo method
#-------------------------------------------------------------------------------
def armijo(direction,x,f0,maxarm,f):
    n=len(x);
    iarm = 0;
    sigma1= 0.8;
    alpha= 1.0e-12;
    armflag= 0;
    x[0]=0.0
    direction[0]=0.0
    xp=[];
    xp+=x;
    xold=[];
    xold+=x;
    xt= [0 for i in range(n)];
    lamb=0.4;
    lamm=1.0;
    lamc=lamb;

    for i in range(0,n):
        xt[i]= x[i]-lamb*direction[i];
    ft= f(xt);
    nft = norm(ft);
    nf0 = norm(f0);
    ff0 = nf0*nf0;
    ffc = nft*nft;
    ffm = nft*nft;
    maxarm=40;
    while nft>= ((1-alpha*lamb)*nf0):
        xold=[];
        xold+=xt;
        fp=[]
        fp+=ft;
        lamb=0.5*lamb
        '''
        if iarm ==0:
          lamb = sigma1*lamb;
        else:
          lamb = parab3p(lamc, lamm, ff0, ffc, ffm);
        '''
        for i in range(0,n):
              xt[i]= x[i] -lamb*direction[i];

        lamm = lamc;
        lamc = lamb;
        # Keep the books on the function norms.
        ft= f(xt);
        nft= norm(ft);
        ffm = ffc;
        ffc = nft*nft;
        iarm= iarm+1;
        if (iarm > maxarm):
            armflag= 1;
            x=[]
            x+=xold;
            f0=[]
            f0+=fp;
            return x;
    x=[]
    x += xt;
    f0=[]
    f0 += ft;
    return x;
