class onephasetrfm(object):
    def __init__(self):
        self.frnode=[-2,-2]
        self.tonode=[-2,-2]
        self.g=0.0#the impedance behind the voltage turns ratio
        self.b=0.0
        self.kre=0.0#the real part of voltage turns ratio
        self.kim=0.0#the imagine part of voltage turns ratio
        self.frnodename=['','']
        self.tonodename=['','']
        self.branchid=[-1,-1]
