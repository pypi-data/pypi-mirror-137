from math import acos,cos,sin,pi,floor,ceil
class Complexe:

    def __init__(self,Re,Im):
        assert type(Re)==type(0) or type(Re)==type(0.0), "La partie réel doit etre un nombre!"
        assert type(Im)==type(0) or type(Im)==type(0.0), "La partie imaginaire doit etre un nombre!"
        self.partieRe=Re
        self.partieIm=Im

    def getRe(self):
        return self.partieRe

    def getIm(self):
        return self.partieIm

    def conj(self):
        return Complexe(self.getRe(),-self.getIm())

    def ad(self,comp):
        #assert type(comp)==type(Complexe(0,0))
        return Complexe(self.getRe()+comp.getRe(),self.getIm()+comp.getIm())

    def sous(self,comp):
        return Complexe(self.getRe()-comp.getRe(),self.getIm()-comp.getIm())

    def mult(self,comp):
        return Complexe((self.getRe()*comp.getRe())-(self.getIm()*comp.getIm()),(self.getRe()*comp.getIm())+(self.getIm()*comp.getRe()))

    def div(self,comp):
        return Complexe(self.mult(comp.conj()).getRe()/(comp.getRe()**2+comp.getIm()**2),self.mult(comp.conj()).getIm()/(comp.getRe()**2+comp.getIm()**2))

    def puiss(self,n):

        m=n%1
        if m!=0:
            m=1/m
            if m>int(m)+0.5:
                m=int(ceil(m))
            else:
                m=int(floor(m))

        n=int(n)
        l=[]
        z=Complexe(1,0)

        if n>0:
            for i in range(n):
                z=z.mult(self)

            if m!=0:
                for i in self.racine(m):
                    l.append(z.mult(i))
                return l
            return [z]

        elif n<0:
            for i in self.puiss(abs(n)):
                l.append(z.div(i))
        else:
            return [z]
        return l

    def racine(self,n):
        assert n!=0, "racine 0 d'un nombre, indéterminé"
        m=n%1
        if m!=0:
            m=1/m
        if m>int(m)+0.5:
            m=int(ceil(m))
        else:
            m=int(floor(m))

        z=Complexe(1,0)
        l=[]
        arg=self.getArgument()**(1/n)
        mod=self.getModule()


        if n>0:
            r=self.puiss(m)
            for i in range(int(n)):
                l.append(Complexe(arg*cos((mod+2*pi*i)/int(n)),arg*sin((mod+2*pi*i)/int(n))))
            for i in range(len(l)):
                l[i]=l[i].mult(r[0])
        elif n<0:
            r=self.racine(abs(int(n)))
            for i in range(len(r)):
                l.append(z.div(r[i]))

        return l

    def getArgument(self):
        return (self.getRe()**2+self.getIm()**2)**(1/2)

    def getModule(self):
        return (acos(self.getRe()/self.getArgument()))

    def __str__(self):
        return str(self.getRe())+"+("+str(self.getIm())+")i"

    def __repr__(self) -> str:
        return self.__str__()

if __name__ == "__main__":
    a=Complexe(1,0)
    z=a.racine(2.5)
    print(z)
    l=[]
    for i in z:
        l.append(i.puiss(2.5))
    print(l)
