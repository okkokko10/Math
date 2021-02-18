from math import gcd as Syt

def Superscript(n):
    superscript = str.maketrans('0123456789','⁰¹²³⁴⁵⁶⁷⁸⁹')
    return str(n).translate(superscript)

class Fraction:
    def __init__(self,numerator,denominator=1):
        if isinstance(numerator,Fraction):
            self.numerator=numerator.numerator
            self.denominator=numerator.denominator
        else:
            self.numerator=numerator
            self.denominator=denominator
        self.Simplify()
    def Simplify(self):
        syt=Syt(self.numerator,self.denominator)
        self.numerator//=syt
        self.denominator//=syt
    def __add__(self,other):
        other=Fraction(other)
        return Fraction(self.numerator*other.denominator+other.numerator*self.denominator,self.denominator*other.denominator)
    def __sub__(self,other):
        other=Fraction(other)
        return Fraction(self.numerator*other.denominator-other.numerator*self.denominator,self.denominator*other.denominator)
    def __neg__(self):
        return Fraction(-self.numerator,self.denominator)
    def __mul__(self,other):
        other=Fraction(other)
        return Fraction(self.numerator*other.numerator,self.denominator*other.denominator)
    def __truediv__(self,other):
        other=Fraction(other)
        return Fraction(self.numerator*other.denominator,self.denominator*other.numerator)
    def __eq__(self,other):
        other=Fraction(other)
        return ((self-other).numerator == 0)
    def __str__(self):
        return str(self.numerator)+('/'+str(self.denominator))*(self.denominator!=1)
    def Latex(self,sign=0,coeff=True):
        #sign 0:nothing in front, 1:positive, 2: negative
        s=[['-',''],['-','+'],['+','-']][sign][(self.numerator>0)]
        if self.denominator==1:
            if abs(self.numerator)==1 and coeff:
                return s
            else:
                return s+str(abs(self.numerator))
        else:
            return s+'\\frac{'+str(abs(self.numerator))+'}{'+str(self.denominator)+'}'

class Poly(dict):
    def __init__(self,value=None):
        if not value:
            value={}
        dict.__init__(self,value)
        self.Clean()
    def copy(self):
        return Poly(dict.copy(self))
    def Clean(self):
        for i in self.keys():
            self[i]=Fraction(self[i])
            if self[i]==0:
                del self[i]
    def __add__(self,other):
        out=self.copy()
        for i in other.keys():
            out[i] = out.setdefault(i,Fraction(0)) +other[i]
        out.Clean()
        return out
    def __sub__(self,other):
        out=self.copy()
        for i in other.keys():
            out[i] = out.setdefault(i,Fraction(0)) -other[i]
        out.Clean()
        return out
    def __mul__(self,other):
        out=Poly()
        for x in self.keys():
            for y in other.keys():
                out[x+y] = out.setdefault(x+y,Fraction(0)) + self[x]*other[y]
        out.Clean()
        return out
    def Divide(self,other):
        history=[]
        target = self.copy()
        whole = Poly()
        divExp=max(other.keys())
        divCoeff=Fraction(other[divExp])
        divAux = other.copy()
        del divAux[divExp]
        while max(target.keys())>=divExp:
            mainExp=max(target.keys())
            mainCoeff=Fraction(target[mainExp])
            split = Poly({mainExp-divExp:mainCoeff/divCoeff})
            whole += split
            history.append((target.copy(),Poly({mainExp:mainCoeff}),whole)) 
            del target[mainExp]
            target -= split*divAux
            #last two lines should be equal to   target -= split*other
        history.append((target,Poly(),Poly()))
        return whole,target,history
    def __truediv__(self,other):
        return self.Divide(other)
    def __str__(self):
        out=''
        for i in sorted(self.keys(),reverse=True):
            coeff=self[i]
            out += (coeff.numerator>0)*'+'+str(coeff) + (i>0)*'x' + (i>1)*Superscript(i)
        return out
    def Latex(self):
        out=''
        for i in sorted(self.keys(),reverse=True):
            coeff=self[i]
            out += coeff.Latex((out!=''),(i>0)) + (i>0)*'x' + (i>1)*('^{'+str(i)+'}')
        return out
def ReadHistory(history,dividend,divisor):
    divExp=max(divisor.keys())
    divCoeff=Fraction(divisor[divExp])
    div =Poly({divExp:divCoeff})
    middle='&:\\left('+divisor.Latex()+'\\right)&'
    out='\\begin{array}{l|l}'
    for i in range(len(history)):
        current=history[i]
        target=history[i][0]
        main=history[i][1]
        whole=history[i-1][2]
        left =  target.Latex()
        removed=' -\\frac{'+main.Latex()+'}{'+div.Latex()+'} \\left('+divisor.Latex() +'\\right)'
        right=  whole.Latex()
        added= '+\\frac{'+main.Latex()+'}{'+div.Latex()+'}'
        out+=left+middle+right
        middle='&&'
        if i<len(history)-1:
            out +='\\\\'+left+removed+middle+right+added+'\\\\'
    
    out+='\\end{array}'
    return out

a=Poly({1:4,4:2,0:-3})
b=Poly({2:5,1:4,0:5})
c=a/b
# print('...')
# print(a)
# print(b)
# print(c[0])
# print(c[1])
# print(',,,')
print(ReadHistory(c[2],a,b))