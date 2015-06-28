class onephaseregulator(object):
    def __init__(self):
        self.frnode=[-2,-2]
        self.tonode=[-2,-2]
        self.rcomp=1.46
        self.xcomp=2.84
        self.tap=0.0
        self.tap0=0.0
        self.ar=1+0.00625*float(self.tap)#default step up
        self.kre=0.0#integer tap
        self.kim=0.0#the imagine part of voltage turns ratio
        self.frnodename=['','']
        self.tonodename=['','']
        self.branchid=[-1,-1]
        self.ct=1000.0/5.0
        self.pt=2400.0/120.0
        self.bandwidth=2.0
        self.voltagelevel=120.0
        
        
