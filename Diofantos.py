

def Diofantos(a,b,c,sayEuclid=True):
    L=[a,b]
    C=[]
    while L[-1]!=0:
        C.append(L[-2]//L[-1])
        L.append(L[-2]%L[-1])
        
    def f(isB):
        if isB:
            D=[0,1]
        else:
            D=[1,0]
        for i in range(len(C)):
            D.append(-D[-1]*C[i]+D[-2])
        return D

    cA=f(0)
    cB=f(1)
    syt=L[-2]
    eqStr=str(a)+'x + '+str(b)+'y = '+str(c)
    if c%syt==0:
        x=cA[-2]*c//syt
        y=cB[-2]*c//syt
        xn=cA[-1]
        yn=cB[-1]
        print('Diofantoksen yhtälö '+eqStr+' toteutuu näillä arvoilla:')
        print('x = '+str(x)+' + n * '+str(xn))
        print('y = '+str(y)+' + n * '+str(yn))
    else:
        print('Diofantoksen yhtälöön '+eqStr+ ' ei ole ratkaisua')
    if sayEuclid:
        print()
        print('Euklideen algoritmillä lukujen '+str(a)+' ja '+str(b)+' suurin yhteinen tekijä lasketaan:')
        for i in range(len(C)):
            print(str(L[2+i])+' = '+str(L[i])+' - '+str(C[i])+' * '+str(L[1+i]))
        print('eli suurin yhteinen tekijä on '+str(syt))

Diofantos(400,210,10)
